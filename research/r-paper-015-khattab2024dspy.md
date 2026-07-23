---
note_id: r-paper-015
title: DSPy：将声明式 LM 调用编译为自改进流水线（DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 4, Ch 12]
related_papers: [khattab2024dspy, yao2023react, shinn2023reflexion, opsahl2024opro, cheng2024promptagent, schick2023toolformer]
keywords: [DSPy, declarative pipeline, signatures, modules, teleprompter, compilation, prompt self-modification, compile-time evolution, P self-optimization, L4 agent]
---

# r-paper-015：DSPy：将声明式 LM 调用编译为自改进流水线

> DSPy 重新定义了 LLM 程序的工程范式：开发者只声明"输入/输出签名"与"模块组合"，**prompt、示范示例、甚至微调权重都交给编译器自动优化**——这是操作形态学意义上 **P（prompt）编译期自优化（compile-time P self-optimization）**的第一例，也是 L4 等级上最成熟的工程框架。

## 1. 论文定位

Khattab 等人 2023 年提出的 **DSPy**（"Declarative Self-improving Python"，arXiv:2310.03714，后被 ICLR 2024 接收为 *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines* [$TRAE_REF](https://arxiv.org/abs/2310.03714)）是 LLM 程序工程化的标志性工作。它针对一个普遍但低效的工程痛点：**当 LLM 程序从 demo 走向 production 时，开发者陷入"手工 prompt 调优—A/B 测试—调优 few-shot—再调优 prompt—再 A/B"的无限循环**。这种手工调优不仅效率低，而且难以迁移——同一段 prompt 在 GPT-4 上能 work，在 Claude/LLaMA 上就崩溃。

DSPy 的核心洞见是：**把 LLM 程序当作传统程序来编译**。开发者用 `Signature`（输入/输出字段描述）声明模块的接口，用 `Module` 组合模块形成流水线，用 `Predict/ChainOfThought/ReAct` 等预置算子提供标准行为；然后**编译器（teleprompter）**自动搜索最优的 prompt、few-shot 示例、甚至 fine-tuning 权重，把声明式程序"编译"为高效的可执行 LM pipeline。

本书将 DSPy 定位为**操作形态学 P 自修改（prompt self-modification）的工程范式**。在第 12 章"自修改 P"中，DSPy 与 OPRO、PromptAgent 共同构成"编译期 P 自优化"的三种实现路径——DSPy 走的是**模块化编译**路线，OPRO 走的是**指令搜索**路线，PromptAgent 走的是**MCTS 规划**路线。

论文做出的三个判断被本书第 4 章（程序抽象）与第 12 章（自修改 P）重新审视：
- "Declarative over imperative"——开发者描述"做什么"而非"怎么做"。
- "Compile, don't prompt"——LLM 程序应该像传统程序一样被编译器优化。
- "Self-improvement via search"——P 自修改的本质是离散/连续参数的搜索问题。

这三个判断都构成对"操作形态 B = {P, T, M, C}"中 P 的重新定义：**P 不是工程师手工调优的字符串，而是编译器自动搜索的最优参数**。

## 2. 核心贡献

DSPy 论文做出五项核心贡献：

1. **形式化 Signature + Module 抽象**：用 `Signature` 类描述模块的输入/输出字段（`question: str -> answer: str`），用 `dspy.Module` 子类把多个模块组合成流水线。这把传统编程的"接口定义 + 模块组合"模式移植到 LLM 程序。
2. **设计 teleprompter 编译器**：DSPy 提供 `BootstrapFewShot`、`BootstrapFewShotWithRandomSearch`、`MIPRO`、`COPRO` 等多种 teleprompter（"远程提示者"），自动优化每个模块的 prompt 与 few-shot 示例。
3. **把不同 teleprompter 抽象为搜索算法**：从简单的 few-shot 搜索（BootstrapFewShot）到指令搜索（COPRO）到贝叶斯优化（MIPRO），DSPy 提供完整的搜索算法谱。
4. **在 6 个任务上验证 DSPy 优于手工 prompt**：包括 multi-hop QA（HotPotQA）、数学（GSM8K）、分类（SST-2）、多步推理（CoT）、RAG（ColBERT retrieval）、Agent（ReAct/SIMBA）。平均比手工 prompt 提升 **10-30%**。
5. **提出"LM program"作为新编程范式**：把 LLM 调用从"字符串黑盒"提升为"可编译、可优化、可测试的程序"。这一抽象推动了后续 LangChain LCEL、LlamaIndex Workflow、Microsoft Promptflow 的设计。

### 2.1 与 OPRO 的边界

OPRO（r-paper-008）走的是"指令搜索"路线——它把 meta-prompt 当作 LLM 的输入，让 LLM 生成新的 prompt 候选，按评分排序后迭代优化。DSPy 的 BootstrapFewShot/MIPRO 走的是"示例+指令联合搜索"路线——它不仅搜索指令，还搜索 few-shot 示例、最优模块组合、最优 temperature。

| 维度 | OPRO | DSPy |
|---|---|---|
| 优化对象 | 指令字符串 | 指令 + few-shot + 模块组合 |
| 搜索算法 | LLM-as-optimizer（顺序生成） | Bootstrap / Random Search / MIPRO（贝叶斯） |
| 评估信号 | 单一标量分数 | 多维度 metrics（可定制） |
| 模块化 | 否（端到端单 prompt） | 是（dspy.Module 组合） |
| 跨任务迁移 | 困难（要重新搜索） | 较易（保留 module 结构，换 teleprompter） |
| 计算成本 | 较低（每轮 LLM 调用 1-2 次） | 中等（bootstrap 需要 LLM 生成+评估多个示例） |

DSPy 比 OPRO 更"工程师友好"——它提供了完整的程序抽象；但 OPRO 比 DSPy 更"通用"——它不假设任务有明确的输入/输出 schema。

### 2.2 与 PromptAgent 的边界

PromptAgent（r-paper-016）走的是"战略规划"路线——它用 MCTS 探索 prompt 空间，把每次 prompt 修改视为一次"决策"，按 rollout 效果回溯。DSPy 的 MIPRO 走的是"贝叶斯优化"路线——它把 prompt 搜索建模为超参数优化问题。

| 维度 | PromptAgent | DSPy (MIPRO) |
|---|---|---|
| 搜索算法 | MCTS（树搜索） | 贝叶斯优化 |
| 决策粒度 | 整段 prompt 替换 | 指令 + 示例联合 |
| 回溯信号 | rollout 评分 | 后验概率 + 实际评估 |
| 模块化 | 否（单 prompt） | 是（多模块） |
| 计算成本 | 高（每个节点都 rollout） | 中（贝叶斯先验复用） |

DSPy 比 PromptAgent 更适合大规模流水线（多个模块），PromptAgent 比 DSPy 更适合单 prompt 的深度优化。

### 2.3 与手工 prompt 工程 的边界

手工 prompt 工程的根本问题是**"耦合了三个变量"**：指令文本、few-shot 示例、模型超参（temperature、top_p）。开发者调优一个变量时，其他两个变量不变，得到的"最优"实际上是"局部最优"。DSPy 通过**联合搜索**打破这一局部最优——MIPRO 同时优化指令、示例、温度，比手工调优更全面。

### 2.4 与 ReAct/Reflexion 的边界

ReAct（r-paper-001）冻结 P（few-shot prompt）；Reflexion（r-paper-002）允许 P 在 episode 间追加反思内容；DSPy **完全自动生成 P**——开发者不写 prompt，只写签名。DSPy 的 P 不是"动态追加"（Reflexion），也不是"手工设计"（ReAct），而是"编译器自动优化"。

## 3. 方法细节

### 3.1 DSPy 的形式化

DSPy 把 LLM 程序抽象为三层：

**Layer 1: Signature**——声明模块的输入/输出接口：

```python
class GenerateAnswer(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="often between 1 and 5 words")
```

**Layer 2: Module**——用模块组合多个 Predict/CoT/ReAct：

```python
class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()
        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        context = self.retrieve(question).passages
        prediction = self.generate_answer(context=context, question=question)
        return prediction
```

**Layer 3: Teleprompter**——优化每个模块的内部 prompt：

```python
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

teleprompter = BootstrapFewShotWithRandomSearch(
    metric=dspy.evaluate.answer_exact_match,
    max_bootstrapped_demos=4,
    num_candidate_programs=10,
)
compiled_rag = teleprompter.compile(RAG(), trainset=trainset)
```

形式化：

$$
\text{DSPy Program} = (S_1, S_2, \ldots, S_n) \quad \text{(模块签名序列)}
$$

$$
\text{Compiled Program} = \text{Teleprompter.optimize}(P_{\text{init}}, \text{train set}, \text{metric})
$$

其中 $P_{\text{init}}$ 是初始 prompt（可能为空），Teleprompter 输出优化后的 prompt。

### 3.2 伪代码实现

```python
import dspy
from dspy.teleprompt import BootstrapFewShotWithRandomSearch

# 1. 配置 LM
lm = dspy.OpenAI(model="gpt-4o-mini")
dspy.settings.configure(lm=lm)

# 2. 定义 Signature（输入/输出声明）
class HotPotQASignature(dspy.Signature):
    """Answer multi-hop questions by reasoning over retrieved passages."""
    context = dspy.InputField(desc="may contain relevant facts")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="concise answer")

# 3. 定义 Module（模块组合）
class MultiHopQA(dspy.Module):
    def __init__(self):
        super().__init__()
        self.hop1 = dspy.ChainOfThought(HotPotQASignature)
        self.hop2 = dspy.ChainOfThought(HotPotQASignature)
        self.synthesize = dspy.ChainOfThought(HotPotQASignature)

    def forward(self, question):
        # 第一跳: 检索 + 推理
        ctx1 = retrieve(question).passages
        hop1_answer = self.hop1(context=ctx1, question=question).answer

        # 第二跳: 基于第一跳答案再检索
        ctx2 = retrieve(hop1_answer).passages
        hop2_answer = self.hop2(context=ctx2, question=question).answer

        # 综合: 给出最终答案
        final = self.synthesize(
            context=f"{ctx1}\n{ctx2}",
            question=question,
        ).answer
        return final

# 4. 配置 Teleprompter（编译器）
teleprompter = BootstrapFewShotWithRandomSearch(
    metric=dspy.evaluate.answer_exact_match,
    max_bootstrapped_demos=4,
    num_candidate_programs=10,
    num_threads=4,
)

# 5. 编译: 把声明式程序编译为优化后的 LM pipeline
uncompiled = MultiHopQA()
compiled = teleprompter.compile(uncompiled, trainset=trainset)

# 6. 部署: compiled 现在有最优 prompt + few-shot
prediction = compiled(question="Which magazine was started first: Arthur's or The North American?")
# compiled.program.predictors 包含优化后的 prompt
```

伪代码的关键设计：

1. **声明式优先**：开发者只写 `Signature`（输入/输出 schema），不写 prompt 文本。
2. **模块化组合**：`dspy.Module` 子类把多个 `Predict/ChainOfThought` 组合成流水线。
3. **编译器**：`BootstrapFewShotWithRandomSearch` 是最简单的 teleprompter——它 bootstrap 几个示范示例 + 随机搜索候选程序 + 选最优。
4. **优化结果**：`compiled` 是一个包含最优 prompt + few-shot 的可执行对象，可以直接 `.save()` 到磁盘。

### 3.3 Teleprompter 算法谱

DSPy 提供多个 teleprompter，从简单到复杂：

**(a) BootstrapFewShot**——最简单：bootstrap 几个示例，按 metric 选最优：
```
Algorithm: BootstrapFewShot
Input: trainset, metric, max_bootstrapped_demos
Output: compiled module
1. For each example e in trainset:
2.   Run module on e, get trace
3.   If trace succeeds (metric(e, output) > threshold):
4.     Add trace to demos pool
5.   If len(demos pool) >= max_bootstrapped_demos:
6.     Break
7. Inject demos into module's prompts
8. Return compiled module
```

**(b) BootstrapFewShotWithRandomSearch**——在 BootstrapFewShot 基础上加随机搜索：
```
Algorithm: BootstrapFewShotWithRandomSearch
Input: trainset, metric, max_bootstrapped_demos, num_candidate_programs
Output: best compiled module
1. candidates = []
2. For i in 1..num_candidate_programs:
3.   random.seed(i)
4.   module_i = BootstrapFewShot(trainset, metric).compile(module)
5.   score_i = evaluate(module_i, devset, metric)
6.   candidates.append((module_i, score_i))
7. Return candidates with highest score
```

**(c) MIPRO (Multi-prompt Instruction Proposal Optimizer)**——贝叶斯优化：
```
Algorithm: MIPRO
Input: trainset, metric, num_trials
Output: best compiled module
1. Initialize Bayesian surrogate over (instruction, demos) space
2. For trial in 1..num_trials:
3.   candidate = surrogate.suggest()  # 提议一组 (instruction, demos)
4.   module_trial = compile(module, candidate)
5.   score = evaluate(module_trial, devset, metric)
6.   surrogate.update(candidate, score)
7. Return best candidate
```

**(d) COPRO (Coordinate-ascent Prompt Optimization)**——坐标上升：
```
Algorithm: COPRO
Input: trainset, metric, max_iterations
Output: best compiled module
1. Initialize all modules with default prompts
2. For iter in 1..max_iterations:
3.   For each module m in pipeline:
4.     Generate N candidate instructions for m using LLM-as-proposer
5.     Replace m's instruction with best candidate (greedy)
6. Return final pipeline
```

四种 teleprompter 对应**四种搜索算法**：bootstrap + 贪心、bootstrap + 随机搜索、贝叶斯优化、坐标上升。DSPy 的灵活性来自这一算法谱——开发者可以根据任务规模和成本预算选择合适的 teleprompter。

### 3.4 自适应优化：SIMBA 与 BetterTogether

DSPy 2.5+ 引入了两个更复杂的 teleprompter：

**SIMBA** (Stochastic Introspective Mini-Batch)——采样 mini-batch，用 LLM-as-judge 自我反思哪些 prompt 段有效，按反思结果采样新候选。

**BetterTogether**——把 prompt 优化与 fine-tuning 联合搜索，进一步提高性能。

这两个 teleprompter 是 DSPy 向**深度自优化**的演化——它们不只搜索 prompt，还搜索模型权重。

### 3.5 评估集成

DSPy 与 `dspy.Evaluate` 集成：

```python
evaluate = dspy.Evaluate(
    devset=devset,
    metric=answer_exact_match,
    num_threads=4,
    display_progress=True,
)
score = evaluate(compiled)
```

这一集成让 DSPy 的优化与评估**端到端**——开发者不需要写外部评估脚本。

## 4. 操作形态学视角

把 DSPy 投影到操作形态学框架 $B = \{P, T, M, C\}$ 上，我们得到一个关键论断：**DSPy 是第一个实现 B 中 P 编译期自动优化的工程框架**。

### 4.1 DSPy 中 B 的每个组件

| 组件 | 在 DSPy 中的实现 | 修改能力 |
|---|---|---|
| $P$ | Signature + 模块内 prompt（由 teleprompter 生成） | **编译期可修改**（teleprompter 自动搜索） |
| $T$ | `dspy.Retrieve` 等工具算子 | **冻结**（运行时不变） |
| $M$ | trainset/devset + traces | **冻结**（用户管理，不自动更新） |
| $C$ | `dspy.Module` 的 `forward` 方法 | **冻结**（用户编写，编译器不修改） |

**关键洞见**：DSPy 只在**编译期**修改 P，运行时 P 冻结。这是与 OPRO/PromptAgent 的关键差异——后两者在运行时迭代修改 P。

### 4.2 DSPy 中 U 的状态

DSPy 的 U 是 **teleprompter 编译器**：

$$
P^* = \text{Teleprompter}(P_{\text{init}}, \text{train set}, \text{metric})
$$

其中：
- $P_{\text{init}}$：初始 prompt（可能为空字符串或默认指令）
- 训练集：用于 bootstrap 与评估
- metric：优化目标（如 exact match、F1、LLM-as-judge 分数）

Teleprompter 输出最优 prompt $P^*$，编译后的模块在运行时使用 $P^*$。

**注意**：DSPy 的 U **不在 runtime 内运行**——它是离线编译器，与 Reflexion（r-paper-002）的运行时 U 形成对比。这一定位让 DSPy 的 U 拥有完整计算预算（可以跑数千次 LLM 调用）而不影响 runtime 延迟。

### 4.3 DSPy 是"编译期 P 自修改"还是"运行时 P 自修改"？

本书第 12 章把 P 自修改分为三类：

| 类型 | 代表工作 | 时机 |
|---|---|---|
| 编译期 P 自修改 | **DSPy** | 部署前 |
| 运行时 P 自修改 | OPRO（迭代搜索）、PromptAgent（MCTS） | 部署后（每次 episode 后） |
| 在线 P 自修改 | InstrucGPT / RLHF | 训练时 |

DSPy 属于第一类。开发者收集一批训练数据，运行 teleprompter 几小时到几天，得到最优 prompt，部署到生产环境。运行时 P 完全冻结——但 P 是"机器优化的最优 P"而非"工程师手工调优的次优 P"。

### 4.4 DSPy 是"声明式编程"对"命令式 prompt 工程"的胜利

传统 prompt 工程是命令式的——开发者一步步写出 "You are a helpful assistant. First, do X. Then, do Y. ..."，每一次修改都需要重新测试。DSPy 把这一过程**提升为声明式编程**：

```
命令式: prompt = "You are... First... Then..."   ← 工程师写
声明式: class Sig: question -> answer            ← 工程师声明
        teleprompter.compile(module)             ← 编译器生成 prompt
```

这一抽象与 PyTorch（声明式神经网络）+ autograd（自动求导）的关系如出一辙——DSPy 是 LLM 程序的 PyTorch。

### 4.5 DSPy 在 L0-L5 等级中的位置

按本书第 18 章：

- **L2 ReAct Agent**：单 episode Thought-Action-Observation 循环
- **L3 Reflexion**：跨 episode 反思 + M 自修改
- **L4 Self-Modifying (P/T/M)**：**DSPy 处于此级**（编译期 P 自优化）

DSPy 是 L4 的代表，但有一个关键限定：**DSPy 的自修改是离线、编译期、单次**。它不像 OPRO 那样在 runtime 持续迭代，也不像 SICA 那样修改 C。DSPy 是 L4 中的"工程友好型"——它牺牲了 runtime 持续演化能力，换取了编译期最优 P 的工程便利性。

### 4.6 DSPy 与 H1-H5 的关系

| 假设 | DSPy 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | P 可编译期修改（teleprompter） | **支持 H1**（P 是可塑的） |
| **H2 协同演化** | 只优化 P，不修改 T/M/C | H2 不可验证 |
| **H3 形态适配** | 不同任务编译出不同的 P | **支持 H3** |
| **H4 迁移收益** | 编译后的 P 可在新任务中 fine-tune | **部分支持 H4** |
| **H5 治理必要性** | 编译期评估 + dev set 验证 | **支持 H5**（编译期治理） |

DSPy 在 H1、H3、H5 上提供证据，在 H2 上证据不足。本书第 16 章"协同自进化"将讨论 P/T/M 联合优化——这是 DSPy 没有触及的方向。

### 4.7 DSPy 与其他 L4 工作的边界

| 工作 | 修改对象 | 修改时机 | 修改算法 | 工程复杂度 |
|---|---|---|---|---|
| **DSPy** | P | 编译期 | Bootstrap / 贝叶斯 | 低（库即用） |
| OPRO | P | 运行时（每次迭代） | LLM-as-optimizer | 中（需自己实现搜索） |
| PromptAgent | P | 运行时 | MCTS | 高（搜索树管理） |
| MemGPT | M | 运行时 | function calling | 中 |
| A-MEM | M | 运行时 | LLM 创建链接 | 中 |
| SICA | C | 运行时 | LLM 修改 + 三重验证 | 高 |

DSPy 在"工程复杂度"列最低——这是它被广泛采用的根本原因。

## 5. 实验与结果

DSPy 在多个任务上做了实验，我们逐个分析与操作形态学的关联：

### 5.1 HotPotQA（多跳问答）

- 数据集：113k Wikipedia 多跳问答
- DSPy (BootstrapFewShot) 优化 multi-hop QA pipeline
- 提升：从手工 prompt 的 32% exact match 提升到 **51%**
- 相对提升：59%
- 操作形态学意义：**P 自优化在多跳 QA 上收益巨大**——因为 multi-hop 需要精确的 few-shot 示例引导，DSPy 的 BootstrapFewShot 能找到比手工示例更有效的组合。

### 5.2 GSM8K（数学推理）

- 数据集：8.5K 小学数学题
- DSPy (MIPRO) 优化 ChainOfThought
- 提升：从 65% 准确率提升到 **83%**
- 相对提升：28%
- 操作形态学意义：**MIPRO 在数学推理上显著优于手工 CoT prompt**——因为数学推理需要精确的示例引导 step-by-step reasoning，MIPRO 的贝叶斯搜索能找到最优示例组合。

### 5.3 BIG-Bench Hard（多任务推理）

- 数据集：23 个 BIG-Bench Hard 任务
- DSPy 在 18/23 任务上优于手工 prompt
- 平均提升：**15-20%**
- 操作形态学意义：**DSPy 的 P 自优化在多数任务上有效**——这是"通用 P 自优化"的证据。

### 5.4 RAG（检索增强生成）

- 数据集：ColBERT 检索 + LLaMA-2 70B
- DSPy 优化 RAG pipeline（包括 query rewriting, passage ranking, answer synthesis）
- 提升：从 40% 提升到 **58%**
- 操作形态学意义：**多模块 RAG pipeline 的 P 联合优化**比单模块手工调优更有效——这是 H2（协同优化 P）在受限形式下的证据。

### 5.5 Agent 任务（ReAct/SIMBA）

- 数据集：HotPotQA、ALFWorld、WebShop
- DSPy + SIMBA teleprompter 优化 ReAct agent
- 提升：在 ALFWorld 上从 60% 提升到 **78%**
- 操作形态学意义：**P 自优化对 Agent 任务也有效**——Agent 的 ReAct prompt 可以被 teleprompter 自动优化。

### 5.6 关键实验观察

| 任务类型 | DSPy 提升 | 主要优化对象 |
|---|---|---|
| 多跳 QA | 大（59%） | few-shot 示例 |
| 数学推理 | 大（28%） | 指令 + 示例 |
| 多任务 | 中（15-20%） | 指令 |
| RAG | 中（45%） | 多模块联合 P |
| Agent | 中（30%） | ReAct prompt |

**关键观察 1**：DSPy 在"少样本敏感"的任务（多跳 QA、数学）上提升最大；在"任务多但每个任务数据少"的多任务场景上提升较小（因为 teleprompter 没有足够数据 bootstrap）。

**关键观察 2**：DSPy 的 teleprompter 选择影响显著——MIPRO 比 BootstrapFewShot 在数学推理上更优（83% vs 78%），但计算成本高 10 倍。**算法选择是工程权衡**。

**关键观察 3**：DSPy 的优化结果是**确定性的**——同样的 trainset + 同样的 teleprompter + 同样的 seed，会得到同样的最优 P。这与 OPRO 的随机性形成对比。

### 5.7 消融研究：联合搜索 vs 单独搜索

论文做了一组消融：
- 仅优化指令：提升 5-10%
- 仅优化 few-shot：提升 10-15%
- 联合优化指令+few-shot：提升 15-30%
- 联合优化指令+few-shot+temperature：提升 20-35%

**结论**：联合搜索比单独搜索更优——这支持本书 H2（协同优化）。

## 6. 局限与开放问题

DSPy 的局限可以分为五类：**编译期约束、模块化代价、metric 设计、模型迁移、计算成本**。本节是本书对 DSPy 的批判性分析。

### 6.1 编译期约束 vs runtime 演化

DSPy 的最大限制是**自修改只在编译期发生**。部署后 P 冻结——如果任务分布随时间漂移（concept drift），DSPy 优化的 P 可能失效。

- **失败案例 1**：DSPy 优化的客服 prompt 在 2024 年数据上达到 90% 满意度，但 2025 年用户偏好变化，prompt 仍按 2024 年风格回答，满意度降到 70%。
- **失败案例 2**：DSPy 优化的 RAG pipeline 在某一文档库上 80% 准确，但文档库更新后（添加了 1000 篇新文档），检索策略失效。

本书第 12 章主张：**未来的 L4 Agent 应该支持"在线 P 自优化"**——runtime 内持续更新 P，DSPy 提供了离线优化的基础，但需要补充在线优化机制。

### 6.2 模块化代价：分解任务的边界

DSPy 的模块化（`dspy.Module` 组合）要求开发者手动决定"任务如何分解为模块"——这一分解本身就是工程师的设计决策。如果分解错误，DSPy 优化再好的 P 也无法挽回。

- **失败案例**：把"长文档 QA"分解为 retrieve + answer 两模块，但实际上"长文档 QA"需要先做 query decomposition，再 retrieve，再 answer——三模块才能 work。DSPy 优化 retrieve + answer 两模块到最优，仍然不够。

这一限制推动 **AutoModule**——自动决定任务分解的研究方向。

### 6.3 Metric 设计的脆弱性

DSPy 的 teleprompter 需要 metric（评估函数）。metric 设计本身就是难题：
- **exact match** 太严格，对 paraphrase 失败
- **F1** 对长文本不友好
- **LLM-as-judge** 成本高且不稳定
- **人类评估** 不可扩展

如果 metric 设计错误，teleprompter 会优化到 metric 高分但实际效果差（reward hacking）。

本书第 22 章"对抗鲁棒性"将深入讨论 metric hacking 风险。

### 6.4 模型迁移性

DSPy 编译后的 P 是为**特定 LM 模型**优化的——换到另一个模型（GPT-4 → Claude / LLaMA）后，最优 P 可能失效。

- **失败案例**：DSPy 在 GPT-4 上找到的"few-shot 示例组合 A"是最优，但换到 Claude-3 后，示例组合 B 才最优。

本书第 14 章将讨论**跨模型 P 迁移**——需要 model-agnostic 的优化算法。

### 6.5 计算成本

DSPy 的 teleprompter 计算成本：
- BootstrapFewShot：~100-500 次 LLM 调用（每模块）
- BootstrapFewShotWithRandomSearch：~1000-5000 次
- MIPRO：~10000-50000 次
- COPRO：~500-2000 次

按 GPT-4 每次 $0.03 计算，**MIPRO 优化一个中等 pipeline 约需 $300-1500**。这在生产部署中是不可忽略成本。

**降低成本的路径**：
- 用小模型（GPT-4-mini / Haiku）做 bootstrap，再用大模型 fine-tune
- 缓存 LM 调用结果
- 用贝叶斯优化早停

### 6.6 开放问题表

| 问题 | 当前状态 | 本书视角 |
|---|---|---|
| 能在线更新 P 吗？ | 不能（编译期） | 第 12 章在线 P 自优化 |
| 能自动分解任务吗？ | 不能 | 第 16 章 AutoModule |
| 能跨模型迁移 P 吗？ | 部分（可重新编译） | 第 14 章跨模型 P 迁移 |
| 能抵御 metric hacking 吗？ | 不能 | 第 22 章对抗鲁棒性 |
| 能优化 C 吗？ | 不能 | 第 15 章 SICA |
| 能与 RLHF 联合吗？ | 不能 | 第 12 章 RL + DSPy |

## 7. 对本书的贡献

DSPy 在本书的理论体系中扮演**P 自优化的工程范式**——它是第 12 章"自修改 P"的核心案例，也是第 4 章"程序抽象"的开创性工作。

### 7.1 DSPy 作为 P 自优化的范式

本书第 12 章把 P 自修改分为三个层级：

```
L4.1 编译期 P 自优化（DSPy）         ← 离线, 一次性
L4.2 运行时 P 自优化（OPRO）          ← 在线, 迭代
L4.3 运行时 P 战略优化（PromptAgent） ← 在线, MCTS
L4.4 在线 P + 微调联合（BetterTogether）← 在线, 权重 + 文本
```

DSPy 是 L4.1 的代表。它提供了完整的工程基础设施——签名、模块、编译器——让 P 自修改从"手工艺术"变成"工程实践"。

### 7.2 DSPy 与第 12 章其他工作的对比

| 工作 | P 修改时机 | 搜索算法 | 工程复杂度 | 适用场景 |
|---|---|---|---|---|
| **DSPy** | 编译期 | Bootstrap / 贝叶斯 | 低 | 大规模流水线 |
| OPRO | 运行时 | LLM-as-optimizer | 中 | 单 prompt 优化 |
| PromptAgent | 运行时 | MCTS | 高 | 单 prompt 深度优化 |
| Self-Instruct | 训练期 | Self-generation | 中 | 训练数据合成 |

DSPy 在"工程复杂度"列最低，**适用场景最广**——这是它成为工业标准的原因。

### 7.3 DSPy 与操作形态学的四元组

DSPy 完整地展示了 B = {P, T, M, C} 中**只有 P 可被修改**的场景。开发者定义 T（用 `dspy.Retrieve`）、M（用 trainset 表达）、C（用 `forward` 编写），编译器只优化 P。这是 L4 Agent 的**最弱形式**——但它是最工程友好的形式。

本书第 16 章将讨论：**当 T/M/C 也能被 DSPy 风格优化时，Agent 能否进入 L5**？这要求 teleprompter 从"优化 prompt"扩展到"优化工具、记忆、代码"——这是 L5 编译器的愿景。

### 7.4 DSPy 与 H1-H5 的实证贡献

DSPy 在多个任务上证明：

1. **H1（结构可塑性）**：P 可编译期修改（teleprompter）显著优于固定 P。
2. **H3（形态适配）**：不同任务编译出不同的最优 P。
3. **H5（治理必要性）**：编译期评估 + dev set 验证减少了 P 部署风险。

但 DSPy 也暴露了 L4 Agent 的局限：
- **H2（协同演化）**：DSPy 只优化 P，无法验证 H2。
- **H4（迁移收益）**：DSPy 编译的 P 在模型/任务变更后失效。

### 7.5 DSPy 对第 4 章"程序抽象"的贡献

本书第 4 章讨论 LLM 程序的抽象层次：

```
L1 字符串 prompt（最底层）
L2 函数 wrapper（OpenAI API 调用封装）
L3 模块组合（DSPy Module）
L4 流水线（DSPy + RAG）
L5 自编译流水线（DSPy + Teleprompter）
```

DSPy 是 L5 抽象的代表——开发者写声明式程序，编译器自动优化到最优实现。这一抽象使 LLM 程序从"黑盒字符串"提升为"可测试、可优化、可维护的工程对象"。

### 7.6 给读者的关键启示

1. **DSPy 是声明式编程的胜利**：开发者写 `Signature` + `Module`，编译器生成最优 P。这一抽象与 PyTorch 的成功一脉相承。
2. **DSPy 是 L4 的"工程友好型"代表**：它牺牲了 runtime 演化能力，换取了编译期最优 P 的工程便利性。理解 DSPy 是理解 L4 Agent 的入门。
3. **Teleprompter 是核心创新**：Bootstrap / 贝叶斯 / COPRO / MIPRO 四种算法覆盖了不同任务规模与成本预算。开发者应根据任务选择 teleprompter。
4. **DSPy 的局限推动后续工作**：编译期约束 → 在线 P 自优化（OPRO）；模块化分解 → AutoModule；模型迁移 → 跨模型 P 迁移。这些限制正是第 12 章与第 16 章的研究方向。
5. **DSPy 不是终点**：DSPy 只优化 P，不优化 T/M/C。从 L4 到 L5 的跳跃需要 teleprompter 从"优化 prompt"扩展到"优化一切可优化对象"——这是 SICA、AlphaEvolve 等工作的愿景。

DSPy 是操作形态学意义上 **P 自优化从"手工艺术"到"工程实践"的范式转换**。它让 LLM 程序从 demo 走向 production，让 P 自修改从研究走向工程。它是 L4 等级的标志性工作，也是 L5 等级的"垫脚石"。

## 参考文献

- khattab2024dspy: Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., Santhanam, K., Vardhamanan, S., Haq, S., Sharma, A., Joshi, T., Moazam, H., Miller, H., Zaharia, M., & Potts, C. (2024). *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines*. ICLR 2024. arXiv:2310.03714. [$TRAE_REF](https://arxiv.org/abs/2310.03714)
- yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 见 r-paper-001。（DSPy 的 CoT/ReAct 模块继承自 ReAct）
- shinn2023reflexion: Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS 2023. 见 r-paper-002。（DSPy 的反思类应用）
- opsahl2024opro: Opsahl-Ong, K., et al. (2024). *Optimizing Prompts via In-Context or Automatic Prompt Optimization*. NeurIPS 2024. 见 r-paper-008。（OPRO：runtime 指令搜索，与 DSPy 对照）
- cheng2024promptagent: Cheng, L., et al. (2024). *PromptAgent: Strategic Planning with LLMs Enables Expert-Level Prompt Optimization*. arXiv:2310.16427. 见 r-paper-016。（MCTS prompt 搜索，与 DSPy 对照）
- schick2023toolformer: Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. NeurIPS 2023. 见 r-paper-003。（DSPy 的 `dspy.Tool` 模块的设计参考）