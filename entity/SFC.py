# -*- coding: utf-8 -*-
import random

import xlrd
from numpy.core.tests.test_mem_overlap import xrange

from entity.VM import VM
from entity.VMList import vmListSingelton
from entity.VNF import VNF
from entity.VNFList import vnfListSingelton

excelFile = xlrd.open_workbook('D:/pycharm workspace'
                               '/GraduationProject/topo/'
                               'cernet2_added.xlsx', 'r')
nums = len(excelFile.sheets())
leftPhysicalNodelist = []
rightPhysicalNodelist = []
delaylist = []

for i in range(nums):
    # 根据sheet顺序打开sheet
    sheet1 = excelFile.sheets()[i]
nrows = sheet1.nrows  # 行
ncols = sheet1.ncols  # 列
# 循环行列表数据
for i in range(nrows):
    list = sheet1.row_values(i)
    # print(int(list[0]),int(list[1]),list[8])
    # 此处的list[0]其实应该是源物理节点，list[1]应该是目的物理节点
    leftPhysicalNode = int(list[0])
    leftPhysicalNodelist.append(leftPhysicalNode)
    rightPhysicalNode = int(list[1])
    rightPhysicalNodelist.append(rightPhysicalNode)
    delay = list[8]
    delaylist.append(delay)
print("this is the SFC.class")
for j in range(len(leftPhysicalNodelist)):
    print(leftPhysicalNodelist[j], rightPhysicalNodelist[j], delaylist[j])
    # print(totalList[j])

class SFC():
    """SFC类"""
    currentDelay = 0
    delay_list = []
    # 此方法应该在SFC的初次形成模块调用，但是现在还没有被调用过
    def __init__(self, SFC_id, SFC_request_max_delay, SFC_request_min_reliability, VNF_list, create_time):
        # SFC的编号
        self.SFC_id = SFC_id
        # SFC所能接受的最大的时延
        self.SFC_request_max_delay = SFC_request_max_delay
        # SFC所需要的最小的可靠性
        self.SFC_request_min_reliability = SFC_request_min_reliability
        # SFC上所连接的VNF列表，一般这个列表是不会更改的
        self.VNF_list = VNF_list
        # SFC的重要程度
        self.importance = random.uniform(0.4, 0.9)
        # SFC的建立时间
        self.create_time = create_time

    def getRequestMinReliability(self):
        return self.SFC_request_min_reliability

    # 获取此SFC需要的所有资源的加和
    def getSFCRequestedResource(self):
        requestedCPU = 0
        requestedMemory = 0
        VNF_list = self.getVNFList()
        for vnfInstanceId in VNF_list:
            vnfInstance = VNF(vnfInstanceId,
                              vnfListSingelton.dict_VNFListType[vnfInstanceId],
                              vnfListSingelton.dict_VNFRequestCPU[vnfInstanceId],
                              vnfListSingelton.dict_VNFRequestMemory[vnfInstanceId],
                              vnfListSingelton.dict_locatedVMID[vnfInstanceId],
                              vnfListSingelton.dict_locatedSFCIDList[vnfInstanceId],
                              vnfListSingelton.dict_numbersOnSFCList[vnfInstanceId],
                              vnfListSingelton.dict_VNFReliability[vnfInstanceId]
                              )
            requestedCPU += vnfInstance.getVNF_request_CPU()
            requestedMemory += vnfInstance.getVNF_request_Memory()
        return requestedCPU + requestedMemory

    # 获取刚开始建立SFC时此SFC的可靠性
    def getSFCReliabilityAtFirst(self):
        #最开始部署的时候的SFC可靠性
        staticSFCReliability = self.get_SFC_relialibility(self.VNF_list)
        return staticSFCReliability

    # 获取SFC的ID
    def getSFCId(self):
        return self.SFC_id
    # 设置SFC的时延
    def setDelay(self, delay):
        self.currentDelay = delay
    # 获取SFC的时延
    def getDelay(self):
        return self.currentDelay

    def setVNFList(self, VNFList):
        self.VNF_list = VNFList
    # 获取SFC上的VNF列表
    def getVNFList(self):
        return self.VNF_list

    # 增加VNF到SFC上，用于初始SFC形成阶段
    def add_VNF_to_SFC(self, VNF_id, current_delay, additional_delay):
        self.VNF_list.append(VNF_id)
        current_delay += additional_delay

    # 删除SFC上的某个VNF
    def delete_VNF_on_SFC(self, VNF_id, current_delay, deleted_VNF_delay):
        self.VNF_list.remove(VNF_id)
        current_delay -= deleted_VNF_delay

    # SFC可靠性计算方法，VNF_list中存储的是SFC上所有VNF的id。
    def get_SFC_relialibility(self, VNF_list):
        SFCReliability = 1
        for i in range(len(VNF_list)):
            vnfid = VNF_list[i]
            VNFInstance = VNF(vnfid,
                              vnfListSingelton.dict_VNFListType[vnfid],
                              vnfListSingelton.dict_VNFRequestCPU[vnfid],
                              vnfListSingelton.dict_VNFRequestMemory[vnfid],
                              vnfListSingelton.dict_locatedVMID[vnfid],
                              vnfListSingelton.dict_locatedSFCIDList[vnfid],
                              vnfListSingelton.dict_numbersOnSFCList[vnfid],
                              vnfListSingelton.dict_VNFReliability[vnfid])
            print("VNF的可靠性为： %f" %VNFInstance.getVNFRliability(vnfid))
            SFCReliability *= VNFInstance.getVNFRliability(vnfid)
        print("SFC的新的可靠性为：%f" % SFCReliability)
        return SFCReliability

    # 获取SFC的时延,时延为SFC上各个VNF之间的时延的加和。
    def get_SFC_delay(self, VNF_list):
        SFCDelay = 0
        index = 0
        for index in range(len(VNF_list) - 1):
            VNFIdLeft = VNF_list[index]
            VNFIdRight = VNF_list[index+1]
            delay = self.delayBetweenVNFs(VNFIdLeft, VNFIdRight)
            self.delay_list.append(delay)
        for i in range(len(self.delay_list)):
            SFCDelay += self.delay_list[i]
        return SFCDelay

    # 根据VNF id获取两个VNF之间的时延。
    # 首先要获得VNF所在的VM，再获取VM所在的物理节点，
    # 然后根据拓扑得到两个物理节点之间的时延
    def delayBetweenVNFs(self, VNFIdLeft, VNFRight):

        delay = 1000000
        VNFInstanceLeft = VNF(VNFIdLeft,
                              vnfListSingelton.dict_VNFListType[VNFIdLeft],
                              vnfListSingelton.dict_VNFRequestCPU[VNFIdLeft],
                              vnfListSingelton.dict_VNFRequestMemory[VNFIdLeft],
                              vnfListSingelton.dict_locatedVMID[VNFIdLeft],
                              vnfListSingelton.dict_locatedSFCIDList[VNFIdLeft],
                              vnfListSingelton.dict_numbersOnSFCList[VNFIdLeft],
                              vnfListSingelton.dict_VNFReliability[VNFIdLeft]
                              )
        VNFInstanceRight = VNF(VNFRight,
                               vnfListSingelton.dict_VNFListType[VNFRight],
                               vnfListSingelton.dict_VNFRequestCPU[VNFRight],
                               vnfListSingelton.dict_VNFRequestMemory[VNFRight],
                               vnfListSingelton.dict_locatedVMID[VNFRight],
                               vnfListSingelton.dict_locatedSFCIDList[VNFRight],
                               vnfListSingelton.dict_numbersOnSFCList[VNFRight],
                               vnfListSingelton.dict_VNFReliability[VNFRight]
                               )
        vmIdleft = VNFInstanceLeft.get_VM_id(VNFIdLeft)
        vmIdRight = VNFInstanceRight.get_VM_id(VNFRight)
        vmInstanceleft = VM(vmIdleft, vmListSingelton.dict_VMRequestCPU[vmIdleft],
                            vmListSingelton.dict_VMRequestMemory[vmIdleft],
                            vmListSingelton.dict_VMLocatedPhysicalnode[vmIdleft],
                            vmListSingelton.dict_VMReliability[vmIdleft])
        vmInstanceright = VM(vmIdRight, vmListSingelton.dict_VMRequestCPU[vmIdRight],
                            vmListSingelton.dict_VMRequestMemory[vmIdRight],
                            vmListSingelton.dict_VMLocatedPhysicalnode[vmIdRight],
                            vmListSingelton.dict_VMReliability[vmIdRight])
        LeftphysicalNodeId = vmInstanceleft.get_physicalNode_id(vmIdleft)
        RightphysicalNodeId = vmInstanceright.get_physicalNode_id(vmIdRight)
        # 由拓扑结构获取到左右两个物理节点之间的时延
        for i in range(len(leftPhysicalNodelist)):
            if LeftphysicalNodeId == leftPhysicalNodelist[i]:
                if RightphysicalNodeId == rightPhysicalNodelist[i]:
                    delay = delaylist[i]
            elif LeftphysicalNodeId == rightPhysicalNodelist[i]:
                if RightphysicalNodeId == leftPhysicalNodelist[i]:
                    delay = delaylist[i]
        return delay

    def getLeftPhysicalNodelist(self):
        return leftPhysicalNodelist

    def getRightPhysicalNodelist(self):
        return rightPhysicalNodelist

    def getDelayBetweenPhysicalNode(self, leftNodeId, rightNodeId):
        delay = 1000000
        # 由拓扑结构获取到左右两个物理节点之间的时延
        for i in range(len(leftPhysicalNodelist)):
            if leftNodeId == leftPhysicalNodelist[i]:
                if rightNodeId == rightPhysicalNodelist[i]:
                    delay = delaylist[i]
            elif leftNodeId == rightPhysicalNodelist[i]:
                if rightNodeId == leftPhysicalNodelist[i]:
                    delay = delaylist[i]
        return delay