# -*- coding: utf-8 -*-
from threading import Timer
from lxml import html
import requests
import config as cfg

previous = 11
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81'}
date = 'На 1 июля 2021 года'


def bot():
    global previous
    global date
    page = requests.get(cfg.url_rating, headers=headers, timeout=10)
    tree = html.fromstring(page.content)
    day = str(tree.xpath("//h1[contains(text(), 'года')]/text()"))[2:-2]
    if day == date:
        rating = tree.xpath("//td[contains(text(),'SURNAME')]/preceding-sibling::td[1]/text()")  # Place your surname instead of the 'SURNAME'
        rate = int(str(rating)[2:-2])
        diff = rate - previous
        if diff == 0:
            data = {'chat_id': cfg.chat_id, 'text': 'С прошедшего дня ничего не изменилось. Текущее место в рейтинге абитуриентов ' + day.lower() + ': ' + str(rate)}
            r = requests.post(cfg.url, data=data, timeout=10)
        if diff < 0:
            data = {'chat_id': cfg.chat_id, 'text': 'Кто-то забрал заявление. Текущее место в рейтинге абитуриентов на' + day.lower() + ': ' + str(rate) + ' (+' + str(abs(diff)) + ')'}
            r = requests.post(cfg.url, data=data, timeout=10)
        if diff > 0:
            data = {'chat_id': cfg.chat_id, 'text': 'Погружение. Текущее место в рейтинге абитуриентов на' + day.lower() + ': ' + str(rate) + ' (-' + str(diff) + ')'}
            r = requests.post(cfg.url, data=data, timeout=10)
        previous = rate
        date = day
        Timer(43200, bot).start()  # Waiting 12 hours and starting the bot again if we found changes
    else:
        Timer(6000, bot).start()  # If the date didn't changed wait for 1 hour

try:
    bot()
except: 
    Timer(3000, bot).start()