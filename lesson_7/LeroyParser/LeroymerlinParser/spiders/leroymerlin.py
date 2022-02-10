import scrapy
from scrapy.http import HtmlResponse
from LeroymerlinParser.items import LeroymerlinparserItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, product, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/search/?q={product}']


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@aria-label,'Следующая страница')]/@href").get()
        if next_page:
             yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//div[@data-qa-product]/a/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.product_parse)

    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', "//meta[@itemprop ='price']/@content")
        loader.add_xpath('photo', "//picture[@slot='pictures']/img/@src")
        loader.add_value('url', response.url)
        loader.add_xpath('_id', "//span[@slot='article']/@content")
        yield loader.load_item()
