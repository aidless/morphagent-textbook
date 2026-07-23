---
note_id: r-paper-024
title: Oxford 4E Cognition 手册：Embodied/Embedded/Enacted/Extended + Enactive + Ecological 与操作形态学的理论根源
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 7, Ch 8, Ch 11]
related_papers: [newen2018oxford, varela1991embodied, clark1998extended, brooks1991intelligence, sumers2023coala, yao2023react, packer2023memgpt, fang2025selfevolving]
keywords: [4E cognition, embodied, embedded, enacted, extended, enactive, ecological, operational morphology, agent-body, tool-as-organ, B = {P, T, M, C} theoretical foundation]
---

# r-paper-024：Oxford 4E Cognition 手册：Embodied/Embedded/Enacted/Extended + Enactive + Ecological 与操作形态学的理论根源

> Albert Newen、Leon de Bruin、Shaun Gallagher 主编的 *The Oxford Handbook of 4E Cognition*（Oxford University Press, 2018 [$TRAE_REF](https://academic.oup.com/book/2753)）是 4E Cognition 运动最具权威性的综述手册——它系统化呈现了 Embodied（具身）、Embedded（嵌入）、Enacted（行动生成）、Extended（延展）四个"E"，并整合了 Enactive（生成）与 Ecological（生态）两个相关传统。本书将这本手册定位为**操作形态学的哲学理论根源**——4E Cognition 回答"认知是否依赖身体、嵌入环境、通过行动生成、延展到外部"，而操作形态学 B = {P, T, M, C} 回答"LLM Agent 的认知结构是否依赖其组件、嵌入环境、通过工具行动、延展到外部工具与记忆"。两者的概念结构高度同构——本书用 4E Cognition 作为 B 框架的哲学根基。

## 1. 论文定位

Albert Newen、Leon de Bruin、Shaun Gallagher 主编的 *The Oxford Handbook of 4E Cognition*（Oxford University Press, 2018 [$TRAE_REF](https://academic.oup.com/book/2753)）是 4E Cognition 运动的"标准参考手册"。4E Cognition 是认知科学中一个相对年轻但极具影响力的传统，主张**认知不能被还原为大脑内部的抽象计算**——它必然依赖身体（Embodied）、嵌入环境（Embedded）、通过行动生成（Enacted）、延展到外部（Extended）。这本手册汇集了 40+ 篇综述章节，由 Gallagher、Clark、Chemero、Noë、Thompson、Hutto 等 4E Cognition 的核心学者撰写，是该领域的权威理论资源。

本书把 Oxford 4E Cognition 手册定位为**操作形态学 B 框架的哲学理论根源**——4E Cognition 回答的是"人类/动物认知的结构"，而 B = {P, T, M, C} 回答的是"LLM Agent 认知的结构"。两者的概念结构高度同构：

| 4E 概念 | 哲学问题 | B = {P, T, M, C} 对应 | LLM Agent 含义 |
|---|---|---|---|
| **Embodied** | 认知是否依赖身体？ | P + C | LLM 是 Agent 的"身体"（神经形态） |
| **Embedded** | 认知是否嵌入环境？ | M（部分） | Agent 嵌入真实环境 |
| **Enacted** | 认知是否通过行动生成？ | T + C | Agent 通过工具调用行动 |
| **Extended** | 认知是否延展到外部？ | T + M（外存部分） | 工具与外部记忆是认知的一部分 |

这一对应不是偶然——**4E Cognition 与操作形态学都关注"认知的结构"问题**，只是应用对象不同（人类/动物 vs LLM Agent）。本书用 4E Cognition 作为 B 框架的哲学根基，让 LLM Agent 的形态学设计有可参照的理论传统。

手册的三个核心论断被本书第 7、8、11 章重新审视：

- **"Cognition is embodied, embedded, enacted, and extended"**——4E Cognition 主张认知的四个"E"是**协同的、不可分割的**——认知不是某个"E"，而是四个"E"的整合。本书第 11 章的 H2 假设（协同演化）正是这一观点的 LLM Agent 版本。
- **"The body is not just input/output, but constitutive of cognition"**——身体不只是接收输入和输出动作的"管道"，而是**认知本身的一部分**。本书第 11 章主张 T 不只是工具调用接口，而是 Agent 认知的**构成性组件**。
- **"Cognitive boundaries are fluid, not fixed"**——认知的边界不是固定的（如"颅骨内"），而是**根据任务动态变化的**（如 Otto 的笔记本）。本书第 14 章的 M 边界演化正是这一观点的 LLM Agent 版本。

这三个论断共同构成本书操作形态学的**哲学理论根基**：LLM Agent 的 B 不是一个静态、固定的组件集合，而是一个**动态、可塑、嵌入环境的形态系统**。

## 2. 核心贡献

Oxford 4E Cognition 手册（Newen 等人主编）汇集了 40+ 章节，覆盖 4E Cognition 的所有核心议题。本笔记重点分析与操作形态学相关的贡献：

### 2.1 四个 E 的精确定义

手册第一章（Rowlands, 2018）给出四个"E"的标准定义：

**Embodied Cognition（具身认知）**：
- **核心论断**：认知过程依赖身体的物理特性（形态、感觉器官、运动能力）。
- **证据**：行为研究、神经科学、机器人学——例如我们理解"推"这个动词依赖我们的肌肉运动经验。
- **强 vs 弱 embodied**：强 embodied 主张"认知即身体"（如 Noë 的 enactive approach）；弱 embodied 主张"认知受身体影响但仍可独立分析"。

**Embedded Cognition（嵌入认知）**：
- **核心论断**：认知发生在具体的环境中，环境是认知过程的组成部分。
- **证据**：生态心理学（Hutafford, Gibson）、情境认知（Suchman）——例如导航依赖环境中的地标，而非纯空间记忆。
- **与 embodied 的区别**：embodied 强调身体，embedded 强调环境。

**Enacted Cognition（行动生成认知）**：
- **核心论断**：认知不是表征的处理，而是通过行动生成的。
- **证据**：Noë 的感知理论、Varela 的 neurophenomenology、行动者-感知者循环——例如视觉不是"看图像"，而是"在环境中移动以探查"。
- **核心方法**：强调 sensorimotor coupling（感知-运动耦合）。

**Extended Cognition（延展认知）**：
- **核心论断**：认知可以延展到身体之外（如笔记本、计算器、其他人的头脑）。
- **证据**：Clark & Chalmers 的 Otto 案例、Hutchins 的航海分布式认知。
- **核心争议**：什么算"延展"？笔记本算，Google 算吗？

### 2.2 Enactive 与 Ecological 的整合

除了四个"E"，手册还整合了两个相关传统：

**Enactive Approach（生成方法，Noë, Varela, Thompson）**：
- 强调"认知是行动生成的"——认知不是表征的处理，而是世界与认知者的耦合。
- 与 embodied 重叠但更激进：enactive 主张**认知没有表征**（无表征主义）；embodied 仍接受表征但强调身体。

**Ecological Approach（生态方法，Gibson, Chemero）**：
- 强调"环境提供 affordance"——环境不只是背景，而是直接提供行动可能性。
- 与 embedded 重叠但更激进：ecological 主张**认知即环境与认知者的直接耦合**（无表征、无计算）。

手册把 enactive 与 ecological 视为 4E 的"激进版本"——它们比 embodied/embedded 更彻底地反对传统认知科学的"内部表征 + 计算"模型。

### 2.3 关键案例与思想实验

手册汇集了多个关键案例：

**Otto 案例（Clark & Chalmers）**：
- 失忆症患者 Otto 把笔记本带在身上，记录所有重要信息。
- 论证：Otto 的笔记本与正常人的生物记忆在功能上等价——认知可以延展到笔记本。
- 本书关联：MemGPT 的 archival storage 就是 Agent 的"Otto 笔记本"。

**Hutchins 分布式认知（Distributed Cognition）**：
- 飞机驾驶舱的导航系统：飞行员、仪表、自动驾驶系统共同完成"导航认知"。
- 论证：认知可以分布在多个体（包括非人）之间。
- 本书关联：多 Agent 系统是分布式认知的工程实现。

**Affordance（Gibson, Chemero）**：
- 椅子 afford "坐"、门 afford "打开"——环境直接提供行动可能性。
- 论证：认知不需要内部表征——世界本身提供"信息"。
- 本书关联：Agent 的 T 提供 affordance——工具的 schema 直接提供"可调用的能力"。

### 2.4 与经典认知科学（computationalism）的边界

手册系统比较了 4E Cognition 与经典认知科学（computationalism / cognitivism）：

| 维度 | 经典认知科学 | 4E Cognition |
|---|---|---|
| **认知的本质** | 表征的计算 | 身体-环境-行动的耦合 |
| **认知的位置** | 大脑内部 | 大脑+身体+环境+外部工具 |
| **认知的方法** | 输入-计算-输出 | 感知-运动循环 |
| **认知的边界** | 颅骨内 | 流体（动态） |
| **AI 的对应** | GOFAI（Good Old-Fashioned AI） | 具身 AI、机器人学 |

这一比较为操作形态学提供了**理论坐标系**——LLM Agent 是处于哪个传统的工程实现？

### 2.5 对 AI 与认知科学的影响

4E Cognition 对 AI 研究的深远影响：

- **具身 AI（Embodied AI）**：机器人、虚拟代理的设计强调物理身体。
- **情境 AI（Situated AI）**：Agent 设计强调环境交互。
- **行动生成 AI（Enactive AI）**：Agent 设计强调主动感知-运动。
- **延展 AI（Extended AI）**：Agent 设计强调工具与外部记忆。

LLM Agent 是这一传统下的"现代版本"——LLM 是"大脑"、工具是"身体延伸"、环境是"情境"、记忆是"延展"。本书用 4E Cognition 作为 LLM Agent 形态学的哲学根基。

## 3. 核心论证

Oxford 4E Cognition 手册不是单一论文，而是**40+ 章节的综述合集**。本节提取与操作形态学相关的核心论证，并把它形式化。

### 3.1 论证 1：Embodied Cognition 的身体依赖性

**核心论点**：认知过程依赖身体的物理特性。

**证据 1（神经科学）**：镜像神经元——我们理解"抓取"这个动作激活与我们自己抓取相同的神经回路。
**证据 2（机器人学）**：波士顿动力机器人——形态（腿的数量、关节的位置）决定了运动控制的可行性。
**证据 3（语言理解）**：embodied semantics——我们理解"踢"激活运动皮层，而不仅仅是抽象语义。

**形式化**：

$$
\text{Cognition} = f(\text{Brain}, \text{Body}, \text{Environment})
$$

认知是身体、大脑、环境的函数，而非仅大脑的函数。

**操作形态学对应**：LLM 是 Agent 的"大脑"，但**认知不是仅 LLM 的**——还依赖 T（工具调用能力）、M（记忆访问能力）、C（执行逻辑）。P 包含了 embodied 因素——few-shot examples 是 Agent 的"运动经验"。

### 3.2 论证 2：Embedded Cognition 的环境嵌入性

**核心论点**：认知发生在具体的环境中，环境是认知的组成部分。

**证据 1（生态心理学）**：Gibson 的 affordance——环境提供直接的"行动可能性"，不需要内部表征。
**证据 2（情境认知）**：Suchman 的 Plans and Situated Actions——计划不是预先制定的，而是根据情境动态调整的。
**证据 3（导航研究）**：人类导航依赖环境中的地标，而非纯空间记忆（McNamara 1986）。

**形式化**：

$$
\text{Cognition}(t) = g(\text{Agent}(t), \text{Environment}(t))
$$

认知是 Agent 与环境的动态耦合。

**操作形态学对应**：Agent 嵌入真实环境——通过 M（外部记忆）、T（外部工具）与环境交互。M 的"embedded"部分（archival storage）是 Agent 与环境耦合的载体。

### 3.3 论证 3：Enacted Cognition 的行动生成性

**核心论点**：认知不是表征的处理，而是通过行动生成的。

**证据 1（Varela 的神经现象学）**：认知是大脑、身体、环境的相互生成——意识不是"看图像"，而是"探查世界"。
**证据 2（Noë 的感知理论）**：视觉不是"看到图像"，而是"在世界中移动以探查"。
**证据 3（机器人学中的行动-感知循环）**：行为机器人通过感知-行动循环完成任务，无需内部表征。

**形式化**：

$$
\text{Cognition} \equiv \text{Action-Perception Loop}
$$

认知等价于感知-行动循环。

**操作形态学对应**：Agent 的认知是 **ReAct 循环**（r-paper-001）——Thought-Action-Observation 是 LLM Agent 的感知-行动循环。C（核心循环）就是 Agent 的 enacted cognition 实现。

### 3.4 论证 4：Extended Cognition 的延展性

**核心论点**：认知可以延展到身体之外，包括工具、笔记、其他人的头脑。

**证据 1（Otto 案例）**：失忆症患者 Otto 的笔记本在功能上等价于正常人的生物记忆。
**证据 2（Hutchins 分布式认知）**：飞机驾驶舱的导航认知分布在飞行员、仪表、自动驾驶系统之间。
**证据 3（数学工具）**：数学家使用符号（π、∫）作为认知延展——这些符号是"外部记忆"。

**形式化**：

$$
\text{Cognition}_{\text{extended}} = \text{Cognition}_{\text{brain}} + \text{Cognition}_{\text{tool}} + \text{Cognition}_{\text{environment}}
$$

认知延展是大脑+工具+环境的总和。

**操作形态学对应**：Agent 的认知延展到 T（工具）和 M（外部记忆）——LLM 自身是"大脑"，工具调用是"认知延展"，长期记忆是"外部笔记本"。MemGPT（r-paper-004）的 archival storage 是 Agent 的"延展认知"——它在功能上等价于 Agent 的长期记忆。

### 3.5 论证 5：四个 E 的协同性

**核心论点**：四个 E 不是独立的，而是协同的、不可分割的——认知是四个 E 的整合。

**证据 1（Varela 的"三个朋友"故事）**：一个机器人需要身体、环境、行动、外部工具才能完整认知。
**证据 2（进化论）**：认知能力的演化必然涉及身体、环境、行动、外部工具的协同。
**证据 3（病理案例）**：身体损伤、环境剥夺、行动限制、外部工具移除都会导致认知障碍。

**形式化**：

$$
\text{Cognition} = E_{\text{body}} \cdot E_{\text{environment}} \cdot E_{\text{action}} \cdot E_{\text{extension}}
$$

四个 E 的乘积（不是加和）才是完整的认知。

**操作形态学对应**：本书第 11 章的 H2 假设（协同演化）正是这一观点的 LLM Agent 版本。**B = {P, T, M, C} 四个组件必须协同修改才能产生最大效果**——单独修改 P 或单独修改 T 都远不如 P+T+M+C 协同修改。

### 3.6 论证 6：Enactive 与 Ecological 的激进主张

**核心论点**：enactive 与 ecological 主张"无表征认知"——认知不需要内部表征。

**证据 1（Gibson 的 affordance）**：环境直接提供行动可能性，不需要内部"翻译"。
**证据 2（Noë 的 enactive perception）**：感知不是表征的处理，而是与环境的直接耦合。
**证据 3（Chemero 的 radical embodied cognition）**：认知科学应该放弃所有表征概念。

**形式化**：

$$
\text{Cognition} \equiv \text{Coupling}(\text{Agent}, \text{Environment}), \quad \text{no representation}
$$

认知等价于 Agent 与环境的耦合，无需表征。

**操作形态学对应**：这一激进主张在 LLM Agent 时代难以完全采纳——LLM 本质上是"内部表征"（神经网络）。但本书第 8 章主张：**LLM 的"内部表征"应被视为 embodied 因素，而非孤立的大脑**——LLM 嵌入在工具、记忆、环境的耦合中。

### 3.7 论证 7：认知边界的流动性

**核心论点**：认知的边界不是固定的，而是根据任务动态变化的。

**证据 1（Otto 案例）**：Otto 在家时认知边界包含笔记本；在街上迷路时认知边界依赖路人。
**证据 2（Sutton 的"外部表征"）**：屏幕、键盘、笔等都是认知的"外部表征"。
**证据 3（Kirsh 的"智能分配"）**：认知资源在内部与外部之间动态分配。

**形式化**：

$$
\text{Cognitive Boundary}(t) = \partial(\text{Useful for current task})
$$

认知边界是"对当前任务有用的范围"——它是动态的。

**操作形态学对应**：本书第 14 章主张 **M 的边界是动态的**——在不同任务中，Agent 的 M 边界扩展或收缩。MemGPT 的 main context 在长对话中扩展、archival storage 在跨 session 时扩展、procedural memory 在新工具时扩展——这些都是 M 边界的动态调整。

## 4. 操作形态学视角

把 Oxford 4E Cognition 手册的核心论证投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到 **B 框架的哲学理论根基**。

### 4.1 四个 E 与 B = {P, T, M, C} 的精确对应

| 4E 概念 | B 组件对应 | 对应说明 |
|---|---|---|
| **Embodied (身体)** | P + C | LLM 是 Agent 的"大脑"；P 包含 embodied 因素（few-shot）；C 是 Agent 的 embodied execution |
| **Embedded (嵌入)** | M（部分） | Agent 嵌入真实环境；M 是环境耦合的载体 |
| **Enacted (行动生成)** | T + C | T 是 Agent 的"行动能力"；C 是 enacted cognition 的实现 |
| **Extended (延展)** | T + M（外存） | 工具与外部记忆是 Agent 的"延展认知" |

这一对应让 B 框架不只是软件工程的便利，而是**有哲学根基的概念系统**。

### 4.2 操作形态 B 中每个组件的 4E 视角

| B 组件 | Embodied | Embedded | Enacted | Extended |
|---|---|---|---|---|
| **P** | few-shot 是 embodied | system prompt 嵌入任务 | prompt 中的行动指令 | prompt 可以包含外部知识 |
| **T** | 工具是身体的延伸 | 工具嵌入环境 | 工具是 enacted 的载体 | 工具是认知的延展 |
| **M** | 记忆依赖 encoding | 记忆嵌入环境 | 记忆通过 recall 行动 | 记忆延展到外部存储 |
| **C** | 循环是 embodied execution | 循环嵌入环境 | 循环是 enacted cognition | 循环可以调用外部资源 |

每个 B 组件都同时具有四个 E 的某些特征——这与 4E Cognition 的"协同性"一致。

### 4.3 4E Cognition 与本书 H 假设的关系

| H 假设 | 4E Cognition 对应 |
|---|---|
| **H1 结构可塑性** | **部分支持**：认知是动态的、可塑的，但 4E 不强调"主动修改" |
| **H2 协同演化** | **强支持**：四个 E 必须协同演化——这正是 H2 的哲学根基 |
| **H3 形态适配** | **强支持**：认知根据任务调整形态——这是 4E 的核心 |
| **H4 迁移收益** | **支持**：延展认知（Otto 案例）支持跨情境迁移 |
| **H5 治理必要性** | **未涉及** |

4E Cognition 在 H2、H3、H4 上提供基础概念，但在 H1、H5 上未涉及——这些是本书的独创性贡献。

### 4.4 4E Cognition 与 L0-L5 等级的关系

按本书第 18 章：

| Agent 等级 | 4E 视角 |
|---|---|
| **L0 静态 LLM** | 纯"大脑"（embodied 但无 enacted/extended） |
| **L1 Tool-using** | 引入 enacted（工具调用） |
| **L2 ReAct Agent** | 完成 enacted（感知-行动循环） |
| **L3 Reflexion** | 引入 embedded（环境反馈） |
| **L4 Self-Modifying (P/T/M)** | 引入 extended 的动态调整 |
| **L5 Self-Evolving (C)** | 完成四个 E 的完整协同 |

**关键观察**：从 L0 到 L5 的进化路径与 4E Cognition 的演化一致——**每个 L 等级对应一个或多个 E 的引入**。

### 4.5 4E Cognition 与工具论（Tool-as-Organ）

4E Cognition 的一个重要论点是：**工具是身体的延伸（tool-as-organ）**。例如：

- 锤子不是"独立的工具"，而是手臂的延伸。
- 计算器不是"外部设备"，而是数学认知的延伸。
- Otto 的笔记本不是"外部物品"，而是记忆的延伸。

这一观点对 LLM Agent 至关重要：

```
LLM Agent 视角：
- search 工具 = Agent "探索环境" 能力的延伸（类似眼睛）
- code_exec 工具 = Agent "操作环境" 能力的延伸（类似手）
- archival storage = Agent "长期记忆" 能力的延伸（类似海马体）
- web browsing = Agent "社会认知" 能力的延伸（类似语言）
```

**工具不是外部资源，而是 Agent 认知的构成部分**。这一观点与本书第 11 章的 H1 假设一致——T 不只是工具接口，而是 Agent 形态的组成。

### 4.6 4E Cognition 与 r-paper-021（Perez）的连接

r-paper-021 揭示 prompt injection 攻击 P 组件。从 4E Cognition 视角：

- **Embodied 攻击**：通过污染 LLM 的输入（少数 token 扰动）改变 Agent 行为。
- **Embedded 攻击**：通过污染环境（外部数据）改变 Agent 行为。
- **Enacted 攻击**：通过污染工具调用（让 Agent 执行恶意操作）改变 Agent 行为。
- **Extended 攻击**：通过污染外部记忆（archival storage）改变 Agent 行为。

Perez 论文的"直接 + 间接注入"在 4E 框架下有了更系统的分类——**prompt injection 是 4E Cognition 攻击的 LLM 版本**。

### 4.7 4E Cognition 与 r-paper-022（CoALA）的连接

CoALA（r-paper-022）把 LLM Agent 形式化为决策/行动循环 + 多记忆类型。从 4E Cognition 视角：

| CoALA 组件 | 4E 对应 |
|---|---|
| Decision/Action Cycle | **Enacted**：行动生成 |
| Working Memory | **Embodied**：短时记忆 |
| Episodic Memory | **Embedded**：环境经历 |
| Semantic Memory | **Extended**：抽象知识 |
| Procedural Memory | **Enacted**：行动规则 |

CoALA 实际上是 **4E Cognition 的认知架构版本**——它把 4E 翻译为 LLM Agent 的具体实现。

## 5. 应用与影响

Oxford 4E Cognition 手册的应用与影响体现在三个层面：哲学层面、认知科学层面、AI 工程层面。本节逐层分析。

### 5.1 哲学层面的影响

4E Cognition 改变了认知哲学的范式：

- **从"内部主义"到"外部主义"**：传统认知哲学把认知视为大脑内部的过程；4E 主张认知可以延展到外部（工具、环境、其他人的头脑）。
- **从"表征主义"到"行动主义"**：传统认知哲学强调表征；4E（特别是 enactive）强调行动-感知循环。
- **从"个体主义"到"分布式"**：传统认知哲学把认知视为个体的属性；4E（Hutchins）强调认知可以分布在多个体之间。

这些哲学层面的影响**间接**作用于 LLM Agent 设计——它让 AI 研究者意识到 Agent 不是孤立的"程序"，而是嵌入环境、通过工具行动、可以延展到外部记忆的认知系统。

### 5.2 认知科学层面的影响

4E Cognition 影响了认知科学的研究方向：

- **具身认知（embodied cognition）**：研究身体如何塑造认知（语言、运动、感知）。
- **生态心理学（ecological psychology）**：研究环境如何提供 affordance（Gibson, Chemero）。
- **行动者-感知者理论（enaction）**：研究认知如何通过行动-感知循环生成（Noë, Varela）。
- **延展心智（extended mind）**：研究认知如何延展到外部工具（Clark, Sutton）。

这些研究**直接**启发了 LLM Agent 设计——Agent 的设计应该考虑身体（embodied）、嵌入（embedded）、行动（enacted）、延展（extended）四个维度。

### 5.3 AI 工程层面的影响

4E Cognition 启发了多个 AI 工程范式：

| AI 范式 | 4E 对应 | 哲学根源 |
|---|---|---|
| **具身 AI（Embodied AI）** | Embodied | 机器人学、仿真环境 |
| **情境 AI（Situated AI）** | Embedded | 生态心理学 |
| **行动生成 AI（Enactive AI）** | Enacted | enactive approach |
| **延展 AI（Extended AI）** | Extended | extended mind thesis |
| **多 Agent AI（Multi-Agent AI）** | Embedded + Extended | 分布式认知 |

LLM Agent 是这一传统下的"现代 LLM 版本"——它**整合**了四个 E：

```
LLM Agent:
- Embodied: LLM (类似大脑) + few-shot examples (类似经验)
- Embedded: 通过 M 嵌入环境 (类似情境)
- Enacted: 通过 T 与 C 行动-感知循环 (类似 sensorimotor)
- Extended: 通过 M 的外部存储 + T 的远程调用延展认知 (类似 Otto 笔记本)
```

本书用 4E Cognition 作为 LLM Agent 形态学的哲学根基——这一对应让 B 框架不只是工程设计，而是**有哲学传统支撑的概念系统**。

### 5.4 对 LLM Agent 设计的具体影响

| 4E 原则 | LLM Agent 设计指导 |
|---|---|
| **Embodied** | Agent 应有"具身经验"（如 ReAct 的 Thought 是 embodied） |
| **Embedded** | Agent 应嵌入真实环境（不是纯 LLM 对话） |
| **Enacted** | Agent 应有行动-感知循环（ReAct 是 enacted 的实现） |
| **Extended** | Agent 的认知应延展到工具与外部记忆（MemGPT 是 extended 的实现） |
| **协同性** | Agent 的四个 E 应协同演化（本书第 16 章协同自进化） |

### 5.5 对操作形态学的具体影响

| 4E 原则 | B = {P, T, M, C} 设计指导 |
|---|---|
| **Embodied** | P 应包含 embodied 因素（few-shot、运动经验模拟） |
| **Embedded** | M 应嵌入环境（外部知识库、长期记忆） |
| **Enacted** | C 应实现行动-感知循环（ReAct、Reflexion） |
| **Extended** | T 与 M 应延展认知（外部工具、外部记忆） |
| **协同性** | B 四个组件应协同修改（H2 假设） |

### 5.6 对其他相关工作的影响

4E Cognition 还影响了以下与操作形态学相关的工作：

- **r-paper-010（Varela 1991）**：The Embodied Mind——4E 的"具身"维度的源头。
- **r-paper-011（Clark 1998）**：The Extended Mind——4E 的"延展"维度的源头。
- **r-paper-012（Brooks 1991）**：Intelligence Without Representation——4E 的"行动生成"维度的源头（enactive AI）。
- **r-paper-022（CoALA）**：认知架构的 LLM 版本——4E 的认知科学基础。
- **r-paper-004（MemGPT）**：extended memory——4E 的"延展"维度的工程实现。

## 6. 局限与开放问题

Oxford 4E Cognition 手册的局限可以分为六类：**激进性的争议、缺乏计算形式化、缺乏 LLM Agent 视角、缺乏自修改视角、缺乏安全治理、缺乏实验验证**。本节是本书对 4E Cognition 的批判性分析。

### 6.1 激进性的争议

4E Cognition 中的激进主张（特别是 enactive 与 ecological）存在重大争议：

- **无表征主义**：主张认知无表征——但 LLM 本身就是大规模表征网络，这一主张难以应用到 LLM Agent。
- **激进 embodied**：主张"认知即身体"——但人类认知中确实有抽象计算（如数学、逻辑），这些不能完全还原为身体。

本书第 8 章采取**温和 4E 立场**：接受 embodied/embedded/enacted/extended 的核心主张，但保留表征与计算的合法性——这让 4E Cognition 能应用到 LLM Agent。

### 6.2 缺乏计算形式化

4E Cognition 主要以**哲学论证 + 案例分析**为主，缺乏严格的计算形式化。本书第 11 章的 B = {P, T, M, C} 是 4E Cognition 的**计算形式化**——它把四个 E 翻译为可操作的软件组件。

### 6.3 缺乏 LLM Agent 视角

4E Cognition 主要关注人类与动物认知——它对 LLM Agent 没有直接论述。本书是**4E Cognition 在 LLM Agent 时代的应用**——这是 4E 在新领域的扩展。

### 6.4 缺乏自修改视角

4E Cognition 把认知视为**动态、可塑**的，但它没有强调"Agent 主动修改自己的认知结构"。本书第 11 章的 H1 假设（结构可塑性）超出 4E 的传统——它主张 Agent 不仅能"动态调整"，还能"主动修改自己的形态"。

### 6.5 缺乏安全治理

4E Cognition 没有涉及"Agent 修改自身认知结构时的安全性"。本书第 22 章的治理框架、r-paper-021 的 prompt injection 都是 4E 传统未涉及的方向。

### 6.6 缺乏实验验证

4E Cognition 的论点多基于**哲学论证 + 行为实验**——缺乏 LLM Agent 层面的系统实验。本书第 21 章的 MorphBench 试图填补这一空白——通过实验验证 B = {P, T, M, C} 框架在 LLM Agent 上的有效性。

### 6.7 开放问题表

| 问题 | 4E 状态 | 本书视角 |
|---|---|---|
| 认知能主动修改自身吗？ | 未涉及 | 第 11 章 H1 假设 |
| 四个 E 能计算形式化吗？ | 未形式化 | 第 11 章 B 框架 |
| 4E 适用于 LLM Agent 吗？ | 未应用 | 第 7、8、11 章 |
| 4E 的安全性如何？ | 未涉及 | 第 22 章治理 |
| 4E 能被实验验证吗？ | 部分 | MorphBench 实验 |
| 4E 与表征如何调和？ | 争议 | 第 8 章温和立场 |

## 7. 对本书的贡献

Oxford 4E Cognition 手册在本书的理论体系中扮演**操作形态学的哲学理论根源**——它为 B = {P, T, M, C} 框架提供哲学根基。

### 7.1 4E Cognition 作为 B 框架的哲学根基

本书第 7、8、11 章把 B 框架建立在 4E Cognition 之上：

- **第 7 章**：介绍 4E Cognition 的核心概念，建立哲学坐标系。
- **第 8 章**：分析 4E 与 LLM Agent 的对应，提取"温和 4E 立场"。
- **第 11 章**：把 4E 形式化为 B = {P, T, M, C}，提出 H1-H5 假设。

这一三步走让 LLM Agent 的形态学不是凭空设计，而是**有哲学根基的概念系统**。

### 7.2 4E Cognition 与 r-paper-010、011、012 的关系

本书已经收录了 4E Cognition 的三个奠基性工作：

- **r-paper-010（Varela 1991, The Embodied Mind）**：4E 的 embodied 来源。
- **r-paper-011（Clark 1998, The Extended Mind）**：4E 的 extended 来源。
- **r-paper-012（Brooks 1991, Intelligence Without Representation）**：4E 的 enactive 来源。

Oxford 手册（r-paper-024）是这三个工作的**综述与整合**——它把 embodied、extended、enactive 整合为 4E Cognition 完整框架。本书用 Oxford 手册作为 4E 的"标准参考"。

### 7.3 4E Cognition 与 r-paper-022（CoALA）的关系

CoALA（r-paper-022）把 4E Cognition 翻译为 LLM Agent 的认知架构：

| 4E | CoALA 对应 |
|---|---|
| Embodied | Working Memory + Internal Actions |
| Embedded | Episodic Memory |
| Enacted | Decision/Action Cycle + External Actions |
| Extended | Semantic Memory + Procedural Memory |

CoALA 与 4E Cognition 的精确对应让 B 框架有了双重根基——**认知科学（4E） + 软件工程（B）**。

### 7.4 4E Cognition 与本书 H 假设的关系

| H 假设 | 4E 哲学根源 |
|---|---|
| **H1 结构可塑性** | 4E 中认知的可塑性（流动性边界） |
| **H2 协同演化** | 4E 的协同性原则 |
| **H3 形态适配** | 4E 的 affordance 与情境认知 |
| **H4 迁移收益** | 4E 的 extended mind（Otto 案例） |
| **H5 治理必要性** | 未涉及（本书独创） |

4E Cognition 是 H1-H4 的哲学根基，但 H5 是本书的独创性贡献。

### 7.5 4E Cognition 对 L0-L5 等级的启示

| L 等级 | 4E 维度 |
|---|---|
| **L0 静态 LLM** | 仅 Embodied（LLM 是"身体"） |
| **L1 Tool-using** | + Enacted（行动-感知） |
| **L2 ReAct** | + Enacted 完整（循环） |
| **L3 Reflexion** | + Embedded（环境反馈） |
| **L4 Self-Modifying (P/T/M)** | + Extended 动态调整 |
| **L5 Self-Evolving (C)** | 四个 E 完整协同 |

从 L0 到 L5 的进化对应 4E 的完整化——**L5 是 4E Cognition 的 LLM Agent 完整实现**。

### 7.6 4E Cognition 对 AGI 安全的启示

4E Cognition 对 AGI 安全的启示是双重的：

- **支持 LLM Agent 的延展**：Agent 的认知延展到工具与记忆是正常的（Otto 案例）——这为 MemGPT 等系统提供合法性。
- **警示失控风险**：如果 Agent 的延展失控（如核心代码被自修改、C 失去控制），后果是灾难性的——这与 SICA（r-paper-006）、Gödel Agent（r-paper-007）的安全边界一致。

第 22 章的治理框架以 4E Cognition 为哲学基础——**Agent 的延展应被治理**。

### 7.7 给读者的关键启示

1. **4E Cognition 是 B 框架的哲学根基**：B 不是凭空设计的概念，而是 4E Cognition 的工程实现。理解 4E 是理解 B 的前提。
2. **四个 E 必须协同**：Embodied、Embedded、Enacted、Extended 不是独立的，而是协同的。这一观点是 H2（协同演化）的哲学根源。
3. **认知边界是流体的**：Agent 的 B 边界应根据任务动态调整——这是 MemGPT、A-MEM 等长期记忆系统的设计哲学。
4. **工具是身体的延伸**：T 不只是工具接口，而是 Agent 形态的组成。这一观点为操作形态学的 T 设计提供哲学支持。
5. **温和 4E 立场适用于 LLM Agent**：完全采纳 enactive 与 ecological 的"无表征主义"难以应用到 LLM（LLM 本质是表征）。本书采取温和立场——接受 4E 的核心主张但保留表征的合法性。
6. **4E 与安全性有双重关系**：4E 支持 Agent 的延展（合法性），但也警示失控风险（需要治理）。本书第 22 章的治理框架以 4E 为哲学基础。

Oxford 4E Cognition 手册是操作形态学的哲学理论根源。它为 B = {P, T, M, C} 提供哲学根基，让 LLM Agent 的形态学不是软件工程的便利，而是**有哲学传统支撑的概念系统**。

理解 Oxford 4E Cognition 手册是理解操作形态学的**哲学层面**——它回答"为什么 B = {P, T, M, C} 是合理的"，而工程层面回答"如何实现 B"。两者共同构成完整的操作形态学体系。

## 参考文献

- newen2018oxford: Newen, A., De Bruin, L., & Gallagher, S. (Eds.). (2018). *The Oxford Handbook of 4E Cognition*. Oxford University Press. [$TRAE_REF](https://academic.oup.com/book/2753)
- varela1991embodied: Varela, F. J., Thompson, E., & Rosch, E. (1991). *The Embodied Mind: Cognitive Science and Human Experience*. MIT Press. 见 r-paper-010。（Embodied Mind——4E 的 embodied 来源）
- clark1998extended: Clark, A., & Chalmers, D. J. (1998). *The Extended Mind*. Analysis, 58(1), 7-19. 见 r-paper-011。（Extended Mind——4E 的 extended 来源）
- brooks1991intelligence: Brooks, R. A. (1991). *Intelligence Without Representation*. Artificial Intelligence, 47, 139-159. 见 r-paper-012。（Intelligence Without Representation——4E 的 enactive 来源）
- gibson1979ecological: Gibson, J. J. (1979). *The Ecological Approach to Visual Perception*. Houghton Mifflin.（生态心理学——4E 的 ecological 来源）
- noonë2004action: Noë, A. (2004). *Action in Perception*. MIT Press.（行动者-感知者——4E 的 enactive 来源）
- varela1996neurophenomenology: Varela, F. J. (1996). *Neurophenomenology: A Methodological Remedy for the Hard Problem*. Journal of Consciousness Studies.（神经现象学——4E 的方法论）
- rowlands2018ch1: Rowlands, M. (2018). *Chapter 1: What 4E Cognition Is (and Isn't)*. In Newen et al. (Eds.), Oxford Handbook of 4E Cognition.（4E 的标准定义来源）
- clark2008supersizing: Clark, A. (2008). *Supersizing the Mind*. Oxford University Press.（extended mind 的系统化论述）
- sutton2010ego: Sutton, J. (2010). *Exograms and Interdisciplinarity*. In Menary (Ed.), The Extended Mind.（外部表征——延展认知的进一步论述）
- kirsh2013embodied: Kirsh, D. (2013). *Embodied Cognition and the Magical Future of Interaction Design*. ACM TiiS.（智能分配——认知的动态调整）
- sumers2023coala: Sumers, T., et al. (2023). *CoALA*. arXiv:2309.02427. 见 r-paper-022。（4E Cognition 的 LLM Agent 翻译）
- yao2023react: Yao, S., et al. (2023). *ReAct*. 见 r-paper-001。（enacted cognition 的 LLM Agent 实现）
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT*. 见 r-paper-004。（extended memory——Otto 案例的 LLM Agent 版本）
- fang2025selfevolving: Fang, W., et al. (2025). *Self-Evolving Agents Survey*. 见 r-paper-009。（4E 在自修改 Agent 中的应用综述）
- perez2022promptinjection: Perez, E., et al. (2022). *Ignore Previous Prompt*. 见 r-paper-021。（4E 攻击的 LLM 版本）