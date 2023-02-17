"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Payment creation
- Payment voiding
- Adjudication

This script also cleans up the data created in pre-script.
"""
from utility.payment_ledger_utility import (get_local_citation_data,
                                            fetch_data_from_payment_ledger,
                                            get_citation_related_data)
from env.logging_interface import logging
from env.session_manager import current_session


def validate_create_citation(db_name):
    test_prefix = "test_case_29:"
    data_to_validate = current_session.get_variable("test_case_29")

    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        issued_fine = data["issued_fine"]

        paid_amount = data["paid_amount"]

        adjudicated_fine = data["adjudicated_fine"]
        court_fee = data["court_fee"]
        due_date = data["due_date"]

        db_rows = get_local_citation_data(db_name=db_name,
                                          ticket_num=ticket_num,
                                          select_cols=["ticket_status", "fine",
                                                       "balance", "due_date"])
        db_ticket_status = db_rows[0]["ticket_status"]
        db_due_date = db_rows[0]["due_date"]
        if db_due_date:
            db_due_date = db_due_date.strftime("%Y-%m-%d")
        db_fine = float(db_rows[0]["fine"] if db_rows[0]["fine"] is not None else 0)
        db_balance = float(db_rows[0]["balance"] if db_rows[0]["balance"] is not None else 0)

        if (db_ticket_status.lower() == "open"
                and db_fine == adjudicated_fine
                and db_balance == (adjudicated_fine + court_fee)
                and db_due_date == due_date):
            logging.write(True,
                          f"{test_prefix} {ticket_num}'s passed for citation creation "
                          f"and adjudication.")
        else:
            logging.write(False,
                          f"citation creation or adjudication for {test_prefix} {ticket_num} "
                          f"didn't happen properly.")

        db_rows = fetch_data_from_payment_ledger(db_name=db_name, ticket_num=ticket_num)

        if len(db_rows) == 5:
            for id_, row in enumerate(db_rows):
                db_pos_fine = float(row["positive_adjustment"] if row["positive_adjustment"] is not None else 0)
                db_neg_fine = float(row["negative_adjustment"] if row["negative_adjustment"] is not None else 0)
                db_category = row["category"]
                if id_ == 0 and not (db_pos_fine == issued_fine
                                     and db_category == "fine"
                                     and db_neg_fine == 0):
                    logging.write(False,
                                  f"{test_prefix} {ticket_num}'s actual fine issued "
                                  f"was not properly recorded by back-population in payment ledger.")
                    break
                elif id_ == 1 and not (db_neg_fine == paid_amount
                                       and db_category == "payment"
                                       and db_pos_fine == 0):
                    logging.write(False,
                                  f"{test_prefix} {ticket_num}'s paid amount "
                                  f"was not properly recorded by back-population in payment ledger.")
                    break
                elif id_ == 2 and not (db_neg_fine == issued_fine
                                       and db_category == "fine_reversal"
                                       and db_pos_fine == 0):
                    logging.write(False,
                                  f"{test_prefix} {ticket_num}'s actual fine issued "
                                  f"was not properly reversed by back-population in payment ledger.")
                    break
                elif id_ == 3 and not (db_pos_fine == adjudicated_fine
                                       and db_category == "fine"
                                       and db_neg_fine == 0):
                    logging.write(False,
                                  f"{test_prefix} {ticket_num}'s adjudicated fine issued "
                                  f"was not properly recorded by back-population in payment ledger.")
                    break
                elif id_ == 4 and not (db_pos_fine == court_fee
                                       and db_category == "court_fee"
                                       and db_neg_fine == 0):
                    logging.write(False,
                                  f"{test_prefix} {ticket_num}'s court fee issued "
                                  f"was not properly recorded by back-population in payment ledger.")
                    break
            else:
                logging.write(True, f"payment ledger has properly recorded entries "
                                    f"for {test_prefix} {ticket_num}'s citation "
                                    f"creation, payment and adjudication.")

        else:
            logging.write(False, f"{test_prefix} {ticket_num} gave more/less rows than expected")

        db_rows = get_citation_related_data(db_name=db_name, ticket_num=ticket_num,
                                            select_cols=["payment_amount", "void"],
                                            table_name="local_payment")
        db_payment_amount = float(db_rows[0]["payment_amount"]
                                  if db_rows[0]["payment_amount"] is not None else 0)
        db_void = db_rows[0]["void"]

        if (db_payment_amount == paid_amount
                and db_void.lower() == "t"):
            logging.write(True, f"payment was successfully voided "
                                f"for {test_prefix} {ticket_num}'s ")
        else:
            logging.write(False, f"payment voiding failed for {test_prefix} {ticket_num}'s ")


def main(*args):
    db_name = args[0][0]
    validate_create_citation(db_name)

    test_data = current_session.get_variable("test_case_29")
    ticket_numbers = tuple(i["ticket_num"] for i in test_data)

    cleanup_fun = current_session.get_variable("cleanup_citation_data")
    tables_to_cleanup = ["local_citation", "local_citation_statuses",
                         "citation_edit_logs", "payment_ledger",
                         "local_payment", "adjudication_table"]
    cleanup_fun(db_name, ticket_numbers, tables_to_cleanup)

