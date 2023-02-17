"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Citation Voiding
"""
from datetime import datetime
from utility.citation_utility import create_citation, void_citation
from env.session_manager import current_session
import random, json


def citation_creation(start_num, end_num):
    ticket_num_prefix = "L000"
    test_data = []

    for i in range(start_num, end_num + 1):
        ticket_num = f"{ticket_num_prefix}{i}"
        fine = random.randrange(start=150, stop=300, step=10)
        data = {"ticket_num": ticket_num, "fine": fine,
                "violation_code": "420.01",
                "violation_description": "No State Plates",
                "hearing_date": datetime.now().date()}
        create_citation(data)
        void_citation(ticket_num=ticket_num, ticket_type="local")
        test_data.append({"ticket_num": data["ticket_num"]})

    current_session.add_variable("test_case_7", test_data)


def main(*args):
    citation_creation(13, 14)
