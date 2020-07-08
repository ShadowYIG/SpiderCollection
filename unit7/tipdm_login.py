#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/4/21 13:04
# @Author     : ShadowY
# @File       : tipdm_login.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: tipdm官网登陆

import requests
import matplotlib.pyplot as plt

s = requests.session()  # 创建会话
url = 'http://www.tipdm.org/login.jspx?'  # 会员登录主页
rqq = s.get('http://www.tipdm.org/captcha.svl')  # 获取登录的验证码
with open('./login.jpg', 'wb') as f:
    f.write(rqq.content)  # 保存到本地
pic = plt.imread('./login.jpg')  # 读取是一个三通道的0-255的数值
plt.imshow(pic)
plt.show()
a = input('请输入验证码：')
# 构建表单数据
formDatas = {
    'username': '',  # 用户名
    'password': '',  # 密码
    'captcha': a
}

# 以基于表单交互和会话的方式向会员登录页面发出请求
rqqLogin = s.post(url, data=formDatas)  # 以会话中以post方法向会员登录页面发出请求
print(rqqLogin.url)
print(rqqLogin.content.decode('utf8'))  # 返回登录成功的网页内容
rqq_noSession = requests.get(url)
print(rqq_noSession.content.decode('utf8'))