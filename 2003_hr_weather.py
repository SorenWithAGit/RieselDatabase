from src import weatherFiles as wf
import pandas as pd


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

daily_dw03 = dw03.groupby(pd.Grouper(key = "DATETIME", freq = "D"))[["TGAD", "TMAX", "TMIN", "RHMXD",
                                                                   "RHUMD", "SRAD", "WIND", "WINDDIR",
                                                                   "WMAX", "RAIN", "STAVG", "STMAX", "STMIN"]].mean()


neg_daily_dw03 = daily_dw03[(daily_dw03["STMIN"] < 2.5)]
# print(neg_daily_dw03)
# print(len(neg_daily_dw03))

for week_start_date, weekly_data in daily_dw03.groupby(pd.Grouper(freq = "W")):
    print("Start of weeK: " + str(week_start_date))
    print(weekly_data)
    print("\n")