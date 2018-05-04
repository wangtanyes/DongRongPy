import pymysql.cursors
import pandas as pd
import numpy as np
from WindPy import w
from sqlalchemy import create_engine
import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
'''
每年,每月,每日,每周,每季,每周定时获取万得数据到MySQL
相关得MySQL表:detail(最终数据存放位置),datacode(获取周,月,日等得分类代码)
'''
class Dataerror(RuntimeError):
    #异常类
    def __init__(self, arg):
        self.args = arg
    def __str__(self):
        return repr(self.value)


'''
连接数据库查询
:return: 
'''
config = {
    'host':'192.168.123.243',
    'port': 3306,
    'user': 'datadepartment',
    'password': 'datacode',
    'db': 'futures_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}
db = pymysql.connect(**config)
cursor = db.cursor()
nowtime = time.strftime("%Y-%m-%d", time.localtime())

def execute(arg1,arg2):
    '''
    arg1参数指代 代码编号
    arg2参数指代种类
    :return: 
    '''
    engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/futures_db?charset=utf8")
    # 连接数据库
    w.start()
    # 开启万得

    #获取当前的时间
    dset = w.edb(arg1, "2017-09-30","2017-09-30","Fill=Previous")
    dset.Data.insert(0,dset.Times)
    s = dset.Data
    #追加
    dset.Data.insert(0,[arg2])
    dset.Data.insert(2,[3])
    dset.Data.append(["2017-09-30"])
    h = map(list,zip(s[0],s[1],s[2],s[3],s[4]))
    #通过zip将[1,2,3],[a,b,c]转换为[[1,a],[2,b],[3,c]]
    h1 = list(h)
    if (h1[0][3] is None):
        print(arg2+" ,it's an empty value,no inserted")
    else:
        df = pd.DataFrame(h1,columns=("dataname","datatime","datatype","value","introtime"))
        try:
            df.to_sql(name="detail",con=engine,if_exists='append',index= False)
        except:
            print(h1[0][0]+"no update")

def everymonth():
    cursor.execute("select * from datacode")
    results = cursor.fetchall()
    result = list(results)
    for r in result:
        if (r['frequency']) == '月':
            try:
                execute(r['num'],r['dataname'])
            except Dataerror as e:
                print("no data")
                e.value
        else:
            pass
    print(nowtime +"everymonth inserted success")

def everyquartites():
    cursor.execute("select * from datacode")
    results = cursor.fetchall()
    result = list(results)
    for r in result:
        if (r['frequency']) == '季':
            try:
                execute(r['num'], r['dataname'])
            except Dataerror as e:
                e.value
        else:
            pass
    print(nowtime +"quarties inserted success")

def everyday():
    cursor.execute("select * from datacode")
    results = cursor.fetchall()
    result = list(results)
    for r in result:
        if (r['frequency']) == '日':
            try:
                execute(r['num'], r['dataname'])
            except Dataerror as e:
                e.value
        else:
            pass
    print( nowtime + "day inserted success")

def everyweek():
    cursor.execute("select * from datacode")
    results = cursor.fetchall()
    result = list(results)
    for r in result:
        if (r['frequency']) == '周':
            try:
                execute(r['num'], r['dataname'])
            except Dataerror as e:
                e.value
        else:
            pass
    print(nowtime + "week inserted success")

def everyyear():
    cursor.execute("select * from datacode")
    results = cursor.fetchall()
    result = list(results)
    for r in result:
        if (r['frequency']) == '年':
            try:
                execute(r['num'], r['dataname'])
            except Dataerror as e:
                e.value
        else:
            pass
    print(nowtime + "year inserted success")

if __name__ == '__main__':

    log = logging.getLogger('apscheduler.executors.default')
    log.setLevel(logging.INFO)  # DEBUG

    fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    h = logging.StreamHandler()
    h.setFormatter(fmt)
    log.addHandler(h)
    print('start to do it')
    sched = BlockingScheduler()

    # of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
    sched.add_job(everyday,"cron",month="*",day="*",hour="15",minute="45")
    #cron调度日度任务
    sched.add_job(everymonth,"cron",month="*", day="28,29,30,31", hour="15", minute="50")
    #Cron调用月度任务
    sched.add_job(everyquartites, "cron", month="3,6,9,12",day="28,29,30,31",hour="16", minute="00")
    #Cron调用季度任务
    sched.add_job(everyweek, "cron", month="*",day="*",hour="16", minute="05")
    #Cron调用周度任务
    sched.add_job(everyyear, "cron", month="11,12,1",day="28,29,30,31",hour="16", minute="10")
    #Cron调用年度任务
    sched.start()

