import pandas as pd
import numpy as np
from src import calculations as cal
from src import weatherFiles as wt

runoff_path = r"I:\USDA-ARS\Georgie\runoff\2019\y2_2019.xls"
web_runoff = r"I:\USDA-ARS\Georgie\runoff\2019\daily_inches\y2\roy219.dly"
time = 10
calcd = wt.read_excel
web_txt = wt.read_txt
df = calcd.read_subdly_runoff(runoff_path)
webro = web_txt.read_txt_runoff(web_runoff)
webro["in"] = webro["in"].astype(float)

rc = cal.runoff_calculator()
flow_df = rc.flow_calculator("Y2", time,  df)

subdaily_df = rc.calculate_runoff(flow_df, time)
print(subdaily_df)

flow_sum = subdaily_df.set_index("date").resample("D")[["flow (in/hr)"]].sum()
# print(flow_sum)

daily_runoff = rc.calculate_daily_runoff(webro, subdaily_df)
print(daily_runoff)


with pd.ExcelWriter(r"I:\USDA-ARS\Merillyn Schantz\Riesel\Riesel Runoff\calculated_runoff\daily\y2_2019.xlsx") as writer:
    subdaily_df.to_excel(writer, sheet_name = "y2 2017 subdaily", index = True)
    daily_runoff.to_excel(writer, sheet_name = "y2 2017 daily", index = True)