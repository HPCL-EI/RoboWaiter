![image](https://github.com/HPCL-EI/RoboWaiter/assets/39987654/fd7a6acf-7c0a-454f-95c3-4f33da0f0815)# RoboWaiter

本项目为参加达闼杯“机器人大模型与具身智能挑战赛”的参赛作品。我们的目标是结合前沿的大模型技术和具身智能技术，开发能在模拟的咖啡厅场景中承担服务员角色并自主完成各种具身任务的智能机器人。这里是我们的参赛作品《基于大模型和行为树和生成式具身智能体》的机器人控制端代码。

# 1. 技术简介

我们提出基于大模型和行为树的生成式具身智能体系统框架

1 行为树是系统的中枢，作为大模型和具身智能之间的桥梁，解决两者结合的挑战

2 大语言模型是系统的大脑。一方面，我们设计了向量数据库和工具调用，另一方面，在实现智能体规划上，我们不再需要大语言模型输出完整的动作序列，而仅仅给出一个任务目标，这大大缓解了大模型的具身幻觉现象。

3 而具身机器人是系统的躯体，在条件节点感知和动作节点控制的函数中，我们优化了接口调用和算法设计，提高感知高效性和控制准确性

![image](https://github.com/HPCL-EI/RoboWaiter/assets/39987654/9b807263-7458-4b5c-8d3a-101351a2fd41)

# 2. 项目安装（必看）

## 2.1 环境要求

Python=3.10

## 2.2 安装步骤

```shell
git clone https://github.com/HPCL-EI/RoboWaiter.git
cd RoboWaiter
pip install -e .
```

以上步骤将完成robowaiter项目以及相关依赖库的安装

## 2.3 安装UI

1. 安装 [graphviz-9.0.0](https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/9.0.0/windows_10_cmake_Release_graphviz-install-9.0.0-win64.exe) (详见[官网](https://www.graphviz.org/download/#windows))

2. 将软件安装目录的bin文件添加到系统环境中。如电脑是 Windows 系统，Graphviz 安装在 D:\Program Files (x86)\Graphviz2.38，该目录下有bin文件，将该路径添加到电脑系统环境变量 path 中，即 D:\Program Files (x86)\Graphviz2.38\bin。如果不行，则需要重启。

3. 安装向量数据库
   conda install -c conda-forge faiss

4. 安装自然语言处理和翻译工具，用于计算相似性

   ```
   pip install translate
   pip install spacy 
   python -m spacy download zh_core_web_lg
   ```
   `zh_core_web_lg` 如果下载较慢，可以直接通过分享的网盘链接下载

   链接：https://pan.baidu.com/s/1vr7dqHsgnh6UChymQc26VA 
   提取码：1201 
   --来自百度网盘超级会员V7的分享

   ```
   pip install zh_core_web_lg-3.7.0-py3-none-any.whl
   ```

## 2.4 快速入门

1. 安装 UE 及 Harix 插件，打开默认项目并运行

2. 不使用 UI 界面 ：运行 tasks_no_ui 文件夹下的任意场景即可实现机器人控制端与仿真器的交互

3. 使用 UI 界面：运行 `run_ui.py` ，显示下面的界面。点击左侧的按钮，机器人就会执行相应的任务。也可以在右上方直接输出目标状态或者对话和机器人直接交互。

![image](https://github.com/HPCL-EI/RoboWaiter/assets/39987654/c436e297-baf8-4e6e-9f73-b9f9ad9ac415)


# 3. 代码框架介绍

代码库被组织成几个模块，每个模块负责系统功能的一部分：

- **behavior_lib：** `behavior_lib` 是行为树节点库类，包括行为树的动作节点和条件节点。它们分别存放在 `act` 和 `cond` 文件夹下。
- **behavior_tree： **`behavior_tree` 是行为树算法类，包括 `ptml` 编译器、最优行为树逆向扩展算法等。
- **robot：** `robot` 是机器人类，包括从 `ptml`加载行为树的方法，以及执行行为树的方法等。
- **llm_client：** `llm_client` 是大模型类，主要实现了大模型的数据集构建、数据处理工具、大模型调用接口、大模型评测、工具调用、工具注册、向量数据库、单论对话、对轮对话等方法或接口。

​	调用大模型接口。运行llm_client.py文件调用大模型进行多轮对话。输入字符即可等待回答/

```shell
cd robowaiter/llm_client
python multi_rounds.py
```
- **scene：**`scene` 是场景基类，该类实现了一些通用的场景操作接口，实现了与 UE 和咖啡厅仿真场景的通信。其中，包括了官方已经封装好的各种接口，如场景初始化、行人控制、操作动画设置、物品设置、机器人 IK 接口等。`task_map` 返回的任务场景都继承于 `Scene`。此外，在 `scene/ui` 中，我们实现了 UI 的界面设计和接口封装。
- **utils：**`utils`为其它工具类，比如绘制行为树并输出为图片文件。
- **algos：**`algos` 是其它算法类，包括MemGPT、导航算法 (`navigator`)、边界探索 (`explore`)、视觉算法 (`vision`)、向量数据库 (`retrieval`) 等。
- **tasks：**tasks文件夹中存放的场景定义及运行代码。

| 缩写                | 任务                   |
| ------------------- | ---------------------- |
| AEM                 | 主动探索和记忆         |
| GQA                 | 具身多轮对话           |
| VLN                 | 视觉语言导航           |
| VLM                 | 视觉语言操作           |
| OT                  | 复杂开放任务           |
| AT                  | 自主任务               |
| CafeDailyOperations | 整体展示：咖啡厅的一天 |
| Interact            | 命令行自由交互         |
# 4. 花絮

**机器人根据顾客的点单，完成订单并送餐**
![image](https://github.com/HPCL-EI/RoboWaiter/assets/39987654/79cff908-9ebd-4e54-9b10-08466cae337a)

**顾客询问物品位置，并要求机器人送回**
![image](https://github.com/HPCL-EI/RoboWaiter/assets/39987654/b8df6475-6889-4816-8e17-b0a1c57160b9)

**咖啡厅生意兴隆，机器人正在依次服务排队的顾客**
![image](https://github.com/HPCL-EI/RoboWaiter/assets/39987654/312714b1-0fb6-45bc-9a71-bf469107e58d)

版权所有 (c) [2023] [NUDT-HPCL-EI]
