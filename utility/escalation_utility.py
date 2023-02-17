import requests
from env.session_manager import current_session
from utility.auth_utility import get_auth_token

json_parser_obj = current_session.get_variable("_json_parser_obj")
domain = json_parser_obj.domain
client_name = json_parser_obj.client_name
url_prefix = f"{domain}/{client_name}"
url = f"{url_prefix}/developer/test_process_notices_and_citation_escalation"


def escalate_citations(process_date: str):
    """

    :param process_date: for eg: "12-02-2022"
        *   date format must always be DD-MM-YYYY
    :return:
    """

    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()
    escalation_url = f"{url}/{process_date}"
    response = requests.post(url=escalation_url, headers=headers, verify=False)
    print("====escalate_citations", response.text)

    return
