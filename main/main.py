import threading
import time

from entity.PhysicalNodeList import nodeListSingelton
from entity.SFC import SFC
from entity.SFCList import sfcListSingleton
from entity.VM import VM
from entity.VMList import vmListSingelton
from entity.VNF import VNF
from entity.VNFList import vnfListSingelton
from migration.MigrationCostCaculation import MigrationCostCaculation
from migration.MigrationPlanEvaluation import MigrationPlanEvaluation
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
migration.migrateVNFsofOneSFC()

# MigrationCostCaculation().getDelayIncreationOfSFC(1, 16)
# delay = SFC(1,sfcListSingleton.dict_maxDelay[1],
#                   sfcListSingleton.dict_minReliability[1],
#                   sfcListSingleton.dict_VNFList[1],
#                   sfcListSingleton.dict_createdtime[1]).getDelayBetweenPhysicalNode(5,6)
# print("delay 增量为： %f" %delay)
# beforelist = [5]
# afterlist = [6]
# MigrationCostCaculation().getDelayIncreationOfSFC1(1, beforelist, afterlist)


"""测试获取SFC可靠性方法"""
# def get_SFC_relialibility(VNF_list):
#     SFCReliability = 1
#     for i in range(len(VNF_list)):
#         vnfid = VNF_list[i]
#         VNFInstance = VNF(vnfid,
#                           vnfListSingelton.dict_VNFListType[vnfid],
#                           vnfListSingelton.dict_VNFRequestCPU[vnfid],
#                           vnfListSingelton.dict_VNFRequestMemory[vnfid],
#                           vnfListSingelton.dict_locatedVMID[vnfid],
#                           vnfListSingelton.dict_locatedSFCIDList[vnfid],
#                           vnfListSingelton.dict_numbersOnSFCList[vnfid],
#                           vnfListSingelton.dict_VNFReliability[vnfid])
#         # print("VNF的可靠性为： %f" % VNFInstance.getVNFRliability(vnfid))
#         SFCReliability *= VNFInstance.getVNFRliability(vnfid)
#     print("原始方法，SFC的可靠性为：%f" % SFCReliability)
#     return SFCReliability
# get_SFC_relialibility([7,8,9])

"""更新获取SFC可靠性的方法，不通过直接读取VNF文件，而是通过读取所在物理节点的可靠性计算"""
"""将更新的VNF的id和新的物理节点的id传入"""
# def get_SFC_relialibility1(vnflist, updatevnfid, nodeid):
#     SFCReliability = 1
#     for i in range(len(vnflist)):
#         vnfid = vnflist[i]
#         if vnfid == updatevnfid:
#             nodeid = nodeid
#             SFCReliability *= nodeListSingelton.dict_provided_reliablity[nodeid]
#         else:
#             VNFInstance = VNF(vnfid,
#                               vnfListSingelton.dict_VNFListType[vnfid],
#                               vnfListSingelton.dict_VNFRequestCPU[vnfid],
#                               vnfListSingelton.dict_VNFRequestMemory[vnfid],
#                               vnfListSingelton.dict_locatedVMID[vnfid],
#                               vnfListSingelton.dict_locatedSFCIDList[vnfid],
#                               vnfListSingelton.dict_numbersOnSFCList[vnfid],
#                               vnfListSingelton.dict_VNFReliability[vnfid])
#             # 读取所在的VM
#             vmid = VNFInstance.get_VM_id(vnfid)
#             vmInstance = VM(vmid, vmListSingelton.dict_VMRequestCPU[vmid],
#                             vmListSingelton.dict_VMRequestMemory[vmid],
#                             vmListSingelton.dict_VMLocatedPhysicalnode[vmid],
#                             vmListSingelton.dict_VMReliability[vmid])
#             nodeid = vmInstance.get_physicalNode_id(vmid)
#             SFCReliability *= nodeListSingelton.dict_provided_reliablity[nodeid]
#         print("更新的方法，SFC的可靠性为：%f" % SFCReliability)
#         return SFCReliability
# get_SFC_relialibility1([7,8,9], 0, 0)

# migration.migrateVNFsofOneSFC()

"""测试通过"""
# migration.judgingIfNodeOverload(1)

"""测试通过"""
"""5代表vnf,1代表位于SFC1上"""
# migration.findDestinationForVNF(5, 1)
# migration.judgeConstrain2(5, 6, 1)
"""测试通过"""
# migration.findSFCWithMinReliability()

"""SFC初始形成模块测试完成"""
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
