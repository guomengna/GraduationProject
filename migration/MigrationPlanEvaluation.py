"""迁移方案评价"""
from entity.SFC import SFC
from entity.SFCList import sfcListSingleton
from migration.MigrationCostCaculation import MigrationCostCaculation

class MigrationPlanEvaluation():
    print("this is MigrationPlanEvaluation class")
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
        for SFCId in sfcListSingleton.getSFCList():
            SFCInstance = SFC(SFCId,
                              sfcListSingleton.dict_maxDelay[SFCId],
                              sfcListSingleton.dict_minReliability[SFCId],
                              sfcListSingleton.dict_VNFList[SFCId],
                              sfcListSingleton.dict_createdtime[SFCId]
                              )
            totalRelibility += SFCInstance.get_SFC_relialibility(SFCInstance.getVNFList())
            print("totalRelibility = %f" %totalRelibility)

        costInstance = MigrationCostCaculation()
        cost = costInstance.getCostOfMigratingVNFsOnOneSFC(self.migrated_SFC_id, self.SFCDelayBeforMigration,
                                                    self.SFCRequestedResourceBefore, self.needMigratedVNFList,
                                                    self.destinationPhysicalNodeList)
        print("cost = %f" %cost)
        return 100 + totalRelibility - cost
