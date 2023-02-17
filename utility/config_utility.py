import mysql.connector
import requests, json, traceback
from env.session_manager import current_session
from env.db_interface import DBConnection

json_parser_obj = current_session.get_variable("_json_parser_obj")
domain = json_parser_obj.domain
client_name = json_parser_obj.client_name
config_db = "config"


def update_feature_flag(config_key: str, config_value: str):
    try:
        disable_safe_update_query = "SET SQL_SAFE_UPDATES = 0;"
        enable_safe_update_query = "SET SQL_SAFE_UPDATES = 1;"
        update_query = f"""update config.config set config_value = "{config_value}"
                            where client_name = "{client_name}" 
                            and config_key = "{config_key}";"""
        get_query = f"""select config_value from config.config
                        where client_name = "{client_name}" 
                        and config_key = "{config_key}";"""
        with DBConnection(
                db_name=config_db
        ) as (db_cur, db_con):
            db_cur.execute(disable_safe_update_query)
            db_cur.execute(update_query)
            db_cur.execute(enable_safe_update_query)
            db_cur.execute(get_query)
            print(f"====db_cur: {db_cur.fetchall()}")
            db_con.commit()
        return True
    except mysql.connector.Error as ex:
        print(traceback.format_exc())
        return False

