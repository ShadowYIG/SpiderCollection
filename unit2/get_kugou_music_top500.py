#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/6 17:40
# @Author  : ShadowY
# @File    : get_kugou_music_top500.PY
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
import time

print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")


# 爬取歌曲信息的函数
def get_info(rank_url):
    """
    :param rank_url: 歌曲top500单页信息的链接
    :return: dict 返回一个含有排名、歌手、歌曲、时间的字典
    """
    head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    wb_data = requests.get(rank_url, headers=head)
    soup = BeautifulSoup(wb_data.text, 'html.parser')
    ranks = soup.select('span.pc_temp_num')
    song_infos = soup.select('div.pc_temp_songlist > ul > li > a')
    times = soup.select('span.pc_temp_tips_r > span')
    for rank, song_info, ti in zip(ranks, song_infos, times):
        data = {
            '排名': rank.get_text().strip(),
            '歌手': song_info.get_text().split('-')[0],
            '歌曲': song_info.get_text().split('-')[1],
            '时间': ti.get_text().strip()
        }
        print(data)


if __name__ == '__main__':
    urls = ['https://www.kugou.com/yy/rank/home/{}-8888.html?from=rank'.format(str(i)) for i in range(1, 24)]
    for url in urls:
        get_info(url)
    time.sleep(1)
