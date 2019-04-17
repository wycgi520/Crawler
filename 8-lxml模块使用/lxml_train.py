#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    功能:实现段子爬取
    作者:国易
"""
from lxml import etree

text = """
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a> # 注意，此处缺少一个 </li> 闭合标签
     </ul>
 </div>
"""

# 能够接收str类型和bytes类型的数据
html = etree.HTML(text)

ret1 = html.xpath ("//li[@class='item-1']/a/@href")

ret2 = html.xpath ("//li[@class='item-1']/a/text()")

# 将url与文本对应取出, 而不是像上面一样分开取出
ret3 = html.xpath ("//a")
# 上面xpath方法取出的是若干element对象, 可对这些对象继续使用xpath方法
for i in ret3:
    url = i.xpath("@href")
    text = i.xpath("text()")
    print(url, text)