# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from tencent.logger import logger
from pymongo import MongoClient
from tencent.items import TencentItem


client = MongoClient(host="192.168.43.174", port=27017)
collection = client["tencent"]["hr"]

class TencentPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "hr":
            if isinstance(item,TencentItem):
                print(item)
                collection.insert_one(dict(item))
        return item
