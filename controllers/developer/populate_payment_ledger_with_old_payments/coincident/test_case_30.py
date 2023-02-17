"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Payment creation
- Payment voiding
- Payment creation
"""
from datetime import datetime, timedelta
from utility.payment_utility import make_payment2, void_payment
from utility.payment_ledger_utility import get_citation_related_data
from env.session_manager import current_session
import random

test_prefix = "coincident/test_case_30:"


def payment_creation(multi_run=""):
    data_to_validate = current_session.get_variable("test_case_30")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        issued_fine = data["issued_fine"]
        remaining_amount = data.get("remaining_amount")
        if remaining_amount:
            paid_amount = random.randrange(start=5, stop=remaining_amount, step=5)
        else:
            paid_amount = random.randrange(start=issued_fine-50, stop=issued_fine-5, step=10)

        remaining_amount = issued_fine-paid_amount
        payment_data = {"citation_type": "local", "payee_address": "from mars",
                        "payee_name": "andrew williams", "received_by": "Test User",
                        "payment_amount": paid_amount,
                        "payment_without_service_fee": paid_amount,
                        "payment_type": "cash", "ticket_number": ticket_num,
                        "check_number": "", "consider_as_full": "F",
                        "consider_as_full_reason": "",
                        "consider_as_full_adjustment": remaining_amount,
                        "restitution_balance": 0,
                        "payment_date": datetime.now().date().strftime("%d/%m/%Y")}
        data[f"paid_amount{multi_run}"] = paid_amount
        data[f"remaining_amount{multi_run}"] = remaining_amount
        make_payment2(payment_data=payment_data)
    current_session.update_variable("test_case_30", data_to_validate)


def payment_voiding(db_name):
    data_to_validate = current_session.get_variable("test_case_30")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        db_rows = get_citation_related_data(db_name=db_name, ticket_num=ticket_num,
                                            select_cols=["id"], table_name="local_payment")
        if len(db_rows) == 0:
            continue
        payment_row_id = db_rows[0]["id"]
        print(f"===={test_prefix} payment_row_id:{payment_row_id}")
        void_payment(_id=payment_row_id, citation_type="local",
                     description="testing", nsf="N")


def main(*args):

    db_name = args[0][0]
    payment_creation()
    payment_voiding(db_name=db_name)
    payment_creation(multi_run="1")


