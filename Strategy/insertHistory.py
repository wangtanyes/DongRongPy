import pymysql
from WindPy import w
from sqlalchemy import create_engine
import pandas as pd
import time

conn = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')# 创建游标
cursor = conn.cursor()
w.start()
engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/fundamentals_db?charset=utf8")


def getNum ():
    cursor.execute("select * from financialIndex_fixedInvestment_num")
    result = cursor.fetchall()
    return result

def updateDate():
    nowtime = time.strftime("%Y-%m-%d", time.localtime())
    result = getNum()
    for i in result:
        #print(i[0])
        #print(i[1])

        nameList = []
        dset = w.edb(i[1], "2017-11-30",nowtime, "Fill=Previous")
        s = dset.Data
        #print(s)
        #print(dset.Times)

        for n in range(len(s[0])):
            nameList.append(i[0])
        s.insert(0, dset.Times)
        s.insert(0, nameList)
        h = map(list, zip(*s))  # 通过zip将[1,2,3],[a,b,c]转换为[[1,a],[2,b],[3,c]]
        h1 = list(h)
        #print(h1)
        for m in h1 :
            list_1 = []
            list_1.append(m)
            print(list_1)
            df = pd.DataFrame(list_1, columns=("dataname", "datatime", "datavalue"))
            try:
                df.to_sql(name="financialIndex_fixedInvestment", con=engine, if_exists='append', index=False)
            except Exception as e:
                print("有异常"+ str(e))

if __name__ == "__main__":

    updateDate()