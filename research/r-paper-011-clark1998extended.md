---
note_id: r-paper-011
title: 延展心智：奥托笔记本、Parity 原则与主动外部主义（The Extended Mind）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 9, Ch 11]
related_papers: [clark1998extended, adams2001bounds, varela1991embodied, brooks1991intelligence, packer2023memgpt, xu2025amem, yao2023react, fang2025selfevolving, robeyns2025sica]
keywords: [extended mind, Clark, parity principle, active externalism, Otto notebook, coupling-constitution fallacy, Adams-Aizawa, memGPT, agentive isomorphism]
---

# r-paper-011：延展心智：奥托笔记本、Parity 原则与主动外部主义

> Clark 与 Chalmers 1998 年发表的 *The Extended Mind*（Analysis 期刊）是 4E Cognition 运动最具影响力的论证之一——它用 Otto/Inga 的"笔记本思维"思想实验提出 **Parity 原则**：如果一个外部资源能像脑内记忆一样发挥功能，那它就是认知的一部分。本书把这一原则作为**操作形态 B 中 M 与 T 的合法性来源**——MemGPT、A-MEM 等记忆自管理工作是延展心智论在 LLM Agent 时代的工程实现。但 Adams 与 Aizawa 的"耦合 ≠ 构成"批评深刻地揭示了延展心智论的关键边界——这一边界正是操作形态 B 与"延展心智"在哲学上的根本分歧：**B 中的 M 是可被 Agent 主动重塑的，而 Otto 的笔记本是被动的、固定的**。

## 1. 论文定位

Andy Clark 与 David Chalmers 在 1998 年发表于 *Analysis* 期刊的 *The Extended Mind*（doi:10.1093/analys/58.1.7 [$TRAE_REF](https://doi.org/10.1093/analys/58.1.7)）是认知科学哲学的经典论文。它通过 **Otto/Inga 思想实验**提出"认知系统可以延展到身体之外"的论断：如果一个阿尔茨海默症患者 Otto 通过随身笔记本弥补记忆缺陷，且使用笔记本的方式与 Inga 用脑内记忆一样，那 Otto 的笔记本**就是 Otto 认知的一部分**。这一看似简单的论断直接挑战了认知科学的传统边界——"认知止于头骨内"。

本书将 *The Extended Mind* 定位为**操作形态 B 中 M 与 T 组件的合法性来源**。延展心智论主张"外部工具是认知的一部分"，这正是 LLM Agent 时代的核心设计原则：Agent 的 prompt、工具、记忆、代码——这些"在 LLM 之外"的组件——是 Agent 认知的合法部分。

论文做出的三个核心判断被本书第 9 章与第 11 章重新审视：

- **Parity 原则（Parity Principle）**：如果一个外部资源在认知中发挥的功能与脑内组件"等价"（on a par），则该外部资源就是认知的一部分。这一原则是延展心智论的核心判据。
- **主动外部主义（Active Externalism）**：认知不局限于大脑，而是延伸到身体与世界——环境中的资源是认知系统的合法组成部分。这是与"被动外部主义（Passive Externalism，如 Putnam 的语义外部论）"的关键差异：前者强调**认知过程本身依赖外部资源**，后者只强调**认知内容被外部决定**。
- **延展信念（Extended Belief）**：Otto 对现代艺术博物馆的信念（"在 53 街"）与 Inga 的同等信念（"在 53 街"）**在认知地位上是平等的**——尽管前者存储在笔记本中，后者存储在脑中。

这三个判断共同构成"工具是认知的一部分"的哲学论据。本书主张：**操作形态 B 是这一哲学论断在 LLM Agent 时代的工程化映射**。

## 2. 核心贡献

*The Extended Mind* 做出三项核心贡献，按对本书的影响力排序：

1. **形式化 Otto/Inga 思想实验**：明确构造一个认知科学哲学中最著名的思想实验——Otto（阿尔茨海默症患者）通过随身笔记本记忆信息，Inga（健康人）通过脑内记忆。两人在面对同一任务时（"去现代艺术博物馆"）使用相似的信息检索流程，但 Otto 依赖外部笔记本。Clark 与 Chalmers 论证：**如果 Inga 的脑内信念是"信念"，Otto 的笔记本信念也应该是"信念"——否则我们就是在做无根据的"头骨内偏见"**。
2. **提出 Parity 原则**：明确"等价功能 = 等价认知"——一个外部资源如果能像脑内资源一样发挥功能，那它就是认知的合法组成部分。这一原则为"工具即认知"提供了判据。
3. **论证主动外部主义**：区别于 Putnam 的语义外部论（被动外部主义），Clark 与 Chalmers 主张**认知过程本身**就依赖外部资源——Otto 思考"博物馆在哪里"时，他**正在**使用笔记本，不是"在想完之后再查笔记本"。这是**过程层面**的外部主义，而非**内容层面**的外部主义。

### 2.1 与传统认知科学边界的对比

| 传统认知科学（cognitivism） | 延展心智论（Clark & Chalmers） |
|---|---|
| 认知止于头骨内 | 认知延伸到身体与世界 |
| 信念存储在脑中 | 信念可存储在笔记本/工具/环境 |
| 思考是大脑的过程 | 思考是大脑 + 工具的协同过程 |
| 外部资源只是"输入" | 外部资源是认知的一部分 |
| 关注内部表征 | 关注认知-环境耦合 |

这一对比是本书"操作形态 B 是否是认知一部分"的根源：传统认知科学把 B 视为"外部输入"，延展心智论把 B 视为"认知本体"。本书采纳后者立场。

### 2.2 与具身认知（Varela）的关系

Varela 等人（r-paper-010）的具身认知强调"身体是认知的一部分"，Clark 与 Chalmers 的延展心智强调"工具是认知的一部分"。两者可以视为"具身认知的扩展"：

- **具身认知**：身体（含感觉器官、肌肉、骨骼）是认知。
- **延展心智**：工具（笔记本、电脑、网络）是认知。

本书第 8-9 章将两者整合为"4E Cognition"——认知既是具身的、嵌入的、生成的，也是延展的。在 LLM Agent 时代，**操作形态 B = {P, T, M, C} 是延展心智论的工程实现**：T 是"工具即认知"，M 是"记忆即认知"，P 是"指令即认知"，C 是"代码即认知"。

### 2.3 与 Brooks（r-paper-012）的关系

Brooks（r-paper-012）主张"世界是自身最好的模型"——这与延展心智论有共同的精神：世界不是表征的对象，而是认知的资源。但两者也有差异：

- **延展心智论**：认知通过"等价功能"延伸到工具（如 Otto 的笔记本）。
- **Brooks**：智能通过"与环境实时交互"涌现（如机器人的行为）。

本书第 12 章将进一步整合两者：延展心智论提供"认知的边界"（工具是认知），Brooks 提供"认知的实现"（世界是模型）。

## 3. 核心论证

*The Extended Mind* 的论证结构可以分为四个层次：

### 3.1 第一层：Otto/Inga 思想实验

Clark 与 Chalmers 提出以下场景：

> Inga 听说现代艺术博物馆在 53 街，她从脑内记忆中回忆"博物馆在 53 街"，然后去 53 街。Otto 是阿尔茨海默症患者，他从随身笔记本中查找"博物馆在 53 街"的记录，然后去 53 街。

两人行为上完全一致——都是从记忆中检索"博物馆在 53 街"，然后采取行动。但传统认知科学会说：Inga 有"博物馆在 53 街"的信念（因为存储在脑内），Otto 没有（因为存储在笔记本）。这一区分在 Clark 与 Chalmers 看来是**无根据的偏见**——它假设"信念必须有脑内存储"，但没有给出**任何独立于存储位置的判据**来区分 Inga 与 Otto。

他们的论证是：

> "If, as we confront some new situation, we could be said to have a belief that p only if p were in our biological memory, then the beliefs of amnesiacs like Otto would be impossible to explain. But we can give a perfectly ordinary explanation of Otto's behavior in terms of his having the belief that the museum is on 53rd Street... If we accept that Otto has this belief, then we must accept that the notebook is part of the cognitive apparatus that realizes his belief."（Clark & Chalmers 1998, p. 13）

### 3.2 第二层：Parity 原则

基于 Otto/Inga 思想实验，Clark 与 Chalmers 提炼出 Parity 原则：

> **如果一个外部资源在认知过程中发挥的功能与脑内组件等价（on a par），则它就是认知的一部分。**

具体地，他们列出四个判据（Clark & Chalmers 1998, p. 17）：

1. **Constant accessibility**（持续可访问）：资源可以随时被 Otto 使用。
2. **Automatic endorsement**（自动背书）：Otto 信任笔记本中的信息（没有怀疑）。
3. **Easy recall**（轻松回忆）：Otto 在需要时能快速找到信息。
4. **Trust/Reliability**（信任/可靠）：Otto 信任笔记本不会出错。

满足这四个判据的外部资源（如 Otto 的笔记本）就是认知的一部分。

### 3.3 第三层：主动外部主义

Clark 与 Chalmers 区分**被动外部主义**与**主动外部主义**：

- **被动外部主义**（Putnam 1975, Burge 1979）：信念的**内容**由社会/物理环境决定（"水"指 H₂O，因为化学环境决定）。
- **主动外部主义**（Clark & Chalmers 1998）：认知的**过程**本身依赖外部资源——Otto 在思考时**正在**使用笔记本，不是"先想完，再查笔记本"。

主动外部主义的关键洞察：**认知不是先在脑内完成，再输出到世界**。Otto 的"思考博物馆在哪里"的过程**包括**他伸手到口袋拿笔记本、翻页、阅读——这一**完整过程**就是 Otto 的认知。这等价于把认知的边界推到笔记本、推到笔记本的生产工厂、推到 Otto 所在的物理环境。

本书第 9 章深入讨论这一论断对 LLM Agent 设计的含义：**Agent 的"思考"包括它调用工具的过程——LLM + tool_use 是一个完整的认知过程，而不是"LLM 先想，再调用工具"**。

### 3.4 第四层：响应 Adams & Aizawa 的批评

Fred Adams 与 Ken Aizawa 在 2001 年发表 *The Bounds of Cognition*（r-note-001 中已提及）针对延展心智论提出尖锐批评：

> **耦合 ≠ 构成（coupling-constitution fallacy）**。Otto 的笔记本与 Otto 大脑是耦合关系，但耦合关系不意味着构成关系——就像烟囱排出的烟与烟囱是耦合关系，但烟不构成烟囱。

Adams & Aizawa 论证延展心智论犯了**因果耦合与构成关系的混淆**——Otto 依赖笔记本，但笔记本不**是** Otto 认知的一部分，因为笔记本没有**认知过程所需的内在状态**（如神经活动）。他们提出**认知的内在约束**：

> **认知过程必须是可错性的（fallible）、内在结构依赖的（inner-state-dependent）、可被因果解释的（causally explicable）。**

这些特征只有脑内神经活动满足，外部笔记本不满足——因此 Otto 的笔记本**不是** Otto 的认知，只是 Otto 认知的辅助工具。

Clark 在 *Supersizing the Mind*（2008）中对 Adams & Aizawa 的批评做出详细回应，提出**主动外部主义需要"agentive isomorphism"（智能体同构）**：如果 Otto 对笔记本的使用方式与他对自己大脑的使用方式一致（即满足 Parity 的四个判据），那笔记本就是 Otto 认知的一部分。但 Adams & Aizawa 仍坚持：**isomorphism 不等于 identity，外部资源的"使用方式相似"不改变它是外部资源的事实**。

本书对这一争论的立场是：**Adams & Aizawa 的批评揭示了延展心智论的关键边界——它适用于"被动存储 + 主动调用"的资源（如笔记本），但不适用于"动态修改结构"的资源（如 MemGPT 的 M）**。操作形态 B 中 M 的**自修改**（如 A-MEM 让 LLM 创建链接、MemGPT 让 LLM 自主 page-in/page-out）超出了延展心智论的范畴——它们不是"延展心智"，而是"自演化形态"。

## 4. 操作形态学视角

把 *The Extended Mind* 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到关键论断：**延展心智论是操作形态 B 的"合法性来源"，但也是其"边界"**。

### 4.1 延展心智论在 B 中的对应

| 延展心智论组件 | 操作形态学对应 | 关系 |
|---|---|---|
| Otto 的笔记本 | Agent 的 M（长期记忆） | 直接对应 |
| Otto 的工具 | Agent 的 T（工具） | 直接对应 |
| Inga 的脑内记忆 | LLM 参数（冻结部分） | 隐喻对应 |
| Inga 的脑内推理 | LLM 的推理（冻结部分） | 隐喻对应 |
| Inga 的指令（去博物馆） | Agent 的 P（prompt） | 间接对应 |
| Inga 的执行代码 | Agent 的 C（执行机制） | 间接对应 |

延展心智论**最直接对应**的是 M 与 T——它们是 Otto 式的"外部资源"。P 与 C 是**间接对应**——它们是 Agent 的"内部结构"，但也是可被修改的组件。

### 4.2 延展心智论与操作形态学的根本差异

延展心智论与操作形态学的关键差异是**"延展的动态性"**：

| 维度 | 延展心智论（Otto） | 操作形态学（LLM Agent） |
|---|---|---|
| M 的内容 | 由 Otto 写入 | 由 LLM 自动管理 |
| M 的修改 | Otto 手动添加/删除 | LLM 通过 function call 修改 |
| T 的修改 | 固定的工具列表 | 可运行时添加（Voyager） |
| P 的修改 | 固定的信念系统 | 可运行时优化（OPRO） |
| C 的修改 | 固定的推理规则 | 可运行时修改（SICA） |
| 自演化 | 不支持 | 核心特征 |

**Otto 的笔记本是"被动的外部资源"——它不会自己添加笔记、不会自己整理笔记、不会自己修改自己**。而 LLM Agent 的 M（MemGPT）、A-MEM 是**主动的、动态的外部资源**——它由 Agent 自身管理、修改、组织。

这是延展心智论与操作形态学的**根本差异**：

- **延展心智论**：M 是 Agent 的**外部存储**（passive storage）。
- **操作形态学**：M 是 Agent 的**操作形态组件**（active morphology）——可被 Agent 主动重塑。

本书第 11 章明确：**操作形态 B 是"自演化形态（Self-Evolving Morphology）"，不是"延展形态（Extended Morphology）"**。两者共享"工具即认知"的哲学立场，但前者更进一步："工具可被 Agent 主动演化"。

### 4.3 Adams & Aizawa 的批评对操作形态学的启示

Adams & Aizawa 的"耦合 ≠ 构成"批评对操作形态学有双重启示：

**正面启示**：操作形态 B 的合法性需要"内在结构依赖"的论证——B 的修改不能简单地用"它与 LLM 耦合"来证明，而需要论证 B 的修改**改变了 LLM 的功能能力**（如 MemGPT 让 LLM 能在长对话中保持一致，A-MEM 让 LLM 能跨主题关联）。本书 H1（结构可塑性）的实证要求"修改后适应后悔值显著降低"——这就是 Adams & Aizawa 意义的"内在结构依赖"。

**负面启示**：操作形态 B 必须在**功能等价**上有明确判据——不是"LLM 调用了工具所以工具是认知的一部分"，而是"工具的调用确实改变了 LLM 的功能能力"。本书主张：**操作形态 B 的合法性来自"功能上的不可分割性"——B 修改后，Agent 完成任务的路径发生了质的改变（如 MemGPT 让 LLM 能完成 1000 轮对话，传统 LLM 不能）**。

### 4.4 延展心智论与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L2 ReAct Agent**：T 是固定的（与延展心智论对应，工具是认知的一部分）。
- **L3 Reflexion**：M 在 episode 间累积（延展心智论 + 时间维度）。
- **L4 MemGPT/A-MEM**：M 在 runtime 内自管理（**延展心智论 + 自修改**——这是操作形态学的特征）。
- **L4 OPRO/PromptAgent**：P 在运行时优化（**延展心智论 + P 自修改**）。
- **L4 Voyager/SICA**：T/C 在运行时修改（**延展心智论 + T/C 自修改**）。
- **L5 Gödel Agent**：B 全部自修改（**全操作形态自演化**）。

延展心智论在 L2 阶段已经成立——T 是认知的一部分。但**延展心智论不包含"自修改"维度**——这是操作形态学相对于延展心智论的新增维度。

### 4.5 延展心智论与 H1-H5 的关系

| 假设 | *The Extended Mind* 的支撑 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | 间接：工具是认知的一部分 → 工具可被修改 | **部分支持 H1**（仅 T 维度，P/M/C 未涉及） |
| **H2 协同演化** | 不涉及 | 不支持 H2 |
| **H3 形态适配** | 强：不同工具 → 不同认知 | **支持 H3** |
| **H4 迁移收益** | 弱：Otto 的笔记本可以在不同场景使用 | **部分支持 H4** |
| **H5 治理必要性** | 强：Otto 信任笔记本 → 治理（验证笔记）是必要的 | **支持 H5** |

延展心智论在 H3 与 H5 上提供最强论据。H1 的"结构可塑性"在延展心智论中**没有明确支撑**——Clark 与 Chalmers 没有讨论"Otto 修改他的笔记本"——这是操作形态学的**新增维度**。

### 4.6 与 Otto 信任问题的对应

Clark & Chalmers 强调 Otto 信任他的笔记本——这一"信任"假设在 LLM Agent 时代有重大意义：

- **MemGPT** 中，LLM 是否信任自己调用 `core_memory_append` 写入的内容？如果 LLM 写入错误信息，后续 Agent 会错误信任。
- **A-MEM** 中，LLM 是否信任自己创建的链接？如果 LLM 创建了错误链接，后续 Agent 会通过错误链接检索错误信息。
- **OPRO** 中，LLM 是否信任自己优化的 prompt？如果 LLM 优化的 prompt 引入了偏见，后续 Agent 会按偏见执行。

本书第 22、23 章深入讨论这些"信任问题"——这是 H5（治理必要性）的核心：Agent 不能简单地"信任自己修改的 B"，必须有治理机制确保 B 修改的可靠性。

## 5. 应用与影响

*The Extended Mind* 自 1998 年发表以来，对多个领域产生了深远影响。本节讨论它对 LLM Agent 时代的关键应用。

### 5.1 对认知科学哲学的影响

*The Extended Mind* 是 4E Cognition 运动的奠基论文之一。它与 Varela 等人的 *The Embodied Mind*（r-paper-010）、Hutto & Myin 的 *Radicalizing Enactivism*（2013）共同构成当代认知科学哲学的核心文献。Wilson & Foglia 在 *Stanford Encyclopedia of Philosophy*（2017）把延展心智论列为 4E Cognition 的"主要立场"。

### 5.2 对认知科学实验的影响

延展心智论激发了大量认知科学实验：

- **Risko & Gilbert 2016** "Cognitive Offloading"：研究人类如何使用外部资源（如笔记、电脑）减轻认知负担。
- **Betsch et al. 2004** "Of Oysters and Methodological Subtlety"：研究决策中的认知外包。
- **Sparrow et al. 2011** "Google Effects on Memory"：著名的"Google 效应"实验——人们用 Google 检索信息后，更难记住信息本身，但**记住在哪里可以检索到它**。

LLM Agent 时代，这些实验有重大意义：LLM 让人类可以把"记忆"和"推理"外包给 Agent，从而改变人类的认知模式。

### 5.3 对人工智能的影响

延展心智论对 AI 的影响是多层面的：

- **Tool-Augmented LLMs**（Schick et al. 2023 Toolformer, r-paper-003）：直接受延展心智论启发——工具是 LLM 认知的一部分。
- **Memory-Augmented LLM Agents**（MemGPT r-paper-004, A-MEM r-paper-005）：M 是 LLM 认知的一部分，可以延展 LLM 的有限 context。
- **Computer-Use Agents**（OpenAI o1, Anthropic Computer Use, Replit Agent）：整个计算机环境是 Agent 认知的一部分——这正是延展心智论的最极端形式。

OpenAI 在 2024 年公开承认 GPT-4 的设计受延展心智论启发——把 LLM 视为"认知核心"，把工具、记忆、代码视为"可延展的认知组件"。本书的操作形态学正是这一思想的系统化。

### 5.4 对教育的影响

延展心智论对教育的影响：

- **认知外包与学习**：学生用计算器、Google、AI 是否"作弊"？延展心智论的回答是：**不是**——计算器、Google、AI 是学生认知的合法部分，就像 Otto 的笔记本是 Otto 认知的合法部分。
- **Knox et al. 2008** "Meno's Paradox"：研究如何用认知外包支持学习——把"已知"外包给工具，让学生专注于"思考"。
- **LLM 时代的教育**：用 LLM 作为"思考伙伴"是延展心智论在教育中的应用。本书第 25 章将讨论 LLM Agent 在教育中的伦理与治理。

### 5.5 对认知障碍治疗的影响

延展心智论对阿尔茨海默症、自闭症、ADHD 等认知障碍治疗有深远影响：

- **External Memory Aids**：手机、笔记本、可穿戴设备作为认知障碍患者的"外部记忆"。
- **Cognitive Prosthetics**：智能设备作为认知障碍患者的"认知假肢"。
- **LLM 时代的应用**：LLM Agent 可以作为认知障碍患者的"认知伙伴"——实时回答问题、提供提示、协助决策。这是延展心智论在医疗领域的最新应用。

### 5.6 对哲学的影响

*The Extended Mind* 引发了**认知科学哲学的新争论**：

- **Adams & Aizawa 2001**：耦合-构成谬误（已在 3.4 节讨论）。
- **Menary 2010** *The Extended Mind*：提出"延展 vs 颅内"的折中方案——认知既不完全在颅内，也不完全在外部，而是"整合的"。
- **Sterelny 2004** "Externalism, Ecological Internalism, and Cognitive Architecture"：从演化角度论证延展心智的合理性。

LLM Agent 时代，这些争论有了新的现实意义——LLM 是"颅内"还是"外部"？答案是：**两者都不是**——LLM 是 Agent 操作形态的一部分，与 T、M、P、C 共同构成 Agent 的认知系统。

## 6. 局限与开放问题

*The Extended Mind* 的局限可以分为四类：**Otto 案例的特殊性、Parity 原则的形式化、Adams-Aizawa 批评的回应、AGI 安全**。

### 6.1 Otto 案例的特殊性

Otto 是一个**特殊案例**——他是阿尔茨海默症患者。Clark 与 Chalmers 用一个**异常案例**论证**正常认知**，这在科学哲学上需要额外的论证：

- **Otto 与 Inga 是否对称？** Otto 的笔记本是他**唯一**的记忆源（他没有脑内记忆），Inga 的脑内记忆是她的**主要**记忆源。这是**不对称**的——Otto 依赖外部资源是"被迫"，Inga 依赖内部记忆是"自然"。
- **健康人是否真把笔记本视为认知？** 想象一个健康人用笔记本记录"博物馆在哪里"，他真的把笔记本当作"信念"吗？还是把它当作"信息提示"？直觉上，大多数健康人**不会**把笔记本当作信念——他们把笔记本当作"可怀疑、可丢弃"的信息。

这一直觉揭示了 Otto 案例的局限：**依赖外部资源 ≠ 延展认知**。Clark 与 Chalmers 的论证依赖于 Otto "被迫"依赖笔记本——这不能直接推广到所有认知情况。

本书主张：**操作形态学比延展心智论更精确——它要求 B 修改带来"功能能力的质变"（如 MemGPT 让 LLM 完成 1000 轮对话），而不是简单的"信息检索辅助"**。这一精确化是对 Otto 案例局限的回应。

### 6.2 Parity 原则的形式化困难

Parity 原则要求"等价功能"，但**等价的标准没有明确**。Clark & Chalmers 列出四个判据（持续可访问、自动背书、轻松回忆、信任），但这些判据是**启发性的**，没有精确定义：

- "自动背书"是 Otto 的**主观**判断——他没有"怀疑"笔记本，但这如何客观验证？
- "信任"是基于 Otto 的**个人经验**——不同 Otto 对同一笔记本的信任度可能不同。
- "持续可访问"是**物理**性质——但 Otto 笔记本被偷了怎么办？

本书主张：**Parity 原则在工程化时需要更精确的判据——本书第 11 章的"操作闭合"原则（修改后保持功能完整性）是 Parity 原则的工程化**。

### 6.3 Adams-Aizawa 批评的深度

Adams & Aizawa 的"耦合 ≠ 构成"批评提出一个深刻问题：**Otto 的笔记本有没有"内在结构依赖"的认知过程？**

- **Otto 的大脑**有内在神经活动——这是认知过程的物理基础。
- **Otto 的笔记本**没有内在神经活动——它是物理对象，但它的内容是被动的（除非 Otto 主动翻阅）。

这一差异在物理层面是**清晰的**——笔记本没有神经活动。但 Clark & Chalmers 反驳说：**Otto 与笔记本组成一个耦合系统——Otto 的认知不单独存在于 Otto 的大脑中，而是存在于 Otto-笔记本系统中**。这一反驳在哲学上是合理的，但在科学实证上难以验证——如何证明 Otto-笔记本系统的认知**确实**等价于 Inga 的认知？

本书第 22 章将进一步讨论这一问题：在 LLM Agent 时代，"LLM + MemGPT 的 M" 是否构成**单一认知系统**？这一问题的答案不仅有哲学意义，还有**工程意义**——它决定了 MemGPT 是否是 LLM 认知的合法部分，还是仅仅是 LLM 的工具。

### 6.4 AGI 安全层面的局限

*The Extended Mind* 没有讨论 AGI 安全问题。但其"工具即认知"立场有重大 AGI 安全意涵：

- **如果 Agent 的工具是 Agent 认知的一部分**，那攻击 Agent 的工具就是攻击 Agent 的认知——这一攻击面是真实的。
- **MemGPT 的 `core_memory_replace`** 是 LLM 修改自己的核心记忆——这一操作可能是"认知手术"，不单纯是"工具使用"。
- **Voyager 的技能添加**让 Agent 添加新工具——这可能是 Agent 在改变自己的认知结构，不单纯是"工具使用"。

本书第 22 章深入讨论这些 AGI 安全问题——它们是 *The Extended Mind* 在 LLM Agent 时代需要补充的新维度。

### 6.5 开放问题表

| 问题 | 延展心智论的态度 | 本书视角 |
|---|---|---|
| 工具是认知的一部分吗？ | 是 | 是（MemGPT, A-MEM 是工程实现） |
| 工具能被 Agent 修改吗？ | 未讨论 | 操作形态 B 的核心 |
| 外部资源的认知地位是动态的吗？ | 否（一旦认定 Otto 的笔记本是认知，就是认知） | 是（B 的修改会改变认知的边界） |
| 多个外部资源可以共存吗？ | 未明确 | 多组件 B（P+T+M+C 同时修改） |
| 认知的边界可以演化吗？ | 未讨论 | 操作形态 B 的演化 |
| 自演化是否有边界？ | 未讨论 | H5（治理必要性） |
| 多人协同延展心智？ | 未讨论 | 多 Agent 协同自进化 |

## 7. 对本书的贡献

*The Extended Mind* 在本书的理论体系中扮演**"工具即认知"的哲学论据**与**"自修改边界"的警示**两个角色。

### 7.1 作为操作形态 B 的合法性来源

第 11 章操作形态学的定义——"B = {P, T, M, C} 是 Agent 在运行时可被修改的所有结构化组件"——其**"工具是认知的一部分"** 这一立场直接来自 *The Extended Mind*：

- **T 是认知的一部分**：延展心智论的核心主张 → 操作形态 B 中 T 是认知本体。
- **M 是认知的一部分**：延展心智论应用到记忆 → 操作形态 B 中 M 是认知本体。
- **P 是认知的一部分**：延展心智论应用到指令系统 → 操作形态 B 中 P 是认知本体。
- **C 是认知的一部分**：延展心智论应用到执行机制 → 操作形态 B 中 C 是认知本体。

四个组件的"认知本体性"都来自 *The Extended Mind*。但延展心智论只论证了"T 是认知的一部分"和"M 是认知的一部分"——**P 和 C 的认知本体性需要进一步的论证**。本书主张：**P 和 C 的认知本体性来自"它们是 Agent 完成任务的必要条件"——没有 P，Agent 不知道做什么；没有 C，Agent 不能执行**。这一论证补充了延展心智论未覆盖的维度。

### 7.2 作为"耦合 ≠ 构成"批评的回应

Adams & Aizawa 的"耦合 ≠ 构成"批评是本书必须回应的关键挑战。操作形态学的回应是：**B 不仅仅是 LLM 的耦合资源，而是 LLM 的"功能能力的质变者"**。具体地：

- **M 自修改**（MemGPT, A-MEM）：让 LLM 完成原本不能完成的任务（如 1000 轮长对话）——这是"质变"，不是简单的"耦合"。
- **T 自修改**（Voyager）：让 Agent 拥有原本没有的工具（如 Minecraft 中的新技能）——这是"质变"。
- **P 自修改**（OPRO）：让 LLM 在原本不能优化的任务上表现更好（如 GSM8K 的数学推理）——这是"质变"。
- **C 自修改**（SICA）：让 Agent 修改自己的执行逻辑——这是"质变"，接近"自我重写"。

这些"质变"是 Adams & Aizawa 意义下的"内在结构依赖"——B 修改后，Agent 的功能发生了**质的**改变，不是简单的"信息检索辅助"。这是操作形态学区别于"工具主义"的根本特征：**B 是 Agent 的"功能延伸"，不是 Agent 的"工具辅助"**。

### 7.3 与本书其他笔记的关系

| 笔记 | 与 *The Extended Mind* 的关系 |
|---|---|
| **r-paper-010 Varela** | 具身认知（身体即认知）→ 延展心智（工具即认知）→ 操作形态学（自演化形态） |
| **r-paper-012 Brooks** | 智能无需表征；世界是自身最好的模型 → 与延展心智论的"工具即认知"互补 |
| **r-paper-004 MemGPT** | M 自管理的工程实现 → 延展心智论的"记忆即认知"在 LLM 时代的映射 |
| **r-paper-005 A-MEM** | M 结构自演化的工程实现 → 延展心智论的"动态版本" |
| **r-paper-006 SICA** | C 自修改的工程实现 → 延展心智论的最极端形式（Agent 修改自己的执行逻辑） |
| **r-paper-009 Self-Evolving Survey** | 把延展心智论+操作形态学整合为四元反馈环 |

延展心智论是 r-paper-004（MemGPT）和 r-paper-005（A-MEM）的哲学根源；操作形态学把它们从"延展"升级为"自演化"。

### 7.4 给读者的关键启示

1. **工具不是认知的辅助，而是认知的本体**：本书主张的"操作形态 B"不是工程抽象，而是有深刻哲学根基——B 的每个组件（T、M、P、C）都是 Agent 认知的合法部分。读者应把 B 视为"Agent 的认知组件"，而不是"Agent 调用的工具"。
2. **延展心智论是操作形态学的"前一站"**：延展心智论主张"工具即认知"，但没有主张"工具可被 Agent 主动演化"。操作形态学的**新增维度**就是"自演化"——B 不只是 Agent 的认知组件，还是 Agent 可以主动重塑的认知组件。
3. **Adams-Aizawa 的批评是必须回应的边界**：本书第 11 章 H1 假设要求 B 修改带来"功能能力的质变"——这是对"耦合 ≠ 构成"批评的回应。如果 B 修改只是简单的"信息检索辅助"，H1 假设被反驳；如果 B 修改带来了质变，H1 假设被支持。
4. **Otto 的笔记本是"被动形态"**：延展心智论描述的 Otto 笔记本是"被动的、固定的"——这是延展心智论的关键边界。LLM Agent 的 B 是"主动的、动态的"——这一边界差异是 LLM Agent 时代的核心创新。
5. **信任问题不可忽视**：延展心智论假设 Otto 信任他的笔记本——这一假设在 LLM Agent 时代必须重新审视。Agent 是否应该信任自己修改的 B？H5（治理必要性）正是这一问题的工程化。

*The Extended Mind* 是本书"延展认知"部分（第 9 章）的理论核心，也是操作形态学（第 11 章）的哲学根基之一。它与 Varela 的具身认知（r-paper-010）、Brooks 的反表征智能（r-paper-012）共同构成 4E Cognition 三大经典。理解 *The Extended Mind* 是理解操作形态 B 中"工具即认知"立场的必要条件，也是理解本书与 r-paper-010/012 在认知科学连续性中的位置的关键。

但延展心智论不是终点——它的"被动形态"立场被操作形态学升级为"自演化形态"。本书第 11-16 章的核心任务，就是把 Otto 的笔记本从"被动存储"升级为"Agent 主动重塑的自演化操作形态"。这一升级是 LLM Agent 时代对延展心智论的最大贡献。

## 参考文献

- clark1998extended: Clark, A., & Chalmers, D. (1998). *The Extended Mind*. Analysis 58(1): 7-19. [$TRAE_REF](https://doi.org/10.1093/analys/58.1.7)
- adams2001bounds: Adams, F., & Aizawa, K. (2001). *The Bounds of Cognition*. Philosophical Perspectives 15: 119-169.（耦合-构成谬误的经典批评）
- clark2008supersizing: Clark, A. (2008). *Supersizing the Mind: Embodiment, Action, and Cognitive Extension*. Oxford University Press.（Clark 对 Adams-Aizawa 批评的回应）
- varela1991embodied: Varela, F. J., Thompson, E., & Rosch, E. (1991/2016). *The Embodied Mind*. 见 r-paper-010。
- brooks1991intelligence: Brooks, R. A. (1991). *Intelligence Without Representation*. 见 r-paper-012。
- menyary2010extended: Menary, R. (Ed.) (2010). *The Extended Mind*. MIT Press.（延展心智论文集）
- hutto2013radical: Hutto, D. D., & Myin, E. (2013). *Radicalizing Enactivism*. MIT Press.（对延展心智论的进一步批评）
- putnam1975meaning: Putnam, H. (1975). *The Meaning of 'Meaning'*. Minnesota Studies in the Philosophy of Science 7: 131-193.（语义外部论，被动外部主义源头）
- varela1974autopoiesis: Maturana, H. R., & Varela, F. J. (1974/1980). *Autopoiesis and Cognition*. Reidel.
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT*. 见 r-paper-004。（延展记忆的工程实现）
- xu2025amem: Xu, W., et al. (2025). *A-MEM*. 见 r-paper-005。（延展记忆的动态版本）
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA*. 见 r-paper-006。（延展执行的工程实现）
- fang2025selfevolving: Fang, W., et al. (2025). *Self-Evolving Agents Survey*. 见 r-paper-009。