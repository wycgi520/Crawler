#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""实现任意贴吧的爬虫, 并保存到本地"""
# 用面向对象的方法实现, 对象的run方法中构建流程: 1. 建立url_list, 2.遍历url_list发送请求, 3.保存文件内容
import requests

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

tieba_name = input("请输入要爬的贴吧名: ")

kw = {'kw':tieba_name}

i = 1
while i <= 100:
    response = requests.get("https://tieba.baidu.com/f", params=kw)
    content = response.content.decode()
    page_nums = 50 * i
    kw['pn'] = str(page_nums)
    file_name = 'D:\我的坚果云\努力，奋斗\就业班\爬虫\\2-贴吧\{}-0{}.txt'.format(tieba_name, i)
    # print(file_name)
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(content)
    i += 1