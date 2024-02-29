import requests
from prettytable import PrettyTable as PT
from bs4 import BeautifulSoup as BS
from selenium import webdriver as WD
from selenium.webdriver.chrome.service import Service as CS
from selenium.webdriver.chrome.options import Options as CO

class NKP:
    def __init__(self):
        self.options = CO()
        opts = ["headless", "disable-dev-shm-usage", "no-sandbox", "disable-gpu", "enable-javascript", "user-agent"]
        for opt in opts: self.options.add_argument(f"--{opt}")

        self.tbl = PT()
        self.tbl.field_names = ["Provider", "Download"]
    
    def get_links(self, title, link): return 0
    def get_info(self, title, link):
        res = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
        soup = BS(res.text, "html.parser")
        boxes = soup.find_all("div", class_="liner")
        print(title)
        for box in boxes:
            reso = box.find("div", class_="name").text.strip().split(" ")[-1]
            listurl = box.find_all("div", class_="listlink")
            for urlgroup in listurl:
                links = urlgroup.find_all("a")
                for linkt in links:
                    provider = linkt.text.strip()
                    download = linkt.get("href")
                    self.tbl.add_row([f"{provider} {reso}", download])
        self.tbl.align = "l"
        print(self.tbl)
        self.tbl.clear_rows()
                
    def search(self, title, limit=None):
        url = f"https://nekopoi.care/search/{title}"
        page_num = 1
        while True:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if res.status_code == 200:
                soup = BS(res.text, "html.parser")
                results = soup.find_all("div", class_="top")
                if limit:
                    if limit == "" or limit == None: self.get_info(results[0].find("a").text.strip(), results[0].find("a")["href"])
                    else:
                        i = 0
                        while i < int(limit):
                            self.get_info(results[i].find("a").text.strip(), results[i].find("a")["href"])
                            i += 1
                        break
                else:
                    for result in results: self.get_info(result.find("a").text.strip(), result.find("a")["href"])
                next_link = soup.find("a", class_="next page-numbers")
                if next_link:
                    page_num += 1
                    url = f"https://nekopoi.care/search/Overflow/page/{page_num}/"
                else: break
            else:
                print("Failed to retrieve data from the URL.")
                break

class LK21:
    def __init__(self):
        self.options = CO()
        opts = ["headless", "disable-dev-shm-usage", "no-sandbox", "disable-gpu", "enable-javascript", "user-agent"]
        for opt in opts: self.options.add_argument(f"--{opt}")

        self.tbl = PT()
        self.tbl.field_names = ["Provider", "Download"]

    def get_links(self, title, link):
        driver = WD.Chrome(service=CS('/usr/bin/chromedriver'), options=self.options)
        driver.get(f"https://dl.lk21static.xyz/get/{link}")
        print(title)
        try:
            html_content = driver.page_source
            soup = BS(html_content, "html.parser")
            items, stream = soup.find_all('tr'), soup.find('p')
            if stream: self.tbl.add_row(["Streaming", stream.find('a')['href']])
            for item in items:
                provider, link = item.find('strong'), item.find('a')
                if provider and link: self.tbl.add_row([provider.text.strip(), link['href']])
        except Exception as e: print("Gagal menunggu elemen:", e)
        self.tbl.align = "l"
        print(self.tbl)
        self.tbl.clear_rows()
        driver.quit()

    def get_info(self, title, link):
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
                                self.get_links(f"{season.find('h4').text.strip()} - Episode {episode_number}", episode_link.split('/')[-2])
        else: self.get_links(title, link.split('/')[-2])

    def search(self, title, limit=None):
        res = requests.get("https://amp.lk21official.mom/search.php", params={"s": title}, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code == 200:
            soup = BS(res.text, "html.parser")
            result = soup.find('div', class_='search-wrapper')
            items = result.find_all(class_='search-item')
            if limit:
                if limit == "" or limit == None: self.get_info(items[0].find('h3').text.strip(), items[0].find('a')['href'])
                else:
                    i = 0
                    while i < int(limit):
                        self.get_info(items[i].find('h3').text.strip(), items[i].find('a')['href'])
                        i += 1
            else:
                for item in items: self.get_info(item.find('h3').text.strip(), item.find('a')['href'])
        else:
            print("Gagal melakukan pencarian:", res.status_code)