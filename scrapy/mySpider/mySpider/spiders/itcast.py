# -*- coding: utf-8 -*-
import scrapy
import logging


class ItcastSpider(scrapy.Spider):
    name = 'itcast'  # 爬虫名
    allowed_domains = ['itcast.cn']  # 允许爬取的范围
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']  # 最开始请求的url地址

    def parse(self, response):
        # 处理start_urls对应的响应
        # ret1 = response.xpath("//div[contains(@class,'tea_con')]//h3/text()").extract()  # extract方法提取所有文字
        # print("*" * 30)
        # print(ret1)
        # print("*" * 30)

        logger = logging.getLogger(__name__)

        li_list = response.xpath("//div[@class='tea_con']//li")
        for li in li_list:
            item = dict()
            item["name"] = li.xpath(".//h3/text()").extract_first()  # 可以直接取xpath列表中第一个
            item["title"] = li.xpath(".//h4/text()").extract_first()
            logger.warning(item)
            yield item
