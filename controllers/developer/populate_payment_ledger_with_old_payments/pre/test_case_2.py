"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Citation Edit
"""
from datetime import datetime
from utility.citation_utility import create_citation, edit_citation
from env.session_manager import current_session
import random


def citation_creation(start_num, end_num):
    ticket_num_prefix = "L000"
    test_data = []

    for i in range(start_num, end_num + 1):
        ticket_num = f"{ticket_num_prefix}{i}"
        data = {"ticket_num": ticket_num, "fine": 100,
                "violation_code": "2.03",
                "violation_description": "PARK DISTRICT: UNATTENDED MOTORIZED VEHICLE (AHE)",
                "hearing_date": datetime.now().date()}
        create_citation(data)

        new_fine = random.randrange(start=20, stop=300, step=5)
        if new_fine == 100:
            new_fine += 10
        citation_edit(ticket_num, new_fine)

        test_data.append({"ticket_num": data["ticket_num"], "old_fine": data["fine"], "new_fine": new_fine})

    current_session.add_variable("test_case_2", test_data)


def citation_edit(ticket_num, new_fine):
    data = {"ticket_num": ticket_num, "fine": new_fine}
    edit_citation(data)


def main(*args):
    citation_creation(3, 4)
