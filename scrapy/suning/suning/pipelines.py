# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from suning.items import SuningItem


class SuningPipeline(object):

    def open_spider(self, spider):
        client = MongoClient(host="192.168.43.174", port=27017)
        self.suning_book_collection = client["Suning"]["book"]

    def process_item(self, item, spider):
        if spider.name == "book":
            if isinstance(item, SuningItem):
                self.suning_book_collection.update({"book_name": item["book_name"]},{"$set":dict(item)}, True)

        return item
