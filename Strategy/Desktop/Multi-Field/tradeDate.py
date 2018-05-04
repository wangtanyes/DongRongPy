import urllib.request as request
import datetime
import pymysql
import time

conn = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')
cursor = conn.cursor()

def get_day_type(query_date):
    url = 'http://tool.bitefu.net/jiari/?d=' + query_date
    resp = request.urlopen(url)
    content = resp.read()
    if content:
        try:
            day_type = int(content)
        except ValueError:
            return -1
        else:
            return day_type
    else:
        return -1
#判断是不是交易日方法
def is_tradeday(query_date):
    weekday = datetime.datetime.strptime(query_date, '%Y%m%d').isoweekday()
    if weekday <= 5 and get_day_type(query_date) == 0:
        return 1
    else:
        return 0

def today_is_tradeday():
    query_date = datetime.datetime.strftime(datetime.datetime.today(), '%Y%m%d')
    return is_tradeday(query_date)

def insertDateToDB(startDate,endDate):
    date_list = []
    begin_date = datetime.datetime.strptime(startDate, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(endDate, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y%m%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    for i in date_list:
        print(i)
        print(is_tradeday(i))
        #判断是不是交易日
        if (is_tradeday(i) == 1):
            query = 'insert into foreignExchange (datatime) values (%s)'
            tradeDate1 = datetime.datetime.strptime(i, '%Y%m%d')
            tradeDate = tradeDate1.strftime("%Y-%m-%d")
            cursor.execute(query, [tradeDate])
        conn.commit()
    cursor.close()
    conn.close()
    print("插入成功")

if __name__ == '__main__':
    nowtime = time.strftime("%Y-%m-%d", time.localtime())

    insertDateToDB("2018-01-12","2018-06-30")



