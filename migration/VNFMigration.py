"""VNF迁移"""
import math

from entity.PhysicalNode import PhysicalNode
from entity.PhysicalNodeList import PhysicalNodeList
from entity.SFC import SFC
from entity.SFCList import sfcListSingleton
from entity.VM import VM
from entity.VNF import VNF
from migration.MigrationPlanEvaluation import MigrationPlanEvaluation


class VNFMigration():
    # 迁移一条SFC
    def migrateVNFsofOneSFC(self):
        # 每次迁移的这一条SFC应该是当前网络中可靠性最低的一条
        migratedsfcId = self.findSFCWithMinReliability()
        SfcInstance = SFC(migratedsfcId)
        # 迁移前此SFC的时延
        delayBefore = SfcInstance.get_SFC_delay(SfcInstance.getVNFList())
        # 迁移之前此SFC需要的资源（CPU+memory）
        requestedResourceBefore = SfcInstance.getSFCRequestedResource()
        # 判断此SFC上所有的VNF所处的节点是否过载
        (overloadNodeListId, migratedVNFList) = self.judgingIfNodeOverload(migratedsfcId)
        # 若是有物理节点过载
        if(overloadNodeListId != None):
            # 为每个migratedVNFList中的VNF计算其目的地
            # 存放所有位于migratedVNFList中的VNF的可以迁移的目的地列表，其存储的顺序以及大小与migratedVNFList一样，只是里边存储的为list
            destinationsForVNFList = []
            for i in range(len(migratedVNFList)):
                vnfId = migratedVNFList[i]
                """调用为VNF计算所有的目的地list"""
                destinationsForVNFList[i] = self.findDestinationForVNF(vnfId, migratedsfcId)
            """迁移方案为：选择migratedVNFList中的一个或者两个VNF进行迁移。将所有的迁移单个VNF和所有的迁移两个VNF的方案进行比较"""
            # 先计算所有迁移一个VNF的方案的代价,字典中存放的是迁移方案及其对应的代价
            maxPlanEvaluation = -9999
            bestPlan = [] # 存放该方案中需要迁移的VNF列表
            bestDes = [] # 存放最佳迁移方案中VNF所对应的目的地ID
            """所有只迁移一个VNF的方案"""
            for i in range(len(migratedVNFList)):
                vnf_id = migratedVNFList[i]
                vnfList = [vnf_id]
                for j in range(len(destinationsForVNFList)):
                    destinationList = [destinationsForVNFList[i][j]]
                    MigrationPlanEvaluationInstance = MigrationPlanEvaluation(migratedsfcId, delayBefore,
                                                                              requestedResourceBefore,
                                                                              vnfList, destinationList)
                    # 方案评分
                    planEvaluation = MigrationPlanEvaluation.evaluation()
                    if (planEvaluation < maxPlanEvaluation):
                        # 更新最高评分
                        maxPlanEvaluation = planEvaluation
                        # 更新最好方案
                        bestPlan = vnfList
                        bestDes = destinationList
            """所有迁移两个VNF的方案"""
            # 如何限制两个VNF入科同时迁移到一个物理节点呢？？
            # 1.先找出所有的两个VNF组合的情况 用两层循环
            # 存放的是待迁移的两个VNF组成的列表
            combineVNFList = []
            for i in range(len(migratedVNFList)):
                vnfid_a = migratedVNFList[i]
                for j in range(len(migratedVNFList)):
                    if(j > i):
                        vnfid_b = migratedVNFList[j]
                        combineVNFList.append([vnfid_a, vnfid_b])
            # 2.在找出所有组合中的符合目的地不重复的所有的迁移组合
            desNodeIdList = []
            for i in range(len(combineVNFList)):
                # 把列表中的组合分别取出，找出两个VNF迁移的不同搭配
                vnfid_a = combineVNFList[i][0]
                vnfid_b = combineVNFList[i][1]
                vnf_list = [vnfid_a, vnfid_b]
                destinationListForvnf_a = self.findDestinationForVNF(vnfid_a, migratedsfcId)
                destinationListForvnf_b = self.findDestinationForVNF(vnfid_b, migratedsfcId)
                for j in range(len(destinationListForvnf_a)):
                    desid_vnf_a = destinationListForvnf_a[j]
                    for k in range(len(destinationListForvnf_b)):
                        if(destinationListForvnf_b[k] != desid_vnf_a):
                            desid_vnf_b = destinationListForvnf_b[k]
                            desNodeIdList.append([desid_vnf_a, desid_vnf_b])
                            des_list = [desid_vnf_a, desid_vnf_b]
                            # 3.计算所有组合的评分
                            MigrationPlanEvaluationInstance = MigrationPlanEvaluation(migratedsfcId, delayBefore,
                                                                                      requestedResourceBefore,
                                                                                      vnf_list, des_list)
                            planEvalu = MigrationPlanEvaluationInstance.evaluation()
                            if(planEvalu > maxPlanEvaluation):
                                maxPlanEvaluation = planEvalu
                                bestPlan = vnf_list
                                bestDes = des_list
            return (maxPlanEvaluation, bestPlan, bestDes)
        else:
            """没有节点过载"""
            maxPlanEvaluation = -9999  # 当前的最高评分
            bestPlan = []  # 存放该方案中需要迁移的VNF列表
            bestDes = []  # 存放最佳迁移方案中VNF所对应的目的地ID
            # 保留三个拥有最大可靠性的VNF,vnfid1最大，vnfid2第二大，vnfid3第三大
            vnfListOnThisSFC = SfcInstance.getVNFList()
            vnfid1 = vnfListOnThisSFC[0]
            vnfid2 = vnfListOnThisSFC[0]
            vnfid3 = vnfListOnThisSFC[0]
            for i in range(len(vnfListOnThisSFC)):
                VNF_id = vnfListOnThisSFC[i]
                vnfInstance = VNF(VNF_id)
                reliability = vnfInstance.getVNFRliability(VNF_id)
                vnfInstance1 = VNF(vnfid1)
                vnfInstance2 = VNF(vnfid2)
                vnfInstance3 = VNF(vnfid2)
                if(reliability > vnfInstance1.getVNFRliability(vnfid1)):
                    vnfid3 = vnfid2
                    vnfid2 = vnfid1
                    vnfid1 = i
                elif(reliability > vnfInstance2.getVNFRliability(vnfid2)):
                    vnfid3 = vnfid2
                    vnfid2 = i
                elif(reliability > vnfInstance3.getVNFRliability(vnfid3)):
                    vnfid3 = i
            # 可以选择迁移vnfid1或者vnfid1和vnfid2或者vnfid1和vnfid2和vnfid3

            # 选择迁移vnfid1
                # 首先获取到vnfid1的所有的目的地节点,共有len(desNodeList)种方案
            desNodeList = self.findDestinationForVNF(vnfid1, migratedsfcId)
            vnf_list = [vnfid1]
            for i in range(len(desNodeList)):
                des_list1 = [desNodeList[i]]
                MigrationPlanEvaluationInstance = MigrationPlanEvaluation(migratedsfcId, delayBefore,
                                                                          requestedResourceBefore,
                                                                          vnf_list, des_list1)
                planEvalu = MigrationPlanEvaluationInstance.evaluation()
                if(planEvalu > maxPlanEvaluation):
                    maxPlanEvaluation = planEvalu
                    bestPlan = vnf_list
                    bestDes = des_list1

            # 选择迁移vnfid1和vnfid2这两个vnf
                # 首先为vnfid2寻找所有的des
            des_list2 = self.findDestinationForVNF(vnfid2, migratedsfcId)
            vnf_list = [vnfid1, vnfid2]
            # 找出所有的组合迁移方案(des_list1与des_list2中各选择一个，要不相同)
            for i in range(len(des_list1)):
                for j in range(len(des_list2)):
                    if(des_list1[i] != des_list2[j]):
                        des_list = [des_list1[i], des_list2[j]]
                        MigrationPlanEvaluationInstance = MigrationPlanEvaluation(migratedsfcId, delayBefore,
                                                                                  requestedResourceBefore,
                                                                                  vnf_list, des_list1)
                        planEvalu = MigrationPlanEvaluationInstance.evaluation()
                        if(planEvalu > maxPlanEvaluation):
                            maxPlanEvaluation = planEvalu
                            bestPlan = vnf_list
                            bestDes = des_list
            """迁移三个VNF的代码实现没有写"""
            # 返回最高评分、最佳方案（VNF列表和目的物理节点列表,两个列表的大小应该是相同的）
            return (maxPlanEvaluation, bestPlan, bestDes)

    # 迁移多条SFC
    def migrateVNFsofMultiSFC(self):

        return None

    # 寻找当前网络中可靠性最低的SFC,返回此SFC的ID
    def findSFCWithMinReliability(self):
        minReliability  = 100
        # 获取到网络中所有的SFC的ID的列表
        SFCList = sfcListSingleton
        for sfcId in SFCList:
            sfcInstance = SFC(sfcId)
            sfcReliability = sfcInstance.get_SFC_relialibility(sfcInstance.getVNFList())
            if (sfcReliability < minReliability):
                minReliability = sfcReliability
        return minReliability

    # 判断一条SFC上VNF们所在的物理节点们谁过载了，返回过载物理节点的list
    def judgingIfNodeOverload(self, sfcId):
        # 存放此SFC所经过的所有的过载的物理节点
        overloadNodeListId = []
        # 存放此SFC上所有位于过载物理节点上的VNF
        VNFonoverNodeListId = []

        sfcInstance = SFC(sfcId)
        vnfList = sfcInstance.getVNFList()
        for vnfId in vnfList:
            vnfInstance = VNF(vnfId)
            vmInstance = VM(vnfInstance.get_VM_id(vnfId))
            # 获取到此VNF所在的物理节点
            nodeId = vmInstance.get_physicalNode_id(vnfInstance.get_VM_id(vnfId))
            # 判断此节点是否过载
            nodeInstance = PhysicalNode(nodeId)
            nodeInstance.if_overloadState()
            overloadeState = nodeInstance.overloadeState
            if (overloadeState == True):
                VNFonoverNodeListId.append(vnfId)
                overloadNodeListId.append(nodeId)
        return (overloadNodeListId, VNFonoverNodeListId)

    # 为VNF计算迁移目的地列表
    def findDestinationForVNF(self, vnfId, migratedSFCId):
        # 存储所有可能的物理节点的id
        allsatidfiedNodeList = []
        # 满足约束条件的都可作为VNF迁移的目的地
        nodeIdList = PhysicalNodeList.getNodeList()
        for nodeId in nodeIdList:
            if(self.judgeIfIsDestination(vnfId, nodeId, migratedSFCId) == True):
                allsatidfiedNodeList.append(nodeId)
        return allsatidfiedNodeList

    # 判断某个物理节点是否是某个VNF迁移的目的地
    # 输入参数为vnf id（需要迁移的VNF的id） 与node id(待选的物理节点的id)，返回布尔值
    def judgeIfIsDestination(self, vnfId, nodeId, migratedSFCId):
        """根据约束条件判断"""
        # 第一个约束条件判断的结果存储在constrain1中
        constrain1 = self.judgeConstrain1(vnfId, nodeId, migratedSFCId)
        if(constrain1 == True):
            # 进行第二个约束条件的判断，将其存放在constrain2中
            constrain2 = self.judgeConstrain2(vnfId, nodeId, migratedSFCId)
            if(constrain2 == True):
                # 进行第三个约束条件的判断
                constrain3 = self.judgeConstrain3(vnfId, nodeId, migratedSFCId)
                if(constrain3 == True):
                    # 进行第四个约束条件的判断
                    constrain4 = self.judgeConstrain4(vnfId, nodeId, migratedSFCId)
                    if(constrain4 == True):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    # 判断第一个约束条件是否满足，满足返回True，否则返回False
    def judgeConstrain1(self, vnfId, nodeId, migratedSFCId):
        # 约束1.1 迁移后的节点可靠性大于迁移前VNF所在节点的可靠性
        VNFInstance = VNF(vnfId)
        # 迁移之前/当前的可靠性（VNF的可靠性也就是物理节点的可靠性）
        currentReliability = VNFInstance.getVNFRliability(vnfId)
        # 若是迁移到nodeId,那么迁移之后的可靠性
        nodeInstance = PhysicalNode(nodeId)
        afterReliability = nodeInstance.get_reliability(nodeId)
        # 判断是否可靠性增大，即满足第一个约束条件
        if (afterReliability > currentReliability):
            # 满足约束条件1.1
            # 判断迁移条件1.2 迁移后整条SFC的可靠性是否大于需求值
            SFCInstance = SFC(migratedSFCId)
            vnfList = SFCInstance.getVNFList()
            requestSFCReliability = SFCInstance.getRequestMinReliability()
            vnfListCopy = vnfList
            # 找到vnfListCopy中id为vnfId的vnf,将它的物理节点换掉，换成迁移之后的node
            for vnf_id in vnfListCopy:
                if(vnf_id == vnfId):
                    VNFInstance = VNF(vnf_id)
                    VMId = VNFInstance.get_VM_id()
                    VMInstance = VM(VMId)
                    # 此时vnfListCopy中的VNF已经更新完了
                    VMInstance.setPhysicalNodeId(nodeId)
            # 使用更新完的vnfListCopy，放入到新的迁移完的SFC中，计算迁移之后的SFC的可靠性
            currentSFCReliability = SFCInstance.get_SFC_relialibility(vnfListCopy)
            if(currentSFCReliability > requestSFCReliability):
                return True
        else:
            # 不满足约束1
            return False

    # 判断第二个约束条件是否满足，满足返回True，否则返回False
    def judgeConstrain2(self, vnfId, nodeId, migratedSFCId):
        # 约束2 迁移之后SFC的时延增加不可超过一个σ（参数设置，以毫秒记）
        delayIncreace = 20 # 设时延的最大增量为20ms
        SFCInstance = SFC(migratedSFCId)
        vnfList = SFCInstance.getVNFList()
        # 迁移之前SFC的时延
        currentDelay = SFCInstance.get_SFC_delay(vnfList)
        # 创建一个VNF副本，用于更新vnf
        vnfListCopy = vnfList
        for vnf_id in vnfListCopy:
            if(vnf_id == vnfId):
                VNFInstance = VNF(vnf_id)
                VMId = VNFInstance.get_VM_id()
                VMInstance = VM(VMId)
                # 此时vnfListCopy中的VNF已经更新完了
                VMInstance.setPhysicalNodeId(nodeId)
        # 使用更新完的VNFList来计算新的SFC的时延
        afterDelay = SFCInstance.get_SFC_delay(vnfListCopy)
        if(afterDelay - currentDelay <= delayIncreace):
            return True
        else:
            return False

    # 判断第三个约束条件是否满足，满足返回True，否则返回False
    def judgeConstrain3(self, vnfId, nodeId, migratedSFCId):
        # 约束3 资源约束，即待迁移VNF迁移到新的物理节点上时，所需要的资源小于当前物理节点可提供的资源
        VNFInstance = VNF(vnfId)
        # VNF需要的CPU和内存资源数量
        requestCPU = VNFInstance.getVNF_request_CPU()
        requestMemory = VNFInstance.getVNF_request_Memory()
        # 新的物理节点可以提供的资源
        nodeInstance = PhysicalNode(nodeId)
        availableCPU = nodeInstance.getAvailable_CPU()
        availableMemory = nodeInstance.getAvailable_Memory()
        # 注意啦！！！不能在这里减去物理节点的CPU和内存资源，因为此时并没有真的迁移到这个物理节点上来。
        # 判断资源是否满足要求
        if(requestCPU < availableCPU and requestMemory < availableMemory):
            return True
        else:
            return False

    # 判断第四个约束条件是否满足，满足返回True，否则返回False
    def judgeConstrain4(self, vnfId, nodeId, migratedSFCId):
        # 约束4 网络中所有节点的负载偏差程度小于η，即负载均衡条件
        # 1.首先要对待迁移VNF所涉及的物理节点进行一个更新，两部分：
        # 当前位于的物理节点资源加上VNF占用的部分，目的地物理节点资源减去VNF占用的部分
        VNFInstance = VNF(vnfId)
        vmId = VNFInstance.get_VM_id()
        VMInstance = VM(vmId)
        nodeBeforeId = VMInstance.get_physicalNode_id(vmId)
        nodeBefore = PhysicalNode(nodeBeforeId)
        # 迁移之前VNF所在的物理机
        nodeBeforeCopy = nodeBefore
        # 迁移的VNF所占用的资源
        cpuResource = VNFInstance.getVNF_request_CPU()
        memoryResource = VNFInstance.getVNF_request_Memory()
        # 原物理机的副本加上此资源
        nodeBeforeCopy.addAvailable_CPU(nodeBeforeId, cpuResource)
        nodeBeforeCopy.addAvailable_Memory(nodeBeforeId, memoryResource)
        # 资源利用率
        (cpu_rate_before, memory_rate_before) = nodeBeforeCopy.occupancy_rate_resource()
        resource_rate_before = (cpu_rate_before + memory_rate_before)/2
        # 迁移之后的物理机减去此资源
        nodeAfter = PhysicalNode(nodeId)
        nodeAfterCopy = nodeAfter
        nodeAfterCopy.deleteAvailable_CPU(nodeId, cpuResource)
        nodeAfterCopy.deleteAvailable_Memory(nodeId, memoryResource)
        (cpu_rate_after, memory_rate_after) = nodeAfterCopy.occupancy_rate_resource()
        resource_rate_after = (cpu_rate_after + memory_rate_after)/2

        # 2.获取到网络中迁移状态之后的所有节点及它们的负载程度（用资源利用率来衡量）
        allNodeList = PhysicalNodeList.getNodeList()
        # 存储网络中所有的物理节点的负载
        loadList = []
        for i in range(len(allNodeList)):
            nodeid = allNodeList[i]
            if(nodeid == nodeId):
                loadList[i] = resource_rate_after
            elif(nodeid == nodeBeforeId):
                loadList[i] = resource_rate_before
            else:
                node = PhysicalNode(nodeid)
                (cpu_rate, memo_rate) = node.occupancy_rate_resource()
                loadList[i] = (cpu_rate + memo_rate)/2

        # 3.判断负载偏差程度是否满足预先设定的阈值，即小于η
        # 计算负载的平均值
        # 物理节点的总共负载
        totalLoad = 0
        # 物理节点的平均负载
        avgLoad = 0
        # 负载的偏差程度（网络中所有物理节点的负载均衡程度）
        loadDeviationDegree = 0
        # 参数设置
        η = 0.1 # 参数设置
        temp = 0
        for load in loadList:
            totalLoad += load
        # 平均负载
            avgLoad = totalLoad/len(loadList)
        # 总体的负载偏差程度
        for load in loadList:
            temp += (load - avgLoad) * (load - avgLoad)
        loadDeviationDegree = math.sqrt(temp)/len(loadList)

        if(loadDeviationDegree <= η):
            return True
        else:
            return False

        """未完待续"""
