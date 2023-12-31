""" Парсер магазина лента. Получить список артикулов товаров по ссылке на каталог. """

from pathlib import Path
import requests
from requests.auth import HTTPBasicAuth
import time
from bs4 import BeautifulSoup

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def read_catalogs_from_txt():
    """Считывает и возвращает список актуальных каталогов из файла"""
    with open('catalogs.txt', 'r', encoding='utf-8') as file:
        catalogs = [f'{line}'.rstrip() for line in file]
        return catalogs


class LentaArticles:
    def __init__(self):
        self.save_path = f'{str(Path(__file__).parents[1])}'
        self.__options = Options()
        # self.__options = uc.ChromeOptions()
        self.__options.add_argument("--start-maximized")
        self.__options.add_argument('--blink-settings=imagesEnabled=false')
        self.__options.add_argument('--disable-blink-features=AutomationControlled')
        # self.__options.add_argument("--disable-extensions")
        # self.__options.add_experimental_option('useAutomationExtension', False)
        # self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__service = Service('chromedriver.exe')
        # self.browser = uc.Chrome(options=self.__options)
        self.browser = webdriver.Chrome(service=self.__service, options=self.__options)
        """Необходимо добавить, чтобы не было детектирования эмуляции"""
        self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            '''
        })
        self.all_art = []

    def get_arts_by_catalogs(self, catalogs):
        """Получить список товаров из каталога, проход по всем страницам"""
        for i in range(len(catalogs)):
            page = 1
            print(f'{bcolors.OKGREEN}{catalogs[i][8:]}{bcolors.ENDC}')
            while page != 0:
                try:
                    self.browser.get(f'{catalogs[i]}?page={page}')
                    print(self.browser.current_url)
                    time.sleep(1)
                    if self.browser.current_url != catalogs[i]:
                        soup = BeautifulSoup(self.browser.page_source, 'lxml')
                        products = soup.find('div', class_='catalog-grid__grid catalog-grid')
                        href = products.findAll('a',
                                                class_='lui-card lui-sku-product-card sku-card-small-container catalog-grid-sku-product-card')
                        for hr in href:
                            url = hr.attrs['href']
                            self.all_art.append(url)
                        page += 1
                    else:
                        page = 0
                except Exception as exp:
                    print(f'{bcolors.FAIL}ERROR: {exp}{bcolors.ENDC}')
                    time.sleep(10)
                    continue
        self.write_txt_file_articles()

    def write_txt_file_articles(self):
        with open('articles.txt', 'a') as output:
            for row in self.all_art:
                output.write(str(row) + '\n')


def main():
    catalogs = read_catalogs_from_txt()
    LentaArticles().get_arts_by_catalogs(catalogs)


if __name__ == '__main__':
    main()
