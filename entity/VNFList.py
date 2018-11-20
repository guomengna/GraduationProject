"""记录网络中所有的VNF数量和ID"""
#网络中VNF list是作为网络的输入值的，即系统开始运行的时候就要确定网络中的VNF list
#此文件要在系统刚开始的时候就调用，给allVNFList赋值
class VNFList(object):
    #存放网络中所有的VNF的ID
    allVNFList = None
    allVNFCount = 0
    #存放当前网络中激活的VNF的id
    activeVNFList = None
    activeVNFCount = 0
    #激活的VNF部分
    def addActiveVNFList(self, VNFID):
        self.activeVNFList.append(VNFID)
        self.activeVNFCount += 1

    def deleteActiveVNFList(self, VNFID):
        self.activeVNFList.remove(VNFID)
        self.activeVNFCount -= 1

    def getActiveVNFList(self):
        return self.activeVNFList

    def getActiveVNFCount(self):
        return self.activeVNFCount

    #全部的VNF部分，包括激活的与未激活的
    def setAllVNFCount(self, allCount):
        self.allVNFCount = allCount

    def setAllVNFList(self, allVNFList):
        self.allVNFList = allVNFList

    def getAllVNFList(self):
        return self.allVNFList

    def getAllVNFCount(self):
        return self.allVNFCount

vnfListSingelton = VNFList()