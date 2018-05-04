#-*-coding:utf-8 -*-
import sys
import pprint
# reload(sys)
# sys.setdefaultencoding('utf-8')
import requests
urldict={}
import os
# try:
#     os.mkdir('D:\\output')
# except:
#     pass

#从巨潮资讯解析出pdf的真实下载地址
# f=open('stkcd.csv','r')
f=open('D:\\深证A.txt','r', encoding='utf-8')
fout=open('D:\\深证A\\urls.csv','w')
for line in f:
    stkcd = str(line[2:9]).strip()
    # print(stkcd)
    if stkcd is not None and stkcd != "":
    # 这一行把“招股说明书”换成　“年报”　“半年报”　之类的，即可批量下载其他的公告
        response=requests.get('http://www.cninfo.com.cn/cninfo-new/fulltextSearch/full?searchkey='+stkcd+'+招股意向书&sdate=&edate=&isfulltext=false&sortName=nothing&sortType=desc&pageNum=1')
        dict=response.json()
        # print(dict)
        for i in dict['announcements']:
            if '摘要' not in i['announcementTitle']:
                # print(i['announcementTitle'])
                url='http://www.cninfo.com.cn/'+i['adjunctUrl']
                # print(url)
                secname=i['secName']
                date=i['adjunctUrl'][10:20]
                urldict.update({stkcd+'-'+secname+'-'+date:url})
                csvtowrite=stkcd+','+secname+','+date+','+url+'\n'
                fout.write(str(csvtowrite.encode('utf-8')))
# pprint.pprint(urldict)
fout.close()

#根据解析出的pdf地址下载到output，并重命名成有规律的文件
from urllib import request
for name in urldict:
    try:
        url=urldict[name]
        response = request.urlopen(url)
        file = open('D:\\深证A\\'+name+".pdf", 'wb')
        file.write(response.read())
        file.close()
        print(name)
    except Exception as e:
        print(e.__context__)
        pass