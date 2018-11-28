import urllib.request
from requests.exceptions import RequestException
from multiprocessing import Pool
import re
import json


def get_one_page(url):
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
        response = urllib.request.urlopen(req)
        response = response.read()
        if True:
            response = response.decode('utf-8')
            return response
        return None
    except RequestException:
        return None


def main(page):
    url = 'https://search.jd.com/Search?keyword=java&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page='+str(page)
    html = get_one_page(url)
    i = 0
    for item in parse_one_page(html):
        if i < 20:
            print(item)
            write_to_file(item)
            i += 1


def parse_one_page(html):
    pattern = re.compile('<em>￥</em><i>(.*?)</i></strong>.*?<em>.*?<font.*?>(.*?)</font>.*?([\u4E00-\u9FFF\d]+)?.*?([\u4E00-\u9FFF\d]+).*?</em>.*?<strong.*?>.*?<a.*?>(.*?)</a>.*?</strong>.*?<span.*?"J_im_icon".*?>.*?<a.*?>(.*?)</a>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '价格（元）': item[0],
            '商品名': item[1]+item[2]+item[3],
            '评论数': item[4],
            '出版社': item[5]
        }


def write_to_file(content):
    with open('spider_results_10.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i for i in range(17)])
