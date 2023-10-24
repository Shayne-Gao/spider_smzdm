
#smzdm爬虫更新v2版本
# 替换mysql为shelve
# 整合邮件发送，替代原本的serverchan/mail
# 适配Python 3.11+
#

#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
 

# reload(sys)
# sys.setdefaultencoding('utf-8')

import requests
import shelve

import time
import json
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import datetime
import smtplib
import time
from email.mime.text import MIMEText

import smtplib
import hashlib
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

 
 
TO_EMAIL_ADDRESS = ['xxx@qq.com']
MAIL_SENDER = "xxx@qq.com"
MAIL_KEY = 'xxxx'
DATA_FILE = 'smzdm.dat'
KEYS_FILE_PATH = './keys'

def get_real_time_data():
    c_time = int(time.time())
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Host': 'www.smzdm.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    url = 'https://www.smzdm.com/homepage/json_more?timesort=' + str(c_time) + '&p=1'
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
        result = {
            'title': title,
            'price': price,
            'link': link,
            'page_url': page_url,
            'pic_url':picUrl,
            'source':'home',
            'rmb_price':rmbPrice,
        }
        resultList.append(result)

    return resultList
#获取发现频道的信息
def get_real_time_data_faxian():
    c_time = int(time.time())
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Host': 'faxian.smzdm.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    url = 'https://faxian.smzdm.com/json_more?type=a&timesort='+ str(c_time) + '&p=1'
    r = requests.get(url=url, headers=headers)

    # data = r.text.encode('utf-8').decode('unicode_escape')
    data = r.text

    dataa = json.loads(data)
    #dataa = dataa['data']

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
        picUrl = string['article_pic_url']
        result = {
            'title': title,
            'price': price,
            'link': link,
            'page_url': page_url,
            'pic_url':picUrl,
            'source':'faxian',
            'rmb_price':string['gtm']['rmb_price'],
        }
        resultList.append(result)

    return resultList


def read_local_file_keys():
    file = open(KEYS_FILE_PATH)
    finalRes = []
    for line in file:
        if line.startswith("#"):
             continue
        res = {}
        lineList = line.lower().replace("\n",'').replace("\r",'').split('|')

        keys = lineList[0].split(',')
        #ignores
        if len(lineList) == 2:
            ignores = lineList[1].split(',')
        else:
            ignores = []
        #price
        if len(lineList) == 4:
            res['min'] = lineList[2]
            res['max'] = lineList[3]
        else:
            res['min'] = -1
            res['max'] = -1

        #source home/faxian
        if len(lineList) == 5:
            res['src'] = lineList[4]
        else:
            res['src'] = 'home'
        res['keys'] = keys
        res['ignores'] = ignores
        finalRes.append(res);

    return finalRes;

def send_mail(data):
    #文件正文
    dataStr  = '''<html>
<body>
<h1>%s</h1>
<a href="%s"> 打开SMZDM页面</a>
<a href="%s"> 直接去购买</a>

<h3>Rule:%s</h3>
<h3>Source:%s</h3>
<img loading="lazy" src="%s" class="avatar" border="0" align="default">

</body>
</html>

'''%(data['title'],data['page_url'],data['link'],data['matched_rule'],data['source'],data['pic_url'])
    title = result['price']+"|"+result['title']


    email_host = "smtp.qq.com"
    email_port = 465
    email_sender = MAIL_SENDER
    password = MAIL_KEY
    email_receiver = TO_EMAIL_ADDRESS
    email_cc = [""]

    msg = MIMEText(dataStr, 'html')
    msg["Subject"] = title  # 邮件主题描述
    msg["From"] = "gaowlj@qq.com"  # 发件人显示,不起实际作用,只是显示一下
    msg["To"] = ",".join(email_receiver)  # 收件人显示,不起实际作用,只是显示一下
    msg["Cc"] = ",".join(email_cc)  # 抄送人显示,不起实际作用,只是显示一下

    with smtplib.SMTP_SSL(email_host, email_port) as smtp:  # 指定邮箱服务器
        smtp.login(email_sender, password)  # 登录邮箱
        smtp.sendmail(email_sender, email_receiver, msg.as_string())  # 分别是发件人、收件人、格式
        smtp.quit()
    print("发送邮件成功!")



#将记录 按照一定规则生成MD5串，这个会影响结果去重
def md5(result):
#    tempResult = sorted(result.items(), key=lambda result: result[0])
    tempResult = result['title']+result['price']+result['page_url']
    tempResult = tempResult.replace(' ','');
    strRes = str(tempResult)
    m = hashlib.md5()
    m.update(strRes.encode(encoding='utf-8'))
    return m.hexdigest()


def is_data_existed(md5result):
    database = shelve.open(DATA_FILE)
    if md5result not in database:
        return False
    else:
        return True

def insert_data(result):
    """
    save data from form submitted
    """
    database = shelve.open(DATA_FILE)
    itemKey = md5(result)
    database[itemKey] = result
    database.close()

#判断记录是否命中，需要推送
#keys['keys']都存在于标题中
#并且keys['ignores']都不存在于标题中
def isHit(result,keys):
    for rule in keys:
            keyMeet = True
            for key in rule['keys']:
                if result['title'].lower().find(key) == -1:
                    #如果有一个key不符合，就break
                    keyMeet = False
                    break
            ignoreMeet = True
            for ig in rule['ignores']:
                if result['title'].lower().find(ig) != -1:
                    #如果有一个ignores能早早到，就不符合
                    ignoreMeet = False
                    break
            if keyMeet and ignoreMeet:
                #判断价格，判断渠道
                if rule['src'] == 'all' or result['source'] == rule['src']:                   
                    if rule['min'] == -1 and rule['max'] == -1:
                        return True,rule
                    elif result['rmb_price'] >=int(rule['min']) and result['rmb_price'] <= int( rule['max']):
                        return True,rule
                    else:
                        break;
    return False,None

if __name__ == '__main__':
            
        startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print (startTime+"---------------------------------------------------------")
        #获取用于过滤的key
        keys = read_local_file_keys()
        #获取数据
        resultList = get_real_time_data()
        resultList += get_real_time_data_faxian()
        #循环处理每次获取的数据
        for result in resultList:
            #查看记录是否命中规则
            isHited,matchRule = isHit(result,keys)
            if matchRule is not None:
                result['matched_rule'] =  "%s|%s"%(",".join(matchRule['keys']),",".join(matchRule['ignores']))
            else:
                result['matched_rule'] = ''
            #结果MD5用于去重
            md5Res = md5(result)
            isExisted = False
            if isHited: 
                if not is_data_existed(md5Res):
                    #如果结果命中并且没有推送过
                    #推送微信
                    #push_wechat(result)
                    #插入mongo/mysql
                    insert_data(result)
                    send_mail(result)
                else:
                    isExisted = True
            #Log
            if isHited:
                hitedStr ='\033[1;31mHit!\033[0m'
            else:
                hitedStr = 'Miss'
            print( "%s|%6s|%s|Exist:%5s|%s|%s|￥%s|%s"%(startTime,result['source'],hitedStr,isExisted,result['title'],result['price'],result['rmb_price'],result['page_url']) )
