from bs4 import BeautifulSoup as bs
import requests
import random
import time
import logging

def save(data):
    with open('D:/tmpdir/dazhong.txt', 'a',encoding='utf-8') as fb:
        fb.write(data)

s = requests.session()
proxies = {
	"http":"http://35.187.232.40:80"
}
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
def getcode(url):
    response = s.get(url, headers=header,proxies=proxies)
    data = response.content.decode('utf-8','ignore')
    soup = bs(data,"html.parser")
    dv = soup.find_all("a", class_="tg-floor-title")
    urlset1 = set()
    sleep_time = random.random()
    time.sleep(sleep_time)
    for some in dv:
        p = some['href']
        urlset1.add(p)
    return urlset1

def play():
    page = 0
    for page in range(0,49):
        urlset = getcode('https://t.dianping.com/list/hangzhou-category_1?pageIndex='+str(1))
        for i in urlset:
            newurl = "https://t.dianping.com"+i
            # print(newurl)
            response = s.get(newurl, headers=header, timeout=0.5)
            data = response.content.decode("utf-8")
            soup = bs(data,"html.parser")
            title = soup.find("h1", class_="title").text
            price = soup.find("span", class_="price-display").text
            menprice = soup.find("span", class_="price-original").text
            yishou = soup.find("em", class_="J_current_join").text
            pingfen = soup.find("span", class_="star-rate").text
            plunshu = soup.find("a", class_="comments-count J_main_comment_jump").text
            date = soup.find("div", class_="validate-date").text
            st = str(title).split("\n")
            dt = st[2].strip()+"   "+str(price).strip()+"    "+str(menprice).strip()+"  "+str(yishou).strip()+"   "\
                +str(pingfen).strip()+"   "+str(plunshu).strip()+"   "+str(date).lstrip()
            print(dt)
if __name__ == '__main__':
    play()