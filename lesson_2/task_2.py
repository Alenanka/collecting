from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_url = 'https://hh.ru/search/vacancy'
search_position = input('Введите должность:')
while 1:
        try:
            page = int(input('Введите количество страниц для выборки: '))
            break
        except ValueError:
            print('Ожидаем целое число')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
list_of_position =[]

def parse_page(p):
    params = {'text': search_position, 'сount': p}
    responce = requests.get(main_url, params=params, headers=headers)
    if responce.ok:
        dom = bs(responce.text,'html.parser')
        positions = dom.find_all('div',{'class':"vacancy-serp-item"})
        for position in positions:
            link = position.find('a',{'data-qa':"vacancy-serp__vacancy-title"}).get('href')
            name = position.find('a',{'data-qa':"vacancy-serp__vacancy-title"}).text
            salary_dict = {}
            try:
                salary = position.find('span',{'data-qa':"vacancy-serp__vacancy-compensation"}).text.split(' ')
                if len(salary) == 4:
                    salary_dict = dict((('min',salary[0].replace('\u202f','')),('max',salary[2].replace('\u202f','')),(('valute'),salary[3].replace('\xa0',''))))
                elif len(salary) == 3 and salary[0] =='от':
                    salary_dict = dict((('min', salary[1].replace('\u202f','')), (('valute'), salary[2].replace('\xa0',''))))
                elif len(salary) == 3 and salary[0] == 'до':
                    salary_dict = dict((('max', salary[1].replace('\u202f', '')), (('valute'), salary[2].replace('\xa0', ''))))
            except:
                salary_dict ={'min', 'зп не задана'}
            list_of_position.append((link,name,salary_dict))

for i in range(page):
    parse_page(i)
pprint(list_of_position)