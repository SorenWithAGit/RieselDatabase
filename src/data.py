import pandas as pd
import sqlite3

class add_data:
    # Connect to database
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()

    # Add a single record to table
    def add_record(self, table_name: str, column_names: list, data: list):
        sql_statement = str("INSERT INTO " + "[" + table_name + "]" + "(")
        for name in column_names:
            sql_statement += str("[" + name + "]" + ",")
        sql_statement += ")"
        sql_statement = sql_statement.replace(",)", ")")
        sql_statement += " VALUES ("
        sql_statement += "?," * len(column_names)
        sql_statement += ")"
        sql_statement = sql_statement.replace(",)", ")")
        # print(sql_statement)
        self.cur.execute(sql_statement, data)
        self.conn.commit()
        self.conn.close()

    # Add a dataframe to table
    def add_df(self, table_name: str, df):
        df.to_sql(table_name, self.conn, if_exists = "append", index = False)
        self.conn.commit()
        self.conn.close()

        
