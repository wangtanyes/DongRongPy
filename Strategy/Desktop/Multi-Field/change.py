import pymysql

conn = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')
cursor = conn.cursor()

def getDataName():
    cursor.execute("select * from SpotPrice_agricultural_products_num")
    result = cursor.fetchall()
    #print(result)
    return result

def getData():
    result = getDataName()

    count = 0
    for i in result:
        print(len(result))
        count += 1
        print(count)
        print(i[0])

        cursor.execute("select datetime,`"+i[0]+"` FROM `SpotPrice_agricultural_products`")
        result2 = cursor.fetchall()
        for j in result2:
            query = """insert into SpotPrice_agricultural_products1 (dataname,datetime,datavalue) values (%s,%s,%s)"""
            cursor.execute(query,[i[0],j[0],j[1]])

    conn.commit()
    print("insert ok")
if __name__ == "__main__":
   getData()

