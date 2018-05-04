from WindPy import w
from sqlalchemy import create_engine
import pandas as pd
import pymysql
import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

class TakeAPosition():
    """持仓数据"""

    def getWindCode(self,startDate,endDate):
        conn = pymysql.connect(host='192.168.123.243', user='root', password='xunji-@sqlcode', db='stock_futures_db',charset='utf8')  # db：库名
        cursor = conn.cursor()    # 创建游标
        cursor.execute("select * from takeAPosition_num")
        result = cursor.fetchall()
        kindList = []
        codeList = []
        for i in result:
            kindList.append(i[0])
            codeList.append(i[1])
        self.dataToDB(kindList,codeList,startDate,endDate)
        conn.close()

    def dataToDB(self,kindList,codeList,startDate,endDate):

        for kind ,code in zip(kindList,codeList):
            print("品种" + kind)
            print("万得代码" + code)
            engine = create_engine("mysql+pymysql://root:xunji-@sqlcode@192.168.123.243:3306/stock_futures_db?charset=utf8")
            w.start()
            dset = w.wset("futureoir","startdate="+startDate+";enddate="+endDate+";varity="+code+";order_by=long;ranks=all")
            print(dset.Data)
            if len(dset.Data)>0:
                list_1 = []
                for i in range(len(dset.Data[0])):
                    list_1.append(kind)
                s = dset.Data
                s.insert(0,list_1)
                h = map(list, zip(*s))
                h1 = list(h)
                list_2 = []
                for j in dset.Fields:
                    list_2.append(j)
                list_2.insert(0,'kind')
                df = pd.DataFrame(h1, columns=list_2)
                pd.io.sql.to_sql(df, "takeAPosition", con=engine, if_exists='append', index=False)


    def start (self,nowtime):

        self.getWindCode(nowtime,nowtime)

if __name__ == "__main__":

    nowtime = time.strftime("%Y-%m-%d", time.localtime())
    # nowtime = '2018-03-14'
    TakeAPosition().start(nowtime)
