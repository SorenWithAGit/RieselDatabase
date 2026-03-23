from pypdf import PdfReader
import fitz
import pandas as pd
import pdfplumber

reader = PdfReader(r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports\ARSRiesel2012.pdf")

print(len(reader.pages))

page1 = reader.pages[1]
text = page1.extract_text()
# print(text)

doc = fitz.open(r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports\ARSRiesel2012.pdf")
fitz_text = doc[1].get_text()
# print(fitz_text)

with pdfplumber.open(r"\\ARS-DATA\Archive\HarmelExit\riesel\GrazinglandQuality\data\GANS reports\ARSRiesel2012.pdf") as pdf:
    table = pdf.pages[1].extract_text()
    print(pdf.pages[1])
    print(table)