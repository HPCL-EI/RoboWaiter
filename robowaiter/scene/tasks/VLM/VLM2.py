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

        ]

    def _reset(self):
        self.gen_obj()
        pass

    def _run(self, op_type=10):
        # 一个行人从门口走到 吧台
        # 打招呼需要什么
        # 行人说 哪里有位置，想晒个太阳
        # 带领行人去有太阳的地方
        # 行人说 有点热
        # 好的，这就去开空调
        scene = self.add_walkers([[47, 920]])
        self.control_walker(
            [self.walker_control_generator(walkerID=0, autowalk=False, speed=200, X=60, Y=520, Yaw=0)])

        cont = scene.walkers[0].name+":请问可以带我去空位上嘛？我想晒太阳"
        self.control_robot_action(0,3,cont)

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
