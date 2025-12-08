import pandas as pd
import sqlite3

class date_range:
    # function to create DataFrame of dates within range
    def generate_dates(start_date: str, end_date: str):
        date_range = pd.date_range(start = start_date, end = end_date)
        date_df = pd.DataFrame({"Date" : date_range})
        return date_df
    
    # function to create DataFrame of years within range
    def generate_years(start_year: str, end_year: str):
        year_range = pd.date_range(start = start_year, end = end_year)
        dates = pd.DataFrame({"Date" : year_range})
        year_df = pd.DataFrame(dates["Date"].dt.year.unique())
        return year_df

class db_dates:
    # connect to database
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()

    # insert dates into database
    def add_dates(self, date_df):
        for i in date_df.index:
            date = str(date_df["Date"][i]).split(" ")[0]
            self.cur.execute('''INSERT INTO Dates (
                            date)
                            VALUES (?)''', (
                            date,)
                            )
        self.conn.commit()

    # insert years into database
    def add_years(self, year_df):
        for i in year_df.index:
            year = str(year_df.iloc[i][0])
            self.cur.execute('''INSERT INTO Year (
                             Year)
                             VALUES (?)''', (
                             year,)
                             )
        self.conn.commit()