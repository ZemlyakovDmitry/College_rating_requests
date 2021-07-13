# -*- coding: utf-8 -*-
from threading import Timer

import config as cfg
import requests
from lxml import html

previous = 11  # Place your current place in the rating
date = 'На 1 июля 2021 года'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36'}

def bot():
    global previous  # idk how to write code and don't use globals
    global date
    page = requests.get(cfg.url_rating, headers=headers, timeout=10)  # 
    tree = html.fromstring(page.content)
    current_date = str(tree.xpath("//h1[contains(text(), 'года')]/text()"))[2:-2]  # get current date 
    if current_date != date:
        rating = tree.xpath(
            "//td[contains(text(),'SURNAME')]/preceding-sibling::td[1]/text()")  # Place your surname instead of the 'SURNAME'
        rate = int(str(rating)[2:-2])
        diff = rate - previous
        def post():
            requests.post(cfg.url, data=data, timeout=10)

        if diff == 0:
            data = {'chat_id': cfg.chat_id,
                    'text': 'С прошедшего дня ничего не изменилось. Текущее место в рейтинге абитуриентов ' + current_date.lower() + ': ' + str(
                        rate)}
            post()
        if diff < 0:
            data = {'chat_id': cfg.chat_id,
                    'text': 'Кто-то забрал заявление. Текущее место в рейтинге абитуриентов на' + current_date.lower() + ': ' + str(
                        rate) + ' (+' + str(abs(diff)) + ')'}
            post()
        if diff > 0:
            data = {'chat_id': cfg.chat_id,
                    'text': 'Погружение. Текущее место в рейтинге абитуриентов на' + current_date.lower() + ': ' + str(
                        rate) + ' (-' + str(diff) + ')'}
            post()
        previous = rate
        date = current_date
        Timer(43200, bot).start()  # Waiting 12 hours and starting the bot again if we found changes
    else:
        Timer(6000, bot).start()  # If the date didn't changed wait for 1 hour

try:
    bot()
except:
     Timer(3000, bot).start()
