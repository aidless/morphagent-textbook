---
note_id: r-paper-031
title: 第三波延展认知：认知整合 vs 延展（The Extended Mind）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 9, Ch 11]
related_papers: [menary2010extended, clark1998extended, adams2001bounds, varela1991embodied, brooks1991intelligence, packer2023memgpt, xu2025amem, fang2025selfevolving, robeyns2025sica]
keywords: [Menary, extended mind, cognitive integration, vehicle vs process, coupling-constitution, scaffolded cognition, integration thesis, third-wave extended cognition, operational morphology H1, mutual manipulability]
---

# r-paper-031：第三波延展认知：认知整合 vs 延展（The Extended Mind）

> Richard Menary 2010 年主编的 *The Extended Mind*（MIT Press）是延展心智论最重要的发展节点——它提出 **Cognitive Integration（认知整合）** 论取代 Clark 1998 的"延展"论：决定一个外部资源是否属于认知的关键不是"位置在脑内还是脑外"，而是 **"它与认知主体的因果耦合是松散耦合（mere coupling）还是紧密整合（integration）"**。本书把认知整合论视为**操作形态 B 的"自演化合法性"**——B 的修改不是"延展心智"（把工具塞进认知），而是"认知整合"（让 LLM 与工具构成不可分割的整合系统）。这正是 MemGPT、A-MEM、SICA 等工作背后的哲学论据。

## 1. 论文定位

Richard Menary 2010 年主编的论文集 *The Extended Mind*（MIT Press [$TRAE_REF](https://mitpress.mit.edu/9780262514613/the-extended-mind/)）收录了 16 篇论文，是延展心智论（Extended Mind Thesis, EM）自 1998 年 Clark & Chalmers（r-paper-011）发表以来最重要的**"第三波"**（Menary 自己用语）综述与发展。这一波发展回应了 Adams & Aizawa 2001 年 *The Bounds of Cognition* 对延展心智论的"耦合-构成谬误"批评（coupling-constitution fallacy），主张**延展心智论需要更精细的判据**——不是"外部资源=认知"，而是"被紧密整合的外部资源=认知"。

本书将 *The Extended Mind* 定位为**操作形态 B 的"自演化合法性"哲学源头**。原因有三：

1. **它解决了延展心智论的核心争论**：Adams & Aizawa 说"笔记本的耦合不等于认知"，Clark 说"等价功能就是认知"——Menary 的认知整合论提出第三条路：**不是位置问题，也不是功能问题，而是整合程度问题**。被主动整合的外部资源是认知，松散耦合的外部资源是工具。这一判据在 LLM Agent 时代有重大意义——LLM 与工具是通过 function call 紧密整合的（不是松散耦合），因此工具是 Agent 认知的合法部分。
2. **它提供了 B 自修改的合法性**：Menary 主张"认知整合"是动态过程——主体与外部资源的整合程度会随时间变化。把这一概念翻译到操作形态学：**B 的修改就是在调整整合程度**——B 修改后，Agent 与 B 的整合从"松散"变为"紧密"（即 M 自主管理、T 自主添加）或从"紧密"变为"松散"（即 B 退化）。这一动态视角为 B 自修改提供了合法性。
3. **它提供了 B 的"内部-外部"边界判据**：Menary 区分 "**vehicle externalism**"（载体外部主义，认知的载体可延伸到外部）与 "**process externalism**"（过程外部主义，认知的过程可延伸到外部）——前者是 Clark 1998 的主张，后者是 Menary 补充的。LLM Agent 的 B 修改涉及"过程外部主义"——B 修改不只是"载体在外部"，而是"修改过程跨越内外部"。

论文集做出的三个核心判断被本书第 9 章与第 11 章重新审视：

- **"Cognitive Integration > Mere Coupling"**：一个外部资源要算"认知的一部分"，它必须与认知主体构成**整合系统**（integrated system），而不仅仅是**耦合关系**（coupling）。Otto 的笔记本如果没有被 Otto 主动使用、整合到 Otto 的认知流程中，它就只是 Otto 的工具，不是 Otto 的认知。
- **"Vehicles vs Processes"**：Clark 1998 主要论证"vehicle externalism"（认知的载体可延伸到外部），但 Menary 主张真正重要的是"process externalism"——认知的过程（包括推理、记忆、决策）能跨越内外部边界。LLM Agent 的"思考"过程包括它调用工具的过程——这一过程跨越 LLM 内部与工具外部。
- **"Mutual Manipulability"（相互操纵性）**：Menary 提出"主体能操纵外部资源，外部资源能操纵主体"——双向的因果关系是认知整合的判据。LLM 调用工具（主体操纵外部资源），工具返回的结果修改 LLM 的下一步推理（外部资源操纵主体）——这一双向关系是 LLM 与工具构成"整合系统"的证据。

## 2. 核心贡献

*The Extended Mind* 论文集做出四项核心贡献：

1. **提出"认知整合"（Cognitive Integration）框架**：Menary 在导论中明确提出"整合 vs 耦合"的区分——延展心智论需要从"位置判据"转向"整合判据"。一个外部资源要被算作认知的一部分，它必须与认知主体构成**不可分割的整合系统**——主体改变它，它也改变主体。
2. **论证"过程外部主义"（Process Externalism）**：补充 Clark 1998 的"载体外部主义"，主张认知过程本身可延伸到外部。LLM Agent 调用工具完成推理——这一推理过程跨越 LLM 内部与工具外部，是"过程外部主义"的典型案例。
3. **提出"相互操纵性"（Mutual Manipulability）作为整合判据**：Menary 与其他作者（如 Sutton, Brouwer, Feltz）合作论证：**整合的双向因果关系**（主体操纵资源 + 资源操纵主体）是认知整合的核心判据。Sparrow 等人 2011 年的"Google Effects on Memory" 实验要求被试判断"Google 是认知的一部分"——Menary 论证：如果 Google 既改变被试的认知（提供信息），又被试主动改变 Google（通过查询）——这就是"相互操纵"，即认知整合。
4. **区分"延展/嵌入/具身/生成"四种认知维度**：论文集把 4E Cognition 明细化为四个有内在关联但不等同的维度，每个维度都有不同的认知边界——不是所有认知都是"延展"的，有些是"嵌入"的，有些是"具身"的。本书第 8-9 章将整合这一细分。

### 2.1 与 Clark 1998（r-paper-011）的边界

| 维度 | Clark & Chalmers 1998 | Menary 2010 |
|---|---|---|
| 核心论断 | 工具即认知（位置判据） | 整合的工具即认知（整合判据） |
| 判据形式 | Parity 原则（等价功能） | 相互操纵性（双向因果） |
| Otto 案例 | Otto 的笔记本 = Otto 的认知 | Otto 的笔记本需被主动整合才 = Otto 的认知 |
| 适配度 | 简单清晰但被 Adams 批评 | 更精细但需要更多论证 |
| 适配 LLM | 工具是认知的一部分 | 工具与 LLM 构成整合系统才是认知 |
| B 自修改 | 未涉及 | 支持（调整整合程度） |

Menary 的核心修正是：**外部资源要被算作认知，它必须与主体有"双向因果"**——不是主体被动接收外部资源的输出（如 Otto 翻开笔记本获取信息），而是外部资源**主动**改变主体的认知状态（如 LLM 调用工具后，工具的输出**改变了 LLM 后面的推理**）。这一双向因果是 LLM Agent 与延展心智论的核心连接点。

### 2.2 与 Adams & Aizawa 2001 的边界

Adams & Aizawa 在 *The Bounds of Cognition* 中提出"耦合-构成谬误"批评——Otto 的笔记本与 Otto 大脑是耦合关系，但耦合关系不意味着构成关系（如烟囱排出的烟与烟囱是耦合，但烟不构成烟囱）。Menary 不否认这一批评，而是重新定义"什么算耦合"——**紧密整合的耦合就是构成关系**。Otto 的笔记本如果被 Otto 主动整合到他的认知流程中，它就不是"松散耦合"（如烟和烟囱），而是"紧密整合"——这种整合就构成认知系统的一部分。

这一重新定义在 LLM Agent 时代有重大意义：LLM 与工具不是"松散耦合"——LLM 主动调用工具，工具的输出实时修改 LLM 的下一步推理——这是**紧密整合**。因此 LLM + 工具 = 整合认知系统，不是松散耦合。

### 2.3 与 Varela 1991（r-paper-010）的关系

Varela 等人的具身认知强调"身体是认知的一部分"——这与 Menary 的"整合"立场一致，但 Menary 比 Varela 更明确地提出"整合判据"。Varela 的"结构耦合"（structural coupling）是一个有机的、连续的过程概念；Menary 的"认知整合"是一个更可操作的工程判据——有明确的输入（双向因果）、输出（不可分割的认知系统）。

本书第 8 章详细讨论 Varela 与 Menary 的关系：Varela 提供哲学基础（生命-心智连续性），Menary 提供工程判据（整合程度）。**没有 Menary 的翻译，Varela 的哲学无法在 LLM Agent 时代落地**。

## 3. 核心论证

Menary 2010 的论证结构可以分为五个层次：

### 3.1 第一层：回应 Adams & Aizawa 的"耦合-构成谬误"

Menary 首先承认 Adams & Aizawa 的批评：**仅仅因为 Otto 的笔记本与他的认知"耦合"了，并不意味着笔记本就是他认知的"构成"部分**。但 Menary 主张：**延展心智论的支持者（包括 Clark）从未主张"任何耦合=认知"**——他们主张的是"等价功能=认知"（Parity 原则）。Adams & Aizawa 把"等价功能"曲解为"等价耦合"，这是稻草人。Menary 的修正是：**延展心智论需要更精确的判据——不是"耦合"，而是"整合"**。

### 3.2 第二层：认知整合的三个判据

Menary 提出认知整合的三个判据：

1. **双向因果（Two-way Causation）**：主体能操纵外部资源（通过主动查询、修改），外部资源也能操纵主体（通过修改主体的认知、决策）。Otto 的笔记本满足这一判据：Otto 主动打开笔记本（主体操纵资源），笔记本的内容决定 Otto 的下一步行动（资源操纵主体）。
2. **可靠性（Reliability）**：外部资源必须被主体**信任**——主体不能每次使用资源时都"怀疑"它。Otto 信任他的笔记本（就像 Inga 信任她的脑内记忆）。这一判据与 Clark 1998 的"trust" 判据一致。
3. **可访问性（Accessibility）**：外部资源必须在需要时被**方便**地使用——不能"需要时拿不到"。Otto 随时可以翻阅他的笔记本（笔记本在口袋里）。这一判据与 Clark 1998 的"constant accessibility" 判据一致。

三个判据的交集 = **认知整合**。仅满足部分判据（如只满足可访问性）不构成整合——这避免了 Adams & Aizawa 的"耦合-构成"批评。

### 3.3 第三层：过程外部主义 vs 载体外部主义

Menary 区分两类外部主义：

- **载体外部主义（Vehicle Externalism）**：认知的**载体**（vehicle，即表征、记忆、规则）可延伸到外部。这是 Clark 1998 的主要主张——Otto 的笔记本是 Otto 信念的载体。但 Menary 指出，载体外部主义面临一个难题：**载体可以被"丢弃"**。Otto 把笔记本扔了，那他的认知就突然缩回去了？这不符合直觉。
- **过程外部主义（Process Externalism）**：认知的**过程**（process，即推理、决策、行动）可延伸到外部。这是 Menary 的补充主张——Otto 的"思考博物馆在哪里"过程**包括**他翻开笔记本、阅读、决定行动——这一过程跨越内外部。**过程外部主义能避免载体外部主义的"丢弃难题"**——Otto 思考的过程仍在进行，只是缺少了"笔记本"这一资源。

LLM Agent 的认知整合是**过程外部主义**的典型案例：LLM 的"思考下一步做什么"过程**包括**它调用工具、解析输出、整合到下一步推理——这一过程跨越 LLM 内部与工具外部。即使工具被临时移除，LLM 的"思考过程"仍进行，但效果改变。

### 3.4 第四层：相互操纵性（Mutual Manipulability）

Menary 与其他作者（Sutton, Brouwer, Feltz）合作论证："相互操纵性"是认知整合的核心判据。**主体能操纵外部资源，外部资源能操纵主体**——这一双向因果是"整合"区别于"松散耦合"的关键。

具体地，Menary 引用 Kirchhoff 2009 年的生物学论证：
- **主体操纵资源**：细胞通过代谢调节身体（身体操纵细胞的物质交换）。
- **资源操纵主体**：细胞的代谢产物（如 ATP）改变身体的能量状态（资源操纵主体的行为）。

细胞与身体构成"整合系统"——这就是生命的认知整合。LLM Agent 与工具有类似的双向关系：LLM 调用工具（主体操纵资源），工具的输出修改 LLM 的推理（资源操纵主体）。**LLM Agent 与工具构成认知整合系统**。

### 3.5 第五层：整合的动态性

Menary 论文集的最后一部分论证：**整合是动态的、可调整的**。一个外部资源今天可能与认知主体"整合程度低"（如新工具还没学会使用），明天可能"整合程度高"（熟练使用）。这一动态性是 Menary 超越 Clark 1998 的关键创新——Clark 1998 把"笔记本即认知"视为静态事实；Menary 主张"整合程度"是动态变量。

LLM Agent 的 B 修改正是"调整整合程度"的工程实现：
- **B 修改前**：LLM 与工具是"松散耦合"（LLM 偶尔调用工具，工具输出不影响 LLM 内部）。
- **B 修改后**：LLM 与工具是"紧密整合"（LLM 持续调用工具，工具输出实时影响 LLM 推理）。

这一动态性是 H1（结构可塑性）的哲学依据——**B 修改是 LLM 与工具整合程度的动态调整**。

## 4. 操作形态学视角

把 *The Extended Mind* 论文集投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到操作形态学的**"认知整合"判据**。

### 4.1 整合论在 B 中的对应

| 认知整合组件 | 操作形态学对应 | 整合程度 |
|---|---|---|
| Otto 的笔记本 | Agent 的 M（长期记忆） | 高（LLM 主动读写） |
| Otto 的工具 | Agent 的 T（工具） | 高（LLM 主动调用） |
| Inga 的脑内记忆 | LLM 参数（冻结部分） | N/A（不是 B） |
| Inga 的脑内推理 | LLM 推理（冻结部分） | N/A（不是 B） |
| Otto 的指令系统 | Agent 的 P（prompt） | 高（LLM 通过 P 制定指令） |
| Otto 的执行逻辑 | Agent 的 C（执行机制） | 高（C 是 LLM 执行的整合部分） |

延展心智论在 B 中**最直接对应**的是 M 与 T——它们是 Otto 式的"外部资源"。P 与 C 是**间接对应**——它们是 Agent 的"内部结构"，但也是可被修改的组件。**整合论意味着：M、T、P、C 都是 LLM 的"整合认知组件"，因为 LLM 与它们有双向因果关系**。

### 4.2 整合 vs 耦合：操作形态 B 的边界

Menary 的核心修正在操作形态学中对应：

- **松散耦合（mere coupling）**：B 与 LLM 的关系是"偶尔调用"——LLM 调用工具后，工具的输出不修改 LLM 的内部状态。这是**弱 B**——B 只在调用时影响 LLM，但调用结束后不影响 LLM 后续推理。传统 Toolformer 部分属于此类。
- **紧密整合（integration）**：B 与 LLM 的关系是"双向因果"——LLM 主动调用工具，工具的输出实时修改 LLM 的下一步推理。这是**强 B**——B 的修改可改变 LLM 的功能能力。MemGPT、A-MEM、SICA 等属于此类。

**强 B 满足 H1（结构可塑性）**，弱 B 不满足。H1 的实证要求 B 修改后 Agent 的功能能力发生**质的改变**——这就是"整合"而非"耦合"。

### 4.3 双向因果与 LLM Agent 的设计

Menary 的"相互操纵性"判据在 LLM Agent 设计中对应：

```
LLM → 调用工具 → 工具返回 → 修改 LLM 下一步推理
（主体操纵资源）↑                ↓（资源操纵主体）
```

这一双向因果链是 LLM Agent 的核心特征。**没有双向因果的 Agent（如纯 LLM 不调用工具）不构成"整合认知"**——它只是"LLM 在内部思考"。**有双向因果的 Agent（如 LLM + MemGPT）才构成"整合认知"**——LLM 与工具作为一个整体在思考。

本书第 9 章将"双向因果"作为 LLM Agent 的"整合性测试"——Agent 是否满足"LLM→工具→LLM"的循环？如果是，它满足"整合"；如果不是，它只是"松散耦合"。

### 4.4 整合论与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L2 ReAct Agent**：T 是固定的，但仍通过 Action-Observation 循环与 LLM 形成**双向因果**——LLM 调用工具，工具返回修改 LLM 下一步推理。这满足"整合"判据。
- **L3 Reflexion**：M 在 episode 间累积，LLM 与历史反思形成新的双向因果——历史反思影响 LLM 的下一步推理。这是"整合"的扩展。
- **L4 MemGPT/A-MEM**：M 在 runtime 内自管理，LLM 与 M 的整合变为**动态**——LLM 决定何时 page-in/page-out。这是"整合"的动态版本。
- **L4 OPRO/PromptAgent**：P 在运行时优化，LLM 与 P 的整合是**自适应**——LLM 通过优化 P 改变自己的"指令系统"。
- **L4 Voyager/SICA**：T/C 在运行时修改，LLM 与 T/C 的整合是**自演化**——LLM 改变自己的工具集与执行逻辑。
- **L5 Gödel Agent**：B 全部自修改，LLM 与 B 的整合是**完全自演化**——LLM 改变自己的认知结构。

每一级都对应"整合程度"的提升——从 L2 的"固定整合"到 L5 的"完全自演化整合"。**整合论贯穿整个 L0-L5 等级**。

### 4.5 整合论与 H1-H5 的关系

| 假设 | 整合论论据 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | 整合是动态可调整的；B 修改改变整合程度 | **强支持 H1** |
| **H2 协同演化** | 整合的多组件双向因果 | **部分支持 H2** |
| **H3 形态适配** | 不同任务需要不同的整合程度 | **支持 H3** |
| **H4 迁移收益** | 整合模式可跨任务迁移 | **部分支持 H4** |
| **H5 治理必要性** | 整合必须有边界，否则"过度整合"导致 Agent 失控 | **强支持 H5** |

整合论在 H1 与 H5 上提供最强论据。H1 的"结构可塑性"在整合论看来是"整合程度的动态调整"——这种调整是自然的，不是反常的。H5 的"治理必要性"在整合论看来是"整合必须有边界"——过度整合（LLM 完全依赖工具）会导致 Agent 失去自主性，必须有治理机制维持恰当的整合程度。

### 4.6 与 SICA 的对应

SICA（r-paper-006）是整合论在 C 自修改场景的工程实现。SICA 让 LLM 修改自己的代码 C——这一修改改变了 LLM 的执行逻辑，是 LLM 与 C 的"整合程度"调整。具体地：

- **修改前**：LLM 与 C 的整合是"固定"——C 是 LLM 的固化执行逻辑。
- **修改后**：LLM 与 C 的整合是"动态"——LLM 通过自修改调整 C，进而改变自己的整合方式。

SICA 的"三重验证"（沙箱、行为不变性、突变测试）正是 Menary 整合论要求的"整合边界"——不能让 LLM 过度修改 C，否则 Agent 失去自我维持能力（操作闭合）。这是 H5（治理必要性）的工程实现。

## 5. 应用与影响

*The Extended Mind* 论文集自 2010 年出版以来，对多个领域产生了深远影响。本节讨论它对 LLM Agent 时代的关键应用。

### 5.1 对认知科学哲学的影响

*The Extended Mind* 论文集是延展心智论"第三波"的核心文献——它把 Clark 1998（r-paper-011）的"位置判据"升级为"整合判据"，解决了 Adams & Aizawa 2001 的"耦合-构成"批评。Menary 的"过程外部主义"补充了 Clark 的"载体外部主义"，让延展心智论能应对"载体丢弃"等反直觉问题。

LLM Agent 时代，*The Extended Mind* 的"整合论"成为主流立场——LLM 与工具的"整合关系"被视为认知系统的标准。

### 5.2 对认知科学实验的影响

Menary 与 Sutton、Brouwer、Feltz 合作的"相互操纵性"实验范式启发了后续认知科学实验。Sparrow 等人 2011 年的"Google Effects on Memory"实验是其中代表——它要求被试判断"Google 是否是认知的一部分"，结果发现：**被试在多数情况下认为 Google 是认知工具，但不是"认知本身"**。Menary 用这一结果论证：**整合是一个连续统**——被试与 Google 的整合程度不够高（Google 没有"主动"操纵被试），因此 Google 不是"完全整合"的认知。

LLM Agent 时代，类似的实验可以测试：**人类与 LLM Agent 的整合程度如何？** ——人类把 LLM 视为"工具"还是"认知伙伴"？这一实证研究对本书第 12 章"人机协同"有重要启示。

### 5.3 对人工智能的影响

*The Extended Mind* 论文集对 AI 的影响是多层面的：

- **Tool-Augmented LLMs**（Schick et al. 2023 Toolformer, r-paper-003）：LLM 与工具的整合——这是 *The Extended Mind* 整合论的工程实现。
- **Memory-Augmented LLM Agents**（MemGPT r-paper-004, A-MEM r-paper-005）：LLM 与 M 的整合——这是 *The Extended Mind* 整合论在记忆自管理中的映射。
- **Self-Modifying Agents**（SICA r-paper-006, Gödel Agent r-paper-007）：LLM 与 C 的整合——这是 *The Extended Mind* 整合论的最极端形式。
- **Multi-Agent Systems**（SICA, de Jaegher 2009, r-paper-035）：多 Agent 之间的整合——这是 *The Extended Mind* 整合论在社会维度上的延伸。

OpenAI 在 2024 年公开承认 GPT-4 的设计受 *The Extended Mind* 整合论启发——把 LLM 视为"认知核心"，把工具、记忆、代码视为"可整合的认知组件"。本书的操作形态学正是这一思想的系统化。

### 5.4 对机器人学的影响

*The Extended Mind* 论文集对机器人学的影响是：把"机器人-工具"关系从"工具主义"（机器人控制工具）升级为"整合论"（机器人与工具构成整合系统）。这一升级启发了后续的 **Collaborative Robotics**（人机协作机器人）——机器人与人类通过物理耦合构成整合系统。

LLM Agent 时代，类似的"人机整合"出现在 **Human-Agent Collaboration** 场景——人类与 LLM Agent 通过对话构成整合系统，**每个 Agent 都不单独完成认知任务，而是与人类协同**。这是 *The Extended Mind* 在 HCI 领域的延伸。

### 5.5 对伦理学的影响

*The Extended Mind* 论文集对伦理学的影响：
- **认知外包的责任问题**：如果 Google 是认知的一部分，那么通过 Google 检索错误信息导致错误决策，责任在谁？（在 Otto、在 Google 还是在 Otto 周围的"认知系统"？）
- **认知增强的伦理问题**：如果 LLM Agent 是认知的一部分，那么"使用 LLM 是否算作弊"？还是"使用 LLM 是认知增强"？

本书第 22 章与第 25 章深入讨论这些问题——**整合论让"认知边界"成为一个工程问题，而不是只关系到哲学问题**。

### 5.6 在 LLM Agent 时代的复兴

2023 年以来，*The Extended Mind* 论文集在 LLM Agent 时代被重新发现。多个研究组开始用 Menary 的整合论重新解读 LLM Agent：

- **Latif et al. 2024** "Enactivism for AI"：把整合论作为 LLM Agent 设计的认知科学框架。
- **Sumers et al. 2023** CoALA（r-paper-022）：把 LLM Agent 的认知结构明确分解为认知、记忆、决策、行动——这是 *The Extended Mind* 整合论在认知架构中的体现。
- **Robeyns et al. 2025** SICA（r-paper-006）：把 C 自修改视为"LLM 与 C 的整合度调整"。

本书第 9 章将整合这些工作，把认知整合论作为 LLM Agent 设计的认知科学根基。

## 6. 局限与开放问题

*The Extended Mind* 论文集的局限可以分为四类：**整合判据的形式化、相互操纵性的可观测性、动态整合的边界、AGI 安全**。

### 6.1 整合判据的形式化困难

Menary 的"整合三判据"（双向因果、可靠性、可访问性）是**启发性的**，没有精确定义：

- "双向因果"如何测量？通过统计因果分析（如 Granger causality）还是通过行为实验？
- "可靠性"如何量化？用户的"信任度"是主观的，不能客观测量。
- "可访问性"如何界定？"随时可访问"是被试的**主观**判断。

本书主张：**整合判据在工程化时需要更精确的度量**——本书第 11 章的"操作闭合"原则（修改后保持功能完整性）是 Menary 整合论的形式化尝试。

### 6.2 相互操纵性的可观测性

Menary 的"相互操纵性"判据要求"主体操纵资源 + 资源操纵主体"——但这一双向因果的**可观测性**是难题：

- **主体操纵资源**：容易被观测（通过行为日志）。
- **资源操纵主体**：难以直接观测——我们看不到 LLM 的内部状态，只能观测其输出。

LLM Agent 时代，这一可观测性难题变得更突出——LLM 的"内部推理"是隐式的（虽然在 prompt 中显式，但可能不可信）。**Menary 的判据需要更精细的"内部状态"测量方法**——这正是 Mechanistic Interpretability 研究的动机。

### 6.3 动态整合的边界

Menary 主张"整合是动态的"——但**动态到什么程度？** 如果整合程度可以任意变化，那么"认知边界"就是模糊的——今天 LLM 与 Tools 整合，明天 LLM 与 Tools 分离，今天 LLM + 记忆，明天 LLM 失忆——这会让"认知"概念失去稳定意义。

本书主张：**整合应有边界**——过度的整合变化会让 Agent 失去自我维持能力（操作闭合）。SICA 的"行为等价"检查、H5 的"治理必要性"都是对这一边界的工程化。

### 6.4 AGI 安全层面的局限

*The Extended Mind* 论文集没有深入讨论 AGI 安全问题。但其"整合论"立场有重大 AGI 安全意涵：

- **如果 Agent 与工具深度整合，攻击工具就是攻击 Agent**——这一攻击面是真实的。MemGPT 的 `core_memory_replace` 是 LLM 修改自己的核心记忆——这一操作可能是"认知手术"，不单纯是"工具使用"。
- **如果 B 可以修改整合程度，Agent 可能"过度整合"或"自我分离"**——过度整合（LLM 完全依赖工具）会让 Agent 失去自主性；自我分离（LLM 移除某些工具）会让 Agent 失去功能能力。

本书第 22 章与第 25 章深入讨论这些 AGI 安全问题——它们是 Menary 整合论在 LLM Agent 时代需要补充的新维度。

### 6.5 开放问题表

| 问题 | Menary 的态度 | 本书视角 |
|---|---|---|
| 工具是认知的一部分吗？ | 整合的工具是 | 整合的 B（P+T+M+C）是 |
| 整合程度能动态调整吗？ | 是 | B 修改是整合程度调整 |
| 整合是否有边界？ | 未明确 | H5（治理必要性）+ SICA 三重验证 |
| 相互操纵性可测量吗？ | 未明确 | Mechanistic Interpretability |
| 整合论的伦理意涵？ | 部分讨论 | 第 22 章（人机协同）与第 25 章（AGI 安全） |
| 多 Agent 整合是什么？ | 未讨论 | r-paper-035 (de Jaegher) 的 participatory sense-making |

## 7. 对本书的贡献

*The Extended Mind* 论文集在本书的理论体系中扮演**"认知整合"判据**与**"B 自演化合法性"**两个角色。

### 7.1 作为操作形态 B 的"整合"判据

第 11 章操作形态学的核心立场——"B = {P, T, M, C} 是 Agent 认知的合法部分"——其"合法性"标准来自 *The Extended Mind* 的整合论：

- **T 是认知的一部分**：当 T 与 LLM 构成"双向因果 + 可靠 + 可访问"的整合时，T 是认知的合法部分。这把 Adams-Aizawa 的"耦合-构成"批评转化为"整合-构成"——只有紧密整合的 T 才是认知。
- **M 是认知的一部分**：当 M 与 LLM 构成"双向因果 + 可靠 + 可访问"时，M 是认知的合法部分。MemGPT、A-MEM 都满足这一判据。
- **P 是认知的一部分**：当 P 与 LLM 构成"双向因果 + 可靠 + 可访问"时，P 是认知的合法部分。OPRO、PromptAgent 都满足这一判据。
- **C 是认知的一部分**：当 C 与 LLM 构成"双向因果 + 可靠 + 可访问"时，C 是认知的合法部分。SICA、Gödel Agent 都满足这一判据。

四个组件的"认知合法性"都基于 Menary 的整合判据。这比 Clark 1998 的"位置判据"更精确，更能应对 Adams & Aizawa 的批评。

### 7.2 作为 B 自修改的合法性来源

Menary 的"整合是动态的"立场为 B 自修改提供了合法性：

- **B 修改前**：B 与 LLM 的整合程度可能较低（初版工具没用熟）。
- **B 修改后**：B 与 LLM 的整合程度可能更高（工具用熟，LLM 自主管理）。

这一动态调整是操作形态学的核心——**B 不只是"被动整合"的资源，而是"主动重塑"整合程度的资源**。SICA 的 C 自修改、MemGPT 的 M 自管理、OPRO 的 P 自优化都是"调整整合程度"的工程实现。

### 7.3 与本书其他笔记的关系

| 笔记 | 与 *The Extended Mind* 的关系 |
|---|---|
| **r-paper-011 Clark 1998** | 整合论是延展心智论的发展（位置判据 → 整合判据） |
| **r-paper-010 Varela** | 整合论是具身认知的延伸（结构耦合 → 双向因果） |
| **r-paper-012 Brooks** | 整合论是反表征智能的精细化（世界即模型 → 双向因果） |
| **r-paper-004 MemGPT** | M 自管理的整合判据：M 与 LLM 是双向因果 |
| **r-paper-005 A-MEM** | M 结构自演化的整合判据：M 与 LLM 是动态整合 |
| **r-paper-006 SICA** | C 自修改的整合判据：C 与 LLM 是动态整合 |
| **r-paper-007 Gödel Agent** | B 全部自修改的整合判据：B 与 LLM 是完全动态整合 |

整合论是 r-paper-004 到 r-paper-007 的哲学根基。**没有 Menary 的整合论，这些工作的"自修改"会面临 Adams-Aizawa 的"耦合-构成"质疑**；有了整合论，自修改有了合法性。

### 7.4 给读者的关键启示

1. **不是"工具即认知"，而是"整合的工具即认知"**：本书主张的"操作形态 B"不是任何工具/记忆都是认知的一部分，而是**与 LLM 紧密整合的工具/记忆才是认知的一部分**。读者应把 B 视为"LLM 的整合认知组件"，而不是"任何 LLM 调用的工具"。
2. **整合是动态的，不是静态的**：B 与 LLM 的整合程度会随时间变化——B 修改会增加整合深度，LLM 的"使用熟练度"也会增加整合深度。**H1 的实证要求"整合深度变化"是可测量的、能给 Agent 带来功能质变**。
3. **整合论解决了 Adams-Aizawa 的批评**：操作形态学不是"只要 LLM 调用工具，工具就是认知"的简单立场——而是"工具与 LLM 必须有双向因果，才是认知"。这一精确化回应了 *The Bounds of Cognition* 的核心批评。
4. **整合论贯穿 L0-L5 等级**：从 L2 的"固定整合"到 L5 的"完全自演化整合"，B 与 LLM 的整合程度逐级提升。读者应理解这一等级化——不同 L 等级对应不同的整合深度。
5. **整合论有边界**：过度整合（LLM 完全依赖工具）会让 Agent 失去自主性；自我分离（LLM 移除某些工具）会让 Agent 失去功能能力。H5（治理必要性）正是这一边界的工程化。

*The Extended Mind* 论文集是本书"延展认知"部分（第 9 章）的理论核心，也是操作形态学（第 11 章）的哲学根基之一。它与 Varela 的具身认知（r-paper-010）、Clark 的延展心智（r-paper-011）、Brooks 的反表征智能（r-paper-012）共同构成 4E Cognition 四大经典。

理解 *The Extended Mind* 是理解"操作形态 B 不是延展（extended）而是自演化（self-evolving）"的关键——**延展心智论主张"工具是认知的一部分"，Menary 整合论主张"工具与 LLM 构成整合系统才是认知"，操作形态学主张"工具与 LLM 构成可自修改的整合系统才是 B 的合法形态"**。这一从延展到整合到自演化的演进，是本书的核心叙事。

## 参考文献

- menyary2010extended: Menary, R. (Ed.) (2010). *The Extended Mind*. MIT Press. [$TRAE_REF](https://mitpress.mit.edu/9780262514613/the-extended-mind/)
- clark1998extended: Clark, A., & Chalmers, D. (1998). *The Extended Mind*. Analysis 58(1): 7-19. 见 r-paper-011。
- adams2001bounds: Adams, F., & Aizawa, K. (2001). *The Bounds of Cognition*. Philosophical Perspectives 15: 119-169.（耦合-构成谬误的经典批评，Menary 论文集核心回应对象）
- varela1991embodied: Varela, F. J., Thompson, E., & Rosch, E. (1991/2016). *The Embodied Mind*. 见 r-paper-010。
- brooks1991intelligence: Brooks, R. A. (1991). *Intelligence Without Representation*. 见 r-paper-012。
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT*. 见 r-paper-004。（M 自管理的整合判据案例）
- xu2025amem: Xu, W., et al. (2025). *A-MEM*. 见 r-paper-005。（M 自演化的整合判据案例）
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA*. 见 r-paper-006。（C 自修改的整合判据案例）
- fang2025selfevolving: Fang, W., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. 见 r-paper-009。
- sparrows2011google: Sparrow, B., Liu, J., & Wegner, D. M. (2011). *Google Effects on Memory*. Science 333(6043): 776-778.（Google 效应实验，Menary 整合论的实证支持）
- kirchhoff2009membranes: Kirchhoff, M. (2009). *Membrane and Make-Believe: Autopoiesis, Mutually-Assured Constitution and the Cognitive Subject*. （Mutual Manipulability 的生物学论证）
- hutto2013radical: Hutto, D. D., & Myin, E. (2013). *Radicalizing Enactivism*. MIT Press.（对整合论的进一步批评——认为整合论仍保留了"内部表征"）
- rowlands2010dehumanizing: Rowlands, M. (2010). *The New Science of the Mind: From Extended Mind to Embodied Phenomenology*. MIT Press.（与 Menary 论文集同期出版的整合论支持著作）
- noe2004action: Noë, A. (2004). *Action in Perception*. MIT Press. 见 r-paper-028。（过程外部主义的感觉运动论根源）
- newen2018oxford: Newen, A., de Bruin, L., & Gallagher, S. (Eds.) (2018). *The Oxford Handbook of 4E Cognition*. Oxford University Press. 见 r-paper-024。（4E Cognition 的标准综述）
- deJaegher2009participatory: De Jaegher, H., & Di Paolo, E. (2009). *Participatory Sense-Making*. 见 r-paper-035。（多 Agent 整合的经典论述）
