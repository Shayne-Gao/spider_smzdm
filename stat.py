#!/usr/bin/env python
# encoding: utf-8
# 访问 http://tool.lu/pyc/ 查看更多信息
import json
import urlparse
import HTMLParser
import ConfigParser
import os
import urllib
import time
import MySQLdb
import sys
##获取每个爬虫关键字每日统计的数量
class LifeDB:
    db = None
    cursor = None
    dictCursor = None
    REC_TYPE_COST = 0
    REC_TYPE_INCOME = 1
    REC_VALID_TRUE = 1
    REC_VALID_FALSE = 0
    
    def __init__(self):
        self.db = MySQLdb.connect('localhost', 'root', 'IWLX8IS12Rl', 'life', charset = 'utf8')
        self.cursor = self.db.cursor()
        self.dictCursor = self.db.cursor(MySQLdb.cursors.DictCursor)
    
    def queryBySql(self, sql,cursorType='default'):
        try:
            if cursorType =='dict':
                thisCursor = self.dictCursor
            else:
                thisCursor = self.cursor
            thisCursor.execute(sql)
            self.db.commit()
            result = thisCursor.fetchall()
            return result
        except Exception as e:
            print 'MYSQL ERROR:', str(e)
            print sql
            self.db.rollback()

    def getSMZDMstat(self,limitdays):
        sql = """SELECT matched_rule,DATE_FORMAT(create_time,'%%Y-%%m-%%d') AS days,COUNT(*) COUNT  
FROM smzdm_record 
where  DATE_SUB(CURDATE(), INTERVAL %s DAY) <= date(create_time)  
GROUP BY matched_rule,days 
order by matched_rule,create_time"""%(str(limitdays))
#        print sql
        res = self.queryBySql(sql,'dict');
        return res

    def getXIANYUstat(self,limitdays):
        sql = """SELECT keywords,DATE_FORMAT(ctime,'%%Y-%%m-%%d') AS days,COUNT(*) COUNT  
FROM xianyu_record 
where  DATE_SUB(CURDATE(), INTERVAL %s DAY) <= date(ctime)  
GROUP BY keywords,days 
order by keywords,ctime"""%(str(limitdays))
#        print sql
        res = self.queryBySql(sql,'dict');
        return res


    def Output(self,days):
        print '-------SMZDM---------'
        smzdmRes = self.getSMZDMstat(days)
        for r in smzdmRes:
            print "%s\t%10s\t%s"%(r['days'],r['matched_rule'][0:5],r['COUNT'])
   
        print '-------XIANYU---------'
        xyRes = self.getXIANYUstat(days)
        for r in xyRes:
            print "%s\t%10s\t%s"%(r['days'],r['keywords'][0:5],r['COUNT'])
if  len(sys.argv)<2:
    print "usage: [limit_days]"
    print "limit_days: 0 for today"
    exit()


LifeDB().Output(sys.argv[1])
