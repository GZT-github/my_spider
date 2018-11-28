import requests
from requests.exceptions import RequestException
import re
import json


def get_one_page(url, payloddata, headers):
    try:
        response = requests.post(url=url, data=json.dumps(payloddata), headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def main():
    url = 'http://flights.ctrip.com/itinerary/api/12808/products'
    payloddata = {
        'airportParams': [{'acity': 'BJS',
                           'acityid': 1,
                           'acityname': '北京',
                           'date': '2018-12-01',
                           'dcity': 'SHA',
                           'dcityid': 2,
                           'dcityname': '上海'}],
        '0': {'acity': 'BJS',
              'acityid': 1,
              'acityname': '北京',
              'date': '2018-12-01',
              'dcity': 'SHA',
              'dcityid': 2,
              'dcityname': '上海'},
        'classType': 'ALL',
        'flightWay': 'Oneway',
        'hasBaby': False,
        'hasChild': False,
        'searchIndex': 1
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Host': 'flights.ctrip.com',
        'Origin': 'http://flights.ctrip.com',
        'Referer': 'http://flights.ctrip.com/itinerary/oneway/sha-bjs?date=2018-12-01',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '223',
        'Content-Type': 'application/json',
        'Cookie': '_abtest_userid=1c6531a4-5ef1-4825-aed3-2070f94bf660; _ga=GA1.2.1318902137.1540475639; _gid=GA1.2.1077265062.1540475639; MKT_Pagesource=PC; _RF1=223.104.34.33; _RSG=h5ahc29GXo5EGfOWiol4S9; _RDG=2833e1f545526b2b4e07785f9c39855a29; _RGUID=5ca14090-a6ae-416b-9704-bf2b2062940e; _bfa=1.1540475637736.3n010f.1.1540481408854.1540514462958.3.16; _bfs=1.1; _jzqco=%7C%7C%7C%7C1540475647776%7C1.1529273247.1540475647557.1540483364680.1540514464793.1540483364680.1540514464793.undefined.0.0.15.15; __zpspc=9.4.1540514464.1540514464.1%234%7C%7C%7C%7C%7C%23; _gat=1; _bfi=p1%3D10320673302%26p2%3D0%26v1%3D16%26v2%3D0'
        }
    html = get_one_page(url,payloddata, headers)
    for item in parse_one_page(html):
        print(item)
        #write_to_file(item)


def parse_one_page(html):
    print(html)
    data = json.loads(html)
    a = data.get('data')
    b = str(a)
    pattern = re.compile('flightNumber\'.*?\'(.*?)\'.*?airlineName\'.*?\'(.*?)\'.*?craftTypeName\'.*?\'(.*?)\'.*?craftTypeKindDisplayName\'.*?\'(.*?)\'.*?cityName\'.*?\'(.*?)\'.*?airportName\'.*?\'(.*?)\'.*?cityName\'.*?\'(.*?)\'.*?airportName\'.*?\'(.*?)\'.*?departureDate\'.*?\'(.*?)\'.*?arrivalDate\'.*?\'(.*?)\'.*?salePrice\': (.*?),', re.S)
    items = re.findall(pattern, b)
    for item in items:
        yield {
            '航空公司名称和航班号': item[1]+item[0],
            '机型': item[2]+item[3],
            '起飞时间': item[8],
            '起飞地': item[4]+item[5],
            '降落时间': item[9],
            '降落地': item[6]+item[7],
            '价格': item[10],
        }


def write_to_file(content):
    with open('spider_results_16.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


if __name__ == '__main__':
    main()
