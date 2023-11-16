# D_star Lite 机器人任务规划
## 目录结构
### 坐标离散化
`discretize_map.py`

### 地图文件(选择缩放倍率)
`map_3.pkl`
`map_4.pkl`
`map_5.pkl`

 ### 导航类
`navigate.py`

### D_star Lite 算法实现
`dstar_lite.py`

### 测试文件
`test.py` 

---

## 世界地图

### 实际坐标范围

`X: -350 ~ 600`

`Y: -400 ~ 1450`

### 5倍缩放后坐标范围

`X: -70 ~ 120`

`Y: -80 ~ 290`

### 网格地图

| Idx | Obj              |
|-----|------------------|
| 0   | free             |
| 1   | obstacle         |
| 2   | dynamic obstacle |

### 代价地图
| Cost    | Obj             |
|---------|-----------------|
| 0       | free            |
| 15-10-5 | obs周围3格         |
| inf     | obstacle        |
| 100     | dynamic obstacle |


---


## 参数
`机器人步长`： 150

`机器人速度`： 150

`机器人观测范围`： 300

`行人半径`： 36

`目标判达距离`： 50

`机器人移动dis_limit`： 10

---

## 使用方法
```python
# 选择缩放合适的地图：3、4、5
file_name = 'map_4.pkl'
if os.path.exists(file_name):
    with open(file_name, 'rb') as file:
        map = pickle.load(file)

# 初始化场景
scene.init_world(1, 11)
scene = scene.Scene(sceneID=0)

# 舒适化导航类
# (需要传入：场景、实际地图范围、离散化地图、缩放比例)
navigator = Navigator(scene=scene, area_range=[-350, 600, -400, 1450], map=map, scale_ratio=4)

# 设置目标
goal = (0, 0)

# 导航
# (animation: 选择是否画出导航过程)
navigator.navigate(goal, animation=False)

```


---

## 可靠性保证

`目标合法性保证`：

- 目标在地图外：重置目标为最近的地图内位置
- 目标在静态障碍物：从当前位置不断向外圈扩展直到找到合法位置，重置目标为该位置

`规划sbgoal合法性保证`：

- 规划subgoal被动态障碍物占据：重新规划路径


`起点合法性保证`：

- 起点在静态障碍物：从当前位置不断向外圈扩展直到找到合法位置，重置起点为该位置
- 起点在动态障碍物范围内：缩小动态障碍物半径，保证起点位置为空闲


`机器人朝向保证`：

- 机器人始终朝向每一步的移动方向


`规划抖动解决`：

- 规划路径不允许有重复点

`避免机器人沿障碍物行走`：

- 障碍物扩张：在代价地图`cost_map`中，静态障碍物周围的空位也会受到影响，并产生cost
