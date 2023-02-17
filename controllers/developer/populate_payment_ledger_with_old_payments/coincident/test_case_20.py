"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Escalation
- Payment Creation
"""
from datetime import datetime, timedelta
from utility.escalation_utility import escalate_citations
from utility.payment_utility import make_payment2
from env.session_manager import current_session
import random

test_prefix = "coincident/test_case_20:"


def escalate_citation():

    process_date = (datetime.today() + timedelta(days=11)).strftime("%d-%m-%Y")
    escalate_citations(process_date=process_date)


def payment_creation():
    data_to_validate = current_session.get_variable("test_case_20")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        issued_fine = data["escalated_fine"]
        paid_amount = random.randrange(start=issued_fine-50, stop=issued_fine, step=10)
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
        data["paid_amount"] = paid_amount
        data["remaining_amount"] = remaining_amount
        make_payment2(payment_data=payment_data)
    current_session.update_variable("test_case_20", data_to_validate)


def main(*args):

    escalate_citation()
    payment_creation()

