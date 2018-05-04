import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
from datetime import datetime,date
import matplotlib.dates as mdate
import matplotlib.ticker as mtick


mpl.rcParams['axes.unicode_minus'] = False      #   可以解决负号显示问题
mpl.rcParams['font.sans-serif'] = ['SimHei']    #  解决中为显示问题
mpl.rcParams['font.size'] = 10
mpl.rc('xtick', labelsize=20) #设置坐标轴刻度显示大小
mpl.rc('ytick', labelsize=20)

# plt.xlim(0,100)     # x轴范围,整体的x范围
# plt.ylim(0,100)     # y轴范围，整体的y范围



fig = plt.figure()
ax1 = fig.add_axes([0.15,0.17,0.8,0.7])
ax1.set_xlim(0,100)     # x轴范围
ax1.set_ylim(0,100)     # y轴范围

# 设置X轴的坐标刻度线显示间隔
# ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d %H:%M:%S'))#设置时间标签显示格式
# plt.xticks(pd.date_range(start='2007-01-08',end='2018-04-14',freq='1min'))#时间间隔
# plt.xticks(rotation=90)

#设置右侧Y轴显示百分数
# fmt='%.2f%%'
# yticks = mtick.FormatStrFormatter(fmt)
# ax1.yaxis.set_major_formatter(yticks)

x = np.arange(100)
y = np.arange(100)
plt.plot(x, y, 'b-', lw=1)      # ‘b-’是懒死实线，lw=1，是线宽为1
tim = [datetime.strftime(x,'%Y-%m-%d') for x in list(pd.date_range(start='2007-01-08',end='2018-04-14',freq='Y'))]
plt.xticks(np.arange(start=0,stop=100,step=10),tim,rotation=30)
plt.title("测试用的标题",loc='center')    # 默认在中间，还有left，right
plt.grid(True)      # 网格展示
plt.xlabel("这是x轴")
plt.ylabel("这是y轴")
plt.show()
ax1.xaxis_date()

# dataRange = pd.date_range(start='2007-01-08',end='2018-04-14',freq='Y').get_values()
# timeRange = []
# for i in dataRange:
#     i = datetime.utcfromtimestamp(i.tolist()/1e9)
#     # i = np.datetime64(i).astype(datetime)
#     i = i.strftime("%Y-%m-%d")
#     print(i)
#     timeRange.append(i)
#     # print(datetime.utcfromtimestamp(i))
#     # print(time.localtime(int(i)))
#     # ti = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(i))
#     # print(ti)
#     # print(datetime.strftime(i,"%Y-%m-%d"))
# print(tuple(timeRange))
# print(len(dataRange))
# t = []
# for x in list(pd.date_range(start='2007-01-08',end='2018-04-14',freq='Y')):
#     t.append(datetime.strftime(x,'%Y-%m-%d'))
#
# print(t)
# date_l=[datetime.strftime(x,'%Y-%m-%d') for x in list(pd.date_range(start='2007-01-08',end='2018-04-14',freq='Y'))]
# print(date_l)