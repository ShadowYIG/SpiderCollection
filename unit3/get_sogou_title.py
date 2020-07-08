#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/12 19:18
# @Author     : ShadowY
# @File       : get_sogou_title.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: None

import re
import requests

print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")
# <a.*?href="(.*?)" uigs-id="nav_[a-z]*" id="[a-z_]*".*?>(.*?)</a>|<span>(.*?)</span>
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
html = requests.get('https://www.sogou.com/', headers=headers)
pat = re.compile(r'<a.*?href *= *[\'"]*(\S+)["\'] uigs-id="nav_[a-z]*" id="[a-z_]*".*?>(.*?)</a>')
search_list = re.findall(pat, html.text)
web = re.findall('<li class="cur"><span>(.*?)</span></li>', html.text)
search_list.insert(1, ('https://www.sogou.com/', web[0]))
for item in search_list:
    print(item)
