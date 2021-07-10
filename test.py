# -*- coding: utf-8 -*-
from threading import Timer
from lxml import html
import requests
import config as cfg

previous = 11
headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 OPR/40.0.2308.81',
}

def bot():
    global previous
    page = requests.get(cfg.url_rating, headers=headers)
    tree = html.fromstring(page.content)
    rating = tree.xpath("//td[contains(text(),'Земляков')]/preceding-sibling::td[1]/text()")
    rate = int(str(rating)[2:-2])
    diff = rate - previous
    if diff == 0:
        data = {'chat_id': cfg.chat_id, 'text': 'С прошедшего дня ничего не изменилось. Текущее место в рейтинге абитуриентов: ' + str(rate)}
        r = requests.post(cfg.url, data=data)
    if diff < 0:
        data = {'chat_id': cfg.chat_id, 'text': 'Кто-то забрал заявление. Текущее место в рейтинге абитуриентов: ' + str(rate) + ' (+' + str(abs(diff)) + ')'}
        r = requests.post(cfg.url, data=data)
    if diff > 0:
        data = {'chat_id': cfg.chat_id, 'text': 'Погружение. Текущее место в рейтинге абитуриентов: ' + str(rate) + ' (-' + str(diff) + ')'}
        r = requests.post(cfg.url, data=data)
    previous = rate
    Timer(43200, bot).start()  # Waiting 12 hours
    
try:
    bot()
except:
    Timer(3000, bot).start()