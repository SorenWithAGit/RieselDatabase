import pandas as pd
import sqlite3

class date_range:
    def generate_dates(start_date: str, end_date: str):
        date_range = pd.date_range(start = start_date, end = end_date)
        date_df = pd.DataFrame({"Date" : date_range})
        return date_df

class db_dates:
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()

    def add_dates(self, date_df):
        for i in date_df.index:
            date = str(date_df["Date"][i]).split(" ")[0]
            self.cur.execute('''INSERT INTO Dates (
                            date)
                            VALUES (?)''', (
                            date,)
                            )
        self.conn.commit()
