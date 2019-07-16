import threading
import time

from entity.SFC import SFC
from entity.SFCList import sfcListSingleton
from entity.VNF import VNF
from entity.VNFList import vnfListSingelton
from migration.VNFMigration import VNFMigration
from monitor.SFCInitialFormed import SFCInitialFormed
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

# 方法调用：可靠性监测模块中的可靠性监测方法
"""SFCList为空，先去试试SFC初次形成模块，生成SFC,存入到文件中，作为系统的输入//或者直接将SFCList生成，作为输入参数读入到系统中"""
# SFCReliabilityMonitorInstance = SFCReliabilityMonitor()
# SFCReliabilityMonitorInstance.reliability_monitor()
migration = VNFMigration()

def get_SFC_relialibility(VNF_list):
    SFCReliability = 1
    for i in range(len(VNF_list)):
        vnfid = VNF_list[i]
        VNFInstance = VNF(vnfid,
                          vnfListSingelton.dict_VNFListType[vnfid],
                          vnfListSingelton.dict_VNFRequestCPU[vnfid],
                          vnfListSingelton.dict_VNFRequestMemory[vnfid],
                          vnfListSingelton.dict_locatedVMID[vnfid],
                          vnfListSingelton.dict_locatedSFCIDList[vnfid],
                          vnfListSingelton.dict_numbersOnSFCList[vnfid],
                          vnfListSingelton.dict_VNFReliability[vnfid])
        print("VNF的可靠性为： %f" % VNFInstance.getVNFRliability(vnfid))
        SFCReliability *= VNFInstance.getVNFRliability(vnfid)
    print("SFC的新的可靠性为：%f" % SFCReliability)
    return SFCReliability

get_SFC_relialibility([7,8,9])

"""测试通过"""
# migration.judgingIfNodeOverload(1)
# migration.migrateVNFsofOneSFC()
"""测试通过"""
"""5代表vnf,1代表位于SFC1上"""
# migration.findDestinationForVNF(5, 1)
"""测试通过"""
# migration.findSFCWithMinReliability()

"""形成模块测试完成"""
# 调用初始化形成模块
# vnftypelist = [1, 2, 3]
# vnftypelist = [3, 4]
# vnftypelist = [2, 3, 4]
# vnftypelist = [1,2,3,4,5]
# relibilty = 0.5
# cpulist = [60, 60, 60, 60, 60]
# memorylist = [60, 60, 60, 60, 60]
# delay = 200
# 括号不能少！！
# SFCInitialFormed().SFC_initial_formed(delay, relibilty, vnftypelist, cpulist, memorylist)
# SFCInitialFormed().SFC_score(delay, len(vnftypelist))
# SFCInitialFormed().delaymin()
# ALLSFCList = sfcListSingleton.getSFCList()
# print("列表长度为：%d" % len(ALLSFCList))
