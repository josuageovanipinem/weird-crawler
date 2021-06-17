import requests
import csv
import argparse
from bs4 import BeautifulSoup 
from datetime import datetime
import sys

#cara menjalankan dengan pemanggilan script
#  ./py nama_script --start 1 --stop 50 --output output

#get data String url dari informasi yang akan diambil dari link

def CookiesValdiationException(error):
    "Cookienya perlu diperbarui"
    sys.exit()

def getBasicArchiveInfo(url_archive, session_cookie):
    session_call = requests.session()
    plain_data = session_call.get(url_archive, cookies=session_cookie)
    data4 = plain_data.text    
    soup = BeautifulSoup(data4, "lxml")
    deface_data = soup.find(id="propdeface")
    #pada sisi arsip
    #MEMANGGIL INFORMASI OS DAN HACKER
    #defacef akan mengembalikan 2 data,
    #data ke 1 menampilkan OS yang digunakan
    #data ke 2 menampilkan hacker
    defacef = deface_data.find_all("li", class_="defacef")
    dOS_name = defacef[1].text.replace("System: ", "")
    dhacker_name = defacef[0].text.replace("Notified by: ", "")
    #Tanggal
    deface0 = deface_data.find_all("li", class_="deface0")
    dtanggal = deface0[0].text.replace("Mirror saved on: ", "")
    #MEMANGGIL URL YANG DI HACK
    defaces = deface_data.find_all("li", class_='defaces')
    dlink_name = defaces[0].text.replace("Domain: ", "")
    dwebserver = defaces[1].text.replace("Web server: ", "")
    #MEMANGGIL IP ADDRESS
    defacet = deface_data.find_all("li", class_="defacet")
    dip_addr = defacet[0].text.replace("IP address:", "")
    #MEMANGGIL LINK YANG DI-SAVE ZONE-H
    dsource = deface_data.findChild('iframe')['src']
    data_returned = [dOS_name, dhacker_name, dlink_name, dwebserver, dip_addr, dsource, dtanggal]
    return data_returned


waktu = datetime.now()
tahun = waktu.year
bulan = waktu.month
hari = waktu.day
#
parser = argparse.ArgumentParser()
parser.add_argument("--start", help="Input page start ", nargs='+')
parser.add_argument("--stop", help="input page stop", nargs='+')
parser.add_argument("--output", help="Output file Name", nargs='+')

args = parser.parse_args()
startJoin = ' '.join(args.start)
start = str(startJoin)
stopJoin = ' '.join(args.stop)
stop = str(stopJoin)
outputJoin = ' '.join(args.output)
output = str(outputJoin)

start = int(start)
stop = int(stop)


with open('output/zoneH-{}-{}-{}-{}.csv'.format(tahun, bulan, hari, output), 'w', newline='') as csvfile:
    writecsv = csv.writer(csvfile)
    writecsv.writerow(["Institusi", "Halaman Terdeface", "Attacker", "H","M","R","Lokasi", "Kejadian", "Arsip", "OS", "Link", "WebServer", "IP Address", "Source", "Tanggal"])

    print("[+] wait, It's Working...")

    for i in range(start, stop+1):
        url = 'http://www.zone-h.org/archive/special=1/domain=.go.id/fulltext=1/page=%s' % i
        sess = requests.session()

        # log.progress("Wait, tt's working...")
        
        #cookie
        myCookie = dict(
            ZHE='e8d8753cb7d9bd56e89a47596d783c50',
            ZH='e8d8753cb7d9bd56e89a47596d783c50',
            PHPSESSID='ojui1h73okkjrg4i7gk922r7d7',
        )        
        data1 = sess.get(url, cookies=myCookie)
        data2 = data1.content               
        bs = BeautifulSoup(data2, 'lxml')        
        table_body = bs.find('table')        
        rows = table_body.find_all('tr', class_=None)[1:]        

        for row in rows:
            kolom = row.findAll('td')            

            if len(kolom) > 1:
                halaman = kolom[7].text
                attacker = kolom[1].text
                H = kolom[2].text
                M = kolom[3].text
                R = kolom[4].text
                Lokasi = kolom[5].encode('utf-8')
                kejadian = kolom[0].text.replace('/', '-')
                arsip = kolom[9].find('a').get('href')
                arsip = str('http://www.zone-h.org%s' % arsip)
                OS = kolom[8].title                
                #ditambah
                tambahan =  getBasicArchiveInfo(arsip, myCookie)                
                writecsv.writerow([None, halaman, attacker, H, M, R, Lokasi, str('%s' % kejadian), str(
                    'www.zone-h.org%s' % arsip), OS, tambahan[2], tambahan[3], tambahan[4], tambahan[5], tambahan[6]])

    print("[✔] Fetching Base Info Done")




