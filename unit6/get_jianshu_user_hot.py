#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/4/10 11:23
# @Author     : ShadowY
# @File       : get_jianshu_user_hot.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 爬取简书某位用户的“热门”信息

import requests
from lxml import etree
import re
import json
import pymysql
import time

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}


def get_page_link(page_url):
    """
    获取详细页链接
    :param page_url:
    :return:None
    """
    res = requests.get(page_url, headers=header)
    html = res.text
    det_urls = re.findall('<a class="title" target="_blank" href="(.*?)">(.*?)</a>', html)
    main_info = re.findall('(?s)<p class="abstract">(.*?)</p>', html)
    infos = list()
    for i, det_url in enumerate(det_urls):
        info = get_detailed_info('https://www.jianshu.com' + det_url[0])
        info['cont'] = main_info[i].replace('\n', '').replace(' ', '')
        infos.append(info)
        print(info['cont'])
    return infos


def get_detailed_info(det_url):
    """
    获取详细页数据
    :param det_url: 详细页链接
    :return: list
    """
    res = requests.get(det_url, headers=header)
    html = res.text
    selector = etree.HTML(html)
    data = selector.xpath('//*[@id="__NEXT_DATA__"]/text()')[0]
    d_data = json.loads(data)
    title = d_data['props']['initialState']['note']['data']['public_title']  # 标题
    content = d_data['props']['initialState']['note']['data']['free_content']  # 文章内容
    comment = d_data['props']['initialState']['note']['data']['comments_count']  # 评论数
    likes_count = d_data['props']['initialState']['note']['data']['likes_count']  # 点赞人数 喜欢人数
    reward = d_data['props']['initialState']['note']['data']['total_rewards_count']  # 打赏人数
    times = timestamp2datetime(d_data['props']['initialState']['note']['data']['first_shared_at'])  # 发表时间
    info = {
        'title': title,
        'content': content,
        'comment': comment,
        'like': likes_count,
        'reward': reward,
        'times': times
    }
    print(info)
    return info


def timestamp2datetime(stamp):
    """
    十位时间戳转时间
    :param stamp:时间戳
    :return:str时间
    """
    time_array = time.localtime(int(stamp))
    other_style_time = time.strftime('%Y{y} %m{m} %d{d} %H:%M:%S', time_array).format(y='年', m='月', d='日')
    return other_style_time


def table_exists(con, table_name):
    """
    判断表是否存在
    :param con: 游标
    :param table_name: 表名
    :return:
    """
    con.execute("show tables;")
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0


def write2mysql(data):
    """
    写入mysql数据库
    :param data: 列表数据
    :return:
    """
    conn = pymysql.connect("localhost", "root", "rootroot", "tkh", charset='utf8')
    cur = conn.cursor()
    create_sql = '''
        CREATE TABLE jianshu_hot (
             title CHAR(200),
             cont TEXT,
             content TEXT,
             comment INT,
             likes_count INT,
             reward_count INT,
             times CHAR(100)
        );
        '''
    if not table_exists(cur, 'jianshu_hot'):  # 判断数据库是否存在
        cur.execute(create_sql)  # 创建数据表
    into = "INSERT INTO jianshu_hot" \
           "(title, cont, content, comment, likes_count, reward_count, times)" \
           " VALUES (%s, %s, %s, %s, %s, %s, %s)"
    for d in data:
        values = (d['title'], d['cont'], d['content'], d['comment'], d['like'], d['reward'], d['times'])
        cur.execute(into, values)


if __name__ == '__main__':
    # 1-26
    urls = ['https://www.jianshu.com/u/9104ebf5e177?order_by=top&page=' + str(page) for page in range(1, 27)]
    for url in urls:
        all_info = get_page_link(url)
        write2mysql(all_info)
    print('写入数据库成功')


