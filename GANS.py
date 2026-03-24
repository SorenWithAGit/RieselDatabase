from src import grazingLandQuality
import glob
import os
import pandas as pd

root = r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports"
graze = grazingLandQuality

files = glob.glob(root + "//" + "*.pdf")
for file in files:
    print(os.path.basename(file).split("/")[-1])
    gan = graze.read_pdf
    gan.read_gans(file)