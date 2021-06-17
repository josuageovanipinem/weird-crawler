#TODO membuat class yang membaca inputan dar 

import pandas as pd
import requests
import csv
import argparse
from bs4 import BeautifulSoup
from datetime import datetime

df = pd.read_csv("./output/zoneH-2021-5-28-output.csv")
column = df.Arsip.values

with open('output/zoneH-{}-{}-{}-{}.csv'.format(tahun, bulan, hari, output), 'w', newline='') as csvfile:
    writecsv = csv.writer(csvfile)
    writecsv.writerow(["Institusi", "Halaman Terdeface", "Attacker",
                       "H", "M", "R", "Lokasi", "Kejadian", "Arsip", "OS"])
    
    print("[+] wait, It's Working...")
