class VM():
    def __init__(self, VM_id, VM_request_CPU, VM_request_Memory, physicalNode_id, VM_reliability):
        #VM的编号
        self.VM_id = VM_id
        #VM所需要的CPU资源的数量
        self.VM_request_CPU = VM_request_CPU
        #VM所需要的内存资源的数量
        self.VM_request_Memory = VM_request_Memory
        #VM所处的物理节点的编号
        self.physicalNode_id = physicalNode_id
        #VM的可靠性
        self.VM_reliability = VM_reliability

