import requests
import time
import xlrd
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from pandas import DataFrame
import urllib.request
import re
textList = []
#worksheet = xlrd.open_workbook('C:/Users/Administrator/Desktop/遗漏的代码.xlsx')
#sheet_names= worksheet.sheet_names()
#for sheet_name in sheet_names:
  #  sheet2 = worksheet.sheet_by_name(sheet_name)
   # rows = sheet2.row_values() # 获取第四行内容
  #  cols = sheet2.col_values(0) # 获取第三列内容


def play(url):
    path = 'E:\软件包\chromedriver_win32\chromedriver.exe'
    driver = webdriver.Chrome(executable_path = path)
    driver.get(url)
    time.sleep(1)
    return driver

url1="http://data.eastmoney.com/report"

if __name__ == '__main__':
  #  url = "http://emweb.securities.eastmoney.com/f10_v2/CompanySurvey.aspx?type=web&code=sh60000"
  #  driver = play(url)
    #soup = bs(driver.page_source, "html.parser") #解析网页
   # grades = soup.find_all("tr")
   # for tr in grades:
    #    print(tr.text, end="\t")
   # print()
   # list_1 = []
    #try:
   # for i in cols:
            time.sleep(1)
            # data = driver.find_element_by_class_name("glyphicon-menu-right")   #空格前后可以省略,它不是百分百匹配
            # data.click()
            url ="http://data.eastmoney.com/report/600054.html#pageAnchor"  #http://data.eastmoney.com/report/#dHA9MCZjZz0wJmR0PTImcGFnZT01
            driver = play(url)
            soup = bs(driver.page_source, "html.parser")
            grades = soup.find_all("li",class_="titleL title")

            for g in grades:
                aa = g.find("a")
                if aa is not None:
                    bb=(aa['href'])
                   # print(bb)
                    url= url1+bb
                   # print(url)
                    data = requests.get(url)
                    soup = bs(data.text,'html.parser')
                    div = soup.find('div',class_ = 'newsContent')

                    textList.append(div.text)
print(textList)
#print(textList[0])
fw=open('C:\\Users\\Administrator\\Desktop\\data.txt','a',encoding='utf-8')
for i in range(len(textList)):
    kk=textList[i]
   # fw=open('C:\\Users\\Administrator\\Desktop\\data.txt','w')
    fw.write(kk)
for i in range(1, 4):
        time.sleep(1)
        data = driver.find_element_by_xpath("//*[@id='PageCont']/a[5]")  #//*[@id="PageCont"]/a[9]  //*[@id="PageCont"]/a[10] //*[@id="PageCont"]/a[11] //*[@id="PageCont"]/a[10]  //*[@id="PageCont"]/a[10]
        data.click()
        time.sleep(1)
        soup = bs(driver.page_source, "html.parser")
        grades = soup.find_all("li", class_="titleL title")

        for g in grades:
            aa = g.find("a")
            if aa is not None:
                bb = (aa['href'])
                # print(bb)
                url = url1 + bb
                # print(url)
                data = requests.get(url)
                soup = bs(data.text, 'html.parser')
                div = soup.find('div', class_='newsContent')

                textList.append(div.text)
print(textList)
fw=open('C:\\Users\\Administrator\\Desktop\\data.txt','a',encoding='utf-8')
for i in range(len(textList)):
    kk=textList[i]
   # fw=open('C:\\Users\\Administrator\\Desktop\\data.txt','w')
    fw.write(kk)











          #  file = open('C:\\Users\\Administrator\\Desktop\\2.txt', 'w', encoding='utf-8')
           # print(grades)
            #for tr in grades:
               # a = tr.text

                #b=  str(a).strip("\n")
               # import re
               # bb=re.sub(r"\s","",b)
                #print(bb,end="\t")
               # #file.writelines(bb)
           # print()
            #driver.quit()
    #except:
    #    print("err,there is no more page")

driver.quit()
