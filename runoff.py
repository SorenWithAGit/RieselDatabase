import pandas as pd
import numpy as np
from src import calculations as cal
from src import weatherFiles as wt

runoff_path = r"I:\USDA-ARS\Georgie\runoff\2019\sw12_2019.xls"
web_runoff = r"I:\USDA-ARS\Georgie\runoff\2019\daily_inches\sw12\rosw1219.dly"
time = 5
calcd = wt.read_excel
web_txt = wt.read_txt
df = calcd.read_subdly_runoff(runoff_path)
webro = web_txt.read_txt_runoff(web_runoff)
webro["in"] = webro["in"].astype(float)

rc = cal.runoff_calculator()
flow_df = rc.check_flow_calculator("SW12", time,  df)

subdaily_df = rc.calculated_runoff(flow_df, time)
# print(subdaily_df)

flow_sum = subdaily_df.set_index("date").resample("D")[["flow (in/hr)"]].sum()
# print(flow_sum)

daily_runoff = rc.calculate_comparison_runoff(webro, subdaily_df)
# print(daily_runoff)


sut = wt.read_txt
sutron = sut.read_sutron(r"I:\USDA-ARS\Kyle Tiner\Runoff Files\sutron2019\sutrondatfiles\SW12SHAFT.dat")
print(sutron)
raw_calc = rc.create_flow_calculator("SW12", 5, sutron)
raw_calc = raw_calc.iloc[:, [0, 1, 2, 5, 6, 7, 9, 10, 11]]
# print(flow_calcutaor)

raw_calc["date"] = pd.to_datetime(raw_calc["date"], format = "mixed")
rosw12 = raw_calc.set_index("date").resample("D")["raw runoff (mm)"].sum()
# print(rosw12)

daily_runoff = pd.merge(daily_runoff, rosw12, on = "date")
daily_runoff["JSKT:GEORGIE"] = daily_runoff["JSKT runoff (mm)"] / daily_runoff["Georgie runoff (mm)"]
daily_runoff["RAW:JSKT"] = daily_runoff["raw runoff (mm)"] / daily_runoff["JSKT runoff (mm)"]
daily_runoff["RAW:GEORGIE"] = daily_runoff["raw runoff (mm)"] / daily_runoff["Georgie runoff (mm)"]
print(daily_runoff)

with pd.ExcelWriter(r"I:\USDA-ARS\Merillyn Schantz\Riesel\Riesel Runoff\calculated_runoff\daily\sw12_2019.xlsx") as writer:
    subdaily_df.to_excel(writer, sheet_name = " Georgie SW12 2019 subdaily", index = True)
    raw_calc.to_excel(writer, sheet_name = "RAW SW12 2019 subdaily")
    daily_runoff.to_excel(writer, sheet_name = "SW12 Comparison", index = True)