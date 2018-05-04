import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from pandas import DataFrame

def play(url):
    path = 'D:\Simulator\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path)
    driver.get(url)
    time.sleep(1)
    return driver

if __name__ == '__main__':
    url = "http://www.sse.com.cn/assortment/stock/list/share/"
    driver = play(url)
    soup = bs(driver.page_source,"html.parser")
    grades = soup.find_all("td")

    for tr in grades:
        print(tr.text, end="\t")
    print()
    #try:
    for i in range(1,54):
            time.sleep(1)
            data = driver.find_element_by_class_name("glyphicon-menu-right")   #空格前后可以省略,它不是百分百匹配
            data.click()
            soup = bs(driver.page_source, "html.parser")
            grades = soup.find_all("td")
            for tr in grades:
                print(tr.text, end="\t")
    #except:
    #    print("err,there is no more page")
    driver.quit()