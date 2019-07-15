"""VNF迁移"""
import math

from entity.PhysicalNode import PhysicalNode
from entity.PhysicalNodeList import PhysicalNodeList, nodeListSingelton
from entity.SFC import SFC
from entity.SFCList import sfcListSingleton, SFCList
from entity.VM import VM
from entity.VMList import vmListSingelton
from entity.VNF import VNF
from entity.VNFList import VNFList, vnfListSingelton
from migration.MigrationPlanEvaluation import MigrationPlanEvaluation


class VNFMigration():
    print("this is VNFMigration class")
    # 迁移一条SFC
    def migrateVNFsofOneSFC(self):
        print("-----------------这是迁移一条SFC的方法本体---------------------")
        # 每次迁移的这一条SFC应该是当前网络中可靠性最低的一条
        migratedsfcId = self.findSFCWithMinReliability()
        print("//////////////migratedsfcId = %d" % migratedsfcId)
        SfcInstance = SFC(migratedsfcId,
                          sfcListSingleton.dict_maxDelay[migratedsfcId],
                          sfcListSingleton.dict_minReliability[migratedsfcId],
                          sfcListSingleton.dict_VNFList[migratedsfcId],
                          sfcListSingleton.dict_createdtime[migratedsfcId]
                          )
        # 迁移前此SFC的时延
        delayBefore = SfcInstance.get_SFC_delay(SfcInstance.getVNFList())
        print("//////////////////迁移前此SFC的时延为：%f" % delayBefore)
        # 迁移之前此SFC需要的资源（CPU+memory）
        requestedResourceBefore = SfcInstance.getSFCRequestedResource()
        print("//////////////////迁移前此SFC的需要资源为：%f" % requestedResourceBefore)
        # 判断此SFC上所有的VNF所处的节点是否过载
        (overloadNodeListId, migratedVNFList) = self.judgingIfNodeOverload(migratedsfcId)
        print("这是迁移一条SFC方法内，过载情况：overloadNodeListId = ")
        print(overloadNodeListId)
        print("len(overloadNodeListId) = %d " % len(overloadNodeListId))
        # 若是有物理节点过载
        if(len(overloadNodeListId) != 0):
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
                    planEvaluation = MigrationPlanEvaluationInstance.evaluation()
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
            print("没有节点过载，进入else语句中")
            maxPlanEvaluation = -9999  # 当前的最高评分
            bestPlan = []  # 存放该方案中需要迁移的VNF列表
            bestDes = []  # 存放最佳迁移方案中VNF所对应的目的地ID
            # 保留三个拥有最大可靠性的VNF,vnfid1最大，vnfid2第二大，vnfid3第三大
            vnfListOnThisSFC = SfcInstance.getVNFList()
            print("这是迁移一条SFC方法中的else语句中，vnfListOnThisSFC = ")
            print(vnfListOnThisSFC)
            vnfid1 = vnfListOnThisSFC[0]
            vnfid2 = vnfListOnThisSFC[1]
            vnfid3 = vnfListOnThisSFC[2]
            i = 0
            while(i < len(vnfListOnThisSFC)):
                print("进入WHILE循环，i = %d " %i)
                VNF_id = vnfListOnThisSFC[i]
                print("vnfListOnThisSFC[i] = %d" %vnfListOnThisSFC[i])
                j = i
                while(j < len(vnfListOnThisSFC)):
                    vnf_id = vnfListOnThisSFC[j]
                    print("vnfListOnThisSFC[j] = %d" % vnfListOnThisSFC[j])
                    if(vnfListSingelton.dict_VNFReliability[VNF_id] <
                            vnfListSingelton.dict_VNFReliability[vnf_id]):
                        temp = vnfListOnThisSFC[i]
                        vnfListOnThisSFC[i] = vnfListOnThisSFC[j]
                        vnfListOnThisSFC[j] = temp
                    j += 1
                i += 1
            print("这是迁移一条SFC方法中的else语句中，vnfListOnThisSFC = ")
            print(vnfListOnThisSFC)
            vnfid1 = vnfListOnThisSFC[0]
            vnfid2 = vnfListOnThisSFC[1]
            vnfid3 = vnfListOnThisSFC[2]
            print("vnfid1 = %d " % vnfid1)
            print("vnfid2 = %d " % vnfid2)
            print("vnfid3 = %d " % vnfid3)
            # 可以选择迁移vnfid1或者vnfid1和vnfid2或者vnfid1和vnfid2和vnfid3

            # 选择迁移vnfid1
            # 首先获取到vnfid1的所有的目的地节点,共有len(desNodeList)种方案
            desNodeList = self.findDestinationForVNF(vnfid1, migratedsfcId)
            print("vnfid1的所有的目的地节点:")
            print(desNodeList)
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
            des_list1 = self.findDestinationForVNF(vnfid1, migratedsfcId)
            des_list2 = self.findDestinationForVNF(vnfid2, migratedsfcId)
            vnf_list = [vnfid1, vnfid2]
            # 找出所有的组合迁移方案(des_list1与des_list2中各选择一个，要不相同)
            for i in range(len(des_list1)):
                for j in range(len(des_list2)):
                    if(des_list1[i] != des_list2[j]):
                        des_list = [des_list1[i], des_list2[j]]
                        MigrationPlanEvaluationInstance = MigrationPlanEvaluation(migratedsfcId, delayBefore,
                                                                                  requestedResourceBefore,
                                                                                  vnf_list, des_list)
                        planEvalu = MigrationPlanEvaluationInstance.evaluation()
                        if(planEvalu > maxPlanEvaluation):
                            maxPlanEvaluation = planEvalu
                            bestPlan = vnf_list
                            bestDes = des_list
            """迁移三个VNF的代码实现没有写"""
            # 返回最高评分、最佳方案（VNF列表和目的物理节点列表,两个列表的大小应该是相同的）
            return (maxPlanEvaluation, bestPlan, bestDes)

    def takeSecond(self, elem):
        return elem[1]

    # 迁移多条SFC（迭代操作），调用一次操作的方法
    def migrateVNFsofMultiSFCIterator(self):
        print("---------------------这是迁移多条SFC的方法本体---------------------")
        sfcListSingleton = SFCList()
        sfclist = sfcListSingleton.getSFCList()
        # 1.存放SFC(可靠性低于需求值的SFC)及其可靠性
        sortedSFClist = []
        for i in range(len(sfclist)):
            sfcid = sfclist[i]
            sfcInstance = SFC(sfcid)
            reliability = sfcInstance.get_SFC_relialibility(sfcInstance.getVNFList())
            if (reliability < sfcInstance.getRequestMinReliability()):
                sortedSFClist.append((sfcid, reliability))

        # 对原数组进行排序(现在temp中存储的数据是按照SFC可靠性来排列的，最小的排在最前边)
        sortedSFClist.sort(key=self.takeSecond, reverse=False)
        # 记录每次迁移的情况
        output_plan_list = []
        out_migrate_VNF_list = []
        out_migrate_VNF_SFC_list = []
        # 如果网络中仍然有SFC可靠性低于要求值，则继续进行迭代过程
        while(len(sortedSFClist) > 0):
            (plan, VNFs, SFCs) = self.migrateVNFsofMultiSFC(sortedSFClist)
            output_plan_list.append(plan)
            out_migrate_VNF_list.append(VNFs)
            out_migrate_VNF_SFC_list.append(SFCs)

            sortedSFClist = []
            for i in range(len(sfclist)):
                sfcid = sfclist[i]
                sfcInstance = SFC(sfcid)
                reliability = sfcInstance.get_SFC_relialibility(sfcInstance.getVNFList())
                if (reliability < sfcInstance.getRequestMinReliability()):
                    sortedSFClist.append((sfcid, reliability))

            # 对原数组进行排序(现在temp中存储的数据是按照SFC可靠性来排列的，最小的排在最前边)
            sortedSFClist.sort(key=self.takeSecond, reverse=False)

    # 迁移多条SFC（一次操作）
    def migrateVNFsofMultiSFC(self, sortedSFClist):
        # 2.一次为每条SFC判断是否有节点过载
        # 存储所有的过载的节点
        overloadNodeidList = []
        # 在开始之前，需要用到一个list，用于存储所有的节点是否被判断过载过（放置重复加入）
        nodeInstance = nodeListSingelton
        allNodeIdlist = nodeInstance.getNodeList()
        # 存放的是（物理节点id,是否被判断过了），起初的状态都是没有被判断过的，当判断之后需要改成True
        ifjudgeList = []
        for nodeid in allNodeIdlist:
            ifjudgeList.append((nodeid, False))
        # 接下来，正式开始为每个SFC判断是否有节点过载（此节点既要位于sortedSFClist中，又要过载）
        # 3.所有过载节点的集合
        overloadedNodeIdList = []
        migVNFWithMinReliaList = []
        migVNFWithMaxFlowList = []
        migVNFWithMinReliaOnSFCIdList = [] #存储migVNFWithMinReliaList中VNF所在的对应的SFC
        migVNFWithMaxFlowOnSFCIdList = []
        for sfcid in sortedSFClist:
            sfc = SFC(sfcid)
            vnfListOnThisSFC = sfc.getVNFList()
            for vnfid in vnfListOnThisSFC:
                vnf = VNF(vnfid)
                vmid = vnf.get_VM_id()
                vm = VM(vmid)
                nodeid = vm.get_physicalNode_id(vmid)
                node = PhysicalNode(nodeid)
                if(node.overloadeState):
                    overloadedNodeIdList.append(nodeid)
        if(overloadedNodeIdList != None):
            # 4.在每个过载节点上选择一个位于可靠性最低的SFC上的VNF，加入到migVNFWithMinReliaList中
            for overload_node_id in overloadedNodeIdList:
                # 为每个过载的节点，优先选择一个位于一个可靠性最低的SFC上的VNF
                # 4.1 获取到每个物理节点上的VM列表
                overload_node = PhysicalNode(overload_node_id)
                vm_list = overload_node.getVMList()
                # 4.2 获取到此节点上的VNF列表
                vnf_list = []
                for vmid in vm_list:
                    vm_instance = VM(vmid)
                    vnfid = vm_instance.getVNFId()
                    vnf_list.append(vnfid)
                # 4.3 从4.2中得到的vnf_list中选择出位于最不可靠SFC上的一个
                min_SFC_reliability = 1000  # 首先设置一个超大的可靠性值(所有的SFC都无法达到这个值)
                min_vnf_id = -1  # 记录此物理节点上找出来的位于最低可靠SFC上的VNF的id
                min_vnf_on_sfcid = -1 # 随时记录可靠性最小的VNF出现在哪条SFC上
                for vnfid in vnf_list:
                    vnf_instance = VNF(vnfid)
                    sfc_id_list = vnf_instance.SFC_id_list # 每个VNF可能位于多条SFC上
                    min_reli_SFC_id = -1  # 记录一个VNF位于耳朵众多的SFC中的可靠性最低的那一条
                    min_SFC_reli = 1000
                    for sfcid in sfc_id_list:
                        sfc_instance = SFC(sfcid)
                        relia = sfc_instance.get_SFC_relialibility(sfc_instance.getVNFList())
                        if(relia < min_SFC_reli):
                            min_SFC_reli = relia
                            min_reli_SFC_id = sfcid
                    if(min_SFC_reli < min_SFC_reliability):
                        min_SFC_reliability = min_SFC_reli
                        min_vnf_id = vnfid
                        min_vnf_on_sfcid = min_reli_SFC_id
                # 将此物理节点上位于最不可靠的SFC上的VNF加入migVNFWithMinReliaList
                migVNFWithMinReliaList.append(min_vnf_id)
                # 同时，将其对应的SFC id加入到migVNFWithMinReliaOnSFCIdList中
                migVNFWithMinReliaOnSFCIdList.append(min_vnf_on_sfcid)
            """至此，每个节点上的位于最不可靠SFC上的VNF就被加入到migVNFWithMinReliaList中了"""

            # 5.在每个物理节点上选择一个流经流量最大的VNF，加入到migVNFWithMaxFlowList中
            # 网络中所有的VNF
            vnfListSingelton = VNFList()
            allVnfList = vnfListSingelton.getActiveVNFList()
            for j in range(len(overloadedNodeIdList)):
                maxFlow = 0
                maxFlowVNF = None
                for i in range(len(allVnfList)):
                    vnf = VNF(allVnfList[i])
                    vmid = vnf.get_VM_id(allVnfList[i])
                    nodeid = VM.get_physicalNode_id(vmid)
                    if(nodeid == overloadedNodeIdList[j]):
                        # 都是位于相同物理机上的,从中挑选流量最大的一个VNF
                        if((vnf.getVNF_request_CPU() + vnf.getVNF_request_Memory()) > maxFlow):
                            maxFlow = vnf.getVNF_request_CPU() + vnf.getVNF_request_Memory()
                            maxFlowVNF = allVnfList[i]
                # 至此，maxFlowVNF中存放的就是此物理节点上流量需求最大的VNF，将其添加到migVNFWithMaxFlowList中
                if(maxFlowVNF not in migVNFWithMinReliaList):
                    migVNFWithMaxFlowList.append(maxFlowVNF)
                    vnf_instance = VNF(maxFlowVNF)
                    sfc_list = vnf_instance.SFC_id_list
                    min_relia = 1000
                    min_sfc_id = -1
                    for sfc_id in sfc_list:
                        sfc_instance = SFC(sfc_id)
                        if(sfc_instance.get_SFC_relialibility(sfc_instance.getVNFList()) < min_relia):
                            min_relia = sfc_instance.get_SFC_relialibility(sfc_instance.getVNFList())
                            min_sfc_id = sfc_id
                    # 将此物理节点上流经流量最大的VNF所在的SFC（选取可靠性最低的一条）存储
                    migVNFWithMaxFlowOnSFCIdList.append(min_sfc_id)
            # 至此，所有过载节点上的流量最大的VNF都已经被添加到migVNFWithMaxFlowList中了

        # 6.当网络中没有节点过载时，选择sortedSFClist中可靠性最低的SFC，
        # 加入到migVNFWithMaxFlowList和migVNFWithMinReliaList中
        elif(overloadedNodeIdList == None):
            # 没有节点过载
            for sfcid in sortedSFClist:
                sfcInstance = SFC(sfcid)
                vnfList = sfcInstance.getVNFList()
                maxReliability = 0
                maxVNFId = -1
                for vnfid in vnfList:
                    vnfInstance = VNF(vnfid)
                    vnfReliability = vnfInstance.getVNFRliability(vnfid)
                    if(vnfReliability > maxReliability):
                        maxVNFId = vnfid
                migVNFWithMinReliaList.append(maxVNFId)
                migVNFWithMinReliaOnSFCIdList.append(sfcid)
                migVNFWithMaxFlowList.append(maxVNFId)
                migVNFWithMaxFlowOnSFCIdList.append(sfcid)

        # 7. 分别为migVNFWithMinReliaList和migVNFWithMaxFlowList中的所有VNF计算可迁移的目的地（其中的每一个VNF都要迁移）
        # 7.1 为migVNFWithMinReliaList中的所有VNF选择迁移目的地
        # 存储migVNFWithMinReliaList中所有vnf的目的地（列表中存储的还是列表）
        VNFWithMinReliaDesList = []
        for i in range(len(migVNFWithMinReliaList)):
            vnfid = migVNFWithMinReliaList[i]
            sfcid = migVNFWithMinReliaOnSFCIdList[i]
            vnfInstance = VNF(vnfid)
            # vnfid所有可能的迁移目的地
            satidfiedNodeList = self.findDestinationForVNF(vnfid, sfcid)
            VNFWithMinReliaDesList.append(satidfiedNodeList)
        # 7.2 为migVNFWithMaxFlowList中的所有VNF寻找所有可能的迁移目的地
        # 存储migVNFWithMaxFlowList中所有vnf的目的地（列表中存储的还是列表）
        VNFWithMaxFlowDesList = []
        for i in range(len(migVNFWithMaxFlowList)):
            vnfid = migVNFWithMaxFlowList[i]
            sfcid = migVNFWithMaxFlowOnSFCIdList[i]
            vnfInstance = VNF(vnfid)
            # vnfid所有可能的迁移目的地
            satidfiedNodeList = self.findDestinationForVNF(vnfid, sfcid)
            VNFWithMaxFlowDesList.append(satidfiedNodeList)
        # 7.3 形成迁移计划
        # migVNFWithMinReliaList中的VNF迁移，形成的迁移计划存储在VNFWithMinReliaPlan中
        VNFWithMinReliaPlan = self.getMigrationPlan(migVNFWithMinReliaList,
                                                    migVNFWithMinReliaOnSFCIdList, VNFWithMinReliaDesList)
        # migVNFWithMaxFlowList中的VNF迁移，形成的迁移计划存储在VNFWithMaxFlowPlan
        VNFWithMaxFlowPlan = self.getMigrationPlan(migVNFWithMaxFlowList,
                                                   migVNFWithMaxFlowOnSFCIdList, VNFWithMaxFlowDesList)
        # 8 两组迁移计划进行评分
        # VNFWithMinReliaPlan组
        # 存储此评价方案的评分
        VNFWithMinReliaPlanEvalu = 0
        for i in range(len(VNFWithMinReliaPlan)):
            migratedsfcId = migVNFWithMinReliaOnSFCIdList[i]
            sfcInstance = SFC(migratedsfcId)
            delayBefore = sfcInstance.getDelay()
            requestedResourceBefore = sfcInstance.getRequestMinReliability()
            vnf_list = [migVNFWithMinReliaList[i]]
            des_list = VNFWithMinReliaPlan[i]
            MigrationPlanEvaluationInstance = MigrationPlanEvaluation(migratedsfcId, delayBefore,
                                                                      requestedResourceBefore,
                                                                      vnf_list, des_list)
            VNFWithMinReliaPlanEvalu += MigrationPlanEvaluationInstance.evaluation()

        # VNFWithMaxFlowPlan组
        # 存储此评价方案的评分
        VNFWithMaxFlowPlanEvalu = 0
        for i in range(len(migVNFWithMaxFlowList)):
            migratedsfcId = migVNFWithMaxFlowOnSFCIdList[i]
            sfcInstance = SFC(migratedsfcId)
            delayBefore = sfcInstance.getDelay()
            requestedResourceBefore = sfcInstance.getRequestMinReliability()
            vnf_list = [migVNFWithMaxFlowList[i]]
            des_list = VNFWithMaxFlowPlan[i]
            MigrationPlanEvaluationInstance = MigrationPlanEvaluation(migratedsfcId, delayBefore,
                                                                      requestedResourceBefore,
                                                                      vnf_list, des_list)
            VNFWithMaxFlowPlanEvalu += MigrationPlanEvaluationInstance.evaluation()
        # 两个的迁移计划已经评价完毕，现在比较评分高低，选出一个评分高的方案输出
        # 存储输出方案
        outPutPlan = None
        finalMigVNFs = None
        finalMigVNFsSFC = None
        if(VNFWithMinReliaPlanEvalu > VNFWithMaxFlowPlanEvalu):
            outPutPlan = VNFWithMinReliaPlanEvalu
            finalMigVNFs = migVNFWithMinReliaList
            finalMigVNFsSFC = migVNFWithMinReliaOnSFCIdList
        else:
            outPutPlan = VNFWithMaxFlowPlanEvalu
            finalMigVNFs = migVNFWithMaxFlowList
            finalMigVNFsSFC = migVNFWithMaxFlowOnSFCIdList
        # 8plus 选择出迁移方案之后，需要对迁移方案中涉及的物理机的资源做出调整：迁移之前的物理机资源增加，迁移之后的物理机资源减少
        # 另外，物理机上记录的VNF的id也得需要更新
        for i in range(len(finalMigVNFs)):
            # 此VNF迁移之后的物理机的id
            node_after_id = outPutPlan[i]
            vnf_id = finalMigVNFs[i]
            vnf_instance = VNF(vnf_id)
            # 此VNF占用的cpu
            cpu_occupied = vnf_instance.getVNF_request_CPU()
            # 此VNF占用的内存
            memo_occupied = vnf_instance.getVNF_request_Memory()
            # 求此VNF迁移之前所在的物理机的ID
            vm_id = vnf_instance.get_VM_id(vnf_id)
            vm_instance = VM(vm_id)
            # 将VM所在的物理机设置成迁移之后的物理机
            vm_instance.setPhysicalNodeId(node_after_id)
            node_before_id = vm_instance.get_physicalNode_id(vm_id)
            # 设置迁移之前物理机的资源
            node_before_instance = PhysicalNode(node_before_id)
            node_before_instance.addAvailable_CPU(node_before_id, cpu_occupied)
            node_before_instance.addAvailable_Memory(node_before_id, memo_occupied)
            # 设置迁移之后的物理机的资源
            node_after_instance = PhysicalNode(node_after_id)
            node_after_instance.deleteAvailable_CPU(node_after_id, memo_occupied)
            node_after_instance.deleteAvailable_CPU(node_after_id, cpu_occupied)
        # 返回 迁移到的物理节点列表、最终的迁移VNF列表、所在SFC列表
        return outPutPlan, finalMigVNFs, finalMigVNFsSFC

    # 根据待迁移VNF列表，待迁移VNF所处SFC列表，待迁移VNF的目的地列表进行迁移组合
    # 返回的是每个VNF迁移目的地的list
    def getMigrationPlan(self, vnfList, sfcList, desList):
        # 两个VNF不能迁移到一个物理机，因此定义一个occupiedNodeIdList，用于存储已经被占用的物理机
        occupiedNodeIdList = []
        finalNodeIdList = []
        # 如何选择每个VNF的目的地呢？首选的是VNF从旧物理机到新物理机之间时延最低的一个
        for i in range(len(vnfList)):
            min_delay = 1000
            final_des = -1
            # 此VNF可以迁移的目的地列表
            vnfDesList = desList[i]
            # 当前VNF所在的物理机
            vnf_Instance = VNF(vnfList[i])
            currentVMId = vnf_Instance.get_VM_id(vnfList[i])
            vmInstance = VM(currentVMId)
            currentNodeId = vmInstance.get_physicalNode_id(currentVMId)
            # 计算从当前VNF所在的物理机到每一个物理机的时延
            for j in range(len(vnfDesList)):
                VNFDesNodeId = vnfDesList[j]
                # 获取两个物理机之间的时延
                sfcInstance = SFC(sfcList[i])
                if(VNFDesNodeId not in occupiedNodeIdList):
                    delay = sfcInstance.getDelayBetweenPhysicalNode(currentNodeId, VNFDesNodeId)
                    if(delay < min_delay):
                        final_des = VNFDesNodeId
                        min_delay = delay
                else:
                    # 若是找不到迁移的目的地，则此VNF的迁移目的地为自己本身，也就是不迁移了
                    final_des = currentNodeId
            # 挑选出一个时延最短的VNF i的目的地，即final_des
            # 将其加入到finalNodeIdList中，即为最终的迁移方案
            finalNodeIdList.append(final_des)
        # 至此，所有的待迁移VNF都已经选定了一个目的地（极特殊情况没有考虑：当有的VNF只能迁移到一个目的地，而此目的地又被占用了，
        # 此时将迁移队列中的此VNF去掉，即为最简便的处理方案），因此，添加上边的else语句，设置没有迁移目的地的VNF的迁移目的地为自己
        # 返回
        return finalNodeIdList

    """通过测试的方法"""
    # 寻找当前网络中可靠性最低的SFC,返回此SFC的ID
    def findSFCWithMinReliability(self):
        print("寻找当前网络中可靠性最低的SFC")
        minReliability  = 100
        SFCIDwithMINRelibility = -1
        # 获取到网络中所有的SFC的ID的列表
        SFCList = sfcListSingleton.AllSFCList
        print(SFCList)
        for sfcId in SFCList:
            print("/////////////////when sfcid = %d" %sfcId)
            sfcInstance = SFC(sfcId,
                              sfcListSingleton.dict_maxDelay[sfcId],
                              sfcListSingleton.dict_minReliability[sfcId],
                              sfcListSingleton.dict_VNFList[sfcId],
                              sfcListSingleton.dict_createdtime[sfcId]
                              )
            print(sfcInstance.getVNFList())
            sfcReliability = sfcInstance.get_SFC_relialibility(sfcInstance.getVNFList())
            if (sfcReliability < minReliability):
                minReliability = sfcReliability
                SFCIDwithMINRelibility = sfcId
        print("SFCIDwithMINRelibility = %d " % SFCIDwithMINRelibility)
        print("寻找可靠性最低的SFC的方法结束///////////////////////")
        return SFCIDwithMINRelibility

    """测试通过"""
    # 判断一条SFC上VNF们所在的物理节点们谁过载了，返回过载物理节点的list
    def judgingIfNodeOverload(self, sfcId):
        print("判断一条SFC上VNF们所在的物理节点们谁过载了，返回过载物理节点的list")
        # 存放此SFC所经过的所有的过载的物理节点
        overloadNodeListId = []
        # 存放此SFC上所有位于过载物理节点上的VNF
        VNFonoverNodeListId = []
        print("要判断的sfcid = ///////////////%d " % sfcId)
        sfcInstance = SFC(sfcId,
                          sfcListSingleton.dict_maxDelay[sfcId],
                          sfcListSingleton.dict_minReliability[sfcId],
                          sfcListSingleton.dict_VNFList[sfcId],
                          sfcListSingleton.dict_createdtime[sfcId]
                          )
        vnfList = sfcInstance.getVNFList()
        print(vnfList)
        for vnfId in vnfList:
            vnfInstance = VNF(vnfId,
                              vnfListSingelton.dict_VNFListType[vnfId],
                              vnfListSingelton.dict_VNFRequestCPU[vnfId],
                              vnfListSingelton.dict_VNFRequestMemory[vnfId],
                              vnfListSingelton.dict_locatedVMID[vnfId],
                              vnfListSingelton.dict_locatedSFCIDList[vnfId],
                              vnfListSingelton.dict_numbersOnSFCList[vnfId],
                              vnfListSingelton.dict_VNFReliability[vnfId]
                              )
            vmInstance = VM(vnfInstance.get_VM_id(vnfId),
                            vmListSingelton.dict_VMRequestCPU[vnfInstance.get_VM_id(vnfId)],
                            vmListSingelton.dict_VMRequestMemory[vnfInstance.get_VM_id(vnfId)],
                            vmListSingelton.dict_VMLocatedPhysicalnode[vnfInstance.get_VM_id(vnfId)],
                            vmListSingelton.dict_VMReliability[vnfInstance.get_VM_id(vnfId)]
                            )
            # 获取到此VNF所在的物理节点
            nodeId = vmInstance.get_physicalNode_id(vnfInstance.get_VM_id(vnfId))
            # 判断此节点是否过载
            nodeInstance = PhysicalNode(nodeId,
                                        nodeListSingelton.dict_capacity_CPU[nodeId],
                                        nodeListSingelton.dict_capacity_Memory[nodeId],
                                        nodeListSingelton.dict_provided_reliablity[nodeId]
                                        )
            overloadeState = nodeInstance.overloadeState
            if (overloadeState == True):
                VNFonoverNodeListId.append(vnfId)
                overloadNodeListId.append(nodeId)
        print("这是判断节点过载类，overloadNodeListId is : ")
        print(overloadNodeListId)
        print("此SFC上所有位于过载物理节点上的VNF:")
        print(VNFonoverNodeListId)
        return (overloadNodeListId, VNFonoverNodeListId)

    """测试通过"""
    # 为VNF计算迁移目的地列表
    def findDestinationForVNF(self, vnfId, migratedSFCId):
        print("这是为VNF计算迁移目的地的方法本体：")
        # 存储所有可能的物理节点的id
        allsatidfiedNodeList = []
        # 满足约束条件的都可作为VNF迁移的目的地
        nodeIdList = nodeListSingelton.getNodeList()
        print("nodeIdList = ")
        print(nodeIdList)
        for nodeId in nodeIdList:
            print("nodeid = %d" %nodeId)
            judge_res = self.judgeIfIsDestination(vnfId, nodeId, migratedSFCId)
            print(judge_res)
            if(judge_res == True):
                print("node 将被加入此VNF的迁移目的地中 %d" % nodeId)
                allsatidfiedNodeList.append(nodeId)
        print("////////////////////////////这是为VNF计算迁移目的地的方法本体：allsatidfiedNodeList = ")
        print(allsatidfiedNodeList)
        return allsatidfiedNodeList

    """测试通过"""
    # 判断某个物理节点是否是某个VNF迁移的目的地
    # 输入参数为vnf id（需要迁移的VNF的id） 与node id(待选的物理节点的id)，返回布尔值
    def judgeIfIsDestination(self, vnfId, nodeId, migratedSFCId):
        print("判断某个物理节点是否是某个VNF迁移的目的地方法本体")
        """根据约束条件判断"""
        # 第一个约束条件判断的结果存储在constrain1中
        constrain1 = self.judgeConstrain1(vnfId, nodeId, migratedSFCId)
        if(constrain1 == True):
            print("约束1满足")
            # 进行第二个约束条件的判断，将其存放在constrain2中
            constrain2 = self.judgeConstrain2(vnfId, nodeId, migratedSFCId)
            if(constrain2 == True):
                print("约束2满足")
                # 进行第三个约束条件的判断
                constrain3 = self.judgeConstrain3(vnfId, nodeId, migratedSFCId)
                if(constrain3 == True):
                    print("约束3满足")
                    # 进行第四个约束条件的判断
                    constrain4 = self.judgeConstrain4(vnfId, nodeId, migratedSFCId)
                    if(constrain4 == True):
                        print("约束4满足")
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    """测试通过"""
    # 判断第一个约束条件是否满足，满足返回True，否则返回False
    def judgeConstrain1(self, vnfId, nodeId, migratedSFCId):
        print("判断约束条件1是是否满足方法本体")
        # 约束1.1 迁移后的节点可靠性大于迁移前VNF所在节点的可靠性
        VNFInstance = VNF(vnfId,
                          vnfListSingelton.dict_VNFListType[vnfId],
                          vnfListSingelton.dict_VNFRequestCPU[vnfId],
                          vnfListSingelton.dict_VNFRequestMemory[vnfId],
                          vnfListSingelton.dict_locatedVMID[vnfId],
                          vnfListSingelton.dict_locatedSFCIDList[vnfId],
                          vnfListSingelton.dict_numbersOnSFCList[vnfId],
                          vnfListSingelton.dict_VNFReliability[vnfId]
                          )
        print("vnfid = %d" %vnfId)
        print("vnfListSingelton.dict_VNFReliability[5] = %f" %vnfListSingelton.dict_VNFReliability[vnfId])
        # print(vnfListSingelton.dict_VNFReliability[5])
        # 迁移之前/当前的可靠性（VNF的可靠性也就是物理节点的可靠性）
        currentReliability = VNFInstance.getVNFRliability(vnfId)
        print("迁移之前此VNF的可靠性 %f" % currentReliability)
        # 若是迁移到nodeId,那么迁移之后的可靠性
        nodeInstance = PhysicalNode(nodeId,
                                    nodeListSingelton.dict_capacity_CPU[nodeId],
                                    nodeListSingelton.dict_capacity_Memory[nodeId],
                                    nodeListSingelton.dict_provided_reliablity[nodeId]
                                    )
        afterReliability = nodeInstance.get_reliability(nodeId)
        print("迁移之后的可靠性：%f" %afterReliability)
        # 判断是否可靠性增大，即满足第一个约束条件
        if (afterReliability > currentReliability):
            print("满足约束1.1， 开始判断约束1.2")
            # 满足约束条件1.1
            # 判断迁移条件1.2 迁移后整条SFC的可靠性是否大于需求值
            SFCInstance = SFC(migratedSFCId,
                              sfcListSingleton.dict_maxDelay[migratedSFCId],
                              sfcListSingleton.dict_minReliability[migratedSFCId],
                              sfcListSingleton.dict_VNFList[migratedSFCId],
                              sfcListSingleton.dict_createdtime[migratedSFCId]
                              )
            vnfList = SFCInstance.getVNFList()
            requestSFCReliability = SFCInstance.getRequestMinReliability()
            vnfListCopy = vnfList
            # 找到vnfListCopy中id为vnfId的vnf,将它的物理节点换掉，换成迁移之后的node
            for vnf_id in vnfListCopy:
                if(vnf_id == vnfId):
                    VNFInstance = VNF(vnf_id,
                                      vnfListSingelton.dict_VNFListType[vnf_id],
                                      vnfListSingelton.dict_VNFRequestCPU[vnf_id],
                                      vnfListSingelton.dict_VNFRequestMemory[vnf_id],
                                      vnfListSingelton.dict_locatedVMID[vnf_id],
                                      vnfListSingelton.dict_locatedSFCIDList[vnf_id],
                                      vnfListSingelton.dict_numbersOnSFCList[vnf_id],
                                      vnfListSingelton.dict_VNFReliability[vnf_id]
                                      )
                    VMId = VNFInstance.get_VM_id(vnf_id)
                    VMInstance = VM(VMId,
                                    vmListSingelton.dict_VMRequestCPU[VMId],
                                    vmListSingelton.dict_VMRequestMemory[VMId],
                                    vmListSingelton.dict_VMLocatedPhysicalnode[VMId],
                                    vmListSingelton.dict_VMReliability[VMId]
                                    )
                    # 此时vnfListCopy中的VNF已经更新完了
                    VMInstance.setPhysicalNodeId(nodeId)
            print(vnfListCopy)
            # 使用更新完的vnfListCopy，放入到新的迁移完的SFC中，计算迁移之后的SFC的可靠性
            currentSFCReliability = SFCInstance.get_SFC_relialibility1(vnfListCopy, vnfId, nodeId)
            if(currentSFCReliability > requestSFCReliability):
                print("约束1满足")
                return True
        else:
            # 不满足约束1
            print("约束1不满足")
            return False

    """测试通过"""
    # 判断第二个约束条件是否满足，满足返回True，否则返回False
    def judgeConstrain2(self, vnfId, nodeId, migratedSFCId):
        # 约束2 迁移之后SFC的时延增加不可超过一个σ（参数设置，以毫秒记）
        delayIncreace = 20 # 设时延的最大增量为20ms
        SFCInstance = SFC(migratedSFCId,
                          sfcListSingleton.dict_maxDelay[migratedSFCId],
                          sfcListSingleton.dict_minReliability[migratedSFCId],
                          sfcListSingleton.dict_VNFList[migratedSFCId],
                          sfcListSingleton.dict_createdtime[migratedSFCId]
                          )
        vnfList = SFCInstance.getVNFList()
        # 迁移之前SFC的时延
        currentDelay = SFCInstance.get_SFC_delay(vnfList)
        # 创建一个VNF副本，用于更新vnf
        vnfListCopy = vnfList
        for vnf_id in vnfListCopy:
            if(vnf_id == vnfId):
                VNFInstance = VNF(vnf_id,
                                  vnfListSingelton.dict_VNFListType[vnf_id],
                                  vnfListSingelton.dict_VNFRequestCPU[vnf_id],
                                  vnfListSingelton.dict_VNFRequestMemory[vnf_id],
                                  vnfListSingelton.dict_locatedVMID[vnf_id],
                                  vnfListSingelton.dict_locatedSFCIDList[vnf_id],
                                  vnfListSingelton.dict_numbersOnSFCList[vnf_id],
                                  vnfListSingelton.dict_VNFReliability[vnf_id]
                                  )
                VMId = VNFInstance.get_VM_id(vnf_id)
                VMInstance = VM(VMId,
                                vmListSingelton.dict_VMRequestCPU[VMId],
                                vmListSingelton.dict_VMRequestMemory[VMId],
                                vmListSingelton.dict_VMLocatedPhysicalnode[VMId],
                                vmListSingelton.dict_VMReliability[VMId]
                                )
                # 此时vnfListCopy中的VNF已经更新完了
                VMInstance.setPhysicalNodeId(nodeId)
        # 使用更新完的VNFList来计算新的SFC的时延
        afterDelay = SFCInstance.get_SFC_delay(vnfListCopy)
        if(afterDelay - currentDelay <= delayIncreace):
            print("约束2满足")
            return True
        else:
            print("约束2不满足")
            return False

    """测试通过"""
    # 判断第三个约束条件是否满足，满足返回True，否则返回False
    def judgeConstrain3(self, vnfId, nodeId, migratedSFCId):
        # 约束3 资源约束，即待迁移VNF迁移到新的物理节点上时，所需要的资源小于当前物理节点可提供的资源
        VNFInstance = VNF(vnfId,
                          vnfListSingelton.dict_VNFListType[vnfId],
                          vnfListSingelton.dict_VNFRequestCPU[vnfId],
                          vnfListSingelton.dict_VNFRequestMemory[vnfId],
                          vnfListSingelton.dict_locatedVMID[vnfId],
                          vnfListSingelton.dict_locatedSFCIDList[vnfId],
                          vnfListSingelton.dict_numbersOnSFCList[vnfId],
                          vnfListSingelton.dict_VNFReliability[vnfId]
                          )
        # VNF需要的CPU和内存资源数量
        requestCPU = VNFInstance.getVNF_request_CPU()
        requestMemory = VNFInstance.getVNF_request_Memory()
        # 新的物理节点可以提供的资源
        nodeInstance = PhysicalNode(nodeId,
                                    nodeListSingelton.dict_capacity_CPU[nodeId],
                                    nodeListSingelton.dict_capacity_Memory[nodeId],
                                    nodeListSingelton.dict_provided_reliablity[nodeId]
                                    )
        availableCPU = nodeInstance.getAvailable_CPU(nodeId)
        availableMemory = nodeInstance.getAvailable_Memory(nodeId)
        # 注意啦！！！不能在这里减去物理节点的CPU和内存资源，因为此时并没有真的迁移到这个物理节点上来。
        # 判断资源是否满足要求
        if(requestCPU < availableCPU and requestMemory < availableMemory):
            print("约束3满足")
            return True
        else:
            print("约束3不满足")
            return False

    """测试通过"""
    # 判断第四个约束条件是否满足，满足返回True，否则返回False
    def judgeConstrain4(self, vnfId, nodeId, migratedSFCId):
        # 约束4 网络中所有节点的负载偏差程度小于η，即负载均衡条件
        # 1.首先要对待迁移VNF所涉及的物理节点进行一个更新，两部分：
        # 当前位于的物理节点资源加上VNF占用的部分，目的地物理节点资源减去VNF占用的部分
        VNFInstance = VNF(vnfId,
                          vnfListSingelton.dict_VNFListType[vnfId],
                          vnfListSingelton.dict_VNFRequestCPU[vnfId],
                          vnfListSingelton.dict_VNFRequestMemory[vnfId],
                          vnfListSingelton.dict_locatedVMID[vnfId],
                          vnfListSingelton.dict_locatedSFCIDList[vnfId],
                          vnfListSingelton.dict_numbersOnSFCList[vnfId],
                          vnfListSingelton.dict_VNFReliability[vnfId]
                          )
        vmId = VNFInstance.get_VM_id(vnfId)
        VMInstance = VM(vmId,
                        vmListSingelton.dict_VMRequestCPU[vmId],
                        vmListSingelton.dict_VMRequestMemory[vmId],
                        vmListSingelton.dict_VMLocatedPhysicalnode[vmId],
                        vmListSingelton.dict_VMReliability[vmId]
                        )
        nodeBeforeId = VMInstance.get_physicalNode_id(vmId)
        nodeBefore = PhysicalNode(nodeBeforeId,
                                  nodeListSingelton.dict_capacity_CPU[nodeBeforeId],
                                  nodeListSingelton.dict_capacity_Memory[nodeBeforeId],
                                  nodeListSingelton.dict_provided_reliablity[nodeBeforeId]
                                  )
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
        nodeAfter = PhysicalNode(nodeId,
                                 nodeListSingelton.dict_capacity_CPU[nodeId],
                                 nodeListSingelton.dict_capacity_Memory[nodeId],
                                 nodeListSingelton.dict_provided_reliablity[nodeId]
                                 )
        nodeAfterCopy = nodeAfter
        nodeAfterCopy.deleteAvailable_CPU(nodeId, cpuResource)
        nodeAfterCopy.deleteAvailable_Memory(nodeId, memoryResource)
        (cpu_rate_after, memory_rate_after) = nodeAfterCopy.occupancy_rate_resource()
        resource_rate_after = (cpu_rate_after + memory_rate_after)/2

        # 2.获取到网络中迁移状态之后的所有节点及它们的负载程度（用资源利用率来衡量）
        allNodeList = nodeListSingelton.getNodeList()
        # 存储网络中所有的物理节点的负载
        loadList = []
        for i in range(len(allNodeList)):
            loadList.append(0)
        for i in range(len(allNodeList)):
            nodeid = allNodeList[i]
            if(nodeid == nodeId):
                loadList[i] = resource_rate_after
            elif(nodeid == nodeBeforeId):
                loadList[i] = resource_rate_before
            else:
                node = PhysicalNode(nodeid,
                                    nodeListSingelton.dict_capacity_CPU[nodeid],
                                    nodeListSingelton.dict_capacity_Memory[nodeid],
                                    nodeListSingelton.dict_provided_reliablity[nodeid]
                                    )
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
            print("满足迁移条件，返回true")
            return True
        else:
            print("不满足迁移条件，返回false")
            return False

        """未完待续"""
