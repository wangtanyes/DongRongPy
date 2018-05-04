import pandas as pd
import  pymysql
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

class plan():
    def __init__(self):
        pass

    def draw(self,x,y):
        plt.figure(figsize=(7,5))
        plt.plot(x, y, 'b-', lw=1)
        plt.grid(True)

        plt.xlabel('时间', fontproperties=font)
        plt.ylabel('指数', fontproperties=font)
        plt.title('结果', fontproperties=font)
        plt.show()

    def listDay(self, time, length):
        days = []
        for i in range(len(time)-length+1):
            day = time.loc[i+length-1,'datatime']
            days.append(str(day))
        return days

    def getOpenStockValue(self, time, firstValue, kind, length):
        values = []
        for i in range(len(time)-length+1):
            value = time.iloc[i+length-1,2]
            values.append(value)
        return values

    def getCloseStockValue(self, time, firstValue, kind, length):
        values = []
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

    def getPlotPrice(self,conn):
        days = []
        values = []
        openStock = []
        closeStock = []
        stockDays = []
        valuesTotal = []

        lastDays = []
        lastValues = []

        metal = ['工业金属','铝','铜']

        for i in range(len(metal)):
            if '工业金属' in metal[i]:
                sql = "SELECT classify_two,datatime, `OPEN`, `CLOSE` from industry_index_two where classify_two = '%s' and datatime >= '2007-01-08'  \
                      ORDER BY datatime" % (str(metal[i]))
            else:
                sql = "SELECT kind, datatime, `open` from futures_Active_contracts where kind = '%s' and datatime >= '2007-01-08'  \
                      ORDER BY datatime" % (str(metal[i]))

            data = pd.read_sql_query(sql, con=conn)
            # print(data)
            firstValue = data.iloc[0,2]
            if '工业金属' in metal[i]:
                stockDays = plan().listDay(data,5)
                openStock = plan().getOpenStockValue(data,firstValue,metal[i],5)
                closeStock = plan().getCloseStockValue(data,firstValue,metal[i],5)
            else:
                days = plan().listDay(data,5)
                value = plan().listValue(data,firstValue,metal[i],5)
                values.append(value)

        for i in range(len(values[0])):
            total = 0
            for j in range(len((values))):
                total += values[j][i]
            valuesTotal.append(float('%.4f' %(total)))

        lastValues.append(pow(10,6))
        lastDays.append(days[0])
        hold = False;
        stockCount = 0;
        price = 0;

        for i in range(min(len(days), len(stockDays))-1):
            if i==0:
                stockCount = pow(10,6)/closeStock[0]
                price = (closeStock[i+1] - openStock[i+1])*stockCount + pow(10,6)
                if valuesTotal[i+1] >= valuesTotal[i]:
                    hold = True
                else:
                    hold = False
                lastDays.append(days[i+1])
                lastValues.append(float('%.4f' %(price)))
            else:
                if hold:
                    price = (closeStock[i+1] - openStock[i+1])*stockCount + price
                    if valuesTotal[i+1] >= valuesTotal[i]:
                        hold = True
                    else:
                        hold = False
                    lastDays.append(days[i+1])
                    lastValues.append(float('%.4f' %(price)))
                else:
                    if valuesTotal[i+1] >= valuesTotal[i]:
                        stockCount = price/openStock[i+1]
                        price = (closeStock[i+1] - openStock[i+1])*stockCount + price
                        hold = True
                    else:
                        hold = False
                    lastDays.append(days[i+1])
                    lastValues.append(float('%.4f' %(price)))

        plan().draw(lastDays,lastValues)

if __name__ == '__main__':

    conn = pymysql.connect(host='192.168.123.243', user='datadepartment', passwd='datacode', port=3306, db='stock_futures_db',charset='utf8')
    cor = conn.cursor()

    plan().getPlotPrice(conn)

    cor.close()
    conn.close()
