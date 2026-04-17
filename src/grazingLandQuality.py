from pypdf import PdfReader
import pymupdf
from itertools import pairwise
import pandas as pd
import pdfplumber
from pprint import pprint
import ast

class read_pdf:

    def __init__(self):
         self.columns = {
         "nirs" : ["Sample", "Pasture Name", "Date Collected", "Date Received",
                            "Crude Protein", "Digestible Organic Matter", "Fecal Nitrogen", "Fecal Phosphorus"],

         "nutbal" : ["Sample", "Sample Date", "Profile Name", "Animal Kind",
                                "Pasture Name", "Breedtype", "Vegetation Type", "Animal Class",
                                "Standard Ref. Wt. (lbs)", "Days Pregnant", "Current Weight (lbs)", "Days Lactating",
                                "Current Body Condition", "Average Age", "Crude Protein Intake (lbs)", "Crude Protein Requirement (lbs)",
                                "Crude Protein Balance (lbs)", "NEm (Meal/day) Intake", "NEm (Meal/day) Requirement", "NEm (Meal/day) Balance",
                                "NEg (Meal/day) Intake", "NEg (Meal/day) Requirement", "NEg (Meal/day) Balance", "Weight Change Goal (lbs/day)",
                                "Estimated Weight Change (lbs/day)", "Estimated Weight in 30 Days (lbs)", "Estimate Body Condition in 30 days",
                                "Performance Limited By", "Dry Matter Intake Concentrates (lbs/day)",
                                "Dry Matter Intake Concentrates (% of Std. Ref. Wt.)", "Dry Matter Intake Concentrates (AUE)",
                                "Dry Matter Intake Roughage (lbs/day)", "Dry Matter Intake Roughage (% of Std. Ref. Wt.)", 
                                "Dry Matter Intake Roughage (AUE)", "Dry Matter Intake Forage (lbs/day)", "Dry Matter Intake Forage (% of Std. Ref. Wt.)",
                                "Dry Matter Intake Forage (AUE)", "Dry Matter Intake Calf DM/d (lbs/d)", 
                                "Dry Matter Intake Calf DM/d (% of std. Ref. Wt.)", "Dry Matter Intake Calf DM/d (AUE)", ""
                                "Dry Matter Intake Total (lbs/d)", "Dry Matter Intake Total (% of Std. Ref. Wt.)", 
                                "Dry Matter Intake Total (AUE)", "CP Consumption (Overall)", "CP Consumption (Forage)",
                                "DOM Consumption (Overall)", "DOM Consumption (Forage)", "DOM/CP (Overall)", "DOM/CP (Forage)",
                                "Potential Milk Production (lbs/day)", "Actual Milk Production (lbs/day)", 
                                "Estimated Fecal Output (lbs/day)", "Fecal P Output (lbs/day)", "Fecal N Output (lbs/day)"]
         }

         self.nirs = pd.DataFrame(columns = self.columns["nirs"])
         self.nutbal = pd.DataFrame(columns = self.columns["nutbal"])

         

    def raw_txt(self, file):
        all_text = []
        with pdfplumber.open(file) as pdf:
            for p, page in enumerate(pdf.pages):
                plum_text = page.extract_text()
                all_text += plum_text.split("\n")
        return all_text
    
    def scrub_text(self, all_text):
        df_map = {
            "nirs" : self.nirs,
            "nutbal" : self.nutbal
        }
        nirs = {i : [] for i in range(len(self.columns["nirs"]))}
        nutbal = {j : [] for j in range(len(self.columns["nutbal"]))}
        current_locals = locals()
        lines = all_text[0:18]
        for line in lines:
            split_line = line.split()
            print(split_line)
            while True:
                try:
                    user_input = input("pass or df selction, columns, vals to append: ")
                    if user_input != "pass":
                        input_list = list(ast.literal_eval(user_input))
                        df_select = input_list[0]
                        df_columns = input_list[1]
                        df_values = input_list[2]
                        if df_select in current_locals and isinstance(current_locals[df_select], dict):
                            if df_select in df_map:
                                for i, col in enumerate(df_columns):
                                    if type(df_values[i]) is list:
                                        # print("value is list")
                                        value = ""
                                        for val in df_values[i]:
                                            value += split_line[val]
                                            value += " "
                                    else:
                                        value = split_line[df_values[i]]
                                    current_locals[df_select][col].append(value)
                            print(current_locals[df_select])
                    break
                except (SyntaxError, ValueError, IndexError):
                    print("Invalid Input Try Again")
                    print(split_line)


    
    def pdf_plum(file):
        table_settings = {
                            "vertical_strategy": "text",
                            "horizontal_strategy": "text", 
                            }
        with pdfplumber.open(file) as pdf:
            row_labels = []
            page = pdf.pages[1]
            table = page.extract_table(table_settings)
            filter_table = [[iter for iter in sublist if iter != ""] for sublist in table]
            filteri_table = list(filter(None, filter_table))
            for l in range(len(filteri_table)):
                for i in range(len(filteri_table[l])):
                    if ":" in filteri_table[l][i]:
                        # print(i)
                        # print(filteri_table[l][i])
                        variable = ""
                        for r in range(i+1):
                            variable += filteri_table[l][r]
                        row_labels.append(variable)
                
        unique_labels = []
        for label in row_labels:
            if label not in unique_labels:
                unique_labels.append(label)
        print(unique_labels)

    def pymu_tables(file):
        NIRS_cols = ["Sample", "Pasture Name", "Date Collected",
                            "Crude Protein", "Digestible Organic Matter", "Fecal Nitrogen", "Fecal Phosphorus"]
        row_labels = []
        row_values = []
        sample_values = []
        pages = pymupdf.open(file)
        # page1 = pages[0]
        for page in pages:
            tables = pages[1].find_tables(strategy = "text")
            # pprint(table[0].extract())
            for t in tables:
                table = t.extract()
                # pprint(table)
                filter_table = [[iter for iter in sublist if iter != ""] for sublist in table]
                filteri_table = list(filter(None, filter_table))
                for l in range(len(filteri_table)):
                    try:
                        row_values.append(filteri_table[l][-1])
                    except:
                        row_values.append("nan")
                    for i in range(len(filteri_table[l])):
                        if ":" in filteri_table[l][i]:
                            # print(i)
                            # print(filteri_table[l][i])
                            variable = ""
                            for r in range(i+1):
                                variable += filteri_table[l][r]
                            row_labels.append(variable)
                
        unique_labels = []
        for label in row_labels:
            if label not in unique_labels:
                unique_labels.append(label)
        # print(unique_labels)
        smpl_data_len = [i for i, x in enumerate(row_labels) if x == "Sample:"]
        smpl_data_len.append(len(row_labels))
        # print(smpl_data_len)
        pprint(unique_labels)

        for c_val, n_val in pairwise(smpl_data_len):
            temp_lst = []
            for dat in range(c_val, n_val):
                temp_lst.append(row_values[dat])
            sample_values.append(temp_lst)
        temp_df = pd.DataFrame(sample_values, columns = unique_labels)
        # print(temp_df)
                    
                

            # pprint(row_values)
            # pprint(filteri_table)
        



    def read_NIRS(file):

        # NIRS_cols = ["Sample", "Pasture Name", "Date Collected", "Date Received",
        #                             "Crude Protein", "Digestible Organic Matter", "Fecal Nitrogen", "Fecal Phosphorus"]
        
        NIRS_cols = ["Sample", "Pasture Name", "Date Collected",
                            "Crude Protein", "Digestible Organic Matter", "Fecal Nitrogen", "Fecal Phosphorus"]

        NIRS_results = pd.DataFrame(columns = NIRS_cols)
        
        # create lists to append data

        ## NIRS lists
        samples = []
        pasture_names = []
        collect_dates = []
        # rcvd_dates = []
        crude_protein = []
        digest_om = []
        fecal_N = []
        fecal_P = []

        # Read raw pdf
        with pdfplumber.open(file) as pdf:
            for p, page in enumerate(pdf.pages):
                plum_text = page.extract_text()
                if "NIRS" in plum_text.split("\n")[0]:
                    for row in plum_text.split("\n"):
                        if "NIRS" in row:
                            pass
                        else:
                            if len(row.split(": ")) == 2:
                                if "Sample: " in row:
                                    samples.append(row.split("Sample: ")[1])
                                elif "Pasture Name: " in row:
                                    pasture_names.append(row.split("Pasture Name: ")[1])
                                elif "Date Collected: " in row:
                                    collect_dates.append(row.split("Date Collected: ")[1])
                                elif "Date Received: " in row:
                                    # rcvd_dates.append(row.split("Date Received: ")[1])
                                    pass
                                elif "Crude Protein: " in row:
                                    crude_protein.append(row.split("Crude Protein: ")[1])
                                elif "Digestible Organic Matter: " in row:
                                    digest_om.append(row.split("Digestible Organic Matter: ")[1])
                                elif "Fecal Nitrogen: " in row:
                                    fecal_N.append(row.split("Fecal Nitrogen: ")[1])
                                elif "Fecal Phosphorus: " in row:
                                    fecal_P.append(row.split("Fecal Phosphorus: ")[1])

                            elif len(row.split(": ")) == 3:
                                if "Sample: " in row:
                                    samples.append(row.split(": ")[1].split(" ")[0])
                                    crude_protein.append(row.split(": ")[2])
                                elif "Pasture Name: " in row:
                                    pasture_names.append(row.split(": ")[1].split(" ")[0])
                                    digest_om.append(row.split(": ")[2])
                                elif "Date Collected: " in row:
                                    collect_dates.append(row.split(": ")[1].split(" ")[0])
                                    fecal_N.append(row.split(": ")[2])
                                elif "Report Date: " in row:
                                    fecal_P.append(row.split(": ")[2])

        NIRS_lsts = [
        samples,
        pasture_names,
        collect_dates,
        # rcvd_dates,
        crude_protein,
        digest_om,
        fecal_N,
        fecal_P
        ]

        # print(NIRS_lsts)

        for c, column in enumerate(NIRS_cols):
            NIRS_results[column] = NIRS_lsts[c]
        print(NIRS_results)


    def read_gans(file):

        NIRS_results = pd.DataFrame(columns = ["Sample", "Pasture Name", "Date Collected", "Date Received",
                                    "Crude Protein", "Digestible Organic Matter", "Fecal Nitrogen", "Fecal Phosphorus"])

        Nut_samples = []
        Nut_smpl_dates = []
        Nut_profiles = []
        Nut_animals = []
        Nut_pastures = []
        Nut_breeds = []
        Nut_vegs = []
        Nut_classes = []
        std_ref_Wts = []
        days_preg = []
        current_Wts = []
        days_lact = []
        body_conds = []
        ages = []
        crude_intake = []
        crude_req = []
        crude_bal = []
        NEm_intake = []
        NEm_req = []
        NEm_bal = []
        NEg_intake = []
        NEg_req = []
        NEg_bal = []
        wcg = []
        ewc = []
        ew30d = []
        ebc30d = []
        perf_limit = []
        conc_lbs_day = []
        conc_PoSRW = []
        conc_AUE = []
        roughage_lbs_day = []
        roughage_PoSRW = []
        roughage_AUE = []
        forage_lbs_day = []
        forage_PoSRW = []
        forage_AUE = []
        calf_DM_d_lbs_day = []
        calf_DM_d_PoSRW = []
        calf_DM_d_AUE = []
        total_lbs_day = []
        total_PoSRW = []
        total_AUE = []
        CP_cons_overall = []
        CP_cons_forage = []
        DOM_cons_overall = []
        DOM_cons_forage = []
        DOM_CP_ratio_overall = []
        DOM_CP_ratio_forage = []
        pmp = []
        amp = []
        est_fecal_out = []
        fecal_P_out = []
        fecal_N_out = []

        with pdfplumber.open(file) as pdf:
            for p, page in enumerate(pdf.pages):
                plum_text = page.extract_text()

                if "NIRS" in plum_text.split("\n")[0]:
                    samples = []
                    pasture_names = []
                    collect_dates = []
                    rcvd_dates = []
                    crude_protein = []
                    digest_om = []
                    fecal_N = []
                    fecal_P = []
                    for row in plum_text.split("\n"):
                        if "NIRS" in row:
                            pass
                        else:
                            if "Sample: " in row:
                                samples.append(row.split("Sample: ")[1])
                            elif "Pasture Name: " in row:
                                pasture_names.append(row.split("Pasture Name: ")[1])
                            elif "Date Collected: " in row:
                                collect_dates.append(row.split("Date Collected: ")[1])
                            elif "Date Received: " in row:
                                rcvd_dates.append(row.split("Date Received: ")[1])
                            elif "Crude Protein: " in row:
                                crude_protein.append(row.split("Crude Protein: ")[1])
                            elif "Digestible Organic Matter: " in row:
                                digest_om.append(row.split("Digestible Organic Matter: ")[1])
                            elif "Fecal Nitrogen: " in row:
                                fecal_N.append(row.split("Fecal Nitrogen: ")[1])
                            elif "Fecal Phosphorus: " in row:
                                fecal_P.append(row.split("Fecal Phosphorus: ")[1])
                    temp_nirs = pd.DataFrame(columns = ["Sample", "Pasture Name", "Date Collected", "Date Received",
                                                "Crude Protein", "Digestible Organic Matter", "Fecal Nitrogen", "Fecal Phosphorus"])

                    temp_nirs["Sample"] = samples
                    temp_nirs["Pasture Name"] = pasture_names
                    temp_nirs["Date Collected"] = collect_dates
                    temp_nirs["Date Received"] = rcvd_dates
                    temp_nirs["Crude Protein"] = crude_protein
                    temp_nirs["Digestible Organic Matter"] = digest_om
                    temp_nirs["Fecal Nitrogen"] = fecal_N
                    temp_nirs["Fecal Phosphorus"] = fecal_P
                    NIRS_results = pd.concat([NIRS_results, temp_nirs])

                elif "NutBal" in plum_text.split("\n")[0]:

                    Nut_cols = ["Sample", "Sample Date", "Profile Name", "Animal Kind",
                                "Pasture Name", "Breedtype", "Vegetation Type", "Animal Class",
                                "Standard Ref. Wt. (lbs)", "Days Pregnant", "Current Weight (lbs)", "Days Lactating",
                                "Current Body Condition", "Average Age", "Crude Protein Intake (lbs)", "Crude Protein Requirement (lbs)",
                                "Crude Protein Balance (lbs)", "NEm (Meal/day) Intake", "NEm (Meal/day) Requirement", "NEm (Meal/day) Balance",
                                "NEg (Meal/day) Intake", "NEg (Meal/day) Requirement", "NEg (Meal/day) Balance", "Weight Change Goal (lbs/day)",
                                "Estimated Weight Change (lbs/day)", "Estimated Weight in 30 Days (lbs)", "Estimate Body Condition in 30 days",
                                "Performance Limited By", "Dry Matter Intake Concentrates (lbs/day)",
                                "Dry Matter Intake Concentrates (% of Std. Ref. Wt.)", "Dry Matter Intake Concentrates (AUE)",
                                "Dry Matter Intake Roughage (lbs/day)", "Dry Matter Intake Roughage (% of Std. Ref. Wt.)", 
                                "Dry Matter Intake Roughage (AUE)", "Dry Matter Intake Forage (lbs/day)", "Dry Matter Intake Forage (% of Std. Ref. Wt.)",
                                "Dry Matter Intake Forage (AUE)", "Dry Matter Intake Calf DM/d (lbs/d)", 
                                "Dry Matter Intake Calf DM/d (% of std. Ref. Wt.)", "Dry Matter Intake Calf DM/d (AUE)", ""
                                "Dry Matter Intake Total (lbs/d)", "Dry Matter Intake Total (% of Std. Ref. Wt.)", 
                                "Dry Matter Intake Total (AUE)", "CP Consumption (Overall)", "CP Consumption (Forage)",
                                "DOM Consumption (Overall)", "DOM Consumption (Forage)", "DOM/CP (Overall)", "DOM/CP (Forage)",
                                "Potential Milk Production (lbs/day)", "Actual Milk Production (lbs/day)", 
                                "Estimated Fecal Output (lbs/day)", "Fecal P Output (lbs/day)", "Fecal N Output (lbs/day)"]
                    


                    for i, row in enumerate(plum_text.split("\n")):
                        if "NutBal" in row:
                            pass
                        else:

                            # print(row.split(": "))
                            if row.split(":")[0] == "Sample":
                                Nut_samples.append(row.split(": ")[1].strip(" Sample Date"))
                                Nut_smpl_dates.append(row.split(": ")[2])
                            elif row.split(":")[0] == "Profile Name":
                                Nut_profiles.append(row.split(": ")[1].replace(" Animal Kind", ""))
                                Nut_animals.append(row.split(": ")[2])
                            elif row.split(": ")[0] == "Pasture Name":
                                Nut_pastures.append(row.split(": ")[1].strip(" Breedtype:"))
                                try:
                                    Nut_breeds.append(row.split(": ")[2])
                                except:
                                    breedln_1 = plum_text.split("\n")[i-1].split(": ")
                                    breedln_2 = plum_text.split("\n")[i+1].split(": ")
                                    breed = str(breedln_1[0]) + " " + str(breedln_2[0])
                                    Nut_breeds.append(breed)
                            elif row.split(": ")[0] == "Vegetation Type":
                                Nut_vegs.append(row.split(": ")[1].strip(" Animal Class"))
                                Nut_classes.append(row.split(": ")[2])
                            elif row.split(": ")[0].split(" ")[0] == "Vegetation":
                                    ln_1 = row.split(": ")[0].strip("Vegetation ").strip(" Animal")
                                    ln_2 = plum_text.split("\n")[i+2].split(": ")[1].split(" Class:")[0]
                                    veg = str(ln_1) + " " + str(ln_2)
                                    Nut_vegs.append(veg)
                                    clas = plum_text.split("\n")[i+1].strip(": ")
                                    Nut_classes.append(clas)

                            elif row.split(": ")[0] == "Animal Condition":
                                pass
                            elif row.split(": ")[0] == "Standard Ref. Wt. (lbs)":
                                std_ref_Wts.append(row.split(": ")[1].strip(" Days Pregnant"))
                                days_preg.append(row.split(": ")[2])
                            elif row.split(": ")[0] == "Current Weight (lbs)":
                                current_Wts.append(row.split(": ")[1].split(" Days Lactating ")[0])
                                days_lact.append(row.split(": ")[1].split(" Days Lactating ")[1])
                            elif row.split(": ")[0] == "Current Body Condition":
                                body_conds.append(row.split(": ")[1].strip(" Average Age"))
                                ages.append(row.split(": ")[2])
                            elif row.split(": ")[0] == "Nutritional Status Intake Requirement Balance":
                                pass
                            elif row.split(": ")[0] == "Crude Protein (lbs)":
                                crude_intake.append(row.split(": ")[1].split(" ")[0])
                                crude_req.append(row.split(": ")[1].split(" ")[1])
                                crude_bal.append(row.split(": ")[1].split(" ")[2])
                            elif row.split(": ")[0] == "NEm (Mcal/day)":
                                NEm_intake.append(row.split(": ")[1].split(" ")[0])
                                NEm_req.append(row.split(": ")[1].split(" ")[1])
                                NEm_bal.append(row.split(": ")[1].split(" ")[2])
                            elif row.split(": ")[0] == "NEg (Mcal/day)":
                                NEg_intake.append(row.split(": ")[1].split(" ")[0])
                                NEg_req.append(row.split(": ")[1].split(" ")[1])
                                NEg_bal.append(row.split(": ")[1].split(" ")[2])
                            elif row.split(": ")[0] == "Performance":
                                pass
                            elif row.split(": ")[0] == "Weight Change Goal (lbs/day)":
                                wcg.append(row.split(": ")[1])
                            elif row.split(": ")[0] == "Estimated Weight Change (lbs/day)":
                                ewc.append(row.split(": ")[1])
                            elif row.split(": ")[0] == "Estimated Weight in 30 days (lbs)":
                                ew30d.append(row.split(": ")[1])
                            elif row.split(": ")[0] == "Estimated Body Condition in 30 days":
                                ebc30d.append(row.split(": ")[1])
                            elif row.split(": ")[0] == "Performance Limited By":
                                perf_limit.append(row.split(": ")[1])
                            elif row.split(": ")[0] == "Dry Matter Intake lbs/day Percent of Std. Ref. Wt. AUE":
                                pass
                            elif row.split(": ")[0] == "Concentrates":
                                conc_lbs_day.append(row.split(": ")[1].split(" ")[0])
                                conc_PoSRW.append(row.split(": ")[1].split(" ")[1])
                                conc_AUE.append(row.split(": ")[1].split(" ")[2])
                            elif row.split(": ")[0] == "Roughage":
                                roughage_lbs_day.append(row.split(": ")[1].split(" ")[0])
                                roughage_PoSRW.append(row.split(": ")[1].split(" ")[1])
                                roughage_AUE.append(row.split(": ")[1].split(" ")[2])
                            elif row.split(": ")[0] == "Forage":
                                forage_lbs_day.append(row.split(": ")[1].split(" ")[0])
                                forage_PoSRW.append(row.split(": ")[1].split(" ")[1])
                                forage_AUE.append(row.split(": ")[1].split(" ")[2])
                            elif row.split(": ")[0] == "Calf DM/d":
                                calf_DM_d_lbs_day.append(row.split(": ")[1].split(" ")[0])
                                calf_DM_d_PoSRW.append(row.split(": ")[1].split(" ")[1])
                                calf_DM_d_AUE.append(row.split(": ")[1].split(" ")[2])
                            elif row.split(": ")[0] == "Total":
                                total_lbs_day.append(row.split(": ")[1].split(" ")[0])
                                total_PoSRW.append(row.split(": ")[1].split(" ")[1])
                                total_AUE.append(row.split(": ")[1].split(" ")[2])
                            elif row.split(": ")[0] == "Diet Quality Overall Forage":
                                pass
                            elif row.split(": ")[0] == "CP Consumption":
                                CP_cons_overall.append(row.split(": ")[1].split(" ")[0])
                                CP_cons_forage.append(row.split(": ")[1].split(" ")[1])
                            elif row.split(": ")[0] == "DOM Consumption":
                                DOM_cons_overall.append(row.split(": ")[1].split(" ")[0])
                                DOM_cons_forage.append(row.split(": ")[1].split(" ")[1])
                            elif row.split(": ")[0] == "DOM / CP Ratio":
                                DOM_CP_ratio_overall.append(row.split(": ")[1].split(" ")[0])
                                DOM_CP_ratio_forage.append(row.split(": ")[1].split(" ")[1])
                            try:
                                if row.split(": ")[0] == "Milk lbs/day":
                                    pass
                                elif row.split(": ")[0] == "Potential Milk Production":
                                    pmp.append(row.split(": ")[1])
                                elif row.split(": ")[0] == "Actual Milk Production":
                                    amp.append(row.split(": ")[1])
                                elif row.split(": ")[0] == "Fecal lbs/day":
                                    pass
                                elif row.split(": ")[0] == "Estimated Fecal Output":
                                    est_fecal_out.append(row.split(": ")[1])
                                elif row.split(": ")[0] == "Fecal P Output":
                                    fecal_P_out.append(row.split(": ")[1])
                                elif row.split(": ")[0] == "Fecal N Output":
                                    fecal_N_out.append(row.split(": ")[1])
                                else:
                                    pass
                            except:
                                pass
                elif "Milk" in plum_text.split("\n")[0]:
                    # print(plum_text.split("\n"))
                    pmp.append(plum_text.split("\n")[1].split("Production: ")[1])
                    amp.append(plum_text.split("\n")[2].split("Production: ")[1])
                    est_fecal_out.append(plum_text.split("\n")[4].split("Output: ")[1])
                    fecal_P_out.append(plum_text.split("\n")[5].split("Output: ")[1])
                    fecal_N_out.append(plum_text.split("\n")[6].split("Output: ")[1])

        Nut_lsts = [
        Nut_samples,
        Nut_smpl_dates,
        Nut_profiles,
        Nut_animals,
        Nut_pastures,
        Nut_breeds,
        Nut_vegs,
        Nut_classes,
        std_ref_Wts,
        days_preg,
        current_Wts,
        days_lact,
        body_conds,
        ages,
        crude_intake,
        crude_req,
        crude_bal,
        NEm_intake,
        NEm_req,
        NEm_bal,
        NEg_intake,
        NEg_req,
        NEg_bal,
        wcg,
        ewc,
        ew30d,
        ebc30d,
        perf_limit,
        conc_lbs_day,
        conc_PoSRW,
        conc_AUE,
        roughage_lbs_day,
        roughage_PoSRW,
        roughage_AUE,
        forage_lbs_day,
        forage_PoSRW,
        forage_AUE,
        calf_DM_d_lbs_day,
        calf_DM_d_PoSRW,
        calf_DM_d_AUE,
        total_lbs_day,
        total_PoSRW,
        total_AUE,
        CP_cons_overall,
        CP_cons_forage,
        DOM_cons_overall,
        DOM_cons_forage,
        DOM_CP_ratio_overall,
        DOM_CP_ratio_forage,
        pmp,
        amp,
        est_fecal_out,
        fecal_P_out,
        fecal_N_out,
        ]

        # print(Nut_lsts)
                            


        NIRS_results = NIRS_results.reset_index()
        print(NIRS_results)
        print("\n")
        print("\n")

        # for l, col in enumerate(Nut_cols):
        #     print(col + " - Length of list: " + str(len(Nut_lsts[l])))

        Nut_Bal_results = pd.DataFrame(columns = Nut_cols)
        for i, column in enumerate(Nut_cols):
            Nut_Bal_results[column] = Nut_lsts[i]
        print(Nut_Bal_results)
        print("\n")