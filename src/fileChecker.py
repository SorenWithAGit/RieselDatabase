import pandas as pd
import os
import glob


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


# # Path to folders and file type to compare
# folder1 = r"\\ARS-DATA\Archive\HarmelExit\riesel\weather\koesterdailyweather"
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


########################################################################


folder_path = r"I:\programming\python\riesel_file_checker\Harmel Evappan"
f = files
fp = f.get_files(folder_path, "32*")[0]
fn = f.get_files(folder_path, "32*")[1]

for path in fp:
    # print(path)
    r = read_excel
    rEV = r.read_evappan(path)
    print(rEV)