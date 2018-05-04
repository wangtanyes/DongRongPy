import pandas as pd
import matplotlib
import  pymysql
import numpy
from sqlalchemy import create_engine
def read():
     engine = create_engine("mysql+pymysql://heye:123456hy@192.168.123.243:3306/stock_futures_db?charset=utf8")
     df1 = pd.read_sql("select * from SHFE_market where kind='白银'",con=engine)
     df2 = pd.read_sql("select * from takeAPosition where kind='白银'",con=engine)
if __name__ == "__main__":
    read()
import pandas as pd
import matplotlib
import  pymysql
import numpy
from sqlalchemy import create_engine
def read():
     engine = create_engine("mysql+pymysql://heye:123456hy@192.168.123.243:3306/stock_futures_db?charset=utf8")
     df1 = pd.read_sql("select * from futures_Active_contracts where kind='白银' and datatime between '2013-01-01' and '2018-01-16'",con=engine)
     df2 = pd.read_sql("select * from takeAPosition where kind='白银' and date between '2013-01-01' and '2018-01-16' and member_name='前二十名合计'",con=engine)
     # print(df1)
     ppd = df2[['date','long_position_increase','short_position_increase']]
     #print(ppd)
     ppd[(ppd['long_position_increase']>0) & (ppd['short_position_increase']>0)]
     ppd['ooo']=1
     print(ppd)
if __name__ == "__main__":
    read()
