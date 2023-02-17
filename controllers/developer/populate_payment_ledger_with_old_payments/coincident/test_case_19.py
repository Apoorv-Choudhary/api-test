"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Escalation
- Adjudication
"""
from datetime import datetime, timedelta
from utility.escalation_utility import escalate_citations
from utility.adjudication_utility import adjudicate_citation
from env.session_manager import current_session
import random

test_prefix = "coincident/test_case_19:"


def escalate_citation():

    process_date = (datetime.today() + timedelta(days=11)).strftime("%d-%m-%Y")
    escalate_citations(process_date=process_date)


def adjudicate_citations():
    data_to_validate = current_session.get_variable("test_case_19")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        issued_fine = data["issued_fine"]
        new_fine = random.randrange(start=issued_fine-100, stop=issued_fine+100, step=10)
        if new_fine == issued_fine:
            new_fine += 10
        next_adjudication_date = (datetime.now().date() + timedelta(days=15)).strftime("%Y-%m-%d")
        due_date = (datetime.now().date() + timedelta(days=30)).strftime("%Y-%m-%d")
        court_fee = random.randrange(start=0, stop=30, step=5)
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
    current_session.update_variable("test_case_19", data_to_validate)


def main(*args):

    escalate_citation()
    adjudicate_citations()

