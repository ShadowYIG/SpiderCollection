#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/23 16:40
# @Author     : ShadowY
# @File       : get_kugou_hot_words.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 输出酷狗热词

import requests
from lxml import etree
print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}
html = requests.get('https://weixin.sogou.com/', headers=header)
html.encoding = 'utf-8'
selector = etree.HTML(html.text)
hot_words = selector.xpath("//ol[@id='topwords']//a/text()")
rankings = selector.xpath("//ol[@id='topwords']//i/text()")
for ranking, hot_word in zip(rankings, hot_words):
    print(ranking, hot_word)
