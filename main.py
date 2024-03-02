import config
import requests
import logging
from bs4 import BeautifulSoup
import time
from urllib import parse

headers = config.headers

qiandao_url = "https://tieba.baidu.com/sign/add"
like_url = "https://tieba.baidu.com/f/like/mylike?&pn=1"
like_url_nopage = "https://tieba.baidu.com/f/like/mylike?&pn="
dateadd1 = "ie=utf-8&kw="
dateadd2 = "&tbs=59a07c0b1eb444bb1665799376"
dateadd3 = "&tbs=9e56bc20d422e95d1705118249"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def bapage():
    tieba_like = []
    tieba_list = []
    page_number = ""
    try:
        html = requests.get(like_url,headers=headers).text
    except Exception as e:
        logger.error("获取关注的贴吧出错")
        return 0

    soup = BeautifulSoup(html,'lxml')
    for item in soup.select('.pagination>a '):
            item = item.string
            page_number += item
    page_number = page_number.find("下") + 1
    for i in range(page_number+1):
        if i != 0:
            url = like_url_nopage + str(i)
            html_like = requests.get(url,headers=headers).text
            cc = BeautifulSoup(html_like,'lxml')
            for dd in cc.select('.forum_main>.forum_table>table>tr>td>a'):
                tieba_like.append(dd.attrs)
    for i in tieba_like:
        if 'class' not in i :
            i['href'] = "https://tieba.baidu.com" + i['href']
            tieba_list.append(i)    
    return tieba_list


def sign(tieba_list):
    for i in tieba_list:
        time.sleep(0.2)
        tieba_title = i['title']
        date = parse.quote(tieba_title)+dateadd2
        data1 = dateadd1+date+dateadd3
        respose = requests.post(url=qiandao_url, headers=headers, data=data1)
        print(respose.text.encode('utf-8').decode('unicode_escape'))

if __name__ == '__main__':
    tieba_list = bapage()
    sign(tieba_list)