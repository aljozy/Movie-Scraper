import os
from datetime import datetime
import time
from selenium import webdriver
from Torrent import constants as const

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import numpy as np


class Torrent(webdriver.Chrome):
    chrome_options = Options()

    chrome_options.add_experimental_option("prefs",
                                           {"profile.default_content_setting_values.notifications": 2
                                            })

    def __init__(self, driver_path=r"C:\Users\www.abcom.in\Music", tear_down=False):
        self.tear_down = tear_down
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path

        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--headless')

        super(Torrent, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

        # capturing urls

    def muvi(self):
        self.get(const.POPULAR["muvi"])
        print("----------------------POPULAR Movies TODAY--------------------------")
        self.fetch_data()

    def tv(self):
        self.get(const.POPULAR["tv"])
        print("----------------------POPULAR TV TODAY--------------------------")
        self.fetch_data()

    def anime(self):
        self.get(const.POPULAR["anime"])
        print("----------------------POPULAR Anime TODAY--------------------------")
        self.fetch_data()

    def top100_muvi(self):
        self.get(const.TOP100["muvi"])
        print("----------------------TOP 100 Movies--------------------------")
        self.fetch_data()

    def top100_anime(self):
        self.get(const.TOP100["anime"])
        print("----------------------TOP 100 Anime--------------------------")
        self.fetch_data()

    def top100_tv(self):
        self.get(const.TOP100["tv"])
        print("----------------------TOP 100 tv--------------------------")
        self.fetch_data()

    def top100_doc(self):
        self.get(const.TOP100["doc"])
        print("----------------------TOP 100 doc--------------------------")
        self.fetch_data()

    def top100_other(self):
        self.get(const.TOP100["other"])
        print("----------------------TOP 100 Other--------------------------")
        self.fetch_data()

    def info_hash(self):
        hash_info = self.find_element(by=By.CSS_SELECTOR, value='div[class="infohash-box"] p span')
        return hash_info.text

    def links(self):
        links = self.find_elements(by=By.CSS_SELECTOR, value="div[class='table-list-wrap'] tbody td.coll-1.name a")

        valid_link = []
        count = 0
        for link in links:
            u = link.get_attribute('href')
            url = u.split()
            if count % 2 == 1:
                valid_link.append(url)
                # print(url)
            count += 1
        return valid_link

    def fetch_data(self):
        all_links = self.links()
        collection = []
        for linker in all_links:

            for link in linker:
                self.get(link)
                name = self.get_name()
                info_hash = self.info_hash()
                magnet = self.get_magnet_link()
                size = self.get_size()
                seeders = self.get_seeders()
                leechers = self.get_leechers()
                timer = self.get_datetime()
                collection.append([name, size, seeders, leechers, info_hash])

                time.sleep(2)
        np.savetxt(f'torrent_{timer}.csv',
                   collection,
                   delimiter=",",
                   fmt='% s')

    def get_name(self):
        t_name = self.find_element(by=By.XPATH, value="//div/h1")
        name = t_name.text
        return name

    def get_magnet_link(self):
        magnt_link = self.find_element(by=By.XPATH, value="(//ul//li)[37]/a")
        magnet = magnt_link.get_attribute("href")
        return magnet

    def get_size(self):
        size = self.find_element(by=By.XPATH, value="//ul/li/strong[text()='Total size']/../span")
        return size.text

    def get_seeders(self):
        seed = self.find_element(by=By.XPATH, value="//ul/li/strong[text()='Seeders']/../span")
        return seed.text

    def get_leechers(self):
        leech = self.find_element(by=By.XPATH, value="//ul/li/strong[text()='Leechers']/../span")
        return leech.text

    def get_datetime(self):
        now = datetime.now()

        current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
        return current_time
