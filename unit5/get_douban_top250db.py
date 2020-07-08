#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/30 16:40
# @Author     : ShadowY
# @File       : get_douban_top250db.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: None
import requests
import re
import pymysql
print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}


def get_one_page_link(page_url):
    """
    获取一页的信息
    :param page_url:
    :return:link_list
    """
    html = requests.get(page_url, headers=header)
    links = re.findall('<div class="hd">\\s*<a href="(.*?)" class="">', html.text)
    return links


def get_movie_info(movie_url, db_cur):
    """
    获取一部电影信息
    :param movie_url:
    :param db_cur: 数据库游标
    :return:
    """
    html = requests.get(movie_url, headers=header)
    rank = int(re.search('<span class="top250-no">No.([0-9]*)</span>', html.text).group(1))  # 排名
    name = re.search('<span property="v:itemreviewed">(.*?)</span>', html.text).group(1)  # 电影名称
    director = re.search('<a href=".*?" rel="v:directedBy">(.*?)</a>', html.text).group(1)  # 导演
    stars = '、'.join(re.findall('<a href=".*?" rel="v:starring">(.*?)</a>', html.text))  # 主演
    types = '、'.join(re.findall('<span property="v:genre">(.*?)</span>', html.text))  # 类型
    country = re.search('<span class="pl">制片国家/地区:</span>\\s*(.*?)\\s*<br/>', html.text).group(1)  # 国家
    release_time = '、'.join(re.findall('<span property="v:initialReleaseDate" content=".*?">(.*?)</span>', html.text))  # 上映时间
    length = '、'.join(re.findall('<span property="v:runtime" content="[0-9]*">(.*?)</span>', html.text))  # 片长
    score = float(re.search('<strong class="ll rating_num" property="v:average">(.*?)</strong>', html.text).group(1))  # 评分
    print(rank, name, director, stars, types, country, release_time, length, score)
    into = "INSERT INTO movietop" \
           "(ranking, movie_name, directors, stars, types, country, release_time, movie_length, score)" \
           " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (rank, name, director, stars, types, country, release_time, length, score)
    db_cur.execute(into, values)


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
    print(table_list)
    if table_name in table_list:
        return 1
    else:
        return 0


if __name__ == '__main__':
    conn = pymysql.connect("localhost", "root", "rootroot", "tkh", charset='utf8')
    cur = conn.cursor()
    create_sql = '''
    CREATE TABLE movietop (
         ranking INT,
         movie_name CHAR(100),
         directors CHAR(50),
         stars MEDIUMTEXT,
         types CHAR(50),
         country CHAR(50),
         release_time VARCHAR(255),
         movie_length CHAR(100),
         score FLOAT(3,1)
    );
    '''
    if not table_exists(cur, 'movietop'):  # 判断数据库是否存在
        cur.execute(create_sql)  # 创建数据表
    urls = ['https://movie.douban.com/top250?start={}&filter='.format(i) for i in range(0, 226, 25)]
    print(urls)
    for url in urls:
        page_links = get_one_page_link(url)
        for link in page_links:
            get_movie_info(link, cur)
    conn.commit()
    conn.close()
