#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/6 18:24
# @Author  : ShadowY
# @File    : qroom_shenzhen.py
# @Software: PyCharm
# 爬取深圳Q房网出租房源信息

import requests
import time
import csv
import re
from bs4 import BeautifulSoup

print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}
start = time.perf_counter()


def get_one_page(page_url, page_num=1):  # 取得一页的数据
    """
    爬取某一页所有房源的链接并调用详细页爬取函数
    :param page_url: 房源某一页的链接
    :param page_num: 当前的页数（仅用于记录总条数用于输出增加爬取体验感）
    :return:
    """
    html = requests.get(page_url, headers=header)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    links = soup.select('div.list-result > ul a.house-title')
    page_list = list()
    num = 0
    for link in links:  # 取得所有href并调用详细页
        num += 1
        print("\r正在爬取第%d页，第%d个房源，已完成%d个房源，用时%.2f秒" % (page_num, num, (page_num - 1) * 30 + num, time.perf_counter() - start), end='')
        house = get_one_det("https://shenzhen.qfang.com" + link.get('href'))
        page_list.append(house)

    return page_list


def get_one_det(det_url):
    """
    爬取详细页信息
    :param det_url: 房源详情页的链接
    :return:
    """
    html = requests.get(det_url, headers=header)
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'lxml')
    name = soup.select('div.head-info-list > ul > li > p > a')[0].get_text()  # 小区名称
    price = soup.select('div.head-info-field.sale-rent.fl.clearfix > p.head-info-price.fl')[0].get_text()  # 价格
    layout = soup.select('div.housing-info-con > ul div')[0].get_text().strip()  # 户型
    area = soup.select('div.housing-info-con > ul div')[2].get_text().strip()  # 面积
    style = soup.select('#hsEvaluation > ul > li > p')[1].get_text().strip().replace(u'\xa0', u'').replace('\n', '').replace(u'\u3000', u'')  # 特点
    agent = soup.select('#headInfo p.name > a')[0].get_text().strip()  # 登记经纪人
    imgs = soup.select('#hsPics > ul img')  # 房源图片
    # 使用正则方式获取所有图片
    # photos = soup.select('#hsPics > ul')
    # img_list = re.findall(r'(?i)(http(?:s)?://.*?\.(?:jpg|png))', str(photos))
    # print("房源图片地址：", photo_urls)
    img_list = list()
    for img in imgs:
        img_list.append(img.get('data-src'))
    house = {
        'name': name,
        'style': style,
        'layout': layout,
        'area': area,
        'price': price,
        'agent': agent,
        'img': img_list
    }
    # time.sleep(0.3)
    return house


def write2csv(datas, dest):
    """
    写入csv文档
    :param datas: 需要写入的数据信息（dict）
    :param dest: 写入的文件路径
    :return:
    """
    headers = ['name', 'style', 'layout', 'area', 'price', 'agent', 'img']
    with open(dest, 'w+', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for data in datas:
            writer.writerow(data)


if __name__ == '__main__':
    urls = ["https://shenzhen.qfang.com/rent/f{}".format(i) for i in range(1, 100)]
    page = 0
    sz_list = list()
    try:
        for url in urls:
            page += 1
            page_lists = get_one_page(url, page)
            print('\n', page_lists, '\n')
            sz_list += page_lists
            # time.sleep(0.3)
    except Exception:
        pass
    print('正在写入文件')
    write2csv(sz_list, 'data.csv')
    print('写入完成')
    print('共', len(sz_list), '个', sz_list)
