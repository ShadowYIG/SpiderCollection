#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/5/12 14:06
# @Author     : ShadowY
# @File       : get_taobao_info.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: 爬取淘宝网（https://www.taobao.com/）某类商品信息

from selenium import webdriver
import pymongo
import time


db_client = pymongo.MongoClient(host='localhost', port=27017)
db = db_client['tkh']
goods_db = db['goods']


def login(driver):
    """
    登陆
    :param driver:
    :return:
    """
    driver.get('https://login.taobao.com/')
    userid = driver.find_element_by_name('fm-login-id')
    userid.clear()
    userid.send_keys('')  # 账号
    pwd = driver.find_element_by_name('fm-login-password')
    pwd.clear()
    pwd.send_keys('')  # 密码
    time.sleep(5)
    driver.find_element_by_css_selector('[type=submit]').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="J_SiteNavHome"]/div/a').click()


def get_info(driver):
    """
    获取信息
    :param driver:
    :return:
    """
    inp = driver.find_element_by_id('q')
    inp.clear()
    inp.send_keys('电脑')
    driver.find_element_by_css_selector('[type=submit]').click()
    while True:
        driver.switch_to.window(driver.window_handles[0])
        peoples = driver.find_elements_by_xpath('//div[@class="deal-cnt"]')
        prices = driver.find_elements_by_xpath('//div[@class="price g_price g_price-highlight"]')
        names = driver.find_elements_by_xpath('//div[@class="row row-2 title"]')
        locations = driver.find_elements_by_xpath('//div[@class="location"]')
        for people, price, name, location in zip(peoples, prices, names, locations):
            data = {
                'name': name.text,
                'people': people.text,
                'price': price.text,
                'location': location.text,
            }
            print(data)
            goods_db.insert_one(data)
        if len(driver.find_elements_by_xpath('//li[@class="item next"]')):
            driver.find_element_by_xpath('//li[@class="item next"]/a').click()
            time.sleep(5)
        else:
            break


if __name__ == '__main__':
    web_driver = webdriver.Chrome()
    login(web_driver)
    get_info(web_driver)

