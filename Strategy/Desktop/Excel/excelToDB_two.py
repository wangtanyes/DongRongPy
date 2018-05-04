import xlrd
import pymysql.cursors

book = xlrd.open_workbook("C:\\Users\\Dell\\Desktop\\禽畜.xls")
sheet = book.sheet_by_name("Sheet1")
sh = book.sheet_by_index(0)
nrows = sh.nrows  #行数
ncols = sh.ncols  #列数

db = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='stock_futures_db',charset='utf8')
cursor = db.cursor()

query = """insert into spotPrice_num (dataname,windcode) values(%s,%s)"""
try:
    cursor.execute(query,[sheet.cell(0,0).value,sheet.cell(0,1).value])
except Exception as e :
    print(e)
for i in range(1,nrows):
    print(i)
    dataname = sheet.cell(i,0).value
    windcode = sheet.cell(i,1).value
    try:
        cursor.execute(query,[dataname,windcode])
    except Exception as e:
        print("有异常" + str(e))
db.commit()
cursor.close()
db.close()
print('insert ok')
