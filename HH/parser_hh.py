"""
Parsing site hh.ru - information about vacancy - Python data engineer
url = 'https://chita.hh.ru/search/vacancy?clusters=true&no_magic=true&items_on_page=
100&order_by=publication_time&enable_snippets=true&search_period=3&salary=&st=searchVacancy&text=data+engineer'
https://chita.hh.ru/search/vacancy?st=searchVacancy&text=data+engineer&area=113&salary=&currency_code=RUR&
experience=doesNotMatter&schedule=remote&order_by=publication_time&search_period=3&items_on_page=100&
no_magic=true&L_save_area=true
"""
import requests
from bs4 import BeautifulSoup as bs
import collections
import time
import random
import json
import csv


HOST = 'https://chita.hh.ru/'

URL = 'https://chita.hh.ru/search/vacancy?st=searchVacancy&text=data+engineer&area=113&salary=&currency_code=RUR&' \
      'experience=doesNotMatter&schedule=remote&order_by=publication_time&search_period=3&items_on_page=20&' \
      'no_magic=true&L_save_area=true&page='

HEADERS = {
    'Host': 'chita.hh.ru',
    'User-agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Content-type': 'application/text',
    'Connection': 'keep-alive'
}


def save_to_file(src, num_row):
    # save page to file
    with open(f"html\index{num_row}.html", "w", encoding='utf-8') as file:
        file.write(src)


def read_file(num_row):
    # read page from file
    with open(f"html\index{num_row}.html", "r") as file:
        src = file.read()
    return src


def get_page(url, params=''):
    req = requests.get(url, headers=HEADERS, params=params)
    status = req.status_code
    src = req.text
    return status, src


def get_pages_num(src):
    """
    Number of paginator pages
    :return:
    """
    page_bs = bs(src, "html.parser")
    try:
        return int(page_bs.find_all("span", class_="pager-item-not-in-short-range")[-1].text.strip())
    except:
        # only one page
        return 1


def get_data_url(src, num):
    # Data from one page
    save_to_file(src, num)
    #
    get_data(src)


def get_data_file(src, num):
    # Data from one file
    get_data(read_file(num))


def get_data(src):
    page_bs = bs(src, 'lxml')
    tags = page_bs.find_all('div', class_='vacancy-serp-item')

    for tag in tags:
        vacancy_name = tag.find("a", class_="bloko-link")  # vacancy name
        vacancy_compensation = tag.find("div", class_="vacancy-serp-item__sidebar").text
        if vacancy_compensation is None:
            vacancy_compensation = '-'

        vacancy_url = vacancy_name["href"]  # link vacancy
        if vacancy_url is None:
            vacancy_url = '-'

        vacancy_org = tag.find("a", class_="bloko-link bloko-link_secondary")  # the name of organization

        org_link = HOST + vacancy_org["href"][1:]

        vacancy_place = tag.find("span", class_="vacancy-serp-item__meta-info").text.strip()

        vacancy_response = HOST + tag.find("div",
                                           class_="vacancy-serp-item__controls-item "
                                                  "vacancy-serp-item__controls-item_response"
                                           ).find('a')['href'][1:].strip()

        vacancy_time = tag.find("span", class_="vacancy-serp-item__publication-date "
                                               "vacancy-serp-item__publication-date_short").text.strip()

        print(vacancy_place + ' - ',
              vacancy_compensation + '\n',
              vacancy_name.text.strip() + ' - ',
              vacancy_url.strip() + '\n',
              vacancy_org.text.strip() + ' - ',
              org_link + '\n',
              'Откликнуться -',
              vacancy_response + '\n',
              vacancy_time + '\n'
              )

    return


def get_data_all_url(url, num_page):
    # get data from URL
    for num in range(num_page):
        html = get_page(URL, params={'page': f'{num}'})
        get_data_url(html[1], num)
        print(f'Готово - {num + 1}. Ждём перед загрузкой следующей страницы...')
        time.sleep(3)
    print(f'Готово - {num + 1} из {num_page}')
    return


def get_data_all_file(num_page):
    # get data from file
    for num in range(num_page):
        get_data_file(num)

    return


def parser():
    html = get_page(URL, params={'page': 0})
    if html[0] == 200:
        num_pages = get_pages_num(html[1])
        print(f'Всего {num_pages} страниц')
        # get data from URL one or all pages
        # get_data_page(html[1], 0)
        get_data_all_url(URL, num_pages)
    else:
        print("Нет доступа!!!")


parser()
