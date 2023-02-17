"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Payment Creation (Consider as full)
- Payment Voiding
- Escalation
"""
import json
from datetime import datetime
from utility.citation_utility import create_citation
from env.session_manager import current_session
import random

from utility.payment_ledger_utility import get_citation_related_data
from utility.payment_utility import make_payment, void_payment2


def citation_creation(start_num, end_num):
    ticket_num_prefix = "L000"
    test_data = []

    for i in range(start_num, end_num + 1):
        ticket_num = f"{ticket_num_prefix}{i}"
        fine = random.randrange(start=150, stop=300, step=10)
        data = {"ticket_num": ticket_num, "fine": fine,
                "violation_code": "420.01",
                "violation_description": "No State Plates",
                "hearing_date": datetime.now().date()}
        create_citation(data)
        test_data.append({"ticket_num": data["ticket_num"],
                          "issued_fine": fine,
                          "escalated_fine": 75})

    current_session.add_variable("test_case_32", test_data)


def payment_creation():
    data_to_validate = current_session.get_variable("test_case_32")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        issued_fine = data["issued_fine"]
        paid_amount = random.randrange(start=issued_fine-50, stop=issued_fine, step=10)
        remaining_amount = issued_fine-paid_amount
        payment_dict = {"ticket_num": ticket_num, "payment_amount": paid_amount,
                        "payment_type": "cash", "check_number": "",
                        "payee_name": "andrew williams",
                        "payee_address": "from mars",
                        "balance": issued_fine,
                        "consider_as_full": "T",
                        "consider_as_full_reason": ""}
        payment_data = {"payment": json.dumps(payment_dict), "ticket_type": "local", "fine": issued_fine,
                        "override_balance": "F", "payment_date": datetime.now().date()}
        data["paid_amount"] = paid_amount
        data["remaining_amount"] = remaining_amount
        make_payment(payment_data=payment_data)
    current_session.update_variable("test_case_32", data_to_validate)


def payment_voiding(db_name):
    data_to_validate = current_session.get_variable("test_case_32")
    test_prefix = "pre/test_case_32:"
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        db_rows = get_citation_related_data(db_name=db_name, ticket_num=ticket_num,
                                            select_cols=["id"], table_name="local_payment")
        payment_row_id = db_rows[0]["id"]
        print(f"===={test_prefix} payment_row_id:{payment_row_id}")
        void_payment2(_id=payment_row_id, citation_type="local",
                     description="testing", nsf="N")


def main(*args):
    citation_creation(630, 640)
    payment_creation()
    db_name = args[0][0]
    payment_voiding(db_name=db_name)
