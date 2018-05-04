import pymysql.cursors
import pandas as pd
import numpy as np
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from WindPy import w
from sqlalchemy import create_engine
import time
from pandas import Series,DataFrame,np


w.start()

#nowtime = time.strftime("%Y-%m-%d", time.localtime())

conn = pymysql.connect(host='192.168.123.166',user='root',password='123',db='gupiao_db',charset='utf8')# 创建游标
cursor = conn.cursor()

dict = {"fixed_investments_num":"fixed_investments"}
def update():

    for n in dict.keys():
        print(n)
        print(dict[n])
        cursor.execute("select * from "+ n +" ")
        results = cursor.fetchall()
        result = list(results)
        for i in result:
            print(i[0])
            print(i[1])
            dest = w.edb(i[1], "2017-8-20", "2017-8-20","Fill=Previous")
            print(dest.Times)
            dest.Data.insert(0,dest.Times)
            s = dest.Data
            h = map(list,zip(*s))
            h1 = list(h)
            print(h1)
            for j in h1:
                print(j[0])
                print(j[1])
                data = str(j[1])
                datelist = str(j[0]).split('-')
                print(datelist)
                date = datelist[0]+'-'+datelist[1]
                print(date)
                a = dict[n]
                #print("UPDATE "+ a +" set `" + i[0] + "`='" + data + "' where datetime='" +date+ "'")
                cursor.execute("UPDATE "+ a +" set `" + i[0] + "`='" + data + "' where datetime='" +date+ "'")

            conn.commit()
    conn.close()
    print('insert ok')

def start():
    update()

if __name__=="__main__":

    start()
    '''log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG

    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)
    print('start to do it')
    sched = BlockingScheduler()
    sched.add_job(start, "cron", month="*", day="*", hour="23", minute="40")
    #sched.add_job(week, "cron", month="*", day="*", hour="23", minute="40")
    #sched.add_job(onlyWeek, "cron", day_of_week='sun', day="*", hour="23", minute="59")
    sched.start()'''
