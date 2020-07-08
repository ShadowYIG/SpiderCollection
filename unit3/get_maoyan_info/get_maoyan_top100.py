#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/17 10:41
# @Author     : ShadowY
# @File       : get_maoyan_top100.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 获取猫眼榜单top100电影信息

import re
import requests
import csv
import pandas as pd
import joblib
import numpy as np
from sklearn.impute import SimpleImputer
from fontTools.ttLib import TTFont

print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}


def get_one_page(url):
    """
    拿到榜单中一页的电影连接
    :param url: 页面的链接
    :return: 返回电影详细页
    """
    html = requests.get(url, headers=header)
    pat = re.compile('(?s)<p class="name"><a href="(.*?)" title=".*?" data-act="boarditem-click" data-val=".*?">(.*?)</a></p>.*?<p class="star">(.*?)</p>')
    infos = re.findall(pat, html.text)  # 链接 电影名 主演
    # film_url_list = ['https://maoyan.com' + abs_url for abs_url in film_url_list]
    ranking = re.findall('<i class="board-index board-index-[0-9]*">([0-9]*)</i>', html.text)  # 排名
    scores = re.findall('<p class="score"><i class="integer">([0-9]*[.])</i><i class="fraction">([0-9]*)</i></p>', html.text)  # 用户评分
    infos = [
        [
            ranking[key],  # 排名
            'https://maoyan.com' + info[0],  # 详细页url
            info[1],  # 电影名
            re.sub('[\n 主演：]', '', info[2]),  # 主演
            scores[key][0] + scores[key][1]  # 用户评分
         ] for key, info in enumerate(infos)
    ]
    return infos


def get_font(font_name):
    """
    下载字库
    :param font_name: 字库的名称
    :return: 返回字体对象
    """
    # file_list = os.listdir('./fonts')
    # if font_name not in file_list:  # 判断是否已下载,未下载则下载库
    #     url = 'http://vfile.meituan.net/colorstone/' + font_name
    #     new_font = requests.get(url, headers=header)
    #     with open('./fonts/' + font_name, 'wb') as f:
    #         f.write(new_font.content)
    # return TTFont('./fonts/' + font_name)
    url = 'http://vfile.meituan.net/colorstone/' + font_name
    new_font = requests.get(url, headers=header)
    with open('./font.woff', 'wb') as f:
        f.write(new_font.content)
    return TTFont('./font.woff')


def knn_predict(data):
    """
    利用knn识别字体
    :param data:需要识别的字库信息
    :return:识别结果列表
    """
    df = pd.DataFrame(data)  # 变换为表
    print(df)
    data = pd.concat([df, pd.DataFrame(np.zeros(
        (df.shape[0], 120 - df.shape[1])), columns=range(df.shape[1], 120))], axis=1)  # 合并，如果自己训练的训练集需要将120改为自己的数据维度
    print(data)
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')  # 补全数据,以免出现错误
    data = pd.DataFrame(imp.fit_transform(pd.DataFrame(data)))  # 标准化
    rf = joblib.load('./knn.model')
    print(rf)
    y_predict = rf.predict(data)
    print(y_predict)
    return y_predict


def modify_data(font, or_data):
    """
    获取编码对应的数字
    :param font:字体文件对象
    :param or_data：需要替换的数据
    :return:
    """
    glyf_order = font.getGlyphOrder()[2:]  # 丢掉前2个
    info = []
    for g in glyf_order:
        coors = font['glyf'][g].coordinates
        coors = [_ for c in coors for _ in c]
        info.append(coors)
    num_list = map(lambda x: str(int(x)), knn_predict(info))  # 预测到的数字
    uni_list = map(lambda x: x.lower().replace('uni', '&#x') + ';', glyf_order)  # 编码
    num_dict = dict(zip(uni_list, num_list))  # 编码-数字字典
    data = or_data
    for key, val in zip(num_dict.keys(), num_dict.values()):
        data = data.replace(key, val)
    return data


def get_one_film_info(url):
    """
    拿到电影的详细页数据
    :param url: 电影的详细页链接
    :return:
    """
    html = requests.get(url, headers=header)
    name = re.search('<h1 class="name">(.*?)</h1>', html.text).group(1)  # 电影名称
    e_name = re.search('<div class="ename ellipsis">(.*?)</div>', html.text).group(1)  # 电影英文名称
    director = re.search('(?s)<div class="info">.*?<a href=".*?" target="_blank" class="name">(.*?)</a>.*?</div>', html.text).group(1).replace('\n', '').replace(' ', '')  # 导演
    film_type = re.search('<a\\s*class="text-link"\\s*href=".*?"\\s*target="_blank">\\s*(.*?)\\s*</a>', html.text).group(1)  # 剧情类型
    release_time = re.search('<li class="ellipsis">((?:[-]?[0-9]*)*).*?</li>', html.text).group(1)  # 上映时间
    film_length = re.search('[0-9]*分钟', html.text).group()  # 片长
    if '<span class="no-info">暂无</span>' not in html.text:  # 处理无票房情况
        box_offices = re.search('<div class="movie-index-content box">\\s*<span class="stonefont">(.*?)</span><span class="unit">(.*?)</span>\\s*</div>', html.text)  # 累计票房,发现这个是字体反爬
        box_office = box_offices.group(1) + box_offices.group(2)
        font_file_name = re.findall('vfile\\.meituan\\.net/colorstone/(\\w+\\.woff)', html.text)[0]  # 字库名称
        font_obj = get_font(font_file_name)  # 拿到字库
        box_office = modify_data(font_obj, box_office)  # 替换编码
    else:
        box_office = '暂无'

    awards = re.findall('<div>\\s*<div class="portrait">\\s*<img src=".*?" alt="">\\s*</div>\\s*(.*?)\\s*</div>', html.text)  # 奖项
    introduction = re.search('<span class="dra">(.*?)</span>', html.text).group(1)  # 剧情简介
    info_dict = {
        '电影名称': name,
        '电影英文名称': e_name,
        '导演': director,
        '剧情类型': film_type,
        '上映时间': release_time,
        '片长': film_length,
        '累计票房': box_office,
        '奖项': awards,
        '剧情简介': introduction,
    }
    return info_dict


def write2csv(datas, dest):
    """
    写入csv文档
    :param datas: 需要写入的数据信息（dict）
    :param dest: 写入的文件路径
    """
    headers = ['排名', '电影名称', '电影英文名称', '导演', '剧情类型', '上映时间', '片长', '累计票房', '主演', '评分', '奖项', '剧情简介']
    with open(dest, 'w+', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, headers)
        writer.writeheader()
        for data in datas:
            writer.writerow(data)


if __name__ == '__main__':
    page_urls = ['https://maoyan.com/board/4?offset=' + str(page) for page in range(0, 100, 10)]
    films_info = list()
    for page_url in page_urls:  # 获取每页的电影信息及链接
        films_info_url = get_one_page(page_url)
        for film_info_url in films_info_url:  # 获取所有电影的详细页面
            film_info = get_one_film_info(film_info_url[1])
            # 将排名页的数据也加到里面
            film_info['排名'] = film_info_url[0]
            film_info['主演'] = film_info_url[3]
            film_info['评分'] = film_info_url[4]
            films_info.append(film_info)
            print(film_info)
    write2csv(films_info, 'catMovie.csv')  # 将信息写入文件
    print('已写入到catMovie.csv')

    # file_info = get_one_page('https://maoyan.com/board/4')
    # file_info = get_one_film_info('https://maoyan.com/films/2039')
    # print(file_info)

    # font = TTFont('./fonts/0a32e3d210f242679444bb7e1cdb50b62268.woff')
    # glyf_order = font.getGlyphOrder()[2:]  # 丢掉前2个
    # info = []
    # for g in glyf_order:
    #     coors = font['glyf'][g].coordinates
    #     coors = [_ for c in coors for _ in c]
    #     info.append(coors)
    # knn_predict(info)