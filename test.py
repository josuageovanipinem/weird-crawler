import requests
import csv
import argparse
from bs4 import BeautifulSoup as bs
from datetime import datetime

url3 = "http://www.zone-h.org/archive/special=1/domain=.go.id/fulltext=1/page=1"
cookie3 = dict(
  ZHE='e8d8753cb7d9bd56e89a47596d783c50',
  ZH='e8d8753cb7d9bd56e89a47596d783c50',
  PHPSESSID='5972vds1nh20ikfqvgqoj1ir64',
)

s3 = requests.session()
data3 = s3.get(url3, cookies=cookie3)
data = data3.text
soup = bs(data, 'lxml')

print(soup)