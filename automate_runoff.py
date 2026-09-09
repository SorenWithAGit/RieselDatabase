import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src import calculations as cal
from src import weatherFiles as wt
import glob
import os
import time
from multiprocessing import Pool
from functools import partial


# sutron_path = r"I:\programming\runoff\raw_logger_files\Y2\Y2_2008_2.DAT"

# sut = wt.read_txt
# sutron = sut.read_sutron(sutron_path)
# print(sutron)


def automate_runoff(site):
    root_folder = rf"I:\programming\runoff\raw_logger_files\\{site}"

    sut = wt.read_txt
    rc = cal.runoff_calculator()

    runoff = pd.DataFrame(columns=["datetime", "site", "raw runoff (in)", "raw runoff (mm)",]).astype({
        "datetime": "datetime64[ns]", "site": "str", "raw runoff (in)": "float", "raw runoff (mm)": "float"
    })
    
    flow_rate = pd.DataFrame(columns=[
        "site", "date", "time", "time (min)", "s level (ft)", "l level (ft)", 
        "discharge rate (cfs)", "runoff rate (in/hr)", "raw runoff (mm)", "raw runoff (in)",  
        "l discharge rate (cfs)", "l runoff rate (in/hr)", "l raw runoff (mm)", "l raw runoff (in)"
    ]).astype({
        "site": "str", "date": "datetime64[ns]", "time": "datetime64[ns]", "time (min)": "float",
        "s level (ft)": "float", "l level (ft)": "float", "discharge rate (cfs)": "float",
        "runoff rate (in/hr)": "float", "raw runoff (mm)": "float", "raw runoff (in)": "float",
        "l discharge rate (cfs)" : "float", "l runoff rate (in/hr)" : "float", "l raw runoff (mm)" : "float", "l raw runoff (in)" : "float"
    })

    file_paths = glob.glob(root_folder + "//" + "*.dat")
    files = [os.path.basename(path).split("/")[-1] for path in file_paths]

    for f, file in enumerate(file_paths):
        try:
            sutron = sut.read_sutron(file)
            sutron.insert(1, "site", site)
            
            flow_calculator = rc.create_flow_calculator(site, sutron)
            flow_calculator["datetime"] = pd.to_datetime(flow_calculator["datetime"])
            flow_calculator.set_index("datetime", inplace=True)

            raw_daily = flow_calculator["raw runoff (mm)"].resample("D").sum().reset_index()
            raw_daily.insert(1, "site", site)
            raw_daily.insert(2, "raw runoff (in)", (raw_daily["raw runoff (mm)"] / 25.4))
            
            runoff = pd.concat([runoff, raw_daily], ignore_index=True)
            runoff = runoff.groupby("datetime", as_index=False).sum()

            flow_calculator["raw runoff (in)"] = flow_calculator["raw runoff (mm)"] / 25.4
            flow_calculator["l raw runoff (in)"] = flow_calculator["l raw runoff (mm)"] / 25.4
            flow_rate = pd.concat([flow_rate, flow_calculator], ignore_index=False)
            
        except Exception as e:
            print(f"Error processing {files[f]}: {e}")

    print(flow_rate)
    
    return site, runoff, flow_rate


if __name__ == "__main__":
    start = time.perf_counter()

    sites = ["SW12", "SW17", "W1", "W6", "W10", "W12", "W13", "Y2", "Y6", "Y8", "Y10", "Y13", "Y14"]

    with Pool() as pool:
        raw_results = pool.map(automate_runoff, sites)

    dataframes = {site: [] for site in sites}
    flows = {site: [] for site in sites}

    for site, runoff_df, flow_df in raw_results:
        dataframes[site] = runoff_df
        flows[site] = flow_df

    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s)')



# with pd.ExcelWriter(r"I:\programming\runoff\raw_logger_files\daily_runoff.xlsx") as writer:
#     for i, site in enumerate(dataframes):
#         dataframe = dataframes[site]
#         dataframe.to_excel(writer, sheet_name = site, index = False)

dir = r"I:\programming\runoff\raw_logger_files"

# for key, df in flows.items():
#     file_path = os.path.join(dir, f"{key}.csv")
#     df.to_csv(file_path, index = True)
#     print(f"Saved: {file_path}")


