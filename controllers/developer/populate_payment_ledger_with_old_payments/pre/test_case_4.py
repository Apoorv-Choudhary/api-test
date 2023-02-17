"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Adjudication
"""
from datetime import datetime, timedelta
from utility.citation_utility import create_citation
from utility.adjudication_utility import adjudicate_citation
from env.session_manager import current_session
import random


def citation_creation(start_num, end_num):
    ticket_num_prefix = "L000"
    test_data = []

    for i in range(start_num, end_num + 1):
        ticket_num = f"{ticket_num_prefix}{i}"
        data = {"ticket_num": ticket_num, "fine": 100,
                "violation_code": "420.01",
                "violation_description": "No State Plates",
                "hearing_date": datetime.now().date()}
        create_citation(data)

        new_fine = random.randrange(start=20, stop=300, step=5)
        if new_fine == 100:
            new_fine += 10
        print(f"adjudicating new fine of {new_fine} for {ticket_num}")
        next_adjudication_date = (datetime.now().date() + timedelta(days=15)).strftime("%Y-%m-%d")
        due_date = (datetime.now().date() + timedelta(days=30)).strftime("%Y-%m-%d")
        ad_data = {"ticket_id": ticket_num,
                   "adjudication_result": "liable", "next_adjudication_date": next_adjudication_date,
                   "next_adjudication_time": None, "service_hours": None,
                   "additional_note": None, "latest_fine": new_fine, "court_fee": 0,
                   "program_option": None, "program_description": None,
                   "complied": False, "due_date": due_date, "program_date": None}
        adjudicate_citation(adjudication_data=ad_data)

        test_data.append({"ticket_num": data["ticket_num"],
                          "issued_fine": data["fine"],
                          "adjudicated_fine": new_fine,
                          "due_date": due_date})

    current_session.add_variable("test_case_4", test_data)


def main(*args):
    citation_creation(7, 8)
