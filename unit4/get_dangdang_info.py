#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/23 16:52
# @Author     : ShadowY
# @File       : get_dangdang_info.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 获取当当网机器学习图书信息

import requests
from lxml import etree
import xlwt
print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}


def get_main_page(url):
    """
    获取主页书籍信息
    :param url:需要爬取的url
    :return:
    """
    html = requests.get(url, headers=header)
    html.encoding = 'GB2312'
    selector = etree.HTML(html.text)
    book_infos = selector.xpath('//li[starts-with(@class, "line")]')
    infos = list()
    for book_info in book_infos:
        name = book_info.xpath('./a/@title')  # 书名
        now_price = book_info.xpath('./p[3]/span[1]/text()')  # 折扣价
        pre_price = book_info.xpath('./p[3]/span[2]/text()')  # 定价
        author = '、'.join(list(set(book_info.xpath('.//a[@name="itemlist-author"]/@title'))))  # 作者
        if len(author) == 0:
            author = '无'
        # print(author)
        date = '、'.join(book_info.xpath('./p[@class="search_book_author"]/span[2]/text()'))  # 出版时间
        # print(date)
        publisher = book_info.xpath('.//a[@name="P_cbs"]/text()')  # 出版社
        comment = book_info.xpath('.//a[@name="itemlist-review"]/text()')  # 评论数
        detail = book_info.xpath('./p[@class="detail"]/text()')  # 简介
        info = {
            '书名': name,
            '折扣价': now_price,
            '定价': pre_price,
            '作者': author,
            '出版日期': date.replace('/', ''),
            '出版社': publisher,
            '评论数': comment,
            '简介': detail,
        }
        infos.append(info)
        # print(info)
        # print(name, now_price, pre_price)
    return infos


if __name__ == '__main__':
    urls = ['http://search.dangdang.com/?key=%BB%FA%C6%F7%D1%A7%CF%B0&act=input&page_index=' + str(i) for i in range(1, 5)]

    book = xlwt.Workbook(encoding='utf - 8')  # 创建工作簿
    sheet = book.add_sheet('Sheet1')  # 创建工作表
    sheet.write(0, 0, '书名')
    sheet.write(0, 1, '折扣价')
    sheet.write(0, 2, '定价')
    sheet.write(0, 3, '作者')
    sheet.write(0, 4, '出版日期')
    sheet.write(0, 5, '出版社')
    sheet.write(0, 6, '出版社')
    sheet.write(0, 7, '评论数')
    for page, url in enumerate(urls):
        infos = get_main_page(url)
        for r, info in enumerate(infos):
            sheet.write(r + 1 + page * 60, 0, info['书名'])
            sheet.write(r + 1 + page * 60, 1, info['折扣价'])
            sheet.write(r + 1 + page * 60, 2, info['定价'])
            sheet.write(r + 1 + page * 60, 3, info['作者'])
            sheet.write(r + 1 + page * 60, 4, info['出版日期'])
            sheet.write(r + 1 + page * 60, 5, info['出版社'])
            sheet.write(r + 1 + page * 60, 6, info['评论数'])
            sheet.write(r + 1 + page * 60, 7, info['简介'])
        book.save('book.xls')  # 保存到文件中
        print('以完成写入第%d页，本页有%d条数据' % (page+1, len(infos)))
