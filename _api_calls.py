import datetime

import bybit
import requests
from bs4 import BeautifulSoup
import os


def get_dollar():
    today = datetime.date.today()
    link = f"http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req={today.day if len(str(today.day)) == 2 else '0' + str(today.day)}/{today.month if len(str(today.month)) == 2 else '0' + str(today.month)}/{today.year}"
    response = requests.get(link)
    soup = BeautifulSoup(response.text, features="html.parser")
    found = soup.find("name", string="US Dollar")
    return found.parent.value.text


class WorkClientCredentials:
    api_key = os.getenv('api_key')
    api_secret = os.getenv('api_secret')


client = bybit.bybit(test=False, api_key=WorkClientCredentials.api_key,
                     api_secret=WorkClientCredentials.api_secret)


def get_balance():
    try:
        balance = client.Wallet.Wallet_getBalance(coin="BTC").result()[0]['result']['BTC']['equity']
        return balance
    except TypeError as ex:
        bot_reply = "Вам нужно добавить api_key и api_secret в переменные среды," \
                    "чтобы узнать ваш баланс."
        return bot_reply


def get_valuta():
    info = client.Market.Market_symbolInfo().result()
    return info[0]['result']


def get_bitcoin():
    valuta = get_valuta()
    for dict_crype in valuta:
        if dict_crype['symbol'] == "BTCUSD":
            last_price = float(dict_crype['last_price'])
            return last_price


def get_ethereum():
    valuta = get_valuta()
    for dict_crype in valuta:
        if dict_crype['symbol'] == "ETHUSD":
            last_price = float(dict_crype['last_price'])
            return last_price


def hello():
    return "Тут будет приветствие."


def bye():
    return "Тут будет прощание."
