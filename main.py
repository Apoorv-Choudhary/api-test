import os.path
import time

from fastapi import FastAPI, Request
import requests
from env import json_parser, script_handler
from env.logging_interface import logging
from threading import Thread
from utility import auth_utility
import traceback

requests.packages.urllib3.disable_warnings()

app = FastAPI()


@app.post("/execute_task")
async def execute_task(json_data: Request):
    json_data = await json_data.json()

    url = ""
    for each_req in json_data:
        from env.session_manager import current_session
        try:
            current_session.session_cleanup()

            json_parser_obj = json_parser.JSONParser(**each_req)
            url = json_parser_obj.url
            controller_name = json_parser_obj.controller_name
            client_name = json_parser_obj.client_name
            feature_name = json_parser_obj.feature_name

            current_session.add_variable("_json_parser_obj", json_parser_obj)

            logging.set_attributes(feature_name=feature_name,
                                   client_name=client_name,
                                   url=url, user_email=json_parser_obj.username)
            feature_dir = os.path.join("controllers", controller_name,
                                       feature_name)
            data_dict = {"feature_dir": feature_dir,
                         "pre_scripts": json_parser_obj.pre_scripts,
                         "coincident_scripts": json_parser_obj.coincident_scripts,
                         "post_scripts": json_parser_obj.post_scripts}
            script_handle_obj = script_handler.ScriptHandler(**data_dict)

            auth_utility.get_auth_token()

            # print("main1.", current_session.objects)
            call_user_scripts(script_handle_obj, script_handle_obj.pre_scripts, "pre")
            # print("main2.", current_session.objects)
            # call_user_scripts(script_handle_obj, script_handle_obj.coincident_scripts, "coincident")
            # print("main3.", current_session.objects)
            # call_main_api(json_parser_obj)

            thread_list = []
            t = Thread(target=call_user_scripts,
                       args=(script_handle_obj, script_handle_obj.coincident_scripts, "coincident"))
            thread_list.append(t)
            t.start()
            t = Thread(target=call_main_api, args=(json_parser_obj,))
            thread_list.append(t)
            t.start()
            for t in thread_list:
                t.join()

            call_user_scripts(script_handle_obj, script_handle_obj.post_scripts, "post")
            # print("main4.", current_session.objects)
            logging.write_into_db()
            current_session.session_cleanup()
        except FileNotFoundError as e:
            print(traceback.format_exc())
        finally:
            current_session.session_cleanup()

    print(f"====logging: start end ids: {logging.start_end_ids}")
    logging.cleanup_data()

    return {"success": 200, "data": url}


def call_user_scripts(script_handler_obj: script_handler.ScriptHandler, script_dict, script_type):
    for script_name, script_args in script_dict.items():
        logging.set_attributes(script_name=script_name, script_type=script_type)
        script_handler_obj.run_script(script_name, script_type, script_args)


def call_main_api(json_parser_obj: json_parser.JSONParser):
    auth_token = auth_utility.get_auth_token()
    # print(f"auth_token: {auth_token}")

    session = requests.Session()
    session.headers = {"Authorization": f"Bearer {auth_token}"}
    session.verify = False

    main_url = json_parser_obj.url
    args = json_parser_obj.arguments
    body = json_parser_obj.body
    method_type = json_parser_obj.method_type.lower()
    session_attr = getattr(session, method_type)

    if callable(session_attr):
        response = session_attr(main_url, params=args, json=body)
        print("main url response", response.text)
    else:
        from env.custom_errors import InvalidMethodType
        raise InvalidMethodType("Only POST, GET, PUT and DELETE are allowed as method types")
    # return response.status_code


@app.get("/callback")
async def call_external_api(url=None):
    callback_url = ""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(callback_url, data={"email": "", "password": ""}, headers=headers, verify=False)
    token = response.json()["token"]
    print("login response status code", response.status_code)
    print("token", token)

    session = requests.Session()
    session.headers = {"Authorization": "Bearer {access_token}".format(access_token=token)}
    session.verify = False

    test_url = ""
    response = session.get(test_url)
    print("test url response", response.json())
    return response.status_code


@app.get("/query_db")
async def test_db_connection():
    import mysql.connector

    try:
        cnx = mysql.connector.connect(user='', password='',
                                      host='', port=0,
                                      database='')
        cur = cnx.cursor()

        client_name = ''

        query = f"""
            INSERT INTO
            `config`
            (
                `client_name`,
                `config_section`,
                `config_key`,
                `config_value`,
                `created_by`,
                `created_on`,
                `modified_on`,
                `modified_by`,
                `is_active`,
                `exposable`)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        data = [(f'{client_name}', 'FeatureFlag', 'test1', 'False', None, None, None, None, 'T', 'T'),
                (f'{client_name}', 'FeatureFlag', 'test2', 'False', None, None, None, None, 'T', 'T'),
                (f'{client_name}', 'FeatureFlag', 'test3', 'False', None, None, None, None, 'T', 'T')
                ]

        cur.executemany(query, data)
        print(cur.lastrowid, cur.rowcount)
        print(type(cur.lastrowid), type(cur.rowcount))
        print(cur.column_names)

        cur.reset()
        cur.reset()
        cur.reset()
        cur.reset()
        cur.close()
        cur.close()
        cur.close()
        cur.close()
        cur.close()
        cnx.commit()
        cnx.close()
        cnx.close()

    except Exception as e:
        import sys, traceback
        print("traceback 2", traceback.print_exc())
        print("sys traceback", sys.exc_info())

    return

#
# import threading, sys
# from env.session_manager import current_session
# print("1.", current_session.objects)
#
# current_session.objects.get("open_sessions").append(0)
# script_path = ["controllers.developer.back_population.pre.temp",
#                "controllers.developer.back_population.pre.temp1.main"]
#
# m = __import__(script_path[0])
# for submodule_name in script_path[0].split(".")[1:]:
#     m = getattr(m, submodule_name)
#
# try:
#     if callable(getattr(m, "main")):
#         main_method = getattr(m, "main")
# except AttributeError as ae:
#     print("Please write 'main' method in your script")
#
#
# t = threading.Thread(target=main_method)
# t.start()
# t.join()
# out, err = p.communicate()
# print("a:", out, "\n=======\n", err)
# print("main1.", current_session.objects)

# p = subprocess.Popen([l_path[1]], shell=True, stdout=subprocess.PIPE,
#                      stderr=subprocess.STDOUT)
# out, err = p.communicate()
# print("b:", str(out), "\n=======\n", err)


