#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/6 18:10
# @Author  : ShadowY
# @File    : baidu_news_title.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup

print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")

url = r"http://news.baidu.com/"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'
}

try:
    html = requests.get(url, headers=header)
    soup = BeautifulSoup(html.text, 'lxml')
    ss = soup.select('#channel-all > div > ul > li > a')
    for s in ss:
        print(url + s.get('href'), s.get_text())
except Exception:
    print("访问超时")



