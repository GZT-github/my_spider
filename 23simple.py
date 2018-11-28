import requests
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup

def get_one_page(url, headers):
    try:
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def write_to_file(content,i):
    with open('spider_results_23simple.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(str(i)+'、'+content, ensure_ascii=False) + '\n')
        f.close()

def write():
    for page in range(0,5):
        if page < 1:
            url = 'https://bbs.pcauto.com.cn/forum-17442.html'
        else:
            url = 'https://bbs.pcauto.com.cn/forum-17442-' + str(page) + '.html'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        soup = BeautifulSoup(get_one_page(url, headers), 'lxml')
        i = j = p = l = m = n = k = 0
        for items in soup.find_all(attrs={'class': 'checkbox_title'}):
            i += 1
            if i < 101:print(items.a.string),write_to_file(items.a.string, str(i))
        for i in soup.find_all(attrs={'class': 'author'}):
            if i.cite:
                j += 1
                if j<101:print(i.cite.a.string),write_to_file(i.cite.a.string, str(j))
        for i in soup.find_all(attrs={'class': 'nums'}):
            if i.cite:
                if i.cite.string:
                    l += 1
                    if l<101:print(str(i.cite.string).strip()),write_to_file(str(i.cite.string).strip(), str(l))
                else:
                    l += 1
                    if l <101:print(i.cite.strong.string.strip()),write_to_file(i.cite.strong.string.strip(), str(l))
        for i in soup.find_all(attrs={'class': 'lastpost'}):
            if i.cite:
                m += 1
                if m<101:print(i.cite.a.string),write_to_file(i.cite.a.string, str(m))
        for i in soup.find_all(attrs={'class': "lastpost"}):
            if i.em:
                n += 1
                if n <101:print(i.em.string),write_to_file(i.em.string, str(n))
        for i in soup.find_all(attrs={'class': 'author'}):
            if i.em:
                k += 1
                if k<101:print(i.em.string),write_to_file(i.em.string, str(k))
        url = 'https://bbs.pcauto.com.cn/forum/loadStaticInfos.ajax?isBrandForum=true&tids=17577747%2C17570877%2C17482396%2C16786205%2C13041689%2C13359823%2C13045091%2C5327907%2C17648400%2C17062864%2C17648329%2C17647850%2C17648007%2C17648214%2C17612860%2C17648094%2C17647996%2C17647929%2C17647562%2C17647783%2C17647818%2C17647845%2C17647855%2C17647803%2C17642981%2C17494661%2C17640611%2C17642661%2C17644585%2C16392504%2C17643188%2C17635605%2C17643300%2C17455202%2C17640474%2C16272016%2C5405610%2C17640533%2C17638788%2C17604174%2C17635729%2C17623481%2C17636424%2C17636106%2C17636149%2C17636013%2C17602523%2C17635586%2C17635661%2C17635585%2C17614195%2C17619435%2C17635328%2C17635280%2C17608667%2C17623626%2C17136371%2C12212555%2C17624362%2C17581111%2C17619741%2C17619441%2C17624018%2C17619691%2C17624139%2C17608594%2C17623996%2C17623819%2C17623728%2C17623835%2C17619469%2C17619482%2C17623556%2C17622270%2C17551614%2C17620311%2C17619972%2C17613051%2C17619407%2C17602891%2C13359823%2C17231022%2C17445660%2C17549513%2C4137885%2C17612485%2C17608207%2C17613760%2C17613714%2C17613599%2C17547665%2C17612878%2C12346597%2C9058158%2C4785804%2C17612742%2C17612672%2C3985109%2C17612251%2C17607957%2C4627110%2C17608359%2C17608513%2C17571111%2C17604191%2C17609601%2C17609506%2C17603889&fid=17442'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36','accept-language': 'zh-CN,zh;q=0.9','referer': 'https://bbs.pcauto.com.cn/forum-17442.html','accept-encoding': 'gzip, deflate, br','x-requested-with': 'XMLHttpRequest'}
        a = requests.get(url=url, headers=headers).text
        if 'topicViews' in json.loads(a).keys():
            for item in json.loads(a).get('topicViews'):
                print(item.get('view'))
                p+=1
                if p<101:write_to_file(str(item.get('view')), str(p))
write()
