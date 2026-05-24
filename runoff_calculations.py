import pandas as pd
import numpy as np
from src import calculations as cal
from src import weatherFiles as wt

runoff_path = r"I:\USDA-ARS\Georgie\runoff\2019\y2_2019.xls"
web_runoff = r"I:\USDA-ARS\Georgie\runoff\2019\daily_inches\y2\roy219.dly"
calcd = wt.read_excel
web_txt = wt.read_txt
df = calcd.read_subdly_runoff(runoff_path)
webro = web_txt.read_txt_runoff(web_runoff)
webro["in"] = webro["in"].astype(float)
# print(webro)
# print(df["level (ft)"].shape)

rc = cal.runoff_calculator()
time = 10
new_df = rc.flow_calculator("Y2", time,  df)
# new_df["runoff (in)"] = new_df["new in/hr"] * .817
new_df["date"] = pd.to_datetime(new_df[["year", "month", "day"]])
# print(new_df)
daily_df = new_df.iloc[:, [0, 11, 4, 5, 6, 8, 7, 9, 10]]
# print(daily_df)

flow_sum = daily_df.set_index("date").resample("D")[["flow (in/hr)"]].sum()
# print(flow_sum)

t = rc.calculate_delta_t(webro, flow_sum)
# print(t)
t["daily (in)"] = t["flow (in/hr)"] * t["delta_t"]
average_t = t[t["delta_t"] != 0]["delta_t"].mean()
# print(average_t)

daily_df["runoff (in)"] = daily_df["new in/hr"] * (time/60)
daily_df = daily_df.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]]
print(daily_df)

runoff_sum = daily_df.set_index("date").resample("D")["runoff (in)"].sum()
jskt_runoff = daily_df.set_index("date").resample("D")["JSKT runoff (mm)"].sum()
# print(jskt_runoff)

comparison_runoff = pd.merge(webro, runoff_sum, on = "date")
comparison_runoff = pd.merge(comparison_runoff, t, on = "date")
# print(comparison_runoff)

comparison_runoff["georgie runoff (mm)"] = comparison_runoff["in_x"] * 25.4

comparison_runoff = pd.merge(comparison_runoff, jskt_runoff, on = "date")

comparison_runoff = comparison_runoff.iloc[:, [0, 1, 7, 4, 2, 8, 9, 10]]
comparison_runoff = comparison_runoff.rename(columns = {"site_x" : "site",
                                                        "delta_t": "calculated time (hr)",
                                                        "in_x" : "georgie runoff (in)", 
                                                        "daily (in)" : "recalculated georgie (in)"})
comparison_runoff["georgie:john"] = comparison_runoff["georgie runoff (mm)"] / comparison_runoff["JSKT runoff (mm)"]
print(comparison_runoff)



# with pd.ExcelWriter(r"I:\USDA-ARS\Merillyn Schantz\Riesel\Riesel Runoff\calculated_runoff\daily\y2_2019.xlsx") as writer:
#     daily_df.to_excel(writer, sheet_name = "y2 2017 subdaily", index = True)
#     comparison_runoff.to_excel(writer, sheet_name = "y2 2017 daily", index = True)