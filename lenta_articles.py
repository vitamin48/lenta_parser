""" Парсер магазина лента. Получить список артикулов товаров по ссылке на каталог. """

from pathlib import Path

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

class Lenta_Articles:
    def __init__(self):
        self.save_path = f'{str(Path(__file__).parents[1])}'
        self.__main_url = 'https://lenta.com/product'
