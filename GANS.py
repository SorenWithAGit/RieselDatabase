from src import grazingLandQuality
import glob
import os
import pandas as pd

root = r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports"

graze = grazingLandQuality.read_pdf()

# 2012_NIRS = graze.read_NIRS(r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports\ARSRiesel2012.pdf")
# dec_2013_NIRS = graze.read_NIRS(r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports\Dec2013GANS.pdf")

# gans_2012 = graze.raw_txt(r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports\ARSRiesel2012.pdf")
# print(gans_2012)

test_gans = graze.raw_txt(r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports\Aug2013GANS.pdf")
# print(test_gans[28:63])
test_scrub = graze.scrub_text(test_gans)


# pdfplumb = graze.pdf_plum(r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports\ARSRiesel2012.pdf")
# pymu_2013_NIRS = graze.NIRS_tables(r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports\ARSRiesel2012.pdf")

# dec2013 = graze.raw_txt(r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports\Dec2013GANS.pdf")
# for row in dec2013:
#     print(row.split(": "))

# files = glob.glob(root + "//" + "*.pdf")
# for file in files:
#     if os.path.basename(file).split("/")[-1] != "Riesel_SampleForm.pdf":
#         print(os.path.basename(file).split("/")[-1])
#         gan = graze.read_pdf
#         gan.read_gans(file)