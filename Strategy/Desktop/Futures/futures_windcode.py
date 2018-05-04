import xlwt

list = ["05","06","07","08","09","10","11","12","13","14","15","16","17","18"]
list1 = ["01","02","03","04","05","06","07","08","09","10","11","12"]
list_mon = ["01","05","09"]
list_year = ["15","16","17","18"]
list3 = []
for i in list_year:
    for j in list_mon:
        str = "IC"+i+j+".CFE"
        list3.append(str)


print(list3)

f = xlwt.Workbook()  # 创建工作簿
sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
l_ = range(len(list3))
for i in l_:
    sheet1.write(i, 0, list3[i])  # write的第一个,第二个参数时坐标, 第三个是要写入的数据
    sheet1.write(i,1,"中证500指数期货")
    sheet1.write(i,2,"CFFEX")
# sheet1.write(0,0,start_date,set_style('Times New Roman',220,True))
f.save("C:\\Users\\Dell\\Desktop\\中证500指数期货.xls")  # 保存文件
