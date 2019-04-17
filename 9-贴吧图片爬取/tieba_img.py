#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    功能:实现豆瓣图片的爬取
    作者:国易
"""
from lxml import etree
import requests
import os
import re
import random
from parse_url import parse_url

class TBSpider():

    def __init__(self, tieba_name):
        self.path = "D:\我的坚果云\努力，奋斗\就业班\爬虫\练习\9-贴吧图片爬取\img_data"
        self.proxies_list = list()
        self.tieba_name = tieba_name

    def get_list_pages(self, url):
        html_str = parse_url(url)
        html = etree.HTML(html_str)

        list_pages = html.xpath("//a[contains(@class,'j_th_tit')]")
        new_list_pages = list()
        for pages in list_pages:
            item = dict()
            item["url"] = "https://tieba.baidu.com"+pages.xpath("@href")[0]
            item["title"] = pages.xpath("@title")[0]
            new_list_pages.append(item)

        next_url_suffix_list = html.xpath("//a[contains(@class,'next pagination-item')]/@href")
        if not next_url_suffix_list:
            next_url = "https:" + next_url_suffix_list[0]
        else:
            next_url = None
        return new_list_pages, next_url

    def get_one_page_img_data(self, page_url):
        page_html_str = parse_url(page_url)
        html = etree.HTML(page_html_str)

        list_img_url_suffix = html.xpath("//img[contains(@class,'BDE_Image')]/@src")
        new_list_img_url = list()
        for img_url in list_img_url_suffix:
            suffix = re.match(r"https://imgsa.baidu.com/.*/(\w+\.jpg)", img_url)
            if suffix:
                new_img_url = "http://imgsrc.baidu.com/forum/pic/item/" + suffix.group(1)
                new_list_img_url.append(new_img_url)

        next_page_url_suffix = html.xpath("//a[text()='下一页']/@href")
        if next_page_url_suffix:
            next_page_url = "https://tieba.baidu.com" + next_page_url_suffix[0]
        else:
            next_page_url = None

        return new_list_img_url, next_page_url

    def get_proxies(self):
        html_str = parse_url("https://proxy.horocn.com/api/proxies?"
                             "order_id=0DOI1629498172860524&num=10&format=text&line_separator=win").decode()
        check_str = re.search("请求频率过快", html_str)
        if not check_str:
            self.proxies_list = html_str.splitlines()
        return self.proxies_list

    def save_one_page_img_data(self, page_num, one_page_img_data, path):

        for i, img_url in enumerate(one_page_img_data):
            print("----------------next--------------")
            # 获取代理
            proxies_list = self.get_proxies()
            proxies_len = len(proxies_list)
            # 选取一个代理IP下载数据
            num = random.randint(0, proxies_len - 1)
            proxies = {
                "http":"http://"+proxies_list[num],
                "https":"http://"+proxies_list[num]
            }
            img_data = parse_url(img_url, proxies=proxies, header_add={'Connection': 'close'})
            if not img_data: continue
            i += 1
            save_path = path+"\\"+f"{page_num}-{i}.jpg"
            print(save_path)
            with open(save_path,'wb') as f:
                f.write(img_data)
            print("----------------done-------------------")

    def get_img_data_and_save(self, page):
        next_page_url = page["url"]
        valid_title = re.sub(r"""/|\\|:|\*|"|\<|\>|\||\?""","",page["title"])

        page_save_path = self.path+"\\"+valid_title
        if not os.path.exists(page_save_path):
            os.makedirs(page_save_path)
        page_num = 1
        while next_page_url:
            one_page_img_data, next_page_url = self.get_one_page_img_data(next_page_url)
            self.save_one_page_img_data(page_num, one_page_img_data, page_save_path)
            page_num += 1

    def run(self):
        start_url = f"https://tieba.baidu.com/f?kw={self.tieba_name}"
        next_url = start_url
        # 循环获取贴吧中每页的响应
        while next_url:
            # 1. 获取列表页数据
            list_pages, next_url = self.get_list_pages(start_url)

            # 2. 获取所有列表页中的图片数据并保存
            for page in list_pages:
                self.get_img_data_and_save(page)


if __name__ == '__main__':
    tieba = TBSpider("李毅")
    tieba.run()