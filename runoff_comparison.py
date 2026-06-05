import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator

raw_excel = r"I:\programming\runoff\raw_logger_files\runoff_clalculated_from_raw.xlsx"
web_excel = r"I:\programming\runoff\raw_logger_files\web_runoff_2006-2019.xlsx"

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
year = 2009

for site in sites:
    df = pd.read_excel(web_excel, sheet_name = site)
    try:
        df = df.rename(columns = {"datetime" : "date", "raw runoff (mm)" : "runoff (mm)"})
    except:
        pass
    df["datetime"] = pd.to_datetime(df["date"])
    df = df[df["datetime"].dt.year == year]
    dataframes[site] = df


year_series = {
    key: df.loc[df["runoff (mm)"] >0.002, "runoff (mm)"]
    for key, df in dataframes.items()
}

combined_df = pd.concat(year_series, axis = 1)

df_melted = combined_df.melt(var_name = "DataFrame_Name", value_name = "Values")


plt.figure(figsize=(14, 6))  # Extra width to fit all 13 labels easily

# Plotting with a clean, built-in color palette
ax = sns.boxplot(
    data=df_melted, 
    x='DataFrame_Name', 
    y='Values', 
    palette='viridis'  # Try 'coolwarm', 'Set3', or 'plasma' for different looks
)

ax.yaxis.set_major_locator(MultipleLocator(10))

# 5. Styling adjustments
plt.title("Web Distrobution " + str(year), fontsize=14, pad=15)
plt.xlabel('Site', fontsize=12)
plt.ylabel('Runoff (mm)', fontsize=12)
plt.xticks(rotation=45)  # Rotates labels 45 degrees so they do not overlap
plt.grid(axis='y', linestyle='--', alpha=0.5)  # Adds clean, faint gridlines
plt.tight_layout()  # Fixes any edge clipping issues
plt.ylim(-2.5, 64.5)

plt.show()


# year_dfs = {
#     "2006" : [],
#     "2007" : [],
#     "2008" : [],
#     "2009" : [],
#     "2010" : [],
#     "2011" : [],
#     "2012" : [],
#     "2013" : [],
#     "2014" : [],
#     "2015" : [],
#     "2016" : [],
#     "2017" : [],
#     "2019" : []
# }

# years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2019,]
# site = "SW12"

# for year in years:
#     df = pd.read_excel(web_excel, sheet_name = site)
#     try:
#         df = df.rename(columns = {"datetime" : "date", "raw runoff (mm)" : "runoff (mm)"})
#     except:
#         pass
#     # print(df)
#     df = df[df["date"].dt.year == year]
#     year_dfs[str(year)] = df
#     # print(year_dfs[str(year)])

# year_series = {
#     key: df.loc[df["runoff (mm)"] >0.002, "runoff (mm)"]
#     for key, df in year_dfs.items()
# }

# combined_df = pd.concat(year_series, axis = 1)

# df_melted = combined_df.melt(var_name = "DataFrame_Name", value_name = "Values")


# plt.figure(figsize=(14,6))  # Extra width to fit all 13 labels easily

# # Plotting with a clean, built-in color palette
# ax = sns.boxplot(
#     data=df_melted, 
#     x='DataFrame_Name', 
#     y='Values', 
#     palette='viridis',  # Try 'coolwarm', 'Set3', or 'plasma' for different looks
    
# )

# ax.yaxis.set_major_locator(MultipleLocator(20))

# # 5. Styling adjustments
# plt.title("Web Distrobution " + str(site), fontsize=14, pad=15)
# plt.xlabel('Year', fontsize=12)
# plt.ylabel('Runoff (mm)', fontsize=12)
# plt.xticks(rotation=45)  # Rotates labels 45 degrees so they do not overlap
# plt.grid(axis='y', linestyle='--', alpha=0.5)  # Adds clean, faint gridlines
# plt.tight_layout()  # Fixes any edge clipping issues
# plt.ylim(0, 105)

# plt.show()