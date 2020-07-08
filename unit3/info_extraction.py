#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time       : 2020/3/13 13:23
# @Author     : ShadowY
# @File       : info_extraction.py
# @Software   : PyCharm
# @Version    : 1.0
# @Description: None

import re
s = "555-1239Moe Szyslak(636) 555-0113Burns, C.Montgomery555-6542Rev. Timothy Lovejoy555 8904Ned Flanders636-555-3226Simpson,Homer5553642Dr. Julius Hibbert"
pat = re.compile("(\\(?\\d+\\)?(?:[- ]\\d+)*)((?:[ .,]?[a-zA-Z]*)*)")
match_list = re.findall(pat, s)
print(match_list)
