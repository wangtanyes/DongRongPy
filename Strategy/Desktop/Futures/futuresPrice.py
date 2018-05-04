import pymysql
import re
import pandas as pd
import numpy as np
from WindPy import w
import time
from sqlalchemy import create_engine

nowtime = time.strftime("%Y-%m-%d", time.localtime())
conn = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')
cursor = conn.cursor()
w.start()

def getInfo():
    cursor.execute("select * from futures_Active_contracts_num")
    result = cursor.fetchall()
    return result

def dateSet(windcode):

    code = re.sub("\D", "", windcode)
    n1 = code[0:2]
    print(n1)
    num1 = int(n1) - 1
    n2 = str(num1)
    # print(n2)
    if num1 < 10:
        startYear = "200" + n2
    else:
        startYear = '20' + n2
    endYear = "20" + n1
    n3 = code[2:4]
    print(n3)
    startDate = startYear + "-" + n3 + "-" + "15"
    endDate = endYear + "-" + n3 + "-" + "15"
    return startDate, endDate



def dataToDB():
    result = getInfo()
    #print(result)
    for i in result:
        dateList = dateSet(i[2])
        startDate = dateList[0]
        endDate = dateList[1]
        print(startDate)
        print(endDate)
        engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/fundamentals_db?charset=utf8")
        # 连接数据库
        dset = w.wsd(i[2], "windcode,open,high,low,close,volume,oi,settle", startDate, endDate)
        list1 = []
        list2 = []
        for j in range(len(dset.Times)):
            list1.append(i[0])
            list2.append(i[1])
        s = dset.Data
        s.insert(0, dset.Times)
        s.insert(0, list2)
        s.insert(0, list1)
        print(s)
        h = map(list, zip(*s))
        h1 = list(h)
        df = pd.DataFrame(h1,columns=("exchange", "kind", "datatime", "windcode", "open", "high", "low", "colse", "volume","oi","settle"))
        #print(df)
        pd.io.sql.to_sql(df, "futures_Active_contracts", con=engine, if_exists='append', index=False)

if __name__ == "__main__":
    dataToDB()
