from py2neo import Graph, Node, Relationship,Path
from WindPy import w
from sqlalchemy import create_engine
from pandas import Series,DataFrame,np
from collections import OrderedDict
import pandas as pd
import pymysql
import time


conn = pymysql.connect(host='192.168.123.243',user='root',password='xunji-@sqlcode',db='fundamentals_db',charset='utf8')  # db：库名
# 创建游标
cursor = conn.cursor()
def getDate():
    enddate = ["2018-01-17", "2017-01-16", "2016-01-15", "2015-01-14", "2014-01-13", "2013-01-12", "2012-01-11",
               "2011-01-10", "2010-01-09",
               "2009-01-08", "2008-01-07", "2007-01-06", "2006-01-05", "2005-01-04", "2004-01-03", "2003-01-02"]
    startdate = []
    for i in enddate:
        list = i.split('-')
        lastyear = str(int(list[0]) - 1)
        lastTime = lastyear + "-" + list[1] + "-" + list[2]
        startdate.append(lastTime)
    return startdate,enddate

def getWindCode():
    cursor.execute("select * from takeAPosition_num_copy")
    result = cursor.fetchall()
    kindList = []
    codeList = []
    for i in result:
        kindList.append(i[0])
        codeList.append(i[1])
    return kindList,codeList


def dataToDB():
    dateList = getDate()
    kindCodeList = getWindCode()
    for kind ,code in zip(kindCodeList[0],kindCodeList[1]):

        for start, end  in zip(dateList[0], dateList[1]):
            print("品种" + kind)
            print("万得代码" + code)
            print("开始时间" + start)
            print("结束时间" + end)

            #engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/fundamentals_db?charset=utf8")
            engine = create_engine("mysql+pymysql://root:xunji-@sqlcode@192.168.123.243:3306/fundamentals_db?charset=utf8")
            w.start()
            #dset = w.wsd(stockCode,"windcode,comp_name,comp_name_eng,nature1,founddate,regcapital,chairman,fiscaldate,business,briefing,majorproducttype,majorproductname,employee,province,city,address,office,zipcode,phone,fax,email,website,discloser,registernumber,abstract,organizationcode,report_cur,listingornot,issuershortened,mainproduct,compprename,nature","2017-11-29", "2017-11-29", "unit=1")
            dset = w.wset("futureoir","startdate="+start+";enddate="+end+";varity="+code+";order_by=long;ranks=all")
            print(dset.Data)
            if len(dset.Data)>0:
                list_1 = []
                for i in range(len(dset.Data[0])):
                    list_1.append(kind)
                s = dset.Data
                s.insert(0,list_1)
                h = map(list, zip(*s))
                h1 = list(h)
                list_2 = []
                for j in dset.Fields:
                    list_2.append(j)
                list_2.insert(0,'kind')
                df = pd.DataFrame(h1, columns=list_2)
                pd.io.sql.to_sql(df, "takeAPosition", con=engine, if_exists='append', index=False)
if __name__ == "__main__":
    dataToDB()