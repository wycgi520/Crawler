#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""实现代理"""

import requests

proxies = {
    "http":"http://163.177.151.23:80",
}

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

r = requests.get("http://www.baidu.com", proxies=proxies, headers=headers)

print(r.status_code)