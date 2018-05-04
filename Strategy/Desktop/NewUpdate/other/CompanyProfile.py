import pymysql.cursors
from WindPy import w
import pymysql
import pandas as pd
from sqlalchemy import create_engine
import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

class CompanyProfile():

    def __init__(self):
        pass

    def compare(self,a, b):
        x = []
        if isinstance(a, list) and isinstance(b, list):
            for i in b:
                if i in a:
                    a.remove(i)
                    x.append(i)
            for y in x:
                b.remove(y)
        return a + b


    # 从公司基本信息得到股票代码
    def getWindCodeFromCompany(self):

        conn = pymysql.connect(host='192.168.123.243', user='datadepartment', password='datacode', db='stock_futures_db',charset='utf8')  # db：库名
        cursor = conn.cursor()
        cursor.execute("select windcode from CompanyBasicInfo")
        results = cursor.fetchall()
        result = list(results)
        stockCodeList = []
        for i in result:
            stockCodeList.append(i[0])
        conn.close()
        return stockCodeList


    # 从公司信息数据库得到股票代码
    def getWindCodeFromStockInfo(self):
        conn = pymysql.connect(host='192.168.123.243', user='datadepartment', password='datacode', db='stock_futures_db',charset='utf8')  # db：库名
        cursor = conn.cursor()
        cursor.execute("select windcode from stockinfo")
        results = cursor.fetchall()
        result = list(results)
        # print(result)
        stockCodelist = []
        for i in result:
            stockCodelist.append(i[0])
        conn.close()
        return stockCodelist


    def comparelist(self,a, b):
        if len(a) > len(b):
            return (self.compare(a, b))
        else:
            return (self.compare(b, a))


    def newOrStop(self):
        cList = self.getWindCodeFromCompany()
        sList = self.getWindCodeFromStockInfo()
        list = self.comparelist(cList, sList)
        print(list)
        new = []
        stop = []
        for i in list:
            if i in cList:
                print("下架 " + i)
                stop.append(i)
            else:
                print("上市 " + i)
                new.append(i)
        return new, stop


    def updateDb(self):
        conn = pymysql.connect(host='192.168.123.243', user='datadepartment', password='datacode', db='stock_futures_db',charset='utf8')  # db：库名
        cursor = conn.cursor()
        result = self.newOrStop()
        new = result[0]
        stop = result[1]
        if len(stop) > 0 :
            for i in stop:
                cursor.execute("delete from CompanyBasicInfo where windcode = '" + i + "' ")
                conn.commit()
            print("去除下架股票成功")

        else:
            print("没有公司下架")
        if len(new) >0  :
            for j in new:
                nowtime = time.strftime("%Y-%m-%d", time.localtime())
                engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/stock_futures_db?charset=utf8")
                w.start()
                print(j)
                dset = w.wss(j,"windcode,sec_name,comp_name,comp_name_eng,nature1,founddate,regcapital,chairman,fiscaldate,business,briefing,majorproducttype,majorproductname,employee,province,city,address,office,zipcode,phone,fax,email,website,discloser,registernumber,organizationcode,listingornot,mainproduct,nature",'unit=1', "tradeDate="+nowtime+"")
                list = []
                list2 = []
                for j in dset.Data:
                    list.append(j[0])
                list2.append(list)
                #print(list2)
                df = pd.DataFrame(list2, columns=dset.Fields)
                df.to_sql(name="CompanyBasicInfo", con=engine, if_exists='append', index=False)
                print("新上市公司添加成功")

        else:
            print("没有公司上市")
        conn.close()

    def start(self):
        self.updateDb()



if __name__ == "__main__":

    CompanyProfile().start()


