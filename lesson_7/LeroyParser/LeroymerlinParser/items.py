# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose

def convert_price(value):
    try:
        value = int(float(value))
    except:
        pass
    finally:
        return value

class LeroymerlinparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_price), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    photo = scrapy.Field()
    _id = scrapy.Field(output_processor=TakeFirst())

