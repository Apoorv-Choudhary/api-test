from datetime import datetime
from env.db_interface import DBConnection


class LoggingInterface:
    def __init__(self):
        self.database = "logging_db"
        self.table_name = "logging_table"
        self.primary_col = "id"
        # below dataset will store ranges of
        # all inserted logs format: list(tuple(int,int))
        self.start_end_ids = []
        self.script_name = ""
        self.script_type = ""
        self.feature_name = ""
        self.client_name = ""
        self.url = ""
        self.user_email = ""
        self.record_count = 0
        self.insert_query_prefix = f"""
            INSERT INTO 
            {self.table_name} 
            (script_type,
            script_name,
            feature_name,
            client_name,
            url,
            result,
            description,
            created_date,
            created_time,
            user_email) 
            VALUES 
        """
        self.insert_query_suffix = ""

    def set_attributes(self, script_name=None, script_type=None, feature_name=None, client_name=None, url=None,
                       user_email=None):
        self.feature_name = feature_name if feature_name else self.feature_name
        self.script_name = script_name if script_name else self.script_name
        self.script_type = script_type if script_type else self.script_type
        self.client_name = client_name if client_name else self.client_name
        self.user_email = user_email if user_email else self.user_email
        self.url = url if url else self.url

    def read(self, file_type="excel"):
        if not self.start_end_ids:
            return -1

        read_query = f"SELECT * FROM {self.table_name} where "

        for id_range in self.start_end_ids:
            read_query += f"{self.primary_col} between {id_range[0]} and {id_range[1]} or "
        read_query = read_query[:-3]
        with DBConnection(
                db_name=self.database
        ) as db_cur:
            db_cur.execute(read_query)
            # TODO: Implement exporting report in csv/excel
            print(db_cur.fetchall())

    def write(self, result: bool = False, message: str = "", commit_now=False):
        created_date = datetime.now().date()
        created_time = datetime.now().time()
        self.insert_query_suffix += f"""('{self.script_type}',
                  '{self.script_name}',
                  '{self.feature_name}',
                  '{self.client_name}',
                  '{self.url}',
                   {result},
                  '{message.replace("'", "''")}',
                  '{created_date}',
                  '{created_time}',
                  '{self.user_email}'),"""
        self.record_count += 1

        if self.record_count == 500 or commit_now:
            self.write_into_db()

    def write_into_db(self):
        with DBConnection(
                db_name=self.database
        ) as (db_cur, db_con):
            db_cur.execute(self.insert_query_prefix + self.insert_query_suffix[:-1])
            self.start_end_ids.append(
                (db_cur.lastrowid, db_cur.lastrowid + db_cur.rowcount - 1)
            )
            db_con.commit()
            self.insert_query_suffix = ""
            self.record_count = 0

    def cleanup_data(self):
        self.start_end_ids = []
        self.record_count = 0
        self.insert_query_suffix = ""


logging = LoggingInterface()
