from entity import VM, PhysicalNode
import random

class VNF():
    """VNF类"""
    def __init__(self, VNF_id, VNF_type, VNF_request_CPU, VNF_request_Memory, VM_id, SFC_id_list, number_on_SFC,
                 VNF_reliability):
        # VNF编号
        self.VNF_id = VNF_id
        # VNF类型
        self.VNF_type = VNF_type
        # VNF所需求的CPU资源总数
        self.VNF_request_CPU = VNF_request_CPU
        # VNF所需要的内存资源总数
        self.VNF_request_Memory = VNF_request_Memory
        # VNF所处的VM的编号
        self.VM_id = VM_id
        # VNF所处的所有SFC的编号
        self.SFC_id_list = SFC_id_list
        # VNF在SFC上所处的位置的编号（是此SFC上的第几个VNF）
        self.number_on_SFC = number_on_SFC
        # VNF的可靠性，等于其所在的物理节点的可靠性
        self.VNF_reliability = VNF_reliability
        # 每个VNF都有自己一个随机生成的迁移花费时间系数
        self.migration_time_coefficient = random.uniform(0.6, 0.9)

    # 根据VNF id获取VM id
    def get_VM_id(self, VNFId):
        if VNFId == self.VNF_id:
            return self.VM_id

    # 根据VNF id获取VNF的可靠性
    def getVNFRliability(self, VNFId):
        if VNFId == self.VNF_id:
            vm = VM()
            return vm.getVMReliability(self.VM_id)

    # 根据VNF_id获取VNF的类型
    def getVNFType(self, VNFId):
        if VNFId == self.VNF_id:
            return self.VNF_type

    def setVNFRequestCPU(self, VNF_request_CPU):
        self.VNF_request_CPU = VNF_request_CPU

    def setVNF_request_Memory(self, VNF_request_Memory):
        self.VNF_request_Memory = VNF_request_Memory

    def getVNF_request_CPU(self):
        return self.VNF_request_CPU

    def getVNF_request_Memory(self):
        return self.VNF_request_Memory

    # 获取当前VNF可以使用的CPU资源数
    def getAvailibleCPU(self, VNFId):
        # 根据VNF所在的物理节点上剩余的CPU来计算（VNF在启用之前已经位于物理机上了，但是并不处于运行状态，所以资源占用为0）
        vmId = self.get_VM_id(VNFId)
        vmInstance = VM()
        physicalNodeId = vmInstance.get_physicalNode_id(vmId)
        physicalNodeInstance = PhysicalNode()
        return physicalNodeInstance.getAvailable_CPU(physicalNodeId)

    # 获取当前VNF可以使用的内存资源数
    def getAvailibleCPU(self, VNFId):
        vmId = self.get_VM_id(VNFId)
        vmInstance = VM()
        physicalNodeId = vmInstance.get_physicalNode_id(vmId)
        physicalNodeInstance = PhysicalNode()
        return physicalNodeInstance.getAvailable_Memory(physicalNodeId)

    def getMigration_time_coefficient(self):
        return self.migration_time_coefficient

