import requests,datetime
from  bs4 import BeautifulSoup as bs
import  pymysql.cursors
import logging
from apscheduler.schedulers.blocking import  BlockingScheduler

firstURL = 'http://www.ccf.com.cn/dynamic_graph/index.php'
afterURL = "http://www.ccf.com.cn/dynamic_graph/index.php"  # 想要爬取的登录后的页面
loginURL = "http://www.ccf.com.cn/member/member.php"  # POST发送到的网址
session = requests.Session()
'''session会话'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

# def getyesterday():
#     '''
#     设置昨天的时间,定时每天8点执行昨天的网页,防止网页更新太慢导致的异常
#     :return:
#     '''
#     today = datetime.date.today()
#     oneday = datetime.timedelta(days=30)
#     yesterday = today - oneday
#     return yesterday


def login(username, password):
    '''登入方法,传递参数给服务器,并使用相同的cookies'''
    # xyz = session.get(firstURL,headers=headers).content
    # _xsrf = bs(xyz,"html.parser").find('input',{'name':'username'}).get("value")
    data = {
        "custlogin": 1,
        "url": "/ dynamic_graph / getPrice.php?monitorId = 4 & type = dd",
        "s": "",
        "action": "login",
        "username": "drxj",
        "password": "81187041",
        "imageField.x": 45,
        "imageField.y": 18,
        "remember_me": True
    }
    resp = session.post(loginURL, data=data, headers=headers)
    response = session.get(afterURL, cookies=resp.cookies, headers=headers)  # 获得登陆后的响应信息，使用之前的cookie
    return response.content

def getdata():
    # today = datetime.date.today()
    # day = datetime.timedelta(days=24)
    # oldday = today - day
    today="2017-11-14"
    oldday = "2017-10-03"
    data1 = {
        "chartTitle": "test",
        "data_father": 200000,
        "endDate": today,
        "ProdClass": "fhzs",
        "ProdID": 210000,
        "startDate": oldday
    }
    ps = session.post(firstURL,data=data1,headers=headers)
    return ps.content

def connect(data1,data2):
    '''
    连接数据库并传递数据到数据库
    :param data1: 
    :param data2: 
    :return: 
    '''
    db = pymysql.connect(host="192.168.123.243", user="heye", password="123456hy", db="futures_db", charset="utf8")
    query = """insert into detail(dataname,datatime,datatype,value,introtime) values(%s,%s,%s,%s,%s)"""
    cursor = db.cursor()
    cursor.execute(query, ["PTA开工率(周平均)", data1, 3, data2, data1])
    cursor.close()
    db.commit()
    db.close()

def start():
    '''
    程序执行的方法,通过解析网页将获取所需的值
    :return: 
    '''
    login("drxj", "81187041")
    ps = getdata()
    soup = bs(ps, "html.parser")
    trlist = soup.find_all("tr", attrs={"bgcolor": "#f6f6f6"})
    num = len(trlist) - 1
    #yesterday = getyesterday()
    yesterday = "2017-11-10"
    if (str(yesterday) == str(trlist[num].find_all("td")[1].text)):
        #print(trlist[num].find_all("td")[1].text)
        #print(trlist[num].find_all("td")[3].text)
        connect(yesterday, trlist[num].find_all("td")[3].text)

if __name__ == '__main__':
    '''定时任务'''
    # log = logging.getLogger("apscheduler.executors.default")
    # log.setLevel(logging.INFO)
    #
    # h = logging.StreamHandler()
    # fmt = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
    # h.setFormatter(fmt)
    # log.addHandler(h)
    # print('start to do it')
    # sched = BlockingScheduler()
    # sched.add_job(start,"cron",month="*",day="*",hour="8",minute="30")
    # sched.start()
    start()
