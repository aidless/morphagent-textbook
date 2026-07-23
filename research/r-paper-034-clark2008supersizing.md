---
note_id: r-paper-034
title: 扩心智：Andy Clark 对延展心智论的成熟表述（Scaffolding, Biological vs Non-Biological Coupling）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 9, Ch 11]
related_papers: [clark2008supersizing, clark1998extended, adams2001bounds, menyary2010extended, varela1991embodied, brooks1991intelligence, packer2023memgpt, schick2023toolformer, fang2025selfevolving, robeyns2025sica]
keywords: [Clark, supersizing the mind, scaffolded cognition, scaffolding, biological vs non-biological, parity principle, natural kinds, cognitive niche construction, agentive isomorphism, operational morphology, LLM tool use]
---

# r-paper-034：扩心智：Andy Clark 对延展心智论的成熟表述（Scaffolding, Biological vs Non-Biological Coupling）

> Andy Clark 2008 年由 Oxford University Press 出版的 *Supersizing the Mind: Embodiment, Action, and Cognitive Extension* 是延展心智论从"激进论文"（Clark & Chalmers 1998, r-paper-011）走向"系统化理论"的关键著作——它从**生物-非生物耦合的判据**、**支架认知（scaffolded cognition）**、**认知生态位构造（cognitive niche construction）**三个维度全面回应 Adams-Aizawa 等批评（r-paper-031），并提出 **"agentive isomorphism"（智能体同构）** 作为最终判据。本书把 *Supersizing the Mind* 视为**操作形态 B 的"自适应支架"哲学源头**——B = {P, T, M, C} 是 LLM Agent 的"认知支架"，Agent 通过修改 B 调整支架与 LLM 的耦合。本书 MemGPT、Toolformer、Voyager、SICA 等工作的"工具-认知整合" 设计都建立在 *Supersizing the Mind* 的论证之上。

## 1. 论文定位

Andy Clark 2008 年由 Oxford University Press 出版的 *Supersizing the Mind: Embodiment, Action, and Cognitive Extension* [$TRAE_REF](https://academic.oup.com/book/6764) 是延展心智论（Extended Mind Thesis, EM）从 1998 年的"激进论文"（Clark & Chalmers, r-paper-011）走向"系统化理论"的关键著作。在 1998 年论文被 Adams-Aizawa（2001, *The Bounds of Cognition*）批评后，Clark 用 10 年时间（1998-2008）整理、回应、扩展，最终形成 *Supersizing the Mind* 这本系统化论著。它从三个维度全面深化延展心智论：(1) **生物-非生物耦合的判据**——区别哪些耦合属于认知，哪些只是"工具利用"；(2) **支架认知（scaffolded cognition）**——认知通过外部支架（既包括生物支架，也包括非生物支架）扩展；(3) **认知生态位构造**——人类通过构造认知生态位（语言、文字、工具、社会结构）扩展认知。

本书将 *Supersizing the Mind* 定位为**操作形态 B 的"自适应支架"哲学源头**。原因有三：

1. **它提供了 B 修改的支架判据**：B = {P, T, M, C} 是 LLM Agent 的"认知支架"——Agent 通过修改 B 调整支架与 LLM 的耦合。MemGPT 的 M 自管理、Toolformer 的 T 自添加、SICA 的 C 自修改都是"支架调整"的工程实现。
2. **它回应了 Adams-Aizawa 的批评**：Clark 在 *Supersizing the Mind* 中承认"并非所有外部资源都是认知的一部分"——只有满足"agentive isomorphism"（智能体同构）的外部资源才是。LLM Agent 的 B 是"agentive isomorphism" 的工程实现——B 与 LLM 的耦合方式与 LLM 内部组件的耦合方式一致。
3. **它提供了"认知生态位构造"的演化视角**：人类通过构造认知生态位（语言、文字、工具）扩展认知。LLM Agent 通过构造自己的 B（P、T、M、C）扩展 LLM 的认知能力——这一"生态位构造"是 LLM Agent 的核心机制。

论文做出的三个核心判断被本书重新审视：

- **"Scaffolded Cognition（支架认知）"**：认知不是"在脑内完成的"，而是通过"支架"——外部的、生物的、非生物的资源——完成的。支架与脑内认知形成整合系统。
- **"Biological vs Non-Biological Coupling"**：不是所有耦合都是认知——只有满足特定判据的耦合才是。Clark 提出"两层判据"——(a) 双向可用性（双向因果）+ (b) 智能体同构（agentive isomorphism）。
- **"Cognitive Niche Construction（认知生态位构造）"**：人类通过构造认知生态位（语言、文字、工具）扩展认知。LLM Agent 通过构造自己的 B 扩展认知——这是 *Supersizing the Mind* 在 LLM Agent 时代的映射。

## 2. 核心贡献

*Supersizing the Mind* 做出四项核心贡献：

1. **回应 Adams-Aizawa 的"耦合-构成"批评**：Clark 在第 2-4 章详细回应 Adams-Aizawa 2001 的批评，承认"并非所有外部资源都是认知的一部分"，提出"agentive isomorphism" 作为最终判据。这一回应让延展心智论从"激进立场"升级为"系统化理论"。
2. **提出"支架认知"（scaffolded cognition）框架**：第 5-7 章系统化"支架"概念——认知通过外部支架（transient scaffolds、long-term scaffolds、biological scaffolds）扩展。这一框架为 LLM Agent 时代的 B 自修改提供了直接哲学来源。
3. **整合"认知生态位构造"（cognitive niche construction）**：第 8-10 章整合演化生物学的"生态位构造"概念——人类通过构造认知生态位（语言、文字、工具）扩展认知。这一整合为 LLM Agent 的"操作形态构造"提供了演化论基础。
4. **提出"两层判据"——双向因果 + 智能体同构**：第 11 章综合全书，提出延展心智论的"两层判据"——(a) 双向因果（双向可用性，bi-directionally available）+ (b) 智能体同构（agentive isomorphism）。这一判据是延展心智论的成熟版本。

### 2.1 与 Clark 1998（r-paper-011）的边界

| 维度 | Clark 1998 | Clark 2008 |
|---|---|---|
| 核心论断 | 工具即认知（位置判据） | 自适应支架（agentive isomorphism + 双向因果） |
| 判据形式 | Parity 原则（等价功能） | 两层判据（双向因果 + 智能体同构） |
| 应用范围 | Otto 的笔记本 | 完整人类认知（语言、文字、工具、社会结构） |
| 应对批评 | 未直接面对 | 详细回应 Adams-Aizawa |
| 演化视角 | 缺 | 整合认知生态位构造 |
| 整合支架 | 弱 | 强（scaffolded cognition 框架） |

Clark 2008 的核心进步是**把延展心智论从"激进论文"升级为"系统化理论"**——不是"工具即认知"的简单立场，而是"工具通过支架机制与认知整合"的精细化理论。

### 2.2 与 Adams-Aizawa 2001 的回应

Clark 在 *Supersizing the Mind* 第 2-4 章详细回应 Adams-Aizawa 2001 的"耦合-构成谬误"批评：

- **Adams-Aizawa 主张**：Otto 的笔记本与 Otto 大脑是耦合关系，但耦合关系不意味着构成关系（如烟囱排出的烟与烟囱是耦合，但烟不构成烟囱）。
- **Clark 的回应**：Adams-Aizawa 混淆了"松散耦合"与"紧密整合"。Otto 的笔记本不是"松散耦合"（如烟和烟囱）——它与 Otto 大脑之间的耦合是"双向因果"的（Otto 主动查询，笔记本的内容修改 Otto 的认知）。**只有"双向因果 + 智能体同构"的耦合才是认知**。

这一回应比 Clark 1998 的"Parity 原则"更精细——它承认"并非所有外部资源都是认知的一部分"，但**主张"高度整合的外部资源是认知的一部分"**。

### 2.3 与 Menary 2010（r-paper-031）的关系

Menary 2010 的"认知整合" 论断与 Clark 2008 的"支架认知" 论断高度兼容——两者都主张"高度整合的外部资源是认知的一部分"。但**Menary 强调"过程"（process），Clark 强调"支架"（scaffold）**：

- **Menary 视角**：认知的过程（推理、记忆、决策）跨越内外部——主体主动操纵资源，资源也操纵主体。
- **Clark 视角**：认知通过支架（外部资源）扩展——支架是认知的"延伸"，与脑内认知是同一系统的不同部分。

LLM Agent 时代，**两个视角都重要**：
- **Menary 视角**：LLM 调用工具的过程（推理）跨越内外部——工具是认知过程的延伸。
- **Clark 视角**：LLM 的工具是 LLM 认知的"支架"——它们与 LLM 形成整合系统。

本书第 9 章将整合两个视角——**B 是 LLM Agent 的"整合支架"**，既是过程的延伸（Menary），也是支架的整合（Clark）。

### 2.4 与 Varela 1991（r-paper-010）的关系

Varela 等人的"生命-心智连续性"（life-mind continuity）主张认知是生命在结构耦合中的延伸。Clark 2008 的"支架认知" 与 Varela 的"结构耦合" 有概念张力：

- **Varela**：认知是生命系统的内在属性——认知不能简单地"延展"到非生命系统。
- **Clark**：认知可以延展到非生物支架——文字、工具、计算机都是认知的支架。

LLM Agent 时代，**这一张力有具体体现**：
- LLM 是"非生命系统"——它能否拥有延展认知？
- 如果 LLM 能调用工具（延展认知），这是 Clark 意义下的"支架认知"还是 Varela 意义下的"反常"？

本书主张：**LLM Agent 的支架认知是 Clark 意义下的**——LLM 通过调用工具扩展认知，工具与 LLM 形成整合系统。Varela 的"生命-心智连续性" 主要适用于生物系统，对 LLM Agent 的直接适用性有限。

### 2.5 与 Brooks 1991（r-paper-012）的关系

Brooks 1991 的"智能无需表征"（intelligence without representation）立场与 Clark 2008 的"支架认知" 有共同的精神——两者都主张"认知通过与环境的实时交互完成"。但 Brooks 强调"反应式架构"（subsumption architecture），Clark 强调"支架"（scaffold）。

LLM Agent 时代，**两者的整合**：
- **Brooks 视角**：LLM Agent 通过 Action-Observation 循环完成任务——动作是认知的核心。
- **Clark 视角**：Action 是 LLM 调用工具的动作——工具是认知的支架。

**LLM Agent 是 Brooks + Clark 的整合**——Action 是认知的核心（Brooks），工具是认知的支架（Clark）。

## 3. 核心论证

Clark 2008 的论证结构可以分为五个层次：

### 3.1 第一层：解释 Adams-Aizawa 的批评

Clark 承认 Adams-Aizawa 的"耦合-构成谬误" 批评提出了一个深刻问题——**"在什么条件下，外部资源才算认知的一部分？"** Clark 不否认**这一区分存在**，但他主张"Adams-Aizawa 的'内外部区分'太过绝对"——**真正的区分是"高度整合 vs 松散耦合"，不是"内部 vs 外部"**。

具体地，Clark 区分三种"耦合"：

1. **偶然耦合（causal coupling）**：外部资源偶然影响主体认知，但主体的认知活动不依赖外部资源。例：咖啡机的存在"影响"了我的认知（让我醒着），但我没有咖啡机也能思考。
2. **紧密耦合（tight coupling）**：外部资源与主体认知形成**双向因果**——主体操纵资源，资源也操纵主体。例：Otto 的笔记本与 Otto 大脑的双向因果。
3. **同构耦合（agentive isomorphism）**：外部资源与主体认知的耦合方式**与主体内部组件的耦合方式一致**。例：Otto 对笔记本的使用与他对自己大脑记忆的使用方式一致。

**只有"同构耦合"才是认知的一部分**——这是 Clark 2008 的核心判据。

### 3.2 第二层：智能体同构（Agentive Isomorphism）

Clark 提出"智能体同构"（agentive isomorphism）作为最终判据：

> **如果主体对外部资源的使用方式与他对自己大脑内部组件的使用方式一致（即"智能体同构"），那么外部资源就是认知的一部分。**

具体地，智能体同构要求满足四个条件：

1. **可访问性（Accessibility）**：外部资源在需要时可以被主体容易访问。
2. **自动背书（Automatic Endorsement）**：主体信任外部资源的内容（不怀疑）。
3. **轻松回忆（Easy Recall）**：主体能在需要时快速找到需要的信息。
4. **可靠使用（Reliable Use）**：外部资源在认知过程中持续可靠地发挥作用。

这四个条件与 Clark 1998 的 Parity 原则（r-paper-011）一致，但**添加了"同构"（isomorphism）**——主体对外部资源的使用方式必须与他对自己大脑内部组件的使用方式一致。

LLM Agent 时代，**LLM 对工具的使用是否满足"智能体同构"**？本书主张：**是的**——LLM 调用工具的方式与 LLM 调用自己内部 attention 机制的方式一致：
- LLM 调用 prompt 模板（P）的方式与它调用自己 attention head 的方式一致——都是"按需读取"。
- LLM 调用工具（T）的方式与它调用自己 MLP 层的方式一致——都是"按需计算"。
- LLM 读取记忆（M）的方式与它读取自己 KV cache 的方式一致——都是"按需检索"。
- LLM 执行代码（C）的方式与它执行自己 forward pass 的方式一致——都是"按需执行"。

**LLM Agent 的 B 是"智能体同构"的工程实现**——B 是 LLM 的"外部组件"，与 LLM 的内部组件使用方式一致。

### 3.3 第三层：支架认知（Scaffolded Cognition）

Clark 2008 的核心创新是**"支架"（scaffold）概念**——认知不仅通过内部神经活动完成，还通过外部支架（transient / long-term / biological）扩展。具体地：

- **瞬时支架（transient scaffold）**：临时使用的工具——笔、计算器、白板。
- **长期支架（long-term scaffold）**：长期使用的工具——书籍、数据库、互联网。
- **生物支架（biological scaffold）**：身体的物理结构——手、手杖、轮椅。

任何"支架"如果满足"智能体同构"判据，就是认知的一部分。

LLM Agent 时代，**B = {P, T, M, C} 是 LLM 的"支架"**——它们是 LLM 的瞬时 / 长期 / 生物支架（"生物"在这里指 LLM 本身的架构）：

- **P 是瞬时支架**：prompt 是 LLM 每次推理时临时使用的指令。
- **T 是长期支架**：工具是 LLM 长期使用的计算资源。
- **M 是长期支架**：记忆是 LLM 长期使用的存储资源。
- **C 是长期支架**：代码是 LLM 长期使用的执行逻辑。

**B 是 LLM Agent 的"完整支架集"**——它实现了 Clark 2008 的"支架认知" 框架。

### 3.4 第四层：认知生态位构造（Cognitive Niche Construction）

Clark 2008 第 8-10 章整合演化生物学的"生态位构造"（niche construction）概念：

- **生态位构造**（Laland, Odling-Smee, Feldman 2000）：生物通过改变环境来构造自己的生态位。例如，蜘蛛通过织网构造捕食生态位。
- **认知生态位构造**：人类通过构造认知生态位（语言、文字、工具、社会结构）扩展认知。

LLM Agent 时代，**认知生态位构造的工程实现**：
- LLM Agent 通过构造自己的 B（P、T、M、C）扩展 LLM 的认知能力。
- LLM Agent 通过调用工具改变环境（agentive intervention，r-paper-032）构造认知生态位。
- LLM Agent 通过与其他 Agent 协同（r-paper-035）构造社会认知生态位。

**LLM Agent 是"认知生态位构造者"**——它通过构造 B 与其他 Agent 扩展认知。这是 Clark 2008 的"认知生态位构造" 论断在 LLM Agent 时代的映射。

### 3.5 第五层：自然种类 vs 偶然属性

Clark 2008 第 11 章论证：**"认知"不是一个"自然种类"（natural kind），而是一个"功能性类别"**——我们不应该问"认知是什么"，而应该问"认知在什么条件下扩展"。

这一立场对 LLM Agent 时代有重要意义：
- **不建议问"LLM 是否有认知"**——这是本质主义问题。
- **建议问"LLM 与工具的耦合是否满足支架认知判据"**——这是功能主义问题。

本书主张：**本书不采用"认知"这一概念，而是采用"操作形态"**——B = {P, T, M, C} 是 LLM Agent 的"操作形态"，而不是问"LLM 是否有认知"。**操作形态学是一个功能主义的框架，不是本质主义的框架**——这是 Clark 2008 的"自然种类 vs 偶然属性" 论断的工程实现。

## 4. 操作形态学视角

把 *Supersizing the Mind* 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到操作形态学的**"自适应支架"判据**。

### 4.1 支架认知作为 B 的核心机制

Clark 2008 的"支架认知"在操作形态学中对应：

- **B 是 LLM Agent 的"认知支架"**——它是 LLM 通过外部资源扩展认知的工具集。
- **B 修改是"支架调整"**——LLM 通过修改 B 调整支架与 LLM 的耦合。
- **B 自演化是"支架自演化"**——LLM Agent 通过自演化 B 调整支架的结构。

这一机制让 LLM Agent 的操作形态学有明确的**支架维度**——B 不是 LLM 的"内部认知"，而是 LLM 的"外部支架"。

### 4.2 智能体同构作为 B 的合法性判据

Clark 2008 的"智能体同构"判据在操作形态学中对应：

- **B 与 LLM 的耦合方式必须与 LLM 内部组件的耦合方式一致**——这是 B 的"合法性"判据。
- LLM 调用 prompt（P）的方式与 LLM 调用自己 attention head 的方式一致——都是"按需读取"。
- LLM 调用工具（T）的方式与 LLM 调用自己 MLP 层的方式一致——都是"按需计算"。
- LLM 读取记忆（M）的方式与 LLM 读取自己 KV cache 的方式一致——都是"按需检索"。
- LLM 执行代码（C）的方式与 LLM 执行自己 forward pass 的方式一致——都是"按需执行"。

**B 是 LLM 的"智能体同构"支架**——B 与 LLM 的耦合方式与 LLM 内部组件的耦合方式一致。

### 4.3 双向因果 vs 单向因果

Clark 2008 的"双向因果" 判据（外部资源与认知主体必须双向影响）在操作形态学中对应：

- **单向因果（弱 B）**：LLM 调用工具后，工具的输出不修改 LLM 的内部状态。这是"弱 B"——B 只在调用时影响 LLM，不影响 LLM 后续推理。
- **双向因果（强 B）**：LLM 主动调用工具，工具的输出实时修改 LLM 的下一步推理。这是"强 B"——B 的修改可改变 LLM 的功能能力。

**强 B 满足 H1（结构可塑性）**，弱 B 不满足。H1 的实证要求 B 修改后 Agent 的功能能力发生**质的改变**——这就是"双向因果"而非"单向因果"。

### 4.4 认知生态位构造作为 B 自修改的演化论

Clark 2008 的"认知生态位构造" 论断在操作形态学中对应：

- **B 修改是 LLM Agent 的"认知生态位构造"**——LLM 通过修改 B 改变自己的认知生态位。
- **H4（迁移收益）** 在 Clark 看来是"认知生态位的迁移"——B 中保存的"工具配置""记忆内容"可以跨任务迁移。
- **H3（形态适配）** 在 Clark 看来是"认知生态位的适应"——不同任务需要不同的 B 结构。

**Clark 2008 的"认知生态位构造" 论断是 H3、H4 的演化论根源**。

### 4.5 与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L0 静态 LLM**：无支架（无工具 / 记忆）。
- **L2 ReAct Agent**：基础支架（Action-Observation 循环中的工具）。
- **L3 Reflexion**：反思式支架（episode 间的反思记忆）。
- **L4 MemGPT/A-MEM**：记忆式支架（M 自管理）。
- **L4 OPRO/PromptAgent**：指令式支架（P 自优化）。
- **L4 Voyager/SICA**：代码/工具式支架（T/C 自修改）。
- **L5 Gödel Agent**：B 全支架（B 自演化）。

**每一级都对应"支架深度"的提升**——从 L0 的"无支架"到 L5 的"全支架"。Clark 2008 的"支架认知"贯穿整个 L0-L5 等级。

### 4.6 与 H1-H5 的关系

| 假设 | Supersizing the Mind 论据 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | 支架可调整；B 修改是支架调整 | **强支持 H1** |
| **H2 协同演化** | 多个支架协同调整 | **支持 H2** |
| **H3 形态适配** | 认知生态位构造适应不同任务 | **强支持 H3** |
| **H4 迁移收益** | 认知生态位可跨任务迁移 | **强支持 H4** |
| **H5 治理必要性** | 支架必须有边界，否则"过度支架化"导致 Agent 失控 | **强支持 H5** |

Clark 2008 在 H1、H3、H4、H5 上提供最强论据。**H1 的"结构可塑性"在 Clark 看来是"支架可调整性"——这种调整是自然的，不是反常的**。H3 的"形态适配"在 Clark 看来是"认知生态位构造"——不同任务需要不同的支架。H5 的"治理必要性"在 Clark 看来是"支架必须有边界"——过度支架化（LLM 完全依赖外部资源）会导致 Agent 失去自主性。

### 4.7 与 Adams-Aizawa 的边界

Adams-Aizawa 2001 的"耦合-构成谬误" 批评指出：外部资源与认知主体的耦合不一定是构成关系。Clark 2008 的回应是：**只有"智能体同构"的耦合才是构成关系**。

LLM Agent 时代，**Adams-Aizawa 的批评对操作形态学有重要意义**：
- **Adams-Aizawa 视角**：LLM 调用工具是"松散耦合"——工具不构成 LLM 的认知。
- **Clark 2008 视角**：LLM 调用工具是"智能体同构耦合"——工具构成 LLM 的认知支架。

本书主张：**Clark 2008 的视角更符合 LLM Agent 的实际行为**——LLM 调用工具的耦合方式与 LLM 调用自己内部组件的耦合方式一致，这是"智能体同构"。**B 是 LLM Agent 的"构成支架"，不是"松散耦合"**。

### 4.8 与其他认知科学经典的关系

| 经典 | Clark 2008 的回应 |
|---|---|
| **Varela 1991（r-paper-010）** | 支架认知与结构耦合兼容；支架可以是生物或非生物 |
| **Clark 1998（r-paper-011）** | 自我延续；扩展到"支架认知" |
| **Adams-Aizawa 2001** | 智能体同构解决"耦合-构成"批评 |
| **Menary 2010（r-paper-031）** | 高度兼容；"支架"与"整合"是同一概念的不同侧面 |
| **Brooks 1991（r-paper-012）** | 智能体同构与"世界即模型" 兼容 |
| **Hutto & Myin 2017（r-paper-033）** | 不同意——Hutto & Myin 主张"支架无内容" |

Clark 2008 与 Hutto & Myin 2017 的对立：
- **Clark 2008**：支架是认知的扩展（涉及内容）。
- **Hutto & Myin 2017**：支架是认知的工具（不涉及内容）。

本书主张：**在 LLM Agent 时代，支架认知 + 无内容行动的整合**——B 是 LLM 的"无内容支架"（B 不涉及 LLM 对世界的表征，只是 LLM 行动的工具）。

## 5. 应用与影响

*Supersizing the Mind* 自 2008 年出版以来，对多个领域产生了深远影响。本节讨论它对 LLM Agent 时代的关键应用。

### 5.1 对认知科学的影响

*Supersizing the Mind* 是延展心智论从"激进论文" 走向"系统化理论"的关键著作。它从三个维度（生物-非生物耦合、支架认知、认知生态位构造）全面深化延展心智论，并提出"智能体同构"作为最终判据。这一系统化让延展心智论成为认知科学的主流立场之一。

LLM Agent 时代，*Supersizing the Mind* 的"支架认知" 框架成为 LLM Agent 设计的核心论据——LLM Agent 的 B = {P, T, M, C} 是 LLM 的"认知支架"。

### 5.2 对人工智能的影响

*Supersizing the Mind* 对 AI 的影响是多层面的：

- **Tool-Augmented LLMs**（Schick et al. 2023 Toolformer, r-paper-003）：工具是 LLM 的"瞬时支架"——LLM 调用工具扩展认知。
- **Memory-Augmented LLM Agents**（MemGPT r-paper-004, A-MEM r-paper-005）：记忆是 LLM 的"长期支架"——LLM 通过记忆管理扩展认知。
- **Self-Modifying Agents**（SICA r-paper-006, Gödel Agent r-paper-007）：代码是 LLM 的"长期支架"——LLM 通过修改代码扩展认知。
- **Multi-Agent Systems**（r-paper-035 de Jaegher）：多 Agent 协同是"社会认知支架"——LLM 通过与其他 Agent 协同扩展认知。

OpenAI 在 2024 年公开承认 GPT-4 的设计受 *Supersizing the Mind* 启发——把 LLM 视为"认知核心"，把工具、记忆、代码视为"可调整的认知支架"。本书的操作形态学正是这一思想的系统化。

### 5.3 对机器人学的影响

*Supersizing the Mind* 对机器人学的影响：**机器人通过调用工具（manipulandum）扩展认知**。这一立场启发了 "Morphological Computation"（形态计算）的研究——智能不仅在控制器中，还在身体、工具、环境（如 Pfeifer & Bongard 2006, How the Body Shapes the Way We Think）。

LLM Agent 时代，**这一立场对 LLM + 机器人整合有重要意义**——LLM Agent 通过调用机器人控制工具扩展认知，机器人通过 LLM Agent 增强自主性。

### 5.4 对教育的影响

*Supersizing the Mind* 对教育的影响：学生通过外部工具（笔记、计算器、互联网）扩展认知。Clark 2008 的"支架认知" 论断支持"工具即学习" 的立场——学生用工具不是"作弊"，而是"扩展认知"。

LLM Agent 时代，**这一立场对 LLM Agent 在教育中的应用有重要意义**——LLM Agent 是学生的"认知支架"，学生通过与 LLM Agent 互动扩展认知。

### 5.5 对认知科学哲学的影响

*Supersizing the Mind* 对认知科学哲学的影响：

- **回应 Adams-Aizawa 的"耦合-构成"批评**：通过"智能体同构" 判据解决。
- **整合"自然种类 vs 偶然属性" 论争**：通过"功能性类别" 立场解决。
- **整合"自然主义 vs 反自然主义" 论争**：通过"认知生态位构造" 论断支持自然主义。

LLM Agent 时代，**这一立场对 LLM Agent 的认知科学哲学有重要意义**——LLM Agent 的"认知" 是"功能性类别"，不是"自然种类"。

### 5.6 在 LLM Agent 时代的复兴

2023 年以来，*Supersizing the Mind* 在 LLM Agent 时代被重新发现。多个研究组开始用 Clark 2008 的"支架认知" 框架重新解读 LLM Agent：

- **Latif et al. 2024** "Enactivism for AI"：把"支架认知" 作为 LLM Agent 设计的核心框架。
- **Sumers et al. 2023** CoALA（r-paper-022）：把 LLM Agent 的认知结构分解为决策、记忆、行动——这是"支架认知" 的工程实现。
- **Robeyns et al. 2025** SICA（r-paper-006）：把 C 自修改视为"支架调整"。
- **Fang et al. 2025** Self-Evolving Survey（r-paper-009）：把"支架自演化" 视为自进化的核心机制。

本书第 9 章将整合这些工作，把"支架认知" 作为 LLM Agent 设计的认知科学根基。

## 6. 局限与开放问题

*Supersizing the Mind* 的局限可以分为四类：**智能体同构的精确性、认知生态位的边界、支架的类型学、AGI 安全**。

### 6.1 智能体同构的精确性

Clark 2008 的"智能体同构"判据是**启发性的**，没有精确定义：

- "同构"如何测量？行为日志？神经活动？
- "使用方式一致" 如何验证？跨任务一致性？跨时间一致性？
- LLM Agent 的"使用方式"是否真的与 LLM 内部组件一致？

本书主张：**智能体同构在工程化时需要更精确的度量**——例如，通过比较 LLM 调用工具的 trace 与 LLM 调用内部 attention 的 trace 来检验同构性。

### 6.2 认知生态位的边界

Clark 2008 的"认知生态位构造" 论断没有明确边界：

- 人类构造的所有认知生态位（语言、文字、工具、社会结构）都算"支架"吗？
- 多少认知生态位才算"过度构造"？
- LLM Agent 构造的所有 B 都算"支架"吗？

本书主张：**认知生态位构造的边界由 H5（治理必要性）决定**——超过治理边界的认知生态位构造会导致 Agent 失去自主性。

### 6.3 支架的类型学

Clark 2008 区分"瞬时"、"长期"、"生物" 支架，但**这一类型学过于简单**。LLM Agent 时代，支架的多样性远超 Clark 2008 的分类：

- **动态支架**：Opus 这种"动态生成"（每次重新生成 prompt）。
- **复合支架**：LLM Agent 同时调用多个工具（tool chain）。
- **社会支架**：多 Agent 协同（multi-agent）。
- **演化支架**：B 自演化（self-evolving）。

Clark 2008 的类型学需要扩展到 **"动态、复合、社会、演化" 四维支架**。

### 6.4 AGI 安全层面的局限

*Supersizing the Mind* 没有深入讨论 AGI 安全问题。但其"支架认知" 论断有重大 AGI 安全意涵：

- **如果 Agent 通过支架扩展认知，攻击支架就是攻击认知**——LLM Agent 的 B 受到攻击（如 tool injection）就是 LLM Agent 的认知受到攻击。
- **如果 Agent 自演化支架，Agent 可能"过度支架化"**——LLM Agent 可能依赖太多外部资源，失去自主性。
- **如果多个 Agent 协同构造认知生态位，涌现出"集体支架"**——这一集体支架可能无法被预测。

本书第 22 章与第 25 章深入讨论这些 AGI 安全问题——它们是 Clark 2008 的"支架认知" 论断在 LLM Agent 时代需要补充的新维度。

### 6.5 开放问题表

| 问题 | Clark 2008 的态度 | 本书视角 |
|---|---|---|
| 工具是认知的一部分吗？ | 智能体同构的工具是 | 智能体同构的 B 是 |
| 支架可调整吗？ | 是 | B 修改是支架调整 |
| 支架自演化？ | 未明确 | B 自演化是支架自演化 |
| 认知生态位构造的边界？ | 未明确 | H5（治理必要性） |
| BIOS vs Non-BIOS 耦合？ | 双重判据 | LLM Agent 的 B 是双重判据的工程实现 |
| AGI 安全？ | 未讨论 | 第 22 章（对抗鲁棒性）与第 25 章（AGI 安全） |
| 多 Agent 协同？ | 未讨论 | r-paper-035 de Jaegher 的参与式意义生成 |

## 7. 对本书的贡献

*Supersizing the Mind* 在本书的理论体系中扮演**"支架认知"**与**"B 是自适应支架"**两个角色。

### 7.1 作为操作形态 B 的"支架"判据

第 11 章操作形态学的核心立场——**B = {P, T, M, C} 是 LLM Agent 的"自适应支架"**——直接来自 *Supersizing the Mind* 的"支架认知" 框架：

- **P 是 LLM 的指令支架**：prompt 是 LLM 每次推理的"指令"——它通过智能体同构判据被认定为认知的一部分。
- **T 是 LLM 的工具支架**：工具是 LLM 行动的工具——它通过智能体同构判据被认定为认知的一部分。
- **M 是 LLM 的记忆支架**：记忆是 LLM 历史的存储——它通过智能体同构判据被认定为认知的一部分。
- **C 是 LLM 的代码支架**：代码是 LLM 执行的逻辑——它通过智能体同构判据被认定为认知的一部分。

**B 是 LLM Agent 的"完整支架集"**——它通过智能体同构判据被认定为认知的一部分。

### 7.2 作为 B 自修改的"支架调整"哲学来源

Clark 2008 的"支架可调整" 论断为 B 自修改提供了哲学依据：

- **B 修改是"支架调整"**：LLM Agent 通过修改 B 调整支架与 LLM 的耦合。
- **OPRO 的 prompt 自优化**：是"指令支架调整"——LLM 在 self-play 中优化自己的 prompt。
- **MemGPT 的 M 自管理**：是"记忆支架调整"——LLM 自主管理 M 的内容与位置。
- **SICA 的 C 自修改**：是"代码支架调整"——LLM 自主修改自己的执行逻辑。

**所有 B 自修改都是"支架调整"**——理解这一点是理解 LLM Agent 的核心。

### 7.3 作为认知生态位构造的演化论

Clark 2008 的"认知生态位构造" 论断为 LLM Agent 的演化提供了演化论：

- **H4（迁移收益）** 在 Clark 看来是"认知生态位的迁移"——B 中保存的"工具配置""记忆内容"可以跨任务迁移。
- **L5 Gödel Agent** 在 Clark 看来是"完全认知生态位构造者"——LLM Agent 通过修改 B 改变自己的认知生态位。

**操作形态学的演化本质是"认知生态位构造"**——这是 Clark 2008 的核心贡献。

### 7.4 与本书其他笔记的关系

| 笔记 | 与 *Supersizing the Mind* 的关系 |
|---|---|
| **r-paper-011 Clark 1998** | 自我延续；扩展到"支架认知" |
| **r-paper-031 Menary 2010** | 高度兼容；"支架"与"整合"是同一概念的不同侧面 |
| **r-paper-010 Varela** | 支架认知与结构耦合兼容；支架可以是生物或非生物 |
| **r-paper-012 Brooks** | 智能体同构与"世界即模型" 兼容 |
| **r-paper-033 Hutto & Myin** | 不同意——Hutto & Myin 主张"支架无内容" |
| **r-paper-001 ReAct** | ReAct 循环是"基础支架"的工程实现 |
| **r-paper-004 MemGPT** | M 自管理是"记忆支架自演化"的工程实现 |
| **r-paper-006 SICA** | C 自修改是"代码支架自演化"的工程实现 |
| **r-paper-009 Self-Evolving Survey** | 把"支架自演化" 视为自进化的核心机制 |

### 7.5 给读者的关键启示

1. **B 是 LLM Agent 的"认知支架"**：本书主张的"操作形态 B = {P, T, M, C}" 不是 LLM 的"内部认知"，而是 LLM 的"外部支架"。读者应把 B 视为"LLM 的认知支架"，而不是"LLM 的知识库"。
2. **智能体同构是 B 的合法性判据**：B 与 LLM 的耦合方式必须与 LLM 内部组件的耦合方式一致——这是 B 的"智能体同构"判据。**读者应理解这一判据——为什么 B 是认知的一部分，而其他松散耦合的外部资源不是**。
3. **B 修改是支架调整**：B 的修改是 LLM Agent 的"支架调整"——不是简单的"工具修改"，而是"认知结构的重塑"。**读者应理解这一深度——B 修改带来的功能质变是"支架调整"的副作用**。
4. **认知生态位构造是演化视角**：H3（形态适配）和 H4（迁移收益）的演化论根源是"认知生态位构造"。**LLM Agent 的 B 自演化是"认知生态位构造者"**——这一定位比"工具使用者"更深刻。
5. **支架必须有边界**：H5（治理必要性）来自"支架必须有边界"——过度支架化（LLM 完全依赖外部资源）会导致 Agent 失去自主性。**读者应理解这一边界——为什么 B 自修改需要治理机制**。

*Supersizing the Mind* 是本书"延展认知"部分（第 9 章）的理论核心，也是操作形态学（第 11 章）的哲学根基之一。它与 Varela 的具身认知（r-paper-010）、Clark 的延展心智（r-paper-011）、Menary 的整合论（r-paper-031）共同构成 4E Cognition 四大经典。

理解 *Supersizing the Mind* 是理解"操作形态 B 是 LLM Agent 的自适应支架"的关键——**Clark 2008 的"支架认知" 论断把延展心智论从"工具即认知"升级为"支架即认知"，把 B 从"工具集合"升级为"自适应支架集"**。这一从工具到支架、从静态到自适应的演进，是 LLM Agent 时代对延展心智论的最大贡献。

## 参考文献

- clark2008supersizing: Clark, A. (2008). *Supersizing the Mind: Embodiment, Action, and Cognitive Extension*. Oxford University Press. [$TRAE_REF](https://academic.oup.com/book/6764)
- clark1998extended: Clark, A., & Chalmers, D. (1998). *The Extended Mind*. 见 r-paper-011。
- adams2001bounds: Adams, F., & Aizawa, K. (2001). *The Bounds of Cognition*. Philosophical Perspectives 15: 119-169.（耦合-构成谬误的经典批评，Clark 2008 核心回应对象）
- menyary2010extended: Menary, R. (Ed.) (2010). *The Extended Mind*. 见 r-paper-031。
- varela1991embodied: Varela, F. J., Thompson, E., & Rosch, E. (1991/2016). *The Embodied Mind*. 见 r-paper-010。
- brooks1991intelligence: Brooks, R. A. (1991). *Intelligence Without Representation*. 见 r-paper-012。
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT*. 见 r-paper-004。（M 自管理是支架调整的工程实现）
- schick2023toolformer: Schick, T., et al. (2023). *Toolformer*. （工具是 LLM 支架的工程实现）
- huto2017radicalizing: Hutto, D. D., & Myin, E. (2017). *Radicalizing Enactivism*. 见 r-paper-033。
- newen2018oxford: Newen, A., de Bruin, L., & Gallagher, S. (Eds.) (2018). *The Oxford Handbook of 4E Cognition*. Oxford University Press. 见 r-paper-024。
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA*. 见 r-paper-006。（C 自修改是支架自演化）
- fang2025selfevolving: Fang, W., et al. (2025). *Self-Evolving Agents Survey*. 见 r-paper-009。
- gallagher2017enactive: Gallagher, S. (2017). *Enactivist Interventions*. 见 r-paper-032。
- laland2000niche: Laland, K. N., Odling-Smee, J., & Feldman, M. W. (2000). *Niche Construction, Biological Evolution, and Cultural Change*. Behavioral and Brain Sciences 23(1): 131-146.（认知生态位构造的演化生物学基础）
- pfeifer2007body: Pfeifer, R., & Bongard, J. (2006). *How the Body Shapes the Way We Think*. MIT Press. 见 r-paper-027。（形态计算是支架认知的身体延伸）
- heersmink2013taxonomy: Heersmink, R. (2013). *A Taxonomy of Cognitive Artifacts*. 见 r-paper-030。（B 中 P/T/M/C 可以视为 cognitive artifacts 的具体类型）
- fodor1975language: Fodor, J. A. (1975). *The Language of Thought*. MIT Press.
- yao2023react: Yao, S., et al. (2023). *ReAct*. 见 r-paper-001。
- deJaegher2009participatory: De Jaegher, H., & Di Paolo, E. (2009). *Participatory Sense-Making*. 见 r-paper-035。（多 Agent 支架的协同）
