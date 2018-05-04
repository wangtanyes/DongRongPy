import pymysql
from WindPy import w
from sqlalchemy import create_engine
import pandas as pd
import time


w.start()

def getNum ():
    """从表格中获得windCode"""
    conn = pymysql.connect(host='192.168.123.243', user='datadepartment', password='datacode', db='stock_futures_db',charset='utf8')  # 创建游标
    cursor = conn.cursor()
    cursor.execute("select * from test_num")
    result = cursor.fetchall()
    return result

def updateDate():
    """将数据导入到数据库"""
    nowtime = time.strftime("%Y-%m-%d", time.localtime())
    result = getNum()
    for i in result:
        nameList = []
        dset = w.edb(i[1],"2005-01-01",nowtime, "Fill=Previous")
        s = dset.Data
        print(s)
        for n in range(len(s[0])):
            nameList.append(i[0])
        s.insert(0, dset.Times)
        s.insert(0, nameList)
        h = map(list, zip(*s))  # 通过zip将[1,2,3],[a,b,c]转换为[[1,a],[2,b],[3,c]]
        h1 = list(h)
        print(h1)
        for m in h1 :
            list_1 = []
            list_1.append(m)
            df = pd.DataFrame(list_1, columns=("dataname", "datatime", "datavalue"))
            try:
                engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/stock_futures_db?charset=utf8")
                df.to_sql(name="macroeconomic", con=engine, if_exists='append', index=False)
            except Exception as e:
                print("有异常"+ str(e))

if __name__ == "__main__":

    updateDate()