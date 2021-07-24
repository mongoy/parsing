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
    response = requests.get(url=f"{URL}depth/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")
    with open("depth.txt", "w") as file:
        file.write(response.text)

    bids = response.json()[f"{coin1}_{coin2}"]["bids"]
    total_bids_amount = 0
    for item in bids:
        price = item[0]
        coin_amount = item[1]
        total_bids_amount += coin_amount * price

    return f"Total bids:{total_bids_amount} $"


def get_trades(coin1='btc', coin2='usd', limit=150):
    # get info about cryptocurrency pairs eth_btc and xrp_btc)
    response = requests.get(url=f"{URL}trades/{coin1}_{coin2}?limit={limit}&ignore_invalid=1")
    with open("trades.txt", "w") as file:
        file.write(response.text)

    total_trades_ask = 0
    total_trades_bid = 0
    for item in response.json()[f"{coin1}_{coin2}"]:
        if item["type"] == 'ask':
            total_trades_ask += item["price"] * item["amount"]
        else:
            total_trades_bid += item["price"] * item["amount"]
    info = f"[-] Total {coin1} Sell:{round(total_trades_ask, 2)} $ \n" \
           f"[+] Total {coin1} Sell:{round(total_trades_bid, 2)} $"
    return info


def parser():
    # print(get_info())
    # print(get_ticker())
    # print(get_depth(limit=150))
    # print(get_depth(limit=2000))
    print(get_trades(limit=150))


if __name__ == "__main__":
    parser()
