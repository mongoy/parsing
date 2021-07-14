"""
Parsing site hh.ru - information about vacancy - Python data engineer
url = 'https://chita.hh.ru/search/vacancy?clusters=true&no_magic=true&items_on_page=
100&order_by=publication_time&enable_snippets=true&search_period=3&salary=&st=searchVacancy&text=data+engineer'
https://chita.hh.ru/search/vacancy?st=searchVacancy&text=data+engineer&area=113&salary=&currency_code=RUR&
experience=doesNotMatter&schedule=remote&order_by=publication_time&search_period=3&items_on_page=100&
no_magic=true&L_save_area=true
"""
import requests
from bs4 import BeautifulSoup
import lxml


HOST = 'https://chita.hh.ru/'
# URL = 'https://chita.hh.ru/search/vacancy?area=113&clusters=true&enable_snippets=true&items_on_page=100&' \
#       'no_magic=true&order_by=publication_time&search_period=3&text=data+engineer&' \
#       'schedule=remote&from=cluster_schedule&showClusters=true'
URL = 'https://chita.hh.ru/search/vacancy?st=searchVacancy&text=data+engineer&area=113&salary=&currency_code=RUR&' \
      'experience=doesNotMatter&schedule=remote&order_by=publication_time&search_period=3&items_on_page=100&' \
      'no_magic=true&L_save_area=true'
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
    items = soup.find_all("div", class_="vacancy-serp-item")
    print(len(items))
    for count, item in enumerate(items):
        # the choice remote vacancy
        remote = item.find("div", class_="bloko-text-tertiary").text.strip()
        if remote is not None:
            # Можно работать из дома
            # print(remote)
            vacancy_name = item.find("a", class_="bloko-link")  # the name of vacancy
            vacancy_url = vacancy_name["href"]
            if vacancy_url is None:
                vacancy_url = '-'
            vacancy_org = item.find("a", class_="bloko-link bloko-link_secondary")  # the name of organization
            org_link = HOST + vacancy_org["href"][1:]
            vacancy_place = item.find("span", class_="vacancy-serp-item__meta-info").text.strip()
            print(count, vacancy_place, vacancy_name.text.strip(), vacancy_url, vacancy_org.text.strip(), org_link)

    return vacancies_list


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        print(get_content(html.text))
    else:
        print("Нет доступа!!!")


parser()
