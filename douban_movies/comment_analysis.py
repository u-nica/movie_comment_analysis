import jieba
import pandas as pd
import pylab
from matplotlib import text, pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob

jieba.setLogLevel(jieba.logging.INFO)
import wordcloud
#-*- coding: UTF-8 -*-

def wordAnalysis(comments):
    f = open(comments, 'r', encoding='utf-8')
    content = f.read()
    f.close()
    ls = jieba.lcut(content)
    txt = ' '.join(ls)

    stopwords = set()
    content = [line.strip() for line in open('停用词表.txt', 'r', encoding='utf-8').readlines()]
    stopwords.update(content)

    wc = WordCloud(font_path='c:\windows\Fonts\STZHONGS.TTF', width=1000, height=700, background_color='white',
                   stopwords=stopwords,collocations=False)

    wc.generate(txt)
    plt.imshow(wc)
    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    plt.tight_layout()
    plt.show()

def run():
    name = input("请输入电影名称：")
    comments = name + '.txt'

    #使用wordcloud生成词云图
    wordAnalysis(comments)
