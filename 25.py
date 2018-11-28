import urllib.request
import re
import json


def get_one_page(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')


def parse_one_page(html):
    pattern = re.compile('<span.*?votes.*?>(.*?)</span>.*?<span.*?comment-info">.*?<a.*?>(.*?)</a>.*?</span>.*?<span.*?"allstar(.*?)0 rating".*?>.*?</span>.*?<span.*?comment-time.*?title=.*?"(.*?)">.*?</span>.*?<span.*?short">(.*?)</span>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'ID': item[1],
            '点赞数': item[0],
            '星数': item[2],
            '评论日期': item[3],
            '评论内容': item[4],
        }


def write_to_file(content):
    with open('spider_results_25.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'https://movie.douban.com/subject/26985127/comments?start=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(50):
        main(i)
