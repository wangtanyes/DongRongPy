import  time
import  _thread
from datetime import datetime,timedelta,date

# 拿到当前的时间
print(date.today())
print(datetime.now().date())
print(datetime.today().strftime("%Y-%m-%d"))

# 时间格式化，把时间转化为字符串
dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(dt)

# 把字符串转化为时间
myTime = datetime.strptime(dt,"%Y-%m-%d %H:%M:%S")
print(type(myTime), myTime)

# 把字符串转化为时间元祖
timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
print(timeArray)

# 将时间元组转换成时间戳
timestamp = time.mktime(timeArray)
print(timestamp)

# 时间计算
# 计算几天、几周前/后
now = datetime.now().date()
three_days_ago = now + timedelta(days=-3)       # 当days=3试，表示3天后，当days=-3时，表示3天前
three_weeks_ago = now + timedelta(weeks=-1)     # 当weeks=-1试，表示一周前，当weeks=1时，表示一周后
print(now,three_days_ago,three_weeks_ago)


#  计算两个时间段之间的时间差
# start = datetime.now()
# time.sleep(10)
# end = datetime.now()
#
# print((end - start).days)   # 相差多少天
# print((end - start).total_seconds())    # 相差多少秒，时间比较精确，有小数
# print((end - start).seconds)        # 相差多少秒，只有整数
# print((end - start).microseconds)   # 相差多少毫秒

# 计算今天是周几
today = date.today()
print(today.weekday())      #  返回weekday，如果是星期一，返回0；如果是星期2，返回1，以此类推；
print(today.isoweekday())   # 返回weekday，如果是星期一，返回1；如果是星期2，返回2，以此类推；

# class complex:
#     i = 0;
#     j = 0;
#     def __init__(self, firsr, second):
#         self.i = firsr;
#         self.j = second;
#
# x = complex(1,2);
# print(x.i,x.j)
# print(time.ctime())

#
# class myThread:
#     def testThread(threadName, delay):
#         count = 0
#         while count < 5 :
#             time.sleep(delay);
#             count+=1;
#             print("%s : %s"  %(threadName, time.ctime(time.time())))
#
# x = myThread();
# try:
#     _thread.start_new_thread(x.testThread(), ("thread-1", 2,))
#     # _thread.start_new_thread(x.testThread(), ("thread-2", 3,))
#
# except:
#     print("Error: unable to start thread")