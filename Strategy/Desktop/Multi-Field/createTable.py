import pymysql.cursors
import pandas as pd
import numpy as np
from WindPy import w
from sqlalchemy import create_engine
import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

conn = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')# 创建游标

cursor = conn.cursor()

def getStockCode():
    cursor.execute("select * from buildingMaterials_boom_num ")
    results = cursor.fetchall()
    result = list(results)
    return result
if __name__=='__main__':
    engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/fundamentals_db?charset=utf8")
    result = getStockCode()
    list1 = []
    list2 = []
    for i in result:
        print(i[0])
        list1.append(i[0])
    #print(list1)
    list1.insert(0,'datetime')
    list2.append(list1)
    #print(list2)
    print(len(list2[0]))
    df = pd.DataFrame( columns=list1)
    print(df)
    # try:
    df.to_sql(name="buildingMaterials_boom", con=engine, if_exists='append', index=False)