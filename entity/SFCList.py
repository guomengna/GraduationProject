"""将此类设置为单例模式，用于记录SFC的个数"""
class SFCList(object):
    print("this is SFCList")
    SFCCount = 0
    AllSFCList = []
    def getSFCCount(self):
        return self.SFCCount
    def getSFCList(self):
        return self.AllSFCList
    def addSFCCount(self):
        self.SFCCount += 1

    def deleteSFCCount(self):
        self.SFCCount -= 1

    def addSFC(self,SFCID):
        self.AllSFCList.append(SFCID)

    def deleteSFC(self, SFCID):
        self.AllSFCList.remove(SFCID)
sfcListSingleton = SFCList()