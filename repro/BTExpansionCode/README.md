# BTExpansionCode — 论文复现实验存档（Stage 2）

> **本文件是本目录的唯一权威说明。** `EXP/behavior_tree/obtea/README.md` 是早期副本，`robowaiter/behavior_tree/obtea/README.md` 是集成主程序时复制的同一份内容，三者口径以本文件为准。仓库级说明见 [`../README.md`](../README.md)。

## 0. 定位与边界

- 对应论文：Chen et al., **IJCAI 2024**, *Integrating Intent Understanding and Optimal Behavior Planning for Behavior Tree Generation from Human Instructions*（arXiv:2405.07474），**Stage 2：OBTEA / HOBTEA 最优行为树扩展与规划实验**。
- **与 MRBTP / BTP（AAAI 2025）无关**，目录名中的 "BTExpansion" 不指向那条研究线。
- 状态：**归档快照**。约 748 个文件保持原样，与 `robowaiter/` 主程序零代码耦合（主程序不 import 本目录），不参与安装，也不影响 `run_ui.py` / `tasks_no_ui/`。
- 因此，`*_old.py`、日期/计时变体、`历史代码/`、中文时间戳目录、硬编码 Windows 路径、拼写不一致，都是**历史版本链的一部分**，用于追溯「哪个脚本产出哪个结果」。**不要按工程代码标准重构、改名、合并或删除 `.py`**；一旦改动，`EXP/存档/` 中的原始结果就与代码不再对应。整理只做「索引 + 标注」。

## 1. 目录速览

```
BTExpansionCode/
├── main.py                          # 顶层入口：规划 → BT 生成 → tick 执行 → ptml → 与基线对比
├── OptimalBTExpansionAlgorithm*.py  # OBTEA 最优扩展算法及其历史变体
├── BTExpansionAlgorithm*.py         # 基线对照算法及其历史变体
├── BehaviorTree.py / Examples.py / tools.py
├── MakeCoffee.ptml / SoftdrinkCost.ptml / goal_states_unique.txt
├── EXP/                             # exp1–exp4 实验脚本、公共库、原始数据与结果
│   ├── exp_tools.py                 # 979 行实验公共库
│   ├── behavior_lib/                # 咖啡厅 act/cond 节点库
│   ├── behavior_tree/               # 另一套 obtea 实现 + ANTLR 生成的 ptml 编译器 + dataset
│   ├── 存档/、1000次结果存档/、BT_Random 实验结果存档/、merge数据存档/、历史代码/
│   ├── bt_randon_*.csv、merged_result_*.csv、合并的实验结果.xlsx
│   └── expanded_bt_obt.* / expanded_bt_xiaocai.*   # 行为树图（png/svg/dot）
├── dataset/                         # easy / medium / hard 指令-目标数据 + 校验器
├── llm_test/                        # Stage 1 早期快照（含两份 LLM_Evaluation_Kit*）
├── utils/                           # 根路径 / BT 加载 / 绘图工具
└── others/、README.assets/
```

## 2. 算法文件：谁是权威版本

> 修正旧版 README 的错误：旧 §2 称「`BTExpansionAlgorithm.py` 实现最优行为树扩展算法」，实际上它是**基线**；最优算法在 `OptimalBTExpansionAlgorithm.py`。旧 §4 写作 `Example.py`，实际文件名为 `Examples.py`。

| 文件 | 主要类 / 函数 | 角色 |
|---|---|---|
| `OptimalBTExpansionAlgorithm.py`（1015 行） | `Action`、`OptBTExpAlgorithm`（`run_algorithm` / `run_algorithm_selTree` / `save_ptml_file` / `print_solution`） | **OBTEA 最优行为树扩展**，`main.py:6` 导入的就是它 |
| `BTExpansionAlgorithm.py`（306 行） | `BTExpAlgorithm` | **基线对照算法**，`main.py:127,131` 中称 `XiaoCaiBT` |
| `BehaviorTree.py`（188 行） | `Leaf`、`ControlBT` | 叶节点 / 控制节点定义，含 `tick` |
| `Examples.py`（195 行） | `MoveBtoB`、`MoveBtoB_num`、`Cond2BelongsToCond3` | 规划案例 `goal / start / actions` |
| `tools.py`（704 行） | `print_action_data_table`、`BTTest*` | 打印与随机鲁棒性测试 |
| `main.py`（172 行） | — | 完整流程入口 |
| `EXP/exp_tools.py`（979 行） | `collect_action_nodes`、`BTTest_easy_medium_hard`、`BTTest_Merge*`、`goal_transfer_str` | 实验公共库 |

基本用法（沿用原 README，已把类名改回实际值）：

```python
from OptimalBTExpansionAlgorithm import Action, OptBTExpAlgorithm

algo = OptBTExpAlgorithm(verbose=True)
algo.clear()
algo.run_algorithm(start, goal, actions)   # 结果在 algo.bt
algo.print_solution()                      # 打印行为树
val, obj = algo.bt.tick(state)             # 执行行为树
algo.save_ptml_file("SoftdrinkCost")       # 保存 ptml
```

```python
from tools import print_action_data_table, BTTest

print_action_data_table(goal, start, actions)
BTTest(seed=1, literals_num=10, depth=10, iters=10)   # 随机生成规划问题做鲁棒性测试
```

**历史变体（不要用它替代上面两个主文件）**：`OptimalBTExpansionAlgorithm_20240108.py`（847 行，日期版）、`_single_goal.py`（654 行，单目标）、`_time.py`（817 行，计时）、`BTExpansionAlgorithm_old.py`（162 行）、`BTExpansionAlgorithm_time.py`（260 行）、`main_old.py`。这些文件含同名的 `run_algorithm` / `print_solution`，原始存档未标注唯一权威版本。

`EXP/behavior_tree/obtea/` 是**另一套** obtea 实现（对外接口 `BTOptExpInterface.process`，见其 `opt_bt_exp_main.py`），其多数同名文件与 `robowaiter/behavior_tree/obtea/` 内容一致，是复制体，**不是**顶层 `main.py` 使用的那套。需要运行现行实现时优先看主程序侧；这里的副本只作对照。

## 3. 运行方式（两套路径约定并存，需同时满足）

脚本中同时存在两类 import：

- 顶层模块式：`from BehaviorTree import ...`、`from Examples import *`、`from tools import ...`（`main.py`、顶层 `test*.py`）
- 包式：`from EXP.exp_tools import ...`、`from utils.bt.load import ...`、`from dataset.data_process_check import ...`（`EXP/exp*.py`）

两者都要求 **`BTExpansionCode/` 在 `sys.path` 上**。同时：

- `EXP/exp*.py` 用相对路径写结果 CSV（`exp2_bt_easy_medium_hard.py:95-96` 的 `cage_bt_result_=*.csv`、`数据校验.py` 的 `csv_dir='./'`），故工作目录应为 `EXP/`；
- `EXP/exp_tools.py` 经 `utils/basic.py:get_root_path()` 把根解析为 **`repro/`** 后再拼 `BTExpansionCode/EXP/...`，所以**不要单独移动 `EXP/` 或改目录名**。

推荐的运行姿势（不修改任何归档文件）：

```bash
cd repro/BTExpansionCode/EXP
PYTHONPATH="$(cd .. && pwd)" python exp2_bt_easy_medium_hard.py   # 结果 CSV 落在当前目录

cd ..
PYTHONPATH="$(pwd)" python main.py                                  # 顶层入口
```

> `../README.md` 早期写的「请在该目录下运行」不足以覆盖 `from EXP.exp_tools` 的导入需求，以本节为准。

- **依赖**：本目录无 `requirements.txt`。脚本直接 import 的第三方包为 `numpy`、`pandas`、`sympy`、`tabulate`、`matplotlib`；`EXP/behavior_tree/ptml/` 是 ANTLR 生成代码，需要 `antlr4-python3-runtime`。根 `requirements.txt` 是主程序环境（UTF-16 编码），不保证覆盖本存档，建议在独立环境先确认。
- **重跑前先备份**：部分脚本用带时间戳的文件名写 CSV，可能与 `EXP/存档/` 中的同名文件冲突。

## 4. 实验脚本 ↔ 产物索引

| 组 | 脚本 | 内容 | 结果落点 |
|---|---|---|---|
| exp1 | `exp1.py`（220 行） | 随机规划问题 + 批量鲁棒性统计（success/failure、树大小、steps、ticks、cost） | stdout → 人工存入 `存档/` |
| exp2 | `exp2.py`（48 行） | 简化随机测试 | stdout |
| | `exp2_bt_easy_medium_hard.py`（96 行） | easy/medium/hard 数据集上 OBTEA vs Baseline | `cage_bt_result_=<时间戳>.csv` |
| | `exp2_bt_easy_medium_hard_10avg.py`（104 行） | 同上，10 次平均 | CSV |
| exp3 | `exp3_Merge.py`（52 行）、`exp3_Merge_easy_medium_hard.py`（91 行）、`_10avg.py`（127 行） | merge 策略对比 | `merged_result_*.csv`、`merge数据存档/` |
| exp4 | `exp4_bt_random*.py` 六个变体 | 随机规划问题的参数扫描（`o` / `cp` / `ap` / `MAE`） | `bt_randon_o=*_cp=*_ap=*_MAE=*_time=*.csv`、`1000次结果存档/`、`BT_Random 实验结果存档/` |
| 绘图 | `Draw_bt_easy_medium_hard.py`、`plot_fig(1).py` | 从 CSV 出图 | `expanded_bt_obt.*`、`expanded_bt_xiaocai.*` |
| 校验 | `数据校验.py` | 汇总 CSV 一致性检查 | stdout |

代表性已归档结果：`EXP/存档/BT_Test_Random最终结果.txt`（由 `exp4_bt_random_final_obj.py` 产出，含 OptBT `success: 1000 failure: 0` 及 steps / tree size / ticks / cost 统计）、`EXP/合并的实验结果.xlsx`。

> ⚠️ **「文件 ↔ 论文图 / 表编号」对照表仍未建立**。上表只给出可从代码与文件名验证的「脚本 ↔ 产物」关系；引用论文具体 Figure / Table 编号前，请先与 arXiv:2405.07474 正文核对（见 `../README.md` §1）。

## 5. 已知问题（只标注，不修复）

| 问题 | 位置 | 说明 |
|---|---|---|
| 4 个脚本直接 `ImportError` | `EXP/exp1.py:4,11`、`exp4_bt_random.py:5`、`exp4_bt_random_final.py:5`、`exp4_bt_random_nodistance.py:5` | 导入 `OptimalBTExpansionAlgorithm_cond2act`，该模块全仓库不存在，属归档时缺失的中间版本。`_final_obj*.py` 用的是存在的 `OptimalBTExpansionAlgorithm`，故 exp4 的最终结果可追溯 |
| 死变量 | `main.py:15`、`exp4_bt_random_final_obj.py:8` | `output_path` 指向不存在的 `outputs/` 且未被使用 |
| 硬编码路径 | `EXP/exp_tools.py`、`utils/bt/load.py`、`utils/basic.py` | 拼接 `BTExpansionCode/EXP/...`；存档 txt 中还有 `D:\Users\caiyi\...` 的 Windows 运行记录 |
| 零字节文件 / 试验脚本 | `EXP/easy.txt`、`EXP/test`、多个空 `__init__.py`、`test.py` / `test2.py` / `test3.py` | 无功能。全目录**无 pytest / unittest**，这些不是测试 |
| 命名与拼写 | `Bahavior`、`bt_randon_*`、`plot_fig(1).py`、`Examples.py` vs `examples.py` | 沿用原始存档，不改名 |

## 6. 历史快照（勿作为现行实现）

`main_old.py`、`BTExpansionAlgorithm_old.py`、`OptimalBTExpansionAlgorithm_*.py` 变体、`EXP/历史代码/`（含整套 `behavior_lib` 复制）、`EXP/behavior_tree/obtea/` 副本、`llm_test/`（Stage 1 早期快照，含 `LLM_Evaluation_Kit/` 与 `LLM_Evaluation_Kit_最终存档0627/` 两份）、`EXP/存档/`、`1000次结果存档/`、`BT_Random 实验结果存档/`、`merge数据存档/`。

## 7. 安全

`llm_test/LLM_Evaluation_Kit*/apis/` 下的 `ERNIE_KEYS.txt` / `gpt3.txt` / `gpt4.txt` 已进入 git 索引（`.gitignore` 对已跟踪文件不生效）。归档前请**人工核查是否含真实密钥**；如含，先轮换密钥再 `git rm --cached`。详见 `../README.md` §4。
