# -*- coding: utf-8 -*-
import xlrd
from numpy.core.tests.test_mem_overlap import xrange

from entity.VM import VM
from entity.VNF import VNF
excelFile = xlrd.open_workbook('D:/pycharm workspace/GraduationProject/topo/cernet2_added.xlsx', 'r')
nums = len(excelFile.sheets())
leftVNFlist = []
rightVNFlist = []
delaylist = []

for i in range(nums):
    # 根据sheet顺序打开sheet
    sheet1 = excelFile.sheets()[i]
nrows = sheet1.nrows  # 行
ncols = sheet1.ncols  # 列
# 循环行列表数据
for i in range(nrows):
    list = sheet1.row_values(i)
    #print(int(list[0]),int(list[1]),list[8])

    leftVNF = int(list[0])
    leftVNFlist.append(leftVNF)
    rightVNF = int(list[1])
    rightVNFlist.append(rightVNF)
    delay = list[8]
    delaylist.append(delay)

for j in range(len(leftVNFlist)):
    print(leftVNFlist[j], rightVNFlist[j], delaylist[j])
    # print(totalList[j])

class SFC():
    """SFC类"""
    def __init__(self, SFC_id, SFC_request_max_delay, SFC_request_min_reliability, VNF_list):
        #SFC的编号
        self.SFC_id = SFC_id
        #SFC所能接受的最大的时延
        self.SFC_request_max_delay = SFC_request_max_delay
        #SFC所需要的最小的可靠性
        self.SFC_request_min_reliability = SFC_request_min_reliability
        #SFC上所连接的VNF列表，一般这个列表是不会更改的
        self.VNF_list = VNF_list

    #增加VNF到SFC上，用于初始SFC形成阶段
    def add_VNF_to_SFC(self, VNF_id, current_delay, additional_delay):
        self.VNF_list.append(VNF_id)
        current_delay += additional_delay

    #删除SFC上的某个VNF
    def delete_VNF_on_SFC(self, VNF_id, current_delay, deleted_VNF_delay):
        self.VNF_list.remove(VNF_id)
        current_delay -= deleted_VNF_delay

    #SFC可靠性计算方法，VNF_list中存储的是SFC上所有VNF的id。
    def get_SFC_relialibility(self, VNF_list):
        VNFInstance = VNF()
        SFCReliability = 0
        for VNFId in VNF_list:
            SFCReliability *= VNFInstance.getVNFRliability(VNFId)
        return SFCReliability

    #获取SFC的时延,时延为SFC上各个VNF之间的时延的加和。
    def get_SFC_delay(self, VNF_list):
        SFCDelay = 0
        for VNFIdLeft,VNFIdRight in VNF_list:
            delay = self.delayBetweenVNFs(VNFIdLeft,VNFIdRight)
            self.delay_list.append(delay)
        for delay in self.delay_list:
            SFCDelay += delay
        return SFCDelay

    #根据VNF id获取两个VNF之间的时延。
    # 首先要获得VNF所在的VM，再获取VM所在的物理节点，
    # 然后根据拓扑得到两个物理节点之间的时延
    def delayBetweenVNFs(self, VNFIdLeft, VNFRight):
        vmInstance = VM()
        delay = 1000000
        VNFInstanceLeft = VNF(VNFIdLeft)
        VNFInstanceRight = VNF(VNFRight)
        LeftphysicalNodeId = vmInstance.get_physicalNode_id(VNFInstanceLeft.get_VM_id())
        RightphysicalNodeId = vmInstance.get_physicalNode_id(VNFInstanceRight.get_VM_id())
        #由拓扑结构获取到左右两个物理节点之间的时延
        for i in len(leftVNFlist):
            if LeftphysicalNodeId == leftVNFlist[i]:
                if RightphysicalNodeId == rightVNFlist[i]:
                    delay = delaylist[i]
            elif LeftphysicalNodeId == rightVNFlist[i]:
                if RightphysicalNodeId == leftVNFlist[i]:
                    delay = delaylist[i]
        return delay


