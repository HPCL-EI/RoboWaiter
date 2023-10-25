# RoboWaiter
大模型具身智能比赛-机器人控制端

# 项目安装（必看）
## 环境要求
Python=3.10

### 安装步骤
```shell
cd RoboWaiter
pip install -e .
```
以上步骤将完成robowaiter项目以及相关依赖库的安装

### 快速入门
1. 安装UE及Harix插件，打开默认项目并运行
2. 运行 run_robowaiter.py 文件即可实现机器人控制端与仿真器的交互


# 运行流程介绍
run_robowaiter.py 入口文件如下：
```python
import os
from robowaiter import Robot, task_map

TASK_NAME = 'GQA'

# create robot
project_path = "./robowaiter"
ptml_path = os.path.join(project_path, 'robot/Default.ptml')
behavior_lib_path = os.path.join(project_path, 'behavior_lib')

robot = Robot(ptml_path,behavior_lib_path)

# create task
task = task_map[TASK_NAME](robot)
task.reset()
task.run()
```

## Robot 
Robot是机器人类，包括从ptml加载行为树的方法，以及执行行为树的方法等


## task_map
task_map是任务字典，通过任务缩写来返回相应的场景类。

| 缩写 | 任务      |
|----|---------|
| AEM  | 主动探索和记忆 |
| GQA  | 具身多轮对话  |
| VLN  | 视觉语言导航  |
| VLM  | 视觉语言操作  |
| OT  | 复杂开放任务   |
| AT  | 自主任务    |


## Scene
Scene是场景基类，task_map返回的任务场景都继承于Scene。
该类实现了一些通用的场景操作接口。

### 场景中物品类别

| ID  | Item                 |
|-----|----------------------|
| 0   | Mug                  |
| 1   | Banana               |
| 2   | Toothpaste           |
| 3   | Bread                |
| 4   | Softdrink            |
| 5   | Yogurt               |
| 6   | ADMilk               |
| 7   | VacuumCup            |
| 8   | Bernachon            |
| 9   | BottledDrink         |
| 10  | PencilVase           |
| 11  | Teacup               |
| 12  | Caddy                |
| 13  | Dictionary           |
| 14  | Cake                 |
| 15  | Date                 |
| 16  | Stapler              |
| 17  | LunchBox             |
| 18  | Bracelet             |
| 19  | MilkDrink            |
| 20  | CocountWater         |
| 21  | Walnut               |
| 22  | HamSausage           |
| 23  | GlueStick            |
| 24  | AdhensiveTape        |
| 25  | Calculator           |
| 26  | Chess                |
| 27  | Orange               |
| 28  | Glass                |
| 29  | Washbowl             |
| 30  | Durian               |
| 31  | Gum                  |
| 32  | Towl                 |
| 33  | OrangeJuice          |
| 34  | Cardcase             |
| 35  | RubikCube            |
| 36  | StickyNotes          |
| 37  | NFCJuice             |
| 38  | SpringWater          |
| 39  | Apple                |
| 40  | Coffee               |
| 41  | Gauze                |
| 42  | Mangosteen           |
| 43  | SesameSeedCake       |
| 44  | Glove                |
| 45  | Mouse                |
| 46  | Kettle               |
| 47  | Atomize              |
| 48  | Chips                |
| 49  | SpongeGourd          |
| 50  | Garlic               |
| 51  | Potato               |
| 52  | Tray                 |
| 53  | Hemomanometer        |
| 54  | TennisBall           |
| 55  | ToyDog               |
| 56  | ToyBear              |
| 57  | TeaTray              |
| 58  | Sock                 |
| 59  | Scarf                |
| 60  | ToiletPaper          |
| 61  | Milk                 |
| 62  | Soap                 |
| 63  | Novel                |
| 64  | Watermelon           |
| 65  | Tomato               |
| 66  | CleansingFoam        |
| 67  | CocountMilk          |
| 68  | SugarlessGum         |
| 69  | MedicalAdhensiveTape |
| 70  | SourMilkDrink        |
| 71  | PaperCup             |
| 72  | Tissue               |
| 73  | YogurtDrink          |
| 74  | Newspaper            |
| 75  | Box                  |
| 76  | PaperCupStarbucks    |
| 77  | CoffeeMachine        |
| 78  | GingerLHand          |
| 79  | GingerRHand          |
| 80  | Straw                |
| 81  | Cake                 |
| 82  | Tray                 |
| 83  | Bread                |
| 84  | Glass                |
| 85  | Door                 |
| 86  | Mug                  |
| 87  | Machine              |
| 88  | Packaged Coffee      |
| 89  | Cube Sugar           |
| 90  | Apple                |
| 91  | Spoon                |
| 92  | Drinks               |
| 93  | Drink                |
| 94  | Take-Away Cup        |
| 95  | Saucer               |
| 96  | Trash Bin            |
| 97  | Knife                |
| 251 | Ginger               |
| 252 | Floor                |
| 253 | Roof                 |
| 254 | Wall                 |
注意：78及以后无法使用add_object方法生成
