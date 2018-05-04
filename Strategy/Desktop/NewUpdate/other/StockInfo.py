import pymysql.cursors
import pandas as pd
import numpy as np
from WindPy import w
from sqlalchemy import create_engine
import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

class StockInfo():
    """股票基本资料"""

    def __init__(self):
        pass


    def createTable(self,nowtime):

        w.start()
        dset = w.wset("sectorconstituent","date="+nowtime+";sectorid=a001010100000000")
        s = dset.Data
        h = map(list,zip(*s)) #通过zip将[1,2,3],[a,b,c]转换为[[1,a],[2,b],[3,c]]
        h1 = list(h)
        df = pd.DataFrame(h1,columns=("datatime","windcode","stockname"))
        print(df)
        engine = create_engine("mysql+pymysql://root:xunji-@sqlcode@192.168.123.243:3306/stock_futures_db?charset=utf8")
        pd.io.sql.to_sql(df,"stockinfo", con=engine, if_exists='replace',index = False)

    def start(self,nowtime):

        self.createTable(nowtime)
        print("update Ok")


if __name__ == "__main__":
    nowtime = time.strftime("%Y-%m-%d", time.localtime())
    # nowtime = '2018-03-14'
    StockInfo().start(nowtime)