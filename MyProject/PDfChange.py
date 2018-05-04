# -*- coding: utf-8-*-
import importlib
import sys
import os
import  pymysql

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser, PDFDocument

importlib.reload(sys)

def parse(_path,reportTime,company,security,reportTitle,stockCode,cor, conn):
    # try:
        fp = open('D:\\文件\\' + _path, 'rb')
        praser_pdf = PDFParser(fp)
        doc = PDFDocument()
        praser_pdf.set_document(doc)
        doc.set_parser(praser_pdf)
        doc.initialize()

        if not doc.is_extractable:
            print("次PDF文件不能别解析")
            return
            # raise PDFTextExtractionNotAllowed
        else:
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)

            value = ""
            count = 0                       # 要取公告信息的下面几行数据的计数器
            noticeCount = 0;                # “公告”出现次数的计数器
            # haveNotice = ""                 # 用来存储公告是否已有

            noticeInfo = ""  # 公告的信息
            noticeDetailInfo = []  # 公告以下文章的具体信息
            riskInfo = []  # 风险提示的信息
            analystInfo = []  # 分析师的信息
            stockRateInfo = []  # 股票评级的信息
            stoceExpectInfo = []  # 股票的预测信息

            noticeDetailInfos = ""  # 公告以下文章的具体信息(此字段整合数据用)
            riskInfos = ""  # 风险提示的信息(此字段整合数据用)
            analystInfos = ""  # 分析师的信息(此字段整合数据用)
            stockRateInfos = ""  # 股票评级的信息(此字段整合数据用)
            stoceExpectInfos = ""  # 股票的预测信息(此字段整合数据用)

            noticeInfoNextLine = []         # 公告信息的具体数据
            riskInfoNextLine = ""           # 风险提示的具体数据
            analystInfoNextLine = ""       # 证券分析师的具体数据

            for page in doc.get_pages():        # doc.get_pages(),循环遍历每一页的内容

                interpreter.process_page(page)
                layout = device.get_result()

                for out in layout:  # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                    # 判断是否含有get_text()方法，图片之类的就没有
                    # if hasattr(out,"get_text"):
                    if isinstance(out, LTTextBoxHorizontal):
                        results = out.get_text()
                        results = results.strip().replace("\n", "").replace(" ", "")
                        print(results.__len__(), results)

                        # if "已有公告" in haveNotice:
                        #     noticeCount += 1
            #             if ("公司" in value and "公告，" in value and "资料来源" not in results and "数据来源" not in results) \
            #                     or ("公司" in value and "公告：" in value and "资料来源" not in results and "数据来源" not in results) \
            #                     or ("公司" in value and "公告" in value and "资料来源" not in results and "数据来源" not in results) \
            #                     or ("事件：" in value) or ("【事件】" in value) or ("事件描述：" in value):
            #                 tag = re.search(re.compile("一、|二、|三、|1、|2、|3、|（1）|（2）|（3）|（4）|【一】|【二】|【三】|【四】||||●|||◎|评论"), results)
            #                 if tag is None:
            #                     if count < 3:
            #                         noticeInfoNextLine.append(results)
            #                         print("公告next~~~~~", results.__len__(), results)
            #                         count = count + 1
            #                         noticeCount = noticeCount + 1
            #                 else:
            #                     count = 0
            #                     value = ""
            #
            #             elif  "风险提示" in value :
            #                 riskInfoNextLine = results
            #                 print("风险提示next~~~~~", results.__len__(), results)
            #                 value = ""
            #             elif "分析师" in value :
            #                 analystInfoNextLine = results
            #                 print("分析师next~~~~~", results.__len__(), results)
            #                 value = ""
            #             else:
            #                 # 重要事项
            #                 if ("公司" in results and "公告，" in results and "资料来源" not in results and "数据来源" not in results and "公司研究/公告点评" not in results)\
            #                         or ("公司" in results and "公告：" in results and "资料来源" not in results and "数据来源" not in results and "公司研究/公告点评" not in results) \
            #                         or ("公司" in results and "公告" in results and str(results).__len__() >=2
            #                             and "资料来源" not in results and "数据来源" not in results and "公司研究/公告点评" not in results) \
            #                         or ("事件：" in results) or ("【事件】" in results) or ("事件描述：" in results):
            #                     if noticeCount == 0:
            #                         if str(results).__len__() > 65:
            #                             print("公告~~~~~", results)
            #                             noticeInfo = results.strip().strip("[Table_Summary]")
            #                             noticeCount = noticeCount + 1
            #                             # haveNotice = "已有公告"
            #                         elif str(results).__len__() <= 65:
            #                             print("公告******", results)
            #                             noticeInfoNextLine.append(results.strip().strip("[Table_Summary]"))
            #                             value = results
            #
            #                 if "一、" in results or "二、" in results or "三、" in results or "四、" in results or "五、" in results or "1、" in results \
            #                         or "2、" in results or "3、" in results or "4、" in results or "5、" in results or "" in results \
            #                         or "" in results or "" in results or "●" in results or "" in results or "" in results or "【一】" in results \
            #                         or "【二】" in results or "【三】" in results or "【四】" in results or "（1）" in results or "（2）" in results \
            #                         or "（3）" in results or "（4）" in results or "" in results or "※" in results:
            #                     noticeDetailInfo.append(str(results).strip().strip("[Table_Summary]").strip())
            #                     print("公告desc~~~~~~", results.__len__(), results)
            #
            #
            #                 # 证券分析师
            #                 if "证券分析师：" in results or "分析师：" in results or "（分析师）" in results:
            #                     analystInfo.append(results.strip())
            #                     print("分析师~~~~~", results.__len__(), results)
            #                 elif "分析师" in results:
            #                     if str(results).__len__() <= 4:
            #                         analystInfo.append(results.strip())
            #                         print("分析师~~~~~", results.__len__(), results)
            #                         value = results
            #
            #                 # 股票增持状态
            #                 if "增持" in results or "推荐" in results or "买入" in results:
            #                     stockRateInfo.append(results.strip())
            #                     print("评级~~~~~", results.__len__(), results)
            #
            #                 # 预测
            #                 if ("预测" in results and "每股收益" in results) or ("EPS" in results and "为" in results) or (
            #                         "预计" in results and "元" in results) or ("EPS" in results and "元" in results and "EPS（元）" not in results) \
            #                         or ("预计" in results and "EPS" in results) or ("预测" in results and "EPS" in results) \
            #                         or ("预测" in results and "PE" in results) or ("预计" in results and "PE" in results) \
            #                         or ("P/E" in results and "评级" in results) or ("PE" in results and "评级" in results) \
            #                         or ("预测" in results and "评级" in results) or ("归母净利润" in results and "为" in results) \
            #                         or ("我们预计公司" in results) or ("公司为国内乃至全球" in results) or ("盈利预测与估值" in results) \
            #                         or ("P/E" in results and "倍" in results) or ("PE" in results and "为" in results) \
            #                         or ("预测" in results and "利润" in results) or ("预测" in results and "收入" in results) \
            #                         or ("EPS" in results and "倍" in results) or ("X" in results and "评级" in results) \
            #                         or ("预计公司" in results and "净利润" in results) or ("倍" in results and "评级" in results):
            #                     stoceExpectInfo.append(results.strip())
            #                     print("预测~~~~~~", results.__len__(), results)
            #
            #                 # 风险
            #                 if "风险提示" in results or "风险因素" in results:
            #                     if str(results).__len__() <= 7:
            #                         riskInfo.append(results.strip())
            #                         print("风险提示~~~~~~", results.__len__(), results)
            #                         value = results
            #                     else:
            #                         riskInfo.append(results.strip())
            #                         print("风险提示~~~~~~", results.__len__(), results)
            #
            # # 公告或者事件信息
            # if noticeInfoNextLine.__len__() != 0:
            #     for i in range(noticeInfoNextLine.__len__()):
            #         noticeInfo += str(noticeInfoNextLine[i]).strip()
            #
            # #  研报的具体数据
            # for i in range(noticeDetailInfo.__len__()):
            #     noticeDetailInfos += str(noticeDetailInfo[i])
            #
            # # 风险提示
            # if riskInfoNextLine.__len__() == 0:
            #     if riskInfo.__len__() != 0:
            #         riskInfos = str(riskInfo[0])
            # elif riskInfoNextLine.__len__() != 0:
            #     if riskInfo.__len__() != 0:
            #         riskInfos = str(riskInfo[0]) + str(riskInfoNextLine)
            #
            # # 分析师
            # if analystInfoNextLine == 0:
            #     if analystInfo.__len__() != 0:
            #         if str(analystInfo[0]).strip() != "分析师":
            #             analystInfos = str(analystInfo[0])
            # elif analystInfoNextLine != 0:
            #     if analystInfo.__len__() != 0:
            #         if str(analystInfo[0]).strip() != "分析师":
            #             analystInfos = str(analystInfo[0]) + str(analystInfoNextLine)
            #
            # # 股票的评级信息
            # if stockRateInfo.__len__() != 0:
            #     for i in range(stockRateInfo.__len__()):
            #         if str(stockRateInfo[i]).strip().__len__() < 12:
            #             # if "增持" in results or "推荐" in results or "买入" in results:
            #                 stockRateInfos = str(stockRateInfo[i])
            #
            # # 股票的预测信息
            # if stoceExpectInfo.__len__() != 0:
            #     for i in range(stoceExpectInfo.__len__()):
            #         stoceExpectInfos += str(stoceExpectInfo[i])
            #
            # print("公告+++++++++++++++", noticeInfo)
            # print("研报具体信息+++++++++++++++", noticeDetailInfos)
            # print("风险提示+++++++++++++++", riskInfos)
            # print("分析师+++++++++++++++", analystInfos)
            # print("股票评级+++++++++++++++", stockRateInfos)
            # print("预测+++++++++++++++", stoceExpectInfos)

            # 执行sq语句，将处理好的数据存入数据库
            # sql = "insert into companyreport(report_time,company,security,report_title,events_or_notice," \
            #       "notice_or_event_detail_info,stock_code,stock_rate_info,stock_expect_info,risk_info,analyst_info) " \
            #       "value('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
            #       % (str(reportTime), str(company), str(security), str(reportTitle), noticeInfo, noticeDetailInfos,
            #          str(stockCode),stockRateInfos,stoceExpectInfos,riskInfos,analystInfos)
            # cor.execute(sql)  # 执行对应的SQL语句
            # conn.commit()

    # except Exception as e:
    #     print("出现了异常", e)
    #     return

# 对时间进行格式化处理
def getTime(reportTime):
    year = reportTime[0:4]
    month = reportTime[4:6]
    day = reportTime[6:8]
    return str(year) + "-" + str(month) + "-" + str(day)


if __name__ == '__main__':

    # 打开数据库
    conn = pymysql.connect(host='192.168.123.24', user='root', passwd='123456', port=3306, db='searchreport', charset='utf8')
    cor = conn.cursor()  # 获取一个游标对象

    # 遍历本地磁盘的文件
    dirs = os.listdir("D:\\文件")
    for filePath in dirs:
        try:
            if str.find(filePath, '：') != -1:
                [fileName, reportTitle] = filePath.split('：')
                reportTitle = str(reportTitle).strip(".pdf")
                fileNameDesc = str(fileName).split("-")
                reportTime = fileNameDesc[0]
                securityName = fileNameDesc[1]
                desc = fileNameDesc[2]
                # [reportTime, securityName,desc] = str(fileName).split("-")
                reportTime = getTime(reportTime);
                if "（" in desc:
                    stockCode = str(desc).split("（")[1].strip("）")
                    company = str(desc).split("（")[0].strip()
                    print(reportTime, securityName, company, stockCode, fileName, reportTitle)
                    parse(filePath,reportTime,company,securityName,reportTitle,stockCode,cor,conn)
                else:
                    print(reportTime, securityName, fileName, reportTitle)
                    parse(filePath, reportTime,company,securityName,reportTitle,stockCode,cor,conn)
            else:
                fileName = filePath.strip(".pdf")
                fileSplit = fileName.split("-")
                reportTime = getTime(fileSplit[0])
                if "（" in desc:
                    stockCode = str(desc).split("（")[1].strip("）")
                    company = str(desc).split("（")[0].strip()
                    print(reportTime, securityName, company, stockCode, fileName, reportTitle)
                    parse(filePath, reportTime,company,securityName,reportTitle,stockCode,cor,conn)
                else:
                    print(reportTime, securityName, fileName, reportTitle)
                    parse(filePath, reportTime,company,securityName,reportTitle,stockCode,cor,conn)
        except Exception as e:
            print(e.__context__)
            pass

    #     关闭数据库连接
    cor.close()
    conn.close()



