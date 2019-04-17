#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    功能:实现段子爬取
    作者:国易
"""
from parse_url import parse_url
# from pprint import pprint
import re
import json



class DuanZiSpider(object):
    def __init__(self):
        pass

    @staticmethod
    def get_content_list(html_str):
        p = re.compile(r"""<a href="\/detail-.+?\.html">(.*?)<\/a>""")
        return p.findall(html_str)

    def run(self):
        html_str = parse_url("http://www.budejie.com/text/")
        content_list = self.get_content_list(html_str)
        with open(r"D:\我的坚果云\努力，奋斗\就业班\爬虫\练习\7-获取段子内容(正则表达式)\duanzi.data","w",encoding="utf-8") as f:
            # 格式化输出到文件中, 增强可读性
            json.dump(content_list, f, ensure_ascii=False, indent=2)
            # for content in content_list:
            #     f.write(content)
            #     f.write('\n\n')

if __name__ == '__main__':
    duanzi = DuanZiSpider()
    duanzi.run()