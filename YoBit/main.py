"""
https://www.youtube.com/watch?v=Z-JXVIbygm0
https://yobitex.net/ru/ - Биржа биткоин и криптовалют!
https://yobitex.net/ru/api - API
"""
import requests
import json


URL = "https://yobit.net/api/3/"


def get_info():
    # get info about cryptocurrency pairs
    response = requests.get(url=f"{URL}info")
    with open("info.txt", "w") as file:
        file.write(response.text)
    return response.text


def get_ticker(coin1='btc', coin2='usd'):
    # get info about cryptocurrency pairs eth_btc and xrp_btc)
    response = requests.get(url=f"{URL}ticker/{coin1}_{coin2}?ignore_invalid=1")
    with open("ticker.txt", "w") as file:
        file.write(response.text)
    return response.text


def get_depth(coin1='btc', coin2='usd', limit=150):
    # get info about  cryptocurrency pairs eth_btc)
    response = requests.get(url=f"{URL}depth/{coin1}_{coin2}?{limit}=150&ignore_invalid=1")
    with open("depth.txt", "w") as file:
        file.write(response.text)
    return response.text


def parser():
    # print(get_info())
    # print(get_ticker())
    print(get_depth())


if __name__ == "__main__":
    parser()
