import  requests
from bs4 import BeautifulSoup as bs
import  re
from urllib import request

# urlsave = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
}



def getHref():
    for j in range(5,0,-1):
        resp = requests.get("http://ipo.csrc.gov.cn/infoBlock.action?pageNo="+ str(j) +"&temp=&temp1=&blockId=1&block=1&blockType=byBlock", headers=headers)
        data = resp.content.decode("utf-8", "ignore")
        hrefs = bs(data, "html.parser").find_all('a', href=re.compile(".+\.pdf"))
        companys = bs(data, "html.parser").find_all('td', align="left", width="30%")
        # print(hrefs)
        # print(companys)
        print("==============================", j)
        count = 0
        for i in hrefs:
            # try:
                urldown = "http://ipo.csrc.gov.cn/" + i["href"]
                companyName = companys[count].text.strip()
                count = count + 1
                response = request.urlopen(urldown)
                file = open('D:\\证监会招股说明书\\' + companyName + ".pdf", 'wb')
                file.write(response.read())
                file.close()
                print(companyName, count)
            # except Exception as e:
            #     print(e.)
            #     pass
            # urlsave.append("http://ipo.csrc.gov.cn/" + str(i["href"]))




if __name__ == "__main__":
    getHref()