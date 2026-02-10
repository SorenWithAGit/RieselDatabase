import pandas as pd
import os
import glob
import csv


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