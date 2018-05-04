import pymysql

conn = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')
cursor = conn.cursor()# 创建游标
def date():
    for year in range(2021):
        date = ''
        if year > 2008:
            for i in range(13):
                if  i>9:
                    date = str(year) +'-'+str(i)
                    #print(date)
                    #return date

                if i <10 and i !=0:
                    date = str(year)+'-0'+str(i)
                    #print(date)
                    #return date
                print(date)
                query = 'insert into print_steel_export_import2 (datetime) values(%s)'
                cursor.execute(query,[date])
    cursor.close()
    conn.commit()
    conn.close()
if __name__ == "__main__":
    date = date()


