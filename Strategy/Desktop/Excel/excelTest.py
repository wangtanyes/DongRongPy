import xlrd
import pymysql.cursors
import time
import datetime

book = xlrd.open_workbook("C:\\Users\\Dell\\Desktop\\工作簿10.xls")
sheet = book.sheet_by_name("Sheet1")
sh = book.sheet_by_index(0)
nrows = sh.nrows  #行数
ncols = sh.ncols  #列数

db = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='stock_futures_db',charset='utf8')
cursor = db.cursor()
query = """insert into GuangFa (dataname,datatime,datavalue) values(%s,%s,%s)"""

#cursor.execute(query,[sheet.cell(0,0).value,sheet.cell(0,1).value,sheet.cell(0,2).value])
for j in range(1,ncols):
    list1 = []
    for i in range(0, nrows):
        if j > 0:
            dataName = sheet.cell(0, j).value
            if len(dataName) == 0 :
                exit()
            print("品种是 ： "+str(dataName))
            dataTime = sheet.cell(i,0).value
            #print(dataTime)
            #date = xldate_as_tuple(sheet.cell(row,col).value,0)
            if i > 0 :
                value = str(sheet.cell(i, j).value)
                print("数据是 ： " + value)
                date = xlrd.xldate.xldate_as_datetime(dataTime, 0)
                print(date)
                if len(value)>0:
                    try:
                        cursor.execute(query, [dataName,date, value])
                    except Exception as e :
                        print(e)

db.commit()

cursor.close()
db.close()
print('insert ok')
