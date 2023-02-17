"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Payment creation (consider as full)
"""
from datetime import datetime
from utility.citation_utility import create_citation
from utility.payment_utility import make_payment
from env.session_manager import current_session
import random, json


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
        paid_amount = random.randrange(start=100, stop=fine-10, step=5)
        payment_dict = {"ticket_num": ticket_num, "payment_amount": paid_amount,
                        "payment_type": "cash", "check_number": "",
                        "payee_name": "andrew williams",
                        "payee_address": "from mars",
                        "balance": fine,
                        "consider_as_full": "T",
                        "consider_as_full_reason": ""}
        payment_data = {"payment": json.dumps(payment_dict), "ticket_type": "local", "fine": data["fine"],
                        "override_balance": "T", "payment_date": datetime.now().date()}
        print(f"====making a partial payment of {paid_amount} for the fine of {fine}")
        make_payment(payment_data=payment_data)

        test_data.append({"ticket_num": data["ticket_num"]})

    current_session.add_variable("test_case_6", test_data)


def main(*args):
    citation_creation(11, 12)
