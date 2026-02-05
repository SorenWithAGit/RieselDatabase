import pandas as pd
import os
import glob


class read_excel:

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

class file_checker:
    
    def check_weather_files(file1: str, file2: str, df1: pd.DataFrame, df2: pd.DataFrame):
        # collect file name from path
        fn1 = os.path.basename(file1).split("/")[-1]
        fn2 = os.path.basename(file2).split("/")[-1]
        # check if weather dataframe from Harmel is equal to Umbraco Website dataframe
        if df1.equals(df2):
            print("Harmel: " + fn1 + " is identical to Umbraco: " + fn2)
            
        else:
            print("Harmel: " + fn2 + " is not identical to Umbraco: " + fn2)

folder1 = r"\\ARS-DATA\Archive\HarmelExit\riesel\weather\koesterdailyweather"
folder2 = r"I:\programming\python\riesel_file_checker\Umbraco Website Files"

# collect paths from 1st and 2nd directories
path1 = glob.glob(folder1 + "//" + "*ries.xls")
path2 = glob.glob(folder2 + "//" + "*ries.xls")


files1 = []
files2 = []

# collect file names from paths
for path in path1:
    file = os.path.basename(path).split("/")[-1]
    files1.append(file)

for path in path2:
    file = os.path.basename(path).split("/")[-1]
    files2.append(file)

# match file names of 2nd path to 1st
files2 = [file for file in files1 if file in files2]

if files1 == files2:
    print("files match")

for p, path in enumerate(path1):
    re = read_excel
    f1 = re.read_weather(path)
    # print("Harmel File: ")
    # print(f1)
    f2 = re.read_weather(path2[p])
    # print("Umbraco Website File: ")
    # print(f2)

    fc = file_checker
    fc.check_weather_files(path, path2[p], f1, f2)