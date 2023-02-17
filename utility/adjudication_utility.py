import requests
from env.session_manager import current_session
from utility.auth_utility import get_auth_token

json_parser_obj = current_session.get_variable("_json_parser_obj")
domain = json_parser_obj.domain
client_name = json_parser_obj.client_name
url_prefix = f"{domain}/{client_name}"
default_url = f"{url_prefix}/adjudication_new/default_remaining_citations"
adjudication_url = f"{url_prefix}/adjudication_new/submit_adjudication_result"


def default_citations(hearing_date: str, hearing_time: str = "09:00"):
    """

    :param hearing_date: hearing date of the court. date format must be "YYYY-MM-DD"
    :param hearing_time: hearing time of the court. this is an optional field
    :return:
    """

    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()
    params = {"hearing_date": hearing_date, "hearing_time": hearing_time}
    response = requests.post(url=default_url, params=params, headers=headers, verify=False)
    print("====default_citations", response.text)

    return


def adjudicate_citation(adjudication_data: dict):
    """

    :param adjudication_data: for eg: {"ticket_id": "L0001",
                         "adjudication_result": "liable", "next_adjudication_date": "2022-09-20",
                         "next_adjudication_time": None, "service_hours": None,
                         "additional_note": None, "latest_fine": 250, "court_fee": 0,
                         "program_option": None, "program_description": None,
                         "complied": false, "due_date": 2022-10-21, "program_date": None}
        * next adjudication date (in future) must be defined in adj_table_date table in database
    :return:
    """
    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url=adjudication_url, params=adjudication_data, headers=headers, verify=False)
    print("====adjudicate_citation", response.text, "====citation data", adjudication_data)

    return
