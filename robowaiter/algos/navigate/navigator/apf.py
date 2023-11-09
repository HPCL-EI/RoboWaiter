import numpy as np
import copy
import matplotlib
matplotlib.use('TkAgg') # 防止画图卡死

## 初始化车的参数


# P0 = np.array([0, - d / 2, 1, 1]) #车辆起点位置，分别代表x,y,vx,vy
#
# Pg = np.array([99, d / 2, 0, 0]) # 目标位置
#
# # 障碍物位置
# Pobs = np.array([
#     [15, 7 / 4, 0, 0],
#     [30, - 3 / 2, 0, 0],
#     [45, 3 / 2, 0, 0],
#     [60, - 3 / 4, 0, 0],
#     [80, 3/2, 0, 0]])



def APF(Pi, Pg, Pobs=None, step_length=100):
    '''
        Args:
            Pi:             robot位置 (x,y)
            Pg:             目标位置 (x,y)
            Pobs:           障碍物位置 [(x,y), ...]
            step_length:    单次移动步长 int
        returns:
            next_step:      robot下一步位置
            UnitVec_Fsum:   合力方向向量
    '''

    # 目标检测
    if np.linalg.norm(Pi-Pg) < step_length:  # 目标检测
        return Pg, (Pg-Pi) / np.linalg.norm(Pg-Pi)

    Eta_att = 5  # 引力的增益系数
    Eta_rep_ob = 15  # 斥力的增益系数
    d0 = 200  # 障碍影响的最大距离
    n = 1  # {P_g}^n 为到目标点的距离，n为可选的正常数 (解决目标不可达问题)

    ## 计算引力
    delta_g = Pg - Pi                   # 目标方向向量(指向目标)
    dist_g = np.linalg.norm(delta_g)    # 目标距离
    UniteVec_g = delta_g / dist_g       # 目标单位向量

    F_att = Eta_att * dist_g * UniteVec_g  # F_att = Eta_att * dist(pi,pg) * unite_vec(pi,pg)
    F_sum = F_att

    ## 计算斥力
    if Pobs:
        delta = np.zeros((len(Pobs), 2))
        unite_vec = np.zeros((len(Pobs), 2))
        dists = []
        # 计算车辆当前位置与所有障碍物的单位方向向量
        for j in range(len(Pobs)):
            delta[j] = Pi - Pobs[j]  # 斥力向量
            dists.append(np.linalg.norm(delta[j]))  # 障碍物距离
            unite_vec[j] = delta[j] / dists[j]  # 斥力单位向量
        # 每一个障碍物对车辆的斥力,带方向
        F_rep_ob = np.zeros((len(Pobs), 2))
        # 在原斥力势场函数增加目标调节因子（即车辆至目标距离），以使车辆到达目标点后斥力也为0
        for j in range(len(Pobs)):
            if dists[j] >= d0:
                F_rep_ob[j] = np.array([0, 0])  # 距离超过阈值则斥力为0
            else:
                # 障碍物的斥力1，方向由障碍物指向车辆
                F_rep_ob1_abs = Eta_rep_ob * (1 / dists[j] - 1 / d0) * dist_g ** n / dists[j] ** 2  # 斥力大小
                F_rep_ob1 = F_rep_ob1_abs * unite_vec[j]  # 斥力向量
                # 障碍物的斥力2，方向由车辆指向目标点
                F_rep_ob2_abs = n / 2 * Eta_rep_ob * (1 / dists[j] - 1 / d0) ** 2 * dist_g ** (n - 1)  # 斥力大小
                F_rep_ob2 = F_rep_ob2_abs * UniteVec_g  # 斥力向量
                # 改进后的障碍物合斥力计算
                F_rep_ob[j] = F_rep_ob1 + F_rep_ob2

        F_rep = np.sum(F_rep_ob, axis=0)  # 斥力合力
        F_sum += F_rep  # 总合力

    ## 合力方向
    UnitVec_Fsum = F_sum / np.linalg.norm(F_sum)  # 合力方向向量: F / |F|

    # 计算车的下一步位置
    next_step = copy.deepcopy(Pi + step_length * UnitVec_Fsum)  # 沿合力方向前进单位距离
    # print(next_step)

    return next_step, UnitVec_Fsum



