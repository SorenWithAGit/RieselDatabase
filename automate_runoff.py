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
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


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
            flow_rate["date"] = pd.to_datetime(flow_rate["date"], format = "mixed")
            
        except Exception as e:
            print(f"Error processing {files[f]}: {e}")

    # print(flow_rate)
    
    return flow_rate


def automate_reported_runoff(site, root_folder):
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
            reported_ro["date"] = pd.to_datetime(reported_ro["date"], format = "mixed")

        except Exception as e:
                    print(f"Error processing {files[f]}: {e}")

    return reported_ro

def automate_merge(site, raw_dat_chunk, report_dat_chunk):
    raw_dat = raw_dat_chunk.copy()

    target_cols = [
    "discharge rate (cfs)", "runoff rate (in/hr)", "raw runoff (mm)", "raw runoff (in)",  
    "l discharge rate (cfs)", "l runoff rate (in/hr)", "l raw runoff (mm)", "l raw runoff (in)"
    ]

    f_cols = [c for c in target_cols if c in raw_dat.columns]

    raw_dat = raw_dat[(raw_dat[f_cols]).notna().any(axis=1)].round(4)

    report_dat = report_dat_chunk.copy()

    raw_dat["date"] = pd.to_datetime(raw_dat["date"], format = "mixed")
    report_dat["date"] = pd.to_datetime(report_dat["date"], format = "mixed")

    raw_dat["time (min)"] = (raw_dat["time (min)"]).astype(int)
    report_dat["time (min)"] = (report_dat["time (min)"]).astype(int)

    raw_dat["raw_index"] = raw_dat.index
    report_dat["report_index"] = report_dat.index

    merged_dat = pd.merge(
        report_dat[["report_index", "file_name", "line_num", "site", "date", "time (min)", "flow (cfs)"]],
        raw_dat[["date", "time (min)", "raw_index", "file_name", "line_num", "s level (ft)", "l level (ft)", "discharge rate (cfs)", "l discharge rate (cfs)"]],
        on = ["date", "time (min)"],
        how = "inner"
    )

    merged_dat = merged_dat.rename(columns = {
        "file_name_x" : "daren_file_name",
        "line_num_x" : "daren_line_num",
        "flow (cfs)" : "daren flow (cfs)",
        "file_name_y" : "raw_file_name",
        "line_num_y" : "raw_line_num",
        "s level (ft)" : "raw s level (ft)",
        "l level (ft)" : "raw l level (ft)",
        "discharge rate (cfs)" : "raw s discharge rate (cfs)",
        "l discharge rate (cfs)" : "raw l discharge rate (cfs)"
    })

    return merged_dat

def automate_l_q_check(comparison_df):
    # Fix the UnboundLocalError by initializing a default empty fallback
    l_q_comparison = pd.DataFrame()
    
    if comparison_df is not None and not comparison_df.empty:
        # Isolate the columns
        l_discharge = comparison_df["raw l discharge rate (cfs)"].astype(float)
        daren_flow = comparison_df["daren flow (cfs)"].astype(float)
        
        # 1. Check that it's not NaN
        not_nan_mask = l_discharge.notna()
        
        # 2. Use np.isclose with your 0.0005 tolerance instead of strict '=='
        # This protects against floating-point binary rounding discrepancies
        matching_mask = np.isclose(l_discharge, daren_flow, rtol=0.0005)
        
        # Combine the masks
        valid_mask = not_nan_mask & matching_mask
        
        # Slice out the matching rows safely
        l_q_comparison = comparison_df.loc[valid_mask].copy()
            
    return l_q_comparison

def automate_runoff_comparison(site, raw_root_folder, report_root_folder):
    raw_root_folder = r"I:\programming\runoff\raw_logger_files\\{site}"
    report_root_folder = r"I:\programming\runoff\daren_reported_runoff\\{site}"

    raw_results = automate_runoff(site, raw_root_folder)
    reported_results = automate_reported_runoff(site, report_root_folder)

    raw_results["date"] = pd.to_datetime(raw_results["date"], format = "mixed")
    reported_results["date"] = pd.to_datetime(reported_results["date"], format = "mixed")

    raw_results["time (min)"] = (raw_results["time (min)"]).astype(int)
    reported_results["time (min)"] = (reported_results["time (min)"]).astype(int)

    merged_data = automate_merge(site, raw_results, reported_results)

    flow = merged_data["daren flow (cfs)"].astype(float)
    discharge = merged_data["raw s discharge rate (cfs)"].astype(float)
    l_discharge = merged_data["raw l discharge rate (cfs)"].astype(float)
    is_consistent = (np.isclose(flow, discharge, rtol = 0.0005)) | (np.isclose(flow, l_discharge, rtol = 0.0005))

    comparison = merged_data.loc[is_consistent].copy()

    return comparison


def plot_runoff_comparison(site, comparison_df, output_folder = None):
                  dates = pd.to_datetime(comparison_df["date"], format = "mixed")
                  x_daren = comparison_df["daren flow (cfs)"].astype(float)
                  y_raw_s = comparison_df["raw s discharge rate (cfs)"].astype(float)
                  y_raw_l = comparison_df["raw l discharge rate (cfs)"].astype(float)

                  plt.figure(figsize=(10, 6))

                  plt.scatter(dates, x_daren, color='blue', alpha=0.6, edgecolors='none', 
                    label='daren discharge rate (cfs)')
                  plt.scatter(dates, y_raw_s, color='red', marker='D', alpha=0.7, edgecolors='none', 
                                      label='Raw s discharge Rate (cfs)')
                  plt.scatter(dates, y_raw_l, color='black', marker='D', alpha=0.7, edgecolors='none', 
                    label='Raw l discharge Rate (cfs)')

                  plt.title(f"Flow Correlation & Consistency Evaluation - Site {site}", fontsize=14, pad=15)
                  plt.xlabel("Date)", fontsize=11)
                  plt.ylabel("Discharge Rate (cfs)", fontsize=11)
                  plt.legend(loc='upper left', frameon=True)
                  plt.grid(True, linestyle='--', alpha=0.5)
                  plt.tight_layout()

                  if output_folder:
                    os.makedirs(output_folder, exist_ok=True)
                    save_path = os.path.join(output_folder, f"{site}/{site}_flow_comparison.png")
                    plt.savefig(save_path, dpi=300)
                    print(f"Saved visualization matrix to: {save_path}")
                    plt.close() # Instantly frees memory blocks
                  
                  else:
                    plt.show()

def plot_first_last_s_box(site, summary_df, save_filepath):
    """
    Generates side-by-side boxplots for First vs Last Large Discharge rates 
    plotted across each unique Date on the X-axis.
    """
    if summary_df is None or summary_df.empty:
        print(f"Skipping boxplot for Site {site}: No summary data available.")
        return

    if "date" not in summary_df.columns:
        local_df = summary_df.reset_index()
    else:
        local_df = summary_df.copy()

    # 1. Reshape ("melt") the data from wide to long format so Seaborn can group it
    # This transforms columns into rows categorized by an identifier column
    melted_df = local_df.melt(
        id_vars=["date"], 
        value_vars=["first_s_discharge", "last_s_discharge"],
        var_name="Discharge_Type", 
        value_name="Discharge_Rate"
    )

    # Convert the type labels to clean display labels
    melted_df["Discharge_Type"] = melted_df["Discharge_Type"].map({
        "first_s_discharge": "First S Discharge",
        "last_S_discharge": "Last S Discharge"
    })

    # Sort by date string or object to keep the timeline chronological on the axis
    melted_df = melted_df.sort_values("date")

    # 2. Initialize the plot layout workspace
    plt.figure(figsize=(12, 6))
    
    # 3. Use Seaborn to plot side-by-side boxplots grouped by Date
    sns.boxplot(
        data=melted_df,
        x="Discharge_Type",
        y="Discharge_Rate",
        hue="Discharge_Type",
        palette=["#1f77b4", "#ff7f0e"], # Custom Blue and Orange color scheme
        width=0.6
    )

    # 4. Clean up design labels and layout structure
    plt.title(f"Overall S Discharge Rate Distribution - Site {site}", fontsize=14, pad=15)
    plt.xlabel("Date", fontsize=11)
    plt.ylabel("s Discharge Rate (cfs)", fontsize=11)
    
    # Rotate the date text labels slightly if your dataset spans across many days
    plt.xticks(rotation=45, ha='right')
    
    plt.legend(title="Discharge Metrics", loc="upper left")
    plt.grid(True, linestyle='--', alpha=0.5, axis='y')
    plt.tight_layout()

    # 5. Handle automatic subfolder path creation safely
    save_path = os.path.join(save_filepath, f"{site}/{site}_l_s_overall_comparison.png")
    # os.makedirs(parent_folder, exist_ok=True)

    # Save to disk
    plt.savefig(save_path, dpi=300)
    print(f"Successfully saved timeline distribution boxplot to: {save_path}")
    plt.close() # Free graphics engine RAM blocks immediately

def plot_first_last_q_box(site, summary_df, save_filepath):
    """
    Generates side-by-side boxplots for First vs Last Large Discharge rates 
    plotted across each unique Date on the X-axis.
    """
    if summary_df is None or summary_df.empty:
        print(f"Skipping boxplot for Site {site}: No summary data available.")
        return

    if "date" not in summary_df.columns:
        local_df = summary_df.reset_index()
    else:
        local_df = summary_df.copy()

    # 1. Reshape ("melt") the data from wide to long format so Seaborn can group it
    # This transforms columns into rows categorized by an identifier column
    melted_df = local_df.melt(
        id_vars=["date"], 
        value_vars=["first_l_discharge", "last_l_discharge"],
        var_name="Discharge_Type", 
        value_name="Discharge_Rate"
    )

    # Convert the type labels to clean display labels
    melted_df["Discharge_Type"] = melted_df["Discharge_Type"].map({
        "first_l_discharge": "First L Discharge",
        "last_l_discharge": "Last L Discharge"
    })

    # Sort by date string or object to keep the timeline chronological on the axis
    melted_df = melted_df.sort_values("date")

    # 2. Initialize the plot layout workspace
    plt.figure(figsize=(12, 6))
    
    # 3. Use Seaborn to plot side-by-side boxplots grouped by Date
    sns.boxplot(
        data=melted_df,
        x="Discharge_Type",
        y="Discharge_Rate",
        hue="Discharge_Type",
        palette=["#1f77b4", "#ff7f0e"], # Custom Blue and Orange color scheme
        width=0.6
    )

    # 4. Clean up design labels and layout structure
    plt.title(f"Overall l Discharge Rate Distribution - Site {site}", fontsize=14, pad=15)
    plt.xlabel("Date", fontsize=11)
    plt.ylabel("l Discharge Rate (cfs)", fontsize=11)
    
    # Rotate the date text labels slightly if your dataset spans across many days
    plt.xticks(rotation=45, ha='right')
    
    plt.legend(title="Discharge Metrics", loc="upper left")
    plt.grid(True, linestyle='--', alpha=0.5, axis='y')
    plt.tight_layout()

    # 5. Handle automatic subfolder path creation safely
    save_path = os.path.join(save_filepath, f"{site}/{site}_l_Q_overall_comparison.png")
    # os.makedirs(parent_folder, exist_ok=True)

    # Save to disk
    plt.savefig(save_path, dpi=300)
    print(f"Successfully saved timeline distribution boxplot to: {save_path}")
    plt.close() # Free graphics engine RAM blocks immediately


if __name__ == "__main__":
    start = time.perf_counter()

    # sites = ["SW12"]
    sites = ["SW12", "SW17", "W1", "W6", "W10", "W12", "W13", "Y2", "Y6", "Y8", "Y10", "Y13", "Y14"]
    l_sites = ["W1", "W6", "W10", "Y2", "Y6", "Y8", "Y10"]

    with Pool() as pool:
        raw_root_folder = r"I:\programming\runoff\raw_logger_files\\{site}"
        report_root_folder = r"I:\programming\runoff\daren_reported_runoff\\{site}"

        comparison_args = raw_args = [(site, raw_root_folder, report_root_folder) for site in sites]
        comparison_results = pool.starmap(automate_runoff_comparison, comparison_args)

    comparisons = {site: [] for site in sites}

    for site, comparison in zip(sites, comparison_results):
             comparisons[site] = comparison          

             if site not in l_sites:
                print(f"--- Filtered Data for Site with no l Q: {site} ---")
                print(comparisons[site])

             elif site in l_sites:
                  print(f"--- Filtered Data for Site with matching l Q: {site} ---")
                  comparisons[site] = automate_l_q_check(comparisons[site])
                  print(comparisons[site])

                  summary_s_q_df = comparisons[site].groupby("date")["raw s discharge rate (cfs)"].agg(
                    first_s_discharge="first",
                    last_s_discharge="last"
                    )
                  print(f"--- First & last s Q: {site} ---")
                  summary_s_q_df = summary_s_q_df[(summary_s_q_df["first_s_discharge"] != float(0)) | (summary_s_q_df["last_s_discharge"] != float(0))]
                  print(summary_s_q_df)

                  summary_l_q_df = comparisons[site].groupby("date")["raw l discharge rate (cfs)"].agg(
                    first_l_discharge="first",
                    last_l_discharge="last"
                    )
                  print(f"--- First & last l Q: {site} ---")
                  summary_l_q_df = summary_l_q_df[(summary_l_q_df["first_l_discharge"] != float(0)) | (summary_l_q_df["last_l_discharge"] != float(0))]
                  print(summary_l_q_df)

                #   output = r"I:\programming\runoff\scatter_plots\daren_l_Q"
                #   plot_runoff_comparison(site, comparisons[site], output)

                  save_path = r"I:\programming\runoff\box_plots\daren_l_Q"
                  plot_first_last_s_box(site, summary_s_q_df, save_path)

                #   save_path = r"I:\programming\runoff\box_plots\daren_l_Q"
                #   plot_first_last_q_box(site, summary_l_q_df, save_path)


#          merged_dat = merges[site]
#          report_dat = reported_flows[site]
#          total_merged = len(merged_dat)
#          flow = merged_dat["daren flow (cfs)"].astype(float)
#          discharge = merged_dat["raw s discharge rate (cfs)"].astype(float)
#          l_discharge = merged_dat["raw l discharge rate (cfs)"].astype(float)
#          is_consistent = (np.isclose(flow, discharge, rtol = 0.0005)) | (np.isclose(flow, l_discharge, rtol = 0.0005))
#          match_count = is_consistent.sum()
#          incosistent_count = (~is_consistent).sum()
#          num_entries = len(report_dat["date"])
#          not_matches = num_entries - total_merged

#         #  print(merged_dat)
#         #  print("\n")
#         #  print("\n")

#          inconsistent_records = merged_dat[~is_consistent].copy()
#          inconsistent_records["daren flow (cfs)"] = pd.to_numeric(inconsistent_records["daren flow (cfs)"], errors='coerce')

#          c = cal.runoff_calculator()
#          inconsistent_records["daren s level (ft)"] = c.calculate_level(inconsistent_records["daren flow (cfs)"], site)[0].copy()
#          inconsistent_records["daren l level (ft)"] = c.calculate_level(inconsistent_records["daren flow (cfs)"], site)[1].copy()
#         #  inconsistent_records = inconsistent_records.iloc[:,[0,1,2,3,4,5,13,14,6,7,8,9,10,11,12]]
#          inconsistent_records = inconsistent_records.loc[:,["report_index", "daren_file_name", "daren_line_num", "site", "date",
#                                                             "time (min)", "daren s level (ft)", "daren l level (ft)", "daren flow (cfs)", "raw_file_name",
#                                                             "raw_line_num", "raw s level (ft)", "raw l level (ft)", "raw s discharge rate (cfs)", 
#                                                             "raw l discharge rate (cfs)"]]
#          print(inconsistent_records)

#          inconsistent_export = r"I:\programming\runoff\mismatched_data"

#         #  file_path = os.path.join(inconsistent_export, site + "_mismatched.csv")
#         #  inconsistent_records.to_csv(file_path, index = False)
#         #  print(f"Saved: {file_path}")

#          missing_records = report_dat[~report_dat.index.isin(merged_dat["report_index"])].copy()

#         #  print(missing_records)

#         #  missing_records["flow (cfs)"] = pd.to_numeric(missing_records["flow (cfs)"], errors='coerce')
#         #  missing_records["flow (in/hr)"] = pd.to_numeric(missing_records["flow (in/hr)"], errors='coerce')


#          missing_target_cols = ["flow (cfs)", "flow (in/hr)"]
#          m_cols = [col for col in target_cols if col in missing_records.columns]
#          # Convert all target columns to floats, converting text/errors to NaN
#         #  missing_records[m_cols] = missing_records[m_cols].apply(pd.to_numeric, errors='coerce')
#          missing_records[m_cols] = missing_records[m_cols].astype(float)
#          is_zero = missing_records["flow (cfs)"] == float(0)
#          zero_count = is_zero.sum()
         

#          # Keep rows where AT LEAST ONE column is not effectively zero and not missing
#          filtered_missing = missing_records[(missing_records[m_cols].abs() > 1e-5).any(axis=1)] 
#          # Strip down the filter to just the flow column
#          missing_records["flow (cfs)"] = pd.to_numeric(missing_records["flow (cfs)"], errors='coerce')
#          missing_records["time (min)"] = pd.to_numeric(missing_records["time (min)"], errors='coerce')
#          filtered_missing = missing_records[((missing_records["flow (cfs)"].abs() > 1e-5) & (missing_records["time (min)"] != 1440))]




#          print(f"{site} number of published entries: {num_entries}")
#          print(site + f" number of mismatched entries: {not_matches:,}")
#          print(site + f" number of mismatched entries == 0: {zero_count:,}")
#          print(f"{site} % Dates Matched: {total_merged / num_entries * 100:,.2f}%")
#          print(site + f" Total overlapping date/time entries: {total_merged:,}")
#          print(site + f" Consistent values (flow matches s or l): {match_count:,}")
#          print(site + f" Inconsistent values (Mismatches):     {incosistent_count:,}")
#          print(f"{site} % Inconsistent Values (Mismatches): {incosistent_count / total_merged * 100:,.2f}%")
#          print("\n")
#          print("\n")


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




