#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/14 18:20
# @Author     : ShadowY
# @File       : get_tipdm_title.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 获取泰迪大数据官网的栏目标题

import re
import requests


def get_title():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}
    html = requests.get('http://www.tipdm.com/tipdm/index.html', headers=header)
    html.encoding = 'utf-8'
    print(html.text)
    pat = re.compile(r'<li.*?><a href="(.*?)".*?>(.*?)</a></li>')
    results = re.findall(pat, html.text)
    data_list = list()
    for match in results:
        url = match[0]
        if 'http' not in url:  # 判断url是否为完整url
            url = 'http://www.tipdm.com:80' + url
        data_list.append([url, match[1]])
        if len(data_list) == 8:
            break
    return data_list


if __name__ == '__main__':
    data = get_title()
    print(data)
