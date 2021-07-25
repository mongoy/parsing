# https://www.youtube.com/watch?v=8LJllhrVJVw
# url = "https://roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc
# &filter_type=tires&arCatalogFilter_458_1500340406=Y&set_filter=Y&arCatalogFilter_463=668736523&PAGEN_1=1"
#
import requests


HOST = 'https://roscarservis.ru/'

URL = "https://roscarservis.ru/catalog/legkovye/?form_id=catalog_filter_form&filter_mode=params&sort=asc&" \
      "filter_type=tires&arCatalogFilter_458_1500340406=Y&set_filter=Y&arCatalogFilter_463=668736523&PAGEN_1=1"

HEADERS = {
    'Host': 'roscarservis.ru',
    'User-agent': 'Mozilla/5.0',
    'Accept': '*/*',
    'Content-type': 'application/text',
    'Connection': 'keep-alive'
}


def get_data():
    response = requests.get(url=URL, headers=HEADERS)
    # with open("index.html", "w", encoding='utf-8') as file:
    #     file.write(response.text)
    print(response.json())


def main():
    get_data()


if __name__ == '__main__':
    main()
