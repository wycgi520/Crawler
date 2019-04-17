#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""实现图片保存"""

import requests

r = requests.get("http://docs.python-requests.org/zh_CN/latest/_static/requests-sidebar.png")

with open("D:\我的坚果云\努力，奋斗\就业班\爬虫\练习\\0-保存图片\\1.png","wb") as f:
    f.write(r.content)