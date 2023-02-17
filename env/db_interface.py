import mysql.connector
from env.session_manager import current_session
from env.config_parser import ConfigParser


class DBConnection:
    def __init__(self, db_name, dict_results=False):
        self.database = db_name
        self.dict_results = dict_results

    def __enter__(self):
        return self.__setup_connection__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__shutdown_connection__()

    def __setup_connection__(self):
        config_parser_obj = ConfigParser()
        temp_dict = config_parser_obj.config_data.get("db_config")
        temp_dict["database"] = self.database
        self.connection = mysql.connector.connect(
            **temp_dict
        )
        self.cursor = self.connection.cursor(dictionary=self.dict_results)
        return self.cursor, self.connection

    def __shutdown_connection__(self):
        self.cursor.reset()
        self.cursor.close()
        self.connection.close()

    def open_connection(self):
        current_session.objects["open_sessions"].append(self)
        self.__setup_connection__()

    def close_connection(self):
        self.__shutdown_connection__()

    def execute_query(self, query):
        self.cursor.execute(query)
