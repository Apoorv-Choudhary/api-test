"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Escalation
- Citation Voiding
"""
from datetime import datetime, timedelta
from env.session_manager import current_session
from utility.citation_utility import void_citation
from utility.escalation_utility import escalate_citations


def escalate_citation():

    process_date = (datetime.today() + timedelta(days=11)).strftime("%d-%m-%Y")
    escalate_citations(process_date=process_date)


def citation_voiding():
    data_to_validate = current_session.get_variable("test_case_9")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        ticket_type = "local"
        void_citation(ticket_num=ticket_num, ticket_type=ticket_type, void_description="abcd")


def main(*args):

    escalate_citation()
    citation_voiding()

