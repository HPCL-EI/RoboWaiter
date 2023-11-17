import random

# all_obj_en = ['Mug', 'Banana', 'Toothpaste', 'Bread', 'Softdrink', 'Yogurt', 'ADMilk', 'VacuumCup', 'BottledDrink', 'PencilVase',
#               'Teacup', 'Caddy', 'Dictionary', 'Cake', 'Date', 'Stapler', 'LunchBox', 'Bracelet', 'MilkDrink', 'CocountWater', 'Walnut', 'HamSausage',
#               'GlueStick', 'AdhensiveTape', 'Calculator', 'Chess', 'Orange', 'Glass', 'Washbowl', 'Durian', 'Gum', 'Towl', 'OrangeJuice', 'Cardcase',
#               'RubikCube', 'StickyNotes', 'NFCJuice', 'SpringWater', 'Apple', 'Coffee', 'Gauze', 'Mangosteen', 'SesameSeedCake', 'Glove', 'Mouse',
#               'Kettle', 'Atomize', 'Chips', 'SpongeGourd', 'Garlic', 'Potato', 'Tray', 'Hemomanometer', 'TennisBall', 'ToyDog', 'ToyBear', 'TeaTray',
#               'Sock', 'Scarf', 'ToiletPaper', 'Milk', 'Soap', 'Novel', 'Watermelon', 'Tomato', 'CleansingFoam', 'CocountMilk', 'SugarlessGum',
#               'MedicalAdhensiveTape', 'SourMilkDrink', 'PaperCup', 'Tissue', 'YogurtDrink', 'Newspaper', 'Box', 'PaperCupStarbucks', 'CoffeeMachine',
#               'Straw', 'Cake', 'Tray', 'Bread', 'Glass', 'Door', 'Mug', 'Machine', 'PackagedCoffee', 'CubeSugar',
#               'Apple', 'Spoon', 'Drinks', 'Drink', 'Take-AwayCup', 'Saucer', 'TrashBin', 'Knife', 'Ginger', 'Floor', 'Roof', 'Wall'] + \
#              ['Broom', 'CoffeeCup', 'Door', 'Glass', 'Mug', 'ZhuZi', 'Towel', 'LaJiTong', 'CoffeeMachine', 'ZaoTai', 'Sofa', 'Cake', 'ChaTou',
#               'Plate', 'CoffeeBag', 'TuoBu', 'KaiGuan', 'Kettle', 'Apple', 'ChaZuo', 'Sugar', 'BaTai', 'BaoJing', 'DrinkMachine', 'KongTiao',
#               'Desk', 'Clip', 'Knife', 'TuoPan', 'BoJi', 'ZhiBeiHe', 'Bread', 'WaterCup', 'Box', 'Chair', 'Hand', 'XiGuan', 'Spoon', 'Container',
#               'IceMachine', 'KaoXiang', 'SaoBa', 'XiangGui']

# , '机器人左手', '机器人右手', 'Bernachon'
all_obj = ['马克杯', '香蕉', '牙膏', '面包', '软饮料', '酸奶', 'AD钙奶', '真空杯', '瓶装饮料', '铅笔花瓶', '茶杯', '茶匙', '词典',
              '蛋糕', '日期', '订书机', '午餐盒', '手镯', '牛奶饮品', '椰水', '核桃', '火腿肠', '胶棒', '胶带', '计算器', '国际象棋', '橙子',
              '玻璃杯', '洗碗盆', '榴莲', '口香糖', '毛巾', '橙汁', '卡片盒', '魔方', '便签', 'NFC汁', '矿泉水', '苹果', '咖啡', '纱布', '芒果',
              '芝麻蛋糕', '手套', '鼠标', '水壶', '雾化器', '薯片', '丝瓜', '大蒜', '土豆', '托盘', '血压计', '网球', '玩具狗', '玩具熊', '茶盘',
              '袜子', '围巾', '卫生纸', '牛奶', '肥皂', '小说', '西瓜', '番茄', '洁面泡沫', '椰奶', '无糖口香糖', '医用胶带', '酸奶饮品', '纸杯',
              '纸巾', '酸奶饮品', '报纸', '盒子', '星巴克纸杯', '咖啡机', '吸管', '蛋糕', '托盘', '面包', '玻璃杯', '门',
              '马克杯', '机器', '包装咖啡', '方糖', '苹果', '勺子', '饮料', '饮料', '外带杯', '茶杯', '垃圾桶', '刀', '姜', '地板', '屋顶', '墙'] + \
             ['扫帚', '咖啡杯', '门', '玻璃杯', '马克杯', '著子', '毛巾', '垃圾桶', '咖啡机', '灶台', '沙发', '蛋糕', '插头', '盘子', '咖啡袋', '拖布', '开关',
              '水壶', '苹果', '插座', '糖', '吧台', '报警', '饮料机', '空调', '桌子', '夹子', '刀', '托盘', '簸箕', '纸杯盒', '面包', '水杯', '盒子', '椅子',
              '手', '吸管', '勺子', '容器', '制冰机', '烤箱', '扫把', '香柜']

# 储藏室
all_loc = ['吧台', '餐桌', '沙发', '灶台', '大门', '灯开关', '空调开关', '橱柜', '卫生间', '窗户', '音响', '休闲区', '工作台', '服务台', '收银台', '墙角',
              '蛋糕柜', '充电处', '冰箱', '书架']

all_loc_en = ['bar', 'Table', 'sofa', 'stove', 'Gate', 'light switch', 'airconditioner switch', 'cabinet', 'bathroom', 'window',
              'audio', 'lounge area', 'workstation', 'service counter', 'cashier counter', 'corner',
              'cake display', 'ChargingPoint', 'refrigerator', 'bookshelf']

loc_map_en = {'bar': {'工作台', '服务台', '收银台', '蛋糕柜'},
           'Table': {'沙发', '大门', '窗户', '休闲区', '墙角', '椅子', '书架'},
           'sofa': {'餐桌', '窗户', '音响', '休闲区', '墙角', '书架'},
           'stove': {'吧台', '橱柜', '工作台', '服务台', '收银台', '蛋糕柜', '冰箱'},
           'Gate': {'吧台', '灯开关', '空调开关', '卫生间', '墙角'},
           'light switch': {'大门', '空调开关', '卫生间', '墙角'},
           'airconditioner switch': {'大门', '灯开关', '卫生间', '墙角'},
           'cabinet': {'灶台', '吧台', '工作台', '服务台', '收银台', '蛋糕柜', '充电处', '冰箱'},
           'bathroom': {'大门', '墙角'},
           'window': {'餐桌', '沙发', '休闲区'},
           'audio': {'餐桌', '沙发', '休闲区', '墙角', '书架'},
           'lounge area': {'沙发', '餐桌', '墙角', '书架', '音响'},
           'workstation': {'吧台', '服务台', '收银台'},
           'service counter': {'吧台', '工作台', '收银台'},
           'cashier counter': {'吧台', '工作台', '服务台'},
           'corner': {'卫生间', '沙发', '灯开关', '空调开关', '音响', '休闲区', '书架'},
           'cake display': {'吧台', '橱柜', '服务台', '收银台', '冰箱'},
           'ChargingPoint': {'吧台', '餐桌', '沙发', '休闲区', '工作台', '服务台', '收银台', '墙角', '书架'},
           'refrigerator': {'吧台', '服务台', '蛋糕柜'},
           'bookshelf': {'餐桌', '沙发', '窗户', '休闲区', '墙角'}
           }


loc_map = {'吧台': {'灶台', '橱柜', '工作台', '服务台', '收银台', '蛋糕柜', '充电处', '冰箱'},
           '餐桌': {'沙发', '大门', '窗户', '休闲区', '墙角', '椅子', '书架'},
           '沙发': {'餐桌', '窗户', '音响', '休闲区', '墙角', '书架'},
           '灶台': {'吧台', '橱柜', '工作台', '服务台', '收银台', '蛋糕柜', '冰箱'},
           '大门': {'吧台', '灯开关', '空调开关', '卫生间', '墙角'},
           '灯开关': {'大门', '空调开关', '卫生间', '墙角'},
           '空调开关': {'大门', '灯开关', '卫生间', '墙角'},
           '橱柜': {'灶台', '吧台', '工作台', '服务台', '收银台', '蛋糕柜', '充电处', '冰箱'},
           '卫生间': {'大门', '墙角'},
           '窗户': {'餐桌', '沙发', '休闲区'},
           '音响': {'餐桌', '沙发', '休闲区', '墙角', '书架'},
           '休闲区': {'沙发', '餐桌', '墙角', '书架', '音响'},
           '工作台': {'吧台', '服务台', '收银台'},
           '服务台': {'吧台', '工作台', '收银台'},
           '收银台': {'吧台', '工作台', '服务台'},
           '墙角': {'卫生间', '沙发', '灯开关', '空调开关', '音响', '休闲区', '书架'},
           '蛋糕柜': {'吧台', '橱柜', '服务台', '收银台', '冰箱'},
           '充电处': {'吧台', '餐桌', '沙发', '休闲区', '工作台', '服务台', '收银台', '墙角', '书架'},
           '冰箱': {'吧台', '灶台', '工作台', '服务台', '收银台', '蛋糕柜'},
           '书架': {'餐桌', '沙发', '窗户', '休闲区', '墙角'}
           }

# print("looc_map:", loc_map['吧台'])
# print("looc_map:", random.choice(list(loc_map['吧台'])))


# import synonyms
# def get_synonyms(word):
#     synonyms_list = synonyms.nearby(word)[0]
#     return synonyms_list
#
# target_word = "高兴"
# synonyms_result = get_synonyms(target_word)
# print("synonyms_result:",synonyms_result)


# def save_variable(self):
#     scene = self.status
#     init_obj_name_set = set()
#     init_obj_info_dict = {}
#     for item in scene.objects:
#         name = item.name
#         location = item.location
#         init_obj_name_set.add(name)
#         # 如果name已经存在，则添加一个唯一标识符
#         if name in init_obj_info_dict:
#             count = 1
#             new_name = f"{name}_{count}"
#             while new_name in init_obj_info_dict:
#                 count += 1
#                 new_name = f"{name}_{count}"
#             name = new_name
#         init_obj_info_dict[name] = location
#     # print("obj_info_dict:",obj_info_dict)
#     # print("obj_name_set:",obj_name_set)
#     import os
#     import pickle
#     absolute_path = r"E:\DATA\Projects\Robot1002 5.2\Plugins\LLM_prompt\data\init_obj_name_set.pkl"
#     target_directory = os.path.dirname(absolute_path)
#     os.makedirs(target_directory, exist_ok=True)
#     # 将变量保存到二进制文件
#     with open(absolute_path, 'wb') as file:
#         pickle.dump(init_obj_name_set, file)