import time

from bs4 import BeautifulSoup
from openpyxl import Workbook
import requests
import password

URL = []
NAME_EXCEL = 'test.xlsx'

with open('url_categoria', 'r') as ff:
    for line in ff:
        URL.append(line.replace('\n', ''))

_WD = Workbook()
_WS = _WD.active

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/81.0.4044.96 YaBrowser/20.4.0.1461 Yowser/2.5 Safari/537.36',
    'accept': '*/*'}


def get_date_url(URL):
    """
    Сбор данных и сохранений файлы в формате xlsx

    :param URL:
    :return:
    """
    _start_position = 0
    _end_position = 0
    session = requests.Session()
    list_pages = []

    for url in URL:
        """
        Сначала цикл проходит по url взятых с файла
        """
        post_r = session.post(url=url, auth=(
            password.login(), password.pas()), headers=headers)

        soup = BeautifulSoup(post_r.text, "lxml")

        page = soup.find('div', class_='page_nav').find_all('a')
        try:
            max_pages_url = int(page[-1].get('href').split('=')[-1])
            for np in range(max_pages_url):
                MAX_PAGE_URL = f'?AVILIBILLITY=Y&PAGEN_1={np + 1}'
                _str_urls = url + MAX_PAGE_URL
                list_pages.append(_str_urls)
        except AttributeError:
            MAX_PAGE_URL = f'?AVILIBILLITY=Y&PAGEN_1=1'
            _str_urls = url + MAX_PAGE_URL
            list_pages.append(_str_urls)

        for url in list_pages:
            """
            Проходит по циклу. Смотрим на категорию и если у нее дополнительные страницы 
            """
            post_r = session.post(url=url, auth=(
                password.login(), password.pas()), headers=headers)

            soup = BeautifulSoup(post_r.text, "lxml")

            _items = soup.find_all("table", class_="list_items_table")
            _items = soup.find("div", class_="catalog_items").find('table').find_all('tr')
            for enum, i in enumerate(_items):
                """
                Сохраниение данных в формат 
                """
                if enum == 0:
                    _WS['A1'] = 'КОД'
                    _WS['B1'] = 'Наименование'
                    _WS['C1'] = 'Размер'
                    _WS['D1'] = 'ОПТ-14%'
                    _WS['E1'] = 'РРЦ'

                else:
                    _required_data = [v.text.replace("\n", '').strip().replace("  ", '') for v in i.find_all('td')]
                    _heder = _required_data[1].replace(",", ' ')
                    _WS[f'A{enum + 1 + _start_position}'] = _required_data[3]
                    _WS[f'B{enum + 1 + _start_position}'] = _heder
                    _WS[f'C{enum + 1 + _start_position}'] = _required_data[2]
                    _WS[f'D{enum + 1 + _start_position}'] = _required_data[10]
                    _WS[f'E{enum + 1 + _start_position}'] = _required_data[13]
                    _end_position = enum
            _start_position += _end_position
            _WD.save(NAME_EXCEL)
        list_pages.clear()


def main():
    tic = time.perf_counter()
    get_date_url(URL)
    toc = time.perf_counter()
    print(f"Вычисление заняло {toc - tic:0.4f} секунд")


if __name__ == "__main__":
    main()
