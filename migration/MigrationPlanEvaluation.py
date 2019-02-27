"""迁移方案评价"""
from entity.SFC import SFC
from entity.SFCList import sfcListSingleton
from migration.MigrationCostCaculation import MigrationCostCaculation

class MigrationPlanEvaluation():
    """迁移方案评价方法"""
    def __init__(self, migrated_SFC_id, SFCDelayBeforMigration,
                 SFCRequestedResourceBefore, needMigratedVNFList, destinationPhysicalNodeList):
        self.migrated_SFC_id = migrated_SFC_id
        self.SFCDelayBeforMigration = SFCDelayBeforMigration
        self.SFCRequestedResourceBefore = SFCRequestedResourceBefore
        self.needMigratedVNFList = needMigratedVNFList
        self.destinationPhysicalNodeList = destinationPhysicalNodeList

    def evaluation(self):
        totalRelibility = 0
        for SFCId in sfcListSingleton:
            SFCInstance = SFC(SFCId)
            totalRelibility += SFCInstance.get_SFC_relialibility(SFCInstance.getVNFList())

        costInstance = MigrationCostCaculation()
        cost = costInstance.getCostOfMigratingVNFsOnOneSFC(self.migrated_SFC_id, self.SFCDelayBeforMigration,
                                                    self.SFCRequestedResourceBefore, self.needMigratedVNFList,
                                                    self.destinationPhysicalNodeList)
        return 100 + totalRelibility - cost
