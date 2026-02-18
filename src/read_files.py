import pandas as pd
import os
import glob
import csv
from datetime import datetime
from pathlib import Path
import numpy as np


class files:
    
    # collect list of file paths and file names from root folders
    def get_files(root_folder: str, file_identifier: str):
        # Collect file paths and file names
        file_paths = glob.glob(root_folder + "//" + file_identifier)
        files = []
        for path in file_paths:
            file = os.path.basename(path).split("/")[-1]
            files.append(file)
        return file_paths, files



class read_excel:

    # read weather data files
    def read_weather(filepath: str):
        # define headers
        headers = ["mo", "day", "year", "Max Temp (C)", "Min Temp (C)", "Precip (mm)"]
        # read excel data into pandas dataframe and drop original labels
        df = pd.read_excel(filepath)
        df = df.drop(index = [0, 1, 2, 3])
        # collect labels to rename columns
        df_columns = df.columns.tolist()
        column_dict = dict(zip(df_columns, headers))
        # rename columns with proper headers
        df = df.rename(columns = column_dict)
        df = df.reset_index(drop = True)
        return df
    

    def read_evappan(filepath: str):
        headers = ["year", "month", "day", "Hook Gauge (in)", "After fill (in)", "Precipitation (in)", "Calculated Evaporation (in)"]
        # read excel data into pandas dataframe and isolate data
        df = pd.read_excel(filepath)
        df = df.drop(index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        df = df.iloc[:,[2, 3, 4, 5, 6, 7, 8]]
        df_columns = df.columns.tolist()
        column_dict = dict(zip(df_columns, headers))
        df = df.rename(columns = column_dict)
        df = df.reset_index(drop = True)
        df["Date"] = pd.to_datetime(df[["year", "month", "day"]])
        df = df.iloc[:, [7, 3, 4, 5, 6]]
        return df
    

class read_txt:

    def read_hr_weather(filepath: str):
        rows = []
        with open(filepath, "r") as file:
            for line in file:
                rows.append(line.split())
        
        filtered_rows = [sublist for sublist in rows if sublist]

        # for i, label in enumerate(column_labels):
        #     print("row " + str(i) + " with len: " + str(len(label)))
        #     print(label)

                # Units for Columns
        # TGAD, average air temp, units deg C
        # TMAX, air temp max, units deg C
        # TMIN, air temp min, units deg C
        # RHMXD, relative humidity max daily, units %
        # RHMUD, relative humidity min daily, units %
        # VPRSD, vapor pressure average daily, units kPa
        # SRAD, solar radiation, units MJ/m2 NEEDS CONVERSION
        # WIND, wind speed average units km/d NEEDS CONVERSION
        # WMAX, Wind max speed, units km/d NEEDS CONVERSION
        # WINDDIR, Wind direction, units deg (daily average)
        # STAVG, soil temp avg, units deg C
        # STMAX, soil temp max, units deg C
        # STMIN, soil temp min, units deg C


        hrwthr = pd.DataFrame(columns = ["DOY", "HOUR", 
                                         "TGAD", "TMAX", "TMIN",
                                         "RHMXD", "RHUMD", "VPRSD",
                                         "SRAD", "WIND", "WINDDIR", 
                                         "WMAX", "RAIN", "STAVG", 
                                         "STMAX", "STMIN"]).astype({
                                             "DOY" : str,
                                             "HOUR" : int,
                                             "TGAD" : float,
                                             "TMAX" : float,
                                             "TMIN" : float,
                                             "RHMXD" : float,
                                             "RHUMD" : float,
                                             "VPRSD" : float,
                                             "SRAD" : float,
                                             "WIND" : float,
                                             "WINDDIR" : float,
                                             "WMAX" : float,
                                             "RAIN" : float,
                                             "STAVG" : float,
                                             "STMAX" : float,
                                             "STMIN" : float
                                         })
        
        # dates = []
        # hours = []
        # avg_air = []
        # max_air = []
        # min_air = []
        # max_rh = []
        # min_rh=[]
        # vp = []
        # sr = []
        # avg_wind = []
        # avg_wind_dir = []
        # max_wind = []
        # precip = []
        # avg_soil = []
        # max_soil = []
        # min_soil = []

        # print("length of row 1: " + str(len(rows[0])))
        # print("length of row 3: " + str(len(rows[2])))

        checkrows = []
        prev_rows = []
        next_rows = []
        
        prev_line_n = []
        check_line_n = []
        next_line_n = []

        # filter years where barometer was not in use
        if len(filtered_rows[0]) == 20 \
        or len(filtered_rows[2]) == 16:
            # print("file does not contain vp")
            # for row in filtered_rows[3:6]:
                # print("length of row: " + str(len(row)))
                # print(row)

            columns1 = ["YEAR", "Day", "HOUR", 
                        "TGAD", "TMAX", "TMIN",
                        "RHMXD", "RHUMD",
                        "SRAD", "WIND", "WINDDIR", 
                        "WMAX", "RAIN", "STAVG", 
                        "STMAX", "STMIN"]
            
            sensor_fails = []
            
            for i, row in enumerate(filtered_rows[3:]):
                for value in row:
                    if value == "na":
                        break
                    try:
                        if float(value) == -99999.00\
                        or float(value) == 99999.00:
                            sensor_fails.append(row)
                            break
                    except:
                        break

            for row in sensor_fails:
                print(row)

            # After finding error in values retrieve the row before
            for i, row in enumerate(filtered_rows[3:]):
                for value in row:
                    try:
                        num_float = float(value)
                    except:
                        prev_row_n = i + 2
                        prev_row = filtered_rows[prev_row_n]
                        prev_line_n.append(prev_row_n + 1)
                        prev_rows.append(prev_row)
                        # prev_line_n.append(prev_row_n + 1)
                        # print(prev_row)
                        break
            prev_df = pd.DataFrame(prev_rows, columns = columns1)
            prev_df.index = prev_line_n
            # print(prev_df)
            # print("\n")

            # Create Dataframe rows containing value errors
            for ic, row in enumerate(filtered_rows[3:]):
                for value in row:
                    try:
                        num_float = float(value)
                    except:
                        row_count = ic + 4
                        check_row = row
                        check_line_n.append(row_count)
                        checkrows.append(check_row)
                        # print(check_row)
                        break

            check_df = pd.DataFrame(checkrows, columns = columns1)
            check_df.index = check_line_n
            # print(check_df)
            # print("\n")
            
            # Create Dataframe of rows after checked row
            for ir, row in enumerate(filtered_rows[3:]):
                for value in row:
                    try:
                        num_float = float(value)
                    except:
                        next_row_n = ir + 4
                        next_row = filtered_rows[next_row_n]
                        next_line_n.append(next_row_n + 1)
                        next_rows.append(next_row)
                        # print(next_row)
                        break
            next_df = pd.DataFrame(next_rows, columns = columns1)
            next_df.index = next_line_n
            # print(next_df)
            # print("\n")

            # filter rows that are also in check_df
            prev_mask = ~prev_df.index.isin(check_df.index)
            prev_df_filter = prev_df[prev_mask]
            for i in prev_df_filter.index:
                prev_df_filter.loc[i, "Marker"] = "Before Check"
            # print(prev_df_filter)

            # print("\n")


            for i in check_df.index:
                check_df.loc[i, "Marker"] = "Check"
            # print(check_df)

            # print("\n")

            # filter out rows that are in check_df
            next_mask = ~next_df.index.isin(check_df.index)
            next_df_filter = next_df[next_mask]
            next_mark = []
            for i in next_df_filter.index:
                next_df_filter.loc[i, "Marker"] = "After Check"
            # print(next_df_filter)

            print("\n")

            # merge dataframes and add Dates
            merged_df = pd.concat([prev_df_filter, check_df, next_df_filter]).sort_index()
            dates = []
            years = merged_df["YEAR"].tolist()
            days = merged_df["Day"].tolist()
            for d, year in enumerate(years):
                year = year
                day = days[d]
                julian_string = str(year + day)
                date = datetime.strptime(julian_string, '%Y%j').date()
                dates.append(date)
            merged_df["DOY"] = dates
            cols = list(merged_df.columns)
            new_order = [cols[-1]] + cols[:-1]
            merged_df = merged_df[new_order]

            # output_file = Path(filepath).stem + "_check.csv"
            # merged_df.to_csv(output_file)

            # Print merged_df as string and print with spacing
            print(merged_df.to_string(col_space = 15))
                        
            print("\n")


        elif len(filtered_rows[0]) == 29 \
        or len(filtered_rows[2]) == 12:
            
            columns2 = ["YEAR", "Day", "HOUR", 
            "TGAD", "TMAX", "TMIN",
            "RHMXD", "RHUMD", "VPRSD",
            "SRAD", "WIND", "WINDDIR", 
            "WMAX", "RAIN", "STAVG", 
            "STMAX", "STMIN"]
            
            sensor_fails = []
            senseor_f_ln = []
            
            for i, row in enumerate(filtered_rows[3:]):

                if len(row) == 17:
                    for value in row:
                        if float(value) == -99999.00 \
                        or float(value) == 99999.00:
                            sensor_fails.append(row)
                            senseor_f_ln.append(i + 4)
                            break

                else:
                    break
            sf_df = pd.DataFrame(sensor_fails, columns = columns2)
            sf_df.index = senseor_f_ln

            dates = []
            sfyears = sf_df["YEAR"].tolist()
            sfdays = sf_df["Day"].tolist()
            for d, year in enumerate(sfyears):
                str_year = str(year)
                str_day = str(sfdays[d])
                str_julian = str_year + str_day
                date = datetime.strptime(str_julian, '%Y%j').date()
                dates.append(date)
            sf_df["DOY"] = dates
            sfcols = list(sf_df.columns)
            sfnew_order = [sfcols[-1]] + sfcols[:-1]
            sf_df = sf_df[sfnew_order]

            print("Rows with Sensor Failures: " + str(len(sf_df.index)))

            # cols = sf_df.columns
            # for col in cols[4:]:
            #     sf_df[col] = sf_df[col].astype(float)
            #     sf_df[col] = sf_df[col].mask(sf_df[col] == -99999.00, np.nan)
            #     sf_df[col] = sf_df[col].mask(sf_df[col] == 99999.00, np.nan)
            # print(sf_df.dtypes)

            print(sf_df)
            
            print("\n")
    
            new_rows = []
            check_rows = []
            index = []
            for i, row in enumerate(filtered_rows[3:]):
                # print("row #: " + str(i + 4))
                if len(row) == 15:
                    while len(row) < 17:
                        row.append("nan")
                
                if len(row) == 17:
                    new_rows.append(row)
                    index.append(i + 4)

                elif len(row) < 17:
                    check_rows.append(row)
                    print("Check row #: " + str(i + 4))

                elif len(row) > 17:
                    check_rows.append(row)
                    print("Check row #: " + str(i + 4))
                    break

            for n, row in enumerate(new_rows):
                for rv, val in enumerate(row):
                    if val == "na":
                        new_rows[n][rv] = val.replace("na", "nan")
            # print(new_rows[0:36])

            print("\n")
            df = pd.DataFrame(new_rows, columns = columns2).astype({
                "YEAR" : int, "Day" : int, "HOUR" : float,
                "RHMXD" : float, "RHUMD" : float, "VPRSD" : float,
                "SRAD" : float, "WIND" : float, "WINDDIR" : float,
                "WMAX" : float, "RAIN" : float, "STAVG" : float,
                "STMAX" : float, "STMIN" : float
            })

            dates = []
            dfyears = df["YEAR"].tolist()
            dfdays = df["Day"].tolist()
            for d, year in enumerate(dfyears):
                str_year = str(year)
                str_day = str(dfdays[d])
                str_julian = str_year + str_day
                date = datetime.strptime(str_julian, '%Y%j').date()
                dates.append(date)
            df["DOY"] = dates
            df.index = index
            dfcols = list(df.columns)
            dfnew_order = [dfcols[-1]] + dfcols[:-1]
            df = df[dfnew_order]

            colms = df.columns
            for colm in colms[4:]:
                df[colm] = df[colm].mask(df[colm] == -99999.00, np.nan)
                df[colm] = df[colm].mask(df[colm] == 99999.00, np.nan)

            # df = pd.concat([df, sf_df]).sort_index()

            print("Readable Rows: " + str(len(df.index)))
            print(df)
            print("\n")



    def read_precip(filepath: str):
        rows = []
        with open(filepath, "r") as file:
            for line in file:
                rows.append(line.split())
                
        # logic to determine beginning row of data
        if rows[1][-1] == "Rain(in)"  \
            or rows[1][-1] == "(in)" \
                and rows[2] != []:
            rows = rows[2:]

        elif rows[1][-1] == "Rain(in)" \
            or rows[1][-1] == "(in)" \
                and rows[2] == []:
            rows = rows[3:]

        rain_df = pd.DataFrame(columns = ["Raingauge", "Date", "Time (min)", "Precip (in)"]).astype({"Raingauge" : str,
                                                                                                "Date" : str,
                                                                                                "Time (min)" : str,
                                                                                                "Precip (in)" : float})
        # create empty lists to append data
        raingauge = []
        dates = []
        time = []
        precip = []

        for row in rows:
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
        rain_df["Precip (in)"] = rain_df["Precip (in)"].astype("float")


        # print(rain_df)
# 
        # convert date column to datetime
        rain_df["Date"] = pd.to_datetime(rain_df["Date"])
        # print(rain_df)


        # create new dataframe with daily values
        daily_df = rain_df.groupby([
            rain_df["Date"].dt.year,
            rain_df["Date"].dt.month,
            rain_df["Date"].dt.day
        ]).last().reset_index(drop = True)
        daily_df["Precip (in)"] = daily_df["Precip (in)"].astype("float")
        daily_df["Cumulative Precip (in)"] = daily_df["Precip (in)"].cumsum()
        # print(daily_df)
        # print(sum(daily_df["Precip (in)"]))



        
        buffer_df = daily_df
        buffer_df = buffer_df.set_index(buffer_df["Date"])
        buffer_df["Monthly Precip (in)"] = buffer_df.groupby([buffer_df.index.year, buffer_df.index.month])["Precip (in)"].cumsum()
        # print(buffer_df)

        # create new dataframe with daily values
        monthly_df = buffer_df.groupby([
            buffer_df["Date"].dt.year,
            buffer_df["Date"].dt.month
        ]).last().reset_index(drop = True)
        monthly_df = monthly_df.iloc[:, [0, 1, 5]]
        monthly_df["Cumulative Precip (in)"] = monthly_df["Monthly Precip (in)"].cumsum()
        print(monthly_df)


    def read_runoff(filepath: str):
        rows = []
        with open(filepath, "r") as file:
            for line in file:
                rows.append(line.split())
        rows = rows[2:]

        # create pandas dataframe and format columns
        runoff_df = pd.DataFrame(columns = ["Watershed", "Date", "Time (min)", 
                                          "flow (cfs)", "flow (in/hr)"]).astype(
                                                {"Watershed" : str,
                                                "Date" : str,
                                                "Time (min)" : int,
                                                "flow (cfs)" : float,
                                                "flow (in/hr)" : float})
        # create empty lists to append data
        Watershed = []
        dates = []
        time = []
        flow_cfs = []
        flow_inhr = []

        # from row append data to corresponding list
        for row in rows[2:]:
            # print(row)
            Watershed.append(row[0])
            date = str(row[1] + "/" + row[2]  + "/" + row[3])
            dates.append(date)
            time.append(row[4])
            flow_cfs.append(row[5])
            flow_inhr.append(row[6])

        runoff_df["Watershed"] = Watershed
        runoff_df["Date"] = dates
        runoff_df["Time (min)"] = time
        runoff_df["flow (cfs)"] = flow_cfs
        runoff_df["flow (in/hr)"] = flow_inhr

        print(runoff_df)

    
    def read_sediment(filepath: str):

        # read rows of text files and append rows containing data
        rows = []
        with open(filepath, "r") as file:
            for line in file:
                if len(line.split()) == 7 \
                and line.split()[1].isnumeric():
                    rows.append(line.split())

                elif len(line.split()) == 5 \
                and line.split()[1].isnumeric():
                    rows.append(line.split())
                
                

        rows = rows[2:]

        # If sediment data is subdaily
        if len(rows[0]) == 7:

            sed_df = pd.DataFrame(columns = ["Watershed", "Date", "Time (min)", "Sed conc (ppm)", 
                                            "Sed amount (t/a)"]).astype(
                                                                        {"Watershed" : str,
                                                                        "Date" : str,
                                                                        "Time (min)" : str,
                                                                        "Sed conc (ppm)" : float,
                                                                        "Sed amount (t/a)" : float})
            
            Waterhsed = []
            dates = []
            time = []
            sedconc = []
            sedamt = []

            for row in rows:
                # print(row)
                Waterhsed.append(row[0])
                date = str(row[1] + "/" + row[2]  + "/" + row[3])
                dates.append(date)
                time.append(row[4])
                sedconc.append(row[5])
                sedamt.append(row[6])
            
            sed_df["Watershed"] = Waterhsed
            sed_df["Date"] = dates
            sed_df["Time (min)"] = time
            sed_df["Sed conc (ppm)"] = sedconc
            sed_df["Sed amount (t/a)"] = sedamt

            sed_df["Date"] = pd.to_datetime(sed_df["Date"])

        # if sediment data is daily
        elif len(rows[0]) == 5:

            sed_df = pd.DataFrame(columns = ["Watershed", "Date", 
                                            "Sed amount (t/a)"]).astype(
                                                                        {"Watershed" : str,
                                                                        "Date" : str,
                                                                        "Sed amount (t/a)" : float})
            
            Waterhsed = []
            dates = []
            sedamt = []

            for row in rows:
                # print(row)
                Waterhsed.append(row[0])
                date = str(row[1] + "/" + row[2]  + "/" + row[3])
                dates.append(date)
                sedamt.append(row[4])
            
            sed_df["Watershed"] = Waterhsed
            sed_df["Date"] = dates
            sed_df["Sed amount (t/a)"] = sedamt

            sed_df["Date"] = pd.to_datetime(sed_df["Date"])

        print(sed_df)


class read_web:

    def read_precip(file_path: str):
        # create blank list to append rows to
        rows = []
        # open web file and convert to csv, append each row
        with open(file_path) as csvconvert:
            csvread = csv.reader(csvconvert)
            for row in csvread:
                rows.append(row[0].split())

        # print("row 2: " + str(rows[1]))
        # print("row 3: " + str(rows[2]))
        
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
        if rows[1][-1] == "Rain(in)"  \
            or rows[1][-1] == "(in)" \
                and rows[2] != []:
            rows = rows[2:]

        elif rows[1][-1] == "Rain(in)" \
            or rows[1][-1] == "(in)" \
                and rows[2] == []:
            rows = rows[3:]

        for row in rows:
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
        rain_df["Precip (in)"] = rain_df["Precip (in)"].astype("float")


        # print(rain_df)

        # convert date column to datetime
        rain_df["Date"] = pd.to_datetime(rain_df["Date"])
        # print(rain_df)


        # create new dataframe with daily values
        daily_df = rain_df.groupby([
            rain_df["Date"].dt.year,
            rain_df["Date"].dt.month,
            rain_df["Date"].dt.day
        ]).last().reset_index(drop = True)
        daily_df["Precip (in)"] = daily_df["Precip (in)"].astype("float")
        daily_df["Cumulative Precip (in)"] = daily_df["Precip (in)"].cumsum()
        # print(daily_df)
        # print(sum(daily_df["Precip (in)"]))



        
        buffer_df = daily_df
        buffer_df = buffer_df.set_index(buffer_df["Date"])
        buffer_df["Monthly Precip (in)"] = buffer_df.groupby([buffer_df.index.year, buffer_df.index.month])["Precip (in)"].cumsum()
        # print(buffer_df)

        # create new dataframe with daily values
        monthly_df = buffer_df.groupby([
            buffer_df["Date"].dt.year,
            buffer_df["Date"].dt.month
        ]).last().reset_index(drop = True)
        monthly_df = monthly_df.iloc[:, [0, 1, 5]]
        monthly_df["Cumulative Precip (in)"] = monthly_df["Monthly Precip (in)"].cumsum()
        print(monthly_df)


    def read_runoff(filepath: str):
        # create blank list to append rows to
        rows = []
        # open web file and convert to csv, append each row
        with open(filepath) as csvconvert:
            csvread = csv.reader(csvconvert)
            for row in csvread:
                rows.append(row[0].split())
        
        # create pandas dataframe and format columns
        runoff_df = pd.DataFrame(columns = ["Watershed", "Date", "Time (min)", 
                                          "flow (cfs)", "flow (in/hr)"]).astype(
                                                {"Watershed" : str,
                                                "Date" : str,
                                                "Time (min)" : int,
                                                "flow (cfs)" : float,
                                                "flow (in/hr)" : float})
            # create empty lists to append data
        Watershed = []
        dates = []
        time = []
        flow_cfs = []
        flow_inhr = []

        # from row append data to corresponding list
        for row in rows[2:]:
            # print(row)
            Watershed.append(row[0])
            date = str(row[1] + "/" + row[2]  + "/" + row[3])
            dates.append(date)
            time.append(row[4])
            flow_cfs.append(row[5])
            flow_inhr.append(row[6])

        runoff_df["Watershed"] = Watershed
        runoff_df["Date"] = dates
        runoff_df["Time (min)"] = time
        runoff_df["flow (cfs)"] = flow_cfs
        runoff_df["flow (in/hr)"] = flow_inhr

        print(runoff_df)



class file_checker:
    
    # compare weather data files from Harmel and Umbraco Website
    def check_weather_files(file1: str, file2: str, df1: pd.DataFrame, df2: pd.DataFrame):
        # collect file name from path
        fn1 = os.path.basename(file1).split("/")[-1]
        fn2 = os.path.basename(file2).split("/")[-1]
        # check if weather dataframe from Harmel is equal to Umbraco Website dataframe
        if df1.equals(df2):
            print("Harmel: " + fn1 + " is identical to Umbraco: " + fn2)
            
        else:
            print("Harmel: " + fn2 + " is not identical to Umbraco: " + fn2)

########################################################################

                        # Read & Compare Weather
########################################################################


# # Path to folders and file type to compare
# folder1 = r"I:\programming\python\riesel_file_checker\Harmel\dailyweather2009"
# folder2 = r"I:\programming\python\riesel_file_checker\Umbraco Website Files\Weather Files"
# file_idenifier = "*ries.xls"

# f = files
# path1 = f.get_files(folder1, file_idenifier)[0]
# files1 = f.get_files(folder1, file_idenifier)[1]

# path2 = f.get_files(folder2, file_idenifier)[0]
# files2 = f.get_files(folder2, file_idenifier)[1]


# # for file in files2:
# #     print(file)


# # match file names of 2nd path to 1st
# files2 = [file for file in files1 if file in files2]

# if files1 == files2:
#         for p, path in enumerate(path1):
#             re = read_excel
#             f1 = re.read_weather(path)
#             # print("Harmel File: ")
#             # print(f1)
#             f2 = re.read_weather(path2[p])
#             # print("Umbraco Website File: ")
#             # print(f2)

#             fc = file_checker
#             fc.check_weather_files(path, path2[p], f1, f2)


########################################################################


                    # Read Hourly Weather
########################################################################

root_folder = r"I:\programming\python\riesel_file_checker\Harmel\Hourly weather"

f = files
fp = f.get_files(root_folder, "*.txt")[0]
fn = f.get_files(root_folder, "*.txt")[1]

for i, path in enumerate(fp):
    print(fn[i])
    rt = read_txt
    dw = rt.read_hr_weather(path)

########################################################################


                        # Read Evappan
########################################################################


# folder_path = r"I:\programming\python\riesel_file_checker\Evappan"
# f = files
# fp = f.get_files(folder_path, "32*")[0]
# fn = f.get_files(folder_path, "32*")[1]

# for path in fp:
#     # print(path)
#     r = read_excel
#     rEV = r.read_evappan(path)
#     print(rEV)


########################################################################


                    # Read Precipitation .Web
########################################################################


# root_folder = r"I:\programming\python\riesel_file_checker\Umbraco 2 Website Files\Rainfall - Subdaily\*"
# folder_list = glob.glob(root_folder, recursive = True)

# for folder in folder_list:
#     fls = files
#     filepaths = fls.get_files(folder, "*.web")[0]
#     file_lst = fls.get_files(folder, "*.web")[1]

#     for i, path in enumerate(filepaths):
#         print(file_lst[i])
#         read = read_web
#         precip = read.read_precip(path)


########################################################################


                    # Read Precipitation .txt
########################################################################


# root_folder = r"I:\programming\python\riesel_file_checker\Umbraco 2 Website Files\Rainfall - Subdaily\*"
# folder_list = glob.glob(root_folder, recursive = True)

# for folder in folder_list:
#     fls = files
#     filepaths = fls.get_files(folder, "*.txt")[0]
#     file_lst = fls.get_files(folder, "*.txt")[1]

#     for i, path in enumerate(filepaths):
#         print(file_lst[i])
#         read = read_txt
#         precip = read.read_precip(path)


########################################################################


                        # Read Runoff .web
########################################################################

# root_folder = r"I:\programming\python\riesel_file_checker\Umbraco 2 Website Files\Rainfall - Subdaily\*"
# folder_list = glob.glob(root_folder, recursive = True)

# for folder in folder_list:
#     fls = files
#     filepaths = fls.get_files(folder, "*.web")[0]
#     file_lst = fls.get_files(folder, "*.web")[1]

#     for i, path in enumerate(filepaths):
#         print(file_lst[i])
#         rw = read_web
#         roweb = rw.read_runoff(path)


########################################################################


                       # Read Runoff .txt
########################################################################

# root_folder = r"I:\programming\python\riesel_file_checker\Umbraco 2 Website Files\Runoff - Subdaily\*"
# folder_list = glob.glob(root_folder, recursive = True)

# # file_count = 0
# for folder in folder_list:
#     fls = files
#     filepaths = fls.get_files(folder, "*.txt")[0]
#     files_lst = fls.get_files(folder, "*.txt")[1]

#     for i, path in enumerate(filepaths):
#         # file_count = i + 1
#         print(files_lst[i])
#         rt = read_txt
#         rotxt = rt.read_runoff(path)
# # print(file_count)


########################################################################


                        # Sedementation
########################################################################


# root_folder = r"I:\programming\python\riesel_file_checker\Umbraco 2 Website Files\Sediment - Daily"


# fls = files
# filepaths = fls.get_files(root_folder, "*.txt")[0]
# file_lst = fls.get_files(root_folder, "*.txt")[1]

# for i, path in enumerate(filepaths):
#     print(file_lst[i])
#     read = read_txt
#     sed = read.read_sediment(path)


########################################################################



########################################################################