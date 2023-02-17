"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
"""
from datetime import datetime
from utility.citation_utility import create_citation, edit_citation
from env.session_manager import current_session


def citation_creation(start_num, end_num):
    ticket_num_prefix = "L000"
    test_data = []

    for i in range(start_num, end_num + 1):
        data = {"ticket_num": f"{ticket_num_prefix}{i}", "fine": 100,
                "violation_code": "2.03",
                "violation_description": "PARK DISTRICT: UNATTENDED MOTORIZED VEHICLE (AHE)",
                "hearing_date": datetime.now().date()}
        create_citation(data)
        test_data.append({"ticket_num": data["ticket_num"], "fine": data["fine"]})

    current_session.add_variable("test_case_1", test_data)


def main(*args):
    citation_creation(1, 2)
