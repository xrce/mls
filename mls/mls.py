import requests
from prettytable import PrettyTable as PT
from bs4 import BeautifulSoup as BS
from selenium import webdriver as WD
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as CS
from selenium.webdriver.chrome.options import Options as CO

class Settings:
    def __init__(self):
        self.options = CO()
        opts = ["headless", "disable-dev-shm-usage", "no-sandbox", "disable-gpu", "enable-javascript", "user-agent"]
        for opt in opts: self.options.add_argument(f"--{opt}")

        self.tbl = PT()
        self.tbl.field_names = ["Provider", "Download"]
        self.tbl.align = "l"
        
        self.link = {
            "IMDB": "https://www.imdb.com/find/",
            "IMDBPLAYER": "https://databasegdriveplayer.xyz/player.php?imdb=",
            "REBAHIN": "http://179.43.169.211/",
            "NKP": "https://nekopoi.care/search/",
            "LK21": "https://tv.lk21official.mom/search.php",
            "LK21INFO": "https://tv12.nontondrama.click/",
            "LK21DL": "https://dl.lk21static.xyz/get/"
        }
        
        self.headers = {"User-Agent": "Mozilla/5.0"}

class IMDB:
    def __init__(self): self.tbl = Settings().tbl
    def get_links(self, link):
        url = f"{Settings().link['IMDBPLAYER']}{link.split('/')[-2]}"
        res = requests.get(url, headers=Settings().headers)
        if res.status_code == 200:
            soup = BS(res.text, "html.parser")
            if soup.find("title").text.strip() != "()":
                print(soup.find("title").text.strip())
                self.tbl.add_row(["Streaming", url])
        print(self.tbl)
        self.tbl.clear_rows()
    
    def search(self, title, limit=None):
        res = requests.get(Settings().link['IMDB'], params={"q": title}, headers=Settings().headers)
        if res.status_code == 200:
            soup = BS(res.text, "html.parser")
            result = soup.find('ul', class_='ipc-metadata-list')
            items = result.find_all('a', class_='ipc-metadata-list-summary-item__t')
            if limit:
                if limit == "" or limit == None: self.get_links(items[0]['href'])
                else:
                    i = 0
                    while i < int(limit):
                        self.get_links(items[i]['href'])
                        i += 1
            else:
                for item in items: self.get_links(item['href'])

class REBAHIN:
    def __init__(self): self.tbl = Settings().tbl
    def get_links(self, title, link):
        driver = WD.Chrome(service=CS('/usr/bin/chromedriver'), options=Settings().options)
        driver.get(f"{link}play/?ep=2&sv=1")
        wait = WDW(driver, 10)
        print(title)
        try:
            wait.until(EC.element_to_be_clickable((By.ID, "downloadmv"))).click
            links = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[style*='padding']"))).find_elements(By.CSS_SELECTOR, "table tbody tr")
            for link in links: self.tbl.add_row([link.find_element(By.CSS_SELECTOR, "td:first-child").text, link.find_element(By.CSS_SELECTOR, "td:last-child a").get_attribute("href")])
        except Exception as e: print("Gagal menunggu elemen:", e)
        print(self.tbl)
        self.tbl.clear_rows()
        driver.quit()
    def search(self, title, limit=None):
        res = requests.get(Settings().link['REBAHIN'], params={"s": title}, headers=Settings().headers)
        if res.status_code == 200:
            soup = BS(res.text, "html.parser")
            result = soup.find('div', class_='movies-list-full')
            items = result.find_all('div', class_='ml-item')
            if limit:
                if limit == "" or limit == None: self.get_links(items[0].find('h2').text.strip(), items[0].find('a')['href'])
                else:
                    i = 0
                    while i < int(limit):
                        self.get_links(items[i].find('h2').text.strip(), items[i].find('a')['href'])
                        i += 1
            else:
                for item in items: self.get_links(item.find('h2').text.strip(), item.find('a')['href'])

class NKP:
    def __init__(self): self.tbl = Settings().tbl
    def get_info(self, title, link):
        res = requests.get(link, headers=Settings().headers)
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
        print(self.tbl)
        self.tbl.clear_rows()
                
    def search(self, title, limit=None):
        url = f"{Settings().link['NKP']}{title}"
        page_num = 1
        while True:
            res = requests.get(url, headers=Settings().headers)
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
            else: break

class LK21:
    def __init__(self): self.tbl = Settings().tbl
    def get_links(self, title, link):
        driver = WD.Chrome(service=CS('/usr/bin/chromedriver'), options=Settings().options)
        driver.get(f"{Settings().link['LK21DL']}{link}")
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
        print(self.tbl)
        self.tbl.clear_rows()
        driver.quit()

    def get_info(self, title, link):
        if "Series" in title:
            res = requests.get(f"{Settings().link['LK21INFO']}{link.split('/')[-2]}/", headers=Settings().headers)
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
        res = requests.get(Settings().link['LK21'], params={"s": title}, headers=Settings().headers)
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