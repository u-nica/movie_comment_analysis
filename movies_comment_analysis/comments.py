import urllib.request
from bs4 import BeautifulSoup
import random
import time
import requests
import csv

# """获取url页面"""
user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
]

headers = {
    'Cookie': 'bid=NQVd8G1_Go4; viewed="30425286_34933159_34950212_35228068_35283391_35427944_35776311_35813434_34815293_26644280"; _ga=GA1.1.1608230401.1715267136; _pk_id.100001.8cb4=85b3df6d63e3de26.1724299278.; _ga_RXNMP372GL=GS1.1.1725431352.3.0.1725431359.53.0.0; ll="108314"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.26274; dbcl2="262744898:4Ba7k5dHxRM"; _vwo_uuid_v2=DE12137C5503A2FE69CCD8021C7858F70|a1f9eda6657ac8cb1e93b32e7d492365; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1733357135%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.8cb4=1; ap_v=0,6.0; __utma=30149280.1608230401.1715267136.1733298216.1733357136.14; __utmz=30149280.1733357136.14.9.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ck=zuQQ; __utmc=30149280; frodotk_db="06f551025853463c14dff30708f9d2b4"; __utmt=1; __utmb=30149280.54.9.1733358738985',
    'User-Agent': 'str(random.choice(user_agents))',
    'Referer': 'https: // movie.douban.com / subject / 26752088 / comments?status = P',
    'Connection': 'keep-alive'
}


def get_movie_id(movie_name, file_path):
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                if row[0] == movie_name:
                    return row[1]
        return "未找到对应的电影ID，请检查电影名称是否正确。"
    except FileNotFoundError:
        return "文件未找到，请检查文件路径。"
    except Exception as e:
        return f"发生错误：{e}"

def getHtml(url,user_agents,headers):
    req = urllib.request.Request(url, headers=headers)
    req = urllib.request.urlopen(req)
    content = req.read().decode('utf-8')

    return content
def getComment(url):
    """解析HTML页面"""
    html = getHtml(url,user_agents,headers)
    soupComment = BeautifulSoup(html, 'html.parser')

    comments = soupComment.findAll('span', 'short')
    onePageComments = []
    for comment in comments:
        # print(comment.getText()+'\n')
        onePageComments.append(comment.getText()+'\n')

    return onePageComments

def run ():
    file_path = 'movies.csv'
    movie_name = input("请输入电影名称：")
    movie_id = get_movie_id(movie_name, file_path)
    print(f"对应的电影ID是：{movie_id}")
    filename = movie_name+'.txt'
    f = open(filename, 'a', encoding='utf-8')
    j = 0
    for page in range(20):
        url = 'https://movie.douban.com/subject/'+str(movie_id)+'/comments?start=' + str(20*page) + '&limit=20&sort=new_score&status=P'
        print('第%s页的评论:' % (page+1))
        print(url + '\n')
        if '你访问豆瓣的方式有点像机器人程序' or '无法访问此页面' not in getComment(url):
            for i in getComment(url):
                f.write(str(j))
                f.write(i)
                print(j,i)
                j += 1
            time.sleep(5)
            print('\n')
        if '你访问豆瓣的方式有点像机器人程序' in getComment(url):
            headers["Cookie"] = str(input("更新cookie值: "))
