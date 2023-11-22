"""
视觉语言操作
机器人根据指令人的指令调节空调，自主探索环境导航到目标点，通过手臂的运动规划能力操作空调，比如开关按钮、调温按钮、显示面板
"""

import time
from robowaiter.scene.scene import Scene

class SceneVLM(Scene):
    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件， (事件发生的时间，事件函数)
        self.signal_event_list = [
            (3, self.add_walker,  (0,0,700)),
            (1, self.control_walker, (6, False,100, 60, 520,0)), #[walkerID,autowalk,speed,X,Y,Yaw]
            (3, self.customer_say, (6, "好热呀，想开空调，想要温度调低点！")),
            (5, self.control_walker, (6, False, 200, 60, 80, 0)),
            (-1, self.customer_say, (6, "谢谢！这下凉快了！")),  #(-100,600)

            # 有人提出要开空调和关窗帘
            # bar (60, 520)
            # (28, self.add_walker, (0, 0, 0)),
            # (33, self.control_walker, (7, False, 100, 60, 520, 180)),
            # (35, self.customer_say, (7,"好热呀！太阳也好大！")),
            # (45, self.control_walkers_and_say, ([[[7, False, 100, 270, -240, -65, "谢谢，这下凉快了！"]]])),

            # (3, self.add_walker, (0, 0, 0)),
            # (1, self.control_walker, (5, False, 100, 60, 520, 180)),
            # (1, self.customer_say, (5,"好热呀！太阳也好大！")),
            # (-1, self.control_walkers_and_say, ([[[5, False, 100, 270, -240, -65, "谢谢，这下凉快了！"]]])),
        ]

    def _reset(self):
        self.gen_obj()
        # self.state["condition_set"] = {'At(Robot,Bar)', 'Is(AC,Off)',
        #  'Holding(Nothing)','Exist(Yogurt)','Exist(Softdrink)','On(Yogurt,Bar)','On(Softdrink,Table1)',
        #  'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
        #  'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}
        # # 随机生成4个自由行走，一个在 BrightTable4,BrightTable5(-20,220)
        self.add_walkers([[4,1, 880], [31,250, 1200],[6,-55, 750],[10,70, -200],[27,-290, 400, 180],[26, 60,-320,90]])
        # [3,1, 880] 1号桌旁边小女孩
        # [31,250, 1200] 最角落QuietTable1女红色
        # [6,-55, 750] 1号桌附近小男孩
        # [10,70, -200]  另一边角落 QuietTable2 男黄色
        # [27,-290, 400, 180] 中间 BrightTable4 女灰
        # [26, 60,-320,90] 另一边角落 BrightTable5 红胖男
        self.control_walkers(walker_loc=[[-55, 750], [70, -200], [250, 1200], [0, 880]],is_autowalk = True)

        # 0-3男孩  4-7女孩 8-26男
        # 3男孩 31女红  32女灰  10黄色衣服男瘦  9男灰瘦 26红胖男
        # 17 是员工 police
        # [0, -150,180]


        # self.control_walkers(walker_loc=[[-55, 750]],is_autowalk = False)
        # 在场景中随机增加一堆行人。
        # walker_loc = [[-55, 750], [70, -200], [250, 1200], [0, 880]]
        # controls = []
        # for i in range(len(s.walkers)):
        #     loc = walker_loc[i]
        #     is_autowalk = False
        #     pose = GrabSim_pb2.Pose(X=loc[0], Y=loc[1], Yaw=180)
        #     controls.append(GrabSim_pb2.WalkerControls.WControl(id=i, autowalk=is_autowalk, speed=200, pose=pose))
        # scene = sim_client.ControlWalkers(GrabSim_pb2.WalkerControls(controls=controls, scene=scene_id))

        # self.gen_obj(type=5)
        # self.gen_obj(type=9)
        # self.op_task_execute(op_type=16, obj_id=0)
        # self.move_task_area(op_type=4)
        pass

    def _run(self, op_type=10):
        # 共17个操作
        # "制作咖啡","倒水","夹点心","拖地","擦桌子","开筒灯","搬椅子",    # 1-7
        # "关筒灯","开大厅灯","关大厅灯","关闭窗帘","打开窗帘",            # 8-12
        # "调整空调开关","调高空调温度","调低空调温度",                   # 13-15
        # "抓握物体","放置物体"                                       # 16-17
        #
        # self.gen_obj()
        # if op_type <=15:
        #     self.move_task_area(op_type)
        #     self.op_task_execute(op_type)
        # if op_type == 16:   # 16: 抓操作需要传入物品id
        #     self.move_task_area(op_type, obj_id=0)
        #     self.op_task_execute(op_type, obj_id=0)
        # # 原始吧台处:[247.0, 520.0, 100.0], 空调开关旁吧台:[240.0, 40.0, 100.0], 水杯桌:[-70.0, 500.0, 107]
        # # 桌子1:[-55.0, 0.0, 107],抹布桌:[340.0, 900.0, 99.0]   # 桌子2:[-55.0, 150.0, 107],
        # if op_type == 17:   # 17: 放操作需要传入放置位置周围的可达区域
        #     pos = [240.0, 40.0, 100.0]
        #     self.move_task_area(op_type, release_pos=pos)
        #     self.op_task_execute(op_type, release_pos=pos)   # [325.0, 860.0, 100]
        #
        # 流程测试
        # 抓握放置:抓吧台前生成的酸奶，放到抹布桌上
        # self.gen_obj()
        # self.move_task_area(16, obj_id=0)
        # self.op_task_execute(16, obj_id=0)
        # pos = [340.0, 900.0, 99.0]
        # self.move_task_area(17, release_pos=pos)
        # self.op_task_execute(17, release_pos=pos)
        #
        # # 做咖啡:做完的咖啡放到水杯桌上
        # self.move_task_area(1)
        # self.op_task_execute(1)
        #
        # self.find_obj("CoffeeCup")
        #
        # self.move_task_area(16, obj_id=275)
        # self.op_task_execute(16, obj_id=275)
        # pos = [-70.0, 500.0, 107]
        # self.move_task_area(17, release_pos=pos)
        # self.op_task_execute(17, release_pos=pos)
        #
        # # 倒水:倒完的水放到旁边桌子上
        # self.move_task_area(2)
        # self.op_task_execute(2)
        #
        #
        # self.move_task_area(16, obj_id=190)
        # self.op_task_execute(16, obj_id=190)
        # pos = [-55.0, 0.0, 107]
        # self.move_task_area(17, release_pos=pos)
        # self.op_task_execute(17, release_pos=pos)
        #
        # self.test_yaw()

        pass
    
    def _step(self):
        pass


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneVLM(robot)
    task.reset()
    task.run()
