#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/23 19:00
# @Author     : ShadowY
# @File       : analysis_time_comparison.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 利用爬取深圳q房网出租房数据比较lxml，beautifulsoup，re三种解析方式的耗时

import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import time
import matplotlib.pyplot as plt
import csv
import numpy as np
print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")


class GetQRoom:
    def __init__(self, page_url):
        """
        :param page_url: 页面链接
        """
        self.page_html = ''
        self.url = page_url
        self.time = {'lxml': 0.0, 'bs': 0.0, 're': 0.0, 'get_page': 0.0}
        self.data = list()
        self.get_html()

    def get_html(self):
        """
        获取网页数据
        :param page_url:网页url
        """
        start = time.perf_counter()
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}
        html = requests.get(self.url)
        self.page_html = html.text.encode("gbk", 'ignore').decode("gbk", 'ignore')
        self.time['get_page'] = time.perf_counter() - start

    def bs_analysis_page(self):
        """
        利用beautifulsoup库解析并获取数据和时长
        """
        start = time.perf_counter()
        soup = BeautifulSoup(self.page_html, 'lxml')
        layouts = soup.select('div.house-metas.clearfix > p:nth-child(2)')  # 户型
        names = list()
        for i in range(len(layouts)):
            name = soup.select('ul > li:nth-child(' + str(i+1) + ') > div.list-main.fl > div.house-location.clearfix > div > a:nth-child(3)')  # 楼盘名称
            if len(name) == 0:
                name = soup.select('ul > li:nth-child(' + str(i + 1) + ') > div.list-main.fl > div.house-location.clearfix > div > a:nth-child(1)')  # 楼盘名称
            names.append(name[0].get_text())

        areas = soup.select('div.house-metas.clearfix > p:nth-child(4)')  # 面积
        floors = soup.select('div.house-metas.clearfix > p:nth-child(8)')  # 楼层
        prices = soup.select('ul > li > div.list-price > p')  # 租金
        addrs = soup.select('div.house-location.clearfix > div > a:nth-child(1)')  # 区域
        schools = soup.select('div.house-tags.clearfix > a > span')  # 教育配套
        for name, layout, area, floor, price, addr, school in zip(names, layouts, areas, floors, prices, addrs, schools):
            info = {
                '楼盘名称': name,
                '户型': layout.get_text(),
                '面积': area.get_text(),
                '楼层': floor.get_text().replace('\t', '').replace('\n', '').replace('\r', ''),
                '租金': price.get_text().replace('\t', '').replace('\n', '').replace('\r', ''),
                '区域': addr.get_text(),
                '教育配套': school.get_text(),
            }
            self.data.append(info)
        self.time['bs'] = time.perf_counter() - start

    def lxml_analysis_page(self):
        """
        利用lxml的方式获取分析时长以及数据
        """
        start = time.perf_counter()
        selector = etree.HTML(self.page_html)
        infos = selector.xpath('//div[@class="list-result"]/ul/li')
        for item in infos:
            names = item.xpath('.//div[@class="house-location clearfix"]/div/a[3]/text()')  # 楼盘名称
            if len(names) == 0:
                name = item.xpath('.//div[@class="house-location clearfix"]/div/a[1]/text()')[0]  # 楼盘名称
            else:
                name = names[0]
            layout = item.xpath('.//div[@class="house-metas clearfix"]/p[1]/text()')[0]  # 户型
            area = item.xpath('.//div[@class="house-metas clearfix"]/p[2]/text()')[0]  # 面积
            floor = item.xpath('.//div[@class="house-metas clearfix"]/p[4]/text()')[0]  # 楼层
            price = item.xpath('.//div[@class="list-price"]//text()')  # 租金
            addr = item.xpath('.//div[@class="house-location clearfix"]/div/a[1]/text()')[0]   # 区域
            school = item.xpath('.//div[@class="house-tags clearfix"]/a//text()')[0]  # 教育配套
            info = {
                '楼盘名称': name,
                '户型': layout,
                '面积': area,
                '楼层': floor.replace('\t', '').replace('\n', '').replace('\r', ''),
                '租金': ''.join(price).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', ''),
                '区域': addr,
                '教育配套': school,
            }
            self.data.append(info)
        self.time['lxml'] = time.perf_counter() - start

    def re_analysis_page(self):
        """
        利用正则表达式的方式获取分析时长以及数据
        """
        start = time.perf_counter()
        items = re.findall('(?s)<li class="items clearfix">(.*?)</li>', self.page_html)
        for item in items:
            texts = re.findall('(?s)<a class="link".*?key="showKeyword" href=".*?">(.*?)</a>', item)
            if len(texts) == 3:
                name = texts[2]
            else:
                name = texts[0]
            metas = re.findall('<p class="meta-items">\\s*(.*?)\\s*</p>', item)
            layout = metas[0]  # 户型
            area = metas[1]  # 面积
            floor = metas[3]  # 楼层
            prices = re.search('<p class="bigger">\\s*<span class="amount">([0-9]*)</span>\\s*<span class="unit">(.*?)</span>\\s*</p>', item)  # 租金
            price = prices.group(1) + prices.group(2)
            addrs = re.findall('<a class="link" key="showKeyword" href=".*?" >(.*?)</a>', item)  # 区域
            if len(addrs) == 0:
                addr = re.findall('<a class="link" target="_blank" key="showKeyword" href=".*?">(.*?)</a>', item)[0]
            else:
                addr = addrs[0]
            school = re.search('<a class="school fl" href=".*?"><span.*?>(.*?)</span></a>', item).group(1)  # 教育配套
            info = {
                '楼盘名称': name,
                '户型': layout,
                '面积': area,
                '楼层': floor.replace('\t', '').replace('\n', '').replace('\r', ''),
                '租金': ''.join(price).replace('\t', '').replace('\n', '').replace('\r', '').replace(' ', ''),
                '区域': addr,
                '教育配套': school,
            }
            self.data.append(info)
        self.time['re'] = time.perf_counter() - start

    def get_time(self):
        """
        获取时间
        :return:
        """
        return self.time

    def get_data(self):
        """
        去除字典重复并返回字典列表
        :return:
        """
        new_list = list()
        for its in self.data:
            flag = 0
            for it in new_list:
                if its['楼盘名称'] == it['楼盘名称'] and \
                        its['户型'] == it['户型'] and\
                        its['面积'] == it['面积'] and\
                        its['楼层'] == it['楼层'] and\
                        its['租金'] == it['租金'] and\
                        its['区域'] == it['区域'] and \
                        its['教育配套'] == it['教育配套']:
                    flag = 1  # 发现已存在
            if flag == 0:
                new_list.append(its)
        return new_list
        # return self.data


def write2csv(datas, dest):
    """
    写入csv文档
    :param datas: 需要写入的数据信息（dict）
    :param dest: 写入的文件路径
    :return:
    """
    headers = ['楼盘名称', '户型', '面积', '楼层', '租金', '区域', '教育配套']
    with open(dest, 'w+', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for data in datas:
            writer.writerow(data)


if __name__ == '__main__':
    urls = ["https://shenzhen.qfang.com/rent/f{}".format(i) for i in range(1, 11)]
    # 初始化时间列表用于绘图
    all_list = list()
    bs_time = list()
    lxml_time = list()
    re_time = list()
    get_page_time = list()
    pages = list()
    total_time = {'lxml': [], 'bs': [], 're': [], 'get_page': []}
    fig = plt.figure(figsize=(20, 10), dpi=80)

    for page, url in enumerate(urls):
        ans = GetQRoom(url)
        ans.bs_analysis_page()
        ans.lxml_analysis_page()
        ans.re_analysis_page()
        lists = ans.get_data()
        all_list += lists
        # print(ans.get_time())
        # print(len(ans.get_data()))

        # 利用时间作图
        times = ans.get_time()
        pages.append(page + 1)
        bs_time.append(times['bs'])
        lxml_time.append(times['lxml'])
        re_time.append(times['re'])
        get_page_time.append(times['get_page'])
        if page == 0:
            total_time['lxml'].append(times['lxml'])
            total_time['bs'].append(times['bs'])
            total_time['re'].append(times['lxml'])
            total_time['get_page'].append(times['get_page'])
        else:
            total_time['lxml'].append(total_time['lxml'][-1] + times['lxml'])
            total_time['bs'].append(total_time['bs'][-1] + times['bs'])
            total_time['re'].append(total_time['re'][-1] + times['re'])
            total_time['get_page'].append(total_time['get_page'][-1] + times['get_page'])

        plt.rcParams['font.sans-serif'] = ['SimHei']
        fig.suptitle('各解析库耗时分析')
        p1 = fig.add_axes([0.05, 0.05, 0.4, 0.85])
        p2 = fig.add_axes([0.55, 0.05, 0.4, 0.85])
        # 绘制每页用时子图
        p1.set_title("每页用时")
        A, = p1.plot(pages, bs_time, color='green', label="BeautifulSoup耗时%.4f秒" % bs_time[-1])
        B, = p1.plot(pages, lxml_time, color='red', label="lxml耗时%.4f秒" % lxml_time[-1])
        C, = p1.plot(pages, re_time, color='skyblue', label="正则耗时%.4f秒" % re_time[-1])
        D, = p1.plot(pages, get_page_time, color='blue', label="请求耗时%.4f秒" % get_page_time[-1])
        p1.set_xlabel('页码')
        p1.set_ylabel('时间')
        p1.set_yticks([0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.20, 0.4, 0.8, 1.0, 1.2, 1.4, 1.8])
        for a, b, c, d, e in zip(pages, bs_time, lxml_time, re_time, get_page_time):
            p1.text(a, b, '%.4f' % b, ha='center', va='bottom', fontsize=7)  # 每个点的数值
            p1.text(a, c, '%.4f' % c, ha='center', va='bottom', fontsize=7)  # 每个点的数值
            p1.text(a, d, '%.4f' % d, ha='center', va='bottom', fontsize=7)  # 每个点的数值
            p1.text(a, e, '%.4f' % e, ha='center', va='bottom', fontsize=7)  # 每个点的数值
        legend = p1.legend(handles=[A, B, C, D],
                           labels=["BeautifulSoup 平均耗时%.4f秒" % bs_time[-1],
                                   "lxml 平均耗时%.4f秒" % lxml_time[-1],
                                   "正则 平均耗时%.4f秒" % re_time[-1],
                                   "请求 平均耗时%.4f秒" % get_page_time[-1]], loc=2)
        # 绘制总用时子图
        p2.set_title("总用时")
        p2.plot(pages, total_time['bs'], color='green', label="BeautifulSoup耗时%.4f秒" % np.mean(total_time['bs']))
        p2.plot(pages, total_time['lxml'], color='red', label="lxml耗时%.4f秒" % np.mean(total_time['lxml']))
        p2.plot(pages, total_time['re'], color='skyblue', label="正则耗时%.4f秒" % np.mean(total_time['re']))
        p2.plot(pages, total_time['get_page'], color='blue', label="请求耗时%.4f秒" % np.mean(total_time['get_page']))
        p2.set_xlabel('页码')
        p2.set_ylabel('时间')
        for a, b, c, d, e in zip(pages, total_time['bs'], total_time['lxml'], total_time['re'], total_time['get_page']):
            p2.text(a, b, '%.4f' % b, ha='center', va='bottom', fontsize=7)  # 每个点的数值
            p2.text(a, c, '%.4f' % c, ha='center', va='bottom', fontsize=7)
            p2.text(a, d, '%.4f' % d, ha='center', va='bottom', fontsize=7)
            p2.text(a, e, '%.4f' % e, ha='center', va='bottom', fontsize=7)

        legend = p2.legend(handles=[A, B, C, D],
                           labels=["BeautifulSoup耗时%.4f秒" % total_time['bs'][-1],
                                   "lxml耗时%.4f秒" % total_time['lxml'][-1],
                                   "正则耗时%.4f秒" % total_time['re'][-1],
                                   "请求耗时%.4f秒" % total_time['get_page'][-1]], loc=2)
        plt.pause(0.1)

    plt.show()
    # 保存矢量图
    fig.savefig('各解析库耗时分析(矢量).svg', dpi=600, format='svg')
    print('各解析库耗时分析(矢量).svg')
    write2csv(all_list, 'zhufang.csv')
    print('文件写入成功')
