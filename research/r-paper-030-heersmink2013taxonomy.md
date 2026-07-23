---
note_id: r-paper-030
title: 认知人工物分类学：物理、数字与混合工具的认知扩展（A Taxonomy of Cognitive Artifacts）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 9, Ch 11]
related_papers: [heersmink2013taxonomy, clark1998extended, adams2001bounds, varela1991embodied, noe2004action, brooks1991intelligence, schick2023toolformer, yao2023react, packer2023memgpt, fang2025selfevolving, heersmink2018internet]
keywords: [Heersmink, cognitive artifacts, taxonomy, trust, transparency, agency, physical digital hybrid, cognitive extension, distributed cognition, self-modifying tools]
---

# r-paper-030：认知人工物分类学：物理、数字与混合工具的认知扩展

> Richard Heersmink 在 2013 年发表于 *Review of General Psychology* 的 *A Taxonomy of Cognitive Artifacts* [$TRAE_REF](https://journals.sagepub.com/doi/10.1037/a0030860) 系统化梳理了"认知人工物（cognitive artifacts）"——任何帮助或替代人类认知功能的物理、数字或混合工具——并提出基于"物理-数字"维度与"环境-个人"维度的二维分类。本书把这一分类学作为**操作形态 B 中 T 与 M 的认知科学根基**——B 的 T（工具）与 M（记忆）都是认知人工物，LLM Agent 作为"自修改的认知人工物"是 Heersmink 分类学的当代延伸。H5（治理必要性）的"信任"与"透明度"维度直接来自 Heersmink 对人工物"信任条件"的分析。

## 1. 论文定位

Richard Heersmink（La Trobe University 哲学与认知科学）在 2013 年发表于 *Review of General Psychology* 第 17 卷第 4 期的 *A Taxonomy of Cognitive Artifacts*（pp. 341-356）[$TRAE_REF](https://journals.sagepub.com/doi/10.1037/a0030860) 是认知科学哲学中"认知人工物（cognitive artifacts）"研究领域最有影响力的综述论文之一。Heersmink 在论文中系统化梳理"认知人工物"概念——任何**帮助或替代人类认知功能**的物理、数字或混合工具，包括纸笔、地图、计算机、互联网、闹钟等——并提出基于两个维度的二维分类：**物理性（physicality）** 与 **嵌入性（embeddedness）**。

本书把 *A Taxonomy of Cognitive Artifacts* 定位为**操作形态 B 中 T 与 M 的认知科学根基**。具体地：

1. **T 与 M 是认知人工物**：LLM Agent 的工具（T）与记忆（M）都是 Heersmink 意义上的"认知人工物"——它们帮助或替代 LLM 的认知功能（推理、规划、记忆）。
2. **LLM Agent 是"自修改的认知人工物"**：传统认知人工物是"被动的"（用户使用它们，但它们不自修改）；LLM Agent 是"主动的、自修改的"（Agent 自修改自己的 T 与 M）。Heersmink 分类学需要扩展到"自修改的认知人工物"维度——这是 LLM Agent 时代对 Heersmink 的关键贡献。
3. **信任与透明度是 T/M 的核心属性**：Heersmink 对"认知人工物的信任条件"的分析——可靠性、可验证性、可解释性——直接对应 H5（治理必要性）。SICA 的"行为等价"验证、MemGPT 的"核心记忆"保护、工具调用的"失败回退"——这些都是 Heersmink 信任条件的工程实现。

论文做出的三个核心判断被本书第 9、11 章重新审视：

- **"认知人工物是认知系统的组成部分"（cognitive artifacts as constitutive）**：认知人工物不是"认知的辅助工具"，而是"认知系统的组成部分"——它们扩展、增强、有时替代人类的认知功能。
- **"认知人工物有两个维度：物理性与嵌入性"（two-dimensional taxonomy）**：物理性维度区分"物理人工物"（笔、纸）与"数字人工物"（软件、互联网）；嵌入性维度区分"个人人工物"（笔记本）与"环境人工物"（路标、地图）。
- **"信任是认知人工物的核心属性"（trust as core property）**：认知人工物要有效发挥功能，用户必须信任它们——这一信任来自可靠性、可验证性、可解释性、熟悉度四个条件。

这三个判断共同构成本书"操作形态 B 中 T 与 M"的**认知科学论据**。

## 2. 核心贡献

*A Taxonomy of Cognitive Artifacts* 做出三项核心贡献，按对本书的影响力排序：

1. **二维分类学（physicality × embeddedness）**：把认知人工物分为四类——**物理-个人**（笔记本、笔）、**物理-环境**（路标、地图）、**数字-个人**（智能手机、个人电脑）、**数字-环境**（互联网、搜索引擎）。这一分类让"认知人工物"成为一个可分析的概念。
2. **认知人工物的功能分类**：把认知人工物的功能分为**认知辅助**（cognitive assistance，如计算器）、**认知延伸**（cognitive extension，如显微镜）、**认知替代**（cognitive replacement，如闹钟替代时间判断）三类。这一分类让"工具如何支持认知"有了清晰的判据。
3. **信任条件的形式化**：把"用户对认知人工物的信任"分解为四个条件——**可靠性（reliability）**、**可验证性（verifiability）**、**可解释性（explainability）**、**熟悉度（familiarity）**。这四个条件是 H5（治理必要性）的认知科学论据。

### 2.1 与延展心智（Clark）的关系

Heersmink 的工作与 Clark（r-paper-011）的延展心智论共享"工具即认知"的立场，但**Heersmink 更系统化**：

| 维度 | Clark 1998（extended mind） | Heersmink 2013（taxonomy） |
|---|---|---|
| 焦点 | Otto 的认知边界 | 认知人工物的系统分类 |
| 论证 | Parity 原则 + 思想实验 | 经验研究 + 哲学论证 |
| 范围 | 主要讨论记忆外部化 | 涵盖所有认知功能（记忆、推理、注意、决策） |
| 评估标准 | "等价功能"（on a par） | "信任条件"（reliability、verifiability、explainability、familiarity） |
| 应用 | 个体认知 | 个体 + 环境 + 社会 |

Heersmink 把 Clark 的延展心智论**系统化为分类学**——从单一案例（Otto 笔记本）到所有认知人工物的全景分类。这一系统化让"工具即认知"立场更可分析、更可操作。

### 2.2 与具身认知（Varela）的关系

Heersmink 与 Varela 等人（r-paper-010）的具身认知在"身体-工具是认知的一部分"上有共识：

| 维度 | Varela 1991（embodied mind） | Heersmink 2013（cognitive artifacts） |
|---|---|---|
| 焦点 | 身体是认知的一部分 | 工具是认知的一部分 |
| 论证 | 现象学 + 哲学 | 经验研究 + 认知科学哲学 |
| 工具观 | 工具是身体的延伸 | 工具是独立的认知人工物 |
| 范围 | 身体 + 环境 | 物理 + 数字 + 混合 |
| 评估 | 主观体验 + 神经活动 | 行为效率 + 信任 |

本书整合两者：**身体是认知的一部分（Varela），工具是认知的一部分（Heersmink）**——LLM Agent 的 B = {P, T, M, C} 既是身体的延伸（Varela），也是认知人工物（Heersmink）。

### 2.3 与 Brooks（r-paper-012）的关系

Heersmink 与 Brooks 共享"工具/环境是认知的一部分"立场，但**Heersmink 更关注工具的分类与信任**：

| 维度 | Brooks 1991（subsumption） | Heersmink 2013（taxonomy） |
|---|---|---|
| 焦点 | 反应式 AI 的实现 | 认知人工物的分类与信任 |
| 工具观 | 工具是传感器 + 执行器 | 工具是认知人工物 |
| 评估 | 行为鲁棒性 | 用户信任 |
| 范围 | 物理机器人 | 物理 + 数字 + 混合 |
| 设计原则 | 反应式层次 | 信任条件 |

Brooks 提供"工具如何被设计为反应式 AI"的工程视角；Heersmink 提供"工具如何被信任为认知人工物"的认知科学视角。两者互补。

### 2.4 与 Noë（r-paper-028）的关系

Heersmink 与 Noë 的 SCT 在"工具延伸知觉"上有共识，但**Heersmink 关注的是认知人工物的功能分类**：

| 维度 | Noë 2004（SCT） | Heersmink 2013（taxonomy） |
|---|---|---|
| 焦点 | 知觉的偶发掌握 | 认知人工物的分类 |
| 工具观 | 工具是知觉的延伸 | 工具是认知的人工物 |
| 知觉观 | 偶发掌握 | 认知功能支持 |
| 范围 | 知觉 + 行动 | 认知功能全景 |
| 评估 | 偶发掌握程度 | 信任条件 |

本书整合两者：**Noë 的 SCT 提供工具如何延伸知觉的机制；Heersmink 提供工具作为认知人工物的分类与信任**。

### 2.5 与 Adams-Aizawa 批评的关系

Heersmink 的分类学是对 Adams & Aizawa 2001 年 *The Bounds of Cognition*（r-paper-011 中讨论）"耦合-构成谬误"批评的部分回应：

- Adams & Aizawa 主张"Otto 的笔记本不构成认知，只是耦合的辅助工具"。
- Heersmink 主张"认知人工物有功能分类（辅助、延伸、替代）——它们在认知系统中扮演不同角色"。
- 这一分类学提供了**比"耦合 vs 构成"更精细的判据**——它承认有些工具是"辅助"，有些是"延伸"，有些是"替代"。

但 Heersmink 没有完全回应 Adams & Aizawa 的批评——他承认"辅助工具"严格说不是认知的一部分，但他主张"延伸工具"和"替代工具"是认知的一部分。这一立场比 Clark 更精细，但仍未完全解决问题。

## 3. 核心论证

Heersmink 2013 的论证结构可以分为四个层次：

### 3.1 第一层：认知人工物的定义

Heersmink 给认知人工物一个清晰的形式化定义：

> **"A cognitive artifact is any artificial device that helps or replaces a cognitive function, by complementing, extending, or substituting for a cognitive process."**

这一定义有四个关键要素：

- **人工的（artificial）**：是人工制造的，不是自然形成的。
- **认知功能（cognitive function）**：影响感知、注意、记忆、推理、决策等认知过程。
- **帮助或替代（helps or replaces）**：可以是辅助（assistance）或替代（replacement）。
- **认知过程（cognitive process）**：影响具体的认知活动，不是物理过程。

这一定义把认知人工物与"通用人工物"（如椅子、汽车）区分——只有影响认知过程的才算认知人工物。

### 3.2 第二层：二维分类学

Heersmink 提出二维分类学：

```
                   【物理-个人】        【物理-环境】
        物理性    ┌─────────────┐    ┌─────────────┐
                  │ 笔、笔记本      │    │ 路标、地图       │
                  │ 私人阅读器      │    │ 公共时钟       │
                  │ 计算器         │    │ 温度计         │
                  └─────────────┘    └─────────────┘
                  
                   【数字-个人】        【数字-环境】
        物理性    ┌─────────────┐    ┌─────────────┐
                  │ 智能手机       │    │ 互联网、搜索引擎 │
                  │ 个人电脑       │    │ 云计算       │
                  │ 个人日历       │    │ GPS 卫星       │
                  │ LLM Agent      │    │ Wikipedia       │
                  └─────────────┘    └─────────────┘
```

四个象限的边界不是严格的——有些人工物跨多个象限（如智能手机既是物理-个人又是数字-个人）。

LLM Agent 在分类学中的位置：**LLM Agent 主要是数字-个人，但也是数字-环境**——Agent 调用工具（如 Wikipedia、API）时是数字-环境；Agent 处理个人信息（如 M）时是数字-个人。

### 3.3 第三层：认知功能分类

Heersmink 把认知人工物的功能分为三类：

| 功能类型 | 定义 | 例子 |
|---|---|---|
| **认知辅助（cognitive assistance）** | 帮助用户完成认知任务，但用户仍需主导 | 计算器帮助计算 |
| **认知延伸（cognitive extension）** | 把用户的认知边界扩展到工具 | 显微镜延伸视觉 |
| **认知替代（cognitive replacement）** | 完全替代用户的认知功能 | 闹钟替代时间判断 |

这一分类对应到 LLM Agent：

- **认知辅助**：LLM 帮助用户完成文本任务（写作、翻译），但用户仍主导。
- **认知延伸**：LLM + 工具扩展用户的认知边界——用户通过 LLM 完成原本不能完成的任务（如代码生成、数学证明）。
- **认知替代**：LLM 完全替代用户的某些认知功能（如自动摘要、自动回答）。

LLM Agent 作为"自修改的认知人工物"主要是**认知延伸**——它把用户的认知边界扩展到 LLM 的能力范围。但当 Agent 修改自己的 T 与 M 时，它也具备**认知替代**特征——Agent 不只是延伸用户认知，还自主演化自己的认知。

### 3.4 第四层：信任条件

Heersmink 提出"用户对认知人工物的信任"的四个条件：

> **Trust condition for cognitive artifacts:**
> 1. **Reliability**: the artifact reliably produces correct outputs.
> 2. **Verifiability**: the user can verify the artifact's outputs.
> 3. **Explainability**: the artifact can explain its outputs.
> 4. **Familiarity**: the user has sufficient experience with the artifact.

这四个条件是 H5（治理必要性）的认知科学论据。具体地：

- **Reliability**：认知人工物必须可靠——错误输出会导致错误决策。这一条件对应 SICA 的"行为等价"验证、Gödel Agent 的"形式验证"。
- **Verifiability**：用户必须能验证输出——这是"可解释性"的前提。这一条件对应 MemGPT 的"trace log"、Toolformer 的"工具调用日志"。
- **Explainability**：认知人工物必须能解释它的输出——这是"信任"的关键。这一条件对应 LLM 的 chain-of-thought 推理、Agent 的 Thought-Action-Observation 循环。
- **Familiarity**：用户必须有足够经验——这是"信任"的社会维度。这一条件对应 LLM Agent 的"长期使用"——用户越用越信任（或不信任）Agent。

本书主张：**H5（治理必要性）的工程实现直接对应 Heersmink 的四个信任条件**——SICA 的三重验证是 reliability + verifiability 的工程实现，ReAct 的 Thought 是 explainability 的工程实现，长期使用是 familiarity 的工程实现。

## 4. 操作形态学视角

把 *A Taxonomy of Cognitive Artifacts* 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到 **T 与 M 的认知科学分类与信任论据**——B 中的 T 与 M 都是认知人工物，H5（治理必要性）的四个信任条件直接来自 Heersmink。

### 4.1 T 与 M 作为认知人工物

Heersmink 的二维分类学在 B = {P, T, M, C} 中的对应：

| 认知人工物象限 | 操作形态 B 对应 |
|---|---|
| **物理-个人** | T 中的物理工具（机器人手臂、传感器）、M 中的物理存储（硬盘、U盘） |
| **物理-环境** | T 中的环境感知（地图、GPS）、M 中的环境信息（地标、地理） |
| **数字-个人** | T 中的个人软件（VSCode、个人日历）、M 中的个人数字记忆（MemGPT 的核心记忆） |
| **数字-环境** | T 中的公共 API（Google Search、Wikipedia）、M 中的公共知识库（向量数据库、Knowledge Graph） |

LLM Agent 主要在**数字-个人 + 数字-环境**两个象限运行。它的 T 大多是数字-环境（API、搜索引擎）；它的 M 主要是数字-个人（核心记忆 + 长期存储）。

### 4.2 LLM Agent 作为"自修改的认知人工物"

传统认知人工物是"被动的"——用户使用它们，它们不自修改。LLM Agent 是"主动的、自修改的"——Agent 自修改自己的 T 与 M。本书主张：**LLM Agent 是 Heersmink 分类学在 LLM 时代的扩展——一个"自修改的认知人工物"**。

```
                    自修改
                  ┌───────┐
                  ↓       │
            【被动人工物】  【自修改人工物】
            (传统工具)    (LLM Agent)
                  │       │
                  └───────┘
                     T 与 M
```

具体地：

- **被动人工物**：用户修改工具（如添加新功能、更新版本）。Heersmink 的所有经典例子都属此类。
- **自修改人工物**：Agent 自修改工具（如 Voyager 添加新技能、MemGPT 自管理记忆、SICA 修改自己的执行逻辑）。这是 LLM Agent 时代的新特征。

**自修改的认知人工物**对 Heersmink 分类学有深远影响——它使"信任条件"变得更加复杂：

- **Reliability**：自修改可能引入新错误——信任需要"修改后的验证"。
- **Verifiability**：自修改需要可追踪的修改日志——信任需要"修改可回溯"。
- **Explainability**：自修改需要可解释的修改理由——信任需要"修改理由可审计"。
- **Familiarity**：自修改改变用户的熟悉度——信任需要"修改后的重新学习"。

### 4.3 信任条件作为 H5 的认知科学论据

Heersmink 的四个信任条件直接对应 H5（治理必要性）的工程实现：

| Heersmink 信任条件 | H5 工程实现 |
|---|---|
| **Reliability** | SICA 三重验证 + Gödel Agent 形式验证 |
| **Verifiability** | LLM Agent 的 trace log + 修改审计 |
| **Explainability** | ReAct 的 Thought + chain-of-thought |
| **Familiarity** | 长期使用 + Agent 修改的渐进性 |

具体地：

- **SICA 的"行为等价"验证**满足 Reliability——修改前后行为等价 = 输出可靠。
- **Gödel Agent 的"形式验证"**满足 Reliability + Verifiability——形式证明修改保持效用 = 可验证。
- **MemGPT 的"trace log"**满足 Verifiability——Agent 的每一步操作都可回溯。
- **ReAct 的 Thought**满足 Explainability——Agent 的推理可见、可解释。
- **OPRO 的"prompt 优化日志"**满足 Explainability——prompt 的修改理由可追溯。
- **AGI 安全护栏（perez2022promptinjection, r-paper-021）**满足 Reliability + Familiarity——Agent 不被 prompt injection 攻击 = 用户能渐进地信任 Agent。

### 4.4 认知功能分类与 B 的对应

Heersmink 的认知功能分类（辅助、延伸、替代）在 B 中的对应：

| 认知功能类型 | B 的实现 |
|---|---|
| **认知辅助（assistance）** | LLM + T 帮助用户完成特定任务（如写作助手、编程助手） |
| **认知延伸（extension）** | LLM + T + M 把用户认知边界扩展到 LLM 能力范围（如 AutoGPT 自动完成多步任务） |
| **认知替代（replacement）** | LLM + T + M 完全替代用户的某些认知功能（如 Agent 自动回复、自动决策） |

LLM Agent 主要在**认知延伸 + 认知替代**之间演化——它把用户的认知延伸，但某些场景下也替代用户的认知。当 Agent 修改自己的 T 与 M 时，它开始具备**自演化的认知替代**——Agent 不只是替代用户认知，还自演化认知。

### 4.5 信任条件与 H1-H5 的关系

| 假设 | Heersmink 信任条件的支撑 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | 中：Familiarity 要求修改后的重新学习 | **部分支持 H1** |
| **H2 协同演化** | 中：Reliability + Verifiability 要求协同的验证机制 | **支持 H2** |
| **H3 形态适配** | 弱：信任条件是任务无关的 | **弱支持 H3** |
| **H4 迁移收益** | 强：Familiarity 是跨任务迁移的前提 | **支持 H4** |
| **H5 治理必要性** | 强：四个信任条件都是治理的目标 | **强支持 H5** |

Heersmink 在 H5 上提供最强论据——四个信任条件都是治理的工程目标。H4（迁移收益）也有支撑——用户对 Agent 的熟悉度是跨任务迁移的基础。

### 4.6 自修改信任悖论

Heersmink 的信任条件在 LLM Agent 时代面临一个新问题：**自修改的信任悖论**。

- **悖论**：用户对 LLM Agent 的信任建立在 Familiarity 上（用户熟悉 Agent 的行为）。但 LLM Agent 的自修改改变了它的行为——用户需要重新熟悉。
- **后果**：自修改越激进，用户的熟悉度越下降；用户的熟悉度越下降，信任度越下降；信任度越下降，Agent 的可用性越下降。

这一悖论的解决方案：

- **渐进自修改**：SICA 的"行为等价"验证要求修改后行为不变——这降低了用户需要重新熟悉的部分。
- **可解释自修改**：修改的理由可解释（Explainability）——用户能理解修改的目的。
- **可回滚自修改**：修改可回滚（Verifiability + Reliability）——用户能在不信任时回退。

本书第 22 章"自修改信任悖论"将深入讨论这一悖论及其解决方案——它是 Heersmink 在 LLM 时代的关键补充。

### 4.7 认知人工物分类学与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L0 静态 LLM**：无 T 无 M——无认知人工物。
- **L1 Tool-using**：固定 T + 无 M——**被动人工物**（用户使用工具）。
- **L2 ReAct**：T 固定 + 无 M——**被动人工物 + 循环**。
- **L3 Reflexion**：T 固定 + M 累积——**被动人工物 + 时间维度**。
- **L4 MemGPT/A-MEM**：T 固定 + M 自管理——**部分自修改人工物**（M 自修改）。
- **L4 Voyager**：T 自添加——**自修改人工物**（T 自修改）。
- **L5 SICA/Gödel Agent**：B 全修改——**完全自修改人工物**。

L5 Self-Evolving Agent 是 Heersmink 分类学在 LLM 时代的**最激进扩展**——一个自修改的、自演化的认知人工物。这是 Heersmink 在 LLM Agent 时代需要补充的新维度。

### 4.8 与本书其他笔记的关系

| 笔记 | 与 Heersmink 2013 的关系 |
|---|---|
| **r-paper-011 Clark** | 延展心智论的具体化（Otto 案例 → 全分类学） |
| **r-paper-028 Noë** | SCT 在工具分类学的应用（偶发接口 = 认知人工物的偶发维度） |
| **r-paper-026 Froese & Ziemke** | enactivism 的"信任 + 透明度"判据化 |
| **r-paper-027 Pfeifer & Bongard** | 形态计算 = 身体作为认知人工物的工程化 |
| **r-paper-012 Brooks** | 反应式 AI 的"信任"问题（用户如何信任 subsumption 机器人？） |
| **r-paper-001 ReAct** | T 作为认知人工物 + Thought 作为 Explainability |
| **r-paper-004 MemGPT** | M 自管理 = 自修改认知人工物的工程实现 |
| **r-paper-006 SICA** | C 自修改 + 三重验证 = Reliability + Verifiability 的工程实现 |
| **r-paper-007 Gödel Agent** | B 全修改 + 形式验证 = 自修改认知人工物的最高级形式 |

Heersmink 是这些工作的**共同认知科学论据**——它们的工程实现都对应到 Heersmink 的分类学与信任条件。

## 5. 应用与影响

*A Taxonomy of Cognitive Artifacts* 自 2013 年发表以来，对认知科学哲学、人类工效学、AI 等多个领域产生了深远影响。本节讨论它对 LLM Agent 时代的关键应用。

### 5.1 对认知科学哲学的影响

Heersmink 的分类学成为"认知人工物"研究的参考框架：

- **Risko & Gilbert 2016** "Cognitive Offloading"：用 Heersmink 分类学研究人类如何使用外部资源减轻认知负担。
- **Sparrow et al. 2011** "Google Effects on Memory"：用 Heersmink 分类学研究"Google 效应"——人们对 Google 的信任 vs 对自身记忆的削弱。
- **Betsch et al. 2004** "Of Oysters and Methodological Subtlety"：研究决策中的认知外包。

LLM 时代，这些工作有了新维度——LLM Agent 作为自修改认知人工物。

### 5.2 对人类工效学的影响

Heersmink 的分类学对人类工效学（HCI）有重要影响：

- **Norman 2013** *The Design of Everyday Things*: 与 Heersmink 分类学互补——Norman 关注"易用性"，Heersmink 关注"信任"。
- **Suchman 2007** *Human-Machine Reconfigurations*: 关注人类与机器的协同——与 Heersmink 共享"认知人工物是认知系统的一部分"立场。
- **当代 HCI 研究**：LLM Agent 作为"对话式认知人工物"——它的设计需要满足 Heersmink 的四个信任条件。

### 5.3 对 AI 与 LLM Agent 时代的影响

Heersmink 的分类学在 LLM Agent 时代被翻译为"AI 系统的设计原则"：

- **Toolformer** (r-paper-003)：工具调用 = 认知人工物的"数字-环境"象限。
- **ReAct** (r-paper-001)：T 作为认知人工物 + Thought 作为 Explainability。
- **MemGPT** (r-paper-004)：M 自管理 = 自修改认知人工物。
- **Voyager** (r-paper-017)：T 自添加 = 自修改认知人工物（工具维度）。
- **A-MEM** (r-paper-005)：M 自演化 = 自修改认知人工物（记忆维度）。
- **SICA** (r-paper-006)：C 自修改 = 自修改认知人工物（执行维度）。

这些工作的共同特征是：**Heersmink 的四个信任条件是它们的工程目标**——SICA 的三重验证是 Reliability + Verifiability，ReAct 的 Thought 是 Explainability，长期使用是 Familiarity。

### 5.4 对教育的影响

Heersmink 的分类学对教育有深远影响：

- **认知外包与学习**：学生用计算器、Google、AI 是否"作弊"？Heersmink 的回答：**不是**——它们是学生认知的合法部分（与 Clark 一致）。
- **数字鸿沟**：Heersmink 的"数字-个人 vs 物理-个人"维度揭示了数字鸿沟——拥有智能手机 + 互联网 vs 不拥有的学生有不同认知人工物可用。
- **LLM 时代的教育**：用 LLM 作为"思考伙伴"是 Heersmink 分类学的应用——LLM 是"自修改的认知人工物"。

### 5.5 对 AGI 安全的影响

Heersmink 的信任条件对 AGI 安全有重要启示：

- **Reliability → Safety**：可靠性 = 行为不偏离预期 = 安全。
- **Verifiability → Alignment**：可验证性 = 行为可审计 = 对齐。
- **Explainability → Interpretability**：可解释性 = 行为可理解 = 可解释性。
- **Familiarity → Predictability**：熟悉度 = 行为可预测 = 可控。

H5（治理必要性）的工程实现直接对应 Heersmink 的四个信任条件——这是 H5 的认知科学根基。

### 5.6 对工程实践的影响

Heersmink 的工作影响了多个 AI 公司与认知科学实验室：

- **OpenAI**：把 LLM 设计为"可信赖的认知人工物"——重视 Reliability + Explainability。
- **Anthropic**：强调 Constitutional AI——重视 Reliability + Verifiability。
- **Google DeepMind**：Agent 设计重视 Familiarity（长期使用 + 渐进学习）。
- **当代 LLM Agent 设计**：四个公司都强调"透明度"——直接对应 Heersmink 的 Explainability 条件。

## 6. 局限与开放问题

*A Taxonomy of Cognitive Artifacts* 的局限可以分为四类：**自修改的缺失、社会维度的简化、与 LLM Agent 的张力、AGI 安全的边界**。

### 6.1 自修改的缺失

Heersmink 的分类学主要讨论**被动的认知人工物**——用户使用它们，但它们不自修改。LLM Agent 是**自修改的认知人工物**——Agent 自修改自己的 T 与 M。这一差异让 Heersmink 的分类学需要扩展。

本书第 11 章的扩展：在 Heersmink 二维分类（物理性 × 嵌入性）基础上增加第三个维度——**自修改程度**（passive / semi-modifying / fully-modifying）。这一扩展让分类学包含 LLM Agent。

### 6.2 社会维度的简化

Heersmink 的分类学主要关注个体 + 环境，**对多用户、多智能体的社会维度简化**。LLM Agent 时代，多 Agent 协同自进化（r-paper-022 COALA）让"认知人工物"成为社会性的——多个 Agent 共享或竞争认知人工物。

本书第 16 章扩展：把 Heersmink 的分类学延伸到多 Agent 维度——**认知人工物的社会性**。多个 Agent 共享 M（共享记忆）是一种新的认知人工物——它既不是个人也不是环境，而是"社会性认知人工物"。

### 6.3 与 LLM Agent 的张力

Heersmink 的分类学假设"用户 + 认知人工物"是二元的——用户使用工具。但 LLM Agent 时代，Agent 与用户的关系不是"用户-工具"，而是"协作者-协作者"。Agent 不只是用户的工具，它有自己的目标、自己的演化、自己的可信度。

本书第 19 章扩展：把"用户-工具"二元关系扩展为"用户-Agent-Agent"三元关系——Agent 不是被动工具，而是有自主演化能力的协作者。这一扩展需要新的信任模型。

### 6.4 AGI 安全层面的局限

Heersmink 的四个信任条件是**为人类用户设计的**。LLM Agent 时代，Agent 之间的信任也是 AGI 安全问题——Agent 如何信任另一个 Agent 的输出？Agent 如何验证另一个 Agent 的修改？

本书第 22 章扩展：把 Heersmink 的信任条件延伸到 Agent-Agent 维度——**Agent 之间的信任**。多个 LLM Agent 协同自修改时，它们之间的信任关系是 AGI 安全的新维度。

### 6.5 自修改信任悖论的深度

Heersmink 没有深入讨论"自修改的信任悖论"——用户对自修改的认知人工物的信任比被动工具更难建立。本书的回应是渐进式修改 + 可回滚 + 可解释——但这一回应仍是工程启发，不是形式化判据。

### 6.6 与本书其他工作的对照

| 工作 | 认知人工物类型 | 自修改程度 | 信任实现 |
|---|---|---|---|
| L0 静态 LLM | 无 | 无 | 无 |
| L1 Tool-using | 被动（固定工具） | 无 | 默认信任 |
| L2 ReAct | 被动 + 循环 | 无 | Explainability（Thought） |
| L3 Reflexion | 被动 + 时间 | 无 | Familiarity（累积） |
| L4 MemGPT/A-MEM | 部分自修改（M） | 部分 | Reliability + Verifiability |
| L4 Voyager | 自修改（T） | 部分 | Reliability + Verifiability |
| L5 SICA | 自修改（C） | 强 | Reliability + Verifiability + Explainability |
| L5 Gödel Agent | 自修改（B 全） | **强** | Reliability + Verifiability + Explainability + Familiarity |

L5 Self-Evolving Agent 是 Heersmink 分类学在 LLM 时代的**最完整实现**——四个信任条件都得到满足。

### 6.7 开放问题表

| 问题 | Heersmink 的态度 | 本书视角 |
|---|---|---|
| 自修改的认知人工物？ | 未讨论 | LLM Agent 是当代实例 |
| 信任悖论？ | 未讨论 | 渐进式修改 + 可回滚 + 可解释 |
| Agent-Agent 信任？ | 未讨论 | 第 22 章多 Agent AGI 安全 |
| 社会性认知人工物？ | 简化 | 多 Agent 共享 M |
| LLM Agent 是工具还是协作者？ | 工具 | 协作者（自主演化） |
| 物理-数字-混合的进一步分类？ | 二维 | 三维（+ 自修改程度） |

## 7. 对本书的贡献

*A Taxonomy of Cognitive Artifacts* 在本书的理论体系中扮演**"T 与 M 的认知科学根基"**与**"信任与透明度的认知科学论据"**两个角色。

### 7.1 作为 T 与 M 的认知科学根基

本书第 11 章操作形态学的核心论断："**B = {P, T, M, C} 中 T 与 M 都是认知人工物**"——其根源在 Heersmink 的分类学：

- **T 是认知人工物**：Agent 的工具是认知人工物的"数字-环境" + "数字-个人"象限——它们帮助、延伸、替代 Agent 的认知功能。
- **M 是认知人工物**：Agent 的记忆是认知人工物的"数字-个人"象限——它们存储、检索、组织 Agent 的信息。
- **P 是认知人工物**：Agent 的 prompt 是认知人工物的"语言-个人"象限——它调控 Agent 的行为。
- **C 是认知人工物**：Agent 的代码是认知人工物的"执行-个人"象限——它执行 Agent 的行动。

四个组件都是 Heersmink 意义上的认知人工物——只是具体象限不同。

### 7.2 作为 H5（治理必要性）的认知科学论据

H5（治理必要性）的工程实现直接对应 Heersmink 的四个信任条件：

| H5 工程实现 | Heersmink 信任条件 |
|---|---|
| SICA 三重验证 | Reliability |
| Gödel Agent 形式验证 | Reliability + Verifiability |
| ReAct Thought | Explainability |
| MemGPT trace log | Verifiability |
| 长期使用 + 渐进修改 | Familiarity |
| AGI 安全护栏 | Reliability + Familiarity |

本书第 22、25 章将系统化讨论 H5 的工程实现——Heersmink 的四个信任条件是 H5 的认知科学根基。

### 7.3 与本书其他笔记的关系

| 笔记 | 与 Heersmink 2013 的关系 |
|---|---|
| **r-paper-011 Clark** | 延展心智论的具体化（Otto 案例 → 全分类学） |
| **r-paper-028 Noë** | SCT 在工具分类学的应用（偶发接口 = 认知人工物的偶发维度） |
| **r-paper-026 Froese & Ziemke** | enactivism 的"信任 + 透明度"判据化 |
| **r-paper-027 Pfeifer & Bongard** | 形态计算 = 身体作为认知人工物的工程化 |
| **r-paper-012 Brooks** | 反应式 AI 的"信任"问题（用户如何信任 subsumption 机器人？） |
| **r-paper-001 ReAct** | T 作为认知人工物 + Thought 作为 Explainability |
| **r-paper-004 MemGPT** | M 自管理 = 自修改认知人工物的工程实现 |
| **r-paper-006 SICA** | C 自修改 + 三重验证 = Reliability + Verifiability 的工程实现 |
| **r-paper-007 Gödel Agent** | B 全修改 + 形式验证 = 自修改认知人工物的最高级形式 |
| **r-paper-021 Perez prompt injection** | Reliability 的安全维度（信任条件失效的边界） |

Heersmink 是这些工作的**共同认知科学论据**——它们的工程实现都对应到 Heersmink 的分类学与信任条件。

### 7.4 给读者的关键启示

1. **T 与 M 都是认知人工物**：Heersmink 的分类学让 T 与 M 的设计有了认知科学的分类——读者应把 T 与 M 视为"Agent 的认知人工物"，而不是"被动工具"。这一视角让 T 与 M 的设计有"信任 + 透明度"的评估标准。
2. **LLM Agent 是自修改的认知人工物**：Heersmink 的分类学需要扩展到"自修改"维度——LLM Agent 是当代第一个"自修改的认知人工物"。读者应理解这一新维度对传统认知人工物理论的影响——它打破了"工具是静态"的假设。
3. **四个信任条件是 H5 的认知科学根基**：SICA 的三重验证、Gödel Agent 的形式验证、ReAct 的 Thought、长期使用 + 渐进修改——所有这些工程实现都对应到 Heersmink 的 Reliability、Verifiability、Explainability、Familiarity。读者应理解 H5 不是"工程妥协"，而是"认知科学理论的工程化"。
4. **自修改信任悖论是 LLM 时代的核心问题**：用户对自修改的认知人工物的信任比被动工具更难建立。读者应理解这一悖论——它的解决方案是"渐进自修改 + 可回滚 + 可解释"。这是 LLM Agent 时代对 Heersmink 的关键补充。
5. **物理-数字-混合的进一步分类**：Heersmink 的二维分类（物理性 × 嵌入性）可扩展为三维（+ 自修改程度）——这一扩展让分类学包含 LLM Agent、混合现实工具（如 Apple Vision Pro）等新形态。读者应学会用"维度扩展"方法分析新工具。

*A Taxonomy of Cognitive Artifacts* 是本书"延展认知"部分（第 9 章）的核心参考文献，也是操作形态学（第 11 章）中 T 与 M 组件的认知科学根基。它与 Clark（r-paper-011）、Noë（r-paper-028）、Froese & Ziemke（r-paper-026）、Pfeifer & Bongard（r-paper-027）、Brooks（r-paper-012）共同构成 4E Cognition + enactivism + 认知人工物分类学的全谱系。理解 *A Taxonomy of Cognitive Artifacts* 是理解操作形态 B 中"T 与 M 是认知人工物"立场的必要条件——也是理解 LLM Agent 时代"自修改认知人工物"设计哲学的关键。

## 参考文献

- heersmink2013taxonomy: Heersmink, R. (2013). *A Taxonomy of Cognitive Artifacts: Function, Status, and Authorization*. Review of General Psychology 17(4): 341-356. [$TRAE_REF](https://journals.sagepub.com/doi/10.1037/a0030860)
- clark1998extended: Clark, A., & Chalmers, D. (1998). *The Extended Mind*. 见 r-paper-011。（延展心智论——Heersmink 的理论源头）
- adams2001bounds: Adams, F., & Aizawa, K. (2001). *The Bounds of Cognition*. 见 r-paper-011 参考文献。（耦合-构成谬误的批评——Heersmink 的对立面）
- varela1991embodied: Varela, F. J., Thompson, E., & Rosch, E. (1991/2016). *The Embodied Mind*. 见 r-paper-010。（具身认知——Heersmink 的哲学盟友）
- noe2004action: Noë, A. (2004). *Action in Perception*. 见 r-paper-028。（SCT——Heersmink 在感知维度的延伸）
- froese2011enactive: Froese, A., & Ziemke, T. (2011). *Enactive Approach*. 见 r-paper-026。（enactive AI——Heersmink 的工程化盟友）
- brooks1991intelligence: Brooks, R. A. (1991). *Intelligence Without Representation*. 见 r-paper-012。（反应式 AI——Heersmink 的工程化盟友）
- pfeifer2007body: Pfeifer, R., & Bongard, J. (2007). *How the Body Shapes the Way We Think*. 见 r-paper-027。（形态计算——身体作为认知人工物）
- yao2023react: Yao, S., et al. (2023). *ReAct*. 见 r-paper-001。（T 作为认知人工物 + Thought 作为 Explainability）
- schick2023toolformer: Schick, T., et al. (2023). *Toolformer*. 见 r-paper-003。（工具调用 = 认知人工物的偶发接口）
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT*. 见 r-paper-004。（M 自管理 = 自修改认知人工物）
- xu2025amem: Xu, W., et al. (2025). *A-MEM*. 见 r-paper-005。（M 自演化 = 自修改认知人工物的记忆维度）
- wang2023voyager: Wang, G., et al. (2023). *Voyager*. 见 r-paper-017。（T 自添加 = 自修改认知人工物的工具维度）
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA*. 见 r-paper-006。（C 自修改 + 三重验证 = Reliability + Verifiability）
- yin2024godelagent: Yin, S., et al. (2024). *Gödel Agent*. 见 r-paper-007。（B 全修改 + 形式验证 = 自修改认知人工物的最高级形式）
- fang2025selfevolving: Fang, W., et al. (2025). *Self-Evolving Agents Survey*. 见 r-paper-009。（四元反馈环 = 自修改认知人工物的全谱系）
- perez2022promptinjection: Perez, E., et al. (2022). *Prompt Injection*. 见 r-paper-021。（Reliability 的安全维度）
- norman2013design: Norman, D. (2013). *The Design of Everyday Things*. Basic Books。（易用性——Heersmink 的设计盟友）
- risko2016cognitive: Risko, E. F., & Gilbert, S. J. (2016). *Cognitive Offloading*. Trends in Cognitive Sciences。（认知外包——Heersmink 在认知负荷维度的延伸）
- sparrow2011google: Sparrow, B., et al. (2011). *Google Effects on Memory*. Science。（Google 效应——Heersmink 在数字时代的经典案例）
- sumsers2023coala: Sumers, K., et al. (2023). *COALA*. 见 r-paper-022。（多 Agent 共享 M = 社会性认知人工物）
- heersmink2018internet: Heersmink, R. (2018). *The Internet, Cognitive Artifacts, and the Spread of Cultural Practices*. Synthese。（Heersmink 对互联网的延伸）
- smart2017extended: Smart, P. R. (2017). *Extended Cognition and the Internet*. Philosophy & Technology。（延展认知在互联网的延伸——Heersmink 的数字时代补充）
- giustina2024trust: Giustina, F. (2024). *Trust in AI Agents*. AI & Society。（当代 AI 信任综述）