class SFCReliabilityMonitor():
    """SFC可靠性监测类"""
    #本方法呗调用的次数
    callCount = 0
    # 上一次的时间间隔，每次调用该方法之后都要更新此值,此时，本次计算的结果应该是下一次的baseLastTime
    baseLastTime = 100000
    #参数设置
    w1 = 0.1
    #初始时间间隔
    baseInterval = 3 #此处原本应该调用的是根据流量确定初始时间间隔方法
    #可靠性监测方法
    def reliability_monitor(self):
        self.callCount += 1
        #用于判断是否是第一次调用本方法，即是否是首次监测SFC可靠性。
        if self.callCount == 1:
            #首次调用该监测方法，时间间隔设置为初始值，而初始值的确定与流量多少有关
            interval = self.baseInterval
        else:
            #并非首次调用，即存在上一次的时间间隔
            interval = self.baseLastTime-self.baseInterval*self.w1 #此处的计算应该使用流量增多或是减少对应的时间间隔

        #更新上一次时间间隔的值，本次计算的结果应该是下一次的baseLastTime
        self.baseLastTime = self.baseInterval

    #监测此时网络中流量的多少（网络中的流量应该怎么在这里表示呢？？是否可以用网络中VNF们总共所需要的资源来表示呢）
    def flow_monitor(self):
        return 0

    #根据网络中流量的多少来确定初始时间间隔baseInterval
    def set_inital_interval(self):
        return 0

    #判断流量增多还是减少，分别使用增多和减少时的公式来计算新的时间间隔
    def caculate_new_interval(self):
        return 0



