"""迁移代价计算类"""
import time

from entity.SFC import SFC
from entity.SFCList import sfcListSingleton
from entity.VM import VM
from entity.VNF import VNF


class MigrationCostCaculation():
    """迁移一条SFC Si上的VNFs所需要的代价计算"""
    def getCostOfMigratingVNFsOnOneSFC(self, migrated_SFC_id, SFCDelayBeforMigration,
                                       SFCRequestedResourceBefore, needMigratedVNFList,
                                       destinationPhysicalNodeList):
        # 由5部分组成：迁移Si上VNF所需要的时间、迁移后Si的时延增量、
        # 迁移后消耗的资源的增量、迁移过程中造成的Si的服务质量下降程度、迁移Si上的VNF造成的额外代价
        migrationTime = self.getMigrationTime(migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList)
        delayIncreationOfSFC = self.getDelayIncreationOfSFC(migrated_SFC_id, SFCDelayBeforMigration)
        resourceIncreationOfSFC = self.getResourceIncreationOfSFC(migrated_SFC_id, SFCRequestedResourceBefore)
        QoSDecreationOfSFC = self.getQoSDecreationOfSFC(migrated_SFC_id,
                                                        needMigratedVNFList, destinationPhysicalNodeList)
        costOfMigratingVNFsOnOneSFC = migrationTime + delayIncreationOfSFC \
                                      + resourceIncreationOfSFC + QoSDecreationOfSFC
        return costOfMigratingVNFsOnOneSFC

    # 迁移Si上的VNF所需要消耗的时间
    def getMigrationTime(self, migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList):
        # 存放此SFC上需要迁移的VNF们的迁移所需要的时间
        VNFsMigrationTimeList = []
        # 由SFC的ID得到此条SFC上所有的VNF
        SFCInstance = SFC(migrated_SFC_id)
        VNFList = SFCInstance.getVNFList
        # 寻找此SFC上应当进行迁移的VNF(s),根据不同的迁移情形分别获取，在本项目中的其他位置实现此方法
        # 假设此时在此处已经获取到了需要迁移的VNF，即为needMigratedVNFList,此列表作为输入参数由外部传入
        # 系统开始运行之前随机给每个VNF赋一个迁移时间的系数，当迁移发生时，此系数乘以源至目的地的距离，作为相对迁移时间。
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
    def getDelayIncreationOfSFC(self, migrated_SFC_id, SFCDelayBeforMigration):
        SFCInstance = SFC(migrated_SFC_id)
        VNFList = SFCInstance.getVNFList
        SFCDelayAfterMigration = SFCInstance.get_SFC_delay(VNFList)
        return SFCDelayAfterMigration - SFCDelayBeforMigration

    # 迁移后此SFC消耗资源的增量
    def getResourceIncreationOfSFC(self, migrated_SFC_id, SFCRequestedResourceBefore):
        sfcInstance = SFC(migrated_SFC_id)
        SFCRequestedResourceAfter = sfcInstance.getSFCRequestedResource()
        return SFCRequestedResourceAfter - SFCRequestedResourceBefore

    # 迁移过程中造成的Si的服务质量下降程度
    def getQoSDecreationOfSFC(self, migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList):
        # beta1与beta2分别表示Si重要性与SFC暂停时间对服务质量的影响程度
        beta1 = 0.5
        beta2 = 0.5
        servicePauseTime = self.getMigrationTime(migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList)
        allSFCsImportance = 0
        for sfcInstanceId in sfcListSingleton:
            sfcInstance = SFC(sfcInstanceId)
            allSFCsImportance += sfcInstance.importance
        QoSDecreationOfSFC = beta1 * (SFC(migrated_SFC_id).importance/allSFCsImportance)
        + beta2 * (servicePauseTime/(time.time - SFC(migrated_SFC_id).create_time))
        return QoSDecreationOfSFC

    # 迁移Si上的VNF造成的额外代价
    def getAdditonalCostOfSFC(self, migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList):
        additionDelay = 0
        # 考虑每个需要迁移的VNF
        for i in range(len(needMigratedVNFList)):
            vnfInstanceId = needMigratedVNFList[i]
            vnfInstance = VNF(vnfInstanceId)
            SFCIdListOfThisVNF = vnfInstance.SFC_id_list
            # 考虑此VNF经过的每一个SFC
            for sfcId in SFCIdListOfThisVNF:
                if(sfcId != migrated_SFC_id):
                    # VNF位于除此条SFC之外的其他SFC上
                    SFCInstance = SFC(sfcId)
                    delayBefore = SFCInstance.getDelay()
                    # 更新SFC中的VNFList
                    VNFList = SFCInstance.getVNFList()
                    VMInstance = VM(vnfInstance.get_VM_id(vnfInstanceId))
                    VMInstance.setPhysicalNodeId(destinationPhysicalNodeList[i])
                    SFCInstance.setVNFList(VNFList)
                    # 更新SFC的VNFList之后重新计算SFC的时延
                    delayAfter = SFCInstance.get_SFC_delay(VNFList)
                    additionDelay += delayAfter - delayBefore
        return additionDelay