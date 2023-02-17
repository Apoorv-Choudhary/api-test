"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation

This script also cleans up the data created in pre-script.
"""
from utility.payment_ledger_utility import fetch_data_from_payment_ledger
from env.logging_interface import logging
from env.session_manager import current_session
from env.db_interface import DBConnection


def validate_create_citation():
    test_prefix = "test_case_1:"
    data_to_validate = current_session.get_variable("test_case_1")

    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        fine = data["fine"]
        db_rows = fetch_data_from_payment_ledger("berwyn_test", ticket_num)
        if len(db_rows) == 1:
            db_fine = db_rows[0]["positive_adjustment"]
            if db_fine == fine:
                logging.write(True, f"{test_prefix} {ticket_num} passed.")
            else:
                logging.write(False,
                              f"""{test_prefix} {ticket_num}'s fine in payment ledger doesn't match with the actual fine issued.""")
        else:
            logging.write(False, f"{test_prefix} {ticket_num} gave more/less rows than expected")


def cleanup_citation_data(db_name: str, ticket_numbers: tuple, tables: list):
    disable_foreign_key_check = "set foreign_key_checks = 0;"
    enable_foreign_key_check = "set foreign_key_checks = 1;"

    with DBConnection(db_name) as (db_cur, db_con):
        db_cur.execute(disable_foreign_key_check)

        for table in tables:
            delete_query = f"""Delete From {db_name}.{table}
                        where {"ticket_number" 
                            if table.lower() in ["payment_ledger", "citation_edit_logs"] 
                            else "ticket_num"} 
                        in {ticket_numbers} and id > 0;
                    """
            db_cur.execute(delete_query)

        db_cur.execute(enable_foreign_key_check)
        db_con.commit()


def main(*args):
    print(f"====args: {args}")
    validate_create_citation()
    test_data = current_session.get_variable("test_case_1")
    ticket_numbers = tuple(i["ticket_num"] for i in test_data)
    tables_to_cleanup = ["local_citation", "local_citation_statuses", "payment_ledger"]

    db_name = args[0][0]
    cleanup_citation_data(db_name, ticket_numbers, tables_to_cleanup)

    current_session.add_variable("cleanup_citation_data", cleanup_citation_data)
