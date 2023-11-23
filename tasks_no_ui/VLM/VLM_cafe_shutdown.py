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
        # 出现员工和机器人说关门了(机器人可能手上还拿着东西)
        self.new_event_list = [
            (3, self.add_walker, (17, 60, 1000)),
            (6, self.control_walkers_and_say, ([[[6, False, 500, 60, 520, 0, "下班啦！别忘了打扫卫生。"]]])),
        ]

    def _reset(self):
        self.gen_obj()
        self.state["condition_set"] = {'At(Robot,Bar)', 'Is(AC,Off)',
         'Holding(Nothing)','Exist(Yogurt)','Exist(Softdrink)','On(Yogurt,Bar)','On(Softdrink,Table1)',
         'Is(HallLight,Off)', 'Is(TubeLight,On)', 'Is(Curtain,On)',
         'Is(Table1,Dirty)', 'Is(Floor,Dirty)', 'Is(Chairs,Dirty)'}
        # 随机生成4个自由行走，一个在 BrightTable4,BrightTable5(-20,220)
        self.add_walkers([[3,1, 880], [31,250, 1200],[6,-55, 750],[10,70, -200],[27,-290, 400, 180],[26, 60,-320,90]])
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

        pass

    def _run(self, op_type=10):

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
