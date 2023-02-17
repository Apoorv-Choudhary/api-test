"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Citation Voiding

This script also cleans up the data created in pre-script.
"""
from utility.payment_ledger_utility import get_local_citation_data
from env.logging_interface import logging
from env.session_manager import current_session


def validate_create_citation(db_name):
    test_prefix = "test_case_7:"
    data_to_validate = current_session.get_variable("test_case_7")

    for data in data_to_validate:
        ticket_num = data["ticket_num"]

        db_rows = get_local_citation_data(db_name=db_name,
                                          ticket_num=ticket_num,
                                          select_cols=["ticket_status", "void_status"])
        db_ticket_status = db_rows[0]["ticket_status"]
        db_void_status = db_rows[0]["void_status"]

        if db_ticket_status.lower() == "closed" and db_void_status.lower() == "y":
            logging.write(True,
                          f"""{test_prefix} {ticket_num}'s passed for citation voiding.""")
        else:
            logging.write(False,
                          f"{test_prefix} {ticket_num}'s voiding didn't happen properly.")


def main(*args):
    db_name = args[0][0]
    validate_create_citation(db_name)

    test_data = current_session.get_variable("test_case_7")
    ticket_numbers = tuple(i["ticket_num"] for i in test_data)

    cleanup_fun = current_session.get_variable("cleanup_citation_data")
    tables_to_cleanup = ["local_citation", "local_citation_statuses",
                         "citation_edit_logs", "void_request"]
    cleanup_fun(db_name, ticket_numbers, tables_to_cleanup)
