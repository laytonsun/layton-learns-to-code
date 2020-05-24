#!/usr/bin/env python3
# app: 豆瓣电影 Top 250 爬虫
# author: Layton
# update: 2020-05-24

import urllib.request as request  # 引入 urllib.request 模块
from bs4 import BeautifulSoup  # 引入通过 pip install BeautifulSoup 安装好的模块
from time import localtime, strftime  # 引入 time 模块中需要的函数

headline = '豆瓣电影 Top 250'  # 定义文件标题
update = strftime('%Y-%m-%d', localtime())  # 计算文件生成时间
results = []  # 定义一个空列表，用于存放处理后的结果

siteURL = 'https://movie.douban.com/top250'  # 定义目标网站地址
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0 Win64 x64 rv: 76.0) Gecko/20100101 Firefox/76.0'
}  # 模拟真实浏览器的 header 参数（否则会被限制访问），更复杂的情况还需要模拟 cookies


def getData(url):  # 封装爬虫函数，用于多次调用
    req = request.Request(url, headers=headers)  # 封装包含 url 和 header 的 http 请求
    with request.urlopen(req) as response:  # 发送请求，使用 with 语法更安全
        data = response.read().decode('utf-8')  # 获取网页内容，并应用 utf-8 编码（否则会是乱码）
    soup = BeautifulSoup(data, 'html.parser')  # 使用 html 方式解析网页内容

    items = soup.select('ol.grid_view li')  # 使用 css 选择器筛出榜单上各部影片的信息，以列表形式返回
    for item in items:  # 遍历影片信息列表
        # 获得每部影片的排名，处理成整形
        rank = int(item.find('em').string)
        # 获得每部影片的评分，处理成浮点
        rating = float(item.find('span', class_='rating_num').string)
        # 获得每部影片的片名，一部影片可能有多个片名，用推导式遍历后拼接成字符串
        name = "".join(title.string for title in item.find_all(class_='title'))

        movie = (rank, rating, name)  # 用一个元组存放一部影片的信息
        results.append(movie)  # 将影片的元组添加至结果列表

    nextPage = soup.find('a', string='后页>')['href']  # 获取后一页的链接，注意最后一页没有「后页」链接
    return nextPage  # 将该链接抛回给函数


pageURL = siteURL  # 定义第一个目标网页
while True:  # 循环调用爬虫函数
    try:
        pageURL = siteURL + getData(pageURL)  # 爬取当前页面，抛出后一页的链接并拼接起来
    except TypeError:  # 最后一页没有「后页」链接，将会出错，则终止循环
        break

with open('data.txt', 'w', encoding='utf-8') as file:  # 打开一个文本文件，使用 with 语法更安全
    file.write('{0} 截止 {1}'.format(headline, update))  # 写入文件标题行
    file.write('\n' + '{0}\t{1}\t{2}'.format('#', '评分', '影片名称'))  # 换行，写入表格标题
    for result in results:  # 将结果循环写入
        file.write('\n' + '{0}\t{1}\t{2}'.format(*result))  # 变量可以简写为「星号+元组」
