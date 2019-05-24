"""从文件中读取系统中总共的物理节点，包括物理节点的所有属性"""
import xlrd


class PhysicalNodeList(object):
    # 存放所有的物理节点的id
    nodeList = []
    # 存放物理节点可以提供的CPU资源
    dict_capacity_CPU = {}
    # 存放物理节点可以提供的内存资源
    dict_capacity_Memory = {}
    # 存放物理节点可以提供的可靠性
    dict_provided_reliablity = {}
    excelFile = xlrd.open_workbook('D:/pycharm workspace'
                                   '/GraduationProject/topo/'
                                   'NodeList_copy.xlsx', 'r')
    nums = len(excelFile.sheets())
    for i in range(nums):
        # 根据sheet顺序打开sheet
        sheet1 = excelFile.sheets()[i]
    nrows = sheet1.nrows  # 行
    ncols = sheet1.ncols  # 列
    for i in range(nrows):
        list = sheet1.row_values(i)
        nodeList.append(int(list[0]))
        dict_capacity_CPU[int(list[0])] = list[1]
        dict_capacity_Memory[int(list[0])] = list[2]
        dict_provided_reliablity[int(list[0])] = list[3]
    print(nodeList)
    print(dict_capacity_CPU)
    print(dict_capacity_Memory)
    print("dict_provided_reliablity = ")
    print(dict_provided_reliablity)

    """缺少对nodeList的赋值操作"""
    def setNodeList(self):
        """给nodeList赋值方法体"""

    def getNodeList(self):
        return self.nodeList

nodeListSingelton = PhysicalNodeList()

"""物理节点创建实例的格式如下：
nodeInstance = PhysicalNode(nodeId, nodeListSingelton.dict_capacity_CPU[nodeId],
                    nodeListSingelton.dict_capacity_Memory[nodeId],
                    nodeListSingelton.dict_provided_reliablity[nodeId])
"""