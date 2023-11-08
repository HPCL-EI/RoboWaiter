import os
from robowaiter import Robot, task_map

TASK_NAME = 'OT'

# create robot
project_path = "./robowaiter"
ptml_path = os.path.join(project_path, 'robot/Default.ptml')
behavior_lib_path = os.path.join(project_path, 'behavior_lib')

robot = Robot(ptml_path,behavior_lib_path)

# create task
task = task_map[TASK_NAME](robot)
task.reset()
task.run()