"""SFC初始形成"""
#SFC初始形成方法
# VNF_list里边包含VNF id、需求的资源、类型
from entity.PhysicalNode import PhysicalNode
from entity.SFC import SFC
from entity.SFCList import sfcListSingleton
from entity.VM import VM
from entity.VNF import VNF
from entity.VNFList import vnfListSingelton
class SFCInitialFormat():
    K = 6
    # 存放找出来的前K个SFC
    foundSFCList = None
    def SFC_initial_formed(self, request_delay, request_reliability, VNFTyprList, VNFRequestCPU, VNFRequestMemory):
        # step1，寻找前K个满足约束条件的SFC
        while len(self.foundSFCList) < self.K:
            self.foundSFCList.append(self.find_a_SFC(request_delay,
                                                     request_reliability, VNFTyprList, VNFRequestCPU, VNFRequestMemory))
        # step2, 判断每条SFC加入后是否会引起节点过载，并预测过载程度
        # 存放每条SFC的评分
        scoreList = None
        maxScore = 0  # 最高评分
        maxScoreSFCId = None  # 拥有最高评分的SFC的id
        # 挨个分析每一条SFC
        for i in self.K:
            analysisSFC = self.foundSFCList[i]
            # 但是由于挑选VNF的时候已经确定了VNF能够提供足够多的资源，所以挑选出来的SFC都不会过载？
            # 可以选择将VNF的资源需求值上升一个随机（比如说增加从0到0.1之间的任意数倍）的倍数，防止运行中需求的资源会上升。
            # 再去预测是否会过载（但这个还是留待提升阶段再用吧）
            # 现阶段的节点过载程度都为0，节点的可靠性没有变化，即每条SFC加入后对网络中已有SFC的影响值为0

            # step3,为每条SFC评分，选择出评分最高的SFC作为初始形成的SFC
            # 评分标准简化为时延的相反数，此值越小越好
            scoreList.append(self.SFC_placement_plan_scoring(analysisSFC.getSFCId()))
            if maxScore < self.SFC_placement_plan_scoring(analysisSFC.getSFCId()):
                maxScore = self.SFC_placement_plan_scoring(analysisSFC.getSFCId())
                maxScoreSFCId = analysisSFC.getSFCId()
        # 将拥有最高可靠性的SFC加入到SFCList单例中
        sfcListSingleton.addSFC(maxScoreSFCId)
        # 返回拥有最高得分的SFC，作为最初的SFC部署方案
        return maxScoreSFCId

    # SFC部署方案的评分方法
    def SFC_placement_plan_scoring(self, SFC_id):
        # SFC的得分
        score = 0
        for i in len(self.foundSFCList):
            if SFC_id == self.foundSFCList[i].getSFCId():
                score = -self.foundSFCList[i].getDelay(SFC_id)
            break
        return score

    # 寻找一条满足约束条件的SFC
    # 输入的参数：SFC所需要的最大时延、最低可靠性、VNF类型列表、VNF所需CPU资源的列表、VNF所需内存资源的列表
    def find_a_SFC(self, MaxSFCDelay, MinSFCReliablity, VNFTyprList, VNFRequestCPU, VNFRequestMemory):
        # 存储根据VNF类型和所需CPU、内存资源条件筛选出来的VNFs
        VNFList = None
        for i in len(VNFTyprList):
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
        sfcInstance = SFC(MaxSFCDelay, MinSFCReliablity, VNFList)
        # 接下来判断此SFC是否满足时延和可靠性的约束
        if(sfcInstance.get_SFC_delay() < MaxSFCDelay):
            if(sfcInstance.get_SFC_relialibility(VNFList) > MinSFCReliablity
                    and sfcInstance.SFC_id not in sfcListSingleton.SFCList):# 此SFC没有被选择过
                sfcInstance.setDelay(sfcInstance.get_SFC_delay())
                # SFC满足要求,返回值是SFC实例
                sfcListSingleton.addSFCCount()
                sfcInstance.SFC_id = sfcListSingleton.getSFCCount()+1
                sfcListSingleton.addSFC(sfcListSingleton.getSFCCount()+1)
                return sfcInstance
            else:
                print("此SFC实例的可靠性不满足要求")
        else:
            print("此SFC实例的时延不满足要求")

    # 从所有的VNF中挑选出一个符合VNF类型要求的VNF,VNF type用数字来代替
    def getAVNFByType(VNFtype):
        # 网络中总共的VNFs
        allVNFList = vnfListSingelton.getAllVNFList()
        # 同类型中已经被选过的VNF列表
        VNFHadPicked = None
        for i in len(allVNFList):
            VNFinstance = VNF()
            if(VNFinstance.getVNFType(allVNFList[i]) == VNFtype and allVNFList[i] not in VNFHadPicked):
                VNFHadPicked.append(allVNFList[i])
                return VNFinstance
            else:
                return None
