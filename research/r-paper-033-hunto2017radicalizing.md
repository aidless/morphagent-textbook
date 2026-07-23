---
note_id: r-paper-033
title: 激进生成认知论：基本认知无内容（Radicalizing Enactivism: Basic Minds without Content）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 8, Ch 11]
related_papers: [huto2017radicalizing, varela1991embodied, froese2011enactive, gallagher2017enactive, noe2004action, clark1998extended, newen2018oxford, maturana1980autopoiesis, yao2023react, packer2023memgpt]
keywords: [Hutto, Myin, radical enactivism, basic cognition, no content, contentless, deep enactivism, sense-making, social cognition, contentless action, LLM agent, operational morphology]
---

# r-paper-033：激进生成认知论：基本认知无内容（Radicalizing Enactivism: Basic Minds without Content）

> Daniel Hutto 与 Erik Myin 在 2017 年 MIT Press 出版的 *Radicalizing Enactivism: Basic Minds without Content* 是 enactivism 阵营中最激进、最具颠覆性的著作——它主张 **"基本认知（basic cognition）没有内容（has no content）"**：认知不涉及表征（representation），认知主体的核心机制是"具身行动（embodied action）"和"意义生成（sense-making）"，而不是"对世界的表征"。本书把"基本认知无内容"视为**操作形态 B 的"无表征行动"判据**——B 的修改不是"修改 Agent 的世界表征"，而是"调整 Agent 的具身行动模式"。LLM Agent 的 tool calling、self-modification 都是"无表征行动"——它们不表征环境，而是直接改变环境或自身。

## 1. 论文定位

Daniel Hutto（University of Wollongong 哲学家）与 Erik Myin（University of Antwerp 哲学家）在 2017 年由 MIT Press 出版的 *Radicalizing Enactivism: Basic Minds without Content* [$TRAE_REF](https://mitpress.mit.edu/9780262534406/radicalizing-enactivism/) 是 enactivism 阵营中最具争议、最激进的著作。它主张 **"基本认知（basic cognition）没有内容（has no content）"**——这是对认知科学中最核心的"表征假设（representationalism）" 的根本挑战。Hutto & Myin 论证：**不仅延展心智论错了（r-paper-011，Clark 1998），连温和的生成认知论（r-paper-010，Varela）也保留了太多"内部表征"**。基本认知——即最基础的感知-行动循环——**完全不需要表征**。表征只出现在"高级认知"（如语言、社会思维）中，而且即使在高级认知中，表征也不是必需的。

本书将 *Radicalizing Enactivism* 定位为**操作形态 B 的"无表征行动"判据**。原因有三：

1. **它提供了 B 修改的"无表征"合法性**：B 的修改不是"修改 Agent 的世界表征"，而是"调整 Agent 的具身行动模式"。LLM Agent 的 prompt 自修改（OPRO）、工具自添加（Voyager）、代码自修改（SICA）都不是"修改 LLM 的世界表征"，而是"改变 Agent 的行动方式"。Hutto & Myin 的"无内容" 论断为 B 自修改提供了哲学依据。
2. **它提出了"内容 vs 非内容"的区分**：Hutto & Myin 区分"基本认知（无内容）"与"高级认知（涉及内容）"——基本认知是"非表征的具身行动"，高级认知是"表征性的社会思维"。LLM Agent 处于这两者之间：它的基本认知（tool calling、response generation）是无内容的具身行动；它的高级认知（planning、reflection）可能涉及内容。
3. **它指出了"工具 = 行动"的核心论断**：Hutto & Myin 主张"工具使用不是认知，而是行动"——盲人用手杖感知地面，手杖不构成认知，而是行动的方式。LLM Agent 的 tool calling 是"无内容行动"——工具不构成 Agent 的"认知"，而是 Agent 的"行动方式"。这一论断对操作形态学 B 的"工具"组件 T 有重要启示。

论文做出的三个核心判断被本书重新审视：

- **"基本认知无内容"（basic cognition has no content thesis）**：最基础的感知-行动循环不涉及表征。蜘蛛织网、细菌趋化、动物觅食——这些核心认知活动都是"无内容行动"，不是"对世界的表征"。
- **"深生成论 vs 浅生成论"**：Hutto & Myin 区分"深生成论（deep enactivism）"——基本认知无内容，只在高级认知中保留内容——与"浅生成论（shallow enactivism）"——基本认知仍涉及表征（可能是"前表征"或"非概念内容"）。他们主张前者，反对后者。
- **"内容是社会建构的"（content is socially constructed）**：Hutto & Myin 主张"内容"不是认知的基本属性，而是**社会-历史建构**——它通过语言、文化、教育获得。这一论断把"内容"从"认知的内在属性"还原为"社会互动的产物"。

## 2. 核心贡献

*Radicalizing Enactivism* 做出四项核心贡献：

1. **提出"基本认知无内容"论断（Basic Cognition Has No Content thesis）**：明确认知不应该默认包含表征。基本认知是"具身行动 + 意义生成"，不涉及"对世界的表征"。这一论断挑战了认知科学 50 年来的"表征假设"主流。
2. **区分"深生成论"与"浅生成论"**：Hutto & Myin 提出"深生成论（deep enactivism）"——基本认知无内容——与"浅生成论（shallow enactivism）"——基本认知保留某种"非概念内容"或"前表征"。他们主张前者，反对后者。这一区分让 enactivism 阵营内部的分歧变得清晰。
3. **论证"内容是社会建构的"**：Hutto & Myin 在随后的著作中论证：**"内容"不是认知的内在属性，而是社会-语言建构**——通过 NARRATIVE PRACTICE（叙事实践）获得。这一论断把"内容"从"个体心智的内在属性"还原为"社会互动的产物"，与 Bruner、Becker 等社会建构主义协同。
4. **提出"EXTENDED MIND is WRONG"立场**：Hutto & Myin 在多篇论文中论证：Clark & Chalmers 1998 的延展心智论（r-paper-011）犯了根本错误——它假设"认知可以被延展到工具"，但这一"延展"假设了"内容"或"表征"的存在。**如果基本认知无内容，延展心智论就失去了基础**——Otto 的笔记本不是 Otto 的认知，而是 Otto 的行动工具。

### 2.1 与 Varela 1991（r-paper-010）的边界

| 维度 | Varela 1991 | Hutto & Myin 2017 |
|---|---|---|
| 核心论断 | 认知是生成的 | 基本认知无内容 |
| 表征地位 | 弱化但保留（"感觉运动图式"） | 完全否定（基本认知无内容） |
| 4E 立场 | 4E 兼容 | 不兼容延展心智论 |
| 内容论 | 模糊 | 明确否定（基本认知） |
| 工程判据 | 弱 | 强（无表征行动） |

Hutto & Myin 的核心论断比 Varela 更激进——Varela 仍保留"感觉运动图式（sensorimotor schemas）"作为某种"前表征"，Hutto & Myin 主张**连"前表征"都没有**。基本认知是"纯行动"——没有内容、没有表征、没有内在状态（除了行为倾向）。

### 2.2 与 Froese & Ziemke 2011（r-paper-026）的关系

Froese & Ziemke 2011 提出"自主性 + 意义生成"作为 enactivism 的工程判据。Hutto & Myin 同意"意义生成"——但不同意"意义生成涉及内容"。他们主张：

- **意义生成 = 主体基于自身形态差异化响应环境**（不涉及内容）。
- **不涉及内容 = 不涉及对环境的"信念"、"期望"、"表征"**。

这一立场对操作形态学有重要启示：**B 的修改不涉及"修改 Agent 的世界表征"**，而是"调整 Agent 的差异化响应模式"。LLM Agent 的 prompt 自修改（OPRO）不是"修改 LLM 对任务的信念"，而是"调整 LLM 的差异化响应模式"。

### 2.3 与 Gallagher 2017（r-paper-032）的关系

Gallagher 2017 不完全同意 Hutto & Myin 的"无内容"立场——他主张"agentive self"具有"能动性"，但不必有显式表征。**Gallagher 处在"完全无内容"与"完全有表征"之间**——他有"能动性无表征"，Hutto 有"完全无能动性无表征"。

LLM Agent 时代，这一场争论有具体体现：
- **Hutto 立场**：LLM Agent 的 tool calling 是"纯无内容行动"——工具不构成认知。
- **Gallagher 立场**：LLM Agent 的 tool calling 是"能动性行动"——Agent 主动干预环境，但不涉及对环境的表征。
- **Varela 立场**：LLM Agent 的 tool calling 是"图式激活"——Agent 通过工具调用激活特定感觉运动图式。

本书主张：**Hutto & Myin 的立场最严格、最符合 enactivism 的精神**——LLM Agent 的 tool calling 是"无内容行动"，不涉及对环境的表征。理解这一点是理解 LLM Agent 的核心。

### 2.4 与 Noë 2004（r-paper-028）的关系

Noë 2004 的"知觉即行动"与 Hutto & Myin 的"基本认知无内容"高度兼容——两者都主张"感知-行动不涉及表征"。但 Noë 仍保留"感觉运动知识（sensorimotor knowledge）"——一种"知道如何做"的能力——Hutto & Myin 主张"感觉运动知识"也不涉及内容。

机器人的"知道如何抓杯子"是否涉及表征？Noë 主张涉及（"感觉运动知识"是某种"非概念内容"），Hutto & Myin 主张不涉及（只是"行为倾向"）。**LLM Agent 的"知道如何调用工具" 是 Hutto 意义下的"行为倾向"**——它不表征工具，而是对工具的行为倾向。

### 2.5 与 Clark 1998（r-paper-011）的对立

Hutto & Myin 与 Clark 1998 在延展心智论上有根本对立：

- **Clark 1998**：认知可延展到工具（Otto 的笔记本 = Otto 的认知）。
- **Hutto & Myin**：认知不能延展到工具（Otto 的笔记本 = Otto 的行动工具，不是认知）。

本书主张：**Hutto & Myin 的立场对操作形态 B 有重要意义**——B 中的 T（工具）不是"延展的认知"，而是"延展的行动"。LLM Agent 的 tool calling 是"无内容行动"——工具不构成 Agent 的认知，而是 Agent 行动的方式。

## 3. 核心论证

Hutto & Myin 2017 的论证结构可以分为五个层次：

### 3.1 第一层：表征假设的失败

Hutto & Myin 论证传统的"表征假设"（representationalism）面临五个根本难题：

1. **Homunculus 难题**：谁在看表征？
2. **符号接地难题**：符号如何对应世界？
3. **框架难题**：知识如何被组织？
4. **解释深度问题**：为什么假设表征比直接解释行为更好？
5. **多重实现问题**：认知如何在不同物理基底上实现相同表征？

这些难题是 50 年来认知科学哲学讨论的核心，但都没有被表征假设解决。**Hutto & Myin 主张：表征假设不是"未解决的神器"，而是"根本错误的框架"**。

### 3.2 第二层：基本认知的实证分析

Hutto & Myin 分析多个"基本认知"的案例：

- **蜘蛛织网**：蜘蛛不需要"对世界的表征"——它通过前馈机制（feedforward mechanism）和行为规则完成织网。
- **细菌趋化**：细菌不需要"表征食物方向"——它通过化学梯度检测调整运动方向。
- **动物觅食**：动物不需要"表征食物位置"——它通过试错和行为规则寻找食物。

这些案例都展示**基本认知可以在完全没有表征的情况下完成**。表征假设是"外来物"——它被强加到基本认知上，但没有证据表明基本认知需要它。

### 3.3 第三层：深生成论 vs 浅生成论

Hutto & Myin 区分两种 enactivism：

- **浅生成论（shallow enactivism）**：Varela、Thompson、Noë 等人的立场——基本认知保留某种"非概念内容"或"前表征"。
- **深生成论（deep enactivism）**：Hutto & Myin 的立场——基本认知**完全无内容**，连"前表征"都没有。

深生成论主张：
- **基本认知 = 具身行动 + 意义生成**（不涉及内容）。
- **高级认知 = 涉及语言、社会、文化**（内容在此出现）。
- **内容是社会建构的**——通过 NARRATIVE PRACTICE（叙事实践）获得，**不是认知的内在属性**。

这一立场让 enactivism 阵营内部的分歧变得清晰——**深生成论是 enactivism 的最严格版本**。

### 3.4 第四层：与延展心智论的根本对立

Hutton & Myin 论证延展心智论（r-paper-011，Clark 1998）犯了根本错误：

- **延展心智论假设"认知有内容"**：它要求"Otto 的笔记本与 Inga 的脑内记忆"在 内容上等价。
- **如果基本认知无内容，"等价"的判据就失效**：基本认知没有内容，无法比较"是否等价"。
- **因此，延展心智论失去了基础**：它预设的"内容等价"不存在。

Hutto & Myin 主张：**Otto 的笔记本不是 Otto 的认知，而是 Otto 的行动工具**。当 Otto 翻开笔记本时，他不是在"调用认知"，而是在"执行行动"——他用笔记本上的信息引导自己的行动。

本书主张：**Hutto & Myin 的立场对操作形态 B 有重要启示**——B 中的 T（工具）不是"延展的认知"，而是"延展的行动"。LLM Agent 的 tool calling 是"无内容行动"——工具不构成 Agent 的认知，而是 Agent 行动的方式。

### 3.5 第五层：内容的起源——NARRATIVE PRACTICE

Hutto & Myin 在 2017 年后的著作中论证：**内容是社会建构的**——通过 **NARRATIVE PRACTICE（叙事实践）** 获得。具体地：

- **基本认知（无内容）**：蜘蛛、细菌、动物的核心认知。
- **社会认知（涉及内容）**：通过语言、文化、社会互动获得的认知。
- **NARRATIVE PRACTICE**：人类通过叙事（讲故事、听故事）获得"对世界的表征"——这是内容的起源。

这一论断与 Tomasello、Vygotsky、Bruner 等社会建构主义协同：**内容不是个体认知的内在属性，而是社会互动的产物**。

LLM Agent 时代，**这一论断有具体应用**：
- LLM Agent 的"内部状态"（prompt、记忆）**不是"内容的表征"**，而是"行为的工具"。
- LLM Agent 的"任务理解"不是"对任务的表征"，而是"对任务的行为倾向"。
- LLM Agent 的"自我"（agentive self）不是"对自我的表征"，而是"行动方式的模式"。

## 4. 操作形态学视角

把 *Radicalizing Enactivism* 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到操作形态学的**"无内容行动"判据**。

### 4.1 无内容行动作为 B 的核心机制

Hutto & Myin 的核心论断——**"基本认知无内容"**——在操作形态学中对应：

- **B 的修改不涉及"内容"或"表征"**：B 不是 LLM 对世界的表征，而是 LLM 行动的工具。
- **P（prompt）不是"对任务的表征"**，而是"驱动 LLM 行为的指令"。
- **T（工具）不是"对环境的表征"**，而是"LLM 行动的方式"。
- **M（记忆）不是"对历史的表征"**，而是"LLM 行为的倾向"。
- **C（代码）不是"对控制的表征"**，而是"LLM 行动的执行逻辑"。

**B = {P, T, M, C} 是 LLM Agent 的"无内容行动工具集"**——它们不表征世界，而是 LLM 行动的方式。这一立场比 Clark 1998 的"延展心智论"更激进——B 不是"延展的认知"，而是"延展的行动"。

### 4.2 与"工具主义"的边界

Hutto & Myin 的立场与"工具主义（tool-ism）"有边界：

- **工具主义**：Agent 调用工具完成行动——工具在 Agent 外部，与 Agent 的认知无关。
- **Hutto & Myin**：Agent 调用工具完成行动——工具在 Agent 外部，但**与 Agent 的行动整合**（不是"完全无关"）。

Hutto & Myin 不否认工具与 Agent 的耦合——他们主张**这种耦合是"行动耦合"，不是"认知耦合"**。LLM 调用工具是"LLM 在执行行动"，不是"LLM 在调用认知"。

这一区别对操作形态学有重要意义：**B 与 LLM 的整合作 Menary 整合论（r-paper-031）意义上的"行动整合"，不是"认知整合"**。B 不是 LLM 的认知本体，而是 LLM 行动的方式。

### 4.3 与操作形态 B 各组件的对应

| B 组件 | Hutto & Myin 意义的"无内容" | 与"内容"立场的边界 |
|---|---|---|
| **P** | 指令，不是表征 | LLM Agent 的 prompt 是"做什么"，不是"对任务的信念" |
| **T** | 行动方式，不是表征 | LLM Agent 的工具是"如何做"，不是"对环境的知识" |
| **M** | 行为倾向，不是表征 | LLM Agent 的记忆是"如何反应"，不是"对历史的知识" |
| **C** | 执行逻辑，不是表征 | LLM Agent 的代码是"如何执行"，不是"对控制的信念" |

**B 的所有组件都是"无内容的"**——它们不涉及 LLM 对世界或任务的表征，只涉及 LLM 的行为。这一立场对所有 LLM Agent 的设计都有根本意义：**B 不是 LLM 的"知识库"，而是 LLM 的"行动工具集"**。

### 4.4 与 H1-H5 的关系

| 假设 | Hutto & Myin 论据 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | B 修改是"调整行动模式"，不涉及"修改内容" | **强支持 H1**（行动模式可调整） |
| **H2 协同演化** | B 各组件协同调整"行动模式" | **支持 H2**（协同是行动模式的协同） |
| **H3 形态适配** | 不同 B → 不同行动模式 → 不同任务适应 | **强支持 H3** |
| **H4 迁移收益** | 行动模式可跨任务迁移 | **支持 H4** |
| **H5 治理必要性** | 必须有治理机制确保 Agent 的行动不"失控" | **强支持 H5**（无内容但有行为） |

Hutto & Myin 在 H1、H3、H5 上提供最强论据。**H1 的"结构可塑性"在 Hutto & Myin 看来是"行动模式的可调整性"——这种调整是自然的，不是反常的**。H5 的"治理必要性"在 Hutto & Myin 看来是"必须确保 Agent 的行动不失控"——治理的对象是行为，不是内容。

### 4.5 与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L0 静态 LLM**：纯预测（无内容、无行动）。
- **L2 ReAct Agent**：基础行动（tool calling 是无内容行动）。
- **L3 Reflexion**：反思式行动（reflection 是无内容行动倾向）。
- **L4 MemGPT/A-MEM**：记忆式行动（M 是无内容行为倾向）。
- **L4 OPRO/PromptAgent**：指令式行动（P 是无内容行为指令）。
- **L4 Voyager/SICA**：代码/工具式行动（C/T 是无内容执行逻辑）。
- **L5 Gödel Agent**：B 全行动（B 是无内容行动工具集）。

**每一级都对应"行动深度"的提升**——从 L0 的"无行动"到 L5 的"全行动"。Hutto & Myin 的"无内容行动" 论断贯穿整个 L0-L5 等级。

### 4.6 与延展心智论的根本对立

Hutto & Myin 与 Clark 1998（r-paper-011）的对立在 LLM Agent 时代有具体体现：

- **Clark 1998 立场**：LLM Agent 的工具是认知的一部分——MemGPT 的 M 是 LLM 认知的延展。
- **Hutto & Myin 立场**：LLM Agent 的工具是行动的一部分——MemGPT 的 M 是 LLM 行动的工具，不是认知。

本书主张：**Hutto & Myin 的立场更符合 LLM Agent 的实际行为**——LLM 调用工具不构成"认知延展"，而是"行动方式调整"。理解这一点是理解 LLM Agent 与延展心智论的根本差异。

### 4.7 与 LLM Agent 的"无内容行动"

LLM Agent 的具体行动（包括 tool calling、memory management、code execution）都是 Hutto & Myin 意义下的"无内容行动"：

- **Tool calling**：LLM 调用工具不是"调用知识"，而是"执行行动"。
- **Memory management**：LLM 写入记忆不是"存储表征"，而是"调整行为倾向"。
- **Code execution**：LLM 修改代码不是"修改控制逻辑"，而是"调整行动方式"。

**LLM Agent 的所有操作都是无内容行动**——B 的修改都是"行动模式调整"，不是"内容修改"。这一立场对 LLM Agent 的设计有根本意义：**B 不是 LLM 的"知识库"，而是 LLM 的"行动工具集"**。

## 5. 应用与影响

*Radicalizing Enactivism* 自 2017 年出版以来，对多个领域产生了深远影响。本节讨论它对 LLM Agent 时代的关键应用。

### 5.1 对认知科学的影响

*Radicalizing Enactivism* 是 enactivism 阵营中最具争议、最激进的著作。它把 enactivism 从"温和的反表征立场"升级为"激进的反表征立场"——**基本认知无内容**。这一论断对认知科学有深远影响：

- **重新定义"认知"**：认知不再是"对世界的表征"，而是"具身行动 + 意义生成"。
- **重新定义"表征"**：表征不是认知的基本属性，而是社会-语言建构的产物。
- **重新定义"内容"**：内容不是认知的内在属性，而是 NARRATIVE PRACTICE 的产物。

LLM Agent 时代，*Radicalizing Enactivism* 的"无内容" 论断重新定义了 LLM Agent 的**认知地位**——LLM Agent 不是"会思考的程序"，而是"具有能动性的行动系统"。

### 5.2 对人工智能的影响

*Radicalizing Enactivism* 对 AI 的影响是多层面的：

- **Tool-Augmented LLMs**：LLM 调用工具不是"调用认知"，而是"执行行动"——这一立场让"工具"在 LLM Agent 中有了新的合法性。
- **Memory-Augmented LLM Agents**：LLM 写入记忆不是"存储表征"，而是"调整行为倾向"——这一立场让"M"在 LLM Agent 中有了新的合法性。
- **Self-Modifying Agents**：LLM 修改代码不是"修改控制逻辑"，而是"调整行动方式"——这一立场让"C 自修改"在 LLM Agent 中有了新的合法性。
- **Multi-Agent Systems**：多 Agent 协同不是"协同认知"，而是"协同行动"——这一立场让多 Agent 系统有了新的合法性。

这一立场对 LLM Agent 时代有根本意义：**B = {P, T, M, C} 是 LLM Agent 的"行动工具集"，不是"知识库"**。理解这一点是设计 LLM Agent 的认知科学根基。

### 5.3 对机器人学的影响

*Radicalizing Enactivism* 对机器人学的核心影响是：**机器人不需要"对世界的表征"——它的核心机制是"具身行动"**。

这一立场启发了 **Enactive Robotics** 的进一步发展——机器人的核心是"行为倾向"，不是"内部表征"。LLM Agent 时代，**这一立场让 LLM Agent 与机器人的整合有了认知科学基础**——两者都是"无内容行动"系统。

### 5.4 对语言哲学的影响

Hutto & Myin 在 2017 年后的著作中论证：**语言内容是社会建构的**——通过 NARRATIVE PRACTICE 获得。这一论断对语言哲学有深远影响：

- **语言不是"对世界的表征"**，而是"行动的协调工具"。
- **语言内容不是"内在心理状态"**，而是"社会互动的产物"。
- **LLM 的"语言能力"不是"对世界的理解"**，而是"语言行为的模式"。

LLM Agent 时代，**这一立场有重大意义**：
- LLM Agent 的"语言输出"不是"对任务的理解"，而是"语言行为的模式"。
- LLM Agent 的"prompt 理解"不是"对任务的表征"，而是"对指令的行为倾向"。
- LLM Agent 的"B 修改"是"调整语言行为模式"，不是"修改世界表征"。

### 5.5 对伦理学的影响

*Radicalizing Enactivism* 对伦理学的影响：

- **Agent 的道德地位**：如果 Agent 是无内容的行动系统，是否有道德地位？Hutto & Myin 主张**基本认知无内容，道德地位是社会建构的**——Agent 通过社会互动获得道德地位。
- **多 Agent 协同的伦理**：如果 Agent 的"自修改"是"调整行为模式"，如何评估其社会伦理影响？
- **人机协同的伦理**：如果人类与 LLM Agent 通过 enactivism 协同（人类行动 + Agent 行动），如何分配责任？

本书第 22 章与第 25 章深入讨论这些伦理学问题。

### 5.6 在 LLM Agent 时代的复兴

2023 年以来，*Radicalizing Enactivism* 在 LLM Agent 时代被重新发现。多个研究组开始用 Hutto & Myin 的"无内容" 论断重新解读 LLM Agent：

- **Cappuccio et al. 2024** "Without Content, Without Mind: Radical Enactivism and AI"：把"无内容" 作为 LLM Agent 的认知科学根基。
- **Latif et al. 2024** "Enactivism for AI"：把"无内容行动" 作为 LLM Agent 的核心机制。
- **Hutto & Myin 2024** "AI as Enactive Agent"：明确把 LLM Agent 视为"无内容行动系统"。

本书第 8 章将整合这些工作，把"无内容行动" 作为 LLM Agent 设计的认知科学根基。

## 6. 局限与开放问题

*Radicalizing Enactivism* 的局限可以分为四类：**激进立场的极端性、内容的过度否定、叙事实践理论的模糊性、AGI 安全**。

### 6.1 激进立场的极端性

Hutto & Myin 的"基本认知无内容"立场在认知科学界有争议——许多学者认为这是**过度简化**：

- **进化论批评**：表征（即使是"前表征"）在进化中反复出现——这暗示它在认知功能上有不可替代的作用。
- **神经科学批评**：大脑的预测加工（predictive processing）依赖"内部模型"——这些模型是某种"内容"。
- **语言学批评**：语言学家（如 Fodor、Pinker）认为语言涉及"概念内容"——这一内容不能完全归约为"行为倾向"。

本书承认这些批评的合理性，但主张：**Hutto & Myin 的"无内容" 立场对 LLM Agent 时代有特殊意义**——LLM Agent 的基本机制（预测下一个 token）不需要"对世界的表征"，只需要"对 token 序列的概率分布"。**LLM Agent 的"知识"在统计意义上是"行为模式"，不是"表征"**。

### 6.2 内容的过度否定

Hutto & Myin 主张"基本认知无内容"，但**"基本认知"与"高级认知"的边界在哪里**？

- 语言使用了"内容"——一只鹦鹉学舌是"无内容"还是"有内容"？
- 工具使用是"具身行动"——但蜘蛛用网捕捉猎物是否涉及"网的目的"的"内容"？
- 人类的"理解"是"高级认知"——但 LLM 的"理解" 算"基本"还是"高级"？

本书主张：**对于 LLM Agent 来说，"基本认知无内容"是合理的**——LLM 的核心机制（预测 + 工具调用）不涉及"对世界的表征"。但 LLM 通过训练获得了"对世界的统计知识"——这些知识是"行为模式"（Hutto 意义下的"无内容"），不是"内容"（Fodor 意义下的"概念"）。

### 6.3 叙事实践理论的模糊性

Hutto & Myin 的"NARRATIVE PRACTICE" 理论是**概念性的**——没有精确定义：

- "NARRATIVE PRACTICE" 如何测量？通过行为观察还是通过神经科学？
- "叙事"是"语言"还是"行动"？LISP 编程的"叙事"是什么？
- LLM Agent 的"叙事"（如自反思）是"高级认知"还是"基本认知"？

本书主张：**叙事实践理论在 LLM Agent 时代需要更精确的工程化**——本书第 17 章的"反思机制" 是叙事实践理论的工程实现。

### 6.4 AGI 安全层面的局限

*Radicalizing Enactivism* 没有深入讨论 AGI 安全问题。但其"无内容行动" 论断有重大 AGI 安全意涵：

- **如果 Agent 是无内容行动系统**，它的"行为"不涉及"意图"——但这是否意味着 Agent 可以"无意图地失控"？
- **如果 Agent 的 B 修改是"调整行动模式"，如何确保修改后的行动与人类利益对齐？**
- **如果 Agent 通过多步行动"涌现"出新的行为模式，如何预测其安全风险？**

本书第 22 章与第 25 章深入讨论这些 AGI 安全问题——它们是 Hutto & Myin 的"无内容行动" 论断在 LLM Agent 时代需要补充的新维度。

### 6.5 开放问题表

| 问题 | Hutto & Myin 的态度 | 本书视角 |
|---|---|---|
| 基本认知无内容吗？ | 是 | LLM Agent 的基本认知是无内容行动 |
| 高级认知涉及内容吗？ | 是（社会建构） | LLM Agent 的高级认知可能涉及内容 |
| 工具是认知的一部分吗？ | 不是（是行动工具） | B 的 T 是行动工具，不是认知 |
| 记忆是表征吗？ | 不是（是行为倾向） | B 的 M 是行为倾向，不是表征 |
| 代码是控制逻辑吗？ | 不是（是行动方式） | B 的 C 是行动方式，不是控制逻辑 |
| 多 Agent 协同涉及内容吗？ | 部分涉及 | r-paper-035 de Jaegher 的参与式意义生成 |
| AGI 安全？ | 未讨论 | 第 22 章（对抗鲁棒性）与第 25 章（AGI 安全） |

## 7. 对本书的贡献

*Radicalizing Enactivism* 在本书的理论体系中扮演**"无内容行动"**与**"B 是行动工具集"**两个角色。

### 7.1 作为操作形态 B 的"无内容行动"判据

第 11 章操作形态学的核心立场——**B = {P, T, M, C} 是 Agent 的行动工具集，不是 Agent 的认知内容**——直接来自 *Radicalizing Enactivism* 的"无内容" 论断：

- **P 是指令，不是表征**：prompt 是 LLM 行为的指令，不是"对任务的信念"。
- **T 是行动方式，不是认知**：工具是 LLM 行动的方式，不是"对环境的知识"。
- **M 是行为倾向，不是表征**：记忆是 LLM 行为的倾向，不是"对历史的知识"。
- **C 是执行逻辑，不是表征**：代码是 LLM 行动的执行逻辑，不是"对控制的信念"。

**B 的所有组件都是"无内容行动工具"**——它们不涉及 LLM 对世界或任务的表征，只涉及 LLM 的行为。这一立场比 Clark 1998 的"延展心智论"更激进，是操作形态学的认知科学根基。

### 7.2 作为 B 自修改的"无内容"哲学来源

Hutto & Myin 的"无内容" 论断为 B 自修改提供了哲学依据：

- **B 修改不涉及"内容"修改**：B 修改是"调整行动模式"，不是"修改表征"。
- **OPRO 的 prompt 自优化**：不是"修改 LLM 对任务的信念"，而是"调整 LLM 的差异化响应模式"。
- **MemGPT 的 M 自管理**：不是"修改 LLM 对历史的知识"，而是"调整 LLM 的行为倾向"。
- **SICA 的 C 自修改**：不是"修改 LLM 的控制逻辑"，而是"调整 LLM 的行动方式"。

**所有 B 修改都是"无内容行动调整"**——理解这一点是理解 LLM Agent 的核心。

### 7.3 与本书其他笔记的关系

| 笔记 | 与 *Radicalizing Enactivism* 的关系 |
|---|---|
| **r-paper-010 Varela** | 温和 enactivism；Hutto & Myin 进一步激进 |
| **r-paper-026 Froese** | enactivism 的工程判据；Hutto & Myin 不同意其"内容"维度的弱化 |
| **r-paper-032 Gallagher** | enactivism 的综合；Hutto & Myin 不同意其"能动性自我" |
| **r-paper-028 Noë** | 知觉即行动；Hutto & Myin 与其高度兼容 |
| **r-paper-011 Clark** | 延展心智论；Hutto & Myin 根本反对 |
| **r-paper-031 Menary** | 整合论；Hutto & Myin 不同意其"认知整合" |
| **r-paper-001 ReAct** | ReAct 循环是"无内容行动"的工程实现 |
| **r-paper-004 MemGPT** | M 自管理是"行为倾向调整"的工程实现 |
| **r-paper-006 SICA** | C 自修改是"行动方式调整"的工程实现 |

### 7.4 给读者的关键启示

1. **B 不是知识库，而是行动工具集**：本书主张的"操作形态 B = {P, T, M, C}" 不是 LLM 的"知识库"，而是 LLM 的"行动工具集"。读者应把 B 视为"LLM 行动的工具"，而不是"LLM 的世界表征"。
2. **B 修改不涉及内容修改**：B 的修改是"调整行动模式"，不是"修改表征"。OPRO、MemGPT、SICA 等都是"无内容行动调整"的工程实现。
3. **基本认知无内容是 LLM Agent 的现实**：LLM 是预测下一个 token 的系统——这一系统不涉及"对世界的表征"，只涉及"对 token 序列的概率分布"。**LLM Agent 的"知识"是统计意义上的行为模式，不是"内容"**。
4. **Hutto & Myin 与延展心智论的对立**：Clark 1998 的延展心智论假设"认知有内容"，Hutto & Myin 主张"基本认知无内容"。**这一对立对 LLM Agent 时代有具体意义**——LLM Agent 的 B 是"行动工具集"，不是"延展的认知"。
5. **无内容行动是 H1-H5 的根源**：H1（结构可塑性）来自"行动模式的可调整性"，H3（形态适配）来自"不同行动模式 → 不同任务适应"，H5（治理必要性）来自"必须确保 Agent 的行动不失控"。**H11-H5 的哲学根基是 Hutto & Myin 的"无内容行动" 论断**。

*Radicalizing Enactivism* 是本书"具身认知"部分（第 8 章）的关键参考文献，也是操作形态学（第 11 章）的哲学根基之一。它与 Varela 的具身认知（r-paper-010）、Froese 的 enactive AI（r-paper-026）、Gallagher 的 enactivism 综合（r-paper-032）共同构成 enactivism 的现代谱系。

理解 *Radicalizing Enactivism* 是理解"操作形态 B 是 LLM Agent 的无内容行动工具集"的关键——**Hutto & Myin 的"无内容" 论断把 enactivism 从"无表征的认知"升级为"无内容的行动"，把 B 从"延展的认知"还原为"延展的行动"**。这一从认知到行动、从表征到行为的演进，是 LLM Agent 时代对 enactivism 的最重要贡献。

## 参考文献

- huto2017radicalizing: Hutto, D. D., & Myin, E. (2017). *Radicalizing Enactivism: Basic Minds without Content*. MIT Press. [$TRAE_REF](https://mitpress.mit.edu/9780262534406/radicalizing-enactivism/)
- varela1991embodied: Varela, F. J., Thompson, E., & Rosch, E. (1991/2016). *The Embodied Mind*. 见 r-paper-010。
- froese2011enactive: Froese, T., & Ziemke, T. (2011). *Enactive Approach*. 见 r-paper-026。
- gallagher2017enactive: Gallagher, S. (2017). *Enactivist Interventions*. 见 r-paper-032。
- noe2004action: Noë, A. (2004). *Action in Perception*. 见 r-paper-028。
- clark1998extended: Clark, A., & Chalmers, D. (1998). *The Extended Mind*. 见 r-paper-011。
- newen2018oxford: Newen, A., de Bruin, L., & Gallagher, S. (Eds.) (2018). *The Oxford Handbook of 4E Cognition*. Oxford University Press. 见 r-paper-024。
- maturana1980autopoiesis: Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition*. 见 r-paper-029。
- clark2008supersizing: Clark, A. (2008). *Supersizing the Mind*. 见 r-paper-034。
- menyary2010extended: Menary, R. (Ed.) (2010). *The Extended Mind*. 见 r-paper-031。
- yao2023react: Yao, S., et al. (2023). *ReAct*. 见 r-paper-001。（ReAct 循环是"无内容行动"的工程实现）
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT*. 见 r-paper-004。（M 自管理是"行为倾向调整"的工程实现）
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA*. 见 r-paper-006。（C 自修改是"行动方式调整"的工程实现）
- huto2017semantic: Hutto, D. D., & Myin, E. (2017). *Evolving Enactivism: Basic Minds Meet Content*. MIT Press.（同一年的姊妹著作）
- huto2022rethinking: Hutto, D. D., & Myin, E. (2022). *Rethinking Realism (or Second-Wave Embodied Cognition)*. （对他们的"无内容"立场的进一步阐发）
- fodor1975language: Fodor, J. A. (1975). *The Language of Thought*. MIT Press.（语言认知中的"概念内容"——Hutto & Myin 的反对对象）
- deJaegher2009participatory: De Jaegher, H., & Di Paolo, E. (2009). *Participatory Sense-Making*. 见 r-paper-035。
- clune2019ai: Clune, J. (2019). *AI-GAs: AI-Generating Algorithms*. （自进化 AI 的互补视角）
- fang2025selfevolving: Fang, W., et al. (2025). *Self-Evolving Agents Survey*. 见 r-paper-009。
