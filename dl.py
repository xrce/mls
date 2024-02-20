import requests, argparse, os
from prettytable import PrettyTable as PT
from bs4 import BeautifulSoup as BS
from selenium import webdriver as WD
from selenium.webdriver.chrome.service import Service as CS
from selenium.webdriver.chrome.options import Options as CO

options = CO()
opts = ["headless", "disable-dev-shm-usage", "no-sandbox", "disable-gpu", "enable-javascript", "user-agent"]
for opt in opts: options.add_argument(f"--{opt}")

parse = argparse.ArgumentParser()
parse.add_argument('-t', help='Judul Film', dest='title')
parse.add_argument('-l', help="Limit", dest='limit')
args = parse.parse_args()

title = input("Masukkan judul : ") if not args.title else args.title
res = requests.get("https://amp.lk21official.mom/search.php", params={"s": title}, headers={"User-Agent": "Mozilla/5.0"})

def banner():
    os.system('clear')
    print('''

░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░   ░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓████▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░  ░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░   ░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░         ░▒▓█▓▒░ 
░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░  ░▒▓█▓▒░ 

''')

def get_links(title, link):
    print(title)
    driver = WD.Chrome(service=CS('/usr/bin/chromedriver'), options=options)
    driver.get(f"https://dl.lk21static.xyz/get/{link}")
    try:
        html_content = driver.page_source
        soup = BS(html_content, "html.parser")
        items, stream = soup.find_all('tr'), soup.find('p')
        if stream: tbl.add_row(["Streaming", stream.find('a')['href']])
        for item in items:
            provider, link = item.find('strong'), item.find('a')
            if provider and link: tbl.add_row([provider.text.strip(), link['href']])
    except Exception as e: print("Gagal menunggu elemen:", e)
    tbl.align = "l"
    print(tbl)
    tbl.clear_rows()
    driver.quit()

def get_info(title, link):
    if "Series" in title:
        res = requests.get(f"https://tv12.nontondrama.click/{link.split('/')[-2]}/", headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code == 200:
            soup = BS(res.text, "html.parser")
            season_list = soup.find_all('div', class_='season-list')
            for season in season_list:
                episode_list = season.find_next_sibling('div', class_='episode-list')
                if episode_list:
                    episodes = episode_list.find_all('a')
                    for episode in episodes:
                        episode_number = episode.text.strip()
                        if "Info" not in episode_number:
                            episode_link = episode['href']
                            get_links(f"{season.find('h4').text.strip()} - Episode {episode_number}", episode_link.split('/')[-2])
    else: get_links(title, link.split('/')[-2])

if res.status_code == 200:
    banner()
    soup = BS(res.text, "html.parser")
    result = soup.find('div', class_='search-wrapper')
    items = result.find_all(class_='search-item')

    tbl = PT()
    tbl.field_names = ["Provider", "Download"]
    
    if args.limit:
        if args.limit == "" or args.limit == None: get_info(items[0].find('h3').text.strip(), items[0].find('a')['href'])
        else:
            i = 0
            while i < int(args.limit):
                get_info(items[i].find('h3').text.strip(), items[i].find('a')['href'])
                i += 1
    else:
        for item in items: get_info(item.find('h3').text.strip(), item.find('a')['href'])
else: print("Gagal melakukan pencarian:", res.status_code)