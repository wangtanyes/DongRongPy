import pymysql.cursors
import pandas as pd
import numpy as np
from WindPy import w
from sqlalchemy import create_engine
import time
from pandas import Series,DataFrame,np

class ForeignExchangeAndRateOfInterest():

    def __init__(self):
        pass

    def updateData(self,db,db_num,startDate,endDate):
        w.start()
        conn = pymysql.connect(host='192.168.123.243', user='datadepartment', password='datacode', db='stock_futures_db',charset='utf8')  # 创建游标
        cursor = conn.cursor()
        cursor.execute("select * from "+db_num+"")
        results = cursor.fetchall()
        result = list(results)
        count = 0
        for i in result:
            count += 1
            print(i[0])
            dest = w.wsd(i[1], "close", startDate, endDate, "")
            dest.Data.insert(0,dest.Times)
            s = dest.Data
            h = map(list,zip(*s))
            h1 = list(h)
            for j in h1:
                print(db)
                print("count是- - - - - - - - - - -"+str(count)+"- - - - - - - - - - - - -")
                print(j[0])
                print(j[1])
                data = str(j[1])
                date = str(j[0])
                cursor.execute("UPDATE "+db+" set `" + i[0] + "`='" + data + "' where datatime='" + date+ "'")
            conn.commit()
        conn.close()
        print('insert ok')

    def start(self,nowtime):
        dbs = ['foreignExchange','rateOfInterest']
        for db in dbs:
            db_num = db+"_num"
            self.updateData(db,db_num,nowtime,nowtime)

if __name__ == '__main__':
    ForeignExchangeAndRateOfInterest().start()