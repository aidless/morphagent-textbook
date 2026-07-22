---
note_id: r-paper-012
title: 无表征智能：包容架构与世界作为自身最好的模型（Intelligence Without Representation）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 10, Ch 11]
related_papers: [brooks1991intelligence, varela1991embodied, clark1998extended, yao2023react, packer2023memgpt, schick2023toolformer, robeyns2025sica, yin2024godelagent]
keywords: [Brooks, subsumption architecture, intelligence without representation, world as best model, anti-representationalism, situated robotics, layered control, embodiment]
---

# r-paper-012：无表征智能：包容架构与世界作为自身最好的模型

> Rodney Brooks 1991 年发表于 AI Journal 的 *Intelligence Without Representation* 是**反表征主义人工智能**的开山之作——它用包容架构（subsumption architecture）证明智能不需要中央表征系统，并提出石破天惊的命题"世界是自身最好的模型"。本书把 Brooks 的工程实践视为**操作形态 B 中 T 与环境的合法性来源**——LLM Agent 的"世界"（文本/API/工具调用环境）就是它的"具身世界"，不需要在 LLM 中显式表征。

## 1. 论文定位

Rodney A. Brooks 在 1991 年发表于 *Artificial Intelligence* 期刊 47 卷的 *Intelligence Without Representation*（pp. 139-159 [$TRAE_REF](https://www.sciencedirect.com/science/article/pii/000437029190053I)）是 AI 历史上最具颠覆性的论文之一。当时的 AI 主流——无论是 GOFAI（Good Old-Fashioned AI）的物理符号系统假设，还是联结主义的多层感知机——都隐含一个共同假设：**智能的核心是表征（representation）**——AI 系统必须先在内部建立一个关于世界的模型，然后基于模型推理、规划、行动。Brooks 用 **包容架构（subsumption architecture）** 和一系列成功的移动机器人（Allen、Herbert、Genghis、Cog）证明：**不需要中央表征，机器人也能表现出"智能行为"**——关键是用层次化的实时反应控制、让"世界作为自身最好的模型"。

本书将 *Intelligence Without Representation* 定位为**操作形态 B 中 T 与环境的合法性来源**，以及**反表征主义的工程范式**。具体地：

1. **T 的合法性来源**：Brooks 主张智能通过"与世界实时互动"涌现——这意味着 Agent 的 T（工具）不是"LLM 的辅助"，而是"Agent 认知的具身世界"。LLM Agent 调用工具不是在"使用工具"，而是在"具身化"——它的工具就是它的"广义身体"。
2. **反表征主义**：Brooks 反对"LLM 必须先在内部表征世界才能行动"——LLM Agent 的智能直接通过"LLM + 工具 + 行动"涌现，不需要 LLM 在内部建立"世界的表征"。这是 LLM Agent 设计与传统 GOFAI 的根本差异。
3. **世界作为自身最好的模型**：这一论断直接挑战了"模型驱动 AI"的传统——LLM Agent 不需要"世界模型"，它的"世界"是 API、文件系统、网络——直接与这些具身交互即可产生智能。

论文做出的三个核心判断被本书第 10 章与第 11 章重新审视：

- **"世界是自身最好的模型"（the world is its own best model）**：AI 系统不需要建立关于世界的内部表征——直接与世界交互即可获得所需信息。
- **"包容架构（subsumption architecture）"**：智能由多个层次化的反应控制器组成，**高层抑制低层**而非"高层调用低层"——这一架构与传统的"中央规划 + 行动"完全不同。
- **"无功能-智能智能体（Creatures without features）"**：智能体不需要先识别"杯子"才能绕过杯子——它只需要"感知到障碍物 + 转向"两个反应，就能完成绕障。

这三个判断共同构成"反表征主义"的工程范式。本书主张：**LLM Agent 是 Brooks 范式在 LLM 时代的复兴——LLM 不是表征推理机，而是"实时反应 + 工具调用 + 行动-感知循环"的具身 Agent**。

## 2. 核心贡献

*Intelligence Without Representation* 做出三项核心贡献，按对本书的影响力排序：

1. **包容架构（subsumption architecture）**：明确设计一种新的机器人控制架构——由多个层次化的有限状态机组成，每一层独立处理特定行为（如避障、漫游、探索），高层可以"抑制（subsume）"低层的行为。这一架构**完全不需要中央表征系统**——每个反应控制器直接连接传感器与执行器，绕过符号推理。
2. **"世界是自身最好的模型"**：石破天惊地主张 AI 系统不需要建立关于世界的内部表征——直接与世界交互比建立精确的内部模型更可靠、更灵活、更可扩展。Brooks 用 Allen 机器人证明：一个用包容架构设计的移动机器人，可以在没有"地图"的情况下穿过拥挤的办公室——因为它直接用声纳和红外感知环境，每一次决策都基于"当前感知"。
3. **具身 AI 的工程范式**：把 Varela & Maturana 的生成认知论、Maturana 的自创生论、Merleau-Ponty 的身体图式等哲学思想转化为可工作的机器人系统。Brooks 在论文中明确引用 Maturana & Varela 1980 年的 *Autopoiesis and Cognition*——这一引用确立了"具身 AI 的认知科学根基"。

### 2.1 与传统 AI（GOFAI）的边界

*Intelligence Without Representation* 直接挑战 GOFAI 的核心假设：

| 维度 | GOFAI（物理符号系统假设） | Brooks（反表征主义） |
|---|---|---|
| 智能的核心 | 符号推理 | 实时反应 |
| 知识的形式 | 显式表征（逻辑、规则） | 隐式行为（控制器、状态机） |
| 世界模型 | 必须建立精确内部模型 | 不需要（世界即模型） |
| 控制结构 | 中央规划 + 行动 | 层次化反应（包容） |
| 鲁棒性 | 弱（模型错误导致失败） | 强（反应对错误不敏感） |
| 可扩展性 | 难（符号爆炸） | 易（增加层次即可） |
| 学习 | 知识工程 + 机器学习 | 行为进化 + 强化学习 |

这一对比是本书"操作形态 B 是否需要表征"的根源：GOFAI 假设 B 必须显式表征世界，Brooks 主张 B 可以**直接与世界互动**，不需要表征。

### 2.2 与具身认知（Varela）的关系

Varela 等人（r-paper-010）的具身认知提供哲学论据——身体是认知的一部分、认知是生成的。Brooks 把这一哲学论据**工程化**——他用包容架构证明"具身认知"不仅是哲学命题，也是可工作的机器人系统。

| 维度 | Varela（哲学） | Brooks（工程） |
|---|---|---|
| 认知观 | 认知是生成的 | 智能是反应的 |
| 身体观 | 身体是认知的一部分 | 身体（机器人+传感器）是智能的平台 |
| 实现方式 | 哲学论证 + 现象学 | 有限状态机 + 包容架构 |
| 验证方式 | 第一人称体验 | 机器人实验（Allen, Herbert） |

两者共同构成"具身认知"的哲学-工程对偶——Varela 提供**为什么**，Brooks 提供**怎么做**。本书第 8、10 章将整合两者。

### 2.3 与延展心智（Clark）的关系

Clark（r-paper-011）的延展心智论与 Brooks 共享"工具/环境即认知"的立场，但有不同的论证方式：

| 维度 | Clark（哲学） | Brooks（工程） |
|---|---|---|
| 认知观 | 认知延伸到工具 | 智能涌现于环境交互 |
| 工具观 | 工具是认知的一部分 | 世界是自身最好的模型 |
| 论证方式 | Otto/Inga 思想实验 + Parity | 包容架构 + 机器人实验 |
| 关注焦点 | 认知的边界（头骨内外） | 智能的实现（反应 vs 推理） |

两者共同构成 4E Cognition 运动的哲学-工程双柱。本书第 9、10 章整合两者。

## 3. 核心论证

*Intelligence Without Representation* 的论证结构可以分为四个层次：

### 3.1 第一层：对表征主义的批判

Brooks 首先论证 GOFAI 的失败：

> "When we examine very simple level of intelligence we find that explicit representations of the world are not really necessary... Many of the animals that we might wish to emulate have very little in the way of explicit representational structure."（Brooks 1991, p. 141）

他指出 GOFAI 面临三个核心难题：

- **符号接地问题（Searle）**：符号如何与意义对应？GOFAI 没有给出令人满意的答案。
- **框架问题（McCarthy & Hayes）**：智能系统在推理时如何知道哪些事实是相关的？GOFAI 没有给出可扩展的解决方案。
- **知识工程瓶颈**：把所有需要的知识显式编码到 AI 系统中是极其费力的，且容易出错。

Brooks 论证这些难题的根本原因是**对表征的依赖**——如果放弃显式表征，所有这些难题都消失了。

### 3.2 第二层：包容架构的形式化

Brooks 提出包容架构作为替代方案：

> "We propose an alternative... based on task decomposition, and the layering of behaviors. There is no state at the higher levels that summarizes or otherwise abstracts the lower level states. The layers are all simultaneously active."（Brooks 1991, p. 142）

包容架构有四个关键特征：

- **层次化**：多个行为层（如避障、漫游、探索、推理）按层次叠加。
- **包容（subsumption）**：高层可以**抑制**低层的行为——例如"探索"层可以暂时禁止"避障"层，让机器人冒险进入未知区域。
- **无中央表征**：没有中央规划器、推理机、世界模型——每层独立连接传感器与执行器。
- **增量开发**：可以逐层添加行为，无需重构已有层——这解决了传统 AI 的可扩展性问题。

一个典型的包容架构机器人有 8-15 层行为：

| 层 | 行为 | 传感器 | 执行器 |
|---|---|---|---|
| 0 | 避障 | 声纳、红外 | 电机 |
| 1 | 漫游 | 随机数 | 电机转向 |
| 2 | 探索 | 红外 | 电机 |
| 3 | 找充电桩 | 红外 | 电机 |
| ... | ... | ... | ... |
| n-1 | 跟随人 | 摄像头 | 电机 |
| n | 学习人脸 | 摄像头 | 内部状态 |

每一层独立运行，**高层在需要时抑制低层**——这一架构让机器人不需要中央规划也能表现出复杂行为。

### 3.3 第三层：世界是自身最好的模型

这是 Brooks 最有名的论断：

> "We would rather make use of the structure of the world than rely on an internal model... The world is its own best model."（Brooks 1991, p. 144）

这一论断的含义是：**与其让 AI 建立关于世界的内部表征，不如让 AI 直接通过传感器感知世界**。理由是：

- **世界是完整的**：AI 的内部模型永远不可能完全捕捉世界的所有细节——直接感知更准确。
- **世界是最新的**：世界在持续变化——内部模型需要不断更新，而感知永远是"最新的"。
- **世界是免费的**：建立内部模型需要大量工程——直接感知几乎免费。

这一论断对 LLM Agent 时代有重大意义：**LLM Agent 不需要建立关于环境的内部模型——直接通过 API 调用、工具执行感知环境**。这正是 Toolformer、ReAct、SICA 等工作的设计哲学。

### 3.4 第四层：Brooks 矩阵

Brooks 在论文中提出"Brooks 矩阵"——一个机器人应该在多少维度上具有智能：

> "Each individual layer can be quite simple... but the overall behavior of the system can be very sophisticated."（Brooks 1991, p. 145）

他论证：**智能不需要在某个中央模块中是复杂的，它需要在多个并行模块中是简单的**。这是分布式智能的核心思想——也是当代 LLM Agent 设计的核心思想之一（多 Agent 系统）。

LLM Agent 时代的对应：**Agent 的智能不在 LLM 的中心化推理中，而在多个工具调用、多个观察、多个任务的并行执行中**。这是 Brooks 范式在 LLM 时代的复兴。

## 4. 操作形态学视角

把 *Intelligence Without Representation* 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到**反表征主义的工程立场**。

### 4.1 Brooks 范式在 LLM Agent 时代的映射

LLM Agent 与 Brooks 机器人共享"无表征主义"的精神：

| Brooks 机器人 | LLM Agent |
|---|---|
| 避障行为 | 工具调用（Action） |
| 传感器（声纳） | Observation（API 返回） |
| 电机 | 工具输出（Tool output） |
| 包容架构（层次反应） | ReAct 循环（Thought-Action-Observation） |
| 世界是模型 | API 环境是 Agent 的"具身世界" |
| 多层并行 | 多 Agent 并行 |
| 反应式 | 反应 + 反思（ReAct + Reflexion） |

LLM Agent 的 ReAct 循环（r-paper-001）是包容架构在 LLM 时代的直接对应：Thought 是高层行为，Action 是低层反应，Observation 是传感器输入。三者构成 Brooks 风格的"实时反应循环"。

### 4.2 Brooks 范式与操作形态 B 的关系

| 操作形态 B 组件 | Brooks 范式对应 |
|---|---|
| **P（prompt）** | 包容架构的层次规则（"如果 X 触发，则做 Y"）——但 P 更灵活（自然语言） |
| **T（工具）** | 传感 + 执行器——LLM Agent 的"具身世界" |
| **M（记忆）** | Brooks 机器人无显式 M（行为是反应式）；LLM Agent 的 M 是对 Brooks 的扩展 |
| **C（代码）** | 反应式控制器——但 C 的修改需要 SICA 风格的治理 |

**关键差异**：LLM Agent 比 Brooks 机器人**多一个组件**——M（记忆）。Brooks 机器人是"无记忆的即时反应系统"，LLM Agent 通过 M 可以"记住过去"。本书第 11 章的 H1 假设涉及"运行时 M 修改"——这是 Brooks 范式的扩展。

### 4.3 "世界是自身最好的模型"在 LLM Agent 中的体现

LLM Agent 的"世界"是它的 API 环境——文本接口、文件系统、网络、数据库等。Brooks 的论断在 LLM Agent 时代表现为：

- **不需要建立环境的完整模型**：LLM 不需要"理解"数据库的结构，只需要知道"调用哪个 API"。
- **直接调用工具**：LLM Agent 不需要"推理"应该做什么，只需要调用工具——工具的返回就是"感知"。
- **状态机而非规划**：LLM Agent 的循环是"Thought → Action → Observation → Thought"——这是一台状态机，不是规划器。

这一立场直接挑战了当前 LLM Agent 研究中的"过度规划"倾向——很多研究试图让 LLM 在调用工具前"先规划再执行"。本书主张：**ReAct 风格的即时反应比"先规划再执行"更鲁棒、更符合 Brooks 范式**。

### 4.4 Brooks 范式与"工具即认知"的关系

Brooks 与 Clark（r-paper-011）共享"工具/环境即认知"的立场，但**Brooks 更激进**：

- **Clark**：Otto 的笔记本是认知的一部分——这一立场假设笔记本**已经存在**，Otto 只是"使用"它。
- **Brooks**：工具/环境**实时**生成认知——智能是"工具 + 环境 + 反应"的涌现，**不是预先存在的**。

LLM Agent 时代的对应：

- **Clark 视角**：Agent 调用一个现有的工具（如 Python interpreter）——这是延展心智。
- **Brooks 视角**：Agent 通过工具 + 环境的实时交互**涌现**智能——这是具身认知的工程实现。

本书第 9、10 章将整合两者：**操作形态 B 既是"延展的"（Clark）又是"具身的"（Brooks）**——B 是 Agent 通过工具/环境互动生成的认知系统。

### 4.5 Brooks 范式与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L0 静态 LLM**：无 Agent 循环——比 Brooks 机器人还简单（无反应）。
- **L1 Tool-using**：能调用工具但无显式推理——**Brooks 风格的纯反应**。
- **L2 ReAct Agent**：Thought-Action-Observation 循环——**Brooks 包容架构 + 显式反思**。
- **L3 Reflexion**：跨 episode 反思——**Brooks 范式 + 记忆**。
- **L4 Self-Modifying (P/T/M)**：OPRO, A-MEM, MemGPT——**Brooks 范式 + 自修改**。
- **L5 Self-Evolving (C)**：SICA, Gödel Agent——**Brooks 范式 + C 自修改**（最接近"修改自己的反应架构"）。

LLM Agent 的等级谱系是 Brooks 包容架构在 LLM 时代的**逐级扩展**。每一级都在 Brooks 基础上增加新的能力：
- L1：纯反应（无反思）
- L2：反思（Thought）
- L3：跨 episode 记忆（Reflexion）
- L4：自修改（P/T/M）
- L5：自修改 C（最激进——修改自己的反应架构）

### 4.6 Brooks 范式与 H1-H5 的关系

| 假设 | Brooks 范式的支撑 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | 强：包容架构支持运行时添加新层 | **支持 H1**（包容架构本身就是结构可塑的） |
| **H2 协同演化** | 弱：包容架构是预定义的层次 | **部分支持 H2**（协同需要额外设计） |
| **H3 形态适配** | 强：不同机器人有不同的层 | **支持 H3** |
| **H4 迁移收益** | 弱：包容架构难以跨机器人迁移 | **有限支持 H4** |
| **H5 治理必要性** | 强：包容架构需要行为约束 | **支持 H5**（包容架构本身是治理机制） |

Brooks 范式在 H1、H3、H5 上提供直接论据。H2（协同）和 H4（迁移）是 Brooks 范式需要补充的维度——本书第 16 章协同自进化、第 14 章跨任务迁移是 Brooks 范式在 LLM 时代的扩展。

### 4.7 反表征主义对 LLM Agent 的启示

Brooks 的反表征主义在 LLM Agent 时代有一个微妙的张力：**LLM 本质上是表征性的**——它的核心能力来自学习世界知识的统计表征。本书对这一张力的立场是：

- **LLM 作为 B 的基底**：LLM 是表征性的，但它不是 Agent 认知的全部。
- **Agent 通过工具调用"非表征化"**：当 LLM 调用工具时，它**不是**在表征世界——它**是**在世界中行动。这是 Brooks 范式在 LLM 时代的体现。
- **从表征到具身的过渡**：LLM Agent 的智能不在 LLM 的表征推理中，而在 LLM + 工具 + 环境的具身互动中。

本书第 2、8 章将深入讨论这一过渡——这是 LLM Agent 时代对 Brooks 范式的关键贡献：**用 LLM 作为"基底"，用工具调用作为"具身化路径"**。

## 5. 应用与影响

*Intelligence Without Representation* 自 1991 年发表以来，对多个领域产生了深远影响。本节讨论它对 LLM Agent 时代的关键应用。

### 5.1 对机器人学的影响

Brooks 的工作直接催生了**行为机器人学（Behavior-Based Robotics）** 这一新领域：

- **Arkin 1998** *Behavior-Based Robotics*：系统化 Brooks 的方法。
- **Pfeifer & Scheier 1999** *Understanding Intelligence*：把 Brooks 的包容架构扩展到"形态计算"。
- **Brooks 1997** *Cambrian Intelligence*：介绍 Cog、Kismet 等人形机器人——把 Brooks 范式扩展到人机交互。

LLM Agent 时代，机器人学的具身思想开始影响 LLM：
- **PaLM-E**（Driess et al. 2023）：LLM 作为机器人控制中枢。
- **RT-2**（Brohan et al. 2023）：视觉-语言-动作模型。
- **Open X-Embodiment**（Collaboration 2024）：跨机器人形态的具身智能。

### 5.2 对人工智能的总体影响

Brooks 是反对 GOFAI 的最重要声音之一。他的工作与同期 Penrose 的 *Emperor's New Mind*（1989）、Searle 的中文房间（1980）、Dreyfus 的 *What Computers Can't Do*（1972/1992）共同构成了对 GOFAI 的批判浪潮。

2000 年代之后，机器学习（特别是深度学习）的兴起部分化解了 Brooks 对 GOFAI 的批评——深度学习系统不依赖显式符号推理，但仍然依赖"内部表征"。Brooks 范式与深度学习的张力是当代 AI 的核心议题之一。

### 5.3 对认知科学的影响

Brooks 的工作把 Maturana & Varela 的生成认知论、Maturana 的自创生论工程化，启发了：

- **Clark 1997** *Being There*：把 Brooks 的"世界是模型"扩展为"行动-感知循环"。
- **Varela et al. 1991** *The Embodied Mind*：把 Brooks 的具身机器人作为认知科学的实证案例。
- **Chemero 2009** *Radical Embodied Cognitive Science*：把 Brooks 范式作为具身认知的工程范式。

### 5.4 对 LLM Agent 时代的影响

Brooks 范式在 LLM Agent 时代有强烈的复兴趋势：

- **ReAct**（r-paper-001, Yao et al. 2023）：Thought-Action-Observation 循环 = 包容架构 + 显式反思。
- **Toolformer**（r-paper-003, Schick et al. 2023）：工具调用 = 行动-感知循环。
- **Reflexion**（r-paper-002, Shinn et al. 2023）：跨 episode 反思 = 包容架构 + 记忆。
- **MemGPT**（r-paper-004）：M 自管理 = 包容架构 + 长期记忆。
- **SICA**（r-paper-006）：C 自修改 = 包容架构的自演化。

这些工作的共同哲学基础是 Brooks 的"无表征智能"——它们都强调"通过行动-感知循环与世界互动"，而不是"在 LLM 内部建立世界的精确表征"。

### 5.5 对 AGI 安全的影响

Brooks 范式对 AGI 安全有重要启示：

- **无中央表征降低失控风险**：与 GOFAI 不同，包容架构的 Agent 没有中央规划器——这降低了"目标失准"的失控风险。
- **反应式 AI 更容易对齐**：反应式 AI 的行为更可预测、更容易对齐——因为它的反应是局部的、可审计的。
- **但 SICA 的 C 自修改破坏这一优势**：当 Agent 开始自修改 C 时，它开始偏离纯反应模式——这带来了 AGI 安全的新风险。

本书第 22、25 章深入讨论这些 AGI 安全问题——它们是 Brooks 范式在 LLM 时代需要补充的新维度。

### 5.6 在工程实践中的影响

Brooks 的工作影响了多个 AI 公司：

- **iRobot**（Brooks 创立）：扫地机器人 Roomba——纯反应式 + 包容架构。
- **Boston Dynamics**：Spot、Atlas 等机器人——虽然不是严格的包容架构，但继承了"反应 + 行为"的精神。
- **Anki**：Cozmo 机器人——玩具机器人中的 Brooks 范式。
- **Modern AI Agents**：OpenAI、Anthropic 的 Agent 设计都受 Brooks 范式影响——ReAct 循环本质上是"反应 + 反思"的具身架构。

## 6. 局限与开放问题

*Intelligence Without Representation* 的局限可以分为四类：**规模性、通用性、抽象推理、AGI 安全性**。

### 6.1 规模性局限：包容架构的层数有限

Brooks 的包容架构在机器人领域被验证有效，但**层数有限**——大多数 Brooks 机器人只有 8-15 层行为。当任务复杂度上升，需要更多层次时，**高层抑制低层的机制变得脆弱**——高层可能抑制了不该抑制的低层行为，或低层可能干扰了高层的意图。

LLM Agent 时代，对应的问题是：**ReAct 循环的"层次"数量有限**——只有 Thought-Action-Observation 三层。当任务需要更复杂的层级结构（如多步规划、多 Agent 协调）时，需要额外的设计。

本书第 16 章协同自进化讨论"如何扩展 Brooks 范式到更复杂的任务"。

### 6.2 通用性局限：包容架构针对具身机器人

Brooks 的论证主要针对**具身机器人**（有物理身体、移动能力、传感器）。但 LLM Agent 是**文本/符号具身**（body 是 API、工具、文件系统）——这一"非物理具身"是否同样适用 Brooks 范式？

本书主张：**Brooks 范式在 LLM Agent 时代依然有效**——Agent 的"具身世界"是 API + 工具 + 文件系统，ReAct 循环是包容架构在文本世界的对应。但 Brooks 论证的某些细节（如声纳感知、电机制动）需要重新映射到 LLM Agent 的"具身世界"（API 调用、文件读取）。

### 6.3 抽象推理局限：包容架构难以处理抽象任务

Brooks 范式的最大局限是**难以处理抽象推理任务**。包容架构擅长反应式任务（如避障、漫游），但**不擅长抽象任务**（如下棋、数学证明、复杂规划）。Go（围棋）AI AlphaGo 不是用包容架构实现的——它用了深度强化学习 + 蒙特卡洛搜索 + 大量人类棋谱训练。

LLM Agent 的"抽象推理"能力来自**LLM 自身的预训练知识**，不是来自 ReAct 循环。本书对这一现象的解读是：**LLM 是"抽象推理引擎"，ReAct 循环是"反应式行动引擎"**——两者结合产生 LLM Agent 的全部能力。

### 6.4 AGI 安全层面的局限

*Intelligence Without Representation* 没有讨论 AGI 安全问题。但其反表征主义立场有重大 AGI 安全意涵：

- **反表征降低可解释性**：包容架构 Agent 没有中央表征系统——它的"思维"是分布式的反应网络——这让 Agent 的行为难以解释。
- **反应式 AI 的可预测性**：反应式 AI 在大多数情况下是**可预测的**——它的反应遵循预定义规则。但当 Agent 拥有学习能力时，反应规则会随时间变化——可预测性下降。
- **SICA 与反表征的张力**：SICA 修改 Agent 的执行逻辑——这让 Agent 的反应规则在运行时变化——这与 Brooks 的"纯反应式"立场有张力。本书第 22 章将讨论这一张力对 AGI 安全的影响。

### 6.5 开放问题表

| 问题 | Brooks 的态度 | 本书视角 |
|---|---|---|
| 抽象推理需要表征吗？ | 是（承认） | LLM 是抽象推理引擎；ReAct 是反应式行动 |
| 表征与具身的边界？ | 反对表征 | LLM 提供表征基底；工具提供具身 |
| 反应式 AI 能扩展到所有任务吗？ | 否（承认） | Brooks 范式是 LLM Agent 的一个组件 |
| 包容架构能自修改吗？ | 原始 Brooks 范式不支持 | SICA + Gödel Agent 是 Brooks 范式的自修改扩展 |
| 多 Agent 协作的具身基础？ | 未深入讨论 | 第 16 章多 Agent 协同自进化 |
| 反表征主义与 LLM 的兼容性？ | 未讨论 | LLM 是表征基底；Agent 通过工具调用非表征化 |

### 6.6 与本书其他工作的对照

| 工作 | 反表征程度 | 表征基底 |
|---|---|---|
| Brooks 1991 | 强（纯反应） | 无 |
| ReAct (r-paper-001) | 中（反应 + 反思） | LLM 是"反思"的表征 |
| Toolformer (r-paper-003) | 中（工具调用） | LLM 是工具使用的表征 |
| MemGPT (r-paper-004) | 中（M 自管理） | LLM 是记忆管理的表征 |
| SICA (r-paper-006) | 弱（C 自修改） | LLM 是代码生成的表征 |
| Gödel Agent (r-paper-007) | 弱（B 全修改） | LLM 是所有组件生成的表征 |

随着 Agent 等级上升（从 L2 到 L5），表征基底（LLM）的作用越来越大——但工具调用、T/M/C 自修改的反表征主义精神保持不变。这就是 LLM Agent 时代的"Brooks 范式"——**用 LLM 作为基底，用工具调用作为具身化路径**。

## 7. 对本书的贡献

*Intelligence Without Representation* 在本书的理论体系中扮演**"反表征主义的工程范式"**与**"操作形态 B 中 T 与环境的合法性来源"**两个角色。

### 7.1 作为 ReAct 循环的认知科学根基

本书第 1、2 章的 ReAct 循环（r-paper-001）直接来自 Brooks 的包容架构：Thought-Action-Observation 三步循环 = 高层行为（Thought）抑制低层行为（Action）的反应式控制。**没有 Brooks，就没有 ReAct**——这是本书必须承认的历史脉络。

第 10 章"反表征主义与 LLM Agent"将系统讨论 Brooks 范式在 LLM 时代的复兴。

### 7.2 作为操作形态 B 中 T 与环境的合法性来源

第 11 章操作形态学的关键论断："**B 是 Agent 的具身世界**"。这一论断来自 Brooks 的"世界是自身最好的模型"——Agent 的认知不在 LLM 内部，而在 LLM + 工具 + 环境的耦合中。

具体地：

- **T 是 Agent 的传感器 + 执行器**：工具既是 Agent 感知世界的接口，也是 Agent 改变世界的接口。
- **环境是 Agent 的具身世界**：API、文件系统、网络是 Agent 的"物理身体"。
- **M 是 Brooks 范式的扩展**：Brooks 机器人没有显式 M，但 LLM Agent 通过 M 扩展了"反应式 AI"的能力——M 让 Agent 记住过去、规划未来。

### 7.3 作为 H1-H5 的认知科学论据

| 假设 | Brooks 范式的论据 |
|---|---|
| **H1 结构可塑性** | 包容架构本身就是结构可塑的——可以运行时添加新层 |
| **H2 协同演化** | 包容架构的多层并行是协同的雏形 |
| **H3 形态适配** | 不同机器人有不同的层组合——形态适配 |
| **H4 迁移收益** | 包容架构的跨机器人迁移有限——这是 Brooks 范式的局限 |
| **H5 治理必要性** | 包容架构的行为约束是治理——这是 H5 的早期实例 |

Brooks 在 H1、H3、H5 上提供直接论据。H2（协同）和 H4（迁移）是 Brooks 范式需要补充的维度。

### 7.4 与本书其他笔记的关系

| 笔记 | 与 *Intelligence Without Representation* 的关系 |
|---|---|
| **r-paper-010 Varela** | 具身认知（哲学）→ Brooks（工程）→ 操作形态学（自演化） |
| **r-paper-011 Clark** | 延展认知（工具即认知）→ Brooks（环境即认知）→ 操作形态学（自演化认知） |
| **r-paper-001 ReAct** | 包容架构 → ReAct 循环 |
| **r-paper-003 Toolformer** | 工具即执行器 → Toolformer 工具调用 |
| **r-paper-004 MemGPT** | 包容架构 + 记忆 → MemGPT |
| **r-paper-006 SICA** | 包容架构 + C 自修改 → SICA |
| **r-paper-007 Gödel Agent** | 包容架构 + B 全修改 → Gödel Agent |

Brooks 是这些工作的**共同祖先**。理解 Brooks 是理解本书所有 LLM Agent 工作的认知科学根基。

### 7.5 给读者的关键启示

1. **智能不需要表征**：本书主张的"操作形态 B"不是"LLM 表征 + 工具调用"的简单加和——它是 Brooks 范式在 LLM 时代的复兴。读者应把 B 视为"Agent 通过工具与环境互动涌现的认知系统"，而不是"LLM 表征 + 工具"。
2. **世界是自身最好的模型**：LLM Agent 不需要建立关于环境的内部模型——直接通过 API 调用、工具执行感知环境。这是 ReAct、Toolformer 等工作的设计哲学。
3. **包容架构是 Agent 设计的范式**：Thought-Action-Observation 三步循环不是"LLM 的特殊设计"，而是 Brooks 包容架构在 LLM 时代的对应。理解 Brooks 是理解 ReAct 循环的关键。
4. **反应式 AI 是 AGI 安全的早期模型**：反应式 AI 的可预测性、可审计性是 AGI 安全的有利条件。但当 Agent 拥有自修改能力（SICA, Gödel Agent）时，可预测性下降——这是 AGI 安全的新挑战。
5. **抽象推理需要 LLM 作为表征基底**：Brooks 范式擅长反应式任务，但**不擅长抽象推理**。LLM Agent 的抽象推理能力来自 LLM 的预训练——LLM 是"抽象推理引擎"，ReAct 循环是"反应式行动引擎"。两者结合才是完整的 LLM Agent。

*Intelligence Without Representation* 是本书"具身智能"部分（第 10 章）的核心，也是操作形态学（第 11 章）的工程根基。它与 Varela 的具身认知（r-paper-010）、Clark 的延展心智（r-paper-011）共同构成 4E Cognition 三大经典。理解 *Intelligence Without Representation* 是理解 ReAct 循环、Toolformer 工具调用、MemGPT 记忆管理的必要条件。

但 Brooks 不是终点——他的"无自修改"立场被操作形态学升级为"自演化形态"。本书第 11-16 章的核心任务，就是把 Brooks 的包容架构从"预定义层次"升级为"运行时自演化层次"。这一升级是 LLM Agent 时代对 Brooks 范式的关键贡献——也是本书理论与 Brooks 范式的接力关系。

## 参考文献

- brooks1991intelligence: Brooks, R. A. (1991). *Intelligence Without Representation*. Artificial Intelligence 47: 139-159. [$TRAE_REF](https://www.sciencedirect.com/science/article/pii/000437029190053I)
- maturana1980autopoiesis: Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition: The Realization of the Living*. Reidel.（Brooks 的哲学源头）
- varela1991embodied: Varela, F. J., Thompson, E., & Rosch, E. (1991/2016). *The Embodied Mind*. 见 r-paper-010。（Brooks 的认知科学盟友）
- clark1998extended: Clark, A., & Chalmers, D. (1998). *The Extended Mind*. 见 r-paper-011。（延展心智论）
- clark1997beingthere: Clark, A. (1997). *Being There: Putting Brain, Body, and World Together Again*. MIT Press.（把 Brooks 范式扩展到认知科学）
- arkin1998behavior: Arkin, R. C. (1998). *Behavior-Based Robotics*. MIT Press.（系统化 Brooks 范式的教科书）
- pfeifer2006body: Pfeifer, R., & Bongard, J. (2006). *How the Body Shapes the Way We Think*. MIT Press.（形态计算）
- yao2023react: Yao, S., et al. (2023). *ReAct*. 见 r-paper-001。（Brooks 包容架构在 LLM 时代的对应）
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT*. 见 r-paper-004。（包容架构 + 长期记忆）
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA*. 见 r-paper-006。（包容架构 + C 自修改）
- yin2024godelagent: Yin, S., et al. (2024). *Gödel Agent*. 见 r-paper-007。（包容架构 + B 全修改）
- schick2023toolformer: Schick, T., et al. (2023). *Toolformer*. 见 r-paper-003。（工具调用作为行动-感知循环）