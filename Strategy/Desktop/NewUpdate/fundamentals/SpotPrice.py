import pymysql
from WindPy import w
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
from datetime import timedelta

class SpotPrice():
    """价格数据"""


    def __init__(self):
        pass

    def getNum (self,dbName,numDbName,startDate,endDate):
        conn = pymysql.connect(host='192.168.123.243', user='datadepartment', password='datacode', db='stock_futures_db',charset='utf8')  # 创建游标
        cursor = conn.cursor()
        cursor.execute("select * from "+numDbName+"")
        result = cursor.fetchall()
        self.updateDate(dbName,result,startDate,endDate)
        conn.close()

    def updateDate(self,dbName,result,startDate,endDate):
        engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/stock_futures_db?charset=utf8")
        count = 0
        for i in result:
            count = count + 1
            print("")
            print(count)
            print("当前数据库:   "+dbName)
            nameList = []
            w.start()
            dset = w.edb(i[1], startDate,endDate, "Fill=Previous")
            s = dset.Data
            for n in range(len(s[0])):
                nameList.append(i[0])
            s.insert(0, dset.Times)
            s.insert(0, nameList)
            h = map(list, zip(*s))  # 通过zip将[1,2,3],[a,b,c]转换为[[1,a],[2,b],[3,c]]
            h1 = list(h)
            print(h1)
            for m in h1 :
                if 'quota exceeded' in str(m[2]):
                    print("数据超限")
                    return
                list_1 = []
                list_1.append(m)
                df = pd.DataFrame(list_1, columns=("dataname", "datatime", "datavalue"))
                try:
                    df.to_sql(name=dbName, con=engine, if_exists='append', index=False)
                except Exception as e:
                    if 'PRIMARY' in str(e):
                        print("                    主键重复                   ")
                    elif 'quota exceeded'in str(e):
                        print("数据超限")
                        return
                    else:
                        print(e)
                print("---------------------------------------------------------")

    def start(self,fritime):

        print("昨天的日期是" + fritime)
        #fritime = '2018-03-14'
        self.getNum("spotPrice","spotPrice_num",fritime,fritime)



if __name__ == "__main__":

    SpotPrice().start()


