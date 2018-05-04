from WindPy import w
import pandas as pd
import pymysql.cursors
from sqlalchemy import create_engine

class TTM():

    def __init__(self):
        pass

    def getFactor(self):
        w.start()
        conn = pymysql.connect(host='192.168.123.243', user='datadepartment', password='datacode', db='stock_futures_db',charset='utf8')  # db：库名
        cursor = conn.cursor()
        cursor.execute("SELECT ﻿factor FROM `STOCK_FACTOR_CONTRAST`")
        factors = cursor.fetchall()
        conn.close()
        return factors

    def getStockCode(self):
        conn = pymysql.connect(host='192.168.123.243', user='datadepartment', password='datacode', db='stock_futures_db',charset='utf8')  # db：库名
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT `code` FROM `STOCK_FACTOR`")
        stockCodes = cursor.fetchall()
        conn.close()
        return stockCodes

    def UpdateTable(self,date):
        factors = self.getFactor()
        stockCodes = self.getStockCode()
        for stockCode in stockCodes:
            for factor in factors:

                dset = w.wss(stockCode[0],factor[0],"rptDate="+date+"")
                datas = dset.Data
                datas[0].insert(0,date)
                datas[0].insert(0,factor[0])
                datas[0].insert(0,stockCode[0])
                print(datas)
                df = pd.DataFrame(datas, columns=("code", "factor", "date","value"))
                try:
                    engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/stock_futures_db?charset=utf8")
                    df.to_sql(name="STOCK_FACTOR", con=engine, if_exists='append', index=False)
                except Exception as e :
                    print(e)

    def start(self,nowtime):
        self.UpdateTable(nowtime)

if __name__ == '__main__':

    TTM().start()