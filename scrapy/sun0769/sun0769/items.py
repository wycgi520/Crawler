# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Sun0769Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    number = scrapy.Field()
    hanle_state = scrapy.Field()
    update_time = scrapy.Field()
    involved_department = scrapy.Field()
    content = scrapy.Field()
    content_img_url = scrapy.Field()