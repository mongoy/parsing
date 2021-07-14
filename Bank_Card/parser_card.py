# https://www.youtube.com/watch?v=ykjBVT57r68&t=971s
"""
Парсинг типов банковских карт
"""
import requests
from bs4 import BeautifulSoup
# import csv


HOST = 'https://minfin.com.ua/'
URL = 'https://minfin.com.ua/cards/'
HEADERS = {
    'accept': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 '
              'YaBrowser/21.6.0.616 Yowser/2.5 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.106 YaBrowser/21.6.0.616 Yowser/2.5 Safari/537.36',
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
    """
    Faind all tags with attribute class = 'sc-14ydfjo-0 jYdA-De' - card description
    :param html:
    :return:
    """
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="sc-14ydfjo-0 jYdA-De")
    cards_list = []
    for count, item in enumerate(items):
        """
        list cards
        """
        tag_name = item.find('a', class_="sc-6nr3q5-0 iyqRre")  # name card

        if tag_name is not None:
            tag_linc = HOST + item.find('a', class_="sc-6nr3q5-0 iyqRre")['href'][1:]  #

        else:
            tag_name = item.find('div', class_="sc-6nr3q5-0 iyqRre")
            tag_linc = '-'

        tag_bank = item.find('span', class_="bfjox4-20 jtOFL")  # bank
        tag_img = item.find('img', class_="bfjox4-10 ekxCIS")['src']  # image

        cards_list.append(
            {
                'title': tag_name.text.strip(),
                'bank': tag_bank.text.strip(),
                'link': tag_linc,
                'image': tag_img,
            }
        )

    return cards_list


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        print(get_content(html.text))
        print("Количество карт -", len(get_content(html.text)))
    else:
        print("Нет доступа!!!")


parser()
