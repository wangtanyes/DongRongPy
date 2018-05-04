# -*- coding: utf-8-*-

import importlib
import sys
import re
import os
import random
from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup

# 安装此模块使用 pip install pdfminer3k
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

'''
 解析pdf 文本，保存到txt文件中
'''
importlib.reload(sys)


def parse(path):
    fp = open(path, 'rb')  # rb以二进制读模式打开本地pdf文件
    # print("文件的名字是：", fp.name)
    # request = Request(url=_path, headers={'User-Agent': random.choice(user_agent)})  # 随机从user_agent列表中抽取一个元素
    # fp = urlopen(request) #打开在线PDF文档

    # 用文件对象来创建一个pdf文档分析器
    praser_pdf = PDFParser(fp)

    # 创建一个PDF文档
    doc = PDFDocument()

    # 连接分析器 与文档对象
    praser_pdf.set_document(doc)
    doc.set_parser(praser_pdf)

    # 提供初始化密码doc.initialize("123456")
    # 如果没有密码 就创建一个空的字符串
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        # 创建PDf资源管理器 来管理共享资源
        rsrcmgr = PDFResourceManager()

        # 创建一个PDF参数分析器
        laparams = LAParams()

        # 创建聚合器
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

        # 创建一个PDF页面解释器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一页的内容
        # doc.get_pages() 获取page列表
        for page in doc.get_pages():
            # 使用页面解释器来读取
            interpreter.process_page(page)

            # 使用聚合器获取内容
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，

            for out in layout:
                # 判断是否含有get_text()方法，图片之类的就没有
                # if hasattr(out,"get_text"):
                if isinstance(out, LTTextBoxHorizontal):
                    # with open(r'D:\\2.txt', 'r+') as f:
                    results = out.get_text()
                    # print("=========================" + results)
                    results = results.strip().replace("\n", "").replace(" ", "").replace("\t", "")

                    # print("=====================================================================")
                    # pat1 = re.compile(r"[^\d]+[^\s]+")
                    pat1 = re.compile(r'\D+\S+')
                    results = re.search(pat1, results)


                    if results is not None:
                        print(results.group())
                        # with open("d:\\2.txt", "a") as f:
                        #     f.writelines(results.group() + "\n")
                        #     f.flush()
                        #     print(results.group())

                        # if(results.__len__() >=4):
                        # f.writelines(results)
                        # f.flush()


if __name__ == '__main__':
    dirs = os.listdir("D:\\dataset")
    for filePath in dirs:
        if str.find(filePath, '：') != -1:

            print(os.path, "====================================")
            [fileName, reportTitle] = filePath.split('：')
            reportTitle = str(reportTitle).strip(".pdf")
            [reportTime, securityName,desc] = str(fileName).split("-")
            rex1 = re.compile(r'\d+\.\w{2}')
            rex2= re.compile(r'（\d+\.\w{2}）')
            company = str(desc).strip(re.search(re.compile(rex2),desc).group())
            stockCode = re.search(rex1,desc).group()
            startIndex = str(desc).index('（')
            endIndex = str(desc).index('）')

            print("D:\\dataset\\" + filePath,reportTime, securityName, company, stockCode, fileName, reportTitle)

            parse("D:\\dataset\\" + filePath)

        else:
            fileName = filePath.strip(".pdf")
            fileSplit = fileName.split("-")
            print([fileSplit[0], fileSplit[1], fileSplit[2], fileName])


    # url = "D:\\guokai.pdf"
    # parse(url)