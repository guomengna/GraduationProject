import time
import math
import threading

from threading import Timer

from entity.PhysicalNodeList import nodeListSingelton


class PhysicalNode():
    """物理节点类"""
    # 其上所承载的VM列表
    VM_list = []
    #设置阈值
    #CPU利用率
    UCPU = 0.8
    #内存利用率
    UMEMORY = 0.7
    #测量的时间间隔
    time_interval = 2
    #过载时间段的阈值
    OP = 5
    #负载能力
    loadCapacity = 0.6
    #过载程度与过载时间对节点可靠性下降程度影响参数
    overloadDegree_contribution = 0.5
    overloadPriod_contribution = 0.5

    #初始化方法
    def __init__(self, physicalNode_id, capacity_CPU, capacity_Memory, provided_reliablity):
        # 物理节点的编号，在拓扑中，编号即代表位置
        self.physicalNode_id = physicalNode_id
        # 可提供的CPU资源的总数
        self.capacity_CPU = capacity_CPU
        # 可提供的内存资源的总数
        self.capacity_Memory = capacity_Memory
        # 物理节点所能提供的可靠性
        self.provided_reliablity = provided_reliablity
        # 物理节点上的可用CPU资源数
        self.available_CPU = capacity_CPU
        # 物理节点上可用内存资源数
        self.available_Memory = capacity_Memory
        #当前占用的CPU资源总数
        self.occupied_CPU = 0
        #当前占用的内存资源总数
        self.occupied_Memoty = 0

        #物理节点过载持续时间段
        self.overloadPeriod = 0
        # 物理节点的过载状态
        self.overloadeState = False
        # 物理节点的过载程度
        self.overloadeDegree = 0

    #物理节点增加VM方法
    def add_VM_to_physicalNode(self, VM_id, VM_request_CPU, VM_request_Memory):
        #物理节点上的VM列表中加入新来的VM
        self.VM_list.append(VM_id)
        #物理节点上的可用资源减去新加入VM所占用的资源
        self.available_CPU -= VM_request_CPU
        self.available_Memory -= VM_request_Memory

    #物理节点删除VM方法
    def delete_VM_on_physicalNode(self, VM_id, VM_request_CPU, VM_request_Memory):
        #物理节点上的VM列表中删除此VM
        self.VM_list.romove(VM_id)
        #物理节点上的可用资源加上此删除VM所占用的资源
        self.available_CPU -= VM_request_CPU
        self.available_Memory -= VM_request_Memory

    #计算物理节点上VM当前占用的资源
    def occupied_resources(self):
        self.occupied_CPU = self.capacity_CPU - self.available_CPU
        self.occupied_Memory = self.capacity_Memory - self.available_Memory
        return self.occupied_CPU, self.occupied_Memory

    #计算物理节点资源利用率方法
    def occupancy_rate_resource(self):
        self.occupied_resources()
        self.occupancy_rate_CPU = self.occupied_CPU/self.capacity_CPU
        self.occupancy_rate_Memory = self.occupied_Memory / self.capacity_Memory
        return self.occupancy_rate_CPU, self.occupancy_rate_Memory

    # 判断物理节点CPU和内存的利用率是否超过阈值，返回CPU与内存过载状态的布尔值
    def if_overload(self):
        self.occupancy_rate_resource()
        CPUOverloadState = False
        MemoryOverloadState = False
        # CPU利用率是否超阈值
        if self.occupancy_rate_CPU >= self.UCPU:
            print ("节点CPU利用率超过阈值")
            CPUOverloadState = True
        elif self.occupancy_rate_CPU < self.UCPU:
            CPUOverloadState = False
        # 内存利用率是否超阈值
        if self.occupancy_rate_Memory >= self.UMEMORY:
            print("节点内存利用率超过阈值")
            MemoryOverloadState = True
        elif self.occupancy_rate_Memory < self.UMEMORY:
            MemoryOverloadState = False
        resourceState = CPUOverloadState and MemoryOverloadState
        return resourceState

    # 物理节点是否进入了过载状态,返回过载程度与过载时间
    def if_overloadState(self):
        print("判断物理节点是否过载方法本体")
        # t = Timer(self.time_interval, self.if_overload)
        # t = Timer(self.time_interval, self.if_overloadState)
        # t.start()
        resourceOverload = self.if_overload()
        print("resourceOverload = ")
        print(resourceOverload)
        if(resourceOverload == True):
            self.overloadPeriod += self.time_interval
        else:
            self.overloadPeriod = 0
        if self.overloadPeriod >= self.OP:
            self.overloadState = True
            overloadeDegree1 = (self.occupancy_rate_CPU - self.UCPU) / self.UCPU
            overloadeDegree2 = (self.occupancy_rate_Memory - self.UMEMORY) / self.UMEMORY
            self.overloadeDegree = (overloadeDegree1 + overloadeDegree2) / 2
            #停止Timer
            # t.cancel()
        else:
            self.overloadState = False
            self.overloadPeriod = 0
            self.overloadeDegree = 0
        # 返回过载状态，过载时长和过载程度
        return self.overloadState, self.overloadPeriod, self.overloadeDegree

        # while True:
        #     if(resourceOverload == True):
        #         self.overloadPeriod += self.time_interval
        #     else:
        #         self.overloadPeriod = 0
        #     if self.overloadPeriod >= self.OP:
        #         self.overloadState = True
        #         overloadeDegree1 = (self.occupancy_rate_CPU - self.UCPU) / self.UCPU
        #         overloadeDegree2 = (self.occupancy_rate_Memory - self.UMEMORY) / self.UMEMORY
        #         self.overloadeDegree = (overloadeDegree1 + overloadeDegree2) / 2
        #         #停止Timer
        #         t.cancel()
        #     else:
        #         self.overloadState = False
        #         # 15秒后停止定时器
        #         time.sleep(15)
        #         t.cancel()



    #获取物理节点可靠性方法，返回可靠性
    def get_reliability(self, NodeId):
        print("获取物理节点可靠性的方法本体")
        reliability = 0
        if NodeId == self.physicalNode_id:
            print("NodeId = %d" %NodeId)
            print("nodeListSingelton.dict_provided_reliablity[NodeId] = ")
            print(nodeListSingelton.dict_provided_reliablity[NodeId])
            (overloadeState, overloadPeriod, overloadDegree) = self.if_overloadState()
            print("这是物理节点类159行，overloadeState = ")
            print(overloadeState)
            #若物理节点不过载，则直接返回它可提供的可靠性
            if overloadeState == False:
                reliability = self.provided_reliablity
                print("不过载，物理节点的可靠性为：")
                print(reliability)
            #若物理节点过载，则根据过载程度和过载时间段计算过载后物理节点的可靠性
            elif overloadeState == True:
                reliability = self.overloadDegree_contribution * self.overloadeDegree \
                              + self.overloadPriod_contribution * self.overloadPeriod
            return reliability

    #根据物理节点的ID获取此节点上当前可用CPU
    def getAvailable_CPU(self, physicalNodeId):
        if(physicalNodeId == self.physicalNode_id):
            return self.available_CPU

    # 根据物理节点的ID获取此节点上当前可用内存
    def getAvailable_Memory(self, physicalNodeId):
        if (physicalNodeId == self.physicalNode_id):
            return self.available_Memory

    # CPU资源更新(增加)
    def addAvailable_CPU(self, physicalNodeId, cpu_resource):
        if(physicalNodeId == self.physicalNode_id):
            self.available_CPU += cpu_resource

    # memory资源更新(增加)
    def addAvailable_Memory(self, physicalNodeId, memory_resource):
        if(physicalNodeId == self.physicalNode_id):
            self.available_Memory += memory_resource

    # CPU资源更新（删除）
    def deleteAvailable_CPU(self, physicalNodeId, cpu_resource):
        if (physicalNodeId == self.physicalNode_id):
            self.available_CPU -= cpu_resource

    # memory资源更新（删除）
    def deleteAvailable_Memory(self, physicalNodeId, memory_resource):
        if (physicalNodeId == self.physicalNode_id):
            self.available_Memory -= memory_resource

    # 返回物理节点的VM列表
    def getVMList(self):
        return self.VM_list