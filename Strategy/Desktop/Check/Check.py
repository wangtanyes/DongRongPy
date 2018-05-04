import pymysql
from datetime import datetime
from datetime import timedelta
import pymysql.cursors
import pandas as pd
import numpy as np
from WindPy import w
from sqlalchemy import create_engine
import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123', db='t1', charset='utf8')  # db：库名
# 创建游标
cursor = conn.cursor()

engine = create_engine("mysql+pymysql://datadepartment:datacode@localhost:3306/t1?charset=utf8")

def getDataFromWind(num):
    # 开启万得
    w.start()
    # 获取15天前的时间
    mytime = datetime.now() - timedelta(days=55)
    fritime = mytime.strftime('%Y-%m-%d')
    print("15天前的日期是"+fritime)

    dset = w.edb(num, fritime, fritime, "Fill=Previous")
    dset.Data.insert(0,dset.Times)
    #print(dset.Data)
    print('实际导出数据的日期是')
    print(dset.Data[0][0])
    if str(fritime) == str(dset.Data[0][0]):
        return dset.Data[1][0]
    else:
        return None

def getDataFromMysql(name):
    mytime = datetime.now() - timedelta(days=55)
    fritime = mytime.strftime('%Y-%m-%d')

    print(name)
    print(fritime)
    #从数据库查询十五天前dataname 的value值

    cursor.execute("select * from detail_copy1 where dataname='" + name + "' and datatime = '" + fritime + "'")
    results = cursor.fetchall()
    print(results)
    #print(results[0][3])
    if len(results)>0:
        return results[0][3]
    else:
        return None
    # 提交
    conn.commit()
    # 关闭指针对象
    #cursor.close()
    # 关闭连接对象
    #conn.close()

def updateDataToMysql(dataname,data):

    mytime = datetime.now() - timedelta(days=55)
    fritime = mytime.strftime('%Y-%m-%d')
    # 获取十五天前的时间
    print("15天前的日期是"+fritime)
    cursor.execute("update detail_copy1 set value = '"+data+"' where dataname='" + dataname + "' and datatime = '" + fritime + "'")


    conn.commit()



def execute(num,dataname):

    mytime = datetime.now() - timedelta(days=55)
    fritime = mytime.strftime('%Y-%m-%d')
    # 获取15天前的日期
    print("15天前的日期是"+fritime)


    engine = create_engine("mysql+pymysql://root:123@localhost:3306/t1?charset=utf8")
    # 连接数据库
    w.start()
    # 开启万得
    nowtime = time.strftime('%Y-%m-%d',time.localtime())
    # 获取当前的时间
    dset = w.edb(num , fritime,fritime,"Fill=Previous")
    s = dset.Data
    s.insert(0,dset.Times)
    #添加字段
    s.insert(0,[dataname])
    s.insert(2,[3])
    s.append([nowtime])
    h = map(list,zip(s[0],s[1],s[2],s[3],s[4]))
    # 通过zip将[1,2,3],[a,b,c]转换为[[1,a],[2,b],[3,c]]
    h1 = list(h)
    if (h1[0][3] is None):
        print(dataname+" ,it's an empty value,no inserted")
    else:
        df = pd.DataFrame(h1,columns=("dataname","datatime","datatype","value","introtime"))
        try:
            df.to_sql(name="detail_copy1",con=engine,if_exists='append',index= False)
        except:
            print("添补数据有误")

def getDataNum():
    cursor.execute("select * from datacode")
    results = cursor.fetchall()
    result = list(results)
    return result

    conn.commit()

def start ():

    try:
        result = getDataNum()
    except:
        print('get num fail')

    for r in result:
        print('______________________________________________________________________________________')
        print('--------------------------------------------------------------------------------------')
        #打印datacode表中的字段
        print(r)
        # 调用函数getDataFromWind得到wind15天前数据
        try:
            data = getDataFromWind(r[2])
        except:
            print('get data from wind fail')
        print('data值是')
        print(data)

        # 调用函数getDataFromMysql得到数据库15天前的数据
        try:
            values = getDataFromMysql(r[0])
        except:
            print('get data from mysql fail')
        print('values值是')
        print(values)

        #如果data是None说明当天没数据
        if data == None:
            print('today has no day')
        else:
            if values !=None and values != None:
                data = str(data)
                #如果数据库的数据和wind的数据一样说明数据没问题
                if float(data) == float(values):
                    print("the data has no question")
                #如果数据库和wind的数据不同更新wind的数据到数据库
                else:
                    print('更新数据')
                    '''try:'''
                    updateDataToMysql(r[0], data)
                    '''except:
                        print('update data to mysql fail')'''

            #如果数据库的数据为None而wind的有数据则插入数据到数据库
            else:
                print('添补数据')
                data = str(data)
                try:
                    execute(r[2], r[0])
                except:
                    print(" wind insert to mysql fail")


if __name__ == '__main__':

    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG

    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)
    print('start to do it')
    sched = BlockingScheduler()
    sched.add_job(start, "cron", month="*", day="*", hour="1", minute="40")


    sched.start()
