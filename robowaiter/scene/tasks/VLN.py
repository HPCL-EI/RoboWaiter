"""
视觉语言导航
识别顾客（NPC）靠近、打招呼、对话、领位导航到适合人数的空闲餐桌
开始条件：监测到顾客靠近
结束条件：完成领位，语音：“请问您想喝点什么？”，并等待下一步指令
"""
import os
import pickle
import time
import random

import matplotlib.pyplot as plt
import numpy as np

from robowaiter.scene.scene import Scene,init_world  # TODO: 文件名改成Scene.py

from robowaiter.scene.scene import Scene


class SceneVLN(Scene):
    def __init__(self, robot):
        super().__init__(robot)
        # 在这里加入场景中发生的事件， (事件发生的时间，事件函数)
        self.event_list = [
            (5, self.create_chat_event("测试VLN：前往桌子")),
        ]

    def _reset(self):
        file_name = './robowaiter/algos/navigate/DstarLite/map_5.pkl'
        with open(file_name, 'rb') as file:
            map = pickle.load(file)

        self.state['map']['2d'] = map
        self.state['map']['obj_pos']['Table'] = np.array((-100, 700))
