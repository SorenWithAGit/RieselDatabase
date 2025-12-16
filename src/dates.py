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
        self.conn.close()

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
        self.conn.close()

class seasons:
    # make df of seasons
    def __init__(self, database):
        seasons = {"Season" : ["Spring", "Summer", "Fall", "Winter"],
           "Start Date" : ["3/1", "6/1", "9/1", "12/1"],
           "End Date" : ["5/31", "8/31", "11/30", "2/28"]}

        self.seasons_df = pd.DataFrame(seasons)

        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()

    def add_seasons(self):
        for ind in self.seasons_df.index:
            season = str(self.seasons_df.iloc[ind]["Season"])
            start_date = str(self.seasons_df.iloc[ind]["Start Date"])
            end_date = str(self.seasons_df.iloc[ind]["End Date"])
            self.cur.execute('''INSERT INTO Seasons (
                             [Season],
                             [Start Date],
                             [End Date])
                             VALUES (?, ?, ?)''', (
                             season,
                             start_date,
                             end_date,)
                             )
            self.conn.commit()
        self.conn.close()