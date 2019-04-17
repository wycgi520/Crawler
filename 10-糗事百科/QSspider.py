#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    功能:实现糗事百科段子爬取
    作者:国易
"""
from lxml import etree
import threading
import os
import re
import random
from parse_url import parse_url
import json
from queue import Queue

class QSSpider():

    def __init__(self, page_nums):
        self.path = "D:\我的坚果云\努力，奋斗\就业班\爬虫\练习\\10-糗事百科\\duanzi_data"
        self.page_nums = page_nums
        self.proxies_list = list()
        self.url_queue = Queue()
        self.pages_queue = Queue()
        self.content_queue = Queue()

    def generate_url_list(self):
        i = 1
        while i <= self.page_nums:
            url = "https://www.qiushibaike.com/8hr/page/{}/".format(i)
            self.url_queue.put(url)
            i += 1

    def get_list_pages(self):
        while True:
            url = self.url_queue.get()
            html_str = parse_url(url)
            html = etree.HTML(html_str)
            print(url)

            list_pages = html.xpath("//div[contains(@class,'recommend-article')]/ul/li[@id]")
            new_list_pages = list()
            for pages in list_pages:
                item = dict()
                item["url"] = "https://www.qiushibaike.com"+pages.xpath("./a/@href")[0]
                item["title"] = pages.xpath("./div/a/text()")[0]
                item["type"] = (pages.xpath("./@class")[0].split("_"))[1]
                item["laugher_nums"] = pages.xpath("//div[contains(@class,'recmd-num')]/span[1]/text()")[0]
                item["comments"] = pages.xpath("//div[contains(@class,'recmd-num')]/span[4]/text()")[0]
                user_img_url = pages.xpath("//a[contains(@class,'recmd-user')]/img/@src")[0]
                user_img_url = re.match(r"([^\?]+).*", user_img_url).group(1)
                item["user_img_url"] = "https:"+user_img_url
                item["user_name"] = pages.xpath("//a[contains(@class,'recmd-user')]/img/@alt")[0]
                new_list_pages.append(item)
            self.pages_queue.put(new_list_pages)
            self.url_queue.task_done()

    def get_one_page_data(self, page, path):
        duanzi_data = list()
        page_html_str = parse_url(page["url"])
        html = etree.HTML(page_html_str)
        if page["type"] =="video":
            video_data = "https:" + html.xpath("//video/source/@src")[0]
            duanzi_data.append(video_data)
        elif page["type"] =="image":
            img_data = "https:" + html.xpath("//div[contains(@class,'thumb')]/img/@src")[0]
            duanzi_data.append(img_data)
        elif page["type"] =="multi":
            img_data = html.xpath("//div[contains(@class,'thumb')]/img/@src")
            duanzi_data = ["https:"+url_suffix for url_suffix in img_data]
        elif page["type"] =="word":
            word_data = html.xpath("//div[contains(@class,'word')]/div/text()")[0]
            duanzi_data.append(word_data)
        self.content_queue.put((page, duanzi_data, path))


    def save_page_data(self):
        while True:
            page, one_page_data, path = self.content_queue.get()
            valid_title = re.sub(r"""/|\\|:|\*|"|\<|\>|\||\?""", "", page["title"])
            # 保存基本信息
            info_save_path = path + "\\" + "{}_info.txt".format(valid_title)
            with open(info_save_path, 'w', encoding='utf-8') as h:
                json.dump(page, h, ensure_ascii=False, indent=2)

            for i, page_data in enumerate(one_page_data):
                print("----------------next--------------")
                print(page_data)

                data_need_save = None
                if page_data.startswith("http"):
                    while not data_need_save:
                        data_need_save = parse_url(page_data, header_add={'Connection': 'close'})
                else:
                    data_need_save = page_data
                i += 1
                if page["type"] == "video":
                    save_path = path + "\\" + "{}.mp4".format(valid_title)
                elif page["type"] == "image":
                    save_path = path + "\\" + "{}.jpg".format(valid_title)
                elif page["type"] == "multi":
                    if "gif" in page_data:
                        save_path = path + "\\" + "{}-{}.gif".format(valid_title, i)
                    else:
                        save_path = path + "\\" + "{}-{}.jpg".format(valid_title, i)
                elif page["type"] == "word":
                    save_path = path + "\\" + "{}.txt".format(valid_title)
                print(save_path)
                if page["type"] == "word":
                    with open(save_path,'w') as f:
                        f.write(data_need_save)
                else:
                    with open(save_path,'wb') as f:
                        f.write(data_need_save)
                print("----------------done-------------------")
            self.content_queue.task_done()

    def get_data(self):
        while True:
            list_pages = self.pages_queue.get()
            print(list_pages)
            for page in list_pages:
                valid_title = re.sub(r"""/|\\|:|\*|"|\<|\>|\||\?""","",page["title"])

                page_save_path = self.path+"\\"+valid_title
                if not os.path.exists(page_save_path):
                    os.makedirs(page_save_path)

                self.get_one_page_data(page, page_save_path)
            self.pages_queue.task_done()

    def run(self):
        thread_pool = list()
        # 生成url池
        t_url = threading.Thread(target=self.generate_url_list)
        thread_pool.append(t_url)

        # 循环获取糗事百科热门中每页的响应
        t_pages = threading.Thread(target=self.get_list_pages)
        thread_pool.append(t_pages)

        # 2. 获取所有列表页中的数据
        t_data = threading.Thread(target=self.get_data)
        thread_pool.append(t_data)

        # 保存数据
        t_save = threading.Thread(target=self.save_page_data)
        thread_pool.append(t_save)

        for t in thread_pool:
            t.setDaemon(True)  # 把子线程设置为守护线程，该线程不重要,主线程结束，子线程结束
            t.start()

        # 等待所有队列的阻塞解除后, 主线程结束
        for q in [self.url_queue, self.pages_queue, self.content_queue]:
            q.join()


if __name__ == '__main__':
    qiushi = QSSpider(1)
    qiushi.run()
