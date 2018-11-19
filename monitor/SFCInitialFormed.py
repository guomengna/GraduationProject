"""SFC初始形成"""
#SFC初始形成方法
# VNF_list里边包含VNF id、需求的资源、类型
from entity.PhysicalNode import PhysicalNode
from entity.SFC import SFC
from entity.VM import VM
from entity.VNF import VNF


def SFC_initial_formed(self, request_delay, request_reliability, VNF_list):
    #step1，寻找前K个满足约束条件的SFC

    return None

#SFC部署方案的评分方法
def SFC_placement_plan_scoring():

    return None

# 寻找一条满足约束条件的SFC
# 输入的参数：SFC所需要的最大时延、最低可靠性、VNF类型列表、VNF所需CPU资源的列表、VNF所需内存资源的列表
def find_a_SFC(MaxSFCDelay, MinSFCReliablity, VNFTyprList, VNFRequestCPU, VNFRequestMemory):
    #存储根据VNF类型和所需CPU、内存资源条件筛选出来的VNFs
    VNFList = None
    for i in len(VNFTyprList):
        aVNFInstance = VNF()
        vmInstance = VM()
        physicalInstace = PhysicalNode()
        vmId = aVNFInstance.get_VM_id(getAVNFByType())
        physicalNodeId = vmInstance.get_physicalNode_id(vmId)
        if(physicalInstace.getAvailable_CPU(physicalNodeId) > VNFRequestCPU and
        physicalInstace.getAvailable_Memory(physicalNodeId) > VNFRequestMemory):
            #将此VNF的id加入到list中，作为此SFC中的一环
            VNFList.appends(getAVNFByType())
    #所有需要的VNF都找到了，一条SFC就挑选出来了
    sfcInstance = SFC(MaxSFCDelay, MinSFCReliablity, VNFList)
    #接下来判断此SFC是否满足时延和可靠性的约束
    if(sfcInstance.get_SFC_delay() < MaxSFCDelay):
        if(sfcInstance.get_SFC_relialibility(VNFList) > MinSFCReliablity):
            #SFC满足要求,返回值是什么呢？SFC的id吗？id还没生成
            return True

    return None

# 从所有的VNF中挑选出一个符合VNF类型要求的VNF
def getAVNFByType():
    return None#返回的是被选中VNF的id
