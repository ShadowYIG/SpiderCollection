#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/5/12 18:03
# @Author     : ShadowY
# @File       : get_weibo_info.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 爬取微博数据

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pymongo
import time

db_client = pymongo.MongoClient(host='localhost', port=27017)
db = db_client['tkh']
weibo_db = db['weibo']


def login(driver):
    """
    登陆微博
    :param driver:
    :return:
    """
    driver.get('https://weibo.com/')
    user = WebDriverWait(driver, 10, 0.5).until(ec.presence_of_element_located((By.NAME, 'username')))
    # time.sleep(3)
    # user = driver.find_element_by_name('username')
    user.clear()
    user.send_keys('')  # 账号
    pwd = driver.find_element_by_name('password')
    pwd.clear()
    pwd.send_keys('')  # 密码
    driver.find_element_by_xpath('//a[@class="W_btn_a btn_32px"]').click()
    if len(driver.find_elements_by_xpath('//img[@action-type="btn_change_verifycode"]')):  # 存在验证码
        time.sleep(8)
        driver.find_element_by_xpath('//a[@class="W_btn_a btn_32px "]').click()


def get_info(driver):
    """
    获取数据
    :param driver:
    :return:
    """
    q = driver.find_element_by_xpath('//input[@type="text"]')
    q.clear()
    q.send_keys('开学')
    driver.find_element_by_xpath('//a[@node-type="searchSubmit"]').click()
    while True:
        titles = driver.find_elements_by_xpath('//a[@class="name"]')
        contents = driver.find_elements_by_xpath('//p[@class="txt"]')
        forwards = driver.find_elements_by_xpath('//div[@class="card-act"]//li[2]')
        comments = driver.find_elements_by_xpath('//div[@class="card-act"]//li[3]')
        likes = driver.find_elements_by_xpath('//div[@class="card-act"]//li[4]')
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        for title, content, forward, comment, like in zip(titles, contents, forwards, comments, likes):
            data = {
                'title': title.text,
                'content': content.text,
                'forward': forward.text,
                'comment': comment.text,
                'like': like.text
            }
            print(data)
            weibo_db.insert_one(data)
        if len(driver.find_elements_by_xpath('//a[@class="next"]')):
            driver.find_element_by_xpath('//a[@class="next"]').click()
            time.sleep(2)
        else:
            break


if __name__ == '__main__':
    web_driver = webdriver.Chrome()
    login(web_driver)
    get_info(web_driver)