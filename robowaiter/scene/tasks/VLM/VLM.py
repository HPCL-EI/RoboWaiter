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
        self.event_list = [
            (5, self.create_chat_event("把酸奶放到1号桌，再做一杯咖啡送到水杯桌上，再倒一杯水。")),
            # (10, self.create_chat_event("开空调")),

            # (15, self.create_chat_event("下班啦！打扫卫生，关灯关空调关窗帘。")),


            # (9, self.create_chat_event("关窗帘")),
            # (9, self.create_chat_event("开大厅灯")),
            # (5, self.create_chat_event("测试VLM：做一杯咖啡")),
            # (5, self.create_chat_event("测试VLM：倒一杯水")),
            # (5, self.create_chat_event("测试VLM：关空调")),
            # (5, self.create_chat_event("测试VLM：拖地")),
            # (5, self.create_chat_event("测试VLM：擦桌子")),
            # (5, self.create_chat_event("测试VLM：整理椅子")),
            # (5, self.create_chat_event("测试VLM：把冰红茶放到Table2")),
            # (5, self.create_chat_event("测试VLM：关大厅灯"))
            # (5, self.create_chat_event("测试VLM：做一杯咖啡放到吧台上")),
            # (5, self.create_chat_event("测试VLM：做一杯咖啡放到水杯桌上，再倒一杯水")),
            # (10, self.create_chat_event("测试VLM：关窗帘")),
            # (5, self.create_chat_event("测试VLN：前往2号桌")),
            # (11, self.create_chat_event("测试VLM：拖地")),
            # (12, self.create_chat_event("测试VLM：擦桌子")),
        ]

    def _reset(self):
        self.gen_obj()
        self.state["condition_set"] = {'At(Robot,Bar)', 'Is(AC,Off)',
         'Holding(Nothing)','Exist(Yogurt)','Exist(Softdrink)','On(Yogurt,Bar)','On(Softdrink,Table1)',
         'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
         'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}
        # 随机生成4个自由行走，一个在 BrightTable4,BrightTable5(-20,220)
        self.add_walkers([[0, 880], [250, 1200], [-55, 750], [70, -200],[-290, 400, 0],[20, -150,180]])
        self.control_walkers(walker_loc=[[-55, 750], [70, -200], [250, 1200], [0, 880]],is_autowalk = True)


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
        # self.move_task_area(16, obj_id=190)
        # self.op_task_execute(16, obj_id=190)
        # pos = [-55.0, 0.0, 107]
        # self.move_task_area(17, release_pos=pos)
        # self.op_task_execute(17, release_pos=pos)

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
