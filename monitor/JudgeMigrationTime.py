"""迁移时机判断"""
from entity.SFC import SFC

#总体可靠性下降程度阈值
THRESHOLD_DEGREE = 0.1

class JudgeMigrationTime():
    print("this is JudgeMigrationTime class")
    # 需要迁移的SFC列表
    neededMigrationSFCList = []
    totalReliabilityBelowDegree = 0
    # 需要迁移的SFC的可靠性下降程度的列表
    reliabilityBelowDegreeList = []

    #判断是否该进行SFC迁移,根据monitor中的unreliableSFCList判断
    def ifNeedMigration(self, unreliableSFCList):
        needIf = False
        if(len(unreliableSFCList)>0):
            needIf = True
        return needIf

    #判断是需要迁移一条SFC还是多条SFC,返回True代表需要迁移一条
    def migrationOneOrMore(self, unreliableSFCList, unreliableSFCReliabilityList):
        self.neededMigrationSFCList = []
        self.totalReliabilityBelowDegree = 0
        self.reliabilityBelowDegreeList = []

        for i in range(len(unreliableSFCList)):
            SFCInstance = SFC(unreliableSFCList[i])
            requiredReliability = SFCInstance.getRequestMinReliability()
            reliabilityBelowDegree = (requiredReliability - unreliableSFCReliabilityList[i])/requiredReliability
            self.totalReliabilityBelowDegree += reliabilityBelowDegree
            self.neededMigrationSFCList.append(unreliableSFCList[i])
            self.reliabilityBelowDegreeList.append(reliabilityBelowDegree)
            if (self.totalReliabilityBelowDegree >= THRESHOLD_DEGREE):
                return True
            else:
                return False

    #获取需要迁移的SFC的可靠性下降程度的列表
    def getReliabilityBelowDegreeList(self):
        return self.reliabilityBelowDegreeList

    # 获取需要迁移的SFC列表
    def getNeededMigrationSFCList(self):
        return self.neededMigrationSFCList