"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Payment Creation
- Citation Voiding

This script also cleans up the data created in pre-script.
"""
from utility.payment_ledger_utility import get_local_citation_data, fetch_data_from_payment_ledger
from env.logging_interface import logging
from env.session_manager import current_session


def validate_create_citation(db_name):
    test_prefix = "test_case_11:"
    data_to_validate = current_session.get_variable("test_case_11")

    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        issued_fine = data["issued_fine"]
        paid_amount = data["paid_amount"]
        db_rows = get_local_citation_data(db_name=db_name,
                                          ticket_num=ticket_num,
                                          select_cols=["ticket_status", "payment_status"])
        db_ticket_status = db_rows[0]["ticket_status"]
        db_payment_status = db_rows[0]["payment_status"]

        if (db_ticket_status.lower() == "closed"
                and db_payment_status.lower() == "paid by cash"):
            logging.write(True,
                          f"{test_prefix} {ticket_num}'s passed for payment creation "
                          f"and citation voiding.")
        else:
            logging.write(False,
                          f"{test_prefix} {ticket_num}'s payment or voiding didn't happen properly.")

        db_rows = fetch_data_from_payment_ledger(db_name=db_name, ticket_num=ticket_num)

        if len(db_rows) == 2:
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
            else:
                logging.write(True, f"{test_prefix} {ticket_num} passed.")

        else:
            logging.write(False, f"{test_prefix} {ticket_num} gave more/less rows than expected")


def main(*args):
    db_name = args[0][0]
    validate_create_citation(db_name)

    test_data = current_session.get_variable("test_case_11")
    ticket_numbers = tuple(i["ticket_num"] for i in test_data)

    cleanup_fun = current_session.get_variable("cleanup_citation_data")
    tables_to_cleanup = ["local_citation", "local_citation_statuses",
                         "citation_edit_logs", "payment_ledger",
                         "local_payment", "void_request"]
    cleanup_fun(db_name, ticket_numbers, tables_to_cleanup)

