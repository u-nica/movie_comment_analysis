import csv
import re
import time
from time import sleep

from bs4 import BeautifulSoup
from lxml import etree
import requests
import json
import pandas as pd

start_url = "?start="
end_url = "&sort=seq&playable=0&sub_type="

def requests_get(url):
    # 伪装头部
    headers = {'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0'}
    # 进行请求
    r = requests.get(url, headers=headers)
    # 进行编码设置
    r.encoding = 'utf-8-sig'
    # 返回获取信息
    return r


# 爬取界面信息
def get_soup(url):
    html = requests_get(url)
    soup = BeautifulSoup(html.text, "lxml")
    return(soup)

def get_movies(target_url):
    n = 0
    i = 1
    movie_ids = []
    movie_names = []
    movie_dis = []
    movie_grade = []
    movie_director = []
    movie_types = []
    movie_actor = []
    movie_addr = []
    movie_year = []

    # 判断是否获取所有的信息，共有626部
    while n < 650:        #构建url
        url = target_url + start_url + str(n) + end_url
        div_list = get_soup(url)
        soup = get_soup(url)
        for each in soup.find_all('div',class_='title'):
        # 在div中，a标签的text的内容就是电影名称
            movie_name = each.a.text.split(' ')[8]
            movie_names.append(movie_name)
            # 提取电影 ID
            href = each.a['href']  # 获取 href 属性
            movie_id = href.split('/')[-2]  # 提取倒数第二段，即 ID
            movie_ids.append(movie_id)
        for each in soup.find_all('div', class_='rating'):
            # 在div中，第二个span的text内容为评分，第三个span的text的内容为评价人数
            a = each.text.split('\n')
            # 获取字符串中的数字
            x = ''.join(re.findall(r'[0-9]', str(a[3])))
            movie_dis.append(x)
            movie_grade.append(float(a[2]))
        for each in soup.find_all('div', class_='abstract'):
            a = each.text
            # .匹配任意字符，除了换行符
            tp = re.search(r'类型: (.*)', a)
            # 对空值和字符进行处理
            if tp == None:
                movie_types.append(" ")
            else:
                movie_types.append(tp.group(1))
            actor = re.search(r'主演: (.*)', a)
            if actor == None:
                movie_actor.append(" ")
            else:
                movie_actor.append(actor.group(1))
            director = re.search(r'导演: (.*)', a)
            if director == None:
                movie_director.append(" ")
            else:
                movie_director.append(director.group(1))
            addr = re.search(r'制片国家/地区: (.*)', a)
            if addr == None:
                movie_addr.append(" ")
            else:
                movie_addr.append(addr.group(1))
            year = re.search(r'年份: (.*)', a)
            if year == None:
                movie_year.append(" ")
            else:
                year_str = year.group(1)
                sj = int(year_str[:2]) + 1
                nd = year_str[2] + '0'
                movie_year.append(str(sj) + '世纪' + nd + '年代')
        n += 25
        print("page "+str(i)+" over!")
        #time.sleep(10)
        i = i+1
    movies = list(zip(movie_names,movie_ids,movie_types,movie_grade,movie_director,movie_addr,movie_actor,movie_year,movie_dis))
    return movies

def run():
    target_url = "https://www.douban.com/doulist/240962/"
    movies = get_movies(target_url)
    # 输出CSV文件的列名
    header = ["names", "ids", "types", "grade", "director", "addr", "actor",
              "year", "comment"]

    # 写入到CSV文件
    with open("movies_test.csv", "w", newline="", encoding="utf_8_sig") as csvfile:
        writer = csv.writer(csvfile)
        # 写入表头
        writer.writerow(header)
        # 写入电影数据`
        writer.writerows(movies)

    print("电影数据已成功写入 movies_test.csv 文件！")




