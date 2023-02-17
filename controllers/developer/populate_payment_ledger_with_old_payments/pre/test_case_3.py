"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Escalation
"""
from datetime import datetime, timedelta
from utility.citation_utility import create_citation
from utility.escalation_utility import escalate_citations
from env.session_manager import current_session


def citation_creation(start_num, end_num):
    ticket_num_prefix = "L000"
    test_data = []

    for i in range(start_num, end_num + 1):
        ticket_num = f"{ticket_num_prefix}{i}"
        data = {"ticket_num": ticket_num, "fine": 25,
                "violation_code": "420.01",
                "violation_description": "No State Plates",
                "hearing_date": datetime.now().date()}
        create_citation(data)

        test_data.append({"ticket_num": data["ticket_num"],
                          "issued_fine": data["fine"],
                          "escalated_fine": 75})

    current_session.add_variable("test_case_3", test_data)


def main(*args):
    citation_creation(5, 6)
    process_date = (datetime.today() + timedelta(days=11)).strftime("%d-%m-%Y")
    print(f"====process_date:{process_date} for escalation in pre/test_case_3")
    escalate_citations(process_date=process_date)
