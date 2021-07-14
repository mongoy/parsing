"""
Parsing site hh.ru - information about vacancy - Python data engineer
url = 'https://chita.hh.ru/search/vacancy?clusters=true&no_magic=true&items_on_page=
100&order_by=publication_time&enable_snippets=true&search_period=3&salary=&st=searchVacancy&text=data+engineer'
"""
import requests
from bs4 import BeautifulSoup
import lxml


URL = 'https://chita.hh.ru/search/vacancy?clusters=true&no_magic=true&items_on_page=100&' \
      'order_by=publication_time&enable_snippets=true&search_period=3&salary=&st=searchVacancy&text=data+engineer'
HEADERS = {
    'Host': 'chita.hh.ru',
    'User-agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Content-type': 'application/text',
    'Connection': 'keep-alive'
}


def get_html(url, params=''):
    """
    Get content from url
    :param url:
    :param params:
    :return:
    """
    response = requests.get(URL, headers=HEADERS, params=params)
    return response


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    vacancies_list = []
    items = soup.find_all('dav', class_='vacancy-serp-item vacancy-serp-item_premium')
    for item in items:
        print(item)

    return vacancies_list


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        print(get_content(html.text))
    else:
        print("Нет доступа!!!")


parser()
