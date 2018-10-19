class PhysicalNode():
    """物理节点类"""
    #其上所承载的VM列表
    VM_list = []
    #初始化方法
    def __init__(self, physicalNode_id, capacity_CPU, capacity_Memory, provided_reliablity):
        # 物理节点的编号，在拓扑中，编号即代表位置
        self.physicalNode_id = physicalNode_id
        # 可提供的CPU资源的总数
        self.capacity_CPU = capacity_CPU
        # 可提供的内存资源的总数
        self.capacity_Memory = capacity_Memory
        # 物理节点上的可用CPU资源数
        self.available_CPU = capacity_CPU
        # 物理节点上可用内存资源数
        self.available_Memory = capacity_Memory
        #当前占用的CPU资源总数
        self.occupied_CPU = 0
        #当前占用的内存资源总数
        self.occupied_Memoty = 0
        #物理节点所能提供的可靠性
        self.provided_reliablity = provided_reliablity

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
        self.occupied_CPU = self.capacity_CPU - self.available_CPU
        self.occupied_Memory = self.capacity_Memory - self.available_Memory
        self.occupancy_rate_CPU = self.occupied_CPU/self.capacity_CPU
        self.occupancy_rate_Memory = self.occupied_Memory / self.capacity_Memory
        return self.occupancy_rate_CPU, self.occupancy_rate_Memory