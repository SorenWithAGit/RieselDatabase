import pandas as pd
import csv

class read_web_files:


    def read_precip(file_path: str):
        # create blank list to append rows to
        rows = []
        # open web file and convert to csv, append each row
        with open(file_path) as csvconvert:
            csvread = csv.reader(csvconvert)
            for row in csvread:
                rows.append(row[0].split())
                # print(row[0].split())

        # create pandas dataframe and format columns
        rain_df = pd.DataFrame(columns = ["Raingauge", "Date", "Time (min)", "Precip (in)"]).astype({"Raingauge" : str,
                                                                                                "Date" : str,
                                                                                                "Time (min)" : str,
                                                                                                "Precip (in)" : float})

        # create empty lists to append data
        raingauge = []
        dates = []
        time = []
        precip = []

        # from row append data to corresponding list
        for row in rows[2:]:
            # print(row)
            raingauge.append(row[0])
            date = str(row[1] + "/" + row[2]  + "/" + row[3])
            dates.append(date)
            time.append(row[4])
            precip.append(row[5])

        # add data from lists to dataframe
        rain_df["Raingauge"] = raingauge
        rain_df["Date"] = dates
        rain_df["Time (min)"] = time
        rain_df["Precip (in)"] = precip


        # print(rain_df)

        # convert date column to datetime
        rain_df["Date"] = pd.to_datetime(rain_df["Date"])


        # create new dataframe with last date and time entries
        last_day_df = rain_df.groupby([
            rain_df["Date"].dt.year,
            rain_df["Date"].dt.month
        ]).last().reset_index(drop = True)
        print(last_day_df)
        return(last_day_df)
    
rwb = read_web_files
rwb.read_precip(r"C:\Users\john.sorensen\Documents\rg2a60.web")