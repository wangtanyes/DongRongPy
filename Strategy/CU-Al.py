import pandas as pd
import  pymysql
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
from matplotlib.dates import AutoDateLocator, DateFormatter
from datetime import datetime
from datetime import datetime

class plan():
    def __init__(self):
        pass

    def draw(self,x,y):
        dates = []
        for i in range(len(x)):
            da = datetime.strptime(x[i], '%Y-%m-%d').date()
            dates.append(da)
        fig = plt.figure(figsize=(7,5))
        ax1 = fig.add_subplot(2,1,1)
        ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))

        plt.plot(dates, y, 'b-', lw=1)
        plt.xticks(pd.date_range('2007-01-08','2018-04-14'),rotation=60)
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

    def getStockValue(self, time, length,type):
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
            value = 0;
            for j in range(length):
                value += time.loc[i+j,'datavalue']
            if "铜" in kind or "铝" in kind:
                val = (value)*0.5/(length*firstValue)
                values.append(val)
            else:
                val = (value)*0.10/(length*firstValue)
                values.append(val)
        return values

    def getPlotPrice(self,conn,INTERVAL):
        days = []
        values = []
        openStock = []
        closeStock = []
        stockDays = []
        valuesTotal = []

        lastDays = []
        lastValues = []

        #metal = ['工业金属','镍','铅','铝','锌','铜']
        metal = ['工业金属','铝','铜']

        for i in range(len(metal)):
            if '工业金属' in metal[i]:
                sql = "SELECT classify_two,datatime, `OPEN`, `CLOSE` from industry_index_two where classify_two = '%s' and datatime >= '2007-01-08'  \
                      ORDER BY datatime" % (str(metal[i]))
            elif "铝" in metal[i]:
                sql = "SELECT * from spotPrice where dataname = '上海金属网:平均价:%s:A00' and datatime >= '2007-01-08' ORDER BY datatime" % (str(metal[i]))
            else:
                sql = "SELECT * from spotPrice where dataname = '上海金属网:平均价:%s:1#' and datatime >= '2007-01-08' ORDER BY datatime" % (str(metal[i]))

            data = pd.read_sql_query(sql, con=conn)

            if '工业金属' in metal[i]:
                stockDays = plan().listDay(data,INTERVAL)
                openStock = plan().getStockValue(data,INTERVAL,"open")
                closeStock = plan().getStockValue(data,INTERVAL, "close")
            else:
                firstValue = data.iloc[0,2]
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

        # print(len(valuesTotal),valuesTotal)
        # print(len(days),days)
        # print(len(stockDays), stockDays)
        # print(len(openStock), openStock)
        # print(len(closeStock), closeStock)

        for i in range(min(len(days), len(stockDays))):
            if days[i] != stockDays[i]:
                day = datetime.strptime(days[i], '%Y-%m-%d')
                stockDay = datetime.strptime(stockDays[i], '%Y-%m-%d')
                days.insert(i,stockDays[i])
                valuesTotal.insert(i,valuesTotal[i-1])

        # print(len(valuesTotal),valuesTotal)
        # print(len(days),days)
        # print(len(stockDays), stockDays)
        # print(len(openStock), openStock)
        # print(len(closeStock), closeStock)

        lastValues.append(pow(10,6))
        lastDays.append(days[0])
        hold = True
        stockCount = pow(10,6)/closeStock[0]
        money = pow(10,6)-(pow(10,6)*0.00003)
        numTrade = 1

        for i in range(min(len(days), len(stockDays))-1):
            if hold:
                if valuesTotal[i+1] < valuesTotal[i]:
                    money = money-(money*0.001)
                    numTrade+=1
                    hold = False
                else:
                    money = (closeStock[i+1] - openStock[i+1])*stockCount + money

                lastDays.append(days[i+1])
                lastValues.append(float('%.4f' %(money)))
            else:
                if valuesTotal[i+1] > valuesTotal[i]:
                    stockCount = money/openStock[i+1]
                    money = (closeStock[i+1] - openStock[i+1])*stockCount + money - (money*0.0003)
                    hold = True

                lastDays.append(days[i+1])
                lastValues.append(float('%.4f' %(money)))

        # print(len(lastDays), lastDays)
        # print(len(lastValues), lastValues)
        print('交易的次数是%d' %(numTrade))
        plan().draw(lastDays,lastValues)

if __name__ == '__main__':

    conn = pymysql.connect(host='192.168.183.243', user='datadepartment', passwd='datacode', port=3306, db='stock_futures_db',charset='utf8')
    cor = conn.cursor()

    plan().getPlotPrice(conn, 5)

    cor.close()
    conn.close()
