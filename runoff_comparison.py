import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MultipleLocator
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

raw_excel = r"I:\programming\runoff\raw_logger_files\runoff_clalculated_from_raw.xlsx"
web_excel = r"I:\programming\runoff\raw_logger_files\web_runoff_2006-2019.xlsx"

# dataframes = {
#     "SW12" : [],
#     "SW17" : [],
#     "W1" : [],
#     "W6" : [],
#     "W10" : [],
#     "W12" : [],
#     "W13" : [],
#     "Y2" : [],
#     "Y6" : [],
#     "Y8" : [],
#     "Y10" : [],
#     "Y13" : [],
#     "Y14" : []
# }

# sites = ["SW12", "SW17", "W1", "W6", "W10", "W12", "W13", "Y2", "Y6", "Y8", "Y10", "Y13", "Y14"]
# year = 2009

# for site in sites:
#     df = pd.read_excel(web_excel, sheet_name = site)
#     try:
#         df = df.rename(columns = {"datetime" : "date", "raw runoff (mm)" : "runoff (mm)"})
#     except:
#         pass
#     df["datetime"] = pd.to_datetime(df["date"])
#     df = df[df["datetime"].dt.year == year]
#     dataframes[site] = df


# year_series = {
#     key: df.loc[df["runoff (mm)"] >0.002, "runoff (mm)"]
#     for key, df in dataframes.items()
# }

# combined_df = pd.concat(year_series, axis = 1)

# df_melted = combined_df.melt(var_name = "DataFrame_Name", value_name = "Values")


# plt.figure(figsize=(14, 6))  # Extra width to fit all 13 labels easily

# ax = sns.boxplot(
#     data=df_melted, 
#     x='DataFrame_Name', 
#     y='Values', 
#     palette='viridis' 
# )

# ax.yaxis.set_major_locator(MultipleLocator(10))

# plt.title("Web Distrobution " + str(year), fontsize=14, pad=15)
# plt.xlabel('Site', fontsize=12)
# plt.ylabel('Runoff (mm)', fontsize=12)
# plt.xticks(rotation=45)  
# plt.grid(axis='y', linestyle='--', alpha=0.5)  
# plt.tight_layout()  
# plt.ylim(-2.5, 64.5)

# plt.show()


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


# plt.figure(figsize=(14,6)) 

# ax = sns.boxplot(
#     data=df_melted, 
#     x='DataFrame_Name', 
#     y='Values', 
#     palette='viridis',  
    
# )

# ax.yaxis.set_major_locator(MultipleLocator(20))

# # 5. Styling adjustments
# plt.title("Web Distrobution " + str(site), fontsize=14, pad=15)
# plt.xlabel('Year', fontsize=12)
# plt.ylabel('Runoff (mm)', fontsize=12)
# plt.xticks(rotation=45)  
# plt.grid(axis='y', linestyle='--', alpha=0.5)  
# plt.tight_layout() 
# plt.ylim(0, 105)

# plt.show()


year = 2008
sites = ["SW12", "SW17", "W1", "W6", "W10", "W12", "W13", "Y2", "Y6", "Y8", "Y10", "Y13", "Y14"]
# site = "SW12"
for site in sites:
    web_df = pd.read_excel(web_excel, sheet_name = site)
    # try:
    #     web_df = web_df.rename(columns = {"datetime" : "date", "web runoff (mm)" : "runoff (mm)"})
    # except:
    #     pass
    # web_df["datetime"] = pd.to_datetime(web_df["date"])
    # web_df = web_df[web_df["date"].dt.year == year]  
    web_df = web_df.rename(columns = {"runoff (in)" : "web runoff (in)",
                                    "runoff (mm)" : "web runoff (mm)"})
    # print(web_df)


    raw_df = pd.read_excel(raw_excel, sheet_name = site)
    try:
        raw_df = raw_df.rename(columns = {"datetime" : "date", "raw runoff (mm)" : "runoff (mm)"})
    except:
        pass
    # print(raw_df)
    # raw_df["datetime"] = pd.to_datetime(raw_df["date"])
    # raw_df = raw_df[raw_df["date"].dt.year == year]  
    raw_df = raw_df.rename(columns = {"runoff (in)" : "raw runoff (in)", 
                                    "runoff (mm)" : "raw runoff (mm)"})
    print(raw_df)

    dates = pd.date_range(start = f"{year}-01-01", end = f"{year}-12-31", freq = "D")

    combined_df = pd.merge(web_df, raw_df, on = "date", how = "inner")
    # print(combined_df)
    series_web = combined_df[combined_df["web runoff (mm)"] != 0]
    sereies_raw = combined_df[combined_df["raw runoff (mm)"] != 0]

    x_web = combined_df["web runoff (mm)"].squeeze()
    y_web = combined_df["raw runoff (mm)"].squeeze()
    
    axis_min = min(x_web.min(), y_web.min())
    axis_max = max(x_web.max(), y_web.max())
    one_to_one = [axis_min, axis_max]

    slope, intercept = np.polyfit(x_web, y_web, 1)
    correlation_matrix = np.corrcoef(x_web, y_web)
    r_squared = correlation_matrix[0, 1] ** 2

    linear_eq = f"$y_web = {slope:.2f}x + {intercept:.24}$\nR^2 = {r_squared:.3f}"

    plt.figure(figsize = (10, 5))
    # plt.scatter(series_web["date"], series_web["web runoff (mm)"], color = "blue", label = "web runoff (mm)")
    # plt.scatter(sereies_raw["date"], sereies_raw["raw runoff (mm)"], color = "red", label = "raw runoff (mm)")

    plt.scatter(x_web, y_web, color = "red", label = "raw runoff (mm)")
    # plt.plot(x_web, slope * x_web + intercept, color = "blue", linestyle = "--")

    plt.plot(one_to_one, one_to_one, color = "black", label = "1:1 runoff (mm)")

    # plt.gca().text(0.05, 0.95, linear_eq, transform=plt.gca().transAxes,
    #         fontsize=12, verticalalignment='top', 
    #         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.xlabel("web runoff (mm)")
    plt.ylabel("Raw Runoff (mm)")
    plt.title(site + " Runoff: Web Data vs Calculated Data")
    plt.legend(loc = "upper left")
    plt.grid(True, linestyle = ":", alpha = 0.6)
    plt.show()