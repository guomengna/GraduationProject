"""记录网络中所有的VNF数量和ID"""
#网络中VNF list是作为网络的输入值的，即系统开始运行的时候就要确定网络中的VNF list
#此文件要在系统刚开始的时候就调用，给allVNFList赋值
import xlrd

class VNFList(object):
    # 存放网络中所有的VNF的ID
    allVNFList = []
    # 存放网络中总共拥有的VNF的数量
    allVNFCount = 0

    excelFile = xlrd.open_workbook('D:/pycharm workspace'
                                   '/GraduationProject/topo/'
                                   'allVNFList_copy.xlsx', 'r')
    nums = len(excelFile.sheets())
    for i in range(nums):
        # 根据sheet顺序打开sheet
        sheet1 = excelFile.sheets()[i]
    nrows = sheet1.nrows  # 行
    ncols = sheet1.ncols  # 列
    for i in range(nrows):
        list = sheet1.row_values(i)
        allVNFList.append(int(list[0]))
    # 打印出所有VNF的ID
    # for i in range(len(allVNFList)):
    #     print(allVNFList[i])

    # 读入之后更新网络中VNF的总数量
    allVNFCount = len(allVNFList)
    print("allVNFCount = %d" % allVNFCount)

    # 存放当前网络中激活的VNF的id
    activeVNFList = []
    # 网络中所有激活的VNF的数量
    activeVNFCount = 0
    excelFile = xlrd.open_workbook('D:/pycharm workspace'
                                   '/GraduationProject/topo/'
                                   'activeVNFList.xlsx', 'r')
    nums = len(excelFile.sheets())
    for i in range(nums):
        # 根据sheet顺序打开sheet
        sheet1 = excelFile.sheets()[i]
    nrows = sheet1.nrows  # 行
    ncols = sheet1.ncols  # 列
    for i in range(nrows):
        list = sheet1.row_values(i)
        activeVNFList.append(int(list[0]))
    # 更新网络中所有激活的VNF的数量（此时所用的数据，网络中所有的VNF都是被激活的）
    activeVNFCount = len(activeVNFList)
    print("activeVNFCount = %d" % activeVNFCount)

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

    # 存放网络中所有VNF的种类（用字典存储，（VNFID，VNF种类））,以下几个值都是字典存储
    VNFListType = []
    dict_VNFListType = {}
    # 存放VNF所需的CPU资源
    VNFRequestCPU = []
    dict_VNFRequestCPU = {}
    # 存放VNF所需的内存资源
    VNFRequestMemory = []
    dict_VNFRequestMemory = {}
    # 存放所在的VM的id
    locatedVMID = []
    dict_locatedVMID = {}
    # 存放所处的SFC的id的列表
    locatedSFCIDList = []
    dict_locatedSFCIDList = {}
    # 存放所处SFC上的位置编号的列表
    numbersOnSFCList = []
    dict_numbersOnSFCList = {}
    # 存放此VNF的可靠性
    VNFReliability = []
    dict_VNFReliability = {}

    for i in range(nrows):
        list = sheet1.row_values(i)
        VNFListType.append(list[1])
        dict_VNFListType[int(list[0])] = int(list[1])
        VNFRequestCPU.append(list[2])
        dict_VNFRequestCPU[int(list[0])] = int(list[2])
        VNFRequestMemory.append(list[3])
        dict_VNFRequestMemory[int(list[0])] = int(list[3])
        locatedVMID.append(list[4])
        dict_locatedVMID[int(list[0])] = int(list[4])
        locatedSFCIDList.append(list[5])
        dict_locatedSFCIDList[int(list[0])] = int(list[5])
        numbersOnSFCList.append(list[6])
        dict_numbersOnSFCList[int(list[0])] = int(list[6])
        VNFReliability.append(list[7])
        dict_VNFReliability[int(list[0])] = list[7]
    # for i in range(len(activeVNFList)):
    #     print("%d %d %d %d %d %d %d %f" %(activeVNFList[i], VNFListType[i], VNFRequestCPU[i], VNFRequestMemory[i]
    #                            , locatedVMID[i], locatedSFCIDList[i], numbersOnSFCList[i], VNFReliability[i]))
    # print(dict_VNFListType)
    # print(dict_VNFRequestCPU)
    # print(dict_VNFRequestMemory)
    # print(dict_locatedVMID)
    # print(dict_locatedSFCIDList)
    # print(dict_numbersOnSFCList)
    # print(dict_VNFReliability)

    def get_dict_VNFListType(self):
        return self.dict_VNFListType

    def get_dict_VNFRequestCPU(self):
        return self.dict_VNFRequestCPU

    def get_dict_VNFRequestMemory(self):
        return self.dict_VNFRequestMemory

    def get_dict_locatedVMID(self):
        return self.dict_locatedVMID

    def get_dict_locatedSFCIDList(self):
        return self.dict_locatedSFCIDList

    def get_dict_numbersOnSFCList(self):
        return self.dict_numbersOnSFCList

    def get_dict_VNFReliability(self):
        return self.dict_VNFReliability

vnfListSingelton = VNFList()
"""VNF创建实例的格式如下：
VNFInstance = VNF(VNFid,
               vnfListSingelton.dict_VNFListType[VNFid],
               vnfListSingelton.dict_VNFRequestCPU[VNFid],
               vnfListSingelton.dict_VNFRequestMemory[VNFid],
               vnfListSingelton.dict_locatedVMID[VNFid],
               vnfListSingelton.dict_locatedSFCIDList[VNFid],
               vnfListSingelton.dict_numbersOnSFCList[VNFid],
               vnfListSingelton.dict_VNFReliability[VNFid]
               )
"""