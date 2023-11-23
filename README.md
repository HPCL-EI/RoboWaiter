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

### 安装UI
1. 安装 [graphviz-9.0.0](https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/9.0.0/windows_10_cmake_Release_graphviz-install-9.0.0-win64.exe) (详见[官网](https://www.graphviz.org/download/#windows))
2. 将软件安装目录的bin文件添加到系统环境中。如电脑是Windows系统，Graphviz安装在D:\Program Files (x86)\Graphviz2.38，该目录下有bin文件，将该路径添加到电脑系统环境变量path中，即D:\Program Files (x86)\Graphviz2.38\bin。

### 快速入门
1. 安装UE及Harix插件，打开默认项目并运行
2. 运行 tasks 文件夹下的任意场景即可实现机器人控制端与仿真器的交互


# 代码框架介绍


## Robot 
Robot是机器人类，包括从ptml加载行为树的方法，以及执行行为树的方法等


## tasks
tasks文件夹中存放的场景定义及运行代码。

| 缩写                  | 任务          |
|---------------------|-------------|
| AEM                 | 主动探索和记忆     |
| GQA                 | 具身多轮对话      |
| VLN                 | 视觉语言导航      |
| VLM                 | 视觉语言操作      |
| OT                  | 复杂开放任务      |
| AT                  | 自主任务        |
| CafeDailyOperations | 整体展示：咖啡厅的一天 |
| Interact            | 命令行自由交互     |


## Scene
Scene是场景基类，task_map返回的任务场景都继承于Scene。
该类实现了一些通用的场景操作接口。

# 调用大模型接口
运行llm_client.py文件调用大模型进行多轮对话。
```shell
cd robowaiter/llm_client
python multi_rounds.py
```
输入字符即可等待回答
