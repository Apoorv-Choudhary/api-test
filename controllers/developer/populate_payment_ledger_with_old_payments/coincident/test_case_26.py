"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Adjudication
- Payment Creation (Consider as full)
"""
from datetime import datetime, timedelta
from utility.adjudication_utility import adjudicate_citation
from utility.payment_utility import make_payment2
from env.session_manager import current_session
import random

test_prefix = "coincident/test_case_26:"


def adjudicate_citations():
    data_to_validate = current_session.get_variable("test_case_26")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        issued_fine = data["issued_fine"]
        new_fine = random.randrange(start=issued_fine-100, stop=issued_fine+100, step=10)
        if new_fine == issued_fine:
            new_fine += 10
        next_adjudication_date = data.get("next_adjudication_date")
        if not next_adjudication_date:
            next_adjudication_date = datetime.now().date()
        else:
            next_adjudication_date = datetime.strptime(next_adjudication_date, "%Y-%m-%d")
        next_adjudication_date = (next_adjudication_date + timedelta(days=15)).strftime("%Y-%m-%d")
        data["next_adjudication_date"] = next_adjudication_date
        due_date = (datetime.strptime(next_adjudication_date, "%Y-%m-%d") +
                    timedelta(days=15)).strftime("%Y-%m-%d")
        court_fee = 0
        ad_data = {"ticket_id": ticket_num,
                   "adjudication_result": "liable", "next_adjudication_date": next_adjudication_date,
                   "next_adjudication_time": None, "service_hours": None,
                   "additional_note": None, "latest_fine": new_fine, "court_fee": court_fee,
                   "program_option": None, "program_description": None,
                   "complied": False, "due_date": due_date, "program_date": None}
        adjudicate_citation(adjudication_data=ad_data)
        data["adjudicated_fine"] = new_fine
        data["due_date"] = due_date
        data["court_fee"] = court_fee
    current_session.update_variable("test_case_26", data_to_validate)


def payment_creation():
    data_to_validate = current_session.get_variable("test_case_26")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        issued_fine = data["adjudicated_fine"]
        paid_amount = random.randrange(start=issued_fine-50, stop=issued_fine, step=10)
        remaining_amount = issued_fine-paid_amount
        payment_data = {"citation_type": "local", "payee_address": "from mars",
                        "payee_name": "andrew williams", "received_by": "Test User",
                        "payment_amount": paid_amount,
                        "payment_without_service_fee": paid_amount,
                        "payment_type": "cash", "ticket_number": ticket_num,
                        "check_number": "", "consider_as_full": "T",
                        "consider_as_full_reason": "",
                        "consider_as_full_adjustment": remaining_amount,
                        "restitution_balance": 0,
                        "payment_date": datetime.now().date().strftime("%d/%m/%Y")}
        data["paid_amount"] = paid_amount
        data["remaining_amount"] = remaining_amount
        make_payment2(payment_data=payment_data)
    current_session.update_variable("test_case_26", data_to_validate)


def main(*args):

    adjudicate_citations()
    payment_creation()

