import xlrd
import pymysql.cursors

book = xlrd.open_workbook("C:\\Users\\Dell\\Desktop\\CZCE.xls")
sheet = book.sheet_by_name("Sheet1")
sh = book.sheet_by_index(0)
nrows = sh.nrows  #行数
ncols = sh.ncols  #列数

db = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')
cursor = db.cursor()
query = """insert into CZCE_exchange_num(exchange,kind,windcode)values(%s,%s,%s)"""

cursor.execute(query,[sheet.cell(0,0).value,sheet.cell(0,1).value,sheet.cell(0,2).value])
for i in range(1,nrows):
    print(i)
    exchange = sheet.cell(i,0).value
    kind = sheet.cell(i,1).value
    windcode = sheet.cell(i,2).value
    cursor.execute(query,[exchange,kind,windcode])
db.commit()
cursor.close()
db.close()
print('insert ok')
