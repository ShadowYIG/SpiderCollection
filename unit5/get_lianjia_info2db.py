#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/30 17:20
# @Author     : ShadowY
# @File       : get_lianjia_info2db.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 获取链家二手房数据存储到mongodb中
import requests
from lxml import etree
import pymongo
print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}
db_client = pymongo.MongoClient(host='localhost', port=27017)
db = db_client['tkh']
lianjia = db['lianjia']


def get_one_page(page_url):
    """
    获取一页房源数据
    :param page_url: 每页的链接
    :return:
    """
    html = requests.get(page_url, headers=header)
    selector = etree.HTML(html.text)
    houses = selector.xpath("//ul[@class='lists']/li[@class='pictext']")
    for house in houses:
        other_info = house.xpath(".//div[contains(@class,'item_other')]/text()")[0]
        other_list = other_info.split('/')
        name = other_list[3]  # 名称
        layout = other_list[0]  # 户型
        area = other_list[1]  # 面积
        orientation = other_list[2]  # 朝向
        price_info = house.xpath(".//div[@class='item_minor']//text()")
        total_price = price_info[0] + price_info[1]  # 总价
        unit_price = price_info[2]  # 单价
        info = {
            'name': name,
            'layout': layout,
            'area': area,
            'orientation': orientation,
            'total': total_price,
            'unit': unit_price
        }
        print(info)
        lianjia.insert_one(info)


if __name__ == '__main__':
    urls = ['https://m.lianjia.com/gz/ershoufang/index/pg{}/'.format(i) for i in range(1, 101)]
    for url in urls:
        get_one_page(url)
