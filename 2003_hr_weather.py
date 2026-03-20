from src import weatherFiles as wf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


rt = wf.read_txt
dw03 = rt.read_hr_weather(r"I:\programming\python\riesel_file_checker\Harmel\Hourly weather\2003ries.txt")
# print(dw03.dtypes)

dw03["HOUR"] = dw03["HOUR"].replace("2400, 0000")
dw03["padded_time"] = dw03["HOUR"].str.zfill(4)
dw03["padded_time"] = dw03["padded_time"].replace("2400", "0000")
dw03["time"] = pd.to_datetime(dw03["padded_time"], format = "%H%M", errors = "coerce").dt.time
dw03["time"] = dw03["time"].astype("str")
dw03["DATETIME"] = (dw03["DOY"] + " " + dw03["time"]).str.strip()
dw03["DATETIME"] = pd.to_datetime(dw03["DATETIME"], format = "%Y-%m-%d %H:%M:%S", errors = "coerce")
dw03 = dw03.iloc[:, [19, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]

num_vals = len(dw03["STMIN"])
neg_STMIN_vals = (dw03["STMIN"] < 0).sum()
print("\n")
print("Number of negative STMIN values: " + str(neg_STMIN_vals))
print("STMIN values negative: " + str(f"{neg_STMIN_vals/num_vals*100:.2f}") + "%")

print("\n")

neg_STMAX_vals = (dw03["STMAX"] < 0).sum()
print("Number of negative STMAX values: " + str(neg_STMAX_vals))
print("STMAX values negative: " + str(f"{neg_STMAX_vals/num_vals*100:.2f}") + "%")
print("\n")

neg_ST = dw03[(dw03["STMIN"] < 0)]
# print(neg_ST)
# print("\n")

neg_air = dw03[(dw03["TGAD"] < 0)]
# print(neg_air)

daily_dw03 = dw03.groupby(pd.Grouper(key = "DATETIME", freq = "D"))[["TGAD", "TMAX", "TMIN", "RHMXD",
                                                                   "RHUMD", "SRAD", "WIND", "WINDDIR",
                                                                   "WMAX", "RAIN", "STAVG", "STMAX", "STMIN"]].mean()
# daily_dw03 = daily_dw03.reset_index()
# print(daily_dw03)

neg_daily_dw03 = daily_dw03[(daily_dw03["STMIN"] < 2.5)]
# print(neg_daily_dw03)
# print(len(neg_daily_dw03))

# for week_start_date, weekly_data in daily_dw03.groupby(pd.Grouper(freq = "W")):
#     print("Start of weeK: " + str(week_start_date))
#     print(weekly_data)
#     print("\n")

# Scatter Plot of DATE vs STMIN

# x = daily_dw03.index
# y = daily_dw03["STMIN"]

# plt.scatter(x, y)
# plt.xlabel("DATE")
# plt.ylabel("SOIL TEMP MIN")
# plt.show()


# Scatter Plot of TGAD vs STMIN

at = daily_dw03["TGAD"][daily_dw03["TGAD"].notna()]
st = daily_dw03["STMIN"][daily_dw03["STMIN"].notna()]
m, b = np.polyfit(at, st, 1)
# print("intercept of line: " + str(b))
# print("slope of line: " + str(m))


# plt.scatter(at, st)
# plt.plot(at, 3.5*m*at + b + 7, color = "steelblue", linestyle = "--", linewidth = 2)
# plt.xlabel("AVG TEMP")
# plt.ylabel("SOIL TEMP MIN")
# plt.show()

best_fit_st = m*at + b
filtered_data = [(ati, sti) for ati, sti, fyi in zip(at, st, best_fit_st) if sti >= fyi]
f_at, f_st = zip(*filtered_data)
f_at_array = np.array(f_at)
f_st_array = np.array(f_st)
# print(len(f_at))

mi, bi = np.polyfit(f_at, f_st, 1)
best_fit_sti = mi*f_at_array + bi

# plt.scatter(f_at_array, f_st_array)
# plt.plot(f_at_array, mi*f_at_array + bi, color = "steelblue", linestyle = "--", linewidth = 2)
# plt.xlabel("AVG TEMP")
# plt.ylabel("SOIL TEMP MIN")
# plt.show()


# Histogram of STMIN

# plt.hist(daily_dw03["STMIN"], bins = 30, color = "skyblue")
# plt.show()

dw03["STMIN_mask"] = dw03["STMIN"].mask(dw03["STMIN"] < (5*m*dw03["TGAD"] + b+2), np.nan)
# print(dw03)

t = dw03["TGAD"]
fst = dw03["STMIN_mask"]

# plt.scatter(t,fst)
# plt.xlabel("Average Temperature")
# plt.ylabel("Filtered Soil Temp")
# plt.show()

new_daily = dw03.groupby(pd.Grouper(key = "DATETIME", freq = "D"))[["TGAD", "TMAX", "TMIN", "RHMXD",
                                                                   "RHUMD", "SRAD", "WIND", "WINDDIR",
                                                                   "WMAX",
                                                                   "RAIN", "STAVG", "STMAX", 
                                                                   "STMIN", "STMIN_mask"]].mean()

# for week_start_date, weekly_data in new_daily.groupby(pd.Grouper(freq = "W")):
#     print("Start of weeK: " + str(week_start_date))
#     print(weekly_data)
#     print("\n")



new_dt = new_daily["TGAD"][new_daily["STMIN_mask"].notna()]
new_dst = new_daily["STMIN_mask"][new_daily["STMIN_mask"].notna()]

new_m, new_b = np.polyfit(new_dt, new_dst, 1)

# plt.scatter(new_dt, new_dst)
# plt.plot(new_dt,new_m *new_dt + new_b, color = "steelblue", linestyle = "--", linewidth = 2)
# plt.xlabel("Daily Average Temperature")
# plt.ylabel("Daily Soil Temp Min")
# plt.show()


t = daily_dw03["TGAD"][daily_dw03["STMAX"].notna()]
stm = daily_dw03["STMAX"][daily_dw03["STMAX"].notna()]

m_stm, b_stm = np.polyfit(t, stm, 1)

# plt.scatter(t, stm)
# plt.plot(0.95*t,m_stm*t + b_stm+7, color = "steelblue", linestyle = "--", linewidth = 2)
# plt.xlabel("Daily Average Soil Temp")
# plt.ylabel("Daily Soil Temp Max")
# plt.show()

dw03["STMAX_mask"] = dw03["STMAX"].mask(dw03["STMAX"] < (0.95*m_stm*dw03["TGAD"] + b_stm+7), np.nan)

new_daily = dw03.groupby(pd.Grouper(key = "DATETIME", freq = "D"))[["TGAD", "TMAX", "TMIN", "RHMXD",
                                                                   "RHUMD", "SRAD", "WIND", "WINDDIR",
                                                                   "WMAX",
                                                                   "RAIN", "STAVG", "STMAX", 
                                                                   "STMIN", "STMAX_mask", "STMIN_mask"]].mean()


ti = new_daily["TGAD"][new_daily["STMAX_mask"].notna()]
stmi = new_daily["STMAX_mask"][new_daily["STMAX_mask"].notna()]

m_stmi, b_stmi = np.polyfit(ti, stmi, 1)

# plt.scatter(ti, stmi)
# plt.plot(ti, m_stmi*ti + b_stmi, color = "steelblue", linestyle = "--", linewidth = 2)
# plt.xlabel("Daily Avg Temp")
# plt.ylabel("Daily STMAX")
# plt.show()

ta = new_daily["TGAD"][new_daily["STAVG"].notna()]
sta = new_daily["STAVG"][new_daily["STAVG"].notna()]

m_sta, b_sta = np.polyfit(ta, sta, 1)

# plt.scatter(ta, sta)
# plt.plot(ta, 1.8*m_sta*ta + 2+ b_sta, color = "steelblue", linestyle = "--", linewidth = 2)
# plt.xlabel("Air Temperature")
# plt.ylabel("Soil Temp Avg")
# plt.show()

dw03["STAVG_mask"] = dw03["STAVG"].mask(dw03["STAVG"] < (1.8*m_sta*dw03["TGAD"] + b_sta+2), np.nan)

new_daily = dw03.groupby(pd.Grouper(key = "DATETIME", freq = "D"))[["TGAD", "TMAX", "TMIN", "RHMXD",
                                                                   "RHUMD", "SRAD", "WIND", "WINDDIR",
                                                                   "WMAX",
                                                                   "RAIN", "STAVG", "STMAX", 
                                                                   "STMIN", 
                                                                   "STAVG_mask", "STMAX_mask", "STMIN_mask"]].mean()

new_daily = new_daily.round(2)

tai = new_daily["TGAD"][new_daily["STAVG_mask"].notna()]
stai = new_daily["STAVG_mask"][new_daily["STAVG_mask"].notna()]

m_stai, b_stai = np.polyfit(tai, stai, 1)

# plt.scatter(tai, stai)
# plt.plot(tai, m_stai*tai + b_stai, color = "steelblue", linestyle = "--", linewidth = 2)
# plt.xlabel("Daily Avg Air Temp")
# plt.ylabel("Daily Average STAVG")
# plt.show()

dstm = new_daily["STMAX_mask"][new_daily["STAVG_mask"].notna()]
dsta = new_daily["STAVG_mask"][new_daily["STAVG_mask"].notna()]

# plt.scatter(dstm, dsta)
# plt.xlabel("Daily STMAX")
# plt.ylabel("Daily STAVG")
# plt.show()

dw03 = dw03.set_index("DATETIME")

new_daily["#STAVG"] = dw03["STAVG_mask"].resample("D").count()
new_daily["#STMAX"] = dw03["STMAX_mask"].resample("D").count()
new_daily["#STMIN"] = dw03["STMIN_mask"].resample("D").count()

for week_start_date, weekly_data in new_daily.groupby(pd.Grouper(freq = "W")):
    print("Start of weeK: " + str(week_start_date))
    print(weekly_data.iloc[:,[0,1,2,9,10,11,12,13,14,15,16,17,18]])
    print("\n")