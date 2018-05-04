import  requests
import json
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup as bs
from datetime import datetime
import  pymysql
import  re
import os

tag = ["10","12","20","30","40","50","60","70","80","85","90","92","94","96","98"]
name = ["黑色", "期权", "有色","股指","宏观", "油脂油料","橡胶", "棉花", "白糖","原油", "能源化工", "谷物","贵金属", "国债", "市场"]

proxies = {
	"http":"http://35.187.232.40:80"
    # "http": "http://101.37.42.222:80"
    # "http": "http://121.69.35.174:8118"
}

datas = {"tag":["50"],"tag2":[],"user_id":"18866273820"}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length':'39',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'acw_tc=AQAAAGa8AzMFQAEA1iZ6fSNgJTGJaoBo; Hm_lvt_9b19cc8cf6bd240bb69df6fb93370496=1514363496; Hm_9b19cc8cf6bd240bb69df6fb93370496=1514363826',
    'Host': 'www.bestanalyst.cn',
    'Origin': 'http://www.bestanalyst.cn',
    'Referer': 'http://www.bestanalyst.cn/yantou',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
    'X-Requested-With': 'XMLHttpRequest'
}

session = requests.Session()

url = "http://www.bestanalyst.cn/kx_posted_change_tag"
urlq = "http://www.bestanalyst.cn/yantou"

def getCode():
    resp =  session.post("http://www.bestanalyst.cn/yantou", data=json.dumps(datas, ensure_ascii=False), headers=headers)
    # print(resp.text)
    print(resp.content.decode("utf-8", "ignore"))
    # print(resp.cookies)



    # pa = 'C:\\Users\\chromedriver.exe'
    # driver = webdriver.Chrome(executable_path=pa)
    # driver.get(urlq)
    # time.sleep(20)
    # soup = bs(driver.page_source, "html.parser")
    # soupData = soup.find_all("div", class_="k_row clearfix")
    #
    #
    # if soupData.__len__() != 0:
    #     saveDay = ""
    #     for everyData in soupData:
    #         day = everyData.find("div", class_="k_jian").text
    #         if day != "":
    #             saveDay = day
    #             everyTime = everyData.find("div", class_="it_time").text
    #             allContent = everyData.find("div", class_="it_cont clearfix").text
    #             if "【" in allContent:
    #                 getInfo(saveDay,everyTime,allContent)
    #             else:
    #                 break;
    #         else:
    #             everyTime = everyData.find("div", class_="it_time").text
    #             allContent = everyData.find("div", class_="it_cont clearfix").text
    #             if "【" in allContent:
    #                 getInfo(saveDay, everyTime, allContent)
    #             else: break;

def getInfo(saveDay,everyTime,allContent):
    allContent = allContent.split("【")
    aspectContent = allContent[0]
    detailContent = allContent[1]
    detailContent = str(detailContent).split("】")
    title = detailContent[0]
    desc = detailContent[1]
    time = formatDay(saveDay,everyTime)
    print(time,aspectContent,title,desc)

def formatDay(saveDay, everyTime):
    saveDay = str(saveDay).strip("日")
    [month,day] = saveDay.split("月")
    year = datetime.now().year
    return str(year) + "-" + str(month) + "-" + str(day) + " " + str(everyTime)



if __name__ == '__main__':
    getCode()