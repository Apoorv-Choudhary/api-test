"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Escalation

This script also cleans up the data created in pre-script.
"""
from utility.payment_ledger_utility import fetch_data_from_payment_ledger, get_local_citation_data
from env.logging_interface import logging
from env.session_manager import current_session
from env.db_interface import DBConnection


def validate_create_citation(db_name):
    test_prefix = "test_case_3:"
    data_to_validate = current_session.get_variable("test_case_3")

    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        old_fine = data["issued_fine"]
        new_fine = data["escalated_fine"]
        db_rows = fetch_data_from_payment_ledger("berwyn_test", ticket_num)
        if len(db_rows) == 1:
            row = db_rows[0]
            db_pos_fine = float(row["positive_adjustment"] if row["positive_adjustment"] is not None else 0)
            db_neg_fine = float(row["negative_adjustment"] if row["negative_adjustment"] is not None else 0)
            db_category = row["category"]
            if db_pos_fine == new_fine and db_category == "fine" and db_neg_fine == 0:
                logging.write(True,
                              f"""{test_prefix} {ticket_num}'s passed.""")
            else:
                logging.write(False,
                              f"{test_prefix} {ticket_num}'s escalated fine "
                              f"was not properly recorded by back-population in payment ledger.")

        else:
            logging.write(False, f"{test_prefix} {ticket_num} gave more/less rows than expected")

        db_rows = get_local_citation_data(db_name=db_name,
                                          ticket_num=ticket_num,
                                          select_cols=["ticket_status", "fine"])
        db_ticket_status = db_rows[0]["ticket_status"]
        db_fine = float(db_rows[0]["fine"] if db_rows[0]["fine"] is not None else 0)
        if db_ticket_status.lower() == "1st notice" and db_fine == new_fine:
            logging.write(True,
                          f"""{test_prefix} {ticket_num}'s passed for escalation.""")
        else:
            logging.write(False,
                          f"{test_prefix} {ticket_num}'s escalation didn't happen properly.")


def main(*args):
    db_name = args[0][0]
    validate_create_citation(db_name)

    test_data = current_session.get_variable("test_case_3")
    ticket_numbers = tuple(i["ticket_num"] for i in test_data)

    cleanup_fun = current_session.get_variable("cleanup_citation_data")
    tables_to_cleanup = ["local_citation", "local_citation_statuses", "citation_edit_logs", "payment_ledger"]

    cleanup_fun(db_name, ticket_numbers, tables_to_cleanup)
