#https://www.youtube.com/watch?v=v0ifLIUTHUs&list=PLqGS6O1-DZLprgEaEeKn9BWKZBvzVi_la&index=13
# Error parsing
import requests
import time
from bs4 import BeautifulSoup as bs


HOST = 'https://chita.hh.ru/'

URL = 'https://chita.hh.ru/search/vacancy?st=searchVacancy&text=data+engineer&area=113&salary=&currency_code=RUR&' \
      'experience=doesNotMatter&schedule=remote&order_by=publication_time&search_period=3&items_on_page=20&' \
      'no_magic=true&L_save_area=true&page='

HEADERS = {
    'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.114 YaBrowser/21.6.1.274 Yowser/2.5 Safari/537.36",
    'Accept': '*/*',
}


def test_request(url, headers, retry=5):
    #
    try:
        response = requests.get(url=url, headers=headers)
        print(f"[+] {url} {response.status_code}")
    except Exception as ex:
        time.sleep(3)
        if retry:
            print(f"[INFO] retry={retry} => {url}\n{'-' * 20}")
            return test_request(url, retry=(retry - 1))
        else:
            raise
    else:
        return response


def main():
    with open("book_urls.txt") as file:
        book_urls = file.read().splitlines()
    # print(book_urls)
    for url in book_urls:
        try:
            r = test_request(url, HEADERS)
            soup = bs(r.text, "lxml")
            print(f"{soup.title.string}\n{'-' * 20}")
        except Exception as ex:
            continue


if __name__ == '__main__':
    main()