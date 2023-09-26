# RoboWaiter
大模型具身智能比赛-机器人控制端

### 机器人控制
1. 加载场景
```python
from scene_utils import control
control.init_world(scene_num=1, mapID=3)
```
当前只有一个咖啡馆场景。加载操作只需要执行一遍，当引擎进入相应场景后，可以用`control.reset()`重置场景。