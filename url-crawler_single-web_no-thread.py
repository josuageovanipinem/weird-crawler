import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
from datetime import datetime 

#colorama digunakan untuk memberikan warna pada keluaran
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

#SET
# set internal_urls untuk menyimpan website internal
internal_urls = set()
# set internal_urls untuk menyimpan website eksternal
external_urls = set()
#set untuk konten berupa aset
asset_set = set() 

#LIST
#pengecekan ekstensi yang akan dipisahkan pada list
extensionsToCheck = ('.pdf', '.jpeg', '.jpg', '.pptx', '.ppt', '.mp4', '.doc', '.doc')
bppt_url = ('https://bppt.go.id', 
  'https://csirt.bppt.go.id',
  'https://pmi.bppt.go.id'
)

def is_valid(url):
  """
  Check apabila "url" valid
  """
  parsed = urlparse(url)
  return bool(parsed.netloc) and bool(parsed.scheme)

#build function untuk mengembalikan url yang valid
def get_all_website_links(url):
  """
  mengembalikan URL yang ditemukan pada suatu website yang sama
  """
  urls = set()
  #domain name dari url tanpa protocol
  domain_name = urlparse(url).netloc
  soup = BeautifulSoup(requests.get(url).content, "html.parser")
  for a_tag in soup.findAll("a"):
    href = a_tag.attrs.get("href")
    if href == "" or href is None:
      continue
    href = urljoin(url, href)
    parsed_href = urlparse(href)
    href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
    if not is_valid(href):
    #bukan link yang valid
      continue
    if href in internal_urls:
     #sudah ada pada set
      continue
    if url not in href:
      #cek apakah domain bppt apa bukan
      external_urls.add(href)
      continue
    if href.endswith(extensionsToCheck):
      asset_set.add(href)
      continue
    if domain_name not in href:
    #link url eksternal
      if href not in external_urls:
        print(f"{GRAY}[!] External link:{href}{RESET}")
        external_urls.add(href)
        continue
    print(f"{GREEN}[*] Internal link:{href}{RESET}")
    urls.add(href)
    internal_urls.add(href)
  return urls

total_urls_visited = 0

def crawl(url, max_urls=1):
  """
  melakukan penulusuran terhadap semua link pada website
  kemudian data yang ada kemudian disimpan pada set internal link dan eksternal link. 
  params:
      max_uls (int): merupakan nomor maksimal dari url yang di-crawl
  """
  global total_urls_visited
  total_urls_visited += 1
  print(f"{YELLOW}[*] Crawling: {url}{RESET}")
  links = get_all_website_links(url)
  for link in links:
    if total_urls_visited > max_urls:
      break
    crawl(link, max_urls=max_urls)

def getDate():  
  dt_string = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
  return dt_string

if __name__ == "__main__":
  crawl("https://pmi.bppt.go.id")
  print("Total internal links:", len(internal_urls))
  print("Total eksternal links:", len(external_urls))



