import time

from bs4 import BeautifulSoup
from openpyxl import Workbook
import requests
import password

URL = []

with open('url_categoria', 'r') as ff:
    for line in ff:
        URL.append(line.replace('\n', ''))

WD = Workbook()
ws = WD.active

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/81.0.4044.96 YaBrowser/20.4.0.1461 Yowser/2.5 Safari/537.36',
    'accept': '*/*'}


def get_date(URL):
    n = 0
    pothic = 0
    session = requests.Session()
    list_pages = []
    for url in URL:
        post_r = session.post(url=url, auth=(
            password.login(), password.pas()), headers=headers)

        soup = BeautifulSoup(post_r.text, "lxml")

        page = soup.find('div', class_='page_nav').find_all('a')
        try:
            max_pages_url = page[-1].get('href').split('=')[-1]
            for np in max_pages_url:
                MAX_PAGE_URL = f'?AVILIBILLITY=Y&PAGEN_1={np}'
                _str_urls = url + MAX_PAGE_URL
                list_pages.append(_str_urls)
        except AttributeError:
            list_pages.append(url)
            continue

    for url in list_pages:
        post_r = session.post(url=url, auth=(
            password.login(), password.pas()), headers=headers)

        soup = BeautifulSoup(post_r.text, "lxml")

        _items = soup.find_all("table", class_="list_items_table")
        _items = soup.find("div", class_="catalog_items").find('table').find_all('tr')
        for enum, i in enumerate(_items):
            if enum == 0:
                ws['A1'] = 'КОД'
                ws['B1'] = 'Наименование'
                ws['C1'] = 'Размер'
                ws['D1'] = 'ОПТ-14%'
                ws['E1'] = 'РРЦ'

            else:
                k = [v.text.replace("\n", '').strip().replace("  ", '') for v in i.find_all('td')]
                h = k[1].replace(",", ' ')
                ws[f'A{enum + 1 + n}'] = k[3]
                ws[f'B{enum + 1 + n}'] = h
                ws[f'C{enum + 1 + n}'] = k[2]
                ws[f'D{enum + 1 + n}'] = k[10]
                ws[f'E{enum + 1 + n}'] = k[13]
                pothic = enum
        n += pothic
        WD.save('text2.xlsx')
    list_pages.clear()


def main():
    tic = time.perf_counter()
    get_date(URL)
    # asyncio.run(gather_data())
    toc = time.perf_counter()
    print(f"Вычисление заняло {toc - tic:0.4f} секунд")


if __name__ == "__main__":
    main()
