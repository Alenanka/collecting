from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacncies2712

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['min'], item['max'], item['cur'] = self.process_salary_hh(item['salary'])
        if spider.name == 'superjobru':
            item['min'], item['max'], item['cur'] = self.process_salary_superjobru(item['salary'])
        # del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary_hh(self, salary):
        for i in range(len(salary)):
            salary[i] = salary[i].replace('\xa0', '').replace(' ', '').replace('.', '')
        if salary[0] == 'от' and salary[2] == 'до':
            salary_min = int(salary[1])
            salary_max = int(salary[3])
            salary_currency = salary[5]
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
            salary_currency = salary[3]
        elif salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
            salary_currency = salary[3]
        else:
            salary_min = None
            salary_max = None
            salary_currency = None
        return salary_min, salary_max, salary_currency

    def process_salary_superjobru(self, salary):
        for i in range(len(salary)):
            salary[i] = salary[i].replace('\xa0', '')
        if len(salary) == 1:
            salary_min = None
            salary_max = None
            salary_currency = None
        elif len(salary) == 4:
            salary_min = int(salary[0])
            salary_max = int(salary[1])
            salary_currency = re.search('[A-Za-zА-Яа-я]+', salary[3]).group(0)
        elif salary[0] == 'от':
            salary_min = int(re.search('[\d\s]+', salary[2]).group(0))
            salary_max = None
            salary_currency = re.search('[A-Za-zА-Яа-я]+', salary[2]).group(0)
        elif salary[0] == 'до':
            salary_min = None
            salary_max = int(re.search('[\d\s]+', salary[2]).group(0))
            salary_currency = re.search('[A-Za-zА-Яа-я]+', salary[2]).group(0)
        else:
            salary_min = 0
            salary_max = int(salary[1])
            salary_currency = re.search('[A-Za-zА-Яа-я]+', salary[2]).group(0)
        return salary_min, salary_max, salary_currency