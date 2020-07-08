#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/4/20 16:33
# @Author     : ShadowY
# @File       : get_lagou_info.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 获取拉勾网信息

import requests
import pymongo
import xlwt
import time

# 连接mongodb 创建lagou集合
client = pymongo.MongoClient('localhost', 27017)  # 建立与mongodb的连接
GZQ = client['tkh']
lagou = GZQ['lagou']


def get_info(url, formdata):
    """
    爬取招聘信息 '岗位名称','公司名称','公司规模','福利待遇','工作类型'等信息
    :param url:
    :param formdata:
    :return:
    """
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=pac',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    time.sleep(5)
    ses = requests.session()  # 创建会话
    ses.headers.update(my_headers)  # 更新会话的头部信息
    ses.get('https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=pac')
    res = ses.post(url, data=formdata)
    result = res.json()  # 将请求所返回的内容转换为json
    info = result['content']['positionResult']['result']  # 取出当前页面的信息
    print(len(info))
    info_list = []  # 存放当前页面信息
    for job in info:
        # 写入mongodb中
        LabelList = ''  # 处理成字符串
        info = {
            '岗位名称': job['positionName'],
            '公司名称': job['companyFullName'],
            '公司规模': job['companySize'],
            '福利待遇': LabelList,
            '工作类型': job['firstType'],
            '发布时间': job['createTime'],
            '城市': job['city'],
            '工作地点': job['district'],
            '工资': job['salary'],
            '工作年限': job['workYear'],
            '学历': job['education']
        }
        for companyLabelList in job['companyLabelList']:
            LabelList = LabelList + "," + companyLabelList
        lagou.insert_one(info)
        info_list.append(info)
    return info_list


# 定义main方法
def main():
    page = int(input("请输入需要抓取的页数:"))
    info_result = []  # 定义一个列表存放所有信息
    workbook = xlwt.Workbook(encoding='utf8')
    worksheet = workbook.add_sheet('lagou', cell_overwrite_ok=True)  # 是否可以被重写或覆盖
    for num in range(1, page+1):
        url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
        formdata = {
            'first': 'false',
            'pn': num,
            'kd': '爬虫'  # 关键字
        }
        try:
            info = get_info(url, formdata)
            info_result = info_result + info  # 将每个页面的信息存入info_result
        except Exception as msg:
            # print('爬取第%页出现问题'% num)
            pass
        print(info_result)
        # 写入lagou.xls

        for row, one_zpinfo in enumerate(info_result):
            one_infos = [
                one_zpinfo['岗位名称'],
                one_zpinfo['公司名称'],
                one_zpinfo['公司规模'],
                one_zpinfo['福利待遇'],
                one_zpinfo['工作类型'],
                one_zpinfo['发布时间'],
                one_zpinfo['城市'],
                one_zpinfo['工作地点'],
                one_zpinfo['工资'],
                one_zpinfo['工作年限'],
                one_zpinfo['学历'],
            ]
            for col, one_info in enumerate(one_infos):
                worksheet.write(row, col, one_info)
        workbook.save('./lagou.xls')
        print('爬取的信息已成功保存！！！')


if __name__ == '__main__':
    main()

