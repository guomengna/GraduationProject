import math
import time

from entity.SFC import SFC
from entity.SFCList import sfcListSingleton
from entity.VNF import VNF
from entity.VNFList import VNFList, vnfListSingelton
from migration.VNFMigration import VNFMigration
from monitor.JudgeMigrationTime import JudgeMigrationTime


class SFCReliabilityMonitor():
    """SFC可靠性监测类"""
    print("this is SFCReliabilityMonitor class")
    # 本方法被调用的次数
    callCount = 0

    # 确定初始时间间隔所用到的阈值
    # 流量less阈值
    LESS = 20
    # 流量high阈值
    HIGH = 100
    # 低流量时的初始时间间隔(s)
    LESS_INTERVAL = 6
    # 高流量时的初始时间间隔
    HIGH_INTERVAL = 3

    # 上一次的时间间隔，每次调用该方法之后都要更新此值,此时，本次计算的结果应该是下一次的baseLastTime
    baseLastTime = 100000
    # 上次的流量总数
    lastFlowNeeds = 0
    # 参数设置
    w1 = 0.1
    # 初始时间间隔

    # 流量增减幅度的阈值
    FLOW_ADD_OR_DELETE_Threthold = 0.1
    cunrrentSFCReliabilityList = {}
    # 存储可靠性低于阈值的SFC
    unreliableSFCList = []
    unreliableSFCReliabilityList = []
    count = 0
    starttime = time.perf_counter()
    print("开始时间：%d" % starttime)
    # 可靠性监测方法,按照计算出的当前时间间隔，在当前时钟的基础上加上此时间间隔，计算整个网络中SFC的可靠性
    # 由此，我认为我的时间间隔设置初始值可能太小了，因为计算SFC的可靠性需要一定的时间，此时间应当比时间间隔小很多才好
    def reliability_monitor(self):
        print("可靠性监测方法主体")
        # 如何能间隔不同的时间间隔调用相同的方法？
        # 隔上一个时间间隔就要重新调用SFC_reliability_caculating()方法，计算网络中的SFC可靠性如何实现呢？
        # 定义一个时间间隔变量，用于存储每次算出的时间间隔
        timeIntervalVariable = self.reliability_monitor_timeInterval()
        print("timeIntervalVariable = %d" %timeIntervalVariable)
        # 睡眠时间
        sleepTime = timeIntervalVariable
        print("sleeptime = %d" % sleepTime)
        self.cunrrentSFCReliabilityList = self.SFC_reliability_caculating()
        while(True):
            # # 睡眠时间
            # sleepTime = timeIntervalVariable
            # print("sleeptime = %d" % sleepTime)
            # # 每次都要更新
            # timeIntervalVariable = self.reliability_monitor_timeInterval()
            # self.cunrrentSFCReliabilityList = self.SFC_reliability_caculating()

            # 清空列表
            unreliableSFCList = []
            unreliableSFCReliabilityList = []
            SFCReliabilityMonitorInstance = SFCReliabilityMonitor()
            # 存储全网中所有SFC的可靠性
            """此处是死循环的出现地点，下边的代码不会执行"""
            # SFCReliabilityList = SFCReliabilityMonitorInstance.reliability_monitor() #怀疑这一句是调用错了，调用的应该是下边的方法
            # SFCReliabilityList = SFCReliabilityMonitorInstance.SFC_reliability_caculating()
            # 全网中所有SFC的ID列表
            ALLSFCList = sfcListSingleton.getSFCList()
            # 存储的是网络中SFC的最小可靠性需求值
            SFCReliabilityResqeustList = []
            for i in range(len(ALLSFCList)):
                print("SFC的ID是： %d" %ALLSFCList[i])
                print("sfcListSingleton.dict_minReliability[ALLSFCList[i]] is: %f" %sfcListSingleton.dict_minReliability[ALLSFCList[i]])
                SFCReliabilityResqeustList.append(sfcListSingleton.dict_minReliability[ALLSFCList[i]])
            print("SFCReliabilityResqeustList is :")
            print(SFCReliabilityResqeustList)

            # 判断每条SFC的可靠性是否低于阈值
            for i in range(len(ALLSFCList)):
                SFCInstance = SFC(ALLSFCList[i], sfcListSingleton.dict_maxDelay[ALLSFCList[i]],
                                  sfcListSingleton.dict_minReliability[ALLSFCList[i]],
                                  sfcListSingleton.dict_VNFList[ALLSFCList[i]],
                                  sfcListSingleton.dict_createdtime[ALLSFCList[i]])
                SFCRequestMinReliability = SFCInstance.getRequestMinReliability()
                print(self.cunrrentSFCReliabilityList[ALLSFCList[i]])
                print(SFCReliabilityResqeustList[i])
                if(self.cunrrentSFCReliabilityList[ALLSFCList[i]] < sfcListSingleton.dict_minReliability[ALLSFCList[i]]):#可靠性小于需求值
                    # 将此SFC加入到不满足可靠性要求的SFC列表中
                    unreliableSFCList.append(ALLSFCList[i])
                    unreliableSFCReliabilityList.append(self.cunrrentSFCReliabilityList[ALLSFCList[i]])
                judgeMigrationTimeInstance = JudgeMigrationTime()
                ifNeedMigration = judgeMigrationTimeInstance.ifNeedMigration(unreliableSFCList)
                # 调用JudgeMigrationTime类中的ifNeedMigration方法，判断此时是否需要进行迁移                                                         unreliableSFCReliabilityList)
                if(ifNeedMigration == True):
                    # 判断是迁移一条还是多条SFC,migrationOneOrMore()方法
                    if(judgeMigrationTimeInstance.migrationOneOrMore(unreliableSFCList, unreliableSFCReliabilityList) == True):
                        # 迁移某一条SFC
                        """调用迁移一条SFC的方法，迁移可靠性低于阈值的SFC列表中的第一条SFC，调用方法处"""
                        print("*****************迁移一条SFC*************************")
                        VNFMigration_instance = VNFMigration()
                        VNFMigration_instance.migrateVNFsofOneSFC()

                    else:
                        judgeMigrationTimeInstance = JudgeMigrationTime()
                        neededMigrationSFCList = judgeMigrationTimeInstance.getNeededMigrationSFCList()
                        """调用迁移多条SFC的方法，方法调用处"""
                        print("*****************迁移多条SFC*************************")
                        VNFMigration_instance = VNFMigration()
                        VNFMigration_instance.migrateVNFsofMultiSFCIterator()

            # 睡眠相应的时间间隔之后才再一次去测量
            time.sleep(sleepTime)
            # 睡眠时间
            sleepTime = timeIntervalVariable
            print("sleeptime = %d" % sleepTime)
            # 每次都要更新
            timeIntervalVariable = self.reliability_monitor_timeInterval()
            # 存储的是当前网络中SFC的可靠性
            self.cunrrentSFCReliabilityList = self.SFC_reliability_caculating()
            endtime = time.perf_counter()
            print("结束时间：%d" % endtime)
            self.count += 1
            print("count = %d" % self.count)
            # print("%d" % int(endtime - self.starttime))
            if (int(endtime - self.starttime) >= 30):
                break

    # 全网中所有SFC的可靠性计算方法
    def SFC_reliability_caculating(self):
        # 存储全网中SFC的可靠性
        SFCReliabilityList = []
        # 获取到网络中所有的SFC的列表
        ALLSFCList = sfcListSingleton.getSFCList()
        SFCReliabilityDict = {}
        for i in range(len(ALLSFCList)):
            print("SFC的ID为： %d" %ALLSFCList[i])
            SFCInstance = SFC(ALLSFCList[i],
                              sfcListSingleton.dict_maxDelay[ALLSFCList[i]],
                              sfcListSingleton.dict_minReliability[ALLSFCList[i]],
                              sfcListSingleton.dict_VNFList[ALLSFCList[i]],
                              sfcListSingleton.dict_createdtime[ALLSFCList[i]]
                              )
            SFCreliability = SFCInstance.getSFCReliabilityAtFirst()
            # 字典,存放每个SFC的ID和可靠性
            SFCReliabilityDict[ALLSFCList[i]] = SFCreliability
            # SFCReliabilityDict['SFCID'] = ALLSFCList[i]
            # SFCReliabilityDict['reliability'] = SFCreliability
            # 列表里放的是所有的字典（不知道编译会不会通过）
            # SFCReliabilityList.append(SFCReliabilityDict)
        print(SFCReliabilityDict)
        return SFCReliabilityDict

    # 可靠性测量的时间间隔的确定
    def reliability_monitor_timeInterval(self):
        self.callCount += 1
        # 调用获取此刻网络流量需求的方法（现在的流量需求）
        flowNeeds = self.flow_monitor()
        print("call count = %d" % self.callCount)
        # 用于判断是否是第一次调用本方法，即是否是首次监测SFC可靠性。
        if self.callCount == 1:
            # 首次调用该监测方法，时间间隔设置为初始值，而初始值的确定与流量多少有关
            # 获得此时的初始时间间隔
            baseInterval = self.set_inital_interval(flowNeeds)
            interval = baseInterval
        else:
            # 并非首次调用，即存在上一次的时间间隔
            # interval = self.baseLastTime-self.baseInterval*self.w1 #此处的计算应该使用流量增多或是减少对应的时间间隔
            interval = self.caculate_new_interval(flowNeeds, self.lastFlowNeeds, self.baseLastTime)

        # 更新上一次时间间隔的值，本次计算的结果应该是下一次的baseLastTime
        self.baseLastTime = interval
        # 每次都要更新新的流量需求
        self.lastFlowNeeds = flowNeeds
        print("可靠性测量的时间间隔的确定:%d" % interval)
        return interval

    # 监测此时网络中流量的多少（网络中的流量应该怎么在这里表示呢？？是否可以用网络中所有VNF总共所需要的资源来表示呢）
    def flow_monitor(self):
        # 用当前网络中VNF所需要的资源(CPU)的总量来代表流量
        # VNFListIntance = VNFList()
        # 当前网络中活动的VNF列表,使用单例调用
        current_active_VNF_list = vnfListSingelton.getActiveVNFList()
        dict_VNFListType = vnfListSingelton.get_dict_VNFListType()
        dict_VNFRequestCPU = vnfListSingelton.get_dict_VNFRequestCPU()
        dict_VNFRequestMemory = vnfListSingelton.get_dict_VNFRequestMemory()
        dict_locatedVMID = vnfListSingelton.get_dict_locatedVMID()
        dict_locatedSFCIDList = vnfListSingelton.get_dict_locatedSFCIDList()
        dict_numbersOnSFCList = vnfListSingelton.get_dict_numbersOnSFCList()
        dict_VNFReliability = vnfListSingelton.get_dict_VNFReliability()
        # print(dict_VNFReliability)
        # current_active_VNF_list = VNFListIntance.getActiveVNFList()
        # 总的资源需求值,初始为0
        totalNeededResource = 0
        # 根据活动VNF列表获取列表中每个VNF此刻的资源需求值
        for i in range(len(current_active_VNF_list)):
            # 根据VNF的ID，去文件中获取此VNF的所有数据，用于初始化VNF实例
            VNFID = current_active_VNF_list[i]

            VNFType = dict_VNFListType[VNFID]
            print("VNF Type = %d" % VNFType)
            VNFRequestCPU = dict_VNFRequestCPU[VNFID]
            print("VNF需要的CPU资源是：%d" % VNFRequestCPU)
            VNFRequestMemory = dict_VNFRequestMemory[VNFID]
            print("VNF所需要的内存资源：%d" % VNFRequestMemory)
            locatedVMID = dict_locatedVMID[VNFID]
            print("VNF所在的VM的ID：%d" % locatedVMID)
            locatedSFCIDList = dict_locatedSFCIDList[VNFID]
            print("VNF所处的SFC的ID列表： %d" % locatedSFCIDList)
            numbersOnSFCList = dict_numbersOnSFCList[VNFID]
            print("VNF在所处的SFC上的序号列表： %d" % numbersOnSFCList)
            VNFReliability = dict_VNFReliability[VNFID]
            print("VNF的可靠性：%d" % VNFReliability)
            currentVNF = VNF(current_active_VNF_list[i], VNFType,
                             VNFRequestCPU, VNFRequestMemory, locatedVMID,
                             locatedSFCIDList, numbersOnSFCList,
                             VNFReliability)
            totalNeededResource += currentVNF.VNF_request_CPU
        # 返回所需的资源（CPU）总量
        return totalNeededResource

    # 根据网络中流量的多少来确定初始时间间隔baseInterval
    def set_inital_interval(self, flowNeeds):
        print("流量需求为：%d" %flowNeeds)
        baseTimeInterval = 0
        # 设定2个流量阈值
        # 1.less值，即流量小于等于此值时，将初始时间间隔设置为lessInterval
        lessThrethold = self.LESS
        # 2.high值，即流量大于此值时，将初始时间间隔设置为highInterval
        highThrethold = self.HIGH
        print("lessThrethold = %d" % lessThrethold)
        print("highThrethold = %d" % highThrethold)
        if(flowNeeds <= lessThrethold):
            baseTimeInterval = self.LESS_INTERVAL
        elif(flowNeeds > highThrethold):
            baseTimeInterval = self.HIGH_INTERVAL
        # 返回由流量确定的初始时间间隔
        return baseTimeInterval

    # 判断流量增多还是减少，分别使用增多和减少时的公式来计算新的时间间隔
    # 输入参数为：当前的流量需求，上一次的流量需求，上一次的时间间隔
    def caculate_new_interval(self, currentFlowNeeds, lastFlowNeeds, lastTimeInterval):
        print("上次流量需求：%d" %lastFlowNeeds)
        print("本次流量需求：%d" % currentFlowNeeds)
        # 暂时设置的阈值
        a1 = 2
        a2 = 3
        b1 = 2
        b2 = 3
        # 初始化返回值
        newTimeInterval = 0
        if(currentFlowNeeds > lastFlowNeeds):
            # 若是流量增多
            # w1为流量的增幅
            w1 = (currentFlowNeeds - lastFlowNeeds)/lastFlowNeeds
            if(((w1-1)>0 and (w1-1)<self.FLOW_ADD_OR_DELETE_Threthold)
            or ((1-w1)>0 and (1-w1)<self.FLOW_ADD_OR_DELETE_Threthold)):
                # abs()方法为取绝对值,floor()为向下取整
                newTimeInterval = max(a1, math.floor(abs(lastFlowNeeds - lastFlowNeeds*w1)))
            elif((w1-1)>self.FLOW_ADD_OR_DELETE_Threthold):
                newTimeInterval = a2
            elif(w1<1-self.FLOW_ADD_OR_DELETE_Threthold):
                newTimeInterval = math.floor(lastFlowNeeds - lastFlowNeeds * w1)
        elif(currentFlowNeeds < lastFlowNeeds):
            # 若是流量减少
            # w2为流量的减幅
            w2 = (lastFlowNeeds - currentFlowNeeds)/lastFlowNeeds
            if(abs(w2-1)>0 and abs(w2-1)<self.FLOW_ADD_OR_DELETE_Threthold):
                newTimeInterval = min(b1 ,math.floor(lastFlowNeeds + lastFlowNeeds * w2))
            elif((w2-1)>self.FLOW_ADD_OR_DELETE_Threthold):
                newTimeInterval = b2
            elif(w2<(1-self.FLOW_ADD_OR_DELETE_Threthold)):
                newTimeInterval = math.floor(lastFlowNeeds + lastFlowNeeds * w2)
        else:
            # 若是前后两个时刻的流量需求相同，则不需要修改时间间隔
            newTimeInterval = lastTimeInterval
        return newTimeInterval
