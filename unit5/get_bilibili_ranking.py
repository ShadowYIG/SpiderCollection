#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/30 18:00
# @Author     : ShadowY
# @File       : get_bilibili_ranking.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 爬取bilibili影视磅单

from lxml import etree
import requests
import json
import re
import pymysql
import pymongo
print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}


def get_bili_rank(rank_url):
    """
    获取哔哩哔哩影视排行榜
    :param rank_url:
    :return: list(dict)
    """
    html = requests.get(rank_url, headers=header)
    selector = etree.HTML(html.text)
    items = selector.xpath("//li[@class='rank-item']")
    infos = list()
    for item in items:
        name = item.xpath(".//a[@class='title']/text()")[0]  # 影视名称
        pgc = item.xpath(".//div[@class='pgc-info']/text()")[0]  # 更新集数
        play_info = item.xpath(".//span[@class='data-box']/text()")  # 播放信息
        playback = play_info[0]  # 播放量
        barrage = play_info[1]  # 弹幕量
        like = play_info[2]  # 点赞量
        rank = item.xpath(".//div[@class='num']/text()")[0]  # 排名
        pts = item.xpath(".//div[@class='pts']/div/text()")[0]  # 综合得分
        info = {
            'name': name,
            'pgc': pgc,
            'playback': playback,
            'barrage': barrage,
            'like': like,
            'rank': rank,
            'pts': pts
        }
        infos.append(info)
    return infos


def write2mongodb(data):
    """
    写入mongodb数据库
    :param data: 列表数据
    :return:
    """
    db_client = pymongo.MongoClient(host='localhost', port=27017)
    db = db_client['tkh']
    bili = db['bilibili']
    bili.insert_many(data)


def write2mysql(data):
    """
    写入mysql数据库
    :param data: 列表数据
    :return:
    """
    conn = pymysql.connect("localhost", "root", "rootroot", "tkh", charset='utf8')
    cur = conn.cursor()
    create_sql = '''
        CREATE TABLE bilibili (
             ranking INT,
             v_name CHAR(100),
             pgc CHAR(100),
             playback CHAR(20),
             barrage CHAR(20),
             likes CHAR(20),
             pts INT
        );
        '''
    if not table_exists(cur, 'bilibili'):  # 判断数据库是否存在
        cur.execute(create_sql)  # 创建数据表
    into = "INSERT INTO bilibili" \
           "(ranking, v_name, pgc, playback, barrage, likes, pts)" \
           " VALUES (%s, %s, %s, %s, %s, %s, %s)"
    for d in data:
        values = (d['rank'], d['name'], d['pgc'], d['playback'], d['barrage'], d['like'], d['pts'])
        cur.execute(into, values)


def write2json(data):
    """
    写入json文件
    :param data: 列表数据
    :return:
    """
    with open("bilibili.json", "w", encoding='utf-8') as f:
        json.dump({'infos': data}, f, ensure_ascii=False)


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


if __name__ == '__main__':
    url = 'https://www.bilibili.com/ranking/cinema/177/0/3'
    re_data = get_bili_rank(url)
    # write2mongodb(re_data)
    # write2mysql(re_data)
    # write2json(re_data)
