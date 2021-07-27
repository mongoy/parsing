# Asinc parsing
import json
import time
import requests
from bs4 import BeautifulSoup as bs
import datetime
import csv
import asyncio
import aiohttp


HOST = 'https://www.labirint.ru'

URL = 'https://www.labirint.ru/genres/2308/?available=1&paperbooks=1&display=table'

HEADERS = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.114 YaBrowser/21.6.1.274 Yowser/2.5 Safari/537.36",
    'Accept': '*/*',
}


async def get_page_data(session, page):
    # сбор и сохранение информации
    url = URL + f"&page={page}"
    async with session.get(url=url, headers=HEADERS) as response:
        response_text = await response.text()
        # page_bs = bs(response_text, 'lxml')
        # books_items = page_bs.find("tbody", class_="products-table__body").find_all("tr")
        # for item in books_items:
        #     print(page)
        #     book_data = item.find_all("td")
        #     try:
        #         book_title = book_data[0].find("a").text.strip()
        #
        #     except:
        #         book_title = "Нет названия книги"
        #
        #     try:
        #         book_author = book_data[1].find("a").text.strip()
        #     except:
        #         book_author = "Нет автора"
        #
        #     try:
        #         book_publishing = book_data[2].find_all("a")[0].text.strip()
        #         book_publishing += " : " + book_data[2].find_all("a")[1].text.strip()
        #     except:
        #         book_publishing = "Нет издательства"
        #
        #     try:
        #         book_new_price = int(book_data[3].find("span", class_="price-val")
        #                              .find("span").text.strip().replace(" ", ""))
        #     except:
        #         book_new_price = "Нет новой цены"
        #
        #     try:
        #         book_old_price = int(book_data[3].find("span", class_="price-gray").text.strip().replace(" ", ""))
        #     except:
        #         book_old_price = "Нет старой цены"
        #
        #     try:
        #         book_discount = round(((book_old_price - book_new_price) / book_old_price) * 100)
        #     except:
        #         book_discount = "Нет скидки"
        #
        #     try:
        #         book_status = book_data[5].find("div").text.strip()
        #     except:
        #         book_status = "Нет статуса"
        #
        #     books_data.append(
        #         {
        #             "book_title": book_title,
        #             "book_author": book_author,
        #             "book_publishing": book_publishing,
        #             "book_new_price": book_new_price,
        #             "book_old_price": book_old_price,
        #             "book_discount": book_discount,
        #             "book_status": book_status
        #         }
        #     )
        # print(f"Обработана страница {page}")


async def gather_data():
    # list tasks
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=URL, headers=HEADERS)
        page_bs = bs(await response.text(), "lxml")
        try:
            pages_count = int(page_bs.find_all("a", class_="pagination-number__text")[-1].text.strip())
        except:
            # only one page
            pages_count = 1

        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_page_data(session, page))
            tasks.append(task)

        await asyncio.gether(*tasks)


def main():
    # operating mode
    start_time = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(gather_data())
    finish_time = time.time() - start_time
    print(f"Время затраченное на выполнение скрипта:{finish_time}")


if __name__ == '__main__':
    main()


