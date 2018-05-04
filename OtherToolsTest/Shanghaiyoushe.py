import requests,datetime
from  bs4 import BeautifulSoup as bs
import re
import time


def login():
        session = requests.Session()
        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'

        }
        data = {
            "user_name": "18989494306",
            "password": "b1eef8a2e0a01a704990524beec6969a",
            "source":"cn",
            "promote":""
        }
        resp = session.post("https://user.smm.cn/center_auth", data=data, headers=headers,stream=True)

        ss = re.search("[{][\"][t][\S]+[}]",resp.text)
        datastr = ss.group(0).replace("{","").replace("}","")
        d1 = datastr.split(":")[1]
        d2 = d1.replace("\"","")

        dt = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

        timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")

        timestamp = time.mktime(timeArray)
        resp.cookies['Cookie']="GA1.2.495093812.1514275188; _gid=GA1.2.732006837.1514275188; Hm_lvt_9734b08ecbd8cf54011e088b00686939=1514275189;SMM_auth_token="+d2+";referer_code=https%3A%2F%2Fnews.smm.cn%2Flive; Hm_lpvt_9734b08ecbd8cf54011e088b00686939="+str(timestamp).split(".")[0]+"; _gat_UA-102039857-2=1"

        response = session.get("https://news.smm.cn/live",cookies=resp.cookies,headers=headers)  # 获得登陆后的响应信息，使用之前的cookie
        print(response.text)
        return response.content

if __name__ == '__main__':
        context = login()
        soup = bs(context,"html.parser")
        #print(soup)

