# RoboWaiter
大模型具身智能比赛-机器人控制端

### 机器人控制
1. 加载场景
```python
from scene_utils import control
control.init_world(scene_num=1, mapID=3)
```
当前只有一个咖啡馆场景。加载操作只需要执行一遍，当引擎进入相应场景后，可以用`control.reset()`重置场景。

2. 物品类别

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