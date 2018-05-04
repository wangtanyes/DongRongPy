import time
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
import  pymysql
import re

loginURL = "https://user.smm.cn/center_auth"  # POST发送到的网址
allURL = "https://news.smm.cn/live"
afterURL = "https://news.smm.cn/live?category="   # 想要爬取的登录后的页面

session = requests.Session()

category = ["铜","铝","铅","锌","锡","镍","锰","硅","钴锂","锑","钨","铟镓锗","铋硒碲","小金属","贵金属","稀土","钢铁","再生","利源"]
pageNum = [20,21,22,23,24,25,26,28,29,93,97,95,27,3,2,30,78,98,32]
# cant  = [26,28,93,97,95]


def login():

    conn = pymysql.connect(host='192.168.123.243', user='datadepartment', passwd='datacode', port=3306, db='searchreport', charset='utf8')
    cor = conn.cursor()  # 获取一个游标对象

    # 模拟登陆，此网络设置的反爬虫，模拟登陆失败
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

    }

    data = {
        "user_name": "18989494306",
        "password": "b1eef8a2e0a01a704990524beec6969a",
        "source": "cn",
        "promote": ""
    }
    resp = session.post("https://user.smm.cn/center_auth", data=data, headers=headers,stream=True)

    ss = re.search("[{][\"][t][\S]+[}]", resp.text)
    datastr = ss.group(0).replace("{", "").replace("}", "")
    d1 = datastr.split(":")[1]
    d2 = d1.replace("\"", "")

    dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(timeArray)

    resp.cookies['Cookie'] = "GA1.2.495093812.1514275188; _gid=GA1.2.732006837.1514275188; Hm_lvt_9734b08ecbd8cf54011e088b00686939=1514275189;SMM_auth_token=" + d2 + ";referer_code=https%3A%2F%2Fnews.smm.cn%2Flive; Hm_lpvt_9734b08ecbd8cf54011e088b00686939=" + \
                    str(timestamp).split(".")[0] + "; _gat_UA-102039857-2=1"

    # 爬去不同金属网页的数据
    for i in range(category.__len__()):
        print(i)
        # '''登入方法,传递参数给服务器,并使用相同的cookies'''
        # xyz = session.get(firstURL,headers=headers).content
        # _xsrf = bs(xyz,"html.parser").find('input',{'name':'username'}).get("value")

        response = session.get(afterURL+str(pageNum[i]), cookies=resp.cookies,headers=headers)  # 获得登陆后的响应信息，使用之前的cookie
        time.sleep(3)
        data = response.content.decode("utf-8", "ignore")
        analyseData(data,category[i],int(pageNum[i]),cor)

    #  数据存储完成关闭数据库
    cor.close()  # 关闭游标
    conn.commit()  # 向数据库中提交任何未解决的事务，对不支持事务的数据库不进行任何操作
    conn.close()  # 关闭到数据库的连接，释放数据库资源

# data:网页的数据，cat：金属的种类 ，cat_code：金属的代码，cor:数据库的游标对象
def analyseData(data,cat,cat_code,cor):
    soup = bs(data, "html.parser")
    today = datetime.today().strftime("%Y-%m-%d")

    # 爬取今天的数据
    todayData = soup.find_all('div', class_="news-list news_list_day", data_date=today)
    everyData = bs(str(todayData), "html.parser").find_all('div', class_="news-item news_item ")

    # 从数据库中查询出上次存储数据的最大的时间
    getsql = "SELECT report_time from metal_report where categore_code=%d ORDER BY report_time DESC LIMIT 1" % (
    cat_code)
    cor.execute(getsql)  # 执行对应的SQL语句
    everyTime = cor.fetchall()

    # 便利爬取得每一条数据
    for i in everyData:
        # 取出内容以及标签，取出时间以及标签
        contentTag = bs(str(i), "html.parser").find_all('div', class_="news-item-text")
        timeTag = bs(str(i), "html.parser").find_all('div', class_="news-item-time item_pub_time")

        # 得到内容，得到时间
        contentResult = bs(str(contentTag[0]), "html.parser").text.strip().replace("\n", "")
        timeResult = bs(str(timeTag[0]), "html.parser").text.strip().replace("\n", "")

        contentResult = contentResult.replace("（详情）", "").strip()
        contentResult = contentResult.replace("资讯快递会员专享", "").strip()

        # print(timeResult,contentResult)

        # 判断从数据库取出的时间是否存在，若存在则继续执行，不存在则执行else
        if everyTime.__len__() != 0:
            # 拿到数据库中的时间
            getTime = everyTime[0][0]
            # 拿到从网页爬取得时间，病进行格式化处理
            todayTime = today+" "+timeResult+":00"
            print(todayTime,getTime, todayTime==str(getTime))
            # 判断这两个时间是否相同，若不相同，对内容数据进行处理，并存储
            if todayTime != str(getTime):
                if "】" in contentResult:
                    allContent = contentResult.split("】")
                    title=allContent[0].replace("【","")
                    content=allContent[1]
                    title = str(title).strip("【")
                    if title is not None:
                        sql = "insert into metal_report(category,categore_code,report_title,report_time,report_desc) value('%s','%d','%s','%s','%s')" % (cat, cat_code, str(title), today + " " + timeResult, str(content))
                        cor.execute(sql)  # 执行对应的SQL语句
                        print("方案二",today, timeResult, title, content)

            #      时间相同，结束for循环
            else:break;

        #   数据库中查询不到时间，证明数据不存在，应该直接把数据插入数据库
        elif "】" in contentResult:
            allContent = contentResult.split("】")
            title = allContent[0].replace("【","")
            content = allContent[1]
            if title is not None:
                sql = "insert into metal_report(category,categore_code,report_title,report_time,report_desc) value('%s','%d','%s','%s','%s')" % (
                cat, cat_code, str(title), today + " " + timeResult, str(content))
                cor.execute(sql)  # 执行对应的SQL语句
                print("方案四",today, timeResult, title, content)
        #  否则结束循环
        else:break

# 时间间隔触发器，每个一个小时程序运行一次
def runJob():
    sched = BlockingScheduler()
    sched.add_job(login,'interval', hours=6)
    sched.start()

if __name__ == "__main__":
   # runJob()
    login()
