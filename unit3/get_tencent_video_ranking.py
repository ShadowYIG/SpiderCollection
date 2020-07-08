#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/18 15:27
# @Author     : ShadowY
# @File       : get_tencent_video_ranking.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 爬取腾讯视频热门电视剧榜单

import re
import requests
print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")


def get_ranking(url):
    """
    腾讯排行榜页面url
    :param url:
    :return:返回一个字典
    """
    html = requests.get('https://v.qq.com/biu/ranks/?t=hotsearch&channel=tv')
    html.encoding = 'utf-8'
    ranks = re.findall('<span class="num">([0-9]*)</span>', html.text)  # 排名
    names = re.findall('<a href=".*?" class="name" target="_blank" _stat="list-search-single:item_keyword" title=".*?">(.*?)</a>', html.text)
    region_types = re.findall('<div class="item item_b">(.*?)</div>', html.text)  # 地区及类型
    hots = re.findall('<span class="bar_inner" style="width:([0-9]*)%;;"></span>', html.text)  # 热度
    trends = re.findall('<i class="icon_xs(.*?)">', html.text)  # 趋势
    rt_pat = re.compile('<a class="label" key="[0-9]*" rel="noopener noreferrer" target="_blank" _stat="list-search-single:item_label" href=".*?">(.*?)</a>')
    data_list = list()
    for rank, name, region_type, hot, trend in zip(ranks, names, region_types, hots, trends):
        data = {
            '排名': rank,
            '名称': name,
            '地区': re.findall(rt_pat, region_type)[0],
            '类型': ','.join(re.findall(rt_pat, region_type)[1:]),
            '热度': hot,
            '趋势': trend.replace('icon_hold_xs', '-').replace('icon_rise_xs', '↑').replace('icon_decline_xs', '↓')
        }
        data_list.append(data)
    return data_list


if __name__ == '__main__':
    all_data = get_ranking('https://v.qq.com/biu/ranks/?t=hotsearch&channel=tv')
    # print('{:^4}{:^50}{:^5}{:^30}{:^40}{:^5}'.format('排名', '剧名', '地区', '类型', '热度', '趋势'))
    for data in all_data:
        print(data)

