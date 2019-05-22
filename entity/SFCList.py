"""将此类设置为单例模式，用于记录SFC的个数"""
import xlrd


class SFCList(object):
    print("this is SFCList")
    SFCCount = 0
    # SFC的ID
    AllSFCList = []
    # 存储SFC允许的最大时延(字典的形式（SFC的id，SFC允许的最大时延）)
    dict_maxDelay = {}
    # SFC需求的最小可靠性
    dict_minReliability = {}
    # SFC中的VNF列表（存储的是（SFC的ID，VNF的列表））
    dict_VNFList = {}
    # SFC创建时间
    dict_createdtime = {}

    excelFile = xlrd.open_workbook('D:/pycharm workspace'
                                   '/GraduationProject/topo/'
                                   'allSFCList.xlsx', 'r')
    nums = len(excelFile.sheets())
    for i in range(nums):
        # 根据sheet顺序打开sheet
        sheet1 = excelFile.sheets()[i]
    nrows = sheet1.nrows  # 行
    ncols = sheet1.ncols  # 列
    for i in range(nrows):
        list = sheet1.row_values(i)
        AllSFCList.append(int(list[0]))
        dict_maxDelay[int(list[0])] = int(list[1])
        dict_minReliability[int(list[0])] = list[2]
        l1 = list[3].split(',')
        # 用templist暂时存储从文件中读取的VNFlist，再将其放入到字典中去
        templist = []
        for i in range(len(l1)):
            templist.append(int(l1[i]))
        # print("templist is : ")
        # print(templist)
        dict_VNFList[int(list[0])] = templist
        dict_createdtime[int(list[0])] = list[4]
    # print("dict_VNFList is : ")
    # print(dict_VNFList)
    print("网络中SFC的ID为： ")
    print(AllSFCList)
    # 更新SFCCount
    SFCCount = len(AllSFCList)
    print("总共有SFC：%d" % SFCCount)

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
"""SFC创建实例的形式如下：
SFCInstance = SFC(SFCid,
                  sfcListSingleton.dict_maxDelay[SFCid],
                  sfcListSingleton.dict_minReliability[SFCid],
                  sfcListSingleton.dict_VNFList[SFCid],
                  sfcListSingleton.dict_createdtime[SFCid]
                  )
"""