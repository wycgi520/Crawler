#!/usr/bin/env python 
# -*- coding:utf-8 -*-

""" 日志输出格式设置文件 """

__author__ = "WGY"

import logging

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s [%(filename)s] [%(lineno)d] %(asctime)s  %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S'
)