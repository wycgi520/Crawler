# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    def parse(self, response):
        tr_list = response.xpath("//table[@class='tablelist']/tr")
        for tr in tr_list[1:-1]:
            item = TencentItem()
            item["title"] = tr.xpath(".//a/text()").extract_first()
            item["type"] = tr.xpath("./td[2]/text()").extract_first()
            item["num"] = tr.xpath("./td[3]/text()").extract_first()
            item["location"] = tr.xpath("./td[4]/text()").extract_first()
            item["datetime"] = tr.xpath("./td[5]/text()").extract_first()
            yield item

        next_url = response.xpath("//a[@id='next']/@href").extract_first()
        next_url = "https://hr.tencent.com/" + next_url
        if next_url:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )