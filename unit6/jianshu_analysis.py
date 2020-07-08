#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/4/13 15:40
# @Author     : ShadowY
# @File       : jianshu_analysis.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 利用jieba分词并保存

import jieba.analyse
import csv
data = ''
with open('jianshu_hot.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for i in reader:
        data += i[1]
data = data.replace('cont', '').replace('...', '')
print(data)
f = open('words_total.txt', 'a')
try:
    jieba.analyse.set_stop_words('中文停用词表.txt')
    words = jieba.analyse.extract_tags(data, topK=100, withWeight=True)
    for word in words:
        print(word[0], word[1]*1000)
        f.write(word[0] + '\t' + str(int(word[1]*1000)) + '\n')
finally:
    f.close()
