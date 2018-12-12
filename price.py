#!/usr/bin/python
# -*- coding:utf-8 -*- 
# 用途，按照关键字，在SMZDM的国内/海淘/发现频道中，查询最低价、最值价格和出现的日期
# 
import sys
sys.path.append("/root/python_util")
import MyUtil as Util

reload(sys)
sys.setdefaultencoding('utf-8')

import requests
from lxml import etree
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#获取searchy页面的内容
#keys = k k2 k3
#channel = faxian,youhui,haitao
def getItemInfo(keys,channel,pagelimit=3):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'search.smzdm.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    #拼接keys,按页抓取
    keysStr = '+'.join(keys.split(' '))
    resList = []
    for page in range(1,pagelimit+1):
        url = 'https://search.smzdm.com/?c=%s&s=%s&p=%s'%(channel,keysStr,page)
        r = requests.get(url=url, headers=headers)
        selector=etree.HTML( r.text) #将源码转化为能被XPath匹配的格式
        for itemxpath in selector.xpath('//*[@id="feed-main-list"]/li'):
            itemInfo = {}
            itemInfo['title'] =  itemxpath.xpath('div/div[2]/h5/a[1]/@title')[0]
            itemInfo['price'] =  itemxpath.xpath('div/div[2]/h5/a[2]/div/text()')[0]
            itemInfo['time'] =  itemxpath.xpath('div/div[2]/div[2]/div[2]/span/text()')[0].strip()
            itemInfo['up'] =  int(itemxpath.xpath('div/div[2]/div[2]/div[1]/span[1]/span[1]/span[1]/span/text()')[0])
            itemInfo['down'] =  int(itemxpath.xpath('div/div[2]/div[2]/div[1]/span[1]/span[2]/span[1]/span/text()')[0])
            itemInfo['star'] =  itemxpath.xpath('div/div[2]/div[2]/div[1]/span[2]/span/text()')[0]
            itemInfo['uprate'] = 0 if itemInfo['up'] == 0 else  round (float(itemInfo['up']) / ( itemInfo['up'] + itemInfo['down']),2) * 100 
            #获取可能出现的rmb价格
            itemInfo['rmbprice'] = getRmbPrice(itemInfo['price'])
            resList.append(itemInfo)
        return resList

#把字符串的price中的中文价格数字取出来
def getRmbPrice(priceStr):
    return Util.smzdm_getprice(priceStr)

#打印输出
def printItemInfo(resList):
     print "%15s|%4s=%4s|%3s|%s|%s|%s"%('记录时间','人','推荐','收藏数','价格','价格','标题')  
     cnt=0;
     for itemInfo in resList:
        log= "%11s|%4s=%4s%%|%3s|%6s|%s|%s"%(itemInfo['time'],itemInfo['up']+itemInfo['down'],itemInfo['uprate'],itemInfo['star'],itemInfo['rmbprice'],itemInfo['price'],itemInfo['title'])
        if cnt %2 ==0:
           color = 32
        else:
           color = 32
        cnt = cnt+1
        if itemInfo['uprate'] > 70:
            color = 31
        print Util.colorLog(log,color)

if __name__ == '__main__':
        startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print startTime+"---------------------------------------------------------"
        #获取用于过滤的key
        keys = sys.argv[1]
        priceInfoList = getItemInfo(keys,'youhui')
        print "------------------国内------------------"
        printItemInfo(priceInfoList);
        print "------------------发现------------------"
        printItemInfo(getItemInfo(keys,'faxian'))
        print "------------------海淘------------------"
        printItemInfo(getItemInfo(keys,'haitao'))
