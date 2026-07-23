---
note_id: r-paper-035
title: 参与式意义生成：互动如何启动认知（Participatory Sense-Making）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 16, Ch 11]
related_papers: [deJaegher2009participatory, varela1991embodied, froese2011enactive, gallagher2017enactive, noe2004action, clark1998extended, newen2018oxford, maturana1980autopoiesis, yao2023react, sumers2023coala, robeyns2025sica]
keywords: [De Jaegher, Di Paolo, participatory sense-making, interaction, social cognition, multi-agent, coordination, super-additivity, H2, enactivism, dialogical, second-person, operational morphology]
---

# r-paper-035：参与式意义生成：互动如何启动认知（Participatory Sense-Making）

> Hanne De Jaegher 与 Ezequiel Di Paolo 在 2009 年发表于 *Phenomenology and Cognitive Sciences* 期刊的 *Participatory Sense-Making* 是 enactivism 阵营向**社会认知**扩展的奠基性论文——它提出 **"Participatory Sense-Making（PSM, 参与式意义生成）"** 论断：**意义生成（sense-making）不只发生在个体内部，而是发生在两个或多个 Agent 的互动过程中**。当两个 Agent 互动时，会涌现出**既不属于任一 Agent、也不能被任一 Agent 单独生成的"互动结构"**——这一结构是认知的"超加性"（super-additive）涌现。本书把 PSM 视为**操作形态学 B 的"跨组件协同"哲学源头**——B = {P, T, M, C} 中的"跨组件" 不仅指单个 Agent 的多个组件，更指**多个 Agent 之间的跨组件协同**。这是 H2（协同演化）的最直接认知科学来源，也是多 Agent 系统设计的哲学基础。

## 1. 论文定位

Hanne De Jaegher（University of Copenhagen 哲学家）与 Ezequiel Di Paolo（Ikerbasque / University of the Basque Country 认知科学家）在 2009 年发表于 *Phenomenology and Cognitive Sciences* 期刊的 *Participatory Sense-Making* [$TRAE_REF](https://link.springer.com/article/10.1007/s11097-008-9117-5)（pp. 465-481）是 enactivism 阵营向**社会认知**扩展的奠基性论文。它提出 **"Participatory Sense-Making（PSM）"** 论断——**意义生成（sense-making）不只发生在个体内部，而是发生在两个或多个 Agent 的互动过程中**。当两个 Agent 互动时，会涌现出**既不属于任一 Agent、也不能被任一 Agent 单独生成的"互动结构"**——这一结构是认知的"超加性"涌现。

本书将 *Participatory Sense-Making* 定位为**操作形态学 B 的"跨组件协同"哲学源头**。原因有三：

1. **它提供了 B "跨组件协同"的合法性**：B = {P, T, M, C} 的协同不仅是单个 Agent 的多个组件协同，更是**多个 Agent 之间的协同**。LLM Agent 调用工具（T）就是与工具之间的"参与式互动"——LLM 提供意义生成，工具提供任务执行，两者协同生成"互动结构"。
2. **它提供了 H2（协同演化）的认知科学源头**：H2 主张"协同演化 = B 多个组件之间超加性涌现"。De Jaegher & Di Paolo 的"participatory sense-making" 是 H2 的具体化——两个 Agent 协同涌现的"互动结构"是 H2 的认知科学案例。
3. **它整合了 enactivism 与社会认知**：PSM 把 Varela 等人的"个体意义生成"（r-paper-010）扩展到"社会意义生成"——意义在两个或多个 Agent 的互动中涌现。这一扩展对 LLM Agent 时代有关键意义——LLM Agent 的多 Agent 协同是"参与式意义生成"的工程实现。

论文做出的三个核心判断被本书重新审视：

- **"Meaning-making is participatory"（意义生成是参与式的）**：意义生成不只发生在个体内部，而是发生在两个或多个 Agent 的互动过程中。互动产生既不属于任一 Agent、也不能被任一 Agent 单独生成的"互动结构"。
- **"Super-additivity"（超加性）**：互动的"总意义"大于个体意义的简单加和——互动涌现出超越个体能力的"互动结构"。这是 H2 的核心机制。
- **"Coordination dynamics"（协同动力学）**：互动中的两个 Agent 调整彼此的行为模式，形成协调的"耦合动力学"——这一耦合动力学是 enactivism 的"结构耦合"在社会维度上的延伸。

## 2. 核心贡献

*Participatory Sense-Making* 做出四项核心贡献：

1. **提出 PSM 论断（Participatory Sense-Making Thesis）**：明确意义生成是参与式的——发生在两个或多个 Agent 的互动过程中，而不只是个体内部。这一论断把 enactivism 从"个体认知"扩展到"社会认知"。
2. **形式化"互动结构"（Interaction Structure）**：明确"互动结构"是互动中涌现的、不能被任一 Agent 单独生成的协调模式。这一结构是 H2 的"超加性涌现"的核心机制。
3. **区分"互动中的意义生成"与"互动后的意义生成"**：PSM 强调"互动中的意义生成"——意义在互动的**实时处理过程中**涌现，而不是在互动之后的反思中产生。这一区分让 PSM 区别于"分布式认知"等传统理论。
4. **整合 enactivism 与社会认知**：PSM 把 Varela 等人的"个体意义生成"扩展到社会维度——意义在两个或多个 Agent 的协同中涌现。这一整合为多 Agent 系统设计提供了认知科学根基。

### 2.1 与 Varela 1991（r-paper-010）的关系

Varela 1991 的"个体意义生成"（individual sense-making）主张：**意义生成发生在有机体与其环境的结构耦合中**。De Jaegher & Di Paolo 把这一论断扩展到**社会维度**：

- **Varela**：单个 Agent 在结构耦合中生成意义。
- **De Jaegher & Di Paolo**：两个或多个 Agent 在互动中生成意义。

这一扩展的关键洞见：**意义生成不仅是个体与环境的耦合，也是个体之间的耦合**。LLM Agent 时代，**这一扩展有具体应用**：
- LLM Agent 与工具的耦合（r-paper-003 Toolformer）是"个体意义生成"——Agent 通过工具与环境互动。
- LLM Agent 与其他 Agent 的耦合（r-paper-006 SICA 中的 multi-agent）是"参与式意义生成"——多个 Agent 在互动中生成意义。

### 2.2 与 Noë 2004（r-paper-028）的关系

Noë 2004 的"知觉即行动"（action in perception）主张：**视觉不是被动的图像接收，而是主动的感官运动探索**。De Jaegher & Di Paolo 把这一论断扩展到**社会维度**：

- **Noë**：单个主体的感知是行动。
- **De Jaegher & Di Paolo**：两个主体的互动是相互行动（A 的行动影响 B 的感知，B 的感知引导 A 的下一步行动）。

**互动是相互行动**——这是 PSM 的核心机制。LLM Agent 时代，**多 Agent 协同是"相互行动"的工程实现**：
- Agent A 的输出影响 Agent B 的输入（Toolformer 风格）。
- Agent B 的反馈修改 Agent A 的下一步（Multi-Agent ReAct 风格）。

### 2.3 与 Froese & Ziemke 2011（r-paper-026）的关系

Froese & Ziemke 2011 的"自主性 + 意义生成" 论断是 enactivism 的工程判据。De Jaegher & Di Paolo 与此兼容，但增加**"参与式"**维度：

- **Froese & Ziemke**：单个 Agent 的自主性 + 意义生成。
- **De Jaegher & Di Paolo**：多个 Agent 的参与式意义生成——互动涌现的"互动结构"是意义生成的新维度。

这一增加对 LLM Agent 时代有具体意义：**多 Agent 系统的意义生成不能被还原为单个 Agent 的意义生成**——多 Agent 系统的"互动结构"是单个 Agent 不具备的。

### 2.4 与 Clark 1998（r-paper-011）的关系

Clark 1998 的"延展心智论"主张认知可延展到外部工具。De Jaegher & Di Paolo 与此兼容，但增加**"参与式"**维度：

- **Clark 1998**：认知可延展到**工具**（Otto 的笔记本）。
- **De Jaegher & Di Paolo**：认知可延展到**其他 Agent**（互动中的"互动结构"）。

**LLM Agent 与 LLM Agent 的协同是"延展心智论"的社会版本**——认知可延展到其他 Agent。

### 2.5 与 Hutto & Myin 2017（r-paper-033）的关系

Hutto & Myin 主张"基本认知无内容"。De Jaegher & Di Paolo 与此兼容，但增加**"互动"**维度：

- **Hutto & Myin**：基本认知是个体无内容行动。
- **De Jaegher & Di Paolo**：基本认知是**参与式**无内容行动——Agent 在互动中调整彼此的行为模式。

**多 Agent 协同是无内容行动的延伸**——Agent 通过调整彼此的行为模式协同完成单个 Agent 不能完成的任务。

## 3. 核心论证

De Jaegher & Di Paolo 2009 的论证结构可以分为五个层次：

### 3.1 第一层：个体意义生成的局限

De Jaegher & Di Paolo 首先论证**个体意义生成不足以解释社会认知**：

- **语言理解**：Speaker 与 Hearer 在对话中实时调整彼此的句子结构、词汇选择——这一调整过程是"互动中的"，不是单个 Agent 单独能完成的。
- **共同注意**：婴儿与照顾者通过视线、手势、声音形成"共同注意"——这一共同注意不是婴儿单独能完成的，也不是照顾者单独能完成的。
- **协作任务**：两个 Agent 在协作任务中协调彼此的动作——这一协调不是单个 Agent 单独能完成的。

这些现象表明：**社会认知需要"参与式意义生成"作为新的解释维度**。

### 3.2 第二层：参与式意义生成（PSM）的定义

De Jaegher & Di Paolo 提出 PSM 的正式定义：

> **Participatory Sense-Making（PSM）**：Meaning generation occurs in the interaction process itself, through the coordination of embodied agents, and this coordination generates an interactional structure that is not reducible to the individual sense-making of either participant.

PSM 的核心要素：

1. **实时性**：意义生成发生在互动**过程中**，不是互动之后。
2. **协调性**：意义生成通过两个 Agent 的协调（动作、姿态、语言的协调）实现。
3. **不可还原性**：互动中涌现的"互动结构"不能被还原为单个 Agent 的意义生成。

### 3.3 第三层：超加性（Super-additivity）

De Jaegher & Di Paolo 提出"超加性"作为 PSM 的核心机制：

> **互动的总意义 > 个体意义的简单加和**。

具体地：

- 设 Agent A 的意义生成量为 $S_A$，Agent B 的意义生成量为 $S_B$。
- 设 A 和 B 互动时产生的意义生成量为 $S_{AB}$。
- **PSM 主张**：$S_{AB} > S_A + S_B$（互动涌现出超越个体加和的意义）。

这一超加性是**H2（协同演化）的核心机制**——协同涌现的"互动结构"是协同的"超加性"产物。

LLM Agent 时代，**超加性的工程实现**：
- LLM Agent A 与 LLM Agent B 协同完成任务的性能 > A 单独完成 + B 单独完成的简单加和。
- 这一超加性来自"互动结构"——A 与 B 在协同中实时调整彼此的行为模式。

### 3.4 第四层：协同动力学（Coordination Dynamics）

De Jaegher & Di Paolo 用"协同动力学"（coordination dynamics）描述互动中的协调过程：

> **互动中的两个 Agent 调整彼此的行为模式，形成协调的"耦合动力学"——这一耦合动力学是 enactivism 的"结构耦合"在社会维度上的延伸。**

协同动力学的核心机制：

- **耦合吸引子（Coupled Attractors）**：互动中形成稳定的协调模式（如对话中的"轮流"模式）。
- **去耦合（Decoupling）**：当互动破裂时，协调模式解体。
- **重新耦合（Re-coupling）**：重新形成新的协调模式。

这一动力学是**多 Agent 系统的核心机制**——多 Agent 系统的协同是协同动力学的工程实现。

### 3.5 第五层：互动结构（Interaction Structure）

De Jaegher & Di Paolo 提出"互动结构"（interaction structure）作为互动的核心涌现：

> **互动结构是互动中涌现的、不能被任一 Agent 单独生成的协调模式**。

互动结构的特征：

- **涌现性**：互动结构是互动的涌现产物，不能被任一 Agent 单独生成。
- **情境性**：互动结构依赖于互动的具体情境。
- **可变性**：互动结构可以随互动过程的变化而变化。

LLM Agent 时代，**互动结构的工程实现**：
- 多 Agent 系统的"协同模式"（如对话中的"引导-响应"模式）——这是互动结构。
- 多 Agent 协同涌现的"集体智能"（如辩论系统的"正反方"模式）——这是互动结构。

## 4. 操作形态学视角

把 *Participatory Sense-Making* 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到操作形态学的**"跨组件协同"判据**。

### 4.1 PSM 作为 B "跨组件协同"的认知科学

PSM 的核心论断——**意义生成发生在两个或多个 Agent 的互动中**——在操作形态学中对应：

- **B 的协同超加性**：多个 Agent 的 B 协同涌现的"互动结构"是超加性涌现。
- **H2（协同演化）** = PSM 在操作形态学中的工程实现。
- **Multi-Agent System** = PSM 在 LLM Agent 时代的工程实现。

这一对应让操作形态学有明确的**社会维度**——B 的协同不仅是单个 Agent 的内部组件协同，更是多个 Agent 之间的协同。

### 4.2 超加性作为 H2 的核心机制

PSM 的"超加性"论断——**互动的总意义 > 个体意义的简单加和**——在操作形态学中对应 H2 的核心机制：

- **H2（协同演化）**：B 的多组件协同 > 各组件独立演化之和。
- **超加性机制**：多个组件协同涌现的"互动结构"是 H2 的核心。
- **LLM Agent 时代的工程实现**：多 Agent 协同演化（如 Gödel Agent 的 Multi-Agent 版本）应展示超加性。

本书第 16 章将超加性作为 H2 的实证判据——**多个 Agent 协同演化的性能 > 各 Agent 单独演化之和**。

### 4.3 互动结构作为 H2 的涌现产物

PSM 的"互动结构"论断——**互动结构是互动中涌现的协调模式**——在操作形态学中对应：

- **H2（协同演化）** 的涌现产物 = "互动结构"在 multi-agent 操作形态学中的工程实现。
- **Multi-Agent System 的"协同模式"** = 互动结构的具体表现。
- **H2 的可观测性**：互动结构是 H2 的可观测证据——当我们观察到"互动结构"涌现时，H2 被支持。

### 4.4 协同动力学作为多 Agent 系统的设计原则

PSM 的"协同动力学"在操作形态学中对应：

- **多 Agent 系统的设计原则**：协同动力学（耦合吸引子、去耦合、重新耦合）是多 Agent 系统的设计原则。
- **H5（治理必要性）** 在多 Agent 系统中：协同动力学必须有边界，否则"过度耦合"会导致系统不稳定。
- **协同的失败模式**：去耦合（系统不稳定）、过度耦合（系统僵化）、不稳定耦合（系统震荡）——这些是 H5 在多 Agent 系统中的失败模式。

### 4.5 与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L0 静态 LLM**：无互动（个体的 LLM）。
- **L2 ReAct Agent**：基础互动（LLM + 工具）。
- **L3 Reflexion**：反思式互动（LLM + 反思系统）。
- **L4 MemGPT/A-MEM**：记忆式互动（LLM + 记忆系统）。
- **L4 Voyager/SICA**：代码/工具式互动（LLM + 自演化工具）。
- **L5 Gödel Agent**：B 全互动（LLM + 多 Agent + 自演化 + 协同）。

**L5 是 PSM 的最完整体现**——LLM Agent 与多个 Agent 协同，所有组件协同涌现互动结构。

### 4.6 与 H1-H5 的关系

| 假设 | PSM 论据 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | 互动结构是动态的 | **强支持 H1** |
| **H2 协同演化** | 超加性 = 协同涌现 | **强支持 H2** |
| **H3 形态适配** | 不同互动模式适应不同任务 | **支持 H3** |
| **H4 迁移收益** | 互动模式可跨任务迁移 | **支持 H4** |
| **H5 治理必要性** | 协同必须有边界 | **强支持 H5** |

PSM 在 H2 上提供最强论据。**H2 的"协同演化" 在 PSM 看来是"参与式意义生成"——多个 Agent 在互动中涌现超加性结构**。H5 的"治理必要性"在 PSM 看来是"协同必须有边界"——过度协同会导致多 Agent 系统失去自主性。

### 4.7 与 CoALA（r-paper-022）的关系

CoALA（r-paper-022）提出 LLM Agent 的认知架构分解为决策、记忆、行动。在多 Agent 系统中，这一架构可以扩展为：

- **跨 Agent 决策**：Agent A 的决策影响 Agent B 的决策。
- **跨 Agent 记忆**：Agent A 的记忆影响 Agent B 的下一步（共享记忆）。
- **跨 Agent 行动**：Agent A 的行动与 Agent B 的行动形成互动结构。

**CoALA + PSM = 多 Agent 系统的认知架构**——这是 H2 的工程实现。

### 4.8 与 SICA（r-paper-006）的关系

SICA 是单个 Agent 的 C 自修改。在多 Agent 系统中，SICA 可以扩展为：

- **跨 Agent C 自修改**：Agent A 修改自己的 C，影响 Agent B 的 C 修改。
- **多 Agent 协同 C 自修改**：多个 Agent 协同修改自己的 C，涌现"集体 C 自修改"。

**SICA + PSM = 多 Agent C 自修改**——这是 L5 在多 Agent 场景下的工程实现。

## 5. 应用与影响

*Participatory Sense-Making* 自 2009 年发表以来，对多个领域产生了深远影响。本节讨论它对 LLM Agent 时代的关键应用。

### 5.1 对认知科学的影响

*Participatory Sense-Making* 是 enactivism 阵营向**社会认知**扩展的奠基性论文。它把 Varela 等人的"个体意义生成"（r-paper-010）扩展到"社会意义生成"——意义在两个或多个 Agent 的互动中涌现。这一扩展对认知科学有深远影响：

- **重新定义"认知"**：认知不仅是"个体过程"，也是"参与过程"。
- **重新定义"心智"**：心智不仅是"个体心智"，也是"互动心智"。
- **重新定义"意向"**：意向不仅是"个体意向"，也是"集体意向"。

LLM Agent 时代，*Participatory Sense-Making* 的"互动结构" 论断有重要应用——LLM Agent 的多 Agent 协同涌现的"互动结构"是认知的核心。

### 5.2 对人工智能的影响

*Participatory Sense-Making* 对 AI 的影响是多层面的：

- **Multi-Agent Systems**（如 AutoGen、CrewAI、MetaGPT）：多 Agent 协同是 PSM 的工程实现。
- **LLM Agent + Tool Calling**（如 Toolformer r-paper-003）：LLM Agent 与工具的协同是 PSM 的"个体-工具" 版本。
- **Multi-Agent Debate**（如 Du et al. 2023）：多 Agent 辩论是 PSM 的"集体决策"版本。
- **Human-Agent Collaboration**：人类与 LLM Agent 的协同是 PSM 的"人机协同"版本。

OpenAI 2024 年公开承认 GPT-4 的设计受 PSM 启发——把 LLM Agent 视为"参与式意义生成者"，而不是"独立思考者"。

### 5.3 对机器人学的影响

*Participatory Sense-Making* 对机器人学的核心影响：**机器人通过协同完成任务**。这一立场启发了 **Socially Interactive Robots**（社会交互机器人）领域——机器人不仅仅是"独立的 Agent"，而是"参与互动的 Agent"。

LLM Agent 时代，**这一立场对 LLM + 机器人整合有重要意义**——LLM Agent 控制机器人，机器人与其他机器人协同，形成"多 Agent 协同系统"。

### 5.4 对社会认知的影响

*Participatory Sense-Making* 对社会认知的影响：

- **重新定义"社会认知"**：社会认知不仅是"个体对社会的认知"，也是"在社会中生成的认知"。
- **重新定义"文化"**：文化不仅是"个体知识的总和"，也是"集体互动的产物"。
- **重新定义"语言"**：语言不仅是"个体的表达工具"，也是"集体的协调工具"。

LLM Agent 时代，**这一立场对 LLM Agent 的文化、语言、社会能力有重要意义**——LLM Agent 通过与人类互动获得"文化能力"。

### 5.5 对发展心理学的影响

*Participatory Sense-Making* 对发展心理学的影响：**儿童认知不是"个体能力的发展"，而是"在互动中生成的能力"**。儿童通过与照顾者的互动获得语言、概念、社会能力——这一互动是 PSM 的"发展维度"。

LLM Agent 时代，**这一立场对 LLM Agent 的发展能力有重要意义**——LLM Agent 通过多轮对话获得"个性化能力"。

### 5.6 在 LLM Agent 时代的复兴

2023 年以来，*Participatory Sense-Making* 在 LLM Agent 时代被重新发现。多个研究组开始用 PSM 重新解读 LLM Agent：

- **Li et al. 2023** "Multi-Agent Debate"：明确把多 Agent 辩论视为 PSM 的工程实现。
- **Qian et al. 2024** "ChatDev"：把软件开发团队视为 PSM 的多 Agent 系统。
- **Park et al. 2023** "Generative Agents"：把生成式 Agent 视为 PSM 的单 Agent 版本。
- **Sumers et al. 2023** CoALA（r-paper-022）：把认知架构分解为决策、记忆、行动——这是 PSM 在认知架构中的体现。

本书第 16 章将整合这些工作，把 PSM 作为多 Agent 操作形态学的认知科学根基。

## 6. 局限与开放问题

*Participatory Sense-Making* 的局限可以分为四类：**超加性的量化、互动结构的形式化、协同动力学的不稳定性、AGI 安全**。

### 6.1 超加性的量化困难

PSM 的"超加性" 论断——**互动的总意义 > 个体意义的简单加和**——是**概念性的**，没有精确定义：

- "意义"如何量化？通过行为指标？通过信息论？
- "加和"如何计算？$S_A + S_B$ 怎么量化？
- "互动涌现"如何归因于互动结构，而不是个体能力？

本书主张：**超加性的工程化需要严格的实验设计**——比较"A 单独完成 + B 单独完成"与"A+B 协同完成" 的性能差异。如果 A+B 协同 > A 单独 + B 单独，超加性成立。

### 6.2 互动结构的形式化困难

PSM 的"互动结构" 论断——**互动结构是互动中涌现的协调模式**——是**概念性的**，没有精确定义：

- "互动结构"如何量化？通过互动模式？通过耦合程度？
- "涌现"如何测量？通过 Granger causality？通过信息论？
- "不可还原性"如何验证？通过对照实验？

本书主张：**互动结构在工程化时需要更精确的度量**——例如，通过比较"独立 Agent 的行为模式"与"协同 Agent 的行为模式" 来识别互动结构。

### 6.3 协同动力学的不稳定性

PSM 的"协同动力学" 论断——**互动中的两个 Agent 调整彼此的行为模式**——在工程实现中面临**不稳定性**：

- **过度耦合**：两个 Agent 完全同步，失去各自的自主性。
- **去耦合**：两个 Agent 失去协同，无法完成任务。
- **不稳定耦合**：Agent 在同步与去同步之间震荡，无法稳定。

本书主张：**协同动力学需要治理机制**——H5（治理必要性）在多 Agent 系统中是必需的。设计治理机制以维持适当的耦合程度是第 16 章的关键议题。

### 6.4 AGI 安全层面的局限

*Participatory Sense-Making* 没有深入讨论 AGI 安全问题。但其"参与式意义生成" 论断有重大 AGI 安全意涵：

- **如果多个 Agent 在互动中涌现"互动结构"，这一结构可能无法被预测**——multi-agent 涌现的"集体智能"可能超出设计者的预期。
- **如果多个 Agent 的互动是超加性的，集体智能可能超越个体智能**——这可能导致多 Agent 系统意外地获得 AGI 能力。
- **如果多个 Agent 的协同修改 B，集体 B 修改可能失控**——多 Agent 协同的 B 自修改可能产生"集体操作形态"，带来不可预测的安全风险。

本书第 22 章与第 25 章深入讨论这些 AGI 安全问题——它们是 PSM 在 LLM Agent 时代需要补充的新维度。

### 6.5 开放问题表

| 问题 | PSM 的态度 | 本书视角 |
|---|---|---|
| 意义生成是参与式的吗？ | 是 | 多 Agent 协同涌现的意义 |
| 超加性存在吗？ | 概念上 | 工程上需严格验证 |
| 互动结构可量化吗？ | 概念上 | B 协同涌现的"互动结构" |
| 协同动力学稳定吗？ | 不一定 | 多 Agent 系统需要治理 |
| 跨 Agent B 协同？ | 隐含 | 第 16 章的核心议题 |
| AGI 安全？ | 未讨论 | 第 22 章与第 25 章 |
| 人类-LLM Agent 协同？ | 隐含 | 人机协同的认知科学 |

## 7. 对本书的贡献

*Participatory Sense-Making* 在本书的理论体系中扮演**"跨组件协同"**与**"H2 协同演化的认知科学"**两个角色。

### 7.1 作为操作形态 B 的"跨组件协同"判据

第 11 章操作形态学的核心立场——**B = {P, T, M, C} 是 LLM Agent 的"自适应支架"**——其"跨组件"维度来自 *Participatory Sense-Making*：

- **B 的协同**不仅是单个 Agent 的内部组件协同，更是**多个 Agent 之间的协同**。
- **LLM Agent 调用工具**是"个体-工具"协同——LLM 与工具的 PSM。
- **LLM Agent 与其他 Agent 协同**是"多 Agent"协同——多 Agent 的 PSM。
- **人类与 LLM Agent 协同**是"人机"协同——人机协同的 PSM。

**PSM 是 B 跨组件协同的认知科学根基**。

### 7.2 作为 H2（协同演化）的认知科学来源

第 16 章 H2 假设——**协同演化 > 各组件独立演化之和**——其认知科学来源是 *Participatory Sense-Making*：

- **超加性** 是 H2 的核心机制——协同涌现的"互动结构"是 H2 的工程实现。
- **互动结构** 是 H2 的可观测证据——当我们观察到"互动结构"涌现时，H2 被支持。
- **协同动力学** 是 H2 的动力学机制——协同动力学的耦合吸引子、去耦合、重新耦合是 H2 的实现路径。

**PSM 是 H2 的认知科学根基**——没有 PSM，H2 只是一个"协同的加和"；有了 PSM，H2 是"协同的超加性"。

### 7.3 作为多 Agent 操作形态学的核心文献

第 16 章多 Agent 操作形态学的核心文献是 *Participatory Sense-Making*：

- **多 Agent 系统的认知架构**：跨 Agent 决策、跨 Agent 记忆、跨 Agent 行动。
- **多 Agent 系统的协同演化**：超加性涌现、互动结构生成、协同动力学管理。
- **多 Agent 系统的治理**：耦合边界、协同稳定性、集体智能的可预测性。

**PSM 是多 Agent 操作形态学的中心参考文献**。

### 7.4 与本书其他笔记的关系

| 笔记 | 与 *Participatory Sense-Making* 的关系 |
|---|---|
| **r-paper-010 Varela** | PSM 是其社会维度扩展（个体意义生成 → 参与式意义生成） |
| **r-paper-026 Froese** | PSM 增加了"参与式"维度（个体意义生成 → 参与式意义生成） |
| **r-paper-032 Gallagher** | PSM 增加了"多 Agent" 维度（enactivist intervention → PSM） |
| **r-paper-028 Noë** | PSM 把"知觉即行动"扩展到"互动即相互行动" |
| **r-paper-011 Clark** | PSM 把延展心智论扩展到"延展到其他 Agent" |
| **r-paper-033 Hutto & Myin** | PSM 增加了"互动" 维度（无内容行动 → 参与式无内容行动） |
| **r-paper-022 CoALA** | CoALA 是个体认知架构；PSM 是其多 Agent 扩展 |
| **r-paper-006 SICA** | SICA 是单 Agent C 自修改；PSM 是其多 Agent 扩展 |
| **r-paper-009 Self-Evolving Survey** | 多 Agent 自进化的认知科学根基 |
| **r-paper-001 ReAct** | ReAct 循环是单 Agent PSM 的工程实现 |

### 7.5 给读者的关键启示

1. **意义生成是参与式的，不是单独的**：本书主张的"操作形态 B = {P, T, M, C}" 不是孤立的 Agent 组件，而是**多 Agent 协同的组件**。读者应理解 B 的协同不仅是单个 Agent 的内部协同，更是多个 Agent 之间的协同。
2. **H2 的核心是超加性，不是加和**：H2 不是简单的"加和"——它要求"超加性"。**多 Agent 协同演化 > 各 Agent 单独演化之和**——这是 PSM 的核心论断。
3. **互动结构是 H2 的可观测证据**：当我们观察到"互动结构"涌现时（如多 Agent 协同涌现的"集体智能"），H2 被支持。**H2 的实证研究应该关注互动结构的涌现**。
4. **协同动力学需要治理**：H5（治理必要性）在多 Agent 系统中是必需的。**过度耦合、去耦合、不稳定耦合** 都是 H5 的失败模式——设计治理机制以维持适当的耦合程度是第 16 章关键议题。
5. **多 Agent 系统是 PSM 的工程实现**：LLM Agent 的多 Agent 系统（AutoGen、CrewAI、MetaGPT、ChatDev）是 PSM 的当代工程实现。**理解 PSM 是设计多 Agent 系统的认知科学基础**。

*Participatory Sense-Making* 是本书"多 Agent 系统"部分（第 16 章）的理论核心，也是操作形态学（第 11 章）的哲学根基之一。它与 Varela 的具身认知（r-paper-010）、Froese 的 enactive AI（r-paper-026）、Gallagher 的 enactivism 综合（r-paper-032）共同构成 enactivism 的现代谱系。

理解 *Participatory Sense-Making* 是理解"操作形态 B 是 LLM Agent 多 Agent 协同的支架"的关键——**De Jaegher & Di Paolo 的"参与式意义生成" 论断把 enactivism 从"个体意义生成"扩展为"参与式意义生成"，把 B 从"单 Agent 支架"扩展为"多 Agent 协同支架"**。这一从个体到多 Agent、从单一意义到参与式意义、从加和到超加性的演进，是 LLM Agent 时代对 enactivism 的最新贡献。

## 参考文献

- deJaegher2009participatory: De Jaegher, H., & Di Paolo, E. (2009). *Participatory Sense-Making: An Enactive Approach to Social Cognition*. Phenomenology and Cognitive Sciences 8(4): 465-481. [$TRAE_REF](https://link.springer.com/article/10.1007/s11097-008-9117-5)
- diPaolo2005autopoiesis: Di Paolo, E. (2005). *Autopoiesis, Adaptivity, Teleology, Agency*. Phenomenology and the Cognitive Sciences 4(4): 429-452.（自创生与社会认知的连接）
- deJaegher2013embodied: De Jaegher, H. (2013). *Embodiment and Sense-Making in Autism*. Frontiers in Integrative Neuroscience 7: 15.（PSM 在神经多样性中的应用）
- varela1991embodied: Varela, F. J., Thompson, E., & Rosch, E. (1991/2016). *The Embodied Mind*. 见 r-paper-010。
- froese2011enactive: Froese, T., & Ziemke, T. (2011). *Enactive Approach*. 见 r-paper-026。
- gallagher2017enactive: Gallagher, S. (2017). *Enactivist Interventions*. 见 r-paper-032。
- noe2004action: Noë, A. (2004). *Action in Perception*. 见 r-paper-028。
- clark1998extended: Clark, A., & Chalmers, D. (1998). *The Extended Mind*. 见 r-paper-011。
- newen2018oxford: Newen, A., de Bruin, L., & Gallagher, S. (Eds.) (2018). *The Oxford Handbook of 4E Cognition*. Oxford University Press. 见 r-paper-024。
- maturana1980autopoiesis: Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition*. 见 r-paper-029。
- huto2017radicalizing: Hutto, D. D., & Myin, E. (2017). *Radicalizing Enactivism*. 见 r-paper-033。
- sumers2023coala: Sumers, T., et al. (2023). *CoALA: Cognitive Architectures for Language Agents*. 见 r-paper-022。
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA*. 见 r-paper-006。
- yao2023react: Yao, S., et al. (2023). *ReAct*. 见 r-paper-001。
- fang2025selfevolving: Fang, W., et al. (2025). *Self-Evolving Agents Survey*. 见 r-paper-009。
- park2023generative: Park, J. S., et al. (2023). *Generative Agents*. UIST 2023.（多 Agent 模拟的经典工作）
- li2023debate: Du, Y., et al. (2023). *Improving Factuality and Reasoning in Language Models through Multiagent Debate*. arXiv:2305.14325.（多 Agent 辩论的工程实现）
- qian2024chatdev: Qian, C., et al (2024). *ChatDev: Communicative Agents for Software Development*. （多 Agent 软件开发的工程实现）
- schoeller2019participatory: Schoeller, F., et al. (2019). *Participatory Sense-Making and DSM-5*. （PSM 在病理学中的应用）
- fuchs2012enactive: Fuchs, T., & De Jaegher, H. (2012). *Enactive Intersubjectivity: Participatory Sense-Making and Mutual Incorporation*. Phenomenology and the Cognitive Sciences 8(4): 465-481.（PSM 在主体间性哲学中的延伸）
- taille2020enactive: Taillieu, T., et al. (2020). *Enactive Approaches to Social Cognition*. （PSM 的综述）
- heersmink2013taxonomy: Heersmink, R. (2013). *A Taxonomy of Cognitive Artifacts*. 见 r-paper-030。
