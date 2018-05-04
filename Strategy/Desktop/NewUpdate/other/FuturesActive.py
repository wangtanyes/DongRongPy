import pymysql
from WindPy import w
from sqlalchemy import create_engine
import pandas as pd
import time


class FuturesActive():

    def __init__(self):
        pass

    def getNum(self,startDate,endDate):
        conn = pymysql.connect(host='192.168.123.243', user='datadepartment', password='datacode', db='stock_futures_db',charset='utf8')  # 创建游标
        cursor = conn.cursor()
        cursor.execute("select * from futures_Active_contracts_num")
        result = cursor.fetchall()
        self.upDataToDB(result,startDate,endDate)
        conn.close()

    def upDataToDB(self,result,startDate,endDate):

        for i in result:
            print(i[0])
            print(i[1])
            # 连接数据库
            w.start()
            dset = w.wsd(i[1], "open,high,low,close,volume,amt,oi,settle", startDate, endDate)
            list1 = []
            for j in range(len(dset.Times)):
                list1.append(i[0])
            s = dset.Data
            s.insert(0, dset.Times)
            s.insert(0, list1)
            print(s)
            h = map(list, zip(*s))
            h1 = list(h)
            df = pd.DataFrame(h1, columns=(
            "kind", "datatime", "open", "high", "low", "colse", "volume", "amt", "oi", "settle"))
            print(df)
            try:
                engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/stock_futures_db?charset=utf8")
                pd.io.sql.to_sql(df, "futures_Active_contracts", con=engine, if_exists='append', index=False)
            except Exception as e:
                print("有异常" + str(e))

    def start(self,nowtime):

        self.getNum(nowtime,nowtime)


if __name__ == '__main__':
    FuturesActive().start()