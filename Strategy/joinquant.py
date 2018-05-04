 def initialize(context)
    g.security='000001.xshe'
def handle_data(context,data):
    if g.security not in context.portfolio.positions:
        order(g.security,1000)
    else:
        order(g.security,-800)
#一个完整策略需要两步骤：
#设置初始化函数：initialize
#实现一个函数：handle-data
def initialize(context):
    #定义一个全局变量，保存要操作的股票
    g.security=('000001.XHSE')
    set_benchmark('000300.XSHG')
#每个单位时间调用一次
#获取股票收盘价
def handle_data(context,data):
  security=g.security
#获取过去五天平均价 取得上一时间价格 取得现金
close_data=attribute_history(security,5,'1d',['close']
MA5=close_data['close'].mean()
current_price=close_data['close'][-1]
cash=context.portfolio.cash
#如果上一时间点价格高出五天平均价1%，则全仓买入
#用所有cash买入 并记录
#如果上一时间点价格低于MA51%，则全仓卖出 记录这次卖出 画出上一时间点价格
if current_price>1.01*MA5:
 order_value(security,cash)
log.info("Buying %s"% (security))
elif current_price<MA5 and context.portfolio.positions[security].closeable_amount>0:
order_target(security)
record(stock_price=current_price)
import pandas as pd
import matplotlib
import  pymysql
import numpy
from sqlalchemy import create_engine
class Change():
    def __init__(self):
         pass

    def read(self):
         engine = create_engine(
             "mysql+pymysql://heye:123456hy@192.168.123.243:3306/timeseries_db?charset=utf8")
         df = pd.read_sql(
             "select * from stock_quotes where code='SZ300001'",con=engine)
         # print(df)
         print(df[df['open']<5])  #pandas分析
if __name__ == '__main__':
    test = Change().read()

import  pymysql
import numpy
db = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')
cursor = db.cursor()
cursor.execute( """select * from DCE_market where datatime = '2010-01-01'""")
result = cursor.fetchall()
import pandas as pd
df = pd.DataFrame(result)
print(df)