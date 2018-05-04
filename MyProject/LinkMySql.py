import  pymysql

category = ["铜","铝","铅","锌","锡","镍","锰","硅","钴锂","锑","钨","铟镓锗","铋硒碲","小金属","贵金属","稀土","钢铁","再生","利源"]
pageNum = [20,21,22,23,24,25,26,28,29,93,97,95,27,3,2,30,78,98,32]
dates = ['2017-12-27 23:07', '2017-12-27 12:08', '2017-12-27 10:23','2017-12-27 01:12','2017-12-27 05:09','2017-12-27 15:07']

try:
    # conn=pymysql.connect('localhost','root','123456','mysql')
    # 获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
    # 注意是utf8不是utf-8
    conn = pymysql.connect(host='localhost', user='root', passwd='123456', port=3306,db='searchreport', charset='utf8')
    cor=conn.cursor()       #获取一个游标对象
    # print(type(time(day)))

    for i in range(pageNum.__len__()):
        sql = "SELECT report_time from metal_report where categore_code=%d ORDER BY report_time DESC LIMIT 1" %(pageNum[i])
        cor.execute(sql)       #执行对应的SQL语句
        data = cor.fetchall()
        if data.__len__() != 0:
            print(data.__len__())
        #     comTime = data[0][0]
        #     print(comTime)
    # print(data)
    # for row in data:
    #     print(row)
    #     print(row[0])

    # sql_2 = 'insert into student(name,age,sex) value("田晓霞",26,"男")'
    # cout_2 = cor.execute(sql_2)
    # print("数量： " + str(cout_2))
    # conn.commit()

    cor.close()  # 关闭游标
    conn.commit()  # 向数据库中提交任何未解决的事务，对不支持事务的数据库不进行任何操作
    conn.close()  # 关闭到数据库的连接，释放数据库资源

except Exception as e:
    print(e)