import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from src import calculations as cal
from src import weatherFiles as wt

runoff_path = r"\\ARS-DATA\Teams\Riesel.Team\Georgie\runoff\2019\w1_2019.xls"
web_runoff = r"\\ARS-DATA\Teams\Riesel.Team\Georgie\runoff\2019\daily_inches\w1\row119.dly"
sutron_path = r"I:\USDA-ARS\Kyle Tiner\Runoff Files\sutron2019\sutrondatfiles\W1SHAFT.DAT"
site = "W1"
year = 2019
output_str = r"I:\USDA-ARS\Merillyn Schantz\Riesel\Riesel Runoff\calculated_runoff\daily\\" + site + "_" + str(year) + ".xlsx"
calcd = wt.read_excel
web_txt = wt.read_txt
df = calcd.read_subdly_runoff(runoff_path)
webro = web_txt.read_txt_runoff(web_runoff)
webro["in"] = webro["in"].astype(float)

rc = cal.runoff_calculator()
flow_df = rc.check_flow_calculator(site, df)

subdaily_df = rc.calculated_runoff(site, flow_df)
# print(subdaily_df)

flow_sum = subdaily_df.set_index("date").resample("D")[["flow (in/hr)"]].sum()
# print(flow_sum)

daily_runoff = rc.calculate_comparison_runoff(webro, subdaily_df)
# print(daily_runoff)


sut = wt.read_txt
sutron = sut.read_sutron(sutron_path)
print(sutron)
raw_calc = rc.create_flow_calculator(site, sutron)
raw_calc = raw_calc.iloc[:, [0, 1, 2, 5, 6, 7, 9, 10, 11]]
# print(flow_calcutaor)

raw_calc["date"] = pd.to_datetime(raw_calc["date"], format = "mixed")
raw_daily = raw_calc.set_index("date").resample("D")["raw runoff (mm)"].sum()
# print(rosw12)

daily_runoff = pd.merge(daily_runoff, raw_daily, on = "date")
daily_runoff["JSKT:GEORGIE"] = daily_runoff["JSKT runoff (mm)"] / daily_runoff["Georgie runoff (mm)"]
daily_runoff["RAW:JSKT"] = daily_runoff["raw runoff (mm)"] / daily_runoff["JSKT runoff (mm)"]
daily_runoff["RAW:GEORGIE"] = daily_runoff["raw runoff (mm)"] / daily_runoff["Georgie runoff (mm)"]
print(daily_runoff)

x = np.array(daily_runoff["date"])
xi = np.array(daily_runoff["Georgie runoff (mm)"])
y = np.array(daily_runoff["Georgie runoff (mm)"])
yi = np.array(daily_runoff["JSKT runoff (mm)"])
yii = np.array(daily_runoff["raw runoff (mm)"])

mask = y != 0
maski = yi != 0
maskii = yii != 0
fig, ax = plt.subplots()

# ax.scatter(x[mask], y[mask], color = "red", label = "Georgie")
# ax.scatter(x[maski], yi[maski], color = "blue", label = "JSKT")
# ax.scatter(x[maskii], yii[maskii], color = "black", label = "RAW")
# ax.set_title("Runoff")
# ax.set_xlabel("Date")
# ax.set_ylabel("Runoff (mm)")
# ax.legend()

ax.scatter(x[mask], y[mask], color = "red", label = "Georgie")
ax.scatter(xi[maski], yi[maski], color = "blue", label = "JSKT")
ax.scatter(xi[maskii], yii[maskii], color = "black", label = "RAW")
ax.set_title("Runoff")
ax.set_xlabel("Georgie runoff (mm)")
ax.set_ylabel("Calculated Runoff (mm)")
ax.legend()


# sns.boxplot(x = y, color = "skyblue")
# plt.xlabel("Runoff (mm)")
# plt.title("Spread of Values")
# plt.grid(True, which = "both", linestyle = "--")
# plt.tight_layout
plt.show()

print("Georgie runoff min (mm)" + str(min(y[mask])))
print("Georgie runoff max (mm)" + str(max(y[mask])))

me = rc.calculate_max_error(daily_runoff)
print("Georgie v JSKT max error: " + str(me[0]) + "\n" \
      + "Georgie v RAW max error: " + str(me[1]))


rmse = rc.calculate_rmse(daily_runoff)
print("Georgie v JSKT RMSE: " + str(rmse[0]) + "\n" \
      + "Georgie v RAW RMSE: " + str(rmse[1]) + "\n" \
        + "RAW v JSKT RMSE: " + str(rmse[2]))

# with pd.ExcelWriter(output_str) as writer:
#     subdaily_df.to_excel(writer, sheet_name = "Georgie " + site + " " + str(year) + " subdaily", index = True)
#     raw_calc.to_excel(writer, sheet_name = "RAW" + site + " " + str(year) + " subdaily", index = True)
#     daily_runoff.to_excel(writer, sheet_name = site + " " + str(year) + " Comparison", index = True)