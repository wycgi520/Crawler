#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    功能:图片识别
    作者:国易
"""

from PIL import Image
import pytesseract

file_path = r"D:\我的坚果云\努力，奋斗\就业班\爬虫\练习\13-图像识别\1kfhiznu7c.jpg"

img = Image.open(file_path)
print(pytesseract.image_to_string(img))