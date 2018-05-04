from NewUpdate.other import CompanyProfile, ForeignExchangeAndRateOfInterest, FuturesActive, FuturesVar, StockInfo, \
    TakeAPosition, TTM, ZX_index
import time
import logging
from apscheduler.schedulers.blocking import BlockingScheduler


class Action():
    def __init__(self):

        pass

    def zxIndex(self,nowtime):
        """中信指数"""
        ZX_index.ZX_index().start(nowtime)

    def futuresVar(self,nowtime):
        """分合约行情数据"""
        FuturesVar.FuturesVar().start(nowtime)

    def futuresActive(self,nowtime):
        """活跃行情数据"""
        FuturesActive.FuturesActive().start(nowtime)

    def foreignExchangeAndRateOfInterest(self,nowtime):
        """利率和外汇"""
        ForeignExchangeAndRateOfInterest.ForeignExchangeAndRateOfInterest().start(nowtime)

    def takeAPosition(self,nowtime):
        """持仓数据"""
        TakeAPosition.TakeAPosition().start(nowtime)

    def stockInfo(self,nowtime):
        """股票基本资料"""
        StockInfo.StockInfo().start(nowtime)

    def companyProfile(self):
        """上市公司基本资料"""
        CompanyProfile.CompanyProfile().start()

    def ttm(self,nowtime):
        """TTM"""
        TTM.TTM().start(nowtime)

    def start(self):

        nowtime = time.strftime("%Y-%m-%d", time.localtime())

        # #中信指数
        # try:
        #     self.zxIndex("2018-03-21")
        # except :
        #     print("中信指数导入有误")
        #     return
        #
        # #分合约行情数据
        # try:
        #     self.futuresVar("2018-03-21")
        # except:
        #     print("分合约行情数据导入有误")
        #     return
        #
        # #活跃行情数据
        # try:
        #     self.futuresActive("2018-03-21")
        # except:
        #     print("活跃行情数据导入有误")
        #     return
        #
        # #利率和外汇
        # try:
        #     self.foreignExchangeAndRateOfInterest("2018-03-21")
        # except:
        #     print("利率和外汇导入有误")
        #     return

        #持仓数据
        try:
            self.takeAPosition('2018-03-21')
        except:
            print("持仓数据导入有误")
            return

        # #股票基本资料
        # try:
        #     self.stockInfo(nowtime)
        # except:
        #     print("股票基本资料导入有误")
        #     return

        #上市公司基本资料
        # try:
        #     self.companyProfile()
        # except:
        #     print("上市公司基本资料导入有误")
        #     return
        #
        # print("全部导入成功")

if __name__ == '__main__':

    Action().start()

    # # 主函数入口
    # log = logging.getLogger('apscheduler.executors.default')
    # log.setLevel(logging.INFO)  # DEBUG
    #
    # fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    # h = logging.StreamHandler()
    # h.setFormatter(fmt)
    # log.addHandler(h)
    # print('start to do it')
    # sched = BlockingScheduler()
    # sched.add_job(Action().start, "cron", month="*", day_of_week='mon-fri', hour="23", minute="50")
    # sched.start()