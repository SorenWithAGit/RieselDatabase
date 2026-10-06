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
from pathlib import Path
import math


# sutron_path = r"I:\programming\runoff\raw_logger_files\Y2\Y2_2008_2.DAT"

# sut = wt.read_txt
# sutron = sut.read_sutron(sutron_path)
# print(sutron)


def automate_runoff(site, root_folder):
    root_folder = rf"I:\programming\runoff\raw_logger_files\\{site}"

    sut = wt.read_txt
    rc = cal.runoff_calculator()

    runoff = pd.DataFrame(columns=["datetime", "site", "raw runoff (in)", "raw runoff (mm)",]).astype({
        "datetime": "datetime64[ns]", "site": "str", "raw runoff (in)": "float", "raw runoff (mm)": "float"
    })
    
    flow_rate = pd.DataFrame(columns=[
        "file_name", "line_num", "site", "date", "time", "time (min)", "s level (ft)", "l level (ft)", 
        "discharge rate (cfs)", "runoff rate (in/hr)", "raw runoff (mm)", "raw runoff (in)",  
        "l discharge rate (cfs)", "l runoff rate (in/hr)", "l raw runoff (mm)", "l raw runoff (in)", "thoughts"
    ]).astype({
        "file_name" : "str", "line_num" : "int", "site": "str", "date": "datetime64[ns]", "time": "datetime64[ns]", "time (min)": "float",
        "s level (ft)": "float", "l level (ft)": "float", "discharge rate (cfs)": "float",
        "runoff rate (in/hr)": "float", "raw runoff (mm)": "float", "raw runoff (in)": "float",
        "l discharge rate (cfs)" : "float", "l runoff rate (in/hr)" : "float", "l raw runoff (mm)" : "float", "l raw runoff (in)" : "float", "thoughts" : "str"
    })

    file_paths = glob.glob(root_folder + "//" + "*.dat")
    files = [os.path.basename(path).split("/")[-1] for path in file_paths]

    for f, file in enumerate(file_paths):
        try:
            parts = Path(file).parts
            index = parts.index("raw_logger_files")
            site_name = parts[index + 1]
            print(f"{site_name:<5} |    raw data file {f + 1:02} out of {len(file_paths):02}: {file}")
            sutron = sut.read_sutron(file)
            sutron.insert(1, "site", site)
            
            flow_calculator = rc.create_flow_calculator(site, sutron)
            flow_calculator["datetime"] = pd.to_datetime(flow_calculator["datetime"])
            flow_calculator.set_index("datetime", inplace=True)
            # raw_daily = flow_calculator.drop(columns = ["line_num"])
            # raw_daily = raw_daily["raw runoff (mm)"].resample("D").sum().reset_index()
            # raw_daily.insert(1, "site", site)
            # raw_daily.insert(2, "raw runoff (in)", (raw_daily["raw runoff (mm)"] / 25.4))
            
            # runoff = pd.concat([runoff, raw_daily], ignore_index=True)
            # runoff = runoff.groupby("datetime", as_index=False).sum()

            flow_calculator.insert(0, "file_name", files[f])

            flow_calculator["raw runoff (in)"] = flow_calculator["raw runoff (mm)"] / 25.4
            flow_calculator["l raw runoff (in)"] = flow_calculator["l raw runoff (mm)"] / 25.4
            # print(flow_calculator)
            flow_rate = pd.concat([flow_rate, flow_calculator], ignore_index=True)
            
        except Exception as e:
            print(f"Error processing {files[f]}: {e}")

    # print(flow_rate)
    
    return site, runoff, flow_rate


def automatomate_reported_runoff(site, root_folder):
    root_folder = rf"I:\programming\runoff\daren_reported_runoff\\{site}"
    r = wt.read_txt

    reported_ro = pd.DataFrame(columns = ["file_name", "line_num", "site", "date", "time", "time (min)", 
                                                "flow (cfs)", "flow (in/hr)"]).astype(
                                                        {"file_name" : "str",
                                                        "line_num" : "int",
                                                        "site" : "str",
                                                        "date" : "str",
                                                        "time" : "str",
                                                        "time (min)" : "int",
                                                        "flow (cfs)" : "float",
                                                        "flow (in/hr)" : "float"})
    
    file_paths = glob.glob(root_folder + "//" + "*.txt")
    files = [os.path.basename(path).split("/")[-1] for path in file_paths]
    # print(file_paths)

    for f, file in enumerate(file_paths):
        try:
            parts = Path(file).parts
            index = parts.index("daren_reported_runoff")
            site_name = parts[index + 1]
            print(f"{site_name:<5} |    reported data file {f + 1:02} out of {len(file_paths):02}: {file}")
            ro = r.read_subdaily_runoff(file)
            ro.insert(0, "file_name", files[f])
            reported_ro = pd.concat([reported_ro, ro], ignore_index = True)

        except Exception as e:
                    print(f"Error processing {files[f]}: {e}")

    return site, reported_ro



if __name__ == "__main__":
    start = time.perf_counter()

    sites = ["SW12", "SW17", "W1", "W6", "W10", "W12", "W13", "Y2", "Y6", "Y8", "Y10", "Y13", "Y14"]

    with Pool() as pool:
        raw_data_path = r"I:\programming\runoff\raw_logger_files\\{site}"
        raw_args = [(site, raw_data_path) for site in sites]

        reported_data_path = r"I:\programming\runoff\daren_reported_runoff\\{site}"
        reported_args = [(site, reported_data_path) for site in sites]

        raw_results = pool.starmap(automate_runoff, raw_args)
        reported_results = pool.starmap(automatomate_reported_runoff, reported_args)

    dataframes = {site: [] for site in sites}
    flows = {site: [] for site in sites}
    reported_flows = {site: [] for site in sites}

    target_cols = [
    "discharge rate (cfs)", "runoff rate (in/hr)", "raw runoff (mm)", "raw runoff (in)",  
    "l discharge rate (cfs)", "l runoff rate (in/hr)", "l raw runoff (mm)", "l raw runoff (in)"
]

    for site, runoff_df, flow_df in raw_results:
        dataframes[site] = runoff_df
        f_cols = [c for c in target_cols if c in flow_df.columns]
        # flows[site] = flow_df[(flow_df[f_cols].notna() & (flow_df[f_cols] != 0)).any(axis=1)].round(4)
        flows[site] = flow_df[(flow_df[f_cols]).notna().any(axis=1)].round(4)
        flows[site]["date"] = pd.to_datetime(flows[site]["date"], format = "mixed")
        # flows[site]["time"] = pd.to_timedelta(flows[site]["time"])
        # flows[site] = flows[site].sort_values(by = ["date", "time"])

    for site, reported_runoff in reported_results:
         reported_flows[site] = reported_runoff
         reported_flows[site]["date"] = pd.to_datetime(reported_flows[site]["date"], format = "mixed")
         

    # for site in sites:
    #      print(flows[site])
    #     #  print(flows[site].dtypes)

    # for site in sites:
    #      print(reported_flows[site])
    #     #  print(reported_flows[site].dtypes)

    for site in sites:
         raw_dat = flows[site]
         report_dat = reported_flows[site]

         raw_dat["time"] = pd.to_datetime(raw_dat["time"].astype(str), format="mixed").dt.time
         report_dat["time"] = pd.to_datetime(report_dat["time"].astype(str), format="mixed").dt.time

         raw_dat["time (min)"] = (raw_dat["time (min)"]).astype(int)
         report_dat["time (min)"] = (report_dat["time (min)"]).astype(int)
         
         report_dat.insert(0, "index", report_dat.index)

         merged_dat = pd.merge(
              report_dat[["index", "file_name", "line_num", "site", "date", "time (min)", "flow (cfs)"]],
              raw_dat[["date", "time (min)", "file_name", "line_num", "s level (ft)", "l level (ft)", "discharge rate (cfs)", "l discharge rate (cfs)"]],
              on = ["date", "time (min)"],
              how = "inner"
         )
         total_merged = len(merged_dat)
         flow = merged_dat["flow (cfs)"].astype(float)
         discharge = merged_dat["discharge rate (cfs)"].astype(float)
         l_discharge = merged_dat["l discharge rate (cfs)"].astype(float)
         is_consistent = (np.isclose(flow, discharge, rtol = 0.0005)) | (np.isclose(flow, l_discharge, rtol = 0.0005))
         match_count = is_consistent.sum()
         incosistent_count = (~is_consistent).sum()
         num_entries = len(report_dat["date"])
         not_matches = num_entries - total_merged

        #  print(merged_dat)
        #  print("\n")
        #  print("\n")

         inconsistent_records = merged_dat[~is_consistent].copy()
         inconsistent_records["flow (cfs)"] = pd.to_numeric(inconsistent_records["flow (cfs)"], errors='coerce')

         c = cal.runoff_calculator()
         inconsistent_records["daren s level (ft)"] = c.calculate_level(inconsistent_records["flow (cfs)"], site)[0].copy()
         inconsistent_records["daren l level (ft)"] = c.calculate_level(inconsistent_records["flow (cfs)"], site)[1].copy()
        #  inconsistent_records = inconsistent_records.iloc[:,[0,1,2,3,4,5,13,14,6,7,8,9,10,11,12]]
         inconsistent_records = inconsistent_records.rename(columns = {
              "index" : "merged_index",
              "file_name_x" : "daren_file_name",
              "line_num_x" : "daren_line_num",
              "flow (cfs)" : "daren flow (cfs)",
              "file_name_y" : "raw_file_name",
              "line_num_y" : "raw_line_num",
              "s level (ft)" : "raw s level (ft)",
              "l level (ft)" : "raw l level (ft)",
              "discharge rate (cfs)" : "raw discharge rate (cfs)",
              "l discharge rate (cfs)" : "raw l discharge rate (cfs)"
         })
         inconsistent_records = inconsistent_records.loc[:,["merged_index", "daren_file_name", "daren_line_num", "site", "date",
                                                            "time (min)", "daren s level (ft)", "daren l level (ft)", "daren flow (cfs)", "raw_file_name",
                                                            "raw_line_num", "raw s level (ft)", "raw l level (ft)", "raw discharge rate (cfs)", 
                                                            "raw l discharge rate (cfs)"]]
         print(inconsistent_records)

         inconsistent_export = r"I:\programming\runoff\mismatched_data"

         file_path = os.path.join(inconsistent_export, site + "_mismatched.csv")
         inconsistent_records.to_csv(file_path, index = False)
         print(f"Saved: {file_path}")

         missing_records = report_dat[~report_dat.index.isin(merged_dat["index"])].copy()

        #  print(missing_records)

        #  missing_records["flow (cfs)"] = pd.to_numeric(missing_records["flow (cfs)"], errors='coerce')
        #  missing_records["flow (in/hr)"] = pd.to_numeric(missing_records["flow (in/hr)"], errors='coerce')


         missing_target_cols = ["flow (cfs)", "flow (in/hr)"]
         m_cols = [col for col in target_cols if col in missing_records.columns]
         # Convert all target columns to floats, converting text/errors to NaN
        #  missing_records[m_cols] = missing_records[m_cols].apply(pd.to_numeric, errors='coerce')
         missing_records[m_cols] = missing_records[m_cols].astype(float)
         is_zero = missing_records["flow (cfs)"] == float(0)
         zero_count = is_zero.sum()
         

         # Keep rows where AT LEAST ONE column is not effectively zero and not missing
         filtered_missing = missing_records[(missing_records[m_cols].abs() > 1e-5).any(axis=1)] 
         # Strip down the filter to just the flow column
         missing_records["flow (cfs)"] = pd.to_numeric(missing_records["flow (cfs)"], errors='coerce')
         missing_records["time (min)"] = pd.to_numeric(missing_records["time (min)"], errors='coerce')
         filtered_missing = missing_records[((missing_records["flow (cfs)"].abs() > 1e-5) & (missing_records["time (min)"] != 1440))]




         print(f"{site} number of published entries: {num_entries}")
         print(site + f" number of mismatched entries: {not_matches:,}")
         print(site + f" number of mismatched entries == 0: {zero_count:,}")
         print(f"{site} % Dates Matched: {total_merged / num_entries * 100:,.2f}%")
         print(site + f" Total overlapping date/time entries: {total_merged:,}")
         print(site + f" Consistent values (flow matches s or l): {match_count:,}")
         print(site + f" Inconsistent values (Mismatches):     {incosistent_count:,}")
         print(f"{site} % Inconsistent Values (Mismatches): {incosistent_count / total_merged * 100:,.2f}%")
         print("\n")
         print("\n")


        #  print(filtered_missing)
        #  print("\n")
        #  print("\n")
    
    raw_export_dir = r"I:\programming\runoff\raw_logger_files"

    # for key, df in flows.items():
    #     file_path = os.path.join(raw_export_dir, f"{key}_filtered.csv")
    #     df.to_csv(file_path, index = False)
    #     print(f"Saved: {file_path}")


    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s)')



# with pd.ExcelWriter(r"I:\programming\runoff\raw_logger_files\daily_runoff.xlsx") as writer:
#     for i, site in enumerate(dataframes):
#         dataframe = dataframes[site]
#         dataframe.to_excel(writer, sheet_name = site, index = False)




