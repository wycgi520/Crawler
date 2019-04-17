#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    功能:爬取斗鱼房间信息
    作者:国易
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time


class DouYuSpider():

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        self.drive = webdriver.Chrome(options=chrome_options)
        self.start_url = "https://www.douyu.com/directory/all"


    def get_room_info(self, drive):

        li_list = drive.find_elements_by_xpath("//div[contains(@class,'ListContent')]/ul/li")

        content_list = list()
        for li in li_list:
            item = dict()
            item["title"] = li.find_element_by_xpath(".//h3").text
            item["type"] = li.find_element_by_xpath(".//span[@class='DyListCover-zone']").text
            item["anchor"] = li.find_element_by_xpath(".//h2").text
            item["popularity"] = li.find_element_by_xpath(".//span[@class='DyListCover-hot']").text
            content_list.append(item)

        return content_list

    def save_rome_info(self, rome_info, i):
        file_path = r"D:\我的坚果云\努力，奋斗\就业班\爬虫\练习\14-抓取斗鱼房间信息\page-{}.data".format(i)
        with open(file_path, 'w', encoding="utf-8") as f:
            json.dump(rome_info, f, ensure_ascii=False, indent=2)

    def run(self):
        i = 0
        # 打开首页
        self.drive.get(self.start_url)

        while True:
            time.sleep(5)
            # 提取数据
            rome_info = self.get_room_info(self.drive)

            # 保存首页数据
            self.save_rome_info(rome_info, i)

            # 点击下一页
            next_ele = self.drive.find_elements_by_class_name("dy-Pagination-next")
            if next_ele:
                next_ele[0].click()
                print(f"-------page{i}-------")
            else:
                break

            i += 1

        # 关闭页面
        self.drive.quit()

if __name__ == '__main__':
    douyu = DouYuSpider()
    douyu.run()