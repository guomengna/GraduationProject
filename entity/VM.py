from entity import PhysicalNode


class VM():
    """虚拟机类，一个虚拟机上只有一个VNF"""
    def __init__(self, VM_id, VM_request_CPU, VM_request_Memory, physicalNode_id, VM_reliability):
        # VM的编号
        self.VM_id = VM_id
        # VM所需要的CPU资源的数量
        self.VM_request_CPU = VM_request_CPU
        # VM所需要的内存资源的数量
        self.VM_request_Memory = VM_request_Memory
        # VM所处的物理节点的编号
        self.physicalNode_id = physicalNode_id
        # VM的可靠性，等预期所在的物理节点的可靠性
        self.VM_reliability = VM_reliability

    # 根据VM id获取物理节点的id
    def get_physicalNode_id(self, VMId):
        if(VMId == self.VM_id):
            return self.physicalNode_id

    # 根据ID获取VM的可靠性
    def getVMReliability(self, VMId):
        if(VMId == self.VM_id):
            physicalNode = PhysicalNode()
            return physicalNode.get_reliability(self.physicalNode_id)

    def setPhysicalNodeId(self, physicalNodeId):
        self.physicalNode_id = physicalNodeId
