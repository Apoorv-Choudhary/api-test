"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Adjudication
- Adjudication
"""
from datetime import datetime, timedelta
from utility.adjudication_utility import adjudicate_citation
from env.session_manager import current_session
import random

test_prefix = "coincident/test_case_24:"


def adjudicate_citations(multi_run=""):
    data_to_validate = current_session.get_variable("test_case_24")
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
        court_fee = random.randrange(start=0, stop=30, step=5)
        ad_data = {"ticket_id": ticket_num,
                   "adjudication_result": "liable", "next_adjudication_date": next_adjudication_date,
                   "next_adjudication_time": None, "service_hours": None,
                   "additional_note": None, "latest_fine": new_fine, "court_fee": court_fee,
                   "program_option": None, "program_description": None,
                   "complied": False, "due_date": due_date, "program_date": None}
        adjudicate_citation(adjudication_data=ad_data)
        data[f"adjudicated_fine{multi_run}"] = new_fine
        data[f"due_date{multi_run}"] = due_date
        data[f"court_fee{multi_run}"] = court_fee
    current_session.update_variable("test_case_24", data_to_validate)


def main(*args):

    adjudicate_citations()
    adjudicate_citations(multi_run="1")

