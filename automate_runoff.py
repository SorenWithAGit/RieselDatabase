import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src import calculations as cal
from src import weatherFiles as wt
import glob
import os

# sutron_path = r"I:\programming\runoff\raw_logger_files\Y2\Y2_2008_2.DAT"

# sut = wt.read_txt
# sutron = sut.read_sutron(sutron_path)
# print(sutron)

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
    root_folder = r"I:\programming\runoff\raw_logger_files\\" + site 

    sut = wt.read_txt
    rc = cal.runoff_calculator()

    runoff = pd.DataFrame(columns = ["datetime", "site", "raw runoff (in)", "raw runoff (mm)"]).astype({"datetime" : "datetime64[ns]",
                                                                                                        "site" : "str",
                                                                                                        "raw runoff (in)" : "float",
                                                                                                        "raw runoff (mm)" : "float"})

    file_paths = glob.glob(root_folder + "//" + "*.dat")
    files = []
    for path in file_paths:
        file_name = os.path.basename(path).split("/")[-1]
        files.append(file_name)

    for f, file in enumerate(file_paths):
        try:
            sutron = sut.read_sutron(file)
            sutron.insert(1, "site", site)
            # print(sutron)
            flow_calculator = rc.create_flow_calculator(site, sutron)
            flow_calculator["datetime"] = pd.to_datetime(flow_calculator["datetime"])
            flow_calculator.set_index("datetime", inplace = True)
            # print(flow_calculator)
            raw_daily = flow_calculator["raw runoff (mm)"].resample("D").sum().reset_index()
            raw_daily.insert(1, "site", site)
            raw_daily.insert(2, "raw runoff (in)", (raw_daily["raw runoff (mm)"]/25.4))
            # print(raw_daily)
            runoff = pd.concat([runoff, raw_daily], ignore_index = True)
            runoff = runoff.groupby("datetime", as_index = False).sum()
            
        except:
            print(files[f])

    dataframes[site] = runoff
    print(runoff)

# with pd.ExcelWriter(r"I:\programming\runoff\raw_logger_files\runoff_clalculated_from_raw.xlsx") as writer:
#     for i, site in enumerate(dataframes):
#         dataframe = dataframes[site]
#         dataframe.to_excel(writer, sheet_name = site, index = False)