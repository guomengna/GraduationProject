"""将此类设置为单例类，类似于SFCList与VNFList"""
import xlrd


class VMList(object):
    print("This is VMList class.")
    VMCount = 0
    # 存储VM的ID的列表
    AllVMList = []
    # 存储VM所需要的CPU资源
    dict_VMRequestCPU = {}
    # 存储VM所需要的内存资源
    dict_VMRequestMemory = {}
    # 存储VM所在的物理节点的ID
    dict_VMLocatedPhysicalnode = {}
    # 存储VM的可靠性
    dict_VMReliability = {}

    excelFile = xlrd.open_workbook('D:/pycharm workspace'
                                   '/GraduationProject/topo/'
                                   'allVMList.xlsx', 'r')
    nums = len(excelFile.sheets())
    for i in range(nums):
        # 根据sheet顺序打开sheet
        sheet1 = excelFile.sheets()[i]
    nrows = sheet1.nrows  # 行
    ncols = sheet1.ncols  # 列
    for i in range(nrows):
        list = sheet1.row_values(i)
        AllVMList.append(int(list[0]))
        dict_VMRequestCPU[int(list[0])] = list[1]
        dict_VMRequestMemory[int(list[0])] = list[2]
        dict_VMLocatedPhysicalnode[int(list[0])] = list[3]
        dict_VMReliability[int(list[0])] = list[4]
    # print(AllVMList)
    # 更新网络中VM的数量
    VMCount = len(AllVMList)
    # print(dict_VMRequestCPU)
    # print(dict_VMRequestMemory)
    # print(dict_VMLocatedPhysicalnode)
    # print(dict_VMReliability)
vmListSingelton = VMList()

"""VM创建实例的格式如下：
vmInstance = VM(vmId, vmListSingelton.dict_VMRequestCPU[vmId],
                    vmListSingelton.dict_VMRequestMemory[vmId],
                    vmListSingelton.dict_VMLocatedPhysicalnode[vmId],
                    vmListSingelton.dict_VMReliability[vmId])
"""