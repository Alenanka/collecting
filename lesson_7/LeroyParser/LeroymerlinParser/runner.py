from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from LeroymerlinParser import settings
from LeroymerlinParser.spiders.leroymerlin import LeroymerlinSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    prod = input('Что будем искать? ')
    process.crawl(LeroymerlinSpider, prod)
    process.start()
