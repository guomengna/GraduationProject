"""SFC初始形成"""
#SFC初始形成方法
# VNF_list里边包含VNF id、需求的资源、类型
import datetime

from entity.PhysicalNode import PhysicalNode
from entity.PhysicalNodeList import nodeListSingelton
from entity.SFC import SFC, leftPhysicalNodelist, rightPhysicalNodelist, delaylist
from entity.SFCList import sfcListSingleton
from entity.VM import VM
from entity.VMList import vmListSingelton
from entity.VNF import VNF
from entity.VNFList import vnfListSingelton

class SFCInitialFormed():
    print("SFC初始创建模块")

    SFCCount = 0
    delay_list = []
    # 同类型中已经被选过的VNF列表
    VNFHadPicked = []
    VNFHadPicked1 = []
    K = 6
    # 存放找出来的前K个SFC
    foundSFCList = []
    def SFC_initial_formed(self, request_delay, request_reliability, VNFTyprList, VNFRequestCPU, VNFRequestMemory):
        print("主方法")
        # step1，寻找前K个满足约束条件的SFC
        while len(self.foundSFCList) < self.K:
            self.foundSFCList.append(self.find_a_SFC1(request_delay,
                                                     request_reliability, VNFTyprList, VNFRequestCPU, VNFRequestMemory))
        print("foundSFCList = ")
        print(self.foundSFCList)
        # step2, 判断每条SFC加入后是否会引起节点过载，并预测过载程度
        # 存放每条SFC的评分
        scoreList = []
        maxScore = 100000  # 最高评分
        maxScoreSFCId = 0  # 拥有最高评分的SFC的id
        # 挨个分析每一条SFC
        i = 0
        vmflistforMaxscore = []
        while(i < self.K):
            analysisSFC = self.foundSFCList[i]
            if(analysisSFC != None):
                print("dededdcfedededeeeeeeeeeeeeeeeeeeeee")
                vnflist = analysisSFC.getVNFList()
                print(vnflist)
                # 但是由于挑选VNF的时候已经确定了VNF能够提供足够多的资源，所以挑选出来的SFC都不会过载？
                # 可以选择将VNF的资源需求值上升一个随机（比如说增加从0到0.1之间的任意数倍）的倍数，防止运行中需求的资源会上升。
                # 再去预测是否会过载（但这个还是留待提升阶段再用吧）
                # 现阶段的节点过载程度都为0，节点的可靠性没有变化，即每条SFC加入后对网络中已有SFC的影响值为0

                # step3,为每条SFC评分，选择出评分最高的SFC作为初始形成的SFC
                # 评分标准简化为时延的相反数，此值越小越好
                scoreList.append(self.SFC_placement_plan_scoring(analysisSFC.getSFCId(), vnflist))
                print(self.SFC_placement_plan_scoring(analysisSFC.getSFCId(), vnflist))
                print(maxScore)
                if maxScore < self.SFC_placement_plan_scoring(analysisSFC.getSFCId(), vnflist):
                    print("if 成立")
                    maxScore = self.SFC_placement_plan_scoring(analysisSFC.getSFCId(), vnflist)
                    maxScoreSFCId = analysisSFC.getSFCId()
                    vmflistforMaxscore = vnflist
                    print("maxScoreSFCId = %d" %maxScoreSFCId)
                i += 1
            else:
                break
        # 将拥有最高可靠性的SFC加入到SFCList单例中
        sfcListSingleton.addSFC(maxScoreSFCId)
        # 返回拥有最高得分的SFC，作为最初的SFC部署方案
        print("maxScoreSFCId = ------------------------")
        print(maxScoreSFCId)

        # for vnfid in vmflistforMaxscore:
        #     self.VNFHadPicked.append(vnfid)

        print("maxScoreSFCId = %d" % maxScoreSFCId)

        return maxScoreSFCId
    def delayBetweenVNFs(self, VNFIdLeft, VNFRight):

        delay = 1000000
        VNFInstanceLeft = VNF(VNFIdLeft,
                              vnfListSingelton.dict_VNFListType[VNFIdLeft],
                              vnfListSingelton.dict_VNFRequestCPU[VNFIdLeft],
                              vnfListSingelton.dict_VNFRequestMemory[VNFIdLeft],
                              vnfListSingelton.dict_locatedVMID[VNFIdLeft],
                              vnfListSingelton.dict_locatedSFCIDList[VNFIdLeft],
                              vnfListSingelton.dict_numbersOnSFCList[VNFIdLeft],
                              vnfListSingelton.dict_VNFReliability[VNFIdLeft]
                              )
        VNFInstanceRight = VNF(VNFRight,
                               vnfListSingelton.dict_VNFListType[VNFRight],
                               vnfListSingelton.dict_VNFRequestCPU[VNFRight],
                               vnfListSingelton.dict_VNFRequestMemory[VNFRight],
                               vnfListSingelton.dict_locatedVMID[VNFRight],
                               vnfListSingelton.dict_locatedSFCIDList[VNFRight],
                               vnfListSingelton.dict_numbersOnSFCList[VNFRight],
                               vnfListSingelton.dict_VNFReliability[VNFRight]
                               )
        vmIdleft = VNFInstanceLeft.get_VM_id(VNFIdLeft)
        vmIdRight = VNFInstanceRight.get_VM_id(VNFRight)
        vmInstanceleft = VM(vmIdleft, vmListSingelton.dict_VMRequestCPU[vmIdleft],
                            vmListSingelton.dict_VMRequestMemory[vmIdleft],
                            vmListSingelton.dict_VMLocatedPhysicalnode[vmIdleft],
                            vmListSingelton.dict_VMReliability[vmIdleft])
        vmInstanceright = VM(vmIdRight, vmListSingelton.dict_VMRequestCPU[vmIdRight],
                            vmListSingelton.dict_VMRequestMemory[vmIdRight],
                            vmListSingelton.dict_VMLocatedPhysicalnode[vmIdRight],
                            vmListSingelton.dict_VMReliability[vmIdRight])
        LeftphysicalNodeId = vmInstanceleft.get_physicalNode_id(vmIdleft)
        RightphysicalNodeId = vmInstanceright.get_physicalNode_id(vmIdRight)
        # 由拓扑结构获取到左右两个物理节点之间的时延
        for i in range(len(leftPhysicalNodelist)):
            if LeftphysicalNodeId == leftPhysicalNodelist[i]:
                if RightphysicalNodeId == rightPhysicalNodelist[i]:
                    delay = delaylist[i]
            elif LeftphysicalNodeId == rightPhysicalNodelist[i]:
                if RightphysicalNodeId == leftPhysicalNodelist[i]:
                    delay = delaylist[i]
        return delay
    def get_SFC_delay(self, VNF_list):
        SFCDelay = 0
        index = 0
        for index in range(len(VNF_list) - 1):
            VNFIdLeft = VNF_list[index]
            VNFIdRight = VNF_list[index+1]
            delay = self.delayBetweenVNFs(VNFIdLeft, VNFIdRight)
            self.delay_list.append(delay)
        for i in range(len(self.delay_list)):
            SFCDelay += self.delay_list[i]
        return SFCDelay
    # SFC部署方案的评分方法
    def SFC_placement_plan_scoring(self, SFC_id, vnflist):
        print("评分方法开始")
        # SFC的得分
        score = 0
        score = -self.get_SFC_delay(vnflist)
        # for i in range(len(self.foundSFCList)):
        #     if SFC_id == self.foundSFCList[i].getSFCId():
        #         score = -self.foundSFCList[i].get_SFC_delay(vnflist)
        #         print(score)
        #     break
        print("评分方法结束, score = %f" % score)
        return score

    # 寻找一条满足约束条件的SFC
    # 输入的参数：SFC所需要的最大时延、最低可靠性、VNF类型列表、VNF所需CPU资源的列表、VNF所需内存资源的列表
    def find_a_SFC(self, MaxSFCDelay, MinSFCReliablity, VNFTyprList, VNFRequestCPU, VNFRequestMemory):
        print("发现一条SFC方法")
        # 存储根据VNF类型和所需CPU、内存资源条件筛选出来的VNFs
        VNFList = []
        for i in range(len(VNFTyprList)):
            aVNFInstance = VNF()
            vmInstance = VM()
            physicalInstace = PhysicalNode()
            vmId = aVNFInstance.get_VM_id(self.getAVNFByType())
            physicalNodeId = vmInstance.get_physicalNode_id(vmId)
            if(physicalInstace.getAvailable_CPU(physicalNodeId) > VNFRequestCPU and
            physicalInstace.getAvailable_Memory(physicalNodeId) > VNFRequestMemory):
                # 将此VNF的id加入到list中，作为此SFC中的一环
                VNFList.append(self.getAVNFByType())
        # 所有需要的VNF都找到了，一条SFC就挑选出来了
        sfcid = sfcListSingleton.getSFCCount() + 1
        sfcInstance = SFC(sfcid, MaxSFCDelay, MinSFCReliablity, VNFList, datetime.datetime.now())
        # 接下来判断此SFC是否满足时延和可靠性的约束
        if(sfcInstance.get_SFC_delay(VNFList) < MaxSFCDelay):
            if(sfcInstance.get_SFC_relialibility(VNFList) > MinSFCReliablity
                    and sfcInstance.SFC_id not in sfcListSingleton.SFCList):# 此SFC没有被选择过
                sfcInstance.setDelay(sfcInstance.get_SFC_delay(VNFList))
                # SFC满足要求,返回值是SFC实例
                sfcListSingleton.addSFCCount()
                sfcInstance.SFC_id = sfcListSingleton.getSFCCount()+1
                sfcListSingleton.addSFC(sfcListSingleton.getSFCCount()+1)
                return sfcInstance
            else:
                print("此SFC实例的可靠性不满足要求")
        else:
            print("此SFC实例的时延不满足要求")

    # 寻找一条满足约束条件的SFC
    # 输入的参数：SFC所需要的最大时延、最低可靠性、VNF类型列表、VNF所需CPU资源的列表、VNF所需内存资源的列表
    def find_a_SFC1(self, MaxSFCDelay, MinSFCReliablity, VNFTyprList, VNFRequestCPU, VNFRequestMemory):
        print("发现一条SFC方法开始")
        # 存储根据VNF类型和所需CPU、内存资源条件筛选出来的VNFs
        VNFList = []
        for i in range(len(VNFTyprList)):
            vnftype = VNFTyprList[i]
            vnfid = self.getAVNFByType(vnftype)
            if vnfid != None:
                aVNFInstance = VNF(vnfid, vnfListSingelton.dict_VNFListType[vnfid],
                                   vnfListSingelton.dict_VNFRequestCPU[vnfid],
                                   vnfListSingelton.dict_VNFRequestMemory[vnfid],
                                   vnfListSingelton.dict_locatedVMID[vnfid],
                                   vnfListSingelton.dict_locatedSFCIDList[vnfid],
                                   vnfListSingelton.dict_numbersOnSFCList[vnfid],
                                   vnfListSingelton.dict_VNFReliability[vnfid])
                vmid = aVNFInstance.get_VM_id(vnfid)
                vmInstance = VM(vmid, vmListSingelton.dict_VMRequestCPU[vmid],
                                vmListSingelton.dict_VMRequestMemory[vmid],
                                vmListSingelton.dict_VMLocatedPhysicalnode[vmid],
                                vmListSingelton.dict_VMReliability[vmid])
                nodeid = vmInstance.get_physicalNode_id(vmid)
                physicalInstace = PhysicalNode(nodeid, nodeListSingelton.dict_capacity_CPU[nodeid],
                                               nodeListSingelton.dict_capacity_Memory[nodeid],
                                               nodeListSingelton.dict_provided_reliablity[nodeid])
                if (physicalInstace.getAvailable_CPU(nodeid) > VNFRequestCPU[i] and
                        physicalInstace.getAvailable_Memory(nodeid) > VNFRequestMemory[i]):
                    # 将此VNF的id加入到list中，作为此SFC中的一环
                    VNFList.append(vnfid)
            else:
                print("VNFid = none")
        # 所有需要的VNF都找到了，一条SFC就挑选出来了
        sfcid = self.SFCCount + 1
        sfcInstance = SFC(sfcid, MaxSFCDelay, MinSFCReliablity, VNFList, datetime.datetime.now())
        # 接下来判断此SFC是否满足时延和可靠性的约束
        print("SFC的时延与可靠性分别为：")
        print("SFC的时延为：%f" % (sfcInstance.get_SFC_delay(VNFList)))
        print("SFC的可靠性为：%f" % (sfcInstance.get_SFC_relialibility(VNFList)))

        if (sfcInstance.get_SFC_delay(VNFList) < MaxSFCDelay):
            if (sfcInstance.get_SFC_relialibility(VNFList) > MinSFCReliablity):
                    # and sfcInstance.SFC_id not in sfcListSingleton.getSFCList()):  # 此SFC没有被选择过
                sfcInstance.setDelay(sfcInstance.get_SFC_delay(VNFList))
                # SFC满足要求,返回值是SFC实例
                sfcListSingleton.addSFCCount()
                sfcInstance.SFC_id = sfcListSingleton.getSFCCount() + 1
                sfcListSingleton.addSFC(sfcListSingleton.getSFCCount() + 1)
                print("SFC基本数据：-------------------------------------")
                print("基本数据--SFC的ID为： %d" % sfcInstance.getSFCId())
                print("基本数据--SFC中的vnflist为：")
                print(VNFList)
                print("基本数据--SFC的时延为： %f" % sfcInstance.get_SFC_delay(VNFList))
                print("基本数据--SFC的可靠性为： %f " % sfcInstance.get_SFC_relialibility(VNFList))
                print("发现一条SFC方法结束")
                return sfcInstance
            else:
                print("此SFC实例的可靠性不满足要求")
        else:
            print("此SFC实例的时延不满足要求")

    # 从所有的VNF中挑选出一个符合VNF类型要求的VNF,VNF type用数字来代替
    def getAVNFByType(self, VNFtype):
        print("***********************根据类型寻找VNF方法开始")
        print("vnftype = ")
        print(VNFtype)
        # 网络中总共的VNFs
        allVNFList = vnfListSingelton.getAllVNFList()
        for i in range(len(allVNFList)):
            vnfid = allVNFList[i]
            VNFinstance = VNF(vnfid,
                              vnfListSingelton.dict_VNFListType[vnfid],
                              vnfListSingelton.dict_VNFRequestCPU[vnfid],
                              vnfListSingelton.dict_VNFRequestMemory[vnfid],
                              vnfListSingelton.dict_locatedVMID[vnfid],
                              vnfListSingelton.dict_locatedSFCIDList[vnfid],
                              vnfListSingelton.dict_numbersOnSFCList[vnfid],
                              vnfListSingelton.dict_VNFReliability[vnfid]
                              )
            if VNFinstance.getVNFType(allVNFList[i]) == VNFtype \
                    and allVNFList[i] not in self.VNFHadPicked1:
                self.VNFHadPicked1.append(allVNFList[i])
                print("根据类型寻找VNF方法结束，vnf为：")
                print(VNFinstance.VNF_id)
                return VNFinstance.VNF_id
        print("根据类型寻找VNF方法结束，VNF为空")
        return None

    # 时延最小算法
    def delaymin(self):
        l1 = [1, 6, 11, 16, 21]
        l2 = [2, 7, 12, 17, 22]
        l3 = [3, 8, 13, 18, 23]
        l4 = [4, 9, 14, 19, 24]
        l5 = [5, 10, 15, 20, 25]
        for i in range(len(l3)):
            for j in range(len(l4)):
                # for k in range(len(l5)):
                    v1 = l3[i]
                    v2 = l4[j]
                    # v3 = l5[k]
                    # vnflist = [v1, v2, v3]
                    vnflist = [v1, v2]
                    delay = self.get_SFC_delay(vnflist)
                    if(delay <= 200):
                        print("vnflist = ")
                        print(vnflist)
                        print("delay = %f" % delay)
