#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/17 21:33
# @Author     : ShadowY
# @File       : get_51job_info.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 爬虫51job的招聘信息
import requests
import re
import csv
import time
print("""
姓名：谭康鸿
学号：201806140018
班级：18级数据科学与大数据技术1班
""")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36'}


def get_one_info(url):
    """
    获取一页信息
    :param url:
    :return:
    """
    res = requests.get(url, headers=headers)
    html = res.text.encode('iso-8859-1').decode('gbk')
    positions = re.findall('<span>\\s*<a target="_blank" title=".*?"\\s*href=".*?"\\s*onmousedown="">\\s*(.*?)\\s*</a>\\s*</span>', html)  # 职位名称
    companys = re.findall('<a target="_blank" title="(.*?)" href=".*?">.*?</a>', html)  # 公司名称
    address = re.findall('<span class="t3">(.*?)</span>', html)[1:]  # 地址
    salarys = re.findall('<span class="t4">(.*?)</span>', html)[1:]  # 薪资
    release_times = re.findall('<span class="t5">(.*?)</span>', html)[1:]  # 发布时间
    info_list = list()
    for position, company, address, salary, release_time in zip(positions, companys, address, salarys, release_times):
        info_list.append({
            '职位': position,
            '公司名称': company,
            '工作地点': address,
            '薪资': salary,
            '发布时间': release_time,
        })
    return info_list


def write2csv(datas, dest):
    """
    写入csv文档
    :param datas: 需要写入的数据信息（dict）
    :param dest: 写入的文件路径
    :return:
    """
    head = ['职位', '公司名称', '工作地点', '薪资', '发布时间']
    with open(dest, 'w+', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, head)
        writer.writeheader()
        for data in datas:
            writer.writerow(data)


if __name__ == '__main__':
    urls = ['https://search.51job.com/list/000000,000000,0000,00,9,99,%25E7%2588%25AC%25E8%2599%25AB,2,{}.html?' \
            'lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&' \
            'dibiaoid=0&line=&welfare='.format(str(i)) for i in range(1, 23)]
    infos = list()
    for url in urls:
        time.sleep(1)
        info = get_one_info(url)
        print(info)
        infos += info
    # write2csv(infos, '51job.csv')
    print('已写入51job.csv')
