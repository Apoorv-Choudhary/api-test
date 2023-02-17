"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Payment creation

This script also cleans up the data created in pre-script.
"""
from utility.payment_ledger_utility import get_local_citation_data
from env.logging_interface import logging
from env.session_manager import current_session


def validate_create_citation(db_name):
    test_prefix = "test_case_5:"
    data_to_validate = current_session.get_variable("test_case_5")

    for data in data_to_validate:
        ticket_num = data["ticket_num"]

        db_rows = get_local_citation_data(db_name=db_name,
                                          ticket_num=ticket_num,
                                          select_cols=["ticket_status", "balance"])
        db_ticket_status = db_rows[0]["ticket_status"]

        db_balance = float(db_rows[0]["balance"] if db_rows[0]["balance"] is not None else 0)

        if db_ticket_status.lower() == "closed" and db_balance == 0:
            logging.write(True,
                          f"""{test_prefix} {ticket_num}'s passed for payment creation.""")
        else:
            logging.write(False,
                          f"{test_prefix} {ticket_num}'s payment creation didn't happen properly.")


def main(*args):
    db_name = args[0][0]
    validate_create_citation(db_name)

    test_data = current_session.get_variable("test_case_5")
    ticket_numbers = tuple(i["ticket_num"] for i in test_data)

    cleanup_fun = current_session.get_variable("cleanup_citation_data")
    tables_to_cleanup = ["local_citation", "local_citation_statuses",
                         "citation_edit_logs", "payment_ledger"]
    cleanup_fun(db_name, ticket_numbers, tables_to_cleanup)
    ticket_numbers = tuple(f'|{i["ticket_num"]}|' for i in test_data)
    cleanup_fun(db_name, ticket_numbers, ["local_payment"])
