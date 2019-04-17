# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    channel_name = scrapy.Field()
    channel_name_url = scrapy.Field()
    submenu_name = scrapy.Field()
    submenu_url = scrapy.Field()
    book_type_name = scrapy.Field()
    book_type_url = scrapy.Field()
    book_name = scrapy.Field()
    book_url = scrapy.Field()
    book_price = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    publisher_time = scrapy.Field()