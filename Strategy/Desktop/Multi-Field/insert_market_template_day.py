import pymysql.cursors
import pandas as pd
import numpy as np
from WindPy import w
from sqlalchemy import create_engine
import time
from pandas import Series,DataFrame,np
w.start()

conn = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')# 创建游标
cursor = conn.cursor()
cursor.execute("select * from index_num")
results = cursor.fetchall()
result = list(results)
list1 = []
count = 0
nowtime = time.strftime("%Y-%m-%d", time.localtime())



for i in result:
    count += 1
    print(i[0])
    dest = w.edb(i[1], "2005-01-01", nowtime,"Fill=Previous")
    dest.Data.insert(0,dest.Times)
    s = dest.Data
    h = map(list,zip(*s))
    h1 = list(h)
    for j in h1:
        print("count是- - - - - - - - - - -"+str(count)+"- - - - - - - - - - - - -")
        print(j[0])
        print(j[1])
        data = str(j[1])
        date = str(j[0])
        cursor.execute("UPDATE index_1 set `" + i[0] + "`='" + data + "' where datetime='" + date+ "'")
    conn.commit()
conn.close()
print('insert ok')
