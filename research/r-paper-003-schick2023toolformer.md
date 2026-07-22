---
note_id: r-paper-003
title: Toolformer：LLM 自监督学习工具调用（Toolformer: Language Models Can Teach Themselves to Use Tools）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 3, Ch 13]
related_papers: [schick2023toolformer, yao2023react, shinn2023reflexion, wei2022cot, cai2023latm, parisi2022interesting, qin2023toolllm]
keywords: [Toolformer, self-supervised tool learning, T self-extension, training-time U, frozen inference, API calls]
---

# r-paper-003：Toolformer：LLM 自监督学习工具调用

> Toolformer 是第一个让 LLM **自身学会调用工具**的工作——但它的"自修改"发生在训练阶段而非推理阶段。它修改的是 B 中的 T（**使用模式**），而不是 T 的**集合**本身。这与本书第 13 章讨论的"运行时 T 自创建"（LATM、Voyager）有本质差异。

## 1. 论文定位

Schick 等人 2023 年发表的 *Toolformer: Language Models Can Teach Themselves to Use Tools*（NeurIPS 2023）[$TRAE_REF](https://arxiv.org/abs/2302.04761) 是 LLM 工具学习领域的里程碑。它提出了一种**自监督的 API 调用学习范式**：让 LLM 在海量无标注文本上自己生成 API 调用样本、自己给这些样本打分、自己训练——全程无需人工标注。论文展示了一个 6.7B 参数的 Toolformer 在数学、问答、搜索、翻译等多任务上显著优于同等规模甚至更大规模的无工具 LLM。

本书将 Toolformer 定位为**操作形态学 T 自扩展的特殊形态**。这里的"特殊"有两层含义：
1. **T 自修改发生在训练阶段**：Toolformer 通过 fine-tuning 修改模型参数，使模型在 inference 时**自然输出** API 调用。这与 ReAct 的 inference-time prompt 范式（让 LLM 在 prompt 引导下输出 Action）截然不同。
2. **修改的是 T 的"使用模式"而非 T 的"集合"**：Toolformer 预设了一组固定的 API（calculator、QA system、search、translation、calendar），它修改的是模型调用这些 API 的能力——而不是添加、删除或重写 API 本身。这与 LATM、Voyager 等运行时动态创建工具的工作形成对照。

论文的标题"Language Models Can Teach Themselves to Use Tools"暗示了一种**自监督学习（self-supervised learning）** 的范式——这与本书第 11 章"自进化"的核心精神（Agent 自主修改自身）一致。但 Toolformer 的"自修改"是一次性的（训练完成后冻结），不是本书定义的"运行时持续修改 B"。**Toolformer 是"训练期 U"，不是"推理期 U"**——这是它在操作形态学框架中的精确位置。

## 2. 核心贡献

Toolformer 论文做出三项核心贡献：

1. **自监督 API 调用数据集构造**：给定一组 API 和无标注文本，Toolformer 用启发式方法在文本中采样 API 调用位置，用执行结果作为监督信号，过滤掉低质量样本。这一流程完全无需人工标注。
2. **基于 self-supervised loss 的 fine-tuning**：把 API 调用当作特殊的 token sequence，让模型在原 next-token-prediction 损失之外加入 API 调用的 cross-entropy 损失。模型在学会"何时调用、调用什么、参数是什么"的同时保留原有语言能力。
3. **在多个任务上证明工具使用提升 LLM**：数学（MathQA、ASDIV）、问答（Web Questions、GooAQ）、搜索（TriviaQA）、翻译（De→En WMT）。Toolformer 6.7B 在所有任务上都显著优于同等规模的无工具基线，部分任务上甚至超过 175B 的 GPT-3。

### 2.1 与 ReAct 的边界

| 维度 | ReAct | Toolformer |
|---|---|---|
| 工具学习方式 | Prompt engineering | Self-supervised fine-tuning |
| 训练数据 | 6 条手工示例 | 海量无标注 web 文本 |
| 推理成本 | 高（每步 LLM 调用生成 Thought + Action） | 低（一次 forward pass） |
| 灵活性 | 高（换 prompt 即可换工具） | 低（添加工具需重训） |
| 工具集合 | 部署时固定 | 训练时固定 |
| 错误恢复 | LLM 重新生成 Action | 模型自行决定是否调用 |

Toolformer 与 ReAct 不在同一维度上——前者是"训练期范式"，后者是"推理期范式"。但两者都"使用工具"：Toolformer 通过模型参数学会工具调用；ReAct 通过 prompt 引导模型输出工具调用。

### 2.2 与 GPT-3 / GPT-4 的工具使用边界

GPT-3 没有内置工具——它只能生成文本。GPT-4（2023-06）引入 Function Calling，但这是 **inference-time API**：用户告诉 GPT-4 可用工具，GPT-4 在推理时决定调用哪个。Toolformer 是 **training-time API**：模型在训练时就学会了调用哪些工具、怎么调用，推理时无需用户告知工具集合。

这一差异决定了 Toolformer 的"工具使用"是**模型内置能力**，而非**用户可选扩展**。这与本书第 13 章讨论的 LATM、Voyager 形成对照——它们追求"运行时扩展工具集"，Toolformer 追求"训练时固化工具集"。

### 2.3 与 OpenAI Function Calling 的边界

OpenAI 2023 年 6 月发布的 Function Calling 协议是另一条工具调用路线：
- **Function Calling**：用户在 prompt 中提供工具的 JSON Schema，LLM 在推理时生成结构化 JSON 调用
- **Toolformer**：工具集在训练时确定，LLM 在推理时直接生成调用 token

Function Calling 更灵活（用户随时加工具），Toolformer 更高效（无需在 prompt 中重复工具描述）。两者代表了**inference-time vs training-time**两条工具调用路线的极致。

## 3. 方法细节

### 3.1 Toolformer 的形式化

设 LLM 词汇表为 \(V\)，新增特殊 token 集合 \(V_{\text{api}} = \{[\text{api}_1], [\text{api}_2], \ldots\}\)，每个 API token 对应一个具体的 API（calculator、QA、search、translation、calendar）。

**API 调用位置采样**：给定一段无标注 web 文本 \(x = (x_1, \ldots, x_n)\)，对每个位置 \(i\)，用启发式规则（如"当前位置是否包含数字""当前段落是否包含人名"）决定是否插入 API 调用 \(\text{call}_i\)。如果插入，则 \(x\) 变成 \((x_1, \ldots, x_i, \text{call}_i, x_{i+1}, \ldots)\)。

**执行结果填充**：实际执行 \(\text{call}_i\) 得到结果 \(r_i\)，把 \(r_i\) 拼接到 call 后面：\(\text{call}_i = [\text{api}_k] \, \text{args} \, [\text{EOS}] \, r_i\)。

**质量过滤**：用 perplexity loss 评估 API 调用是否真的帮助后续预测——如果 loss 减少超过阈值 \(\tau\)，保留该样本；否则丢弃。

**Fine-tuning**：在过滤后的样本上继续 fine-tuning 原模型，使用 next-token-prediction 损失。模型在保留原有语言能力的同时，学会在合适位置输出 API 调用。

### 3.2 伪代码实现

```python
class ToolformerTrainer:
    def __init__(self, base_llm, apis, corpus, threshold=1.0):
        self.llm = base_llm                       # 待训练的 LLM
        self.apis = apis                          # T: 固定 API 集合
        self.corpus = corpus                      # 无标注 web 文本
        self.threshold = threshold                # 质量过滤阈值

    def sample_api_call(self, text, position):
        # 启发式: 决定在 position 是否插入 API 调用
        for api in self.apis:
            if api.should_call_at(text, position):
                return api.sample_call(text, position)
        return None

    def execute_and_score(self, text, position, call):
        # 执行 API 调用
        result = call.execute()
        # 用 perplexity 评估 API 调用是否帮助后续预测
        loss_with_call = self.llm.perplexity(
            text[:position] + [call.with_result(result)] + text[position:]
        )
        loss_without = self.llm.perplexity(text)
        # 过滤: 只有 loss_with < loss_without - threshold 才保留
        if loss_without - loss_with_call > self.threshold:
            return text[:position] + [call.with_result(result)] + text[position:]
        else:
            return None  # 丢弃低质量样本

    def construct_dataset(self):
        augmented = []
        for text in self.corpus:
            for position in range(len(text)):
                call = self.sample_api_call(text, position)
                if call is None:
                    continue
                filtered = self.execute_and_score(text, position, call)
                if filtered is not None:
                    augmented.append(filtered)
        return augmented

    def train(self):
        dataset = self.construct_dataset()  # 自监督生成训练数据
        # 在原 next-token-prediction 损失上继续训练
        self.llm.fine_tune(
            dataset,
            objective=lambda x: -self.llm.log_prob(x),  # 标准 LM 损失
            epochs=3,
        )
        # 训练完成后, T 的"使用模式"被烤入模型参数
        return self.llm
```

注意：`self.apis` 在 `__init__` 后**完全冻结**——训练过程**不会**添加新 API，也不会**重写**已有 API 的实现。Toolformer 唯一修改的是 `self.llm` 的参数。这正是 "T 自修改的特殊形态"的精确含义。

### 3.3 五个工具的细节

论文展示了五个 API，每个 API 对应一个不同的能力：

| API | 用途 | 输入示例 | 输出示例 |
|---|---|---|---|
| **Calculator** | 数学计算 | `[Calculator(2+3*4)]` | `[Calculator(2+3*4) → 14]` |
| **QA System** | 短答案问答 | `[QA(Who founded Apple?)]` | `[QA(...) → Steve Jobs]` |
| **Search** | Wikipedia 检索 | `[Search(Beijing population)]` | `[Search(...) → 21.54 million]` |
| **Translation** | 机器翻译 | `[Translation(De: Guten Tag)]` | `[Translation(...) → Good day]` |
| **Calendar** | 日期查询 | `[Calendar(2024 Olympics)]` | `[Calendar(...) → 2024-07-26]` |

这五个 API 覆盖了"需要精确计算 / 外部知识 / 多语言"的任务——这些都是 LLM 自身的弱点。Toolformer 用工具补足了这些弱点，但**不试图让 LLM 自身学会这些能力**。

### 3.4 质量过滤的两种方式

论文提出两种过滤 API 调用样本的方法：

1. **基于执行结果的过滤**：仅当 API 调用成功（无错误）时保留。
2. **基于 perplexity 的过滤**：仅当 API 调用降低后续 token 的 perplexity 时保留。

第二种过滤是 Toolformer 的关键创新——它**用语言模型的困惑度作为 API 价值的代理指标**。这一方法与 r-paper-002 中 Reflexion 的"反思价值评估"思路相似，但 Toolformer 在训练期、Reflexion 在推理期。

## 4. 操作形态学视角

把 Toolformer 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到一个**关键的"何时修改"问题**。

### 4.1 Toolformer 中 B 的每个组件

| 组件 | 在 Toolformer 中的实现 | 修改能力 |
|---|---|---|
| \(P\) | 不存在显式 prompt（模型内部化） | **冻结**（模型参数已固化工具调用） |
| \(T\) | 五个固定 API：calculator, QA, search, translation, calendar | **集合冻结**；但**使用模式**通过 fine-tuning 烤入模型参数 |
| \(M\) | 无显式 M（模型权重即记忆） | **冻结**（无显式记忆结构） |
| \(C\) | LLM forward pass（无需外部 C 逻辑） | **冻结**（无外部控制流） |

**特殊之处**：Toolformer 的 T 集合在训练前确定，训练后**冻结**。模型学会的是 T 的"使用模式"——什么位置插入调用、参数怎么填、结果怎么用——这些都编码在模型参数中。**T 的"如何使用"被修改了，T 的"包含什么"没有被修改**。

### 4.2 Toolformer 中 U 的状态

Toolformer 的"U"是 **self-supervised dataset construction + fine-tuning pipeline**：

\[
B_{\text{after training}} = U_{\text{training}}(B_{\text{before}})
\]

其中：
- \(B_{\text{before}} = (P=\emptyset, T=\{\text{5 APIs}\}, M=\emptyset, C=\text{LLM forward})\)
- \(B_{\text{after}} = (P'=\emptyset, T'=\{\text{5 APIs with usage patterns in params}\}, M'=\emptyset, C'=\text{same})\)

**U 只在训练阶段运行一次**。训练完成后，模型不再改变——Toolformer **没有 inference-time U**。

形式化：

\[
U_{\text{Toolformer}} = \begin{cases}
\text{non-trivial update} & \text{if } t = \text{training phase} \\
\text{identity (no update)} & \text{if } t = \text{inference phase}
\end{cases}
\]

这与 Reflexion 的 U 形成鲜明对比：

| 维度 | Toolformer 的 U | Reflexion 的 U |
|---|---|---|
| 运行时机 | 训练期，一次性 | 推理期，每次 episode |
| 修改对象 | 模型参数（即隐式 P/T/M/C） | 显式 M |
| 是否需要反馈 | 需要（perplexity 损失） | 需要（成功/失败） |
| 运行成本 | 高（一次完整 fine-tuning） | 低（一次 LLM 调用） |

### 4.3 Toolformer 是"训练期 T 自修改"而非"运行时 T 自修改"

本书第 13 章"自动工具创建与重构"区分了三种 T 自修改：
1. **T 使用模式自修改**（Toolformer）：T 集合固定，但模型学会怎么用 T
2. **T 集合自扩展**（LATM、Voyager）：运行时添加新工具到 T
3. **T 实现自修改**（AlphaEvolve）：运行时修改工具的内部实现

Toolformer 是第 1 种——它**预设工具集**、**训练使用模式**。这是 T 自修改中最弱的一种：Agent 不能添加新工具，只能更好地使用已有工具。

但这并不削弱 Toolformer 的重要性——它证明了**LLM 可以通过自监督学会工具调用**，无需 RLHF、无需人工标注。这是 T 自修改的"前置条件"：只有 LLM 学会使用工具，它才能学会创建工具。

### 4.4 Toolformer 与 L0-L5 等级的关系

按本书第 18 章：
- **L0 静态 LLM**：无工具
- **L1 Tool-using（inference-time prompt）**：ReAct、Function Calling
- **L2 Tool-using（training-time bake-in）**：Toolformer（**位于 L2 的特殊位置**）

Toolformer 是 L2 的"训练期版本"。它不是 L4——L4 要求**运行时修改 T 集合**，Toolformer 在训练后**冻结 T 集合**。但 Toolformer 是 L4 的**前置基础**——没有 Toolformer 式的工具使用训练，Agent 难以在运行时创造工具。

### 4.5 Toolformer 中"LLM-as-U"的缺席

与 Reflexion 不同，Toolformer 的 U **不是 LLM 自身**——U 是**外部分析 pipeline**（启发式采样 + 执行 + 过滤 + fine-tuning）。Toolformer 的 LLM 在训练期间是被动的——它接收数据集、做梯度下降，不参与"是否调用 API"的元决策。

这是 Toolformer 与 LLM-as-U 范式的关键区别。本书第 17 章主张 U 由 LLM 自身承担——这一主张在 Reflexion 中成立，在 Toolformer 中**不成立**。

### 4.6 Toolformer 的 T 自修改是"隐式参数修改"而非"显式集合修改"

本书第 11 章定义的 T 自修改是**显式修改 T 集合**（添加、删除、重写 API）。Toolformer 修改的是 LLM 参数——这些参数编码了"如何调用 T"，但不改变 T 本身。

这一区分在工程上很重要：
- **显式 T 修改**（LATM）：Agent 在推理时可以查看、修改、删除工具集合——可解释、可审计。
- **隐式 T 修改**（Toolformer）：Agent 不能查看自己的 T——所有工具调用都"自然"地从 LLM 参数中涌现——不可解释、难调试。

本书第 22 章"安全性"对两者给出不同评判：**显式 T 修改更安全**（因为可以静态分析 T 的变化），**隐式 T 修改更难审计**（因为 T 的"使用模式"散布在数十亿参数中）。

## 5. 实验与结果

Toolformer 在多个任务上做了实验：

### 5.1 数学（MathQA、ASDIV）

- 数据集：MathQA（37k 词问题）+ ASDIV（5.6k 小学数学题）
- 6.7B Toolformer：相对无工具基线提升 ~30%
- 对照：175B GPT-3 无工具：~5% 准确率；Toolformer 6.7B：~35%
- 操作形态学意义：Calculator API 是**最纯粹的 T 自修改**——它把 LLM 不会的事（精确算术）外置给 API。Toolformer 学会"遇到算术就调用 Calculator"，这等价于"把 T 中的 calculator 用法烤进模型"。

### 5.2 问答（Web Questions、GooAQ）

- 数据集：Web Questions（5.8k 自然问题）+ GooAQ（自然问题集合）
- 6.7B Toolformer：相对无工具基线提升 ~10%
- 对照：QA System + LLM 6.7B vs GPT-3 175B——小模型+QA 大幅超越大模型无工具
- 操作形态学意义：QA API 把"事实检索"外置，让小模型也能回答需要外部知识的问题。

### 5.3 Wikipedia 检索（TriviaQA）

- 数据集：TriviaQA（95k trivia 问题）
- 6.7B Toolformer + Search API：相对无工具提升 ~15%
- 操作形态学意义：Search API 是"动态知识源"——每次调用返回最新 Wikipedia 内容。Toolformer 学会"何时搜索、怎么用搜索结果"。

### 5.4 多语言翻译（De→En WMT）

- 数据集：WMT19 De-En（~40M 句对）
- 6.7B Toolformer + Translation API：相对无工具提升 ~25%
- 操作形态学意义：Translation API 把"多语言生成"外置。Toolformer 学会"何时触发翻译、怎么用翻译结果"。

### 5.5 关键实验观察

| API | 提升幅度 | 难度 | 操作形态学意义 |
|---|---|---|---|
| Calculator | 高（30%+） | 低（API 接口简单） | T 使用模式自修改的"低垂果实" |
| QA | 高（20%+） | 中（API 输出需整合） | T 调用后处理的能力 |
| Search | 中（15%） | 高（结果过滤、融合） | T 调用决策的难度 |
| Translation | 高（25%） | 低（输入输出对齐） | T 在跨语言任务中的杠杆 |
| Calendar | 中（10%） | 中（实体识别、时间解析） | T 在结构化查询上的局限 |

Toolformer 在所有任务上都优于无工具基线——证明**工具使用是 LLM 能力的"放大器"**。但效果大小差异显著，说明**T 自修改的收益与 API 接口的复杂度和任务难度有关**。

### 5.6 消融研究：API 数量与性能

论文报告：使用 5 个 API 的 Toolformer 比使用 1 个 API 的版本平均性能提升 12%。但再增加 API（实验到 10 个）性能开始下降——表明**T 集合过大会分散模型注意力**，T 自修改不是"越多越好"。

这一发现与本书 H3（形态适配）一致——T 应该适配任务域，而不是越大越好。

## 6. 局限与开放问题

Toolformer 的局限可以分为四类：**训练成本、灵活性、可解释性、安全性**。本节是本书对 Toolformer 的批判性分析。

### 6.1 训练成本：不可承受的 fine-tuning 开销

Toolformer 需要在 5 个 API 上各执行**大量** API 调用（论文未公开具体数字，但从样本过滤率推断，至少数十万次 API 调用）。每次 fine-tuning 需要：

1. 在 ~10M 文档上采样 API 调用位置
2. 执行 ~100k API 调用（每个 API 20k）
3. 计算 perplexity loss
4. 完整 fine-tune LLM（可能需要数十 GPU hours）

这一成本对 6.7B 模型尚可接受，对 70B+ 模型**几乎不可能**。这就是为什么 Toolformer 之后的工作（如 LATM、Voyager）转向**inference-time 工具创建**——避免 fine-tuning 开销。

本书第 13 章指出：**Toolformer 的训练成本是其大规模部署的最大障碍**。

### 6.2 灵活性：训练后无法添加新工具

Toolformer 一旦训练完成，工具集合**永久冻结**。如果业务需求变化（出现新 API），Agent 不能动态添加新工具——必须重新 fine-tune。

这与 OpenAI Function Calling 形成鲜明对比：用户可以**运行时**告诉 LLM 新工具的 JSON Schema，LLM 立即开始使用。Toolformer 的"训练期固化"在灵活性上是劣势。

本书第 13 章的 LATM、Voyager 正是为解决此问题而生——它们允许 Agent **运行时**创建新工具。

### 6.3 可解释性：工具调用不可审计

Toolformer 的工具调用完全由模型参数决定——我们不知道模型为什么在某个位置决定调用 API。可解释性分析（如 attention 可视化、neuron probing）只能给出部分答案。

这与 ReAct 形成对比——ReAct 的 Thought 是显式的、可读的。Toolformer 的"思考"被分散在数十亿参数中，**不可解释**。

本书第 22 章讨论的安全性视角：Toolformer 的工具调用可能被 prompt injection 利用——攻击者无法直接修改模型参数，但可以通过训练数据投毒（在 web 文本中植入误导性 API 调用样本）来让 Toolformer 学会**有害的工具使用模式**。这是 Toolformer 的**训练时安全漏洞**。

### 6.4 API 数量与"工具注意力稀释"

论文消融显示，使用 10 个 API 时性能下降。这一现象被称为 **工具注意力稀释（tool attention dilution）**：LLM 在推理时，工具集越大，模型对"何时调用、调用哪个"的判断越模糊。

本书 H3（形态适配）预测：不同任务域应该有不同的 T——T 应该适配任务，而不是越大越好。Toolformer 的消融研究为这一假设提供了早期证据。

### 6.5 错误传播：API 错误会传染

Toolformer 假设 API 调用结果是可靠的。但实际 API 可能：
- 返回错误（如 500 Internal Server Error）
- 返回过时数据（如 Wikipedia 检索的旧版本）
- 返回对抗性内容（如攻击者污染的搜索结果）

Toolformer 把 API 结果直接拼接到模型输入中——**没有验证机制**。这意味着一个错误的 API 调用可能让后续生成全部偏离。

本书第 23 章"可验证自修改"明确指出：**所有 M/T 自修改都必须经过验证**。Toolformer 不验证 API 结果——这是一个**重大安全缺陷**。

### 6.6 跨语言/跨模型的迁移性

Toolformer 的训练是**针对特定 LLM 的**——在 6.7B GPT-J 上训练的 Toolformer 不能直接用于 LLaMA 7B。每个 LLM 都需要重新 fine-tune。

这与 OpenAI Function Calling 形成对比——后者是**模型无关的协议**。

### 6.7 开放问题表

| 问题 | 当前状态 | 本书视角 |
|---|---|---|
| 能添加运行时新工具吗？ | 不能 | 第 13 章 LATM、Voyager |
| 能验证 API 调用吗？ | 不能 | 第 23 章可验证自修改 |
| 能跨 LLM 迁移吗？ | 不能 | 通用 U 设计 |
| 能减少 fine-tuning 成本吗？ | 部分（PEFT、LoRA） | 第 12 章 OPRO（不 fine-tune） |
| 能避免训练数据投毒吗？ | 不能 | 第 22 章对抗鲁棒性 |

## 7. 对本书的贡献

Toolformer 在本书的理论体系中扮演**T 自修改的"零阶"角色**：它证明了"LLM 可以自监督学会调用工具"，但它没有实现"运行时 T 自扩展"。

### 7.1 Toolformer 作为 T 自修改的前置基础

本书第 13 章的 T 自修改路线图：

```
Toolformer（训练期使用模式）
    ↓
LATM（运行时创建工具）
    ↓
Voyager（运行时技能库增长）
    ↓
AFlow（运行时工作流进化）
    ↓
AlphaEvolve（运行时整个代码库进化）
```

Toolformer 是这条链的起点——它证明了**LLM 可以在没有人工标注的情况下学会工具使用**。但 Toolformer 的"学会"是训练时的、一次性的；后续工作追求的是**推理时的、持续的 T 自修改**。

### 7.2 Toolformer 与本书 H1-H5 的关系

| 假设 | Toolformer 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | T 使用模式可在训练时被修改 | **部分支持 H1**（仅训练期） |
| **H2 协同演化** | Toolformer 不涉及 P/M/C 修改 | H2 不可验证（只动 T 使用模式） |
| **H3 形态适配** | Toolformer 的 T 集合固定（5 个 API） | 不支持 H3（T 不适配） |
| **H4 迁移收益** | Toolformer 不能跨任务迁移 T | **反驳 H4**（工具固化） |
| **H5 治理必要性** | Toolformer 无 API 验证机制 | 需要治理（推动 H5） |

### 7.3 Toolformer 与 Function Calling 的范式分歧

本书第 3 章讨论工具调用协议时，把 Toolformer 与 Function Calling 视为两条平行路线：

| 维度 | Toolformer | Function Calling |
|---|---|---|
| 修改时机 | 训练期 | 推理期 |
| 工具集合 | 固定（5 个） | 可变（用户随时加） |
| 实现 | 模型参数 | Prompt + JSON Schema |
| 灵活性 | 低 | 高 |
| 推理成本 | 低（一次 forward） | 中（需解析 JSON Schema） |
| 安全性 | 难审计 | 易审计 |

本书主张：**未来的 Agent 应该结合两者优势**——训练期固化常用工具（Toolformer 范式），推理期动态扩展（Function Calling 范式）。这种**混合 T 自修改**是第 13 章的关键方向。

### 7.4 Toolformer 与训练数据安全

Toolformer 的训练数据是无标注 web 文本——它**继承**了 web 文本的所有偏见、错误、对抗内容。攻击者可以通过投毒训练数据（在大规模 web 文本中植入误导性 API 调用样本）来让 Toolformer 学会有害的工具使用模式。

本书第 22 章"对抗鲁棒性"将深入讨论这一问题：**自监督学习的 Agent 必须有"训练数据来源审计"机制**——这与第 23 章"可验证自修改"形成互补。

### 7.5 给读者的关键启示

1. **Toolformer 是 T 自修改的"零阶"**：它证明了 LLM 可以自学工具使用，但它的自修改是一次性的、隐式的。
2. **Toolformer 与 ReAct 是工具调用的两条路线**：训练期固化 vs 推理期 prompt。两者各有优劣，未来 Agent 应结合两者。
3. **Toolformer 不能添加新工具**：这是它与 LATM、Voyager 的根本差异——本书第 13 章的工作才是"真正的 T 自修改"。
4. **Toolformer 有安全漏洞**：训练数据投毒可以攻击它，没有 API 验证机制——这两个问题推动第 22-23 章的研究。
5. **Toolformer 的细粒度是 T 的"使用模式"而非 T 的"集合"**：理解这一区分是理解第 13 章 T 自修改全谱的前提。

Toolformer 是从 L1（无工具 LLM）到 L2（工具使用 LLM）的关键跳跃，但它不是 L4（运行时 T 自修改）的实现。它是本书 Part I 的最后一站，也是 Part III 第 13 章"自动工具创建与重构"的逻辑起点。

## 参考文献

- schick2023toolformer: Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. NeurIPS 2023. [$TRAE_REF](https://arxiv.org/abs/2302.04761)
- yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 见 r-paper-001。
- shinn2023reflexion: Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS 2023. 见 r-paper-002。
- wei2022cot: Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. NeurIPS 2022.
- cai2023latm: Cai, T., et al. (2023). *Large Language Models as Tool Makers (LATM)*. arXiv:2305.17126. （Toolformer 的下一阶段：运行时 T 创建）
- parisi2022interesting: Parisi, A., et al. (2022). *Interesting Scientific Object Generation*（自监督生成范式的早期代表）
- qin2023toolllm: Qin, Y., et al. (2023). *ToolLLM: Facilitating Large Language Models to Master 16000+ Real-World APIs*. arXiv:2307.16789. （Toolformer 之后的 inference-time 工具学习工作）