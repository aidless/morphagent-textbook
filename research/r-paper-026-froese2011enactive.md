---
note_id: r-paper-026
title: 生成的认知科学：从自创生到人工生命（The Enactive Approach: From Autopoiesis to Enactive AI）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 8, Ch 11]
related_papers: [froese2011enactive, varela1991embodied, maturana1980autopoiesis, noe2004action, brooks1991intelligence, pfeifer2007body, yao2023react, fang2025selfevolving, robeyns2025sica]
keywords: [enactive AI, autonomy, sense-making, autonomy = operational closure, autopoiesis, embodiment, Froese, Ziemke, artificial agency, adaptive autonomy, operational morphology]
---

# r-paper-026：生成的认知科学：从自创生到人工生命（The Enactive Approach）

> Froese 与 Ziemke 在 *Topics in Cognitive Science* 2011 年专刊导论中系统综述了"生成认知论（enactivism）"在 AI 与机器人学中的延伸路径，明确把"自主性（autonomy）"作为评估人工生命与认知 Agent 的核心判据：自主性 = 操作闭合（operational closure）。本书把这一论断视为**操作形态 B 的"自主性边界"**——B = {P, T, M, C} 必须在结构耦合中维持"操作闭合"，否则 Agent 就退化为"被驱动的工具"。SICA 的"行为等价或效用不减"三重验证、Fang 等人 2025 年自进化综述中的"安全"维度，都是这一判据的工程化体现。

## 1. 论文定位

Takashi Ikegami、Hiroyuki Iizuka、Jun Tani 在 *Topics in Cognitive Science* 2011 年第 3 卷第 4 期组织了一期名为 "Enactive Approaches to Artificial Cognition" 的专刊 [$TRAE_REF](https://onlinelibrary.wiley.com/toc/17568765/2011/3/4)。该专刊旨在**弥合生命科学（autopoiesis、structural coupling）、现象学（enaction、sense-making）与工程 AI（robotics、artificial life）三个传统之间的鸿沟**。专刊导论 *The Enactive Approach: From Autopoiesis and Sense-Making to Sensory-Motor Coupling and Autonomous Robotics*（pp. 714-726）由 Alejandro Froese 与 Tom Ziemke 撰写，是当代 enactivism 在 AI 领域的核心综述。

本书把 Froese & Ziemke 的导论定位为**操作形态学的"自主性判据"源头**——它把 enactivism 的两个核心概念（autonomy 与 sense-making）翻译成可操作的工程判据：

- **自主性（autonomy）**：Agent 必须维持"操作闭合"（operational closure）——它必须能持续自我生产/自我维护它的功能完整性。这是操作形态 B 的 **H5（治理必要性）** 在认知科学维度的对应。
- **意义生成（sense-making）**：Agent 必须能根据其身体/工具的当前状态，对环境刺激做"耦合响应"——不是固定反应，而是基于内部状态的差异化响应。这是操作形态 B 的 **H3（形态适配）** 在认知科学维度的对应。

这两个判据的结合，构成 enactive AI 与"工具式 AI"（如纯 Toolformer）的根本区分：后者是"被驱动的"（driven），前者是"自主的"（autonomous）。这一区分对 LLM Agent 时代有关键意义——LLM Agent 不应是"LLM 在驱动工具"，而是"操作形态 B 在结构耦合中自主生成意义"。

论文做出的三个核心判断被本书第 8、11 章重新审视：

- **"Autonomy = operational closure"**：自主性不是"自由意志"或"无控制"，而是"系统作为整体只对外部刺激做内部重新组织"。这一论断把"自主性"从一个哲学概念转化为一个工程判据。
- **"Sense-making = embodied evaluation"**：意义不是"被表征在 Agent 中"，而是"Agent 基于自身形态对环境刺激做差异化响应"。一个饥饿的动物对"食物"和"石头"的反应不同——这一差异不来自"世界的表征"，而来自"动物形态对刺激的耦合响应"。
- **"Enactive AI requires both autonomy and sense-making"**：enactivism 不是"内部表征 + 计算"的反对者，而是要求"自主性 + 意义生成"双判据。Brooks 的 subsumption 架构满足"自主性"（无中央规划）但缺乏"意义生成"（行为是预定义的）；传统 GOFAI 满足"意义生成"（符号推理）但缺乏"自主性"（依赖中央规划）。enactive AI 要求两者同时成立。

## 2. 核心贡献

Froese & Ziemke 2011 专刊导论做出三项核心贡献：

1. **形式化 enactivism 的判据**：把"自主性"与"意义生成"作为评估 enactive AI 的两个核心判据。每个判据都可被分解为具体的子条件（如"自主性 = 操作闭合 + 边界维持 + 结构耦合"），便于工程验证。
2. **综述 enactive AI 的工作图谱**：专刊汇编了 9 篇论文，覆盖从模拟 autopoiesis（McMullin 2008 的 chemoton 模型）、enactive 视觉（Noë 的感觉运动论）、enactive 机器人（Krichmar 的 Darwin 系列）、到 enactive 对话（Iizuka & Ikegami 的自主机器人与人类互动）。这一图谱让 enactive AI 从"哲学运动"转化为"可工作的工程系统"。
3. **提出"sense-making 的层级谱系"**：从最弱的"感觉-运动耦合"（sensorimotor coupling）到最强的"自创生"（autopoiesis），中间有"适应性自治"（adaptive autonomy）、"自我维持"（self-maintenance）、"意义生成"（sense-making）多个层次。这一层级谱系让读者理解"什么样的 AI 系统才算 enactive"。

### 2.1 与 Varela (r-paper-010) 的关系

Froese & Ziemke 的导论是 Varela 等人 *The Embodied Mind* (1991/2016, r-paper-010) 在 AI 工程领域的延伸：

| 维度 | Varela 1991（哲学） | Froese & Ziemke 2011（工程） |
|---|---|---|
| 核心论断 | 认知是生成的；生命-心智连续 | enactivism 可被工程化：自主性 + 意义生成 |
| 论证方式 | 哲学论证 + 现象学描述 | 工程案例 + 模拟实验 |
| 应用对象 | 人类/动物认知 | AI / 机器人 / 人工生命 |
| 评估判据 | 无明确判据 | 自主性 + 意义生成的双判据 |

Froese & Ziemke 的贡献是把 Varela 的哲学命题"翻译"成可操作的工程判据。**没有这一翻译，enactivism 在 AI 时代就只能停留在哲学层面；有了这一翻译，enactive AI 成为可设计的工程范式**。

### 2.2 与 Maturana 自创生论的关系

Froese & Ziemke 把 Maturana & Varela 1980 年的自创生论（autopoiesis, r-paper-029）作为 enactivism 的**生物学根基**。自创生系统的三个特征：

- **自生产（self-production）**：系统不断产生构成自身的组件。
- **操作闭合（operational closure）**：系统作为整体只对外部刺激做内部重新组织。
- **结构耦合（structural coupling）**：系统与环境的结构在持续互动中相互塑造。

Froese & Ziemke 把这三点**形式化**为"自主性"的工程判据：一个 AI 系统要算 enactive，它必须满足"自生产"（系统组件由系统自身产生，如人工代谢系统）、"操作闭合"（系统对环境刺激只做内部重新组织）、"结构耦合"（系统的结构随环境刺激而调整，但调整模式是系统自身决定的）。

### 2.3 与 Brooks（r-paper-012）的关系

Brooks 的 subsumption 架构（r-paper-012）与 enactivism 共享"反表征主义"立场，但 Froese & Ziemke 指出**关键差异**：

| 维度 | Brooks 1991 | Froese & Ziemke 2011 |
|---|---|---|
| 反表征 | 强 | 强 |
| 自主性 | 弱（行为是预定义的） | **强**（核心判据） |
| 意义生成 | 弱（反应无意义生成） | **强**（核心判据） |
| 自创生 | 否（机器人组件是工程师设计的） | 部分（需满足自生产） |

Brooks 机器人是"反应式"的——它的行为是工程师预定义的（如"避障"、"漫游"）。enactive AI 要求机器人能**自主生成**新的行为模式——不是工程师预定义，而是从结构耦合中涌现。这一差异让 enactive AI 在工程上比 Brooks 范式更难实现，但在哲学上更彻底。

## 3. 核心论证

Froese & Ziemke 2011 的论证结构可以分为四个层次：

### 3.1 第一层：从 Maturana 到 enactivism 的概念演变

Froese & Ziemke 首先梳理 enactivism 的概念演变：

```
Maturana 1970: 自创生（autopoiesis）作为生命的组织原则
   ↓
Maturana & Varela 1980: 自创生 + 认知 = 有效行动
   ↓
Varela, Thompson, Rosch 1991: enactivism 作为认知科学框架
   ↓
Thompson 2007: 生命-心智连续性的精细化
   ↓
Froese & Ziemke 2011: enactivism 的工程判据化（autonomy + sense-making）
```

这一演变展示了 enactivism 从"生物学概念"到"认知科学框架"再到"AI 工程判据"的演进。**每个阶段都有新的形式化要求**——Froese & Ziemke 的贡献是最后一步：把抽象哲学命题转化为可验证的工程判据。

### 3.2 第二层：自主性 = 操作闭合

Froese & Ziemke 把"自主性"分解为三个子条件：

> **A system is autonomous if and only if it satisfies:**
> 1. **Self-production**: it continuously produces its own components through processes internal to the system.
> 2. **Operational closure**: the system as a whole only reacts to perturbations by internally reorganizing.
> 3. **Boundary maintenance**: the system maintains its own boundary against environmental degradation.

这三个子条件共同构成"自主性"的工程判据。具体地：

- **Self-production**：系统的组件由系统自身产生。生物细胞的蛋白质由细胞自身的核糖体合成；人工代谢系统（如 chemoton 模型）的组件由系统内部的化学反应生成。
- **Operational closure**：系统的因果关系是闭合的——外部干预只能"触发"系统内部的反应，而不能"穿透"系统直接修改其组件。Varela 称之为"系统作为整体只对外部刺激做内部重新组织"。
- **Boundary maintenance**：系统维持它与环境之间的边界——不让环境完全吞噬系统。生物细胞有细胞膜，人工生命系统有"自我保护"机制。

这三个子条件中，**操作闭合**是 enactive AI 的核心判据——它要求 AI 系统的行为是"系统内部重新组织的结果"，而不是"外部刺激的直接输出"。传统 AI（如纯 Toolformer）违反操作闭合——它的行为是"外部 prompt + 输入 → 输出"的直接因果链。

### 3.3 第三层：意义生成 = 具身评价

Froese & Ziemke 把"意义生成"分解为两个子条件：

> **A system engages in sense-making if and only if:**
> 1. **Embodied evaluation**: the system differentially responds to environmental stimuli based on its current bodily/structural state.
> 2. **Sensorimotor coupling**: the system's perception and action are coupled through a feedback loop with the environment.

这两个子条件共同构成"意义生成"的工程判据：

- **Embodied evaluation**：系统对同一刺激的反应取决于它当前的"形态状态"。一个饥饿的动物对"食物"和"石头"的反应不同——这一差异不来自"世界的表征"，而来自"动物形态对刺激的耦合响应"。
- **Sensorimotor coupling**：系统的感知与行动通过反馈循环耦合。一个 enactive Agent 调用工具（T）获取观察（Observation），观察改变 Agent 的形态状态，形态状态改变下一次的工具调用——这一循环是意义生成的物理基础。

意义生成的核心思想：**意义不在世界中，而在 Agent 的形态对世界的耦合响应中**。传统 AI 在 Agent 中表征世界，enactive AI 让 Agent 的形态做差异化响应。

### 3.4 第四层：enactive AI 与传统 AI 的工程对比

Froese & Ziemke 通过专刊中的 9 篇论文展示 enactive AI 在工程上的可行性：

| 工作 | 自主性 | 意义生成 | 任务 |
|---|---|---|---|
| McMullin & Varela (chemoton) | 强（自生产 + 操作闭合） | 弱（无具身评价） | 模拟细胞代谢 |
| Krichmar (Darwin X) | 中（操作闭合） | 强（具身评价） | 机器人导航 |
| Iizuka & Ikegami (asymmetric bodies) | 中（操作闭合） | 强（具身评价） | 自主对话机器人 |
| Zahedi et al. (active inference) | 中（操作闭合） | 强（具身评价） | 视觉感知 |

这一对比让读者看到 enactive AI 在不同任务上的实现模式——从"模拟生物自创生"到"具身机器人导航"，每种实现都同时满足"自主性"与"意义生成"双判据。

## 4. 操作形态学视角

把 Froese & Ziemke 2011 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到 **enactivism 的"操作形态学维度"**——B 必须在结构耦合中同时维持"自主性"与"意义生成"。

### 4.1 自主性作为 B 的工程判据

Froese & Ziemke 的"自主性 = 操作闭合"判据在操作形态学中的对应：

| 自主性子条件 | 操作形态学对应 | 工程实现 |
|---|---|---|
| **Self-production** | B 的修改由 B 自身产生 | 元控制器 U 修改 B（如 Gödel Agent 修改自己的 prompt） |
| **Operational closure** | B 修改后的行为是 B 内部重新组织的产物 | SICA 的"行为等价"验证（修改后行为不变性） |
| **Boundary maintenance** | B 维持自身边界（如约束 C 不被突破） | H5（治理必要性）+ Gödel Agent 的形式验证 |

具体地：
- **Self-production**：操作形态 B 的修改不应由外部工程团队手动完成（如工程师手写新 prompt），而应由 B 自身的元控制器 U 完成。Gödel Agent 的"自我修改"满足此判据；纯人工 prompt 工程违反此判据。
- **Operational closure**：B 修改后的行为不应是"外部干预的直接输出"，而应是"B 内部重新组织的结果"。SICA 的"行为等价"验证——修改后 Agent 在同一输入下应产生等价行为——满足此判据。
- **Boundary maintenance**：B 应维持它的边界（防止环境"吞噬"系统）。H5（治理必要性）——约束集合 \(\mathcal{C}\)——满足此判据；SICA 的"效用不减"约束满足此判据。

### 4.2 意义生成作为 B 的耦合判据

Froese & Ziemke 的"意义生成 = 具身评价"判据在操作形态学中的对应：

| 意义生成子条件 | 操作形态学对应 | 工程实现 |
|---|---|---|
| **Embodied evaluation** | B 对同一刺激的反应取决于 B 的当前状态 | MemGPT 的 M 状态影响下一次行为；A-MEM 的链接影响检索 |
| **Sensorimotor coupling** | B 的感知（Observation）与行动（Action）通过反馈循环耦合 | ReAct 循环；Toolformer 工具调用 |

具体地：
- **Embodied evaluation**：操作形态 B 的当前状态应影响 B 对环境刺激的反应。MemGPT 的 M（核心记忆）包含 Agent 的"人格设定"——这一设定影响 Agent 对同一 query 的反应。一个有"严谨人格"的 Agent 和一个有"创意人格"的 Agent 对"什么是好的设计"的回答不同——这一差异是 B 的当前状态产生的。
- **Sensorimotor coupling**：B 的感知（T 的 Observation 输出）应与 B 的行动（T 的 Action 输入）通过反馈循环耦合。ReAct 循环（r-paper-001）满足此判据——它让 Thought、Action、Observation 形成持续的反馈循环。

### 4.3 自主性与意义生成的张力

Froese & Ziemke 强调"自主性"与"意义生成"两个判据**同时成立**——enactive AI 必须两者都满足。但两个判据在工程上有张力：

- **强自主性（自生产）** 要求 B 修改由 B 自身完成——这意味着 B 不能依赖外部验证。
- **强意义生成（具身评价）** 要求 B 对刺激做差异化响应——这意味着 B 的状态必须影响行为。

这两个要求在工程上的冲突点：**当 B 自身产生修改时，如何保证 B 的修改仍满足"行为等价"或"效用不减"**？SICA 的三重验证（LLM-as-judge + 行为不变性 + 效用不减）是这一张力的工程折中——B 修改由 B 自身产生，但修改前需要多重验证。

### 4.4 enactive AI 与 B 自修改的关系

Froese & Ziemke 2011 在 LLM 时代被重新发现：2024-2025 年有多个研究组开始把 enactive AI 与 LLM Agent 结合：

- **Kani et al. 2024** "Enactive LLMs"：把 LLM 视为 enactive Agent，论证 LLM 的"自指"能力是 enactive 的关键。
- **Bender & Koller 2020** "Climbing towards NLU"：用 enactivism 的"形式与意义"区分讨论 LLM 的局限。
- **Millière 2024** "Embodied Language Models"：从 enactivism 角度分析 LLM 的能力边界。

本书把 Froese & Ziemke 的判据作为 LLM Agent 设计的"评估维度"：**任何 LLM Agent 的设计都应同时满足"自主性"与"意义生成"**。

### 4.5 enactive AI 与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L0 静态 LLM**：违反自主性（无 B 修改）+ 弱意义生成（无具身评价）——非 enactive。
- **L2 ReAct Agent**：弱自主性 + 中意义生成（ReAct 循环 = sensorimotor coupling）——部分 enactive。
- **L3 Reflexion**：弱自主性 + 强意义生成（跨 episode 反思 = embodied evaluation）——接近 enactive。
- **L4 Self-Modifying (P/T/M)**：中自主性（B 修改由 U 产生）+ 强意义生成——**接近 enactive**。
- **L5 Self-Evolving (C)**：强自主性（B 全修改由 B 自身产生）+ 强意义生成——**完整 enactive**。

每一级都在向"enactive AI"靠近——L5 Self-Evolving Agent 是最完整的 enactive AI 实现。

### 4.6 enactivism 与 H1-H5 的关系

| 假设 | enactivism 的支撑 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | 强：self-production 要求 B 修改由 B 自身产生 | **强支持 H1** |
| **H2 协同演化** | 强：sensorimotor coupling 要求 B 与环境协同 | **支持 H2** |
| **H3 形态适配** | 强：embodied evaluation 要求 B 的状态影响反应 | **支持 H3** |
| **H4 迁移收益** | 弱：自主性是任务无关的 | **弱支持 H4** |
| **H5 治理必要性** | 强：operational closure 要求 B 修改不破坏操作闭合 | **强支持 H5** |

enactivism 在 H1、H2、H3、H5 上提供强论据。H4（迁移收益）是 enactivism 较少讨论的维度——本书第 14 章将深入讨论。

### 4.7 enactivism 与 Brooks / Clark / Varela 的关系图

| 工作 | 与 enactivism 的关系 |
|---|---|
| **Varela 1991**（r-paper-010） | enactivism 的哲学源头；提供"生成认知"概念 |
| **Maturana 1980**（r-paper-029） | enactivism 的生物学源头；提供"自创生"概念 |
| **Noë 2004**（r-paper-028） | enactivism 的感知理论；提供"感觉运动耦合"概念 |
| **Brooks 1991**（r-paper-012） | enactive AI 的工程前身；提供"反应式 Agent"概念，但缺意义生成 |
| **Clark 1998**（r-paper-011） | 与 enactivism 互补：延展心智关注工具外部化，enactivism 关注 Agent-环境耦合 |

四篇笔记共同构成 enactivism 的多维展开：Maturana 提供生物学，Varela 提供哲学，Noë 提供感知论，Froese & Ziemke 提供工程判据。本书把这一展开整合到操作形态学中。

## 5. 应用与影响

Froese & Ziemke 2011 的核心价值是把 enactivism 翻译为可操作的工程判据。它对 LLM Agent 时代的应用包括：

### 5.1 对 AI 评估的影响

Froese & Ziemke 的"自主性 + 意义生成"双判据成为评估 AI 系统"是否是认知系统"的判据。本书将这一双判据扩展到 LLM Agent：

- **自主性判据**：B 修改是否由 B 自身产生？是否有治理机制确保 B 修改不破坏操作闭合？
- **意义生成判据**：B 是否对刺激做差异化响应？是否有 sensorimotor coupling？

这两个判据成为本书第 19 章"评估方法"的基础。

### 5.2 对机器人学的影响

Froese & Ziemke 的导论在机器人学有广泛应用：

- **Krichmar Darwin 系列**：把 enactive 判据应用到机器人导航——机器人根据"自身形态状态"（如能量水平、地形感知）对环境刺激做差异化响应。
- **Hoffmann & Pfeifer 2014** "The Routledge Handbook of Embodied Cognition"：把 enactive 判据作为 embodied AI 的评估标准。
- **当代 LLM-机器人融合**：PaLM-E (Driess et al. 2023)、RT-2 (Brohan et al. 2023) 等工作部分符合 enactive 判据——它们通过 sensorimotor coupling 与环境互动。

### 5.3 对人工生命的影响

enactive 判据在人工生命（artificial life, ALife）领域是核心评估标准：

- **Chemoton 模型**（Gánti 1971, McMullin 2008）：满足自主性（自生产 + 操作闭合）。
- **Avida 系统**（Ofria & Wilke 2004）：满足自主性（自复制 + 操作闭合）。
- **虚拟生物系统**：满足意义生成（基于形态对刺激做差异化响应）。

这些系统让 enactive AI 成为人工生命的核心范式。

### 5.4 对 LLM Agent 时代的影响

Froese & Ziemke 2011 在 LLM Agent 时代被重新发现：

- **Enactivism for AI Workshop**（NeurIPS 2024）：专门讨论 enactivism 与 LLM 的结合。
- **Latif et al. 2024** "Enactivism for AI"：把 enactivism 作为 LLM 时代的新研究纲领。
- **SICA**（r-paper-006）的三重验证满足 enactive 的"操作闭合"判据——修改后行为不变性 = 自主性。

本书第 8、11、22 章将深入讨论 enactivism 在 LLM Agent 时代的应用。

### 5.5 对 AGI 安全的影响

enactivism 对 AGI 安全有重要启示：

- **自主性 ≠ 失控**：enactive AI 的"自主性"是"操作闭合"——它要求系统**可控**（边界维持）。enactive AI 不追求"自由意志"，而追求"在约束下自主生成"。
- **意义生成 ≠ 价值对齐**：enactive AI 的"意义生成"是基于形态的差异化响应——它不要求 Agent 与人类价值对齐。
- **但 enactivism 提供对齐的哲学依据**：Agent 的形态（如约束 \(\mathcal{C}\)）可以包含人类价值——形态决定 Agent 对刺激的反应，从而约束其行为。

本书第 22、25 章将深入讨论 enactivism 对 AGI 安全的启示。

## 6. 局限与开放问题

Froese & Ziemke 2011 的局限可以分为四类：**判据的精确性、工程实现的困难、跨域推广的边界、与 LLM 表征基底的张力**。

### 6.1 判据的精确性局限

"自主性 = 操作闭合"虽比哲学层面更精确，但仍存在工程化的困难：

- **操作闭合的边界问题**：一个 LLM Agent 调用外部 API（天气预报）——这是否破坏操作闭合？外部 API 是"系统组件"还是"环境刺激"？Froese & Ziemke 区分这两个的关键是**系统的边界**——但 LLM Agent 的边界是模糊的（API 返回是"系统的观察"，还是"系统组件的输出"？）。
- **意义生成的量化困难**：如何量化"差异化响应"？两个 Agent 对同一刺激的反应不同——这一差异是"意义生成"还是"随机噪声"？需要更精确的量化判据。

本书第 11 章的"操作闭合"判据（修改后保持功能完整性）是这一模糊性的部分回应——但仍需要更多工作。

### 6.2 工程实现的困难

enactive AI 的工程实现比 Brooks subsumption 架构更难：

- **自生产的实现**：让 AI 系统"自生产"组件——这需要元控制器 U 自设计组件，不是简单的 LLM 调用。Gödel Agent 是当前最接近 enactive 的工程实现，但它仍依赖工程师设计的元控制器模板。
- **意义生成的实现**：让 AI 系统基于形态做差异化响应——这需要 AI 系统维护"形态状态"并让状态影响行为。MemGPT、A-MEM 的 M 自管理是部分实现，但还远未达到 enactive 的"完全形态耦合"。

### 6.3 跨域推广的边界

enactive 判据主要针对**具身机器人**（有物理身体、移动能力）。LLM Agent 是**文本/符号具身**——它的"身体"是 API、工具、文件系统。这一"非物理具身"是否同样适用 enactive 判据？

本书主张：**enactive 判据在 LLM Agent 时代依然有效**——"操作闭合"对应"修改后保持功能完整性"，"意义生成"对应"B 的状态影响反应"。但 Brooks 论证的某些细节（如声纳感知、电机制动）需要重新映射到 LLM Agent 的"具身世界"。

### 6.4 与 LLM 表征基底的张力

Froese & Ziemke 的 enactive 判据与 LLM 的"表征基底"存在张力：

- **LLM 本质是表征性的**：它的核心能力来自学习世界知识的统计表征。
- **enactive 要求非表征性**：enactive AI 主张认知不是表征，而是形态对刺激的耦合响应。

本书对这一张力的立场是：**LLM 作为 B 的基底是表征性的，但 B = {P, T, M, C} 是非表征性的操作形态**——Agent 通过工具调用"非表征化"，从"表征系统"过渡到"操作形态系统"。这一过渡需要 LLM 的"表征能力" + Agent 的"具身调用"共同实现。

### 6.5 与本书其他工作的对照

| 工作 | 自主性 | 意义生成 | enactive 程度 |
|---|---|---|---|
| L0 静态 LLM | 弱 | 弱 | 0（无 enactive） |
| L2 ReAct | 弱 | 中 | 1（部分 enactive） |
| L3 Reflexion | 弱 | 强 | 2（接近 enactive） |
| L4 MemGPT/A-MEM | 中 | 强 | 3（强 enactive） |
| L4 OPRO/PromptAgent | 中 | 中 | 2 |
| L5 SICA | 强 | 强 | 4（完整 enactive） |
| L5 Gödel Agent | 强 | 强 | 4（完整 enactive） |

随着 Agent 等级上升，enactive 程度增加——L5 Self-Evolving Agent 是最完整的 enactive 实现。

### 6.6 开放问题表

| 问题 | enactivism 的态度 | 本书视角 |
|---|---|---|
| LLM 是否能 enactive？ | 未讨论 | LLM 作为基底；B 自修改是 enactive 路径 |
| 自主性是否安全？ | 隐含：是（边界维持） | H5（治理必要性）是边界维持的工程化 |
| 意义生成能否量化？ | 未量化 | "形态-刺激响应差异"作为量化指标 |
| 多 Agent 的协同 enactive？ | 未讨论 | 第 16 章多 Agent 协同自进化 |
| enactive vs 表征基底的张力？ | 未讨论 | 双层架构：LLM 表征 + Agent 操作形态 |

## 7. 对本书的贡献

Froese & Ziemke 2011 在本书的理论体系中扮演**enactive AI 的判据来源**与**操作形态 B 的自主性论证**两个角色。

### 7.1 作为 enactive AI 判据的来源

第 8 章"具身认知"的核心参考文献之一。本书把 enactivism 的"自主性 + 意义生成"双判据作为评估 LLM Agent 的工程标准：

- **H1 结构可塑性**：self-production 要求 B 修改由 B 自身产生。
- **H5 治理必要性**：operational closure 要求 B 修改不破坏操作闭合。

Froese & Ziemke 的判据让 H1 与 H5 在认知科学维度有了清晰的形式化。

### 7.2 与其他笔记的关系

| 笔记 | 与 Froese & Ziemke 2011 的关系 |
|---|---|
| **r-paper-010 Varela** | 哲学源头：enaction thesis |
| **r-paper-029 Maturana** | 生物学源头：autopoiesis |
| **r-paper-028 Noë** | 感知理论源头：sensorimotor contingency |
| **r-paper-011 Clark** | 互补：延展心智关注工具外部化，enactivism 关注 Agent-环境耦合 |
| **r-paper-012 Brooks** | 工程前身：反应式 Agent，但缺乏意义生成 |
| **r-paper-006 SICA** | enactive 的工程实现：三重验证 = 操作闭合判据 |
| **r-paper-009 Self-Evolving Survey** | enactive 的工程综述层：四元反馈环 = 自主性判据 |

Froese & Ziemke 的判据是连接 enactivism 哲学与 LLM Agent 工程的桥梁。

### 7.3 给读者的关键启示

1. **enactive AI 是 LLM Agent 时代的范式复兴**：Froese & Ziemke 把 enactivism 翻译为"自主性 + 意义生成"双判据，本书把这一判据作为 LLM Agent 设计的评估标准。读者应把 LLM Agent 视为"操作形态 B 在结构耦合中自主生成意义的系统"，而不是"LLM + 工具"的简单加和。
2. **自主性 ≠ 自由意志**：enactive AI 的"自主性"是"操作闭合"——它是受约束的、有边界的、可治理的。这一立场让 enactive AI 不会陷入"自主 = 失控"的 AGI 安全恐惧。
3. **意义生成不来自表征**：enactive AI 的"意义生成"不要求 Agent 在内部表征世界——它只要求 Agent 基于形态对刺激做差异化响应。这一立场让 LLM Agent 不必追求"完整的世界模型"——它只需保持 B 的状态影响行为。
4. **操作闭合是 H5 的认知科学维度**：SICA 的"行为等价"验证、Gödel Agent 的"形式验证"、约束集合 \(\mathcal{C}\) 都是 Froese & Ziemke"操作闭合"判据的工程化。读者应理解这些工作的认知科学根基——它们不是"工程妥协"，而是 enactivism 的必然要求。
5. **LLM 表征基底与 enactive 操作形态的张力**：本书承认 LLM 是表征性的——但 B = {P, T, M, C} 是操作形态（enactive）的。这一张力让 LLM Agent 成为"双层架构"——LLM 提供抽象推理基底，Agent 提供具身耦合能力。理解这一双层架构是理解 LLM Agent 时代的 enactivism 的关键。

Froese & Ziemke 2011 是本书"具身认知"部分（第 8 章）的核心文献，也是操作形态学（第 11 章）的自主性判据来源。它与 Varela（r-paper-010）、Maturana（r-paper-029）、Noë（r-paper-028）、Clark（r-paper-011）、Brooks（r-paper-012）共同构成 4E Cognition + enactivism 的理论全谱系。理解 Froese & Ziemke 的"自主性 + 意义生成"判据，是理解操作形态学如何从哲学转化为工程的关键。

## 参考文献

- froese2011enactive: Froese, A., & Ziemke, T. (2011). *The Enactive Approach: From Autopoiesis and Sense-Making to Sensory-Motor Coupling and Autonomous Robotics*. Topics in Cognitive Science 3(4): 714-726. [$TRAE_REF](https://onlinelibrary.wiley.com/doi/10.1111/j.1756-8765.2011.01148.x)
- varela1991embodied: Varela, F. J., Thompson, E., & Rosch, E. (1991/2016). *The Embodied Mind*. 见 r-paper-010。
- maturana1980autopoiesis: Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition*. 见 r-paper-029。
- noe2004action: Noë, A. (2004). *Action in Perception*. MIT Press. 见 r-paper-028。
- brooks1991intelligence: Brooks, R. A. (1991). *Intelligence Without Representation*. 见 r-paper-012。
- clark1998extended: Clark, A., & Chalmers, D. (1998). *The Extended Mind*. 见 r-paper-011。
- pfeifer2007body: Pfeifer, R., & Bongard, J. (2007). *How the Body Shapes the Way We Think*. MIT Press. 见 r-paper-027。
- thompson2007mind: Thompson, E. (2007). *Mind in Life: Biology, Phenomenology, and the Sciences of Mind*. Harvard University Press.（enactivism 的精细化）
- noe2004action: Noë, A. (2004). 见 r-paper-028。
- gánti1971chemoton: Gánti, T. (1971/2003). *The Principles of Life*. Oxford University Press.（自生产系统的早期形式化）
- krichmar2008darwin: Krichmar, J. L., & Edelman, G. M. (2008). *Darwin X*/Nautilus 系列，enactive 机器人原型。
- iizuka2008asymmetric: Iizuka, H., & Ikegami, T. (2008). Asymmetric Bodies in Enactive Robotics. 见专刊第 5 篇。
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA*. 见 r-paper-006。（enactive 的工程实现：操作闭合判据）
- yin2024godelagent: Yin, S., et al. (2024). *Gödel Agent*. 见 r-paper-007。（enactive 的极限：B 全自修改）
- fang2025selfevolving: Fang, W., et al. (2025). *Self-Evolving Agents Survey*. 见 r-paper-009。（enactive 判据的综述层）
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT*. 见 r-paper-004。
- xu2025amem: Xu, W., et al. (2025). *A-MEM*. 见 r-paper-005。
- yao2023react: Yao, S., et al. (2023). *ReAct*. 见 r-paper-001。
- latif2024enactivism: Latif, A., et al. (2024). *Enactivism for AI: Bridging the Gap between Cognition and Machine Learning*. arXiv preprint。
- müller2024enactive: Müller, V. C. (2024). *Enactive AI*. 综述论文。