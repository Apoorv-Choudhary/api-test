"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Citation Edit

This script also cleans up the data created in pre-script.
"""
from utility.payment_ledger_utility import fetch_data_from_payment_ledger
from env.logging_interface import logging
from env.session_manager import current_session
from env.db_interface import DBConnection


def validate_create_citation():
    test_prefix = "test_case_2:"
    data_to_validate = current_session.get_variable("test_case_2")

    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        new_fine = data["new_fine"]
        db_rows = fetch_data_from_payment_ledger("berwyn_test", ticket_num)
        if len(db_rows) == 1:
            row = db_rows[0]
            db_pos_fine = float(row["positive_adjustment"] if row["positive_adjustment"] is not None else 0)
            db_neg_fine = float(row["negative_adjustment"] if row["negative_adjustment"] is not None else 0)
            db_category = row["category"]
            if db_pos_fine == new_fine and db_category == "fine" and db_neg_fine == 0:
                logging.write(True, f"{test_prefix} {ticket_num} passed.")
            else:
                logging.write(False,
                              f"{test_prefix} {ticket_num}'s new fine issued was not "
                              f"properly recorded by back-population in payment ledger.")
        else:
            logging.write(False, f"{test_prefix} {ticket_num} gave more/less rows than expected")


def cleanup_citation_data(db_name):
    test_data = current_session.get_variable("test_case_2")
    ticket_numbers = tuple(i["ticket_num"] for i in test_data)
    disable_foreign_key_check = "set foreign_key_checks = 0;"
    delete_local_citation_query = f"""Delete From {db_name}.local_citation
                        where ticket_num in {ticket_numbers} and id > 0;
                    """
    delete_citation_status_query = f"""Delete From {db_name}.local_citation_statuses
                            where ticket_num in {ticket_numbers} and id > 0;
                        """
    delete_citation_edit_logs_query = f"""Delete From {db_name}.citation_edit_logs
                                where ticket_number in {ticket_numbers} and id > 0;
                            """
    delete_payment_ledger_query = f"""Delete From {db_name}.payment_ledger
                                where ticket_number in {ticket_numbers} and id > 0;
                            """
    enable_foreign_key_check = "set foreign_key_checks = 1;"

    with DBConnection(db_name) as (db_cur, db_con):
        db_cur.execute(disable_foreign_key_check)
        db_cur.execute(delete_local_citation_query)
        db_cur.execute(delete_citation_status_query)
        db_cur.execute(delete_citation_edit_logs_query)
        db_cur.execute(delete_payment_ledger_query)
        db_cur.execute(enable_foreign_key_check)
        db_con.commit()


def main(*args):
    validate_create_citation()

    test_data = current_session.get_variable("test_case_2")
    ticket_numbers = tuple(i["ticket_num"] for i in test_data)

    cleanup_fun = current_session.get_variable("cleanup_citation_data")
    tables_to_cleanup = ["local_citation", "local_citation_statuses", "citation_edit_logs", "payment_ledger"]

    db_name = args[0][0]
    cleanup_fun(db_name, ticket_numbers, tables_to_cleanup)
