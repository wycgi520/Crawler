#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    功能:selenium入门
    作者:国易
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 实例化浏览器
# driver = webdriver.Chrome()
# driver = webdriver.PhantomJS(executable_path=r"C:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe")
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

# 设置窗口大小,获取到的截图也会变大
# driver.set_window_size(1920,1080)

# 最大化窗口,但还是原来的800*600
# driver.maximize_window()

driver.get("http://www.baidu.com")
print (driver.get_window_size())

# 网页截图保存
# driver.save_screenshot("./baidu.png")

# 元素定位
driver.find_element_by_id("kw").send_keys("python")
driver.find_element_by_id("su").click()

# 获取requests能用的cookie, 把列表型cookie转换为字典
# cookies = driver.get_cookies()
# cookies = {i["name"]:i["value"] for i in cookies}
# print(cookies)

# 获取html字符串(浏览器element中的内容)
print(driver.page_source)

# 获取当前url, 如果上面使用过click(), 那么将会获得点击之后的页面
print(driver.current_url)

driver.close()  # 关闭页面, 因为浏览器能打开多个页面,如果只剩一个页面, 则相当于退出浏览器
# 退出浏览器
time.sleep(3)
driver.quit()
