from WindPy import w
from sqlalchemy import create_engine
import pandas as pd
import pymysql
import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

class ZX_index():

    def getStockCode(self,Table ,numTable,startDate,endDate):
        conn = pymysql.connect(host='192.168.123.243', user='root', password='xunji-@sqlcode', db='stock_futures_db',charset='utf8')  # db：库名
        cursor = conn.cursor()
        cursor.execute("select * from "+numTable+" ")
        results = cursor.fetchall()
        result = list(results)
        self.dataToDB(Table,result,startDate,endDate)
        conn.close()

    def dataToDB(self,Table,result,startDate,endDate):

        for i in result:
            stockCode = i[1]
            engine = create_engine("mysql+pymysql://root:xunji-@sqlcode@192.168.123.243:3306/stock_futures_db?charset=utf8")
            w.start()
            dset = w.wsd(stockCode, "windcode,open,high,low,close,volume", startDate, endDate, "")
            print(dset.Data)
            nameList = []
            for j in range(len(dset.Times)):
                nameList.append(i[0])
            dset.Data.insert(0,dset.Times)
            dset.Data.insert(0,nameList)
            s = dset.Data
            h = map(list, zip(*s))  # 通过zip将[1,2,3],[a,b,c]转换为[[1,a],[2,b],[3,c]]
            h1 = list(h)
            dset.Fields.insert(0,"datatime")
            if Table == 'industry_index_two':
                dset.Fields.insert(0,"classify_two")
            else:
                dset.Fields.insert(0, "classify_three")
            df = pd.DataFrame(h1, columns=dset.Fields)
            try:
                df.to_sql(name=Table, con=engine, if_exists='append', index=False)
            except Exception as e :
                print(e)

    def start(self,nowtime):
        dbList = ["industry_index_two","industry_index_three"]
        for i in dbList:
            #print("当前数据库:"+ i)
            self.getStockCode(i,i+'_num',nowtime,nowtime)



if __name__ == "__main__":
        ZX_index().start()

        # log = logging.getLogger('apscheduler.executors.default')
        # log.setLevel(logging.INFO)  # DEBUG
        #
        # fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        # h = logging.StreamHandler()
        # h.setFormatter(fmt)
        # log.addHandler(h)
        # print('start to do it')
        # sched = BlockingScheduler()
        #
        # sched.add_job(start, "cron", month="*", day="*", hour="18", minute="50")
        #
        # sched.start()
