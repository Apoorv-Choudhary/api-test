from env.session_manager import current_session
import requests

auth_url = "v2_1/login_and_receive_token"


def get_auth_token(forced_login=False):
    json_parser_obj = current_session.get_variable("_json_parser_obj")
    username = json_parser_obj.username
    password = json_parser_obj.password
    domain = json_parser_obj.domain
    client_name = json_parser_obj.client_name
    login_url = f"""{domain}/{client_name}/{auth_url}"""
    token_name = "_auth_token"

    if not forced_login and current_session.has_variable(token_name):
        # print("====retrieved token from session")
        return current_session.get_variable(token_name)
    else:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        # print(f"====login_url:{login_url}")
        # print(f"====username:{username}")
        # print(f"====password:{password}")
        response = requests.post(login_url, params={"email": username, "password": password}, headers=headers,
                                 verify=False)
        # print(f"====response:{response}")
        # print(f"====response.text:{response.text}")
        token = response.json()["token"]
        if not current_session.has_variable(token_name):
            current_session.add_variable(token_name, token)
        else:
            current_session.update_variable(token_name, token)
        return token

