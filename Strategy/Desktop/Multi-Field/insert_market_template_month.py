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
cursor.execute("select * from print_steel_num ")
results = cursor.fetchall()
result = list(results)
list1 = []
for i in result:
    print(i[0])
    print(i[1])
    dest = w.edb(i[1], "2008-11-24", "2018-12-08","Fill=Previous")
    dest.Data.insert(0,dest.Times)
    s = dest.Data
    h = map(list,zip(*s))
    h1 = list(h)
    for j in h1:
        print(j[0])
        print(j[1])
        data = str(j[1])
        datelist = str(j[0]).split('-')
        print(datelist)
        date = datelist[0]+'-'+datelist[1]
        print(date)
        cursor.execute("UPDATE print_steel_export_import2 set `" + i[0] + "`='" + data + "' where datetime='" + date+ "'")

    conn.commit()
conn.close()
print('insert ok')
