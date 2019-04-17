#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    功能:豆瓣登录等
    作者:国易
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--incognito")  # 启动进入隐身模式

driver = webdriver.Chrome()

driver.get("https://mail.qq.com/")

"""豆瓣登录"""
# driver.switch_to.frame(0)
#
#
# driver.find_element_by_class_name("account-tab-account").click()
# driver.find_element_by_id("username").send_keys("437891878@qq.com")
# driver.find_element_by_id("password").send_keys("1:0.618wgy3.1415")
# time.sleep(3)
# driver.find_element_by_link_text("登录豆瓣").click()
#
# # 获取cookie
# cookies = {i["name"]:i["value"] for i in driver.get_cookies()}
# print(cookies)

"""内涵段子"""
# li_list = driver.find_elements_by_xpath("//div[@class='j-r-list']/ul/li")  # 只能找到元素, 不能直接找到文本或属性
# print(li_list)
# for li in li_list:
#     ret = li.find_element_by_xpath(".//div[contains(@class,'j-r-list-c-desc')]/a").text  # 只能用text属性把元素的文本提取出来
#     print(ret)

"""寻找百度搜索页面的下一页"""
# print(driver.find_element_by_link_text("下一页>").get_attribute("href"))
# print(driver.find_element_by_partial_link_text("下一页").get_attribute("href"))

"""qq邮箱"""
driver.switch_to.frame("login_frame")
driver.find_element_by_id("u").send_keys("437891878@qq.com")

time.sleep(10)
driver.quit()
