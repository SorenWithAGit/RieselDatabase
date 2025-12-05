import sqlite3

class Tables:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
    
    def add_Table(self, table_name: str, attribute_names: list, attribute_types: list):
        tables_script = str("CREATE TABLE " + table_name + " (ID INTEGER PRIMARY KEY,")
        for i, attribute in enumerate(attribute_names):
            tables_script += str(attribute +  " " + attribute_types[i] + ",")
        tables_script += ");"
        tables_script = tables_script.replace(",);", ");")
        # print(tables_script)
        self.cur.executescript(tables_script)
        self.conn.commit()

    def clear_Table(self, table_names: str):
        for table in table_names:
            clear_script = ""
            clear_script += str("TRUNCATE TABLE " + table)
        self.cur.executescript(clear_script)
        self.conn.commit()

    def delete_Table(self, table_names: str):
        for table in table_names:
            delete_script = ""
            delete_script += str("DROP TABLE " + table)
        self.cur.executescript(delete_script)
        self.conn.commit()




