"""迁移代价计算类"""
from entity.SFC import SFC
from entity.VM import VM
from entity.VNF import VNF


class MigrationCostCaculation():
    """迁移一条SFC Si上的VNFs所需要的代价计算"""
    def getCostOfMigratingVNFsOnOneSFC(self, migrated_SFC_id):
        # 由5部分组成：迁移Si上VNF所需要的时间、迁移后Si的时延增量、
        # 迁移后消耗的资源的增量、迁移过程中造成的Si的服务质量下降程度、迁移Si上的VNF造成的额外代价

        return None

    # 迁移Si上的VNF所需要消耗的时间
    def getMigrationTime(self, migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList):
        # 存放此SFC上需要迁移的VNF们的迁移所需要的时间
        VNFsMigrationTimeList = []
        # 由SFC的ID得到此条SFC上所有的VNF
        SFCInstance = SFC(migrated_SFC_id)
        VNFList = SFCInstance.getVNFList
        # 寻找此SFC上应当进行迁移的VNF(s),根据不同的迁移情形分别获取，在本项目中的其他位置实现此方法
        # 假设此时在此处已经获取到了需要迁移的VNF，即为needMigratedVNFList,此列表作为输入参数由外部传入
        # 系统开始运行之前随机给每个VNF赋一个迁移时间的系数，当迁移发生时，此系数乘以源值目的地的距离，作为相对迁移时间。
        # 也就是说还需要一个迁移目的地列表，此处同样作为输入参数传入,源到目的地之间的距离直接用拓扑中的时延来代替
        for i in range(len(needMigratedVNFList)):
            VNFInstance = VNF(needMigratedVNFList)
            VMId = VNFInstance.get_VM_id(needMigratedVNFList[i])
            VMInstance = VM(VMId)
            physicalNodeId = VMInstance.get_physicalNode_id(VMId)
            # physicalNodeId与destinationPhysicalNodeList[i]两个物理节点之间的时延
            delayBetweenSandDNodes = SFCInstance.getDelayBetweenPhysicalNode(physicalNodeId, destinationPhysicalNodeList[i])
            # 计算出此VNF迁移所花费的时间，并将其存放进VNFsMigrationTimeList中的第i个位置
            VNFsMigrationTimeList.append(delayBetweenSandDNodes * VNFInstance.migration_time_coefficient)
        return None

    # 迁移后Si时延的增量
    def getDelayIncreationOfSFC(self):
        return None

    # 迁移后此SFC消耗资源的增量
    def getResourceIncreationOfSFC(self):
        return None

    # 迁移过程中造成的Si的服务质量下降程度
    def getQoSDecreationOfSFC(self):
        return None

    # 迁移Si上的VNF造成的额外代价
    def getAdditonalCostOfSFC(self):
        return None


