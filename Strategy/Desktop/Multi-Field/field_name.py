import pymysql.cursors
import pandas as pd
import numpy as np
from WindPy import w
from sqlalchemy import create_engine
import time
from pandas import Series,DataFrame,np
import xlwt
conn = pymysql.connect(host='192.168.123.243',user='datadepartment',password='datacode',db='fundamentals_db',charset='utf8')# 创建游标
cursor = conn.cursor()
cursor.execute("select COLUMN_NAME from information_schema.COLUMNS where table_name = 'print_steel_import_export' ")
results = cursor.fetchall()
print(results)
