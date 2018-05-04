import pymysql
import pandas as pd
from sqlalchemy import create_engine

def getData():
    db = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')
    cursor = db.cursor()
    cursor.execute("select * from test_takeAPosition")
    result = cursor.fetchall()
    return result

def getFeild():
    db2 = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')
    cursor2 = db2.cursor()
    cursor2.execute("select COLUMN_NAME from information_schema.COLUMNS where table_name = 'IC_takeAPosition' ")
    result2 = cursor2.fetchall()
    list1 = []
    for i in result2:
        list1.append(i[0])
    list1.insert(0,'kind')
    return list1
def toDb():
    engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/fundamentals_db?charset=utf8")
    result = getData()
    Field = getFeild()
    for m in result:
        print(m)
        list_1 = []
        list_1.append(list(m))
        list_1[0].insert(0,"铝")
        print(list_1)
        df = pd.DataFrame(list_1, columns=Field)
        try:
            df.to_sql(name="CFFEX_takeAPosition", con=engine, if_exists='append', index=False)
        except Exception as e:
            print("有异常" + str(e))

if __name__ == "__main__":
    toDb()