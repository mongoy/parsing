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
import time
import datetime
import json
import csv
import os

# from .settings import *
# скрытый ввод пароля
from getpass import getpass
# Импортируем библиотеку по работе с SMTP
import smtplib
# Добавляем необходимые подклассы - MIME-типы
import mimetypes  # Импорт класса для обработки неизвестных MIME-типов,
# базирующихся на расширении файла
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения
from email.mime.audio import MIMEAudio  # Аудио
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект

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


# def processing_attachement(msg, files):
#     """
#     Функция по обработке списка, добавляемых к сообщению файлов
#     :param msg: почтовое сообщение
#     :param files: путь к файлу(ам) вложения
#     :return:
#     """
#     for f in files:
#         if os.path.isfile(f):  # Если файл существует
#             attach_file(msg, f)  # Добавляем файл к сообщению
#         elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
#             dir_files = os.listdir(f)  # Получаем список файлов в папке
#             for file in dir_files:  # Перебираем все файлы и...
#                 attach_file(msg, f + "/" + file)  # ...добавляем каждый файл к сообщению
#
#     return
#
#
# def attach_file(msg, filepath):
#     """
#     Функция по добавлению конкретного файла к сообщению
#     :param msg: почтовое сообщение
#     :param filepath: путь к файлу(ам) вложения
#     :return:
#     """
#     filename = os.path.basename(filepath)  # Получаем только имя файла
#     ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
#     if ctype is None or encoding is not None:  # Если тип файла не определяется
#         ctype = 'application/octet-stream'  # Будем использовать общий тип
#     maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
#     if maintype == 'text':  # Если текстовый файл
#         with open(filepath) as fp:  # Открываем файл для чтения
#             file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
#             fp.close()  # После использования файл обязательно нужно закрыть
#     elif maintype == 'image':  # Если изображение
#         with open(filepath, 'rb') as fp:
#             file = MIMEImage(fp.read(), _subtype=subtype)
#             fp.close()
#     elif maintype == 'audio':  # Если аудио
#         with open(filepath, 'rb') as fp:
#             file = MIMEAudio(fp.read(), _subtype=subtype)
#             fp.close()
#     else:  # Неизвестный тип файла
#         with open(filepath, 'rb') as fp:
#             file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
#             file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
#             fp.close()
#             encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
#     file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
#     msg.attach(file)  # Присоединяем файл к сообщению
#
#
# def send_email(msg_subj, msg_text, files):
#     """
#     Отправка на e-mail
#     :param msg_subj: тема сообщения
#     :param msg_text: текст сообщения
#     :param files: путь к файлу(ам) вложения
#     :return:
#     """
#     # addr_from = input('Введите e-mail отправителя:')
#     password = getpass(f'Введите пароль ({addr_from}):')  # Пароль
#     # addr_to = input('Введите e-mail получателя:')
#
#     msg = MIMEMultipart()  # Создаем сообщение
#     msg['From'] = addr_from  # Адресат
#     msg['To'] = addr_to  # Получатель
#     msg['Subject'] = msg_subj  # Тема сообщения
#
#     body = msg_text
#     msg.attach(MIMEText(body, 'plain'))  # Добавляем в сообщение текст
#     # присоединение файла
#     processing_attachement(msg, files)
#
#     server = smtplib.SMTP('smtp.mail.ru', 25)  # Создаем объект SMTP для MAIL.RU
#     # server.set_debuglevel(True)  # Включаем режим отладки - если отчет не нужен, строку можно закомментировать
#     server.starttls()  # Начинаем шифрованный обмен по TLS
#     server.login(addr_from, password)  # Получаем доступ
#     server.send_message(msg)  # Отправляем сообщение
#     server.quit()  # Выходим
#
#     return


def save_to_file(src, num_row):
    # save page to file
    with open(rf"html\index{num_row}.html", "w", encoding='utf-8') as file:
        file.write(src)


def read_file(num_row):
    # read page from file
    with open(rf"html\index{num_row}.html", "r", encoding='utf-8') as file:
        src = file.read()
    return src


def get_page(url, params=''):
    # get context page from url
    req = requests.get(url, headers=HEADERS, params=params)
    status = req.status_code
    src = req.text
    return status, src


def get_data(src, count_vacancy):
    page_bs = bs(src, 'lxml')
    tags = page_bs.find_all('div', class_='vacancy-serp-item')
    vacancies_dict = {}
    for tag in tags:
        vacancy_dict = {}
        vacancy_name = tag.find("a", class_="bloko-link")  # vacancy name
        vacancy_compensation = tag.find("div", class_="vacancy-serp-item__sidebar").text.replace(u"\u00A0", "")
        if vacancy_compensation is None:
            vacancy_compensation = '-'

        vacancy_url = vacancy_name["href"]  # link vacancy
        if vacancy_url is None:
            vacancy_url = '-'

        vacancy_org = tag.find("a", class_="bloko-link bloko-link_secondary")  # the name of organization

        org_link = HOST + vacancy_org["href"][1:]

        vacancy_place = tag.find("span", class_="vacancy-serp-item__meta-info")

        vacancy_response = HOST + tag.find("div",
                                           class_="vacancy-serp-item__controls-item "
                                                  "vacancy-serp-item__controls-item_response"
                                           ).find('a')['href'][1:].strip()

        vacancy_time = tag.find("span", class_="vacancy-serp-item__publication-date "
                                               "vacancy-serp-item__publication-date_short")
        if vacancy_time is None:
            vacancy_time = '-'
        else:
            vacancy_time = vacancy_time.text.strip()

        vacancy_dict['place'] = vacancy_place.text.strip()
        vacancy_dict['compensation'] = vacancy_compensation
        vacancy_dict['name'] = vacancy_name.text.strip()
        vacancy_dict['url'] = vacancy_url.strip()
        vacancy_dict['org'] = vacancy_org.text.strip()
        vacancy_dict['org_link'] = org_link
        vacancy_dict['response'] = vacancy_response
        vacancy_dict['time'] = vacancy_time

        vacancies_dict[count_vacancy] = vacancy_dict

        # print vacancies
        print(str(count_vacancy) + ' - ', vacancy_place.text.strip() + ' - ',
              vacancy_compensation + '\n',
              vacancy_name.text.strip() + ' - ',
              vacancy_url.strip() + '\n',
              vacancy_org.text.strip() + ' - ',
              org_link + '\n',
              'Откликнуться -',
              vacancy_response + '\n',
              vacancy_time + '\n'
              )
        count_vacancy += 1

    return vacancies_dict, count_vacancy


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


def get_data_all_url(url, num_page):
    # get data from URL
    for num in range(num_page):
        html = get_page(URL, params={'page': f'{num}'})
        save_to_file(html[1], num)
        print(f'Готово - {num + 1}. Ждём перед загрузкой следующей страницы...')
        time.sleep(3)
    print(f'Готово - {num + 1} из {num_page}')
    return


def get_data_all_file(num_page):
    # get data from file
    all_vacancy_dict = {}
    count_vacancy = 1
    # save headers into the csv
    headers = ['place', 'compensation', 'name', 'url', 'org', 'org_link', 'response', 'time']
    with open("all_vacancy_dict.csv", "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

    for num in range(num_page):
        one_page_vacancies = get_data(read_file(num), count_vacancy)
        count_vacancy = one_page_vacancies[1]
        vac = []
        for key in one_page_vacancies[0]:
            all_vacancy_dict[key] = one_page_vacancies[0][key]
            for vac_vol in all_vacancy_dict[key].values():
                print(vac_vol)
                vac.append(vac_vol)
        # append data into csv-file
        with open("all_vacancy_dict.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(vac)
    # save data into the jason-file
    with open("all_vacancy_dict.json", "w", encoding="utf-8") as file:
        json.dump(all_vacancy_dict, file, indent=4, ensure_ascii=False)

    return


# def send_sub():
#     """
#     Отправка почтового сообщения с почтового сервера MAIL.RU
#     :return:
#     """
#     files = [r"HH\all_vacancy_dict.json"]
#     now = datetime.datetime.now()
#     msg_subj = "Вакансии с HH.ru"
#     msg_text = "HH. Список вакансий на " + str(now.strftime("%d-%m-%Y %H:%M"))
#     send_email(msg_subj, msg_text, files)
#     return


def parser():
    # operating mode
    operating_mode = input('Парсинг файлов html (1) или сохранение страниц сайта (2):')

    if operating_mode == "2":
        print(operating_mode)
        # html = get_page(URL, params={'page': 0})
        # if html[0] == 200:
        #     num_pages = get_pages_num(html[1])
        #     print(f'Всего {num_pages} страниц')
        #     # get data from URL one or all pages
        #     get_data_all_url(URL, num_pages)
        #     # parsing saved html file
        #     # html = read_file(0)
        #     get_data_all_file(num_pages)
        # else:
        #     print("Нет доступа!!!")

    elif operating_mode == "1":
        print(operating_mode)
        # if os.path.exists(r"HH\html\index0.html"):
        with open(r"html\index0.html", "r", encoding="utf-8") as fp:
            num_pages = get_pages_num(fp)
            print(f'Всего {num_pages} страниц')
            get_data_all_file(num_pages)
    else:
        # error
        print("Введите '1' или '2'\n")
        return None


if __name__ == '__main__':
    parser()


