import mysql.connector
import requests, json, traceback
from env.session_manager import current_session
from env.db_interface import DBConnection

json_parser_obj = current_session.get_variable("_json_parser_obj")
domain = json_parser_obj.domain
client_name = json_parser_obj.client_name


def fetch_data_from_payment_ledger(db_name, ticket_num):
    query = f"Select * from {db_name}.payment_ledger where ticket_number = '{ticket_num}';"
    with DBConnection(db_name=db_name, dict_results=True) as (db_cur, db_conn):
        db_cur.execute(query)
        return db_cur.fetchall()


def get_local_citation_data(db_name, ticket_num, select_cols):
    if len(select_cols) > 0:
        select_cols = ",".join(select_cols)
    else:
        return []
    query = f"Select {select_cols} from {db_name}.local_citation " \
            f"where ticket_num = '{ticket_num}'"
    with DBConnection(db_name=db_name, dict_results=True) as (db_cur, db_con):
        db_cur.execute(query)
        return db_cur.fetchall()


def get_citation_related_data(db_name, ticket_num, select_cols, table_name):
    if len(select_cols):
        select_cols = ",".join(select_cols)
    else:
        return []
    query = f"Select {select_cols} from {db_name}.{table_name} " \
            f"where ticket_num like '%{ticket_num}%'"
    with DBConnection(db_name=db_name, dict_results=True) as (db_cur, db_con):
        db_cur.execute(query)
        return db_cur.fetchall()
