import threading
import time

from entity.SFCList import sfcListSingleton
from monitor.SFCReliabilityMonitor import SFCReliabilityMonitor

"""系统入口"""
# 每隔一段固定的时间打印一次
# def mytimer():
#     print("hello ")
#     global timer
#     # 重复构造定时器
#     timer = threading.Timer(2, mytimer)
#     timer.start()
# # 定时调度
# timer = threading.Timer(2, mytimer)
# timer.start()
# 50秒后停止定时器
# time.sleep(10)
# timer.cancel()

# count = 0
# starttime = time.perf_counter()
# sleepTime = 2
# while(True):
#     print("hello")
#     count += 1
#     sleeptime = 2
#     time.sleep(sleeptime)
#     endtime = time.perf_counter()
#     # if(count == 3):
#     #     print(endtime - starttime)
#     #     break
#     time.sleep(sleepTime)
#     print("睡眠时长为： %d" % sleepTime)
#     print("已经运行的时长为： %d" % int(endtime - starttime))
#     if (int(endtime - starttime) >= 30):
#         break

SFCReliabilityMonitorInstance = SFCReliabilityMonitor()
SFCReliabilityMonitorInstance.reliability_monitor()

# ALLSFCList = sfcListSingleton.getSFCList()
# print("列表长度为：%d" % len(ALLSFCList))
