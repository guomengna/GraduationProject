"""将此类设置为单例模式，用于记录SFC的个数"""
class SFCList(object):
    SFCCount = 0
    SFCList = []
    def getSFCCount(self):
        return self.SFCCount
    def getSFCList(self):
        return SFCList
    def addSFCCount(self):
        self.SFCCount += 1

    def deleteSFCCount(self):
        self.SFCCount -= 1

    def addSFC(self,SFCID):
        self.SFCList.append(SFCID)

    def deleteSFC(self, SFCID):
        self.SFCList.remove(SFCID)
sfcListSingleton = SFCList()