# -*- coding: utf-8 -*-
import scrapy
from sun0769.items import Sun0769Item


class WzSpider(scrapy.Spider):
    name = 'wz'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/'
                  'question/questionType?type=4&page=0']

    def parse(self, response):
        print(response.body)
        tr_list = response.xpath("//td[@align='center']//tr")
        for tr in tr_list:
            item = Sun0769Item()
            item["title"] = tr.xpath(".//a[2]/@title").extract_first()
            item["href"] = tr.xpath(".//a[2]/@href").extract_first()
            item["number"] = tr.xpath("./td[1]/text()").extract_first()
            item["hanle_state"] = tr.xpath("./td[3]/span/text()").extract_first()
            item["update_time"] = tr.xpath("./td[5]/text()").extract_first()
            item["involved_department"] = tr.xpath(".//a[3]/text()").extract_first()

            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item": item}
            )
        # 翻页
        next_url = response.xpath("//a[text()='>']/@href").extract_first()
        if next_url:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )


    def parse_detail(self, response):
        item = response.meta["item"]
        item["content"] = response.xpath("//div[@class='wzy1']/table[2]/tr[1]//text()").extract()
        item["content_img_url"] = response.xpath("//img/@src").extract()
        item["content_img_url"] = ["http://wz.sun0769.com"+suffix for suffix in item["content_img_url"]]
        yield item
