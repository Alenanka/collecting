from scrapy.utils.python import to_bytes
import re
import scrapy
import hashlib
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LeroymerlinparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.lerya

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
       if item['photo']:
           for img in item['photo']:
               try:
                   yield scrapy.Request(img)
               except Exception as e:
                   print(e)
    def item_completed(self, results, item, info):
        item['photo'] = [res[1] for res in results if res[0]]
        return item
    def file_path(self, request, response=None, info=None, *, item):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        path = item['_id'] + re.sub(r'[\"\';,/\\]', '', item['name'])
        return f"{path}/{image_guid }.jpg"
