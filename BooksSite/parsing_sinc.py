import json
import time
import requests
from bs4 import BeautifulSoup as bs
import datetime
import csv

HOST = 'https://www.labirint.ru'

URL = 'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table'

HEADERS = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.114 YaBrowser/21.6.1.274 Yowser/2.5 Safari/537.36",
    'Accept': '*/*',
}


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


def get_pages_num(src):
    """
    Number of paginator pages
    :return:
    """
    page_bs = bs(src, "html.parser")
    try:
        return int(page_bs.find_all("a", class_="pagination-number__text")[-1].text.strip())
    except:
        # only one page
        return 1


def get_data(src, book_count, file_name):
    books_dict = {}
    page_bs = bs(src, 'lxml')
    books_items = page_bs.find("tbody", class_="products-table__body").find_all("tr")
    for item in books_items:

        book_data = item.find_all("td")
        try:
            book_title = book_data[0].find("a").text.strip()

        except:
            book_title = "Нет названия книги"

        try:
            book_author = book_data[1].find("a").text.strip()
        except:
            book_author = "Нет автора"

        try:
            book_publishing = book_data[2].find_all("a")[0].text.strip()
            book_publishing += " : " + book_data[2].find_all("a")[1].text.strip()
        except:
            book_publishing = "Нет издательства"

        try:
            book_new_price = int(book_data[3].find("span", class_="price-val")
                                 .find("span").text.strip().replace(" ", ""))
        except:
            book_new_price = "Нет новой цены"

        try:
            book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
        except:
            book_old_price = "Нет старой цены"

        try:
            # book_discount = book_data[3].find("span", class_="price-val")["title"].strip()
            book_discount = round(((book_old_price - book_new_price) / book_old_price) * 100)
        except:
            book_discount = "Нет скидки"

        try:
            book_status = book_data[5].find("div").text.strip()
        except:
            book_status = "Нет статуса"

        book_dict = {
            "book_title": book_title,
            "book_author": book_author,
            "book_publishing": book_publishing,
            "book_new_price": book_new_price,
            "book_old_price": book_old_price,
            "book_discount": book_discount,
            "book_status": book_status
        }
        books_dict[book_count] = book_dict
        book_count += 1
        with open(f"{file_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                        (
                            book_title,
                            book_author,
                            book_publishing,
                            book_new_price,
                            book_old_price,
                            book_discount,
                            book_status
                         )
            )
    # print(books_list)
    return books_dict, book_count


def get_data_all_url(url, num_page):
    # get data from URL
    for num in range(num_page):
        html = get_page(url, params={'page': f'{num}'})
        save_to_file(html[1], num)
        print(f'Готово - {num + 1}. Ждём перед загрузкой следующей страницы...')
        time.sleep(3)
    print(f'Готово - {num + 1} из {num_page}')
    return


def get_data_all_file(num_page):
    # get data from file
    cur_time = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M")
    file_name = f"labirint_{cur_time}"
    # save data into csv-file
    headers = [
        'book_title',
        'book_author',
        'book_publishing',
        'book_new_price',
        'book_old_price',
        'book_discount',
        'book_status'
    ]
    with open(f"{file_name}.csv", "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=";")
        writer.writeheader()
        # writer = csv.writer(file, delimiter=";")
        # writer.writerow(
        #     ("Название",
        #      "Автор",
        #      "Издательство",
        #      "Новая цена",
        #      "Старая цена",
        #      "Скидка",
        #      "Статус")
        # )
    all_book_dict = {}
    book_count = 1
    for num in range(num_page):
        one_page_books = get_data(read_file(num), book_count, file_name)
        book_count = one_page_books[1]
        book = []
        for key in one_page_books[0]:
            all_book_dict[key] = one_page_books[0][key]
            for book_vol in all_book_dict[key].values():
                book.append(book_vol)
        # append data into csv-file
        with open(f"{file_name}.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(book)

        print(f"Обработана {num + 1}/{num_page}")
        # print(all_book_dict)
        time.sleep(1)
    # save data into json-file
    with open(f"{file_name}.json", "a", encoding="utf-8") as file:
        json.dump(all_book_dict, file, indent=4, ensure_ascii=False)

    return


def main():
    # operating mode
    start_time = time.time()
    operating_mode = input('Парсинг файлов html (1) или сохранение страниц сайта (2):')
    if operating_mode == "2":
        html = get_page(URL, params={'page': 0})
        if html[0] == 200:
            num_pages = get_pages_num(html[1])
            print(f'Всего {num_pages} страниц')
            # get data from URL one or all pages
            get_data_all_url(URL, num_pages)
            # parsing saved html file
            # get_data_all_file(num_pages)
        else:
            print("Нет доступа!!!")

    elif operating_mode == "1":
        # if os.path.exists(r"HH\html\index0.html"):
        with open(r"html\index0.html", "r", encoding="utf-8") as fp:
            num_pages = get_pages_num(fp)
            print(f'Всего {num_pages} страниц')
            get_data_all_file(num_pages)
    else:
        # error
        print("Введите '1' или '2'\n")
        return None
    finish_time = time.time() - start_time
    print(f"Время затраченное на выполнение скрипта:{finish_time}")


if __name__ == '__main__':
    main()
