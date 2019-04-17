#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""实现百度翻译, 并保存到本地"""
import requests
import js2py
import re

class BDT_S(object):

    def __init__(self, words):
        self.words = words
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
        }
        self.session = requests.Session()

    def request_get(self):
        url = "https://fanyi.baidu.com/"
        r = self.session.get(url, headers=self.headers)
        content = r.content.decode()

        ret_token = re.search(r"token:[^']*'([^']*)'", content)
        token = ret_token.group(1)

        ret_gtk = re.search(r"gtk[^']*('[^']*')", content)
        gtk = ret_gtk.group(1)

        with open('D:\我的坚果云\努力，奋斗\就业班\爬虫\\3-百度翻译\\fanyi.js', 'r') as f:
            JS_file_content = f.read()

        JS_file_content = re.sub(r"window\[l\]", gtk, JS_file_content)

        run_js = js2py.EvalJs({})
        run_js.execute(JS_file_content)
        sign = run_js.e(self.words)

        return token, sign

    def data_make(self, isdetect, **kwargs):
        from_data = {
            "query": self.words
        }
        if not isdetect:
            token, sign = self.request_get()
            from_data["token"] = token
            from_data["sign"] = sign
            from_data["transtype"] = "realtime"
            from_data["simple_means_flag"] = "3"
            from_data.update(kwargs)

        return from_data

    @staticmethod
    def choose_url(isdetect):
        if isdetect:
            return "https://fanyi.baidu.com/langdetect"
        else:
            return "https://fanyi.baidu.com/v2transapi"

    def request_post(self, isdetect, **kwargs):

        from_data = self.data_make(isdetect, **kwargs)
        url = self.choose_url(isdetect)

        # print(from_data)
        # print(url)

        content_dict = self.session.post(url, data=from_data, headers=self.headers).json()
        return content_dict

    def lang_detect(self):
        detect_result = self.request_post(True)
        return detect_result['lan']

    def run(self):
        # 1. 获取检测结果是英文还是中文
        lang_c = self.lang_detect()
        if lang_c == 'en':
            trans_dire = {"from":"en", "to":"zh"}
        elif lang_c == 'zh':
            trans_dire = {"from":"zh", "to":"en"}
        # 2. 根据结果发送请求, 并获取到响应
        content = self.request_post(False, **trans_dire)
        print(content['trans_result']['data'][0]['dst'])

if __name__ == "__main__":
    bd_tran = BDT_S("我用python")
    bd_tran.run()
