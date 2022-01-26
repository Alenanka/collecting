
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=3',
                  'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=2',
                  'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=14&geo%5Br%5D%5B0%5D=4',
                  'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Br%5D%5B0%5D=5&geo%5Br%5D%5B1%5D=6&geo%5Br%5D%5B2%5D=8',
                'https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=426&geo%5Br%5D%5B0%5D=7&geo%5Br%5D%5B1%5D=27']

    def parse(self, response: HtmlResponse ):
        next_page = response.xpath("//a[contains(@class, 'button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class, 'icMQ_ _6AfZ9')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = ' '.join(response.xpath("//h1//text()").getall())
        salary = None
        url = response.url
        salary = response.xpath("//span[@class ='_2Wp8I _3a-0Y _3DjcL _3fXVo']/text()").getall()
        # url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
