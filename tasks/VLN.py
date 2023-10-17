"""
视觉语言导航
识别顾客（NPC）靠近、打招呼、对话、领位导航到适合人数的空闲餐桌
开始条件：监测到顾客靠近
结束条件：完成领位，语音：“请问您想喝点什么？”，并等待下一步指令
"""

from scene_utils import control

# control.init_world(1, 3)

scene = control.Scene(sceneID=0)

# 实现单顾客领位
scene.reset()
scene.add_walker(1085, 2630, 220)
scene.control_walker([scene.walker_control_generator(0, False, 100, 755, 1900, 180)])

# todo: 监测到顾客靠近，打招呼，对话，识别获取空闲餐桌位置
# 可以使用scene.chat_bubble(message)函数实现对话

"""
scene.walk_to(your_free_table_location)
time.sleep(5)
scene.control_walker([scene.walker_control_generator(your_free_table_location)])
"""

reach = True
if reach:
    scene.chat_bubble("请问您想喝点什么？")

print(scene.status.walkers)
