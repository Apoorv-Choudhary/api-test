from datetime import datetime, timedelta
from utility.citation_utility import create_citation, edit_citation, void_citation


def main(*args):
    data = {"ticket_num": "L0002",  "fine": 100, "hearing_date": datetime.now().date() + timedelta(days=2)}
    create_citation([data])
    data = {"ticket_num": "L0002", "fine": 150, "hearing_date": datetime.now().date() + timedelta(days=2)}
    edit_citation([data])
    data = {"ticket_num": "L0002", "ticket_type": "local"}
    void_citation(data)
