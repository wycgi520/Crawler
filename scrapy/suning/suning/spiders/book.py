# -*- coding: utf-8 -*-
import re
import scrapy
import js2xml
import json
from suning.items import SuningItem


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        channel_list = response.xpath("//div[@class='menu-list']//h3/a")
        for i, channel in enumerate(channel_list):
            item = SuningItem()
            # 获取频道目录
            item["channel_name"] = channel.xpath("./text()").extract_first()
            item["channel_name_url"] = channel.xpath("./@href").extract_first()
            channel_sub_menu = response.xpath("//div[@class='menu-sub']")[i]

            # 获取子菜单
            submenu_list = channel_sub_menu.xpath(".//p[@class='submenu-item']")
            # 如果没有em, 则是正常的子菜单
            submenu_list = [i for i in submenu_list if not i.xpath(".//em")]
            if submenu_list:
                for j, submenu in enumerate(submenu_list):
                    item["submenu_name"] = submenu.xpath("./a/text()").extract_first()
                    item["submenu_url"] = submenu.xpath("./a/@href").extract_first()
                    sub_menu_book_type = channel_sub_menu.xpath(".//ul[contains(@class,'book-name-list')]")[j]

                    # 获取书本分类
                    book_type_list = sub_menu_book_type.xpath(".//a")
                    for book_type in book_type_list:
                        item["book_type_name"] = book_type.xpath("./text()").extract_first()
                        item["book_type_url"] = book_type.xpath("./@href").extract_first()
                        book_type_num = re.search(r"/\d-(\d+)-\d", item["book_type_url"])
                        # 避免网页格式不同
                        if book_type_num:
                            book_type_num = book_type_num.group(1)
                            start_data_url =  self.settings["BOOK_DATA_URL_LIST_1"].\
                                format(book_type_num, 0)

                        else:
                            start_data_url = self.settings["BOOK_DATA_URL_LIST_2"]. \
                                format(item["book_type_name"], 0)
                        yield scrapy.Request(
                            start_data_url,
                            callback=self.parse_book_name,
                            meta = {"item": {**item}, "pagenum":0}
                        )

            else:
                item["submenu_name"] = None
                item["submenu_url"] = None
                sub_menu_book_type = channel_sub_menu.xpath(".//ul[contains(@class,'book-name-list')]")

                # 获取书本分类
                book_type_list = sub_menu_book_type.xpath(".//a")
                for book_type in book_type_list:
                    item["book_type_name"] = book_type.xpath("./text()").extract_first()
                    item["book_type_url"] = book_type.xpath("./@href").extract_first()
                    book_type_num = re.search(r"/\d-(\d+)-\d", item["book_type_url"])
                    # 避免网页格式不同
                    if book_type_num:
                        book_type_num = book_type_num.group(1)
                        start_data_url = self.settings["BOOK_DATA_URL_LIST_1"]. \
                            format(book_type_num, 0)

                    else:
                        start_data_url = self.settings["BOOK_DATA_URL_LIST_2"]. \
                            format(item["book_type_name"], 0)
                    yield scrapy.Request(
                        start_data_url,
                        callback=self.parse_book_name,
                        meta = {"item": {**item}, "pagenum":0}
                    )

    def parse_book_name(self, response):
        item = response.meta["item"]
        # 判断是否为多页
        has_pages = response.xpath("//div[@class='search-page']/a")
        book_name_list = response.xpath("//div[@class='res-info']/p[2]/a")
        for i, book_name in enumerate(book_name_list):
            item["book_name"] = book_name.xpath("./@title").extract_first()
            item["book_name"] = item["book_name"].replace("\n","")
            item["book_url"] = book_name.xpath("./@href").extract_first()
            item["book_url"] = "https:" + item["book_url"]
            yield scrapy.Request(
                item["book_url"],
                self.parse_book_price,
                meta={"item": {**item}}
            )

        if has_pages:
            total_page_str = response.xpath("//div[@class='search-page']/a[last()-2]/text()").extract_first()
            total_page = int(total_page_str)
            cp = response.meta["pagenum"] + 1
            if cp < total_page:
                book_type_num = re.search(r"/\d-(\d+)-\d", item["book_type_url"])
                if book_type_num:
                    book_type_num = book_type_num.group(1)
                    data_url = self.settings["BOOK_DATA_URL_LIST_1"]. \
                        format(book_type_num, cp)
                else:
                    data_url = self.settings["BOOK_DATA_URL_LIST_2"]. \
                        format(item["book_type_name"], cp)
                yield scrapy.Request(
                    data_url,
                    callback = self.parse_book_name,
                    meta={"item": {**response.meta["item"]}, "pagenum":cp}
                )

    def parse_book_price(self, response):
        item = response.meta["item"]

        # 获取作者,出版社,出版时间
        others = response.xpath("//li[@class='pb-item']//text()").extract()
        others_len = len(others)
        others_name_list = ["author","publisher","publisher_time"]
        for n in range(0, others_len,2):
            if others[n].find("作者") != -1:
                item["author"] = re.sub(r"\s","", others[n+1])
                others_name_list.remove("author")
            elif others[n].find("出版社") != -1:
                item["publisher"] = re.sub(r"\s", "", others[n+1])
                others_name_list.remove("publisher")
            elif others[n].find("出版时间") != -1:
                item["publisher_time"] = others[n+1]
                others_name_list.remove("publisher_time")
        for name in others_name_list:
            item[name] = None

        # 获取价格
        script_str = response.xpath("//script/text()").extract()[0]
        price_data_url = self.genpriceurl(script_str)
        if price_data_url is not None:
            yield scrapy.Request(
                price_data_url,
                callback=self.parse_price,
                meta={"item": {**item}}
            )
        else:

            item["book_price"] = None
            print(item)
            yield item

    def parse_price(self,response):
        item = response.meta["item"]
        data_dict_str = response.body.decode()
        data_dict_str = re.search(r"pcData\((.*)\)", data_dict_str, re.S)
        data_dict_str = data_dict_str.group(1)
        data_dict = json.loads(data_dict_str)
        item["book_price"] = data_dict["data"]["price"]\
            ["saleInfo"][0]["netPrice"]
        print(item)
        yield item

    def genpriceurl(self, script_str):
        script_html = js2xml.parse(script_str)
        temps = dict()
        for unit in self.settings["PRICE_URL_DATA_LIST"]:
            xpath_route = "//var[@name='sn']//property[@name='{}']/string/text()".format(unit)
            temps[unit] = script_html.xpath(xpath_route)
            if temps[unit]:
                temps[unit] = temps[unit][0]
            else:
                return None
        b = "" if temps["mountType"] != "03" else temps["mountType"]
        price_data_url = self.settings["BOOK_PRICE_URL"]. \
            format(temps["luaUrl"], temps["passPartNumber"], temps["partNumber"], temps["vendorCode"], temps["category1"], temps["cmmdtyType"], b, temps["catenIds"], temps["weight"])
        return price_data_url