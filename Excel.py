#   coding=utf-8

import  numpy as np
import xlrd
import pandas as pd
from math import radians, cos, sin, asin, sqrt,fabs
from datetime import datetime
from xlrd import xldate_as_tuple


class plan():

    EARTH_RADIUS=6371           # 地球平均半径，6371km

    def __init__(self):
        pass

    def hav(self,theta):
        s = sin(theta / 2)
        return s * s

    # 得到两个维度之间的距离，单位是公里
    def get_distance_hav(self,lat0, lng0, lat1, lng1):
        "用haversine公式计算球面两点间的距离。"
        # 经纬度转换成弧度
        lat0 = radians(lat0)
        lat1 = radians(lat1)
        lng0 = radians(lng0)
        lng1 = radians(lng1)

        dlng = fabs(lng0 - lng1)
        dlat = fabs(lat0 - lat1)
        h = plan.hav(self,dlat) + cos(lat0) * cos(lat1) * plan.hav(self,dlng)
        distance = 2 * plan.EARTH_RADIUS * asin(sqrt(h))
        return distance

    # k-means得到的据点是22.98254238471582,113.53753848948959]
    def getDis(self,lat,lon):
        return plan.get_distance_hav(self,lat,lon,22.656098648126363,114.0985451144281)
    def getPrice(self,dis,lat):
        y = (-5.61691555875302) + (dis*0.0537969938296451) + (lat * 3.15026428183607)
        return y

    def readExcel(self):
                # list = ['附件一：已结束项目任务数据','附件二：会员信息数据','附件三：新项目任务数据']
                list = ['附件三：新项目任务数据']
                for fileName in list:
                    worksheet = xlrd.open_workbook("D:\\数据\\"+ fileName + ".xlsx")
                    sheet_names= worksheet.sheet_names()
                    file = open("D:\\数据\\"+ fileName + ".txt", mode="w+",encoding="UTF-8")
                    for sheet_name in sheet_names:
                        sheet2 = worksheet.sheet_by_name(sheet_name)
                        for i in range(sheet2.nrows):
                            value = ""
                            dis = 0
                            lat = 0
                            for j in range(sheet2.ncols):
                                cell = sheet2.cell_value(i,j)
                                if i != 0 and j == 0:
                                    dis = float(cell)
                                elif i != 0 and j == 2:
                                   lat = float(cell)
                            value = plan.getPrice(self,float(dis),float(lat))
                            # value = plan.getDis(self,float(dis),float(lat))
                            print(value)
                            file.writelines(str(value) + "\n")
                    file.flush()
                    file.close()





if __name__ == '__main__':
    # plan().getData()
    plan().readExcel()