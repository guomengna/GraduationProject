class SFC():
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

    #SFC初始形成方法


    #SFC可靠性计算方法


    #SFC可靠性监测模块（还没有考虑好是不是在这个文件中实现，既然是整体上的方法，是不是应该在另一个全局文件中实现呢？？）