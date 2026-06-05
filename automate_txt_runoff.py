import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src import calculations as cal
from src import weatherFiles as wt
import glob
import os

web_txt = wt.read_txt

dataframes = {
    "SW12" : [],
    "SW17" : [],
    "W1" : [],
    "W6" : [],
    "W10" : [],
    "W12" : [],
    "W13" : [],
    "Y2" : [],
    "Y6" : [],
    "Y8" : [],
    "Y10" : [],
    "Y13" : [],
    "Y14" : []
}

sites = ["SW12", "SW17", "W1", "W6", "W10", "W12", "W13", "Y2", "Y6", "Y8", "Y10", "Y13", "Y14"]
for site in sites:
    root_folder = r"I:\programming\runoff\georgie_daily_in\\" + site 

    runoff = pd.DataFrame(columns = ["date", "site", "runoff (in)", "runoff (mm)"]).astype({"date" : "datetime64[ns]",
                                                                                            "site" : "str",
                                                                                            "runoff (in)" : "float",
                                                                                            "runoff (mm)" : "float"})
    file_paths = glob.glob(root_folder + "//" + "*.dly")
    files = []
    for path in file_paths:
        file_name = os.path.basename(path).split("/")[-1]
        files.append(file_name)
        # print(file_name)

    for f, file in enumerate(file_paths):
        try:
            # print(file)
            web_ro = web_txt.read_txt_runoff(file)
            web_ro["runoff (mm)"] = web_ro["runoff (in)"] * 25.4
            # print(web_ro)
            runoff = pd.concat([runoff, web_ro], ignore_index = True)
        except:
            print(files[f])

    dataframes[site] = runoff
    print(runoff)

with pd.ExcelWriter(r"I:\programming\runoff\raw_logger_files\web_runoff_2006-2019.xlsx") as writer:
    for i, site in enumerate(dataframes):
        dataframe = dataframes[site]
        dataframe.to_excel(writer, sheet_name = site, index = False)