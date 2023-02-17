"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Escalation
- Citation Edit
"""
from datetime import datetime, timedelta
from utility.escalation_utility import escalate_citations
from utility.citation_utility import edit_citation
from env.session_manager import current_session
import random

test_prefix = "coincident/test_case_18:"


def escalate_citation():

    process_date = (datetime.today() + timedelta(days=11)).strftime("%d-%m-%Y")
    escalate_citations(process_date=process_date)


def editing_citation():
    data_to_validate = current_session.get_variable("test_case_18")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        new_fine = random.randrange(start=150, stop=300, step=10)
        data_dict = {"ticket_num": ticket_num, "fine": new_fine}
        edit_citation(data_dict)
        data["new_fine"] = new_fine
    current_session.update_variable("test_case_18", data_to_validate)


def main(*args):

    escalate_citation()
    editing_citation()

