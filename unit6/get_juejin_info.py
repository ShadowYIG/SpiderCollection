#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/4/13 17:16
# @Author     : ShadowY
# @File       : get_juejin_info.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 获取掘金后端信息
import requests
import json
import pymongo

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36',
    'Referer': 'https://juejin.im/',
    'X-Agent': 'Juejin/Web',
    'Content-Type': 'application/json'
}
payload = {"operationName": "",
           "query": "",
           "variables": {
               "tags": [],
               "category": "5562b419e4b00c57d9b94ae2",
               "first": 20,
               "after": "",
               "order": "POPULAR"},
           "extensions": {
               "query": {
                   "id": "653b587c5c7c8a00ddf67fc66f989d42"
               }
           }
           }


def get_one_page(page_url, count=9999):
    """
    获取掘金一页信息
    :param page_url:
    :param count:
    :return:
    """
    infos = list()
    while True:
        res = requests.post(page_url, headers=header, data=json.dumps(payload))
        res.encoding = 'utf-8'
        html = res.text
        p_json = json.loads(html)['data']['articleFeed']['items']
        count -= 1
        if count == 0 or not p_json['pageInfo']['hasNextPage']:  # 判断是否结束
            break
        payload['variables']['after'] = p_json['pageInfo']['endCursor']
        datas = p_json['edges']
        for data in datas:
            info = {
                'comment': data['node']['commentsCount'],  # 评论数
                'title': data['node']['title'],  # 标题
                'likes': data['node']['likeCount'],  # 点赞数
                'update': data['node']['updatedAt'],  # 更新时间
                'username': data['node']['user']['username'],  # 用户名称
                'cont_url': data['node']['originalUrl'],  # 文章链接
            }
            print(info)
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
    jue = db['juejin']
    jue.insert_many(data)


if __name__ == '__main__':
    url = 'https://web-api.juejin.im/query'
    all_data = get_one_page(url, 20)
    write2mongodb(all_data)
    print('写入数据库成功')
