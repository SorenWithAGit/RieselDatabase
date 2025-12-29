import sqlite3

class Tables:
    # connect to database
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
    
    # add tables to databse
    def add_Table(self, table_name: str, attribute_names: list, attribute_types: list):
        tables_script = str("CREATE TABLE " + table_name + " (ID INTEGER PRIMARY KEY,")
        for i, attribute in enumerate(attribute_names):
            tables_script += str(attribute +  " " + attribute_types[i] + ",")
        tables_script += ");"
        tables_script = tables_script.replace(",);", ");")
        # print(tables_script)
        self.cur.executescript(tables_script)
        self.conn.commit()
        self.conn.close()

    # Add columns to table
    def add_columns(self, table_name: str, attribute_names: list, attribute_types: list):
        for i, attribute in enumerate(attribute_names):
            script = str("ALTER TABLE " + table_name + " ADD COLUMN " + attribute + attribute_types[i] + ";")
            self.cur.executescript(script)
            self.conn.commit()
        self.conn.close()

    # Remove columns in table
    def remove_columns(self, table_name: str, attribute_names: list):
        for attribute in attribute_names:
            script = str ("ALTER TABLE " + table_name + " DROP COLUMN " + attribute + ";")
            self.cur.executescript(script)
            self.conn.commit()
        self.conn.close()

    # Retrieve column names in table
    def retrieve_names(self, table_name: str):
        self.cur.execute(str("SELECT * FROM " + table_name))
        column_names = list([description[0] for description in self.cur.description])
        for name in column_names:
            if "ID" in name:
                column_names.remove(name)
        self.conn.commit()
        self.conn.close()
        # print(column_names)
        return column_names

    # Rename columns in table
    def rename_columns(self, table_name: str, old_attribute_name: list, new_attribute_name: list):
        for i, attribute in enumerate(old_attribute_name):
            script = str("ALTER TABLE " + table_name + " RENAME COLUMN " + attribute + 
                         " TO " + new_attribute_name[i] + ";")
            self.cur.executescript(script)
            self.conn.commit()
        self.conn.close()

    # Remove specific entries from table
    def remove_entry(self, table_name: str, entry_ids: list):
        for id in entry_ids:
            script = str("DELETE FROM " + table_name + " WHERE id = " + id + ";")
            self.cur.executescript(script)
            self.conn.commit()
        self.conn.close()

    # remove all entries from table
    def clear_Table(self, table_names: str):
        for table in table_names:
            clear_script = ""
            clear_script += str("DELETE FROM " + table)
            self.cur.executescript(clear_script)
            self.conn.commit()
        self.conn.close()

    # remove table from databse
    def delete_Table(self, table_names: str):
        for table in table_names:
            delete_script = ""
            delete_script += str("DROP TABLE " + table)
            self.cur.executescript(delete_script)
            self.conn.commit()
        self.conn.close()
