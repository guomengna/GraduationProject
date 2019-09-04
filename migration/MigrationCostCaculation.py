"""迁移代价计算类"""
import time

from entity.SFC import SFC
from entity.SFCList import sfcListSingleton
from entity.VM import VM
from entity.VMList import vmListSingelton
from entity.VNF import VNF
from entity.VNFList import vnfListSingelton


class MigrationCostCaculation():
    print("this is MigrationCostCaculation class")
    """迁移一条SFC Si上的VNFs所需要的代价计算"""
    def getCostOfMigratingVNFsOnOneSFC(self, migrated_SFC_id, SFCDelayBeforMigration,
                                       SFCRequestedResourceBefore, needMigratedVNFList,
                                       destinationPhysicalNodeList):
        print("needMigratedVNFList = ")
        print(needMigratedVNFList)
        print("destinationPhysicalNodeList = ")
        print(destinationPhysicalNodeList)
        # 由5部分组成：迁移Si上VNF所需要的时间、迁移后Si的时延增量、
        # 迁移后消耗的资源的增量、迁移过程中造成的Si的服务质量下降程度、迁移Si上的VNF造成的额外代价
        migrationTime = self.getMigrationTime(migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList)
        print("migrationTime = %f" % migrationTime)
        delayIncreationOfSFC = self.getDelayIncreationOfSFC(migrated_SFC_id, SFCDelayBeforMigration)
        print("delayIncreationOfSFC = %f" %delayIncreationOfSFC)
        resourceIncreationOfSFC = self.getResourceIncreationOfSFC(migrated_SFC_id, SFCRequestedResourceBefore)
        print("resourceIncreationOfSFC = %f" %resourceIncreationOfSFC)
        QoSDecreationOfSFC = self.getQoSDecreationOfSFC(migrated_SFC_id,
                                                        needMigratedVNFList, destinationPhysicalNodeList)
        print("QoSDecreationOfSFC = %f" %QoSDecreationOfSFC)
        additionnalCost = self.getAdditonalCostOfSFC(migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList)
        print("additionnalCost = %f" %additionnalCost)
        costOfMigratingVNFsOnOneSFC = migrationTime + delayIncreationOfSFC \
                                      + resourceIncreationOfSFC + QoSDecreationOfSFC + additionnalCost
        return costOfMigratingVNFsOnOneSFC

    # 迁移Si上的VNF所需要消耗的时间
    def getMigrationTime(self, migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList):
        # 存放此SFC上需要迁移的VNF们的迁移所需要的时间
        VNFsMigrationTimeList = []
        # 由SFC的ID得到此条SFC上所有的VNF
        SFCInstance = SFC(migrated_SFC_id,
                          sfcListSingleton.dict_maxDelay[migrated_SFC_id],
                          sfcListSingleton.dict_minReliability[migrated_SFC_id],
                          sfcListSingleton.dict_VNFList[migrated_SFC_id],
                          sfcListSingleton.dict_createdtime[migrated_SFC_id]
                          )
        VNFList = SFCInstance.getVNFList
        total_time = 0
        # 寻找此SFC上应当进行迁移的VNF(s),根据不同的迁移情形分别获取，在本项目中的其他位置实现此方法
        # 假设此时在此处已经获取到了需要迁移的VNF，即为needMigratedVNFList,此列表作为输入参数由外部传入
        # 系统开始运行之前随机给每个VNF赋一个迁移时间的系数，当迁移发生时，此系数乘以源至目的地的距离，作为相对迁移时间。
        # 也就是说还需要一个迁移目的地列表，此处同样作为输入参数传入,源到目的地之间的距离直接用拓扑中的时延来代替
        for i in range(len(needMigratedVNFList)):
            vnfid = needMigratedVNFList[i]
            VNFInstance = VNF(vnfid,
                              vnfListSingelton.dict_VNFListType[vnfid],
                              vnfListSingelton.dict_VNFRequestCPU[vnfid],
                              vnfListSingelton.dict_VNFRequestMemory[vnfid],
                              vnfListSingelton.dict_locatedVMID[vnfid],
                              vnfListSingelton.dict_locatedSFCIDList[vnfid],
                              vnfListSingelton.dict_numbersOnSFCList[vnfid],
                              vnfListSingelton.dict_VNFReliability[vnfid]
                              )
            VMId = VNFInstance.get_VM_id(needMigratedVNFList[i])
            VMInstance = VM(VMId,
                            vmListSingelton.dict_VMRequestCPU[VMId],
                            vmListSingelton.dict_VMRequestMemory[VMId],
                            vmListSingelton.dict_VMLocatedPhysicalnode[VMId],
                            vmListSingelton.dict_VMReliability[VMId]
                            )
            physicalNodeId = VMInstance.get_physicalNode_id(VMId)
            # physicalNodeId与destinationPhysicalNodeList[i]两个物理节点之间的时延
            delayBetweenSandDNodes = SFCInstance.getDelayBetweenPhysicalNode(physicalNodeId,
                                                                             destinationPhysicalNodeList[i])
            # 计算出此VNF迁移所花费的时间，并将其存放进VNFsMigrationTimeList中的第i个位置
            VNFsMigrationTimeList.append(delayBetweenSandDNodes * VNFInstance.migration_time_coefficient)
            total_time += delayBetweenSandDNodes * VNFInstance.migration_time_coefficient
        return total_time

    # 更新时延的增量
    def getDelayIncreationOfSFC1(self, migrated_SFC_id, nodebeforelist, nodeafterlist):
        delayadd = 0
        for i in range(len(nodebeforelist)):
            nodebefore = nodebeforelist[i]
            nodeafter = nodeafterlist[i]
            SFCInstance = SFC(migrated_SFC_id, sfcListSingleton.dict_maxDelay[migrated_SFC_id],
                  sfcListSingleton.dict_minReliability[migrated_SFC_id],
                  sfcListSingleton.dict_VNFList[migrated_SFC_id],
                  sfcListSingleton.dict_createdtime[migrated_SFC_id])
            delayadd += SFCInstance.getDelayBetweenPhysicalNode(nodebefore,nodeafter)
        print("delayadd = %f" % delayadd)

    # 迁移后Si时延的增量
    def getDelayIncreationOfSFC(self, migrated_SFC_id, SFCDelayBeforMigration):
        SFCInstance = SFC(migrated_SFC_id,
                          sfcListSingleton.dict_maxDelay[migrated_SFC_id],
                          sfcListSingleton.dict_minReliability[migrated_SFC_id],
                          sfcListSingleton.dict_VNFList[migrated_SFC_id],
                          sfcListSingleton.dict_createdtime[migrated_SFC_id]
                          )
        VNFList = SFCInstance.getVNFList()
        print(VNFList)
        nodeidlist = []
        i = 0
        for vnfid in VNFList:
            if vnfid == 15:
                VNFinstance = VNF(vnfid,
               vnfListSingelton.dict_VNFListType[vnfid],
               vnfListSingelton.dict_VNFRequestCPU[vnfid],
               vnfListSingelton.dict_VNFRequestMemory[vnfid],
               vnfListSingelton.dict_locatedVMID[vnfid],
               vnfListSingelton.dict_locatedSFCIDList[vnfid],
               vnfListSingelton.dict_numbersOnSFCList[vnfid],
               vnfListSingelton.dict_VNFReliability[vnfid])
                vmid = VNFinstance.get_VM_id(vnfid)
                VMinstance = VM(vmid,
                                vmListSingelton.dict_VMRequestCPU[vmid],
                                vmListSingelton.dict_VMRequestMemory[vmid],
                                vmListSingelton.dict_VMLocatedPhysicalnode[vmid],
                                vmListSingelton.dict_VMReliability[vmid]
                                )
                nodeid = VMinstance.get_physicalNode_id(vmid)

                print("before node id = %d" % nodeid)

                VMinstance.setPhysicalNodeId(16)

        SFCDelayAfterMigration = SFCInstance.get_SFC_delay(VNFList)

        print("SFCDelayAfterMigration = %f" %SFCDelayAfterMigration)
        print("SFCDelayBeforMigration = %f" %SFCDelayBeforMigration)
        print(SFCDelayAfterMigration - SFCDelayBeforMigration)
        return SFCDelayAfterMigration - SFCDelayBeforMigration



    # 迁移后此SFC消耗资源的增量
    def getResourceIncreationOfSFC(self, migrated_SFC_id, SFCRequestedResourceBefore):
        sfcInstance = SFC(migrated_SFC_id,
                          sfcListSingleton.dict_maxDelay[migrated_SFC_id],
                          sfcListSingleton.dict_minReliability[migrated_SFC_id],
                          sfcListSingleton.dict_VNFList[migrated_SFC_id],
                          sfcListSingleton.dict_createdtime[migrated_SFC_id]
                          )
        SFCRequestedResourceAfter = sfcInstance.getSFCRequestedResource()
        return SFCRequestedResourceAfter - SFCRequestedResourceBefore

    # 迁移过程中造成的Si的服务质量下降程度
    def getQoSDecreationOfSFC(self, migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList):
        # beta1与beta2分别表示Si重要性与SFC暂停时间对服务质量的影响程度
        beta1 = 0.5
        beta2 = 0.5
        servicePauseTime = self.getMigrationTime(migrated_SFC_id, needMigratedVNFList,
                                                 destinationPhysicalNodeList)
        allSFCsImportance = 0
        for sfcInstanceId in sfcListSingleton.getSFCList():
            sfcInstance = SFC(sfcInstanceId,
                              sfcListSingleton.dict_maxDelay[sfcInstanceId],
                              sfcListSingleton.dict_minReliability[sfcInstanceId],
                              sfcListSingleton.dict_VNFList[sfcInstanceId],
                              sfcListSingleton.dict_createdtime[sfcInstanceId]
                              )
            allSFCsImportance += sfcInstance.importance
        QoSDecreationOfSFC = beta1 * (SFC(migrated_SFC_id, sfcListSingleton.dict_maxDelay[migrated_SFC_id],
                              sfcListSingleton.dict_minReliability[migrated_SFC_id],
                              sfcListSingleton.dict_VNFList[migrated_SFC_id], sfcListSingleton.dict_createdtime[migrated_SFC_id],).importance/allSFCsImportance)
        + beta2 * (servicePauseTime/(time.time() - SFC(migrated_SFC_id, sfcListSingleton.dict_maxDelay[migrated_SFC_id],
                              sfcListSingleton.dict_minReliability[migrated_SFC_id],
                              sfcListSingleton.dict_VNFList[migrated_SFC_id],
                              sfcListSingleton.dict_createdtime[migrated_SFC_id]).create_time))
        return QoSDecreationOfSFC

    # 迁移Si上的VNF造成的额外代价
    def getAdditonalCostOfSFC(self, migrated_SFC_id, needMigratedVNFList, destinationPhysicalNodeList):
        additionDelay = 0
        # 考虑每个需要迁移的VNF
        for i in range(len(needMigratedVNFList)):
            vnfInstanceId = needMigratedVNFList[i]
            vnfInstance = VNF(vnfInstanceId, vnfListSingelton.dict_VNFListType[vnfInstanceId],
               vnfListSingelton.dict_VNFRequestCPU[vnfInstanceId],
               vnfListSingelton.dict_VNFRequestMemory[vnfInstanceId],
               vnfListSingelton.dict_locatedVMID[vnfInstanceId],
               vnfListSingelton.dict_locatedSFCIDList[vnfInstanceId],
               vnfListSingelton.dict_numbersOnSFCList[vnfInstanceId],
               vnfListSingelton.dict_VNFReliability[vnfInstanceId])
            SFCIdListOfThisVNF = vnfInstance.get_SFC_id_list()
            # 考虑此VNF经过的每一个SFC
            # for sfcId in SFCIdListOfThisVNF:
            #     if(sfcId != migrated_SFC_id):
            #         # VNF位于除此条SFC之外的其他SFC上
            #         SFCInstance = SFC(sfcId,
            #                           sfcListSingleton.dict_maxDelay[sfcId],
            #                           sfcListSingleton.dict_minReliability[sfcId],
            #                           sfcListSingleton.dict_VNFList[sfcId],
            #                           sfcListSingleton.dict_createdtime[sfcId]
            #                           )
            #         delayBefore = SFCInstance.getDelay()
            #         # 更新SFC中的VNFList
            #         VNFList = SFCInstance.getVNFList()
                    # VMInstance = VM(vnfInstance.get_VM_id(vnfInstanceId),
                    #                 vmListSingelton.dict_VMRequestCPU[vnfInstance.get_VM_id(vnfInstanceId)],
                    #                 vmListSingelton.dict_VMRequestMemory[vnfInstance.get_VM_id(vnfInstanceId)],
                    #                 vmListSingelton.dict_VMLocatedPhysicalnode[vnfInstance.get_VM_id(vnfInstanceId)],
                    #                 vmListSingelton.dict_VMReliability[vnfInstance.get_VM_id(vnfInstanceId)]
                    #                 )
                    # VMInstance.setPhysicalNodeId(destinationPhysicalNodeList[i])
                    # SFCInstance.setVNFList(VNFList)
                    # # 更新SFC的VNFList之后重新计算SFC的时延
                    # delayAfter = SFCInstance.get_SFC_delay(VNFList)
                    # additionDelay += delayAfter - delayBefore
        return additionDelay