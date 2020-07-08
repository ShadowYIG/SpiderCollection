import requests
from lxml import etree
import csv

# 创建csv

with open('./doubanbook.csv','wt',newline='',encoding='utf-8') as fp:
    writer = csv.writer(fp)
    writer.writerow(('书名', '书的链接', '作者', '出版社', '出版日期', '价格', '评分', '评价')) #写入标题
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}
    urls = ['https://book.douban.com/top250?start={}'.format(str(i)) for i in range(0, 100, 25)]   # 爬虫网页地址
    for url in urls:
        html = requests.get(url, headers=headers)
        selector = etree.HTML(html.text)
        infos = selector.xpath('//tr[@class="item"]')
        # print('书名','书的链接','作者','出版社','出版日期','价格','评分','评价')
        for info in infos:
            name = info.xpath('td/div/a/@title')[0]
            href = info.xpath('td/div/a/@href')[0]
            book_infos = info.xpath('td/p/text()')[0]
            author = book_infos.split('/')[0]
            publisher = book_infos.split('/')[-3]
            date = book_infos.split('/')[-2]
            price = book_infos.split('/')[-1]
            rate = info.xpath('td/div/span[2]/text()')[0]
            comments = info.xpath('td/p/span/text()')
            comments = comments[0] if len(comments) != 0 else '空'
            writer.writerow((name, href, author, publisher, date, price, rate, comments))
