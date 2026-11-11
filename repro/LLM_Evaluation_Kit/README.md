# LLM Evaluation Kit — 基于大模型的意图理解（Instruction → Goal）

> 本目录是论文 **《Integrating Intent Understanding and Optimal Behavior Planning for Behavior Tree Generation from Human Instructions》**（arXiv:2405.07474v2, 2024-06）中**第一板块 / Stage 1：基于大模型的意图理解（§3.2 Intent Understanding、§4.2 Analysis for Intent Understanding、Table 1）** 的实验代码与结果归档快照。
>
> 一句话概括：**让 GPT-3.5 把咖啡厅场景的自然语言服务指令翻译成一阶逻辑合式公式（WFF）形式的目标，用语法/词表校验器 + DNF 归一化评估其语法正确率（GA）与意图解释正确率（IA），并消融研究 few-shot 示例数量与自动反馈纠错轮数的影响。**

---

## 目录

- [0. 这份代码是什么、不是什么](#0-这份代码是什么不是什么)
- [1. 论文背景与代码对应关系](#1-论文背景与代码对应关系)
- [2. 任务的形式化定义](#2-任务的形式化定义)
- [3. 目录结构](#3-目录结构)
- [4. 核心实现与评测流程](#4-核心实现与评测流程)
- [5. 评测数据集](#5-评测数据集)
- [6. 输出文件与实验结果](#6-输出文件与实验结果)
- [7. 快速开始与复现](#7-快速开始与复现)
- [8. 已知问题与注意事项](#8-已知问题与注意事项)
- [9. 扩展与二次开发](#9-扩展与二次开发)
- [10. 引用](#10-引用)

---

## 0. 这份代码是什么、不是什么

**它是：**

- 一个**离线、纯文本到文本**的语义解析（intent-to-goal / semantic grounding）评测基准；
- 一个**实验快照**：包含 100 条标注数据、prompt、GPT-3.5 调用封装、语法/语义校验器、评测主程序，以及论文 Table 1 背后的全部原始输出（45 个 CSV、3 份日志、1 份汇总表）；
- 一个**两因素消融实验**：`few-shot 示例数 ∈ {0, 1, 5}` × `反馈纠错轮数 ∈ {0..5}` × `难度 ∈ {easy, medium, hard}`，每个配置独立重复 5 次。

**它不是：**

- ❌ 不包含论文第二板块 **OBTEA（最优行为树扩展算法）** 的实现，也不包含 BT Expansion / 行为规划；
- ❌ 不调用仿真环境、机器人、ROS、pygame，也不做任务执行成功率评测（日志首行出现的 `pygame` 只是原工程环境自带的启动打印）；
- ❌ 不调用行为树规划器，也不与宿主仓库 `robowaiter/` 主程序有 import 关系；
- ❌ 不是可 pip 安装的库；虽有 `requirements.txt`（仅列复现所需依赖），但没有 `setup.py` / 配置文件，所有参数硬编码在入口脚本里；
- ❌ 不做模型微调（论文明确强调「无需在任何专用数据集上做监督微调」）。

本目录位于 `repro/LLM_Evaluation_Kit/`，是论文两阶段框架的 **Stage 1** 复现快照：产出的 DNF 子目标 / 谓词集合正是 Stage 2 行为规划器所需的符号 goal，Stage 2 的实验代码见 `../BTExpansionCode/`。它与 `robowaiter/` 主程序、Stage 2 实验代码**均无代码耦合**（不 import、也不被引用）。本目录当前尚未纳入 git 跟踪，归档前请先确认 `apis/`、`llms/gpt3.py` 中无真实凭据。

---

## 1. 论文背景与代码对应关系

### 1.1 论文框架

论文提出两阶段的行为树生成框架：

```
人类自然语言指令
      │
      ▼  Stage 1：LLM 意图理解（本 kit 覆盖的部分）
  目标 G：一阶逻辑合式公式 WFF
      │  DNF 归一化 → 若干子目标（每个合取项是一个子目标）
      ▼  Stage 2：OBTEA 最优行为规划（本 kit 不含）
  最优行为树 T*（保证有限时间成功 + 最小代价）
```

WFF 形式的 goal 是两个阶段之间的「桥梁」：对 LLM 而言一阶逻辑语法可读、可生成；对规划器而言 DNF 的每个析取项可直接映射成行为树 condition 节点与子目标。论文咖啡厅示例：

```
Instruction: Could you please clean the table and give me a cup of coffee or tea?
Goal (论文写法): ¬Dirty(Table) ∧ (On(Coffee,Table) ∨ On(Tea,Table))
Goal (本 kit 写法): IsClean_Table1 & (On_Coffee_Table1 | On_Tea_Table1)
```

> 注：论文 §3.1/§4.1 使用的谓词名是 `Dirty` / `Activate`，本快照迭代后统一为 `IsClean` / `Active`（详见 [§8](#8-已知问题与注意事项)）。

### 1.2 §3.2 三种方法 ↔ 代码

| 论文 §3.2 方法 | 论文描述 | 本目录实现 | 关键位置 |
|---|---|---|---|
| **Prompt Engineering** | prompt 由 4 部分构成：① Objects（按 `<food>`/`<place>` 等分类的对象集）② Condition Predicates（谓词及其参数域）③ Few-shot Demonstrations（指令-目标对）④ System（任务说明与输出格式约束） | `generate_prompt1(num_examples, difficulty)` 动态拼接 ①②③④，末尾再拼上 `dataset/prompt_test2.txt` 的 5 条编号任务说明 | `intsr2goal_test_main.py:63-121`、`dataset/prompt_test2.txt` |
| **Reflective Feedback** | 输出后由 **syntax checker** 判断是否构成 WFF，**semantic checker** 校验谓词/对象合法性；出错则把指令连同额外提示重新输入 LLM，用**逐步扩充的黑名单**禁止再次出现非法文本，直到语法错误全部修正或达到最大重试次数 | `format_check()` 做两层校验；`get_feedback_prompt()` 维护并累积三类黑名单；`evaluate_section()` 中 `while feedback_time <= 5` 循环重试 | `dataset/data_process_check.py:38-83`、`intsr2goal_test_main.py:124-153, 186-215` |
| **Goal Normalization** | 把合法 goal 归一化为 **DNF**：一是消除 WFF 歧义以便评估两个 goal 是否等价，二是每个合取项视为一个子目标（任一子目标达成即成功），便于模块化规划 | `sympy.to_dnf` + `goal_transfer_ls_set()`：按 `\|` 拆析取项、按 `&` 拆文字，并把 `On_X_Y` 改写为 `On(X,Y)`、`~` 改写为 `Not ` | `dataset/data_process_check.py:86-104` |

### 1.3 §4.2 实验设置 ↔ 代码

| 论文 §4.2 / Table 1 | 本目录 |
|---|---|
| 100 条指令-目标对，按 easy / medium / hard 三档划分 | `dataset/{easy,medium,hard}_instr_goal.txt`，共 30 + 30 + 40 = 100 条 |
| GA（grammatical accuracy）：无语法错误的输出占比 | `GA-xF`，由 `format_check()` 通过率计算 |
| IA（interpretation accuracy）：与 ground truth 等价的 goal 占比 | `IA-xF`，由 `evaluate_answer()` 的集合包含判定计算（实现较论文表述更宽松，见 §4.6） |
| 消融 1：示例数（Zero-shot / Few-shot-1 / Few-shot-5） | `num_examples = [0, 1, 5]` |
| 消融 2：最大重试次数（GA-NF / GA-1F / GA-5F） | `feedback_time ∈ 0..5`，`max_try_time = 5` 指重复试验次数而非重试次数 |
| 每个结果是 5 次运行的平均 | `max_try_time = 5` 外层循环 + `np.mean` |
| 默认设置：5 个示例 + 5 次重试 | `num_examples` 含 5；反馈上限 5 轮（共最多 6 次调用） |
| 模型：`gpt-3.5-turbo`（论文注明 2024.06 版本），方法 model-agnostic | `llms/gpt3.py` 硬编码 `model="gpt-3.5-turbo"`；类 `LLMGPT3` 是唯一适配器 |
| Table 1 的汇总数字 | `output_results/result.txt`（数值基本一一对应） |
| 咖啡厅场景：80 objects、8 条件谓词、6 动作谓词、1318 literals、1269 actions | 本 kit 只用到条件谓词白名单与约 60 个对象词；动作谓词属于 Stage 2，不在本目录 |

### 1.4 论文结论（§4.2）在本数据上的体现

- **逻辑语法比语义更容易学**：难度上升时 IA 下降明显快于 GA；
- **一个示例胜过一长段解释**（one-shot 相对 zero-shot 提升最大）；
- **反馈纠错主要提升语法**：随允许重试轮数增加 GA 持续上升；
- **无需监督微调**，仅靠 prompt + few-shot + 自动反馈，LLM 就能把自然语言翻译成 WFF 形式的目标。

---

## 2. 任务的形式化定义

### 2.1 环境三元组 ⟨O, Pc, Pa⟩

论文用 ⟨O, Pc, Pa⟩ 描述环境：`O` 为可用对象集，`Pc` 为条件谓词集，`Pa` 为动作谓词集。本 kit 只涉及 `Pc`（8 个条件谓词）与 `O` 的分类词表：

| 谓词模板 | 参数类别 | 含义 | 示例 |
|---|---|---|---|
| `RobotNear_<items_place>` | 物品 + 地点 | 机器人靠近某处 | `RobotNear_Bar` |
| `On_<items>_<place>` | 物品、地点 | 某物被放置在某处 | `On_Coffee_Table2` |
| `Holding_<items>` | 物品 | 机器人手持某物 | `Holding_VacuumCup` |
| `Exists_<makable>` | 可制作物 | 已备好某物 | `Exists_Water` |
| `IsClean_<furniture>` | 家具 | 某处已清洁 | `IsClean_Chairs` |
| `Active_<appliance>` | 电器 | 设备开启 | `Active_AC` |
| `Closed_<furnishing>` | 陈设 | 关闭状态 | `Closed_Curtain` |
| `Low_<control>` | 控制量 | 温度偏低 | `Low_ACTemperature` |

对象类别（见 `generate_prompt1()` 的 `[Objects]` 段）：

```
<items>       ≈ 60 个物品词（Coffee, Water, Yogurt, Chips, VacuumCup, NFCJuice, ...）
<place>       20 个地点（Bar, WaterStation, CoffeeStation, Table1..3,
              WindowTable4/5/6, QuietTable7/8/9, ReadingNook, ...）
<makable>     ['Coffee', 'Water', 'Dessert']
<furniture>   ['Table1', 'Floor', 'Chairs']
<appliance>   ['AC', 'TubeLight', 'HallLight']
<furnishing>  ['Curtain']
<control>     ['ACTemperature']
```

### 2.2 逻辑连接词

| 论文 | 代码 | 含义 |
|---|---|---|
| ∧ | `&` | 合取 AND |
| ∨ | `\|` | 析取 OR |
| ¬ | `~` | 否定 NOT |
| — | `(` `)` | 分组 |

模型被要求**只输出单行公式、不带任何解释**（`prompt_test2.txt:4-5`）。

### 2.3 从公式到子目标

`goal_transfer_ls_set()` 把公式转成「析取项 → 文字集合」的列表，等价于论文 Fig. 2 里的 `ParseSubGoals(G)`：

```
输入: (On_Dessert_Table1 | On_Water_Table2) & Active_HallLight
to_dnf: (On_Dessert_Table1 & Active_HallLight) | (On_Water_Table2 & Active_HallLight)
子目标 1: {"On(Dessert,Table1)", "Active(HallLight)"}
子目标 2: {"On(Water,Table2)", "Active(HallLight)"}
```

每个子目标在 Stage 2 中生成一棵最优子树，最后按代价排序挂到 Fallback 节点下组装成最终行为树。本 kit 到此为止，不做后续规划。

---

## 3. 目录结构

```
LLM_Evaluation_Kit/
├── README.md                          ← 本文件
├── requirements.txt                   复现所需依赖（非原实验环境精确版本）
├── __init__.py                        (空，Python 包占位)
├── intsr2goal_test_main.py            ★ 唯一入口：prompt 构造 + 校验 + 反馈循环 + 指标计算
├── apis/
│   ├── __init__.py                    (空)
│   └── gpt3.txt                       (空，预留的 API 说明/凭证位，从未被引用)
├── llms/
│   ├── __init__.py                    (空)
│   └── gpt3.py                        ★ 唯一 LLM 适配器（OpenAI-compatible Chat Completions）
├── dataset/
│   ├── data_process_check.py          ★ 语法/词表校验 + DNF 归一化
│   ├── easy_instr_goal.txt            30 条，单原子公式
│   ├── medium_instr_goal.txt          30 条，两个文字用 & 或 | 连接
│   ├── hard_instr_goal.txt            40 条，三个以上文字、嵌套括号、否定
│   ├── prompt_test.txt                完整 prompt 草稿（旧谓词 Dirty_，脚本不读）
│   ├── prompt_test1.txt               prompt 上半部分（读入但未被使用，旧谓词 Dirty_）
│   └── prompt_test2.txt               ★ 实际拼到 prompt 末尾的任务说明（5 条编号规则）
└── output_results/
    ├── details_{easy|medium|hard}_shot={0|1|5}_t={0..4}.csv   45 个逐样本明细
    ├── log_easy.txt / log_medium.txt / log_hard.txt             3 份完整终端日志
    └── result.txt                     ★ 论文 Table 1 对应的汇总表（5 次重复平均）
```

> 目录名 `intsr2goal` 是 `instr2goal`（instruction-to-goal）的拼写变体；`prompt_test*.txt` 里的 `test` 指 prompt 模板试验，不是测试集。

---

## 4. 核心实现与评测流程

### 4.1 总流程

```
                       ┌─────────────────────────────────────────────┐
                       │ generate_prompt1(num_examples, difficulty)   │
                       │  [Condition Predicates] + [Objects]          │
                       │  + [Few-shot Demonstrations] + [System]      │
                       │  + dataset/prompt_test2.txt                  │
                       └──────────────────┬──────────────────────────┘
                                          ▼
  数据集按空行切成 section（每 2 行） → ThreadPoolExecutor(max_workers=5) 并发
                                          ▼
   ┌────────────────────────── evaluate_section(prompt, section) ──────────────────────────┐
   │  while feedback_time <= 5:                                                              │
   │    1. llm.request([{"role":"user","content": prompt + "\n" + question}])               │
   │    2. format_check(answer)  → 语法是否合法 + 三类错误集合                              │
   │    3. 合法 → evaluate_answer(标准 goal, 输出) 判语义；把 f..5 的 GA/IA 全部记账；break │
   │       非法 → 当前 f 的 GA/IA 记 0；get_feedback_prompt() 生成黑名单提示；f += 1        │
   │    4. 把模型输出与反馈提示逐列写入 CSV                                                 │
   └───────────────────────────────────────────────────────────────────────────────────────┘
                                          ▼
   汇总 results 字典 → np.mean 得到 GA-0F/1F/5F、IA-0F/1F/5F（打印到 stdout）
   → 5 次重复再取平均 → result.txt（人工归档）
```

### 4.2 LLM 适配器 `llms/gpt3.py`

```python
class LLMGPT3():
    def __init__(self):
        self.client = OpenAI(base_url="URL", api_key="Your-Key")   # 占位符，需自行填写

    def request(self, message):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=message)
        return completion.choices[0].message.content
```

- 只支持 `openai>=1.x` 的 Chat Completions 接口（类名虽有 `GPT3`，实为 chat 模型）；
- 没有 `temperature` / `max_tokens` / `top_p` 设置，全部用服务端默认；**5 次独立重复的随机性正来源于此**；
- `request()` 返回原始字符串，不做任何 JSON/正则抽取；解析与校验全部交给 `data_process_check.py`；
- 另有 `embedding()`、`list_models()`、`list_embedding_models()` 供 `__main__` 自检，评测流程不使用。

### 4.3 Prompt 构造 `generate_prompt1()`（`intsr2goal_test_main.py:63-121`）

最终 prompt = `generate_prompt1(num, difficulty) + "\n" + prompt_test2.txt 内容 + "\n" + Instruction 行`。四段构成对应论文 §3.2 的 Prompt Engineering：

1. `[Condition Predicates]`：8 个谓词模板（§2.1 表格）；
2. `[Objects]`：各类别对象词表；
3. `[Few-shot Demonstrations]`：`num_examples` 取 0 / 1 / 5 时截取对应难度示例列表的前 N 条。示例按难度设计，例如
   - easy：`Instruction: Would you be able to provide some chips at the third table?` → `On_Chips_Table3`
   - medium：`Closed_Curtain | Active_AC`、`On_Chips_Table3 & Active_AC`
   - hard：`(On_Chips_Table3 | On_Chips_Table2)& ~Active_AC`、`IsClean_Chairs & ( On_Apple_Bar | On_Banana_Bar )`
4. `[System]`：说明前三段的作用；`prompt_test2.txt` 再补充任务定义、`& | ~` 的语义、`sympy.to_dnf` 提示、以及「只输出单行公式、不要解释」。

> 论文强调「示例数量不必多，但要尽量覆盖语法与意图的多样性」——这里三档示例正是按 easy/medium/hard 各写 5 条，`1-shot` 时只用第一条。

### 4.4 语法与语义校验器 `dataset/data_process_check.py`

**`format_check(result)`（38-83 行）—— 对应论文的 syntax checker + semantic checker：**

1. 先整体执行 `sympy.to_dnf(result, simplify=True)`；若抛异常 → 立即返回 `False, [异常信息, None, None, None]`，反馈提示为 `"It contains syntax errors or illegal characters."`；
2. 用正则 `r'[()&|~ ]'` 切出每个谓词 token，再按 `_` / `~` 拆成词表；
3. 逐个 token 检查：
   - 词数 ≤ 1 → `wrong_format_set`（格式错）；
   - 首词不在 `predicate_list`（8 个合法谓词）→ `wrong_predicate_set`（谓词错）；
   - 其余词不在 `object_list` → `wrong_object_set`（对象错）；
   - 若谓词在 `dic_pred_obj` 中（仅 `RobotNear` / `IsClean` / `Active` / `Closed` / `Low`）且对象不在该谓词的合法搭配里 → 记入 `wrong_format_set`；`On` / `Holding` / `Exists` 无搭配约束；
4. 三个错误集合全空才返回 `(True, None)`，否则返回 `(False, [None, 格式错集, 谓词错集, 对象错集])`。

> 注意：`object_list`（9-17 行）与 prompt 里的 `<items>/<place>` 词表**并不完全一致**（详见 §8），这是复现时最容易踩的坑。

**`goal_transfer_ls_set(goal)`（86-104 行）—— 对应论文的 Goal Normalization：**

```python
goal_dnf = str(to_dnf(goal, simplify=True))
for g in goal_dnf.split("|"):            # 每个析取项 = 一个子目标
    g = g.replace(" ", "").replace("(", "").replace(")", "").split("&")
    ...
    literal = "On(Coffee,Table2)"        # On_Coffee_Table2 的下游规划器写法
    literal = literal.replace('~', 'Not ')
```

返回 `list[set[str]]`：每个 set 是一个子目标的文字集合。

### 4.5 反馈纠错 `get_feedback_prompt()`（`intsr2goal_test_main.py:124-153`）

`error_black_set = [set(), set(), set()]` 在单条样本的所有轮次间**累积**，对应论文「gradually expanding the blacklists」。生成的提示形如：

```
[Syntax Blacklist] <历次非法 token>
[]Condition Predicate Blacklist] <历次非法谓词>
[Object Blacklist] <历次非法对象>

[Additional Promot]
1. Outputs including texts in the three blacklists are forbidden.
2. If a word from [Object Blacklist] is encountered, choose the closest parameter from the [Objects] table ...
3. If a word from [Condition Predicate Blacklist] is encountered, choose the closest parameter ...
4. Please generate directly interpretable predicate formulas without any additional explanations.
```

（第 144、146 行的 `[]Condition ...]` 与 `Promot` 是原脚本的拼写笔误，不影响功能。）

### 4.6 指标定义与统计口径

**GA-xF（Grammar Accuracy @ x Feedback）**：至多允许 x 轮反馈后，`format_check()` 判定为合法的样本比例。

**IA-xF（Interpretation Accuracy @ x Feedback）**：至多允许 x 轮反馈后，语义被判定正确的样本比例。

记账方式（`evaluate_section()`，167-223 行）：

| 第 f 轮输出 | 记入 `results` | 循环 |
|---|---|---|
| 语法合法 | 对 `f..5` 的 `GA-kF` 全部记 1；`IA-kF` 记 `1 if evaluate_answer(...) else 0` | `break` 退出 |
| 语法非法 | 仅 `GA-fF = 0`、`IA-fF = 0` | `f += 1` 继续 |

因此每个样本在每个指标上恰好贡献一个 0/1 值，**分母恒为样本数 N**（easy/medium 30，hard 40）；`np.mean` 后再对 5 次独立重复取平均，故 `result.txt` 的百分比分母是 150（easy/medium）或 200（hard）。

> **语法一通过就停止反馈**：论文明确 reflective feedback 只纠正语法/词表错误，语义错误不在纠错范围内，代码用 `break` 体现了这一点。代价是语法合法但语义错的样本，其 `IA-kF..IA-5F` 永远为 0。

**语义判定 `evaluate_answer()`（156-164 行）**：

```python
correct_answer_set = set(chain.from_iterable(goal_transfer_ls_set(correct_answer)))
user_answer_set    = set(chain.from_iterable(goal_transfer_ls_set(user_answer)))
return correct_answer_set <= user_answer_set      # 标准文字集合 ⊆ 输出文字集合
```

这是**宽松的集合覆盖判定**，而非论文文字所述的严格「等价」：

- 输出**多写**文字仍算对。`details_easy_shot=0_t=0.csv:2`：标准答案 `Exists_Coffee`，模型输出 `Exists_Coffee & RobotNear_CoffeeStation`，判定 `Content Correct=True`；
- `chain.from_iterable` 把 DNF 各析取项**展平**，忽略 OR 分支结构；`Not ` 前缀只是普通字符串，因此 OR / 否定结构错误可能被漏判为正确；
- 输出**缺**任一标准文字即判错。

**报告口径**：脚本计算 `GA/IA-0F..5F` 共 12 组，但只打印并汇总 `0F / 1F / 5F` 六个（303、325 行），论文 Table 1 的表头 `GA-NF / GA-1F / GA-5F / IA(%)` 与之对应（其中 `GA-NF` = `GA-0F`，IA 单列基本对应 `IA-5F`）。

### 4.7 主循环（`intsr2goal_test_main.py:227-334`）

| 配置项 | 值 | 位置 |
|---|---|---|
| 数据集文件 | `dataset/{easy,medium,hard}_instr_goal.txt` | 229-231 |
| `difficulties` | `["medium"]`，注释提示可扩成三档 | 253 |
| `num_examples` | `[0, 1, 5]` | 254 |
| `max_try_time` | `5`（独立重复次数） | 252 |
| 并发 | `ThreadPoolExecutor(max_workers=5)` | 286 |
| 样本切分 | `re.split(r'\n\s*\n', data_set)`（空行分隔） | 272 |
| CSV 名 | `details_{difficulty}_shot={num}_t={try_time}.csv` | 280 |
| 结果输出 | 仅 `print` 到 stdout | 310-317, 321-334 |

没有任何命令行参数解析；每次运行只跑一个难度，三档结果需要分别修改 `difficulties` 跑三次。`result.txt` 与 `log_*.txt` 是运行时终端重定向 / 事后人工归档的产物，脚本本身不写它们。

---

## 5. 评测数据集

### 5.1 格式

纯文本，**样本间用空行分隔**，每样本恰好两行：

```
Instruction: <英文自然语言指令>
Goal: <谓词逻辑公式>
```

与论文 §4.2 的 100 条评测集一一对应；**没有 train/val/test 划分**，全部 100 条都是评测样本，few-shot 示例硬编码在 `generate_prompt1()` 里、不取自这些文件。

### 5.2 难度分档

| 文件 | 条数 | 论文定义 | 目标公式特征 |
|---|---|---|---|
| `easy_instr_goal.txt` | 30 | 单个正文字 | 单原子谓词 |
| `medium_instr_goal.txt` | 30 | 两个文字用 ∨ 或 ∧ 连接 | 二元合取/析取 |
| `hard_instr_goal.txt` | 40 | 三个文字，含 ∨、∧、¬ | 嵌套括号、否定、多分支 |

样例原文：

```
# easy
Instruction: Please prepare some coffee.
Goal: Exists_Coffee

Instruction: Would you mind fetching my vacuum cup to the hydration area?
Goal: On_VacuumCup_WaterStation

# medium
Instruction: The chairs look a bit dirty, can you clean them up? If not, please deliver some yogurt to the coffee area.
Goal: IsClean_Chairs | On_Yogurt_CoffeeStation

Instruction: The floor seems a bit dusty, could you give it a good sweep? Also, I'd love a refreshing bottled beverage at Table 1 when you have a moment
Goal: IsClean_Floor & On_BottledDrink_Table1

# hard
Instruction: Please, don't forget to turn on the hall light. And, can you either deliver some dessert to Table 1 or bring water to Table 2?
Goal: (On_Dessert_Table1 | On_Water_Table2) & Active_HallLight

Instruction: Could you kindly deliver a coffee to Table 2? And while you're moving around, please avoid hanging around Tables 1 and 3.
Goal: On_Coffee_Table2 & ~(RobotNear_Table1 | RobotNear_Table3)
```

### 5.3 三个 prompt 文件的关系（易混淆）

| 文件 | 内容 | 是否生效 |
|---|---|---|
| `prompt_test.txt` | 完整的 `[Condition Predicates] + [Objects] + 5 示例 + [System] + 任务说明`，是 `prompt_test1.txt` 与 `prompt_test2.txt` 的合并版 | ❌ 脚本从不读取 |
| `prompt_test1.txt` | 上半部分；使用**旧谓词 `Dirty_`**（如 `~Dirty_Chairs`） | ⚠️ 读入赋给 `prompt1`（245-246 行）但**从未使用** |
| `prompt_test2.txt` | 5 条编号任务说明 | ✅ 实际拼到 `generate_prompt1(...)` 结果之后（283 行） |

真正生效的 prompt 全部来自 `generate_prompt1()`（用 `IsClean_`，且示例按难度分三套）+ `prompt_test2.txt`。`prompt_test*.txt` 是早期草稿，保留在归档中。

---

## 6. 输出文件与实验结果

### 6.1 文件命名与内容

`output_results/` 是 `difficulty(3) × shot(3) × t(5) = 45` 个 CSV 加日志和汇总：

| 文件 | 说明 |
|---|---|
| `details_{difficulty}_shot={0,1,5}_t={0..4}.csv` | 逐样本明细，每次重复 × 每个 shot 配置一份；easy/medium 各 30 条记录、hard 40 条 |
| `log_{easy,medium,hard}.txt` | 完整终端输出（约 2509 / 3823 / 5931 行），含每次模型原始输出、错误提示、着色 ANSI 码、逐轮指标 |
| `result.txt` | 三档难度 × 三种 shot 的 5 次重复平均指标，即论文 Table 1 的数据源 |

**CSV 共 17 列**（`init_csv()`，11-22 行）：

```
ID, Instruction, Correct Goal,
Model Output 1, Feedback Given 1,
Model Output 2, Feedback Given 2,
Model Output 3, Feedback Given 3,
Model Output 4, Feedback Given 4,
Model Output 5, Feedback Given 5,
Model Output 6,
Feedback Count, Grammar Correct, Content Correct
```

- `ID` = 样本在 `sections` 中的下标；因 5 线程并发写入，**行顺序是乱序**；
- `Instruction` 保留 `"Instruction: "` 前缀；`Correct Goal` 已去掉 `"Goal: "`；
- `Feedback Given i` 含换行，故 CSV 的**物理行数大于逻辑记录数**（用 `csv` 模块或 pandas 读取，不要按行 `split`）；
- `Feedback Count` = 实际用到的反馈轮数（0..5），`Grammar Correct` / `Content Correct` = 最后一次输出的布尔判定；
- GA/IA **不在 CSV 里**，只存在于日志与 `result.txt`。

### 6.2 归档结果（`output_results/result.txt`，5 次重复平均）

| 难度 | Few-shot | GA-0F | GA-1F | GA-5F | IA-0F | IA-1F | IA-5F |
|---|---|---|---|---|---|---|---|
| easy (30) | Zero-shot | 60.00% | 74.67% | 91.33% | 44.67% | 56.67% | 67.33% |
| easy | 1 | 87.33% | 95.33% | 100.00% | 74.00% | 80.67% | 85.33% |
| easy | 5 | 92.00% | 96.67% | 100.00% | 84.67% | 87.33% | 90.67% |
| medium (30) | Zero-shot | 50.00% | 66.00% | 88.00% | 32.67% | 44.67% | 57.33% |
| medium | 1 | 77.33% | 91.33% | 98.67% | 53.33% | 60.00% | 62.00% |
| medium | 5 | 92.67% | 94.67% | 99.33% | 76.67% | 78.67% | 82.00% |
| hard (40) | Zero-shot | 48.00% | 62.50% | 84.00% | 28.00% | 34.00% | 42.00% |
| hard | 1 | 76.50% | 87.50% | 93.00% | 45.00% | 48.50% | 51.00% |
| hard | 5 | 80.50% | 88.00% | 96.00% | 59.00% | 63.00% | 65.00% |

论文 Table 1 的三列 GA 与这些数据逐项吻合；IA 列基本对应 `IA-5F`（easy zero-shot 一处例外：论文为 56.7%，本地汇总为 67.33%，更接近 `IA-1F`，可能是 PDF 表格排版串位或不同运行批次）。

### 6.3 如何读这组数字

- **难度**：zero-shot 下 GA-0F 从 60.00% → 50.00% → 48.00%，IA-0F 从 44.67% → 32.67% → 28.00%，IA 下降更快，印证论文「逻辑语法易学、自然语言到意图的翻译更难」；
- **示例数消融**（固定反馈上限 5）：5-shot 相比 zero-shot，hard 的 IA-5F 从 42.00% 提升到 65.00%（+23pp）；而 1-shot 相对 zero-shot 的跃升最大（easy GA-0F 60.00% → 87.33%），印证「一个示例胜过一长段解释」；
- **反馈轮数消融**：GA 随允许轮数单调上升（zero-shot hard 48.00% → 62.50% → 84.00%）；IA 提升较小，因为反馈只纠正语法，语法合法但语义错的输出不再重试；
- **标准配置**（5-shot + 5 轮反馈）：GA-5F 达 easy 100.00% / medium 99.33% / hard 96.00%，IA-5F 达 90.67% / 82.00% / 65.00%。

> 这些数字是 `gpt-3.5-turbo`（2024.06）的历史运行结果，模型版本、API 默认采样参数与词表差异都会影响复现值。

---

## 7. 快速开始与复现

### 7.0 只想看结果（不需要 API Key）

直接阅读 `output_results/result.txt`、`log_*.txt`，或用 Python 读明细：

```python
import pandas as pd
df = pd.read_csv("output_results/details_medium_shot=5_t=0.csv")
print(df[["ID", "Instruction", "Correct Goal", "Model Output 1", "Feedback Count", "Grammar Correct", "Content Correct"]].head())
```

### 7.1 环境

Python 3.10（日志显示原环境为 conda `BTPG` + Python 3.10.14）。本目录已补 `requirements.txt`（仅列复现所需依赖，不是原实验环境的精确锁定版本）：

```bash
pip install -r requirements.txt
```

等价的手工安装：`pip install "openai>=1.0" sympy numpy`。

其余为标准库：`csv` / `re` / `concurrent.futures` / `itertools`。`pygame` 不是本 kit 的依赖。

### 7.2 修复包导入（必做）

入口脚本第 7-8 行写的是：

```python
from LLM.llms.gpt3 import LLMGPT3
from LLM.dataset.data_process_check import format_check, goal_transfer_ls_set
```

但目录名是 `LLM_Evaluation_Kit`，直接运行会报 `ModuleNotFoundError: No module named 'LLM'`。两种方案：

**方案 A（推荐，改动最小）**：把这两行改成本地导入，然后从 kit 根目录运行：

```python
from llms.gpt3 import LLMGPT3
from dataset.data_process_check import format_check, goal_transfer_ls_set
```

（`dataset/` 没有 `__init__.py`，靠 Python 3 命名空间包机制仍可导入。）

**方案 B（不改源码）**：在 `repro/` 下建立一个名为 `LLM` 的软链指向本目录，并让 `repro/` 进入 `PYTHONPATH`：

```bash
cd /path/to/RoboWaiter/repro
ln -s LLM_Evaluation_Kit LLM
cd LLM_Evaluation_Kit
PYTHONPATH=.. python intsr2goal_test_main.py
```

> 无论哪种方案，**工作目录必须是 kit 根目录**：所有数据集路径都是 `dataset/...` 相对路径（`229-237` 行），生成的 CSV 也写在 CWD，不会自动进 `output_results/`。

### 7.3 配置 API

`llms/gpt3.py:8-10` 目前是占位符：

```python
self.client = OpenAI(base_url="URL", api_key="Your-Key")
```

填入真实 endpoint 与 key；更安全的方式是删掉这两个参数、改由环境变量提供：

```bash
export OPENAI_API_KEY="..."
export OPENAI_BASE_URL="..."     # 使用兼容网关时才需要
```

仓库中**没有真实密钥**，`apis/gpt3.txt` 是空文件。

### 7.4 配置实验

修改 `intsr2goal_test_main.py:251-254`：

```python
max_try_time = 5                                # 独立重复次数
difficulties = ["easy"]                         # 每次只跑一档；三档需跑三次
num_examples = [0, 1, 5]                        # zero / 1 / 5-shot
```

### 7.5 运行与归档

```bash
cd /path/to/RoboWaiter/repro/LLM_Evaluation_Kit
python intsr2goal_test_main.py 2>&1 | tee output_results/log_easy_new.txt
# 从日志末尾的 "Average Results" 段整理出汇总表
```

> ⚠️ `details_*.csv` 由脚本写在 CWD 且**同名覆盖**，`log_*.txt` 也会被 `tee` 覆盖。上面的命令特意用了新日志名；若要把新结果放进 `output_results/`，请**先备份原有归档**（那是论文 Table 1 的原始证据），或另建一个输出目录。

**调用量与费用估算**：每条样本最多 6 次模型调用 × 3 种 shot × 5 次重复 = 90 次调用，故每档难度上限为 easy/medium 各 `30 × 90 = 2700` 次、hard `40 × 90 = 3600` 次请求（实际因语法通过即停止而少于上限）。5 线程并发，请注意网关限流与费用。

**不改变任何代码地「离线复跑」**：把 `llms/gpt3.py` 的 `request()` 换成从归档 CSV 中按 `ID` 回放 `Model Output i`，即可在不调用 API 的情况下验证 `format_check` / `evaluate_answer` / 指标计算逻辑。

---

## 8. 已知问题与注意事项

复现论文数字前请逐条核对，以下都是本快照的真实状态：

| # | 问题 | 位置 | 影响 / 建议 |
|---|---|---|---|
| 1 | **反馈文本没有真正回传给模型**：`messages` 在 `while` 循环体内每轮重建（188 行），190 行追加的 assistant 回复与 210 行追加的反馈提示在下一轮都被丢弃；每轮请求只包含原始 `prompt + question` | `intsr2goal_test_main.py:186-215` | 按当前脚本运行，「reflective feedback」退化为「重新采样」，`Feedback Given i` 虽被写进 CSV 却未影响模型。归档的 `result.txt` / `log_*.txt` 来自原工程脚本 `E:\worktable\MABTPG\...\gpt3_main_save_并行.py`（见日志首行），与本入口脚本并不完全一致。**要严格复现论文，需把反馈消息累积进下一轮 prompt。** |
| 2 | **导入路径与目录名不符** | `intsr2goal_test_main.py:7-8` | 见 §7.2 |
| 3 | **API 凭据是占位符**，模型名 `gpt-3.5-turbo` 硬编码，无 temperature 等采样参数 | `llms/gpt3.py:9, 13-16` | 见 §7.3；5 次重复的随机性依赖服务端默认采样 |
| 4 | **词表不一致**：校验器 `object_list` 与 prompt 的 `<items>/<place>` 不同（如 prompt 有 `Watermelon` / `CocountMilk` / `QuietTable7` / `YogurtDrink` / `Newspaper`，校验器没有；校验器多出 `OrangeJuice` / `CoconutMilk` / `QuietTable1/2`） | `data_process_check.py:9-17` vs `intsr2goal_test_main.py:70-71` | 模型严格按 prompt 生成某些合法词，会被 `format_check` 误判为语法错误，从而拉低 GA 并触发无谓反馈。复现前应对齐两份词表 |
| 5 | **谓词命名版本混杂**：论文与 `prompt_test*.txt` 用 `Dirty_` / `Activate`，主脚本 `generate_prompt1()` 与校验器用 `IsClean_` / `Active_`，数据集用 `IsClean_` / `Active_` | `prompt_test.txt:2,24`、`data_process_check.py:8` | `prompt_test*.txt` 是未生效的旧草稿，不要拿它当运行时的 prompt |
| 6 | **IA 判定比论文表述宽松**：子集覆盖 + 展平 DNF，非严格逻辑等价；输出多写文字仍算对 | `intsr2goal_test_main.py:156-164` | 解读 IA 时须注意；若要严谨，应逐析取项比较或用 `sympy` 判逻辑等价 |
| 7 | **语法通过即 `break`**，语义错误不再触发反馈 | `intsr2goal_test_main.py:199-204` | 与论文「只纠正语法错误」一致，但会使 IA 存在天花板 |
| 8 | **数据集词表与校验器也可能不匹配**：few-shot 示例里出现 `Exists_Yogurt`，而 `<makable>` 只含 Coffee/Water/Dessert；`On_Chips_WindowTable6` 等依赖词表覆盖 | `intsr2goal_test_main.py:87-106`、数据文件 | 若替换数据集，需同步扩充词表与 `dic_pred_obj` |
| 9 | **相对路径 + 相对 CWD 输出**：`dataset/...` 与 `details_*.csv` 都相对当前目录 | `intsr2goal_test_main.py:229-237, 280-281` | 必须从 kit 根目录运行，并手动把 CSV 归档进 `output_results/` |
| 10 | **CSV 行乱序 + 字段内嵌换行** | `init_csv` / `append_to_csv` 并发写入 | 用 `csv`/pandas 读取，不要按物理行数统计样本数 |
| 11 | **死代码 / 未用变量**：`test.txt`、`data100.txt` 引用了不存在的文件；`prompt1` 读入未用；`evaluate_section(..., csv_filename, ...)` 的参数未用；`llm` 是 `__main__` 内的全局变量 | `intsr2goal_test_main.py:233-246, 167, 251` | 不影响结果，但改造时容易误解 |
| 12 | **拼写笔误**：`diffculty`、`grean`、`[Additional Promot]`、`[]Condition Predicate Blacklist]`、脚本名 `intsr2goal` | 全文 | 无功能影响 |
| 13 | **无配置文件 / 无命令行参数** | `intsr2goal_test_main.py` | 已补 `requirements.txt` 列出依赖；实验配置仍靠改源码，建议后续补 `argparse` |
| 14 | **归档痕迹**：`apis/` 全空；原工程另有文心一言适配器但源码未随快照提供（其 `__pycache__/*.pyc` 编译缓存已在整理时清除）；`log_*.txt` 首行含原作者 Windows 绝对路径与 conda 环境名 | `apis/`、`output_results/log_*.txt:1-2` | 仅作来源说明，非敏感信息 |
| 15 | **版本控制**：本目录已移入 `repro/`，当前尚未纳入 git 跟踪；根 `.gitignore` 并未忽略它 | `repro/LLM_Evaluation_Kit/` | 归档前自行 `git add`，并确认 `apis/`、`llms/gpt3.py` 中无真实凭据 |

---

## 9. 扩展与二次开发

**换一个 LLM**：只需实现与 `LLMGPT3` 相同的接口 `request(message: list[dict]) -> str`，在 `__main__` 中替换 `llm = ...` 即可。论文强调方法 model-agnostic；若换成国产模型或本地模型，建议同时显式设置 `temperature=0` 并另行评估 5 次重复的必要性。

**换评测数据集**：按 §5.1 的两行格式 + 空行分隔添加样本，放回 `dataset/`，并同步：
1. `generate_prompt1()` 的 `[Objects]` / `[Condition Predicates]` 词表；
2. `data_process_check.py` 的 `predicate_list` / `object_list` / `dic_pred_obj`；
3. 每个难度对应的 few-shot 示例列表。

**更严谨的语义评估**：把 `evaluate_answer()` 改成对两个 `goal_transfer_ls_set()` 结果的双向逐析取项比较，或直接用 `sympy.simplify_logic(Equivalent(...))` 判定逻辑等价；同时可以增加 exact-match 指标，避免「多写文字算对」的高估。

**接上下游行为树规划**：`goal_transfer_ls_set()` 返回的 `list[set[str]]` 已是论文 Fig. 2 的 `Gsub`（每个集合是一个子目标的文字集，格式 `On(Coffee,Table2)` / `Not Active(AC)`）。在宿主仓库里，可把它作为 `core/agents/goal_provider.py` 中 `LLMGoalProvider._query_llm()` 的返回值（转成 `frozenset`），从而把「LLM 产 goal」接入决策层；注意宿主项目默认是 `StaticGoalProvider`，且两边目前没有任何 import 关系。

**修复反馈闭环**：把 `evaluate_section()` 的 `messages` 移到循环外，每轮把 `get_feedback_prompt()` 的结果作为新的 user message 追加进去（或把累积黑名单拼进 prompt），才能让本快照真正复现论文 §3.2 的 reflective feedback。

---

## 10. 引用

论文（本目录对应其 Stage 1 / §3.2 / §4.2 / Table 1）：

```bibtex
@article{chen2024integrating,
  title   = {Integrating Intent Understanding and Optimal Behavior Planning for Behavior Tree Generation from Human Instructions},
  author  = {Chen, Xinglin and Cai, Yishuai and Mao, Yunxin and Li, Minglong and Yang, Wenjing and Xu, Weixia and Wang, Ji},
  journal = {arXiv preprint arXiv:2405.07474},
  year    = {2024}
}
```

- arXiv: https://arxiv.org/abs/2405.07474
- 项目主页: https://dids-ei.github.io/Project/LLM-OBTEA/
- 论文 §4.2 使用模型：`gpt-3.5-turbo`（2024.06 版本）
- 原始工程位置（见日志首行）：`MABTPG/mabtpg/algo/llm_client/intsr2goal_test/`
