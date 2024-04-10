"""
人提出请求，机器人完成任务
1. 做咖啡（固定动画）：接收到做咖啡指令、走到咖啡机、拿杯子、操作咖啡机、取杯子、送到客人桌子上
2. 倒水
3. 夹点心

具体描述：设计一套点单规则（如菜单包含咖啡、水、点心等），按照规则拟造随机的订单。在收到订单后，通过大模型让机器人输出合理的备餐计划，并尝试在模拟环境中按照这个规划实现任务。

"""

# todo: 接收点单信息，大模型生成任务规划

from robowaiter.scene.scene import Scene
from robowaiter.behavior_lib._base.Behavior import Bahavior\

class SceneOT(Scene):

    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件
        self.signal_event_list = [
            # (3, self.customer_say, ("System", "It's quite toasty inside, could you please lower the air conditioning temperature?")),
            (3, self.add_walker, (27, 0, 700)),
            (1, self.control_walker, (0, False, 100, 60, 520, 0)),
            (1, self.customer_say, (0, "Could you please turn on the coffee machine at the bar, and make sure the floor is clean or the tube light is off? I enjoy my coffee in a cozy environment.")),  # 给我来杯酸奶和冰红茶，我坐在对面的桌子那儿。
            # (5, self.control_walker, (0, False, 100, -250, 480, 0)),
        ]


    def _reset(self):
        # self.add_walkers([[0, 880], [250, 1200]])
        # self.gen_obj_tmp()
        self.gen_obj()

        start_robowaiter = self.default_state["condition_set"]

        all_obj_place = Bahavior.all_object | Bahavior.tables_for_placement | Bahavior.tables_for_guiding
        start_robowaiter |= {f'Not RobotNear({place})' for place in all_obj_place if place != 'Bar'}
        start_robowaiter |= {f'Not Holding({obj})' for obj in Bahavior.all_object}
        start_robowaiter |= {f'Exists({obj})' for obj in Bahavior.all_object if
                             obj != 'Coffee' and obj != 'Water' and obj != 'Dessert'}
        # 'Softdrink' 在Table1
        start_robowaiter |= {f'Not On(Softdrink,{place})' for place in Bahavior.all_place if place != "Table1"}
        start_robowaiter |= {f'Not On(VacuumCup,{place})' for place in Bahavior.all_place if place != "Table2"}

        # 默认物品都在 Bar 上
        start_robowaiter |= {f'On({obj},Bar)' for obj in Bahavior.all_object if
                             obj != 'Coffee' and obj != 'Water' and obj != 'Dessert' \
                             and obj != 'Softdrink' and obj != 'VacuumCup'}
        for place in Bahavior.all_place:
            if place != "Bar":
                start_robowaiter |= {f'Not On({obj},{place})' for obj in Bahavior.all_object}
            # start_robowaiter |= {f'On({obj},{place})' for obj in Bahavior.all_object if
            #                      obj != 'Coffee' and obj != 'Water' and obj != 'Dessert'}

        # 这三样哪里都没有
        make_obj = {"Coffee", 'Water', 'Dessert'}
        for place in Bahavior.all_place:
            start_robowaiter |= {f'Not On({obj},{place})' for obj in make_obj}

        self.state["condition_set"] = start_robowaiter
        pass


    def _run(self):
        pass


if __name__ == '__main__':
    import os
    from robowaiter.robot.robot import Robot

    robot = Robot()

    # create task
    task = SceneOT(robot)
    task.reset()
    task.run()
