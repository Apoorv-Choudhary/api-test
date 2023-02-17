"""
This test script is to test payment ledger back-population for following Scenario:
- Citation Creation
- Citation Edit
- Citation Voiding
"""

from utility.citation_utility import edit_citation, void_citation
from env.session_manager import current_session
import random, json

test_prefix = "coincident/test_case_8:"


def editing_citation():
    data_to_validate = current_session.get_variable("test_case_8")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        new_fine = random.randrange(start=150, stop=300, step=10)
        data_dict = {"ticket_num": ticket_num, "fine": new_fine}
        edit_citation(data_dict)
        data["new_fine"] = new_fine
    current_session.update_variable("test_case_8", data_to_validate)


def citation_voiding():
    data_to_validate = current_session.get_variable("test_case_8")
    for data in data_to_validate:
        ticket_num = data["ticket_num"]
        ticket_type = "local"
        void_citation(ticket_num=ticket_num, ticket_type=ticket_type, void_description="abcd")


def main(*args):

    editing_citation()
    citation_voiding()

