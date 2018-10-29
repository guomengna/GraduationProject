from entity import VM


class VNF():
    """VNF类"""
    def __init__(self, VNF_id, VNF_request_CPU, VNF_request_Memory, VM_id, SFC_id, number_on_SFC, VNF_reliability):
        #VNF编号
        self.VNF_id = VNF_id
        #VNF所需求的CPU资源总数
        self.VNF_request_CPU = VNF_request_CPU
        #VNF所需要的内存资源总数
        self.VNF_request_Memory = VNF_request_Memory
        #VNF所处的VM的编号
        self.VM_id = VM_id
        #VNF所处的SFC的编号
        self.SFC_id = SFC_id
        #VNF在SFC上所处的位置的编号（是此SFC上的第几个VNF）
        self.number_on_SFC = number_on_SFC
        #VNF的可靠性，等于其所在的物理节点的可靠性
        self.VNF_reliability = VNF_reliability

    #根据VNF id获取VNF的可靠性
    def getVNFRliability(self, VNFId):
        if VNFId == self.VNF_id:
            vm = VM()
            return vm.getVMReliability(self.VM_id)

    #VNF迁移方法
