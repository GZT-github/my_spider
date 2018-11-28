import requests
from requests.exceptions import RequestException
import re
import json


def get_one_page(url, headers):
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        return None
    except RequestException:
        return None


def main(page):
    i = 0
    url = 'https://search.jd.com/search?keyword=%E5%B0%8F%E7%B1%B3%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&bs=1&psort=3&ev=exbrand_%E5%B0%8F%E7%B1%B3%EF%BC%88MI%EF%BC%89%5E&page='+str(page)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    html = get_one_page(url, headers)
    for item in parse_one_page(html):
        if i < 25:
            print(item)
            write_to_file(item)
            i += 1



def parse_one_page(html):
    pattern = re.compile('<div.*?"p-price">.*?<i>(.*?)</i>.*?</div>.*?<em>.*?([\u4E00-\u9FFF]+).*?([\u4E00-\u9FFF]+).*?([\u4E00-\u9FFF]+).*?([\u4E00-\u9FFF]+).*?</em>.*?<strong.*?>.*?<a.*?>(.*?)</a>.*?</strong>.*?<span.*?"J_im_icon".*?>.*?<a.*?>(.*?)</a>',re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            '价格（元）': item[0],
            '商品名': item[1]+item[2]+item[3]+item[4],
            '评论数': item[5],
            '商家': item[6]
        }


def write_to_file(content):
    with open('spider_results_13.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()

if __name__ == '__main__':
    for i in range(1, 9):
        main(i)
