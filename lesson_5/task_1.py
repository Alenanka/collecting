from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import time
import re

from pymongo import MongoClient
import pymongo
client = MongoClient('localhost',27017)
db = client['mvideo']
products = db['products']

def insert_product(product):
 try:
     products.insert_one(product)
 except pymongo.errors.DuplicateKeyError:
     pass

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')
time.sleep(5)

pages = 0
while pages < 10:
    try:
        wait = WebDriverWait(driver, 5)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), ' В тренде')]")))
        button.click()
        break
    except exceptions.TimeoutException as e:
        actions = ActionChains(driver).send_keys(Keys.PAGE_DOWN)
        actions.perform()
        pages += 1

titles = driver.find_elements(By.XPATH,"//mvid-shelf-group//div[@class = 'title']//div")
prices_new = driver.find_elements(By.XPATH,"//mvid-shelf-group//span[@class='price__main-value']")
link = driver.find_elements(By.XPATH,"//mvid-shelf-group//a[@class='img-with-badge ng-star-inserted']")
rating =driver.find_elements(By.XPATH,"//mvid-shelf-group//mvid-star-rating//span[@class='value ng-star-inserted' or @class='stars-container empty-reviews ng-star-inserted']")

for i in range(len(titles)):
    product = {}
    product['name'] = titles[i].text
    product['price'] = int(prices_new[i].text.replace(' ', ''))
    product['link'] = link[i].get_attribute('href')
    product['_id'] = re.search(r'\d+$',link[i].get_attribute('href')).group()
    product['rating'] = rating[i].text
    insert_product(product)

for prod in products.find():
    print(prod)

driver.close()
client.close()