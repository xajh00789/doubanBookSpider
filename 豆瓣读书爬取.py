# coding:utf8
import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
from urllib import parse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"}

query="科幻"


def get_one_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
 #           print(response.text)
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<li.*?href="(.*?)".*?<h2.*?title="(.*?)".*?"pub">\s*(.*?)\s/.*?</div>.*?"rating_nums">(.*?)</span>.*?</li>',
        re.S)
    items = re.findall(pattern, html)
    """
    for item in items:  #遍历列表中的每一个tuple
        print({         #遍历以字典的方式打印每个tuple
            'url':item[0],
            '书名':item[1],
            '作者':item[2],
            '评分':item[3]
        })
"""
    for item in items:
        yield ({
            'url': item[0],
            '书名': item[1],
            '作者': item[2],
            '评分': item[3]
        })


def write_to_file(content):
    with open('豆瓣科幻类图书.txt', 'a',encoding="utf-8") as f:  # a才是追加,w是写入后关闭保存，循环调用会覆盖掉前面写入的
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(num):
    url = "https://book.douban.com/tag/"+query+"?start=" + str(num) + "&type=T"
    print(url)
    html = get_one_page(url)
    parse_one_page(html)
    for item in parse_one_page(html):
        print(item)
        print('\n')
        write_to_file(item)


if __name__ == '__main__':


   # pool=Pool(3)

    for i in range(0,51):  #豆瓣图书每个分类都只有50页信息
        page=(i - 1) * 20
        main(page)

