"""VNF迁移"""
from entity.PhysicalNode import PhysicalNode
from entity.SFC import SFC
from entity.SFCList import sfcListSingleton
from entity.VM import VM
from entity.VNF import VNF


class VNFMigration():
    # 迁移一条SFC
    def migrateVNFsofOneSFC(self):
        # 每次迁移的这一条SFC应该是当前网络中可靠性最低的一条
        migratedsfcId = self.findSFCWithMinReliability()
        # 判断此SFC上所有的VNF所处的节点是否过载
        (overloadNodeListId, migratedVNFList) = self.judgingIfNodeOverload(migratedsfcId)
        #为每个migratedVNFList中的VNF计算其目的地
        for vnfId in migratedVNFList:
            """调用为VNF计算所有的目的地list"""

        return None

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
        # 满足约束条件的都可作为VNF迁移的目的地

        """调用方法：判断某个物理节点是否可以是该VNF迁移的目的地"""

    # 判断某个物理节点是否是某个VNF迁移的目的地
    # 输入参数为vnf id 与node id，返回布尔值
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

        # 2.获取到网络中迁移状态之后的所有节点及它们的负载程度（用资源利用率来衡量）
        # 3.判断负载偏差程度是否满足预先设定的阈值，即小于η
        """未完待续"""
