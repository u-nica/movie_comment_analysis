import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import tkinter as tk
from tkinter import messagebox

# 坐标轴上能显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def years(data):
    y1 = len(data[data['year'] == '20世纪20年代'])
    y2 = len(data[data['year'] == '20世纪30年代'])
    y3 = len(data[data['year'] == '20世纪40年代'])
    y4 = len(data[data['year'] == '20世纪50年代'])
    y5 = len(data[data['year'] == '20世纪60年代'])
    y6 = len(data[data['year'] == '20世纪70年代'])
    y7 = len(data[data['year'] == '20世纪80年代'])
    y8 = len(data[data['year'] == '20世纪90年代'])
    y9 = len(data[data['year'] == '21世纪00年代'])
    y10 = len(data[data['year'] == '21世纪10年代'])

    # 调节图形大小
    plt.rcParams['figure.figsize'] = [12, 8]
    # 定义标签
    labels = ['20世纪20年代', '20世纪30年代', '20世纪40年代', '20世纪50年代', '20世纪60年代', '20世纪70年代',
              '20世纪80年代', '20世纪90年代', '21世纪00年代', '21世纪10年代']
    # 每一小块的值
    sizes = [y1, y2, y3, y4, y5, y6, y7, y8, y9, y10]
    explode = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    plt.pie(
        sizes,
        explode=explode,
        labels=labels,
        autopct='%1.1f%%'
    )

    plt.axis('equal')
    plt.title('电影年代上榜数量分布图')
    plt.legend(loc=2, borderaxespad=0,numpoints=1,fontsize=6)
    plt.savefig("year.png", bbox_inches='tight')
    # plt.show()


def types(data):
    data['types'] = data['types'].apply(lambda x: str(x) if isinstance(x, str) else "")
    data['types'] = data['types'].apply(lambda x: x.split(' / ') if isinstance(x, str) else [])

    types_expanded = data.explode('types')
    types_expanded = types_expanded.dropna(subset=['types', 'grade'])
    type_avg_grades = types_expanded.groupby('types')['grade'].mean()

    type_avg_grades = type_avg_grades.sort_values(ascending=False)
    print(type_avg_grades)

    plt.figure(figsize=(12, 8))
    type_avg_grades.plot(kind='bar', color='skyblue')

    plt.xlabel('类型')
    plt.ylabel('平均评分')

    plt.xticks(rotation=60, fontsize=10)
    plt.tight_layout()
    plt.ylim(type_avg_grades.min() - 0.1, type_avg_grades.max() + 0.1)
    plt.savefig("types.png", bbox_inches='tight')
    # plt.show()


def region_analysis(data):
    data['addr'] = data['addr'].apply(lambda x: x.split('/'))
    region_expanded = data.explode('addr')
    region_counts = region_expanded['addr'].value_counts()
    valid_regions = region_counts[region_counts > 10].index
    region_avg_grades = region_expanded[region_expanded['addr'].isin(valid_regions)].groupby('addr')['grade'].mean()
    region_avg_grades = region_avg_grades.sort_values(ascending=False)

    print(region_avg_grades)


    # 绘制地区与评分的条形图
    plt.figure(figsize=(12, 8))
    region_avg_grades.plot(kind='bar', color='lightcoral')
    plt.xlabel('地区')
    plt.ylabel('平均评分')
    plt.title('不同地区电影平均评分')
    plt.xticks(rotation=45, fontsize=10)
    plt.ylim(8.7, 9.0)
    plt.tight_layout()
    plt.savefig("addr_grades.png", bbox_inches='tight')
    # plt.show()

    # 进一步分析不同地区的电影类型分布
    # 将每个电影的类型字符串拆分成多个类型
    # data['types'] = data['types'].apply(lambda x: x.split(' / '))

    types_expanded = data.explode('types')
    region_type_distribution = types_expanded.explode('addr').groupby(['addr', 'types']).size().unstack().fillna(0)
    # 仅保留有效地区
    region_type_distribution = region_type_distribution.loc[valid_regions]

    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 100)
    print(region_type_distribution)

    # 可视化地区与类型分布的堆叠条形图
    region_type_distribution.plot(kind='bar', stacked=True, figsize=(14, 8), colormap='tab20')
    plt.xlabel('地区')
    plt.ylabel('电影数量')
    plt.title('不同地区电影类型分布')
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()
    plt.savefig("addr_types.png", bbox_inches='tight')
    # plt.show()


def comment(data):
    # 确保评论数和评分是数值类型
    data['comment'] = pd.to_numeric(data['comment'], errors='coerce')
    data['grade'] = pd.to_numeric(data['grade'], errors='coerce')

    # 去除缺失值
    data_cleaned = data.dropna(subset=['comment', 'grade'])

    # 绘制评论数与评分的散点图
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='comment', y='grade', data=data_cleaned, color='blue', alpha=0.6)
    plt.title('评论数与评分的关系')
    plt.xlabel('评论数')
    plt.ylabel('评分')
    plt.tight_layout()
    plt.savefig("comments.png", bbox_inches='tight')
    # plt.show()

    # 计算皮尔逊相关系数，衡量评论数与评分之间的线性关系
    correlation = data_cleaned['comment'].corr(data_cleaned['grade'])

    print(f"评论数与评分之间的皮尔逊相关系数: {correlation:.3f}")

    # 根据相关系数做简单分析
    if correlation > 0.5:
        print("评论数与评分之间存在较强的正相关关系，评论数多的电影评分往往较高。")
    elif correlation < -0.5:
        print("评论数与评分之间存在较强的负相关关系，评论数多的电影评分较低。")
    else:
        print("评论数与评分之间的相关性较弱，评论数并不能显著预测评分。")

def run ():
    data = pd.read_csv('movies.csv')
    years(data)
    types(data)
    region_analysis(data)
    comment(data)
    plt.show()
