import pymongo
from bs4 import BeautifulSoup as bs
import requests
from pymongo import MongoClient
import re
client = MongoClient('localhost',27017)
db = client['parser_position']
vacancy = db['vacancy']
main_url = 'https://hh.ru/search/vacancy'
search_position = input('Введите должность:')
while 1:
        try:
            count_page = int(input('Введите количество страниц для выборки: '))
            break
        except ValueError:
            print('Ожидаем целое число')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}

params = {'text': search_position,
          'page': 0}

list_of_position =[]

def insert_vacancy(vak):
 try:
     vacancy.insert_one(vak)
 except pymongo.errors.DuplicateKeyError:
     pass


def search_vacancy(sal):
    for vak in vacancy.find({"$or": [{'salary_min': {"$gt": sal}}, {'salary_max': {"$gt": sal}}]}):
        print(vak)

while params['page'] < count_page:
    responce = requests.get(main_url, params=params, headers=headers)
    dom = bs(responce.text, 'html.parser')
    positions = dom.find_all('div', {'class': "vacancy-serp-item"})

    if responce.ok and positions:
        for position in positions:
            pos_vok = {}
            link = position.find('a',{'data-qa':"vacancy-serp__vacancy-title"}).get('href')
            id = re.search(r'\d+',link).group()
            name = position.find('a',{'data-qa':"vacancy-serp__vacancy-title"}).text
            try:
                salary = position.find('span',{'data-qa':"vacancy-serp__vacancy-compensation"}).text.split(' ')
                if len(salary) == 4:
                    salary_min = int(salary[0].replace('\u202f', ''))
                    salary_max = int(salary[2].replace('\u202f', ''))
                    salary_currency = salary[3].replace('\xa0', '')
                elif salary[0] == 'от':
                    salary_min = int(salary[1].replace('\u202f', ''))
                    salary_max = None
                    salary_currency = salary[2].replace('\xa0', '')
                elif salary[0] == 'до':
                    salary_min = None
                    salary_max = int(salary[1].replace('\u202f', ''))
                    salary_currency = salary[2].replace('\xa0', '')
            except:
                salary_min = None
                salary_max = None
                salary_currency = None

            pos_vok['_id'] = id
            pos_vok['name'] = name
            pos_vok['link'] = link
            pos_vok['salary_min'] = salary_min
            pos_vok['salary_max'] = salary_max
            pos_vok['salary_currency'] = salary_currency
            insert_vacancy(pos_vok)
            list_of_position.append(pos_vok)
    params['page'] += 1

for doc in vacancy.find():
    print(doc)

salary = int(input('ВВедите от какой зарплаты вывести вакансии:'))
search_vacancy(salary)
