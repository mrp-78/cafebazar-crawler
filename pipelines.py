# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime
from scrapy.exporters import JsonItemExporter


class CafebazaarPipeline:
    def process_item(self, item, spider):
        return item



class JsonPipeline:
    def __init__(self):
        dt_string = datetime.now().strftime("_%Y-%m-%d_%H-%M-%S")
        self.file = open("games" + dt_string + ".json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


import pymongo
from itemadapter import ItemAdapter
from datetime import datetime

class MongoPipeline:

    collection_name = 'games'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        print('connected to mongodb')

    def close_spider(self, spider):
        print('crawl finished')
        print('-'*20)
        self.client.close()

    def process_item(self, item, spider):
        if self.db[self.collection_name].find_one({'packageName': item['packageName']}) == None:
        	item['created_at'] = datetime.now()
        	self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        else:
        	item['updated_at'] = datetime.now()
        	self.db[self.collection_name].update_one({'packageName': item['packageName']}, {"$set": ItemAdapter(item).asdict()})
        return item