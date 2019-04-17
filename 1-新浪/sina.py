#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""实现任意贴吧的爬虫, 并保存到本地"""


import requests

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

response = requests.get("https://www.sina.com.cn/", headers=headers, params=kw)

# encoding能够避免编码错误, 因为windows的txt默认是gbk格式
with open('D:\我的坚果云\努力，奋斗\就业班\爬虫\爬取作业1-新浪\sina01.txt', 'w', encoding='utf-8') as f:
    f.write(response.text)

with open('D:\我的坚果云\努力，奋斗\就业班\爬虫\爬取作业1-新浪\sina02.txt', 'w', encoding='utf-8') as f:
    f.write(response.content.decode())
