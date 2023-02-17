import requests, json
from env.session_manager import current_session
from utility.auth_utility import get_auth_token

json_parser_obj = current_session.get_variable("_json_parser_obj")
domain = json_parser_obj.domain
client_name = json_parser_obj.client_name
url_prefix = f"{domain}/{client_name}"
make_payment_url = f"{url_prefix}/data/payment_accept"
void_payment_url = f"{url_prefix}/data/void_local_payment"
void_payment_url2 = f"{url_prefix}/v3_1/payments"
payment_history_url = f"{url_prefix}/data/payment_history"
make_payment_url2 = f"{url_prefix}/v3_1/payments"


def make_payment(payment_data: dict):
    """

    :param payment_data: for eg:
    payment_dict = {"ticket_num": "L0002", "payment_amount": "150",
                    "payment_type": "cash", "check_number": "",
                    "payee_name": "andrew williams",
                    "payee_address": "from mars",
                    "balance": 150,
                    "consider_as_full": "F",
                    "consider_as_full_reason": ""}
    payment_data = {"payment": json.dumps(payment_dict), "ticket_type": "local", "fine": 250.00,
                    "override_balance": "F", "payment_date": "09/16/2022"}
        *   payment_dict dataset must be stringyfied when sending the payment_data.
        *   If you want to make a payment with consider_as_full set to 'T' then make sure
            override_balance is also set to 'T'.
        *   Use this method when you want to make payment while payment ledger is disabled.
        *   This utility doesn't allow partial payment. For partial payment use make_payment2.
    :return:
    """

    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url=make_payment_url, params=payment_data, headers=headers, verify=False)
    print("====make_payment", response.text, "====payment_data", payment_data)

    return


def make_payment2(payment_data: dict):
    """

    :param payment_data: for eg:
    payment_data = {"citation_type": "local", "payee_address": "", "payee_name": "tester",
                    "received_by": "Test User", "payment_amount": 170,
                    "payment_without_service_fee": 170, "payment_type": "cash",
                    "ticket_number": "L00022", "check_number": "", "consider_as_full": "F",
                    "consider_as_full_reason": "", "consider_as_full_adjustment": 0.00,
                    "restitution_balance": 0, "payment_date": "10/03/2022"}
        *   Use this method when you want to make payment while payment ledger is enabled.
        *   If you want to make a payment with consider_as_full set to 'T' then make sure
            override_balance is also set to 'T'.
        *   In case of partial payments, value of "consider_as_full_adjustment" will be
            (actual fine - payment amount).
    :return:
    """
    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()
    response = requests.post(url=make_payment_url2, params=payment_data, headers=headers, verify=False)
    print("====make_payment2", response.text, "====payment_data", payment_data)

    return


def void_payment2(_id: int, citation_type: str, description: str, nsf: str):
    """

    :param _id: id of the payment row that needs to be voided
    :param citation_type: type of citation
    :param description: reason for voiding payment
    :param nsf:
        *   Use this method when you want to make payment while payment ledger is disabled.
    :return:
    """

    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()
    void_payment_data = {"id": _id, "cit_type": citation_type,
                         "description": description, "nsf": nsf}
    response = requests.post(url=void_payment_url, params=void_payment_data, headers=headers, verify=False)
    print("====void_payment", response.text)

    return


def void_payment(_id: int, citation_type: str, description: str, nsf: str):
    """

    :param _id: id of the payment row that needs to be voided
    :param citation_type: type of citation
    :param description: reason for voiding payment
    :param nsf:
        *   Use this method when you want to make payment while payment ledger is enabled.
    :return:
    """

    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()
    void_payment_data = {"void_payment": "true", "citation_type": citation_type,
                         "reason": description, "nsf": nsf}
    void_payment_url_with_args = f"{void_payment_url2}/{_id}"
    response = requests.put(url=void_payment_url_with_args, params=void_payment_data, headers=headers, verify=False)
    print("====void_payment", response.text, "====void_citation_data", void_payment_data, "id", _id)

    return


def get_payment_history(ticket_num: str, ticket_type: str):
    """

    :param ticket_num:
    :param ticket_type:
    :return:
    """

    bearer_token = get_auth_token(forced_login=True)
    headers = {"Authorization": f"Bearer {bearer_token}"}
    requests.packages.urllib3.disable_warnings()
    data = {"ticket_num": ticket_num, "ticket_type": ticket_type}
    response = requests.post(url=payment_history_url, params=data, headers=headers, verify=False)
    print("====get_payment_history", response.text)

    return response.json()
