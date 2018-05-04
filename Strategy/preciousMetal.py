import pandas as pd
import  pymysql
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
from matplotlib.dates import AutoDateLocator, DateFormatter
from datetime import datetime

class plan():
    def __init__(self):
        pass

    def drawDouble(self,x,y,x1,y1):

    #  上下两张图
        plt.figure(figsize=(7,5))
        ax1 = plt.subplot(211)
        plt.plot(x,y, 'b', lw=1.5, label='1st')
        # plt.plot(kk[:, 0], 'ro')
        plt.grid(True)
        plt.legend(loc=0)
        plt.axis('tight')
        plt.xlabel('时间', fontproperties=font)
        plt.ylabel('指数', fontproperties=font)
        plt.title('结果', fontproperties=font)
        plt.title('Asimple Plot')

        ax1 = plt.subplot(212)
        plt.plot(x1, y1,'g', lw=1.5, label='2nd')
        # plt.plot(kk[:, 1], 'ro')
        plt.legend(loc=0)
        plt.axis('tight')
        plt.xlabel('时间', fontproperties=font)
        plt.ylabel('指数', fontproperties=font)
        plt.title('结果', fontproperties=font)
        plt.show()

    def draw(self,x,y):

        dates = []
        for i in range(len(x)):
            da = datetime.strptime(x[i], '%Y-%m-%d').date()
            dates.append(da)
        fig = plt.figure(figsize=(7,5))
        ax1 = fig.add_subplot(2,1,1)
        ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

        # plt.subplot(111)
        plt.plot(dates, y, 'b-', lw=1)
        plt.xticks(pd.date_range('2007-04-12','2018-01-18', freq='1Y'), rotation=60)
        # plt.plot(x, y, 'r.')
        plt.grid(True)

        # 设置刻度字体大小
        # plt.xticks(fontsize=16)
        # plt.yticks(fontsize=16)

        plt.xlabel('时间', fontproperties=font)
        plt.ylabel('总金额', fontproperties=font)
        # plt.title('', fontproperties=font)
        plt.show()

    def listDay(self, time, length):
        days = []
        for i in range(len(time)-length+1):
            day = time.loc[i+length-1,'datatime']
            days.append(str(day))
        return days

    def getStockValue(self, time, firstValue, kind, length,type):
        values = []
        if type in "open":
            for i in range(len(time)-length+1):
                value = time.iloc[i+length-1,2]
                values.append(value)
        elif type in "close":
            for i in range(len(time)-length+1):
                value = time.iloc[i+length-1,3]
                values.append(value)
        return values


    def listValue(self, time, firstValue, kind, length):
        values = []
        for i in range(len(time)-length+1):
            value = 0
            for j in range(length):
                value += time.iloc[i+j,2]
            if "铜" in kind or "铝" in kind:
                val = (value)*0.50/(length*firstValue)
                values.append(val)
            else:
                val = (value)*0.50/(length*firstValue)
                values.append(val)
        return values

    def getPlotPrice(self,conn, INTERVAL):

        days = []
        values = []
        openStock = []
        closeStock = []
        stockDays = []
        valuesTotal = []



        lastDays = []
        lastValues = []

        metal = ['贵金属','黄金','白银']

        for i in range(len(metal)):
            if '贵金属' in metal[i]:
                sql = "SELECT classify_two,datatime, `OPEN`, `CLOSE` from industry_index_two where classify_two = '%s' and datatime >= '2007-01-08'  \
                      ORDER BY datatime" % (str(metal[i]))
            else:
                sql = "SELECT kind, datatime, `open` from futures_Active_contracts where kind = '%s' and datatime >= '2007-01-08'  \
                      ORDER BY datatime" % (str(metal[i]))
            data = pd.read_sql_query(sql, con=conn)
            # print(data)
            firstValue = data.iloc[0,2]
            if '工业金属' in metal[i]:
                stockDays = plan().listDay(data,INTERVAL)
                openStock = plan().getStockValue(data,firstValue,metal[i],INTERVAL,"open")
                closeStock = plan().getStockValue(data,firstValue,metal[i],INTERVAL, "close")
            else:
                days = plan().listDay(data,INTERVAL)
                value = plan().listValue(data,firstValue,metal[i],INTERVAL)
                values.append(value)

        # for i in range(len(values)):
        #     print(values[i])

        for i in range(len(values[0])):
            total = 0
            for j in range(len((values))):
                total += values[j][i]
            valuesTotal.append(float('%.4f' %(total)))

        print(len(valuesTotal),valuesTotal)
        print(len(days),days)
        print(len(stockDays), stockDays)
        print(len(openStock), openStock)
        print(len(closeStock), closeStock)

        # plan().drawDouble(days,valuesTotal,stockDays,closeStock)

        lastValues.append(pow(10,6))
        lastDays.append(days[0])
        hold = False
        stockCount = 0
        money = 0

        for i in range(min(len(days), len(stockDays))-1):
            if i==0:
                stockCount = pow(10,6)/closeStock[0]
                money = (closeStock[i+1] - openStock[i+1])*stockCount + pow(10,6)
                if valuesTotal[i+1] >= valuesTotal[i]:
                    hold = True
                else:
                    hold = False

                lastDays.append(days[i+1])
                lastValues.append(float('%.4f' %(money)))
            else:
                if hold:
                    money = (closeStock[i+1] - openStock[i+1])*stockCount + money
                    if valuesTotal[i+1] >= valuesTotal[i]:
                        hold = True
                    else:
                        hold = False
                    lastDays.append(days[i+1])
                    lastValues.append(float('%.4f' %(money)))
                else:
                    if valuesTotal[i+1] >= valuesTotal[i]:
                        stockCount = money/openStock[i+1]
                        money = (closeStock[i+1] - openStock[i+1])*stockCount + money
                        hold = True
                    else:
                        hold = False
                    lastDays.append(days[i+1])
                    lastValues.append(float('%.4f' %(money)))

        print(len(lastDays), lastDays)
        print(len(lastValues), lastValues)

        plan().draw(lastDays,lastValues)

if __name__ == '__main__':

    conn = pymysql.connect(host='192.168.183.243', user='datadepartment', passwd='datacode', port=3306, db='stock_futures_db',charset='utf8')
    cor = conn.cursor()

    plan().getPlotPrice(conn,10)

    cor.close()
    conn.close()
