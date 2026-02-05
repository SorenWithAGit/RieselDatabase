import pandas as pd
import csv

class read_web_files:
    def read_precip(file_path):
        rows = []
        with open(file_path) as csvconvert:
            csvread = csv.reader(csvconvert)
            for row in csvread:
                rows.append(row[0].split())
                # print(row[0].split())

        rain_df = pd.DataFrame(columns = ["Raingauge", "Date", "Time (min)", "Precip (in)"]).astype({"Raingauge" : str,
                                                                                                "Date" : str,
                                                                                                "Time (min)" : str,
                                                                                                "Precip (in)" : float})

        raingauge = []
        dates = []
        time = []
        precip = []

        for row in rows[2:]:
            # print(row)
            raingauge.append(row[0])
            date = str(row[1] + "/" + row[2]  + "/" + row[3])
            dates.append(date)
            time.append(row[4])
            precip.append(row[5])

        rain_df["Raingauge"] = raingauge
        rain_df["Date"] = dates
        rain_df["Time (min)"] = time
        rain_df["Precip (in)"] = precip


        # print(rain_df)
        rain_df["Date"] = pd.to_datetime(rain_df["Date"])

        # last_day_df = rain_df[rain_df["Date"].dt.is_month_end]

        last_day_df = rain_df.groupby([
            rain_df["Date"].dt.year,
            rain_df["Date"].dt.month
        ]).last().reset_index(drop = True)
        print(last_day_df)
        return(last_day_df)
    
rwb = read_web_files
rwb.read_precip(r"C:\Users\john.sorensen\Documents\rg2a60.web")