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
            # (5, self.create_chat_event("测试VLM：做一杯咖啡")),
            # (5, self.create_chat_event("测试VLM：倒一杯水")),
            (5, self.create_chat_event("测试VLM：开空调")),
        ]

    def _reset(self):
        self.state["condition_set"] = {'At(Robot,Bar)','Holding(Nothing)','Is(AC,Off)'}
        pass

    def _run(self, op_type=7):
        # 共17个操作
        # "制作咖啡","倒水","夹点心","拖地","擦桌子","开筒灯","搬椅子",    # 1-7
        # "关筒灯","开大厅灯","关大厅灯","关闭窗帘","打开窗帘",            # 8-12
        # "调整空调开关","调高空调温度","调低空调温度",                   # 13-15
        # "抓握物体","放置物体"                                       # 16-17

        # 16: 抓操作需要传入物品id，17: 放操作需要传入放置位置周围的空地区域(桌边而不是桌上)
        # if op_type == 16:
        #     self.gen_obj()
        #     self.op_task_execute(op_type, obj_id=0)
        # # 原始吧台处:[247.0, 520.0, 100.0], 空调开关旁吧台:[240.0, 40.0, 70.0], 水杯桌:[-70.0, 500.0, 107]
        # # 桌子1:[-55.0, 0.0, 107],桌子2:[-55.0, 150.0, 107]
        # elif op_type == 17: self.op_task_execute(op_type, release_pos=[247.0, 520.0, 100.0])#[-55.0, 150.0, 107]
        # else:
        #     self.move_task_area(op_type)
        #     self.op_task_execute(op_type)
        pass
    
    def _step(self):
        pass
