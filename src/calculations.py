import pandas as pd
import numpy as np

class runoff_calculator():

    def __init__(self):
            self.s_per_min = 60
            self.min_per_hr = 60
            self.s_per_hr = 3600
            self.min_per_day = 1440
            self.in_per_ft = 12
            self.mm_per_in = 25.4
            self.ft2_per_acre = 43560
            self.field_constants = {
                                    "area (ac)" :{
                                            "SW12" : 2.97,
                                            "SW17" : 2.99,
                                            "W1" : 174.00,
                                            "W6" : 42.30,
                                            "W10" : 19.80,
                                            "W12" : 9.90,
                                            "W13" : 11.30,
                                            "Y2" : 132.00,
                                            "Y6" : 16.30,
                                            "Y8" : 20.80,
                                            "Y10" : 18.50,
                                            "Y13" : 11.40,
                                            "Y14" : 5.60
                                    },
                                    "flow constants" : {
                                            "SW12" : [[1.93, 1.755], [2.371, 1.93], [2.574, 2.088], [2.488, 2.577]],
                                            "SW17" : [[1.838, 1.723], [2.364, 1.929], [2.593, 2.124], [2.532, 2.239]],
                                            "W1" : [[1.657, 2.72], [2.58, 3.138], [3.455, 4.047]],
                                            "W6" : [[11.67, 2.508], [21.92, 2.914]],
                                            "W10" : [[11.67, 2.508], [21.92, 2.914]],
                                            "W12" : [[14.16, 2.58], [12.59, 2.53], [13.79, 2.66]],
                                            "W13" : [[15.68, 2.6], [13.07, 2.52], [14.17, 2.64]],
                                            "Y2" : [[12.6, 2.55], [15.03, 2.9992], [15.809, 3.11567]],
                                            "Y6" : [[10.24, 2.476], [15.18, 2.751], [18.65, 3.039]],
                                            "Y8" : [[11.67, 2.508], [21.92, 2.914]],
                                            "Y10" : [[11.67, 2.508], [21.92, 2.914]],
                                            "Y13" : [[14.0, 2.56], [12.94, 2.51], [13.84, 2.64]],
                                            "Y14" : [[13.15, 2.55], [14.15, 2.64]]
                                    },
                                    "flow checks" : {
                                            "SW12" : [0.3, 0.6, 1.1, 1.1],
                                            "SW17" : [0.3, 0.6, 1.5, 1.5],
                                            "W1" : [0.399, 0.699, 0.699],
                                            "W6" : [0.219, 0.219],
                                            "W10" : [0.219, 0.219],
                                            "W12" : [0.1, 0.5, 0.5],
                                            "W13" : [0.1, 0.5, 0.5],
                                            "Y2" : [0.65, 0.9, 0.9],
                                            "Y6" : [0.249, 0.499, 0.499],
                                            "Y8" : [0.219, 0.219],
                                            "Y10" : [0.219, 0.219],
                                            "Y13" : [0.2, 0.6, 0.6],
                                            "Y14" : [0.6, 0.6]
                                    }
            }

    def flow_calculator(self, site, t_interval, level_df):
            site = site
            multiplier_list = self.field_constants["flow constants"][site]
            check_list = self.field_constants["flow checks"][site]
            active_checks = check_list[:-1]
            # print(multiplier_list)
            # print(check_list)

            sublist_arr = np.array(multiplier_list, dtype=float)
            multipliers_arr = sublist_arr[:, 0]  # First column: Multipliers
            exponents_arr = sublist_arr[:, 1]  # Second column: Exponents

            last_index = len(multiplier_list) - 1

            clean_series = level_df["level (ft)"].to_numpy()
            indices = np.searchsorted(active_checks, clean_series, side="right")

            indices = np.where(indices >= len(active_checks), last_index, indices)

            matched_multipliers = multipliers_arr[indices]
            matched_exponents = exponents_arr[indices]

            level_df["new cfs"] = (clean_series**matched_exponents) * matched_multipliers

            level_df["new in/hr"] = ((level_df["new cfs"]*self.in_per_ft*self.s_per_hr)/(self.field_constants["area (ac)"][site]*self.ft2_per_acre))

            level_df["JSKT runoff (mm)"] = ((level_df["new cfs"]*self.in_per_ft*self.mm_per_in*(t_interval*self.s_per_min))/(self.field_constants["area (ac)"][site]*self.ft2_per_acre))

            return level_df
    
    def calculate_delta_t(self, runoff_df, flow_sum_df):
            merged_df = pd.merge(flow_sum_df, runoff_df, on = "date")
            merged_df["delta_t"] = merged_df["in"] / merged_df["flow (in/hr)"]
            return merged_df
    
  