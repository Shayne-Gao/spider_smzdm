#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
sys.path.append("/root/python_util")
import MyUtil as Util

reload(sys)
sys.setdefaultencoding('utf-8')

import requests

import time
import json
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import hashlib
import pymysql
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def get_real_time_data(pn):
    c_time = int(time.time())
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host': 'www.smzdm.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

#    url = 'https://www.smzdm.com/homepage/json_more?ps=100&timesort=' + str(c_time) + '&p='+str(pn)
    url = 'https://www.smzdm.com/homepage/json_more?p='+str(pn)
    #url = 'https://faxian.smzdm.com/json_more?type=a&timesort='+ str(c_time) + '&p=1'
    r = requests.get(url=url, headers=headers)

    # data = r.text.encode('utf-8').decode('unicode_escape')
    data = r.text

    dataa = json.loads(data)
    dataa = dataa['data']

    resultList = []

    for string in dataa:
        if string.get('article_title') is None:
            continue
        title = string['article_title']
        price = ''
        if 'article_price' in string.keys():
            price = string['article_price']
        link = ''
        if 'article_link' in string.keys():
            link = string['article_link']
        page_url = string['article_url']
        picUrl = string['article_pic']
        if 'gtm' in string.keys():
            rmbPrice = string['gtm']['rmb_price']
        else:
            rmbPrice = 0
        #获取值不值
        result = {
            'title': title,
            'price': price,
            'date' : string.get('article_date',''),
            'link': link,
            'page_url': page_url,
            'pic_url':picUrl,
            'source':'home',
            'rmb_price':rmbPrice,
            'worthy':float(string.get('article_worthy',0)),
            'unworthy':float(string.get('article_unworthy',0)),
        }
        resultList.append(result)

    return resultList

if __name__ == '__main__':
            
    startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print startTime+"---------------------------------------------------------"
    worthCount = 10 #只显示N个评论以上的
    worthRate = 0.6  #只显示值率50以上的
        #获取用于过滤的key
        #获取数据
    for i in range(1,100):
        resultList = get_real_time_data(i)
        #循环处理每次获取的数据
        for result in resultList:
            wc = result['worthy'] + result['unworthy']
            if wc == 0:
                continue
            wr = result['worthy'] / wc
            if wr>0.9:
                color=31
            elif wr>0.8:
                color=33
            elif wr>0.7:
                color=36
            elif wr>0.6:
                color=32#37
            else:
                color=32

            if( wc > worthCount and wr > worthRate ):
                out = "%s|%4s|%.2f|%3d %3d|￥%4s|%s|%s|%s"%(result['date'],result['source'],wr,result['worthy'],result['unworthy'],result['rmb_price'],result['title'],result['price'],result['page_url'])
                print Util.colorLog(out,color)
        if i%10 == 0:
            raw_input('press any key to Continue')
