import pymysql
import pandas as pd
from WindPy import w
import time
from sqlalchemy import create_engine
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
w.start()
class FuturesVar():

    def __init__(self):
        pass

    def f_all_SHFE(self,nowtime):
        date = str(nowtime)
        dateList = date.split('-')
        if int(dateList[2]) > 14:

            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))
                    d = d - 1
            d = int(dateList[1])
            for m in range(12 - int(dateList[1])):
                if d < 12:
                    d = d + 1
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))

            kindList1 = ["CU", "AU", "AG", "NI", "ZN", "SN", "AL", "PB"]
            kindList2 = ["铜", "金", "银", "镍", "锌", "锡", "铝", "铅"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                codeList = []
                for j in list1:
                    # print(k+str(int(dateList[0])+1)[2:4]+j+".SHF")
                    codeList.append(k1 + str(int(dateList[0]) + 1)[2:4] + j + ".SHF")

                for h in list2:
                    # print(k+str(int(dateList[0]))[2:4]+h+".SHF")
                    codeList.append(k1 + str(int(dateList[0]))[2:4] + h + ".SHF")
                print(codeList)
                print(codeList)
                print(k2)
                allList.append(codeList)
            return allList, kindList2
        else:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                d = d - 1
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))

            d = int(dateList[1])
            for m in range(13 - int(dateList[1])):
                if d < 13:
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))
                    d = d + 1

            kindList1 = ["CU", "AU", "AG", "NI", "ZN", "SN", "AL", "PB"]
            kindList2 = ["铜", "金", "银", "镍", "锌", "锡", "铝", "铅"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                codeList = []
                for j in list1:
                    # print(k+str(int(dateList[0])+1)[2:4]+j+".SHF")
                    codeList.append(k1 + str(int(dateList[0]) + 1)[2:4] + j + ".SHF")

                for h in list2:
                    # print(k+str(int(dateList[0]))[2:4]+h+".SHF")
                    codeList.append(k1 + str(int(dateList[0]))[2:4] + h + ".SHF")
                print(codeList)
                print(codeList)
                print(k2)
                allList.append(codeList)
            return allList, kindList2


    def f_oneFiveNine_SHFE(self,nowtime):
        date = str(nowtime)
        dateList = date.split('-')
        print(dateList[2])

        if int(dateList[2]) > 14:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))
                    d = d - 1
            d = int(dateList[1])
            for m in range(12 - int(dateList[1])):
                if d < 12:
                    d = d + 1
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))

            kindList1 = ["RU"]
            kindList2 = ["橡胶"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                one_five_nine = []
                for j in list1:
                    if int(j) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]) + 1)[2:4] + j + ".SHF")

                for h in list2:
                    if int(h) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]))[2:4] + h + ".SHF")
                print(one_five_nine)
                print(k2)
                allList.append(one_five_nine)
            return allList, kindList2
        else:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                d = d - 1
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))

            d = int(dateList[1])
            for m in range(13 - int(dateList[1])):
                if d < 13:
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))
                    d = d + 1

            kindList1 = ["RU"]
            kindList2 = ["橡胶"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                one_five_nine = []
                for j in list1:
                    if int(j) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]) + 1)[2:4] + j + ".SHF")

                for h in list2:
                    if int(h) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]))[2:4] + h + ".SHF")
                print(one_five_nine)
                print(k2)
                allList.append(one_five_nine)
            return allList, kindList2

    def f_oneFiveTen_SHFE(self,nowtime):

        date = str(nowtime)
        dateList = date.split('-')
        print(dateList[2])

        if int(dateList[2]) > 14:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))
                    d = d - 1
            d = int(dateList[1])
            for m in range(12 - int(dateList[1])):
                if d < 12:
                    d = d + 1
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))

            kindList1 = ["RB", "HC"]
            kindList2 = ["螺纹钢", "热轧卷板"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                one_five_ten = []
                for j in list1:
                    if int(j) in [1, 5, 10]:
                        one_five_ten.append(k1 + str(int(dateList[0]) + 1)[2:4] + j + ".SHF")

                for h in list2:
                    if int(h) in [1, 5, 10]:
                        one_five_ten.append(k1 + str(int(dateList[0]))[2:4] + h + ".SHF")
                print(one_five_ten)
                print(k2)
                allList.append(one_five_ten)
            return allList, kindList2
        else:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                d = d - 1
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))

            d = int(dateList[1])
            for m in range(13 - int(dateList[1])):
                if d < 13:
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))
                    d = d + 1

            kindList1 = ["RB", "HC"]
            kindList2 = ["螺纹钢", "热轧卷板"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                one_five_ten = []
                for j in list1:
                    if int(j) in [1, 5, 10]:
                        one_five_ten.append(k1 + str(int(dateList[0]) + 1)[2:4] + j + ".SHF")

                for h in list2:
                    if int(h) in [1, 5, 10]:
                        one_five_ten.append(k1 + str(int(dateList[0]))[2:4] + h + ".SHF")
                print(one_five_ten)
                print(k2)
                allList.append(one_five_ten)
            return allList, kindList2

    def f_oneFiveNine_DCE(self,nowtime):

        date = str(nowtime)
        dateList = date.split('-')
        print(dateList[2])

        if int(dateList[2]) > 14:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))
                    d = d - 1
            d = int(dateList[1])
            for m in range(12 - int(dateList[1])):
                if d < 12:
                    d = d + 1
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))

            kindList1 = ["M", "Y", "A", "P", "C", "CS", "JD", "L", "V", "PP", "J", "JM", "I"]
            kindList2 = ["豆粕", "豆油", "豆一", "棕榈油", "玉米", "淀粉", "鸡蛋", "塑料", "PVC", "聚丙烯", "焦炭", "焦煤", "铁矿石"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                one_five_nine = []
                for j in list1:
                    if int(j) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]) + 1)[2:4] + j + ".DCE")

                for h in list2:
                    if int(h) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]))[2:4] + h + ".DCE")
                print(one_five_nine)
                print(k2)
                allList.append(one_five_nine)
            return allList, kindList2
        else:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                d = d - 1
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))

            d = int(dateList[1])
            for m in range(13 - int(dateList[1])):
                if d < 13:
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))
                    d = d + 1

            kindList1 = ["M", "Y", "A", "P", "C", "CS", "JD", "L", "V", "PP", "J", "JM", "I"]
            kindList2 = ["豆粕", "豆油", "豆一", "棕榈油", "玉米", "淀粉", "鸡蛋", "塑料", "PVC", "聚丙烯", "焦炭", "焦煤", "铁矿石"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                one_five_nine = []
                for j in list1:
                    if int(j) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]) + 1)[2:4] + j + ".DCE")

                for h in list2:
                    if int(h) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]))[2:4] + h + ".DCE")
                print(one_five_nine)
                print(k2)
                allList.append(one_five_nine)
            return allList, kindList2


    def f_oneFiveNine_CZCE(self,nowtime):

        date = str(nowtime)
        dateList = date.split('-')
        print(dateList[2])

        if int(dateList[2]) > 14:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))
                    d = d - 1
            d = int(dateList[1])
            for m in range(12 - int(dateList[1])):
                if d < 12:
                    d = d + 1
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))

            kindList1 = ["SR", "CF", "ZC", "FG", "TA", "MA", "OI", "RM", "SF", "SM", "AP"]
            kindList2 = ["白糖", "棉花", "动力煤", "玻璃", "PTA", "甲醇", "菜油", "菜籽粕", "硅铁", "锰硅", "苹果"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                one_five_nine = []
                for j in list1:
                    if int(j) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]) + 1)[3:4] + j + ".CZC")

                for h in list2:
                    if int(h) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]))[3:4] + h + ".CZC")
                print(one_five_nine)
                print(k2)
                allList.append(one_five_nine)
            return allList, kindList2
        else:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                d = d - 1
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))
            print(list1)
            d = int(dateList[1])
            for m in range(13 - int(dateList[1])):
                if d < 13:
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))
                    d = d + 1

            kindList1 = ["SR", "CF", "ZC", "FG", "TA", "MA", "OI", "RM", "SF", "SM"]
            kindList2 = ["白糖", "棉花", "动力煤", "玻璃", "PTA", "甲醇", "菜油", "菜籽粕", "硅铁", "锰硅"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                one_five_nine = []
                for j in list1:
                    if int(j) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]) + 1)[3:4] + j + ".CZC")

                for h in list2:
                    if int(h) in [1, 5, 9]:
                        one_five_nine.append(k1 + str(int(dateList[0]))[3:4] + h + ".CZC")
                print(one_five_nine)
                print(k2)
                allList.append(one_five_nine)
            return allList, kindList2

    def f_oneFiveTen_CECE(self,nowtime):
        date = str(nowtime)
        dateList = date.split('-')
        print(dateList[2])

        if int(dateList[2]) > 14:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))
                    d = d - 1
            d = int(dateList[1])
            for m in range(12 - int(dateList[1])):
                if d < 12:
                    d = d + 1
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))

            kindList1 = ["AP"]
            kindList2 = ["苹果"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                one_five_ten = []
                for j in list1:
                    if int(j) in [1, 5, 10]:
                        one_five_ten.append(k1 + str(int(dateList[0]) + 1)[3:4] + j + ".CZC")

                for h in list2:
                    if int(h) in [1, 5, 10]:
                        one_five_ten.append(k1 + str(int(dateList[0]))[3:4] + h + ".CZC")
                print(one_five_ten)
                print(k2)
                allList.append(one_five_ten)
            return allList, kindList2
        else:
            list1 = []
            list2 = []
            d = int(dateList[1])
            for i in range(int(dateList[1])):
                d = d - 1
                if d > 0:
                    if d < 10:
                        list1.append("0" + str(d))
                    else:
                        list1.append(str(d))

            d = int(dateList[1])
            for m in range(13 - int(dateList[1])):
                if d < 13:
                    if d < 10:
                        list2.append("0" + str(d))
                    else:
                        list2.append(str(d))
                    d = d + 1

            kindList1 = ["AP"]
            kindList2 = ["苹果"]
            allList = []
            for k1, k2 in zip(kindList1, kindList2):
                one_five_ten = []
                for j in list1:
                    if int(j) in [1, 5, 10]:
                        one_five_ten.append(k1 + str(int(dateList[0]) + 1)[3:4] + j + ".CZC")

                for h in list2:
                    if int(h) in [1, 5, 10]:
                        one_five_ten.append(k1 + str(int(dateList[0]))[3:4] + h + ".CZC")
                print(one_five_ten)
                print(k2)
                allList.append(one_five_ten)
            return allList, kindList2

    def dataToDB(self,result,exchange,nowtime):

        print(result[0],result[1])
        for codeList,a in zip(result[0],result[1]):
            for i in codeList:
                engine = create_engine("mysql+pymysql://datadepartment:datacode@192.168.123.243:3306/stock_futures_db?charset=utf8")
                # 连接数据库
                dset = w.wsd(i, "windcode,open,high,low,close,volume,oi,settle", nowtime, nowtime)
                list1 = []
                list2 = []
                for j in range(len(dset.Times)):
                    #EXCHANGE
                    list1.append(exchange)
                    list2.append(a)
                s = dset.Data
                s.insert(0, dset.Times)
                s.insert(0, list2)
                s.insert(0, list1)
                print(s)
                h = map(list, zip(*s))
                h1 = list(h)
                df = pd.DataFrame(h1,columns=("exchange", "kind", "datatime", "windcode", "open", "high", "low", "close", "volume","oi","settle"))
                print(df)
                try:
                    pd.io.sql.to_sql(df, "futures_market", con=engine, if_exists='append', index=False)
                except Exception as e:
                    print("有异常"+ str(e))

    def start(self,nowtime):

        #SHFE
        all_SHFE = self.f_all_SHFE(nowtime)
        one_five_nine_SHFE = self.f_oneFiveNine_SHFE(nowtime)
        one_five_ten_SHFE = self.f_oneFiveTen_SHFE(nowtime)

        self.dataToDB(all_SHFE,"SHFE",nowtime)
        self.dataToDB(one_five_nine_SHFE,"SHFE",nowtime)
        self.dataToDB(one_five_ten_SHFE,"SHFE",nowtime)

        #DCE
        one_five_nine_DCE = self.f_oneFiveNine_DCE(nowtime)

        self.dataToDB(one_five_nine_DCE,"DCE",nowtime)

        #CZCE
        one_five_nine_CZCE = self.f_oneFiveNine_CZCE(nowtime)
        one_five_ten_CZCE = self.f_oneFiveTen_CECE(nowtime)

        self.dataToDB(one_five_nine_CZCE,"CZCE",nowtime)
        self.dataToDB(one_five_ten_CZCE,"CZCE",nowtime)





if __name__ == "__main__":
    FuturesVar().start()




