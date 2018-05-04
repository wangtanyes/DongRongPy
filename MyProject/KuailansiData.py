from apscheduler.schedulers.blocking import BlockingScheduler
import  pymysql
import requests
import re

urljson = "http://119.29.63.230/24h/news.json?newsid=0&vs=252421674"

headers = {
    'Referer': 'https://www.baidu.com/link?url=NubwjnwXxvQ2l1fD-Mp2L3MbLu6S4_woQPSJqoncTvO&wd=&eqid=e2d93c3e00032dd3000000045a45e456',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
}

session = requests.Session()

def getCode():
    conn = pymysql.connect(host='192.168.123.243', user='datadepartment', passwd='datacode', port=3306, db='searchreport',charset='utf8')
    cor = conn.cursor()  # 获取一个游标对象

    resp =  session.get(urljson, headers=headers)

    data = resp.content.decode('utf-8', 'ignore')
    rex = re.compile(r'{"newsID".+"Keywords".+}')
    datas = re.findall(rex,data)
    alldata = datas[0].split("}")

    getsql = "SELECT report_time from kuailansireport ORDER BY report_time DESC LIMIT 1"
    cor.execute(getsql)  # 执行对应的SQL语句
    everyTime = cor.fetchall()
    if everyTime.__len__() != 0:
        getTime = everyTime[0][0]
    else:getTime = ""


    for everydata in alldata:
        everydata = everydata.strip(",").strip("{")
        if "newsID" in everydata:
            try:
                allSplit = everydata.split(",")
                newsID = allSplit[0].split(":")[1].strip('\"')
                time = allSplit[1].strip("\"time\"").strip(":").strip('\"')
                allcontent = allSplit[2].split(":")[1].strip('\"')
            except Exception as e:
                pass

            if str(getTime) != str(time):
                if "【" in allcontent:
                    try:
                        detailContent = allcontent.split("】")
                        title = detailContent[0].strip("【")
                        contentDesc = detailContent[1]
                        sql = "insert into kuailansireport(newsID,report_time,report_title,report_desc) value('%s','%s','%s','%s')" % (str(newsID), str(time), str(title),str(contentDesc))
                        cor.execute(sql)  # 执行对应的SQL语句
                        print("执行if",newsID, time, title, contentDesc)
                    except Exception as e:
                        pass
                else:
                    try:
                        title=None
                        contentDesc = allcontent
                        sql = "insert into kuailansireport(newsID,report_time,report_title,report_desc) value('%s','%s','%s','%s')" % (
                        str(newsID), str(time), str(title), str(contentDesc))
                        cor.execute(sql)  # 执行对应的SQL语句
                        print("执行else",newsID, time, title, contentDesc)
                    except BaseException as e:
                        pass
            else:break

        else:break

    cor.close()  # 关闭游标
    conn.commit()  # 向数据库中提交任何未解决的事务，对不支持事务的数据库不进行任何操作
    conn.close()  # 关闭到数据库的连接，释放数据库资源


def runJob():
    sched = BlockingScheduler()
    sched.add_job(getCode,'interval', minutes=1)
    sched.start()

if __name__ == "__main__":
    # runJob()
    getCode()