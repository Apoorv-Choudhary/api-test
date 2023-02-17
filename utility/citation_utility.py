import requests
from env.session_manager import current_session
from utility.auth_utility import get_auth_token

json_parser_obj = current_session.get_variable("_json_parser_obj")
domain = json_parser_obj.domain
client_name = json_parser_obj.client_name
url_prefix = f"{domain}/{client_name}"
url = f"{url_prefix}/v2_3/local"
void_request_url = f"{url_prefix}/data/make_void_request"
void_approval_url = f"{url_prefix}/home/viewed_void_notification"


def create_citation(citation_data: dict):
    """

    :param citation_data: for eg: {"ticket_num": "L0002",  "fine": 100,
    "hearing_date": datetime.now().date() + timedelta(days=2)}
        *   ticket_num key is a must and minimum requirement.
    :return:
    """

    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url=url, params=citation_data, headers=headers, verify=False)
    print("====create_citation", response.text, "=====citation_data", citation_data)

    return


def edit_citation(citation_data: dict):
    """

    :param citation_data: for eg: {"ticket_num": "L0002",  "fine": 100,
    "hearing_date": datetime.now().date() + timedelta(days=2)}
        *   ticket_num key is a must and minimum requirement.
    :return:
    """

    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()
    response = requests.put(url=url, params=citation_data, headers=headers, verify=False)
    print("====edit_citation", response.text, "=====citation_data", citation_data)

    return


def void_citation(ticket_num: str, ticket_type: str, void_description: str):
    """

    :param ticket_num: ticket number of the citation.
    :param ticket_type: ticket type of the citation.
    :param void_description: reason for voiding citation
        *   both of the field are required.
    :return:
    """
    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()

    void_citation_data = {"citation_id": ticket_num, "table": ticket_type, "description": void_description}
    response = requests.post(url=void_request_url, params=void_citation_data, headers=headers, verify=False)

    void_approval_url_with_args = f"{void_approval_url}/{ticket_num}/{ticket_type}/yes"
    response = requests.post(url=void_approval_url_with_args, headers=headers, verify=False)
    print("====void_citation", response.text)

    return
