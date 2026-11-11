# repro/ — 论文复现实验存档

本目录收录与论文结果复现有关的实验代码、原始输出与数据，与 `robowaiter/` 主程序解耦：不参与安装（`setup.py` 只打包 `robowaiter`），不影响 `run_ui.py` / `tasks_no_ui/`。两个子目录沿用原始工程名，便于与论文正文和历史脚本对照。

---

## 1. 论文 ↔ 目录 ↔ 结果

| 论文 | 阶段 / 章节 | 目录 | 可直接核对的结果 |
|---|---|---|---|
| Chen et al., **IJCAI 2024**, *Integrating Intent Understanding and Optimal Behavior Planning for Behavior Tree Generation from Human Instructions*（arXiv:2405.07474） | **Stage 1**：LLM 意图理解（§3.2、§4.2、Table 1） | `LLM_Evaluation_Kit/` | `output_results/result.txt`：GA / IA 在 easy / medium / hard × zero/1/5-shot × 0/1/5 轮反馈下的汇总（对应 Table 1）；45 个 `details_*.csv` 逐样本明细、3 份 `log_*.txt` 完整日志 |
| 同上 | **Stage 2**：OBTEA / HOBTEA 最优行为树扩展与规划实验 | `BTExpansionCode/` | 算法实现 `OptimalBTExpansionAlgorithm*.py` / `BTExpansionAlgorithm*.py`；`EXP/` 下 exp1–exp4 系列实验脚本、原始 CSV 与存档（如 `EXP/存档/BT_Test_Random最终结果.txt`、`EXP/合并的实验结果.xlsx`、`EXP/1000次结果存档/`）；`dataset/` 的 easy / medium / hard 指令-目标数据 |
| 同上（早期迭代） | Stage 1 实验的历史版本 | `BTExpansionCode/llm_test/` | `LLM_Evaluation_Kit/`、`LLM_Evaluation_Kit_最终存档0627/` 两份早期 kit 快照，以及 `prompt*.txt` 试验文件 |

> `LLM_Evaluation_Kit/README.md` §1.3 给出了 Table 1 与代码的逐项对应；`BTExpansionCode/README.md` §4 给出了实验脚本 ↔ 结果文件的可核对索引，但 `BTExpansionCode/EXP/` 的原始存档**仍未附「文件 ↔ 论文图表编号」对照表**，引用具体图 / 表编号时请先与论文正文核对。

---

## 2. 目录速览

```
repro/
├── README.md                    ← 本文件
├── LLM_Evaluation_Kit/          # Stage 1：100 条标注数据 / prompt / 语法校验 / DNF 归一化 / Table 1 原始输出
│   ├── intsr2goal_test_main.py  # 唯一入口
│   ├── dataset/                 # 数据与校验器
│   ├── llms/                    # GPT-3.5 适配器（凭据为占位符）
│   ├── output_results/          # 45 CSV + 3 日志 + result.txt
│   └── README.md                # 代码—论文对应、复现步骤与已知问题
└── BTExpansionCode/             # Stage 2：行为树扩展实验存档
    ├── OptimalBTExpansionAlgorithm*.py / BTExpansionAlgorithm*.py  # 算法实现
    ├── EXP/                     # 实验脚本、behavior_lib、ptml 编译器、原始结果与绘图脚本
    ├── llm_test/                # Stage 1 的历史快照（含两份早期 kit）
    ├── dataset/                 # 指令-目标数据集
    ├── utils/                   # BT 加载 / 绘制工具
    └── README.md                # 算法 API 说明
```

---

## 3. 代码状态与运行须知

**代码状态**：两个子目录的 `.py` 与 `output_results/` 均保持归档原样，未做任何逻辑修改（仅清理编译缓存与 `.DS_Store`，并为 kit 补了 `requirements.txt`）。因此 `LLM_Evaluation_Kit/` 仍是「开箱跑不起来」的快照：入口脚本导入 `LLM.*` 包名不符、`llms/gpt3.py` 的 API 是占位符、反馈消息未真正回传模型、词表与校验器不一致。这些是复现 Table 1 前必须知道的偏差，逐条见 `LLM_Evaluation_Kit/README.md` §7、§8；**不要在归档脚本里直接修**，否则 `result.txt` 与代码不再对应。

- **`LLM_Evaluation_Kit/`**：依赖见 `requirements.txt`；从该目录自身作为工作目录运行 `intsr2goal_test_main.py`，运行前按其 README §7.2 修正 `from LLM....` 导入、§7.3 配置 API。`details_*.csv` 写在当前目录且同名覆盖，重跑前先备份 `output_results/` 中的归档结果。
- **`BTExpansionCode/`**：`EXP/exp_tools.py` 与 `utils/basic.py` 以「本存档的父目录（即 `repro/`）」为基准拼接 `BTExpansionCode/EXP/...`，因此整体移动 `BTExpansionCode/` 时路径仍自洽；实验脚本以 `EXP/` 为工作目录（结果 CSV 用相对路径写出），同时 `from EXP.exp_tools import ...` / `from dataset... import ...` 要求 `BTExpansionCode/` 也在 `sys.path` 上，即需设置 `PYTHONPATH` 指向 `BTExpansionCode/`。完整运行命令、算法文件关系与已知破损见 `BTExpansionCode/README.md` §2–§5。

---

## 4. 版本控制与安全

- `BTExpansionCode/` 已纳入 git，本次以 rename 方式整体移入；`LLM_Evaluation_Kit/` 目前**仍是未跟踪目录**（`?? repro/LLM_Evaluation_Kit/`），是否入库由维护者决定。
- ⚠️ 根 `.gitignore` 末尾列出了 `BTExpansionCode/llm_test/LLM_Evaluation_Kit*/...` 下的凭据类文件，但**这些文件已被 git 跟踪**，忽略规则对已跟踪文件不生效。本次整理只同步了路径前缀、未改动其跟踪状态；若其中含真实 API key，请先轮换密钥，再考虑 `git rm --cached` 并从历史中清理。
- 两份 kit 的 `apis/` 与 `llms/gpt3.py` 是占位 / 历史文件，归档前请自行核查不含密钥。

---

## 5. 相关链接

- [论文 arXiv:2405.07474](https://arxiv.org/abs/2405.07474) · [项目页](https://dids-ei.github.io/Project/LLM-OBTEA/) · [开源代码](https://github.com/DIDS-EI/LLM-OBTEA)
- 根 [README.md](../README.md) 的 *Related Projects* 与 §4 代码框架
