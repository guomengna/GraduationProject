from entity.VNF import VNF


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

    #SFC初始形成方法(是不是应该放在全局文件中比较好？)
    def SFC_initial_formed(self):
        return None

    #SFC可靠性计算方法，VNF_list中存储的是SFC上所有VNF的id。
    def get_SFC_relialibility(self, VNF_list):
        VNFInstance = VNF()
        SFCReliability = 0
        for VNFId in VNF_list:
            SFCReliability *= VNFInstance.getVNFRliability(VNFId)
        return SFCReliability
