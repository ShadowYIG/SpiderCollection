#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/5/11 17:02
# @Author     : ShadowY
# @File       : get_douban_newbook.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 使用 Selenium 插件模拟登录豆瓣网，并爬取登录后“新书速递” 主页上新书的下列信息：
# 书名、评价人数、作者、出版社、出版时期、简介，将 爬取的数据写入到 mongodb 服务器中 mydb 数据下的 new_book 集合中

from selenium import webdriver
import pprint
import pymongo


db_client = pymongo.MongoClient(host='localhost', port=27017)
db = db_client['tkh']
book_db = db['new_book']


def login(driver):
    """
    登陆豆瓣
    :param driver:
    :return:
    """
    driver.get('https://www.douban.com/')
    driver.implicitly_wait(10)
    driver.switch_to.frame(driver.find_elements_by_tag_name('iframe')[0])
    account_login = driver.find_element_by_xpath('//ul[@class="tab-start"]/li[2]')
    account_login.click()  # 切换密码登录模式
    username = driver.find_element_by_id('username')
    username.clear()
    username.send_keys('')  # 账号
    pwd = driver.find_element_by_id('password')
    pwd.clear()
    pwd.send_keys('')  # 密码
    account_login = driver.find_element_by_class_name('account-form-field-submit ')
    account_login.click()


def get_info(driver):
    """
    获取信息
    :param driver:
    :return:
    """
    driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_xpath('//*[@id="db-global-nav"]/div/div[4]/ul/li[2]/a').click()
    driver.switch_to.window(driver.window_handles[1])
    driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div[1]/div[1]/h2/span[2]/a').click()  # 点击更多
    driver.implicitly_wait(10)
    titles = driver.find_elements_by_xpath('//div[@class="detail-frame"]/h2')
    infos = list()
    for i in range(len(titles)):
        if i == 20:
            driver.execute_script('var q=document.documentElement.scrollTop=0')  # 滚动到页面顶部
        links = driver.find_elements_by_xpath('//a[@class="cover"]')
        detail = driver.find_elements_by_xpath('//div[@class="detail-frame"]/p[3]')[i].text
        book_info = driver.find_elements_by_xpath('//div[@class="detail-frame"]/p[2]')[i].text
        title = driver.find_elements_by_xpath('//div[@class="detail-frame"]/h2')[i].text

        links[i].click()  # 进入详细页
        driver.implicitly_wait(15)
        driver.switch_to.window(driver.window_handles[1])
        evaluator = driver.find_element_by_xpath('//div[@class="rating_sum"]/span').text
        book_info = book_info.replace(' ', '').split('/')

        data = {
            'author': book_info[0],
            'evaluators': evaluator,
            'name': title,
            'press': book_info[1],
            'date': book_info[2],
            'detail': detail
        }
        infos.append(data)
        book_db.insert_one(data)
        print(data)
        driver.back()
    pprint.pprint(infos)


if __name__ == '__main__':
    driver = webdriver.Chrome()
    login(driver)
    get_info(driver)



