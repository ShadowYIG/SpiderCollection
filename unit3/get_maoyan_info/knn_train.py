#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/17 19:53
# @Author     : ShadowY
# @File       : knn_train.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 训练font字库，并输出成模型

import re
import os
import requests
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
import joblib
import matplotlib.pyplot as plt
import time
from fontTools.ttLib import TTFont
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}


def get_font():
    """
    拿到字体文件
    :return: 返回一个字体对象
    """
    html = requests.get('https://maoyan.com/board/4', headers=header)
    font_file_name = re.findall('vfile\\.meituan\\.net/colorstone/(\\w+\\.woff)', html.text)[0]  # 字库名称
    file_list = os.listdir('./fonts')
    if font_file_name not in file_list:  # 判断是否已下载,未下载则下载库
        url = 'http://vfile.meituan.net/colorstone/' + font_file_name
        new_font = requests.get(url, headers=header)
        with open('./fonts/' + font_file_name, 'wb') as f:
            f.write(new_font.content)
    return font_file_name


def get_font_data(font_obj, y_train):
    """
    处理字体信息为列表
    :param font_obj: 字体对象
    :param y_train: 对象对应的值
    :return:
    """
    # gly_order = font_obj.getGlyphOrder()[2:]
    # info = list()
    # for i, g in enumerate(gly_order):
    #     coors = font_obj['glyf'][g].coordinates
    #     coors = [_ for c in coors for _ in c]
    #     coors.insert(0, y_train[i])
    #     info.append(coors)
    # return info
    gly_order = font_obj.getGlyphOrder()[2:]
    info = list()
    for i, g in enumerate(gly_order):
        # if i == 2:
        #     break
        coors = font_obj['glyf'][g].coordinates
        x = []
        y = []
        a = np.array(coors)
        maxs = a.max(axis=0)
        for c in coors:
            x.append(c[0])
            y.append(c[1])
        # plt.scatter(x, y)
        plt.plot(x, y)
        plt.xlim(-200, 800)
        plt.ylim(-200, 800)
        plt.show()

        # coors.insert(0, y_train[i])
        # info.append(coors)
    return info


def get_knn(font_data):
    imp = SimpleImputer(missing_values=np.nan, strategy='mean')
    print(pd.DataFrame(font_data))
    print(imp.fit_transform(pd.DataFrame(font_data)))
    print(pd.DataFrame(imp.fit_transform(pd.DataFrame(font_data))))
    data = pd.DataFrame(imp.fit_transform(pd.DataFrame(font_data)))
    x_train = data.drop([0], axis=1)
    print(x_train)
    y_train = data[0]
    print(y_train)
    print('训练维度：', x_train.shape[1])
    knn = KNeighborsClassifier(n_neighbors=1)
    rf = knn.fit(x_train, y_train)
    joblib.dump(rf, 'rf.model')
    return knn


if __name__ == '__main__':
    # count = input('请输入需要训练的字库个数（推荐5个左右）：')
    # fd = list()
    # for _ in range(0, int(count)):
    #     font_name = get_font()
    #     num = input('请按顺序输入数字串(文件名）%s：' % font_name)
    #     num_list = list(num)
    #     font = TTFont('./fonts/' + font_name)
    #     fd += get_font_data(font, num_list)
    # print(fd)
    # get_knn(fd)
    # with open('./fonts/0a32e3d210f242679444bb7e1cdb50b62268.woff') as f:
    font = TTFont('./fonts/0a32e3d210f242679444bb7e1cdb50b62268.woff')
    datas = get_font_data(font, list('3024618795'))
    # get_knn(datas)

    # for i in range(0, 1000):
    #     print(get_font())
    #     time.sleep(1)

