import sqlite3

class createDatabase:
    # create database
    def __init__(self, database):
        self.database = database
        self.conn = sqlite3.connect(self.database)
        self.cur = self.conn.cursor()
        self.conn.commit()

