from NewUpdate.fundamentals import SpotPrice,FinancialIndexAndFixedInvestment,ImportAndExport,Macroeconomic
import time
import datetime
from datetime import timedelta
import logging
from apscheduler.schedulers.blocking import BlockingScheduler


class Action():

    def __init__(self):

        pass

    def spotPrice(self,fritime):
        """价格数据"""
        SpotPrice.SpotPrice().start(fritime)

    def macroeconomic(self,fritime):
        """宏观数据"""
        SpotPrice.SpotPrice().start(fritime)

    def importAndExport(self,fritime):
        """进出口"""
        ImportAndExport.ImportAndExport().start(fritime)

    def financialIndexAndFixedInvestment(self,fritime):
        """财务指标和行业固定投资"""
        FinancialIndexAndFixedInvestment.FinancialIndexAndFixedInvestment().start(fritime)

    def start(self):
        #获取昨天时间
        mytime = datetime.datetime.now() - timedelta(days=1)
        fritime = mytime.strftime('%Y-%m-%d')

        #价格数据
        try:
            self.spotPrice('2018-03-20')
        except:
            print("价格数据导入有误")
            return

        # #宏观数据
        # try:
        #     self.macroeconomic(fritime)
        # except:
        #     print("宏观数据导入有误")
        #     return
        #
        # #进出口
        # try:
        #     self.importAndExport(fritime)
        # except:
        #     print("进出口导入有误")
        #     return
        #
        # #财务指标和行业固定投资
        # try:
        #     self.financialIndexAndFixedInvestment(fritime)
        # except:
        #     print("进出口导入有误")
        #     return


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

