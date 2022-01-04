import requests
from lxml import html
from pprint import pprint
from pymongo import MongoClient
import pymongo

client = MongoClient('localhost',27017)
db = client['mail_ru_news']
top_news = db['top_news']

url = 'https://news.mail.ru/?_ga=2.191373994.1828598494.1640602506-574730024.1629403775'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

def insert_news(news):
 try:
     top_news.insert_one(news)
 except pymongo.errors.DuplicateKeyError:
     pass

response = requests.get(url, headers)
dom = html.fromstring(response.text)

# формируем список всех новостей с картинками(5штук) + те что визуально видны
link_news = (dom.xpath("//a[contains(@class,'topnews__item')]/@href") + dom.xpath("//li[@class = 'list__item']/a/@href"))
if response.ok:
    for link in link_news:
        response_news = requests.get(link, headers)
        dom_news = html.fromstring(response_news.text)
        if response_news.ok:
            name = dom_news.xpath("//h1/text()")
            date = dom_news.xpath("//span/@datetime")
            source =dom_news.xpath("//span[@class = 'note']//span[@class = 'link__text']/text()")
            news = {}
            news['name'] = name[0]
            news['date'] = date[0]
            news['link'] = link
            news['source'] = source[0]
            insert_news(news)

for n in top_news.find():
    print(n)

