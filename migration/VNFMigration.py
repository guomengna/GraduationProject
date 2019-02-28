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
    def findDestinationForVNF(self, vnfId):
        # 满足约束条件的都可作为VNF迁移的目的地

        """调用方法：判断某个物理节点是否可以是该VNF迁移的目的地"""

    # 判断某个物理节点是否是某个VNF迁移的目的地
    # 输入参数为vnf id 与node id，返回布尔值
    def judgeIfIsDestination(self, vnfId, nodeId):
        """根据约束条件判断"""