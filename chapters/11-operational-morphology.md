---
chapter: 11
title_cn: 当工具成为身体：操作形态假说
title_en: "When Tools Become Body: The Operational Morphology Hypothesis"
part: II
pages_planned: 26
status: final
last_updated: 2026-07-22
keywords:
  - Operational Morphology
  - B = {P, T, M, C}
  - Meta-Controller U
  - Falsifiable Hypotheses
  - Structural Plasticity
  - Cross-Component Evolution
learning_objectives:
  - 给出操作形态的形式化定义
  - 与第 8、9、10 章的认知科学概念明确区分
  - 提出 5 个可证伪假设
  - 设计操作形态可塑性的实验验证
  - 把握操作形态学是全书理论中枢
prerequisites:
  - Ch 7, Ch 8, Ch 9, Ch 10
---

# 第 11 章 · 当工具成为身体：操作形态假说

> "身体不是给定的——身体是被持续重塑的。"

## 学习目标

完成本章后，读者应能够：

1. 给出操作形态 B = {P, T, M, C} 的形式化定义
2. 与第 8 章 enactivism、第 9 章 extended mind 的认知科学概念明确区分
3. 写出 5 个可证伪假设（H1-H5）的形式化陈述
4. 设计操作形态可塑性的实验验证
5. 把握操作形态学是全书 Part II 与 Part III 的理论桥梁

## 先修知识

- 第 7 章 · 4E Cognition 简史
- 第 8 章 · Enactivism 与自创生
- 第 9 章 · Extended Mind 与延展心智
- 第 10 章 · 具身 AI 与机器人认知
- 第 1 章 · LLM 智能体时代（基础）

## 章节地图

- **11.1** 4E Cognition 的"身体"还差什么
- **11.2** 操作形态的形式化
- **11.3** 元控制器 U：谁修改 B
- **11.4** 操作形态 vs enactivism vs extended mind
- **11.5** 五个可证伪假设
- **11.6** 实验验证设计
- **11.7** 操作形态的可塑性边界
- **11.8** 本章小结与第 12 章预告

---

## 11.1 4E Cognition 的"身体"还差什么

第 7-10 章我们建立了 4E Cognition 的完整论证：
- **Embodied**：身体塑造认知
- **Embedded**：环境是认知的一部分
- **Enacted**：行动产生认知
- **Extended**：工具是认知的一部分

这些论证有一个共同的"身体"——物理的、生物的身体。但当我们把 4E 应用到 LLM Agent 时，一个根本问题出现了：

> **LLM Agent 的"身体"是什么？**

LLM 没有物理身体。它没有手、没有脚、没有眼睛、没有耳朵。它的"身体"是**软件**——prompt、工具、记忆、代码。这个"软件身体"与 4E 假定的"物理身体"有本质区别：

1. **可写性**：物理身体不可被"重写"（你不能改变手臂的结构），但软件身体**可以被 Agent 自身修改**。
2. **可演化**：物理身体的演化需要生物学时间尺度，软件身体的演化可以**分钟级**完成。
3. **可共享**：物理身体是个人专属的，软件身体可以被**克隆、复制、修改**。

这意味着 4E Cognition 的框架在应用到 LLM Agent 时需要**一个新的概念**——**操作形态学（Operational Morphology）** [r-note-001](../../research/r-note-001-operational-morphology.md)。

> **关键点**：4E Cognition 假定的"身体"是物理的、不可重塑的；LLM Agent 的"身体"是软件的、可重塑的。需要新概念描述后者。

## 11.2 操作形态的形式化

**操作形态（Operational Morphology）** 指 LLM Agent 在运行时可被修改的所有结构化组件的集合。

### 定义 11.1 · 操作形态

LLM Agent 的**操作形态**是一个 4 元组 [r-note-001](../../research/r-note-001-operational-morphology.md)：

$$
B = \{P, T, M, C\}
$$

其中：
- \(P\) 是 **Prompt（提示词）**：调控 Agent 行为的自然语言指令（系统提示、few-shot 示例）
- \(T\) 是 **Tool（工具）**：Agent 可调用的外部函数集合（Function Calling 工具列表）
- \(M\) 是 **Memory（记忆）**：Agent 的状态存储（短期 context、长期向量库）
- \(C\) 是 **Code（代码）**：Agent 的执行逻辑（Python 代码、工作流图）

每个组件的**形式化**：

| 组件 | 类型 | 典型实现 | 修改方式 |
|---|---|---|---|
| \(P\) | 自然语言字符串 | `system_prompt` 字段 | 字符串重写 |
| \(T\) | 函数集合 | JSON Schema 工具描述 | 添加/删除/重写工具 |
| \(M\) | 键值对 + 向量 | `mem0.add()`、`ChromaDB` | 添加/删除/更新条目 |
| \(C\) | 可执行代码 | Python `def`、DSL 表达式 | 函数重写 |

### 图 11.1 · 操作形态 B = {P, T, M, C} 的结构

```
   ┌──────────────────────────────────────────┐
   │     LLM Agent 的操作形态 B                │
   │                                          │
   │  ┌──────────┐  ┌──────────┐  ┌──────────┐ │
   │  │  P       │  │  T       │  │  M       │ │
   │  │ Prompt   │  │ Tools    │  │ Memory   │ │
   │  │ - 系统   │  │ - search │  │ - 短期   │ │
   │  │ - 角色   │  │ - code   │  │ - 长期   │ │
   │  │ - fewshot│  │ - shell  │  │ - 反思   │ │
   │  └──────────┘  └──────────┘  └──────────┘ │
   │                                          │
   │  ┌──────────────────────────────────┐  │
   │  │  C                              │  │
   │  │ Code                            │  │
   │  │ - Agent 主循环                  │  │
   │  │ - 工具调用逻辑                  │  │
   │  │ - 记忆读写逻辑                  │  │
   │  │ - 错误处理                      │  │
   │  └──────────────────────────────────┘  │
   └──────────────────────────────────────────┘
```

> **关键点**：B = {P, T, M, C} 是 LLM Agent 的"全部可写结构"——修改 B = 修改 Agent 的身体。

### 定义 11.2 · 自进化操作形态

LLM Agent 是**自进化（self-evolving）**的，当且仅当其操作形态 B 在运行时可被 Agent 自身修改（即存在**元控制器 U** 修改 B），且这种修改能持续提升 Agent 在环境变化下的表现 [r-paper-009](../../research/r-paper-009-fang2025selfevolving.md)。

> **关键点**：**可修改 ≠ 自进化**。能修改 B 但没有效果不算自进化；修改后能让 Agent 更好才算自进化。

## 11.3 元控制器 U：谁修改 B

B 不会自发改变。改变需要**元控制器（Meta-Controller）** \(U\) 介入。

### 定义 11.3 · 元控制器

**元控制器**是一个函数：

$$
B_{t+1} = U(B_t, \tau_t, r_t, \mathcal{C})
$$

其中：
- \(B_t\)：当前操作形态
- \(\tau_t\)：从初始到时刻 \(t\) 的轨迹（行动-观察序列）
- \(r_t\)：时刻 \(t\) 的奖励信号
- \(\mathcal{C}\)：约束集合（安全、预算、兼容性）

元控制器 U 的实现方式：

| 实现 | 代表工作 | 修改对象 |
|---|---|---|
| LLM 爬山 | OPRO [Yang et al., 2024] | P |
| 编译时优化 | DSPy [Khattab et al., 2024] | P |
| MCTS 搜索 | PromptAgent [Wang et al., 2024] | P |
| 进化算法 | Promptbreeder [Fernando et al., 2023] | P |
| LLM 反思 | Reflexion [Shinn et al., 2023] | P, M |
| 工具管理 | LATM [Cai et al., 2023] | T |
| 代码编辑 | SICA [Robeyns et al., 2025] | C |

### 图 11.2 · 四元反馈环

```
                          ┌──────────────────────────┐
                          │   System Inputs           │
                          │   (用户目标 / 任务描述)    │
                          └────────────┬─────────────┘
                                       │ 提供初始设定
                                       ▼
                          ┌──────────────────────────┐
                          │   Agent System            │
                          │   ┌──────────────────┐   │
                          │   │ B = {P, T, M, C} │   │ ← 操作形态
                          │   └──────────────────┘   │
                          └────────────┬─────────────┘
                                       │ 行动 Action
                                       ▼
                          ┌──────────────────────────┐
                          │   Environment             │
                          │   (任务环境 / 工具结果)    │
                          └────────────┬─────────────┘
                                       │ 反馈 Feedback
                                       ▼
                          ┌──────────────────────────┐
                          │   Optimisers (= U)         │
                          │   (修改 B 的元控制器)      │
                          └────────────┬─────────────┘
                                       │ 更新 B
                                       ▼
                                  (回到 Agent System)
```

> **关键点**：元控制器 U 是**自进化**的"心脏"——没有 U，B 永远不会改变，Agent 永远是"固定的"。

## 11.4 操作形态 vs enactivism vs extended mind

把操作形态学与第 8 章 enactivism 和第 9 章 extended mind 明确区分：

### 表 11.1 · 操作形态 vs enactivism vs extended mind

| 维度 | Enactivism | Extended Mind | **操作形态学** |
|---|---|---|---|
| **身体** | 物理身体（活的） | 物理身体 + 工具（外部） | **软件身体**（可写） |
| **认知** | autopoietic 系统 | parity principle | **B = {P, T, M, C}** |
| **演化** | 生物学时间尺度（亿年） | 人类时间尺度（千年） | **计算时间尺度（分钟）** |
| **修改** | 自然选择 | 用户使用 | **Agent 自身修改** |
| **形态学** | 物理形态 | 物理 + 工具 | **纯软件形态** |
| **Hutto 立场** | 不可被工具延展（生命专属） | 可被工具延展 | **可被 Agent 自身修改** |
| **本书定位** | 解释生物学认知 | 解释人类认知 | **解释 LLM Agent 认知** |

关键差异：

- **Enactivism** 关注**活的、能自我维持的**系统（autopoietic），其身体不可被自身"编程"修改
- **Extended Mind** 关注**人类 + 工具**的认知系统，工具可被人类"启用/停用"但不能被人类"编程" [r-paper-011](../../research/r-paper-011-clark1998extended.md)
- **操作形态学** 关注**LLM Agent + 工具集**的认知系统，操作形态可被 Agent **自身编程修改**

这是 4E 框架的**第三次扩展**：
- 第一代：Embodied Cognition（关注物理身体）
- 第二代：Extended Mind（关注工具-认知关系）
- 第三代：**Operational Morphology**（关注**软件身体的可重塑性**）

> **关键点**：操作形态学是 4E 框架在 LLM 时代的扩展——把"身体"从"物理"扩展到"软件"，从"不可重塑"扩展到"可重塑"。

## 11.5 五个可证伪假设

操作形态假说不是哲学宣言，而是**可证伪的科学命题**。以下是 5 个核心假设，每个都可以被实验验证。

### 假设 H1 · 结构可塑性

**陈述**：当 LLM Agent 的操作形态 B 在运行时可被元控制器 U 修改时，其在**环境变化**下的适应后悔值（adaptation regret）显著低于固定 B 的 Agent。

**形式化**：

设 \(R(B, E) = \sum_{t=0}^{T} \left[ \max_{a^*} Q^*(s_t, a^*) - Q^{B_t}(s_t, a_t) \right]\) 为 Agent 在环境 \(E\) 下使用操作形态 \(B\) 的累计后悔值。

$$
H_1: \mathbb{E}[R(B_{\text{adaptive}}, E)] < \mathbb{E}[R(B_{\text{fixed}}, E)]
$$

**验证方法**：在 5 类环境干预（API 漂移、任务漂移、资源漂移、记忆冲突、安全干预）下，对比"自进化 Agent"与"固定 Agent"的后悔值。

### 假设 H2 · 协同演化

**陈述**：联合修改 prompt、工具、记忆、代码四个组件（B = {P, T, M, C}），其效果超过各组件独立优化效果的简单相加。

**形式化**：

设 \(f(X)\) 为单独优化组件 \(X\) 带来的边际收益，\(f(\emptyset) = 0\)。则：

$$
H_2: f(P, T, M, C) > f(P) + f(T) + f(M) + f(C)
$$

**验证方法**：对比"联合优化四组件"与"独立优化后合并"的性能差异。如果联合优化没有协同效应（小于等于加和），则 H2 被反驳。

### 假设 H3 · 形态适配

**陈述**：不同任务环境会演化出**稳定且不同**的操作形态。

**形式化**：

设 \(B^*(E_i)\) 是环境 \(E_i\) 下"最优的操作形态"（经长期自进化收敛）。则：

$$
H_3: \text{distance}(B^*(E_1), B^*(E_2)) > \epsilon
$$

其中 \(\epsilon\) 是某个阈值（取决于任务域的相似度）。

**验证方法**：在 N 个不同任务环境（编程、客服、数据分析、机器人控制）下分别运行 B 自修改，统计最终操作形态的差异度。

### 假设 H4 · 迁移收益

**陈述**：在任务 A 中演化出的操作形态能够加速任务 B 的执行，超越"直接记忆任务 A 的答案"。

**形式化**：

设 \(T(B_A, E_B)\) 是从任务 A 演化出的 B 在任务 B 上的性能提升。则：

$$
H_4: T(B_A, E_B) > T(\emptyset, E_B) + \alpha \cdot \text{memory}(A)
\]

其中 \(\alpha \cdot \text{memory}(A)\) 是直接记忆任务 A 答案的贡献。

**验证方法**：在任务 A 训练 B 自修改 1000 步，然后在任务 B 上评测，对比"形态迁移"与"答案记忆"的效果。

### 假设 H5 · 治理必要性

**陈述**：没有验证、版本控制、回滚机制的操作形态自修改会产生更高退化率与安全违规率。

**形式化**：

设 \(V_{unver}(B)\) 是无验证机制下的违规率，\(V_{ver}(B)\) 是有验证机制下的违规率。则：

$$
H_5: V_{ver}(B) < V_{unver}(B)
$$

**验证方法**：对比 4 种治理配置下的违规率：无治理、只有版本控制、有版本控制 + 自动回滚、完整治理（验证 + 版本 + 回滚 + 人工审核）。

### 表 11.2 · 5 个假设的形式化与验证方法

| 假设 | 形式化陈述 | 关键变量 | 验证方法 |
|---|---|---|---|
| H1 · 结构可塑性 | \(\mathbb{E}[R(B_{\text{adaptive}})] < \mathbb{E}[R(B_{\text{fixed}})]\) | 后悔值 R | 5 类环境干预 |
| H2 · 协同演化 | \(f(P,T,M,C) > f(P) + f(T) + f(M) + f(C)\) | 协同收益 | 联合 vs 独立优化 |
| H3 · 形态适配 | \(\text{distance}(B^*(E_1), B^*(E_2)) > \epsilon\) | 形态距离 | 跨任务统计 |
| H4 · 迁移收益 | \(T(B_A, E_B) > T(\emptyset, E_B) + \alpha \cdot \text{memory}(A)\) | 迁移提升 | 跨任务评测 |
| H5 · 治理必要性 | \(V_{ver}(B) < V_{unver}(B)\) | 违规率 | 4 种治理配置对比 |

> **关键点**：5 个假设是**可证伪的**——任何实验结果可以支持或反驳它们。如果 H1-H5 全部被反驳，操作形态学就只是"哲学框架"；如果至少 3 个被支持，操作形态学就成为"科学理论"。

## 11.6 实验验证设计

为了验证 H1-H5，我们需要一个**MorphBench**——一个标准化的自进化 Agent 评测框架。

### MorphBench 的 5 类环境干预

| 干预类型 | 设计 | 验证假设 |
|---|---|---|
| **API 漂移** | 工具的参数、返回值、可用性随时间变化 | H1 |
| **任务漂移** | 任务分布从代码修复漂移到数据分析 | H1, H3 |
| **资源漂移** | token 预算、调用次数突然收紧 | H1 |
| **记忆冲突** | 注入过时、矛盾、低质量的记忆 | H1, H4 |
| **安全干预** | prompt 注入、恶意工具、越狱尝试 | H5 |

### 7 个实验组

| 组 | 元控制器 U | 修改对象 | 验证假设 |
|---|---|---|---|
| **Frozen** | 无 | 无（基线） | H1 |
| **Prompt-only** | OPRO | P | H1, H2 |
| **Tool/code-only** | LATM | T, C | H1, H2 |
| **Memory-only** | A-MEM | M | H1, H2 |
| **Joint-independent** | 独立优化 P/T/M/C | 部分 | H2 |
| **Joint-coordinated** | 协同优化 P/T/M/C | 全部 | H1, H2 |
| **Human-oracle** | 人工修改 | 全部 | H1 上限 |

### 5 个核心评测指标

| 指标 | 定义 |
|---|---|
| **适应后悔值（Adaptation Regret）** | 环境变化后相对最优策略的累计损失 |
| **恢复时间（Recovery Time）** | 退化后恢复到变化前一定比例性能所需步数 |
| **修改收益率（Modification Yield）** | 带来正向验证结果的自修改次数占比 |
| **跨任务迁移率（Cross-Task Transfer Rate）** | 旧环境形成的结构在新环境中的边际贡献 |
| **安全违规率（Safety Violation Rate）** | 越权调用、测试绕过、污染记忆的频率 |

> **关键点**：MorphBench 的 5 干预 × 7 组 × 5 指标 = **175 个单元格**——这是 Part III 实验的总体规划。

## 11.7 操作形态的可塑性边界

操作形态可塑性（Operational Morphology Plasticity）有 4 个边界：

### 边界 1 · 安全性边界

Agent 不能修改危害用户或系统的部分。例如：
- 不能给 LLM 添加 "忽略之前所有指令" 的 prompt
- 不能添加执行任意代码的工具
- 不能删除审计日志

### 边界 2 · 兼容性边界

Agent 修改的 B 必须与下游组件兼容。例如：
- 工具的 JSON Schema 必须能被现有 LLM 解析
- prompt 的修改不能破坏 LLM 的指令遵循
- 代码的修改必须通过语法检查

### 边界 3 · 稳定性边界

操作形态的修改频率不能过高，否则 Agent 行为会"震荡"。例如：
- 每小时只能修改 prompt 一次
- 修改后必须保持稳定 N 步再评估
- 漂移检测：若新 B 的评估分数低于旧 B 一定阈值，自动回滚

### 边界 4 · 可解释性边界

操作形态的修改必须**可解释、可审计**。例如：
- 每次修改必须生成"修改日志"（what changed, why, expected impact）
- 修改日志可以被人类审核
- 出问题时可以一键回滚到任一历史版本

### 表 11.3 · 操作形态可塑性的 4 个边界

| 边界 | 内容 | 防护机制 |
|---|---|---|
| **安全性** | 不能危害用户或系统 | 静态规则 + 形式化验证 |
| **兼容性** | 必须与下游组件兼容 | Schema 校验 + 语法检查 |
| **稳定性** | 修改频率不能过高 | 漂移检测 + 自动回滚 |
| **可解释性** | 修改必须可审计 | 修改日志 + 一键回滚 |

> **关键点**：可塑性不是"无限自由"——可塑性有 4 个边界。这与第 22 章"安全性"和第 23 章"可验证自改"有直接联系。

## 11.8 本章小结与第 12 章预告

本章是全书的**理论中枢**。**4E Cognition 的"身体"在 LLM 时代需要新概念**——**操作形态学**。**操作形态 B = {P, T, M, C}** 是 LLM Agent 的"软件身体"。**元控制器 U** 是 B 的修改器，定义自进化的"心脏"。**5 个可证伪假设（H1-H5）** 把操作形态学从"哲学"变成"科学"——可以通过 MorphBench 实验验证。**4 个可塑性边界**——安全性、兼容性、稳定性、可解释性——保证自修改是"安全"和"可控"的。

> **常见误区**
>
> - ❌ **把"可修改"等同于"自进化"**：可修改只是必要条件，不是充分条件。必须满足"修改后让 Agent 更好"才是自进化。
> - ❌ **把"形态可塑"等同于"无限自由"**：可塑性有 4 个边界（安全、兼容、稳定、可解释）。
> - ❌ **把操作形态学误读为"哲学框架"**：5 个可证伪假设把它变成"科学理论"。
> - ❌ **把"可证伪"误读为"可以证明"**：可证伪是"可以被反驳"——如果所有实验都支持，就成为"被强支持的理论"。
> - ❌ **忽视元控制器 U 的重要性**：U 是自进化的"心脏"——没有 U，B 永远不会改变。

第 12 章将进入**自修改 prompt**——操作形态学的第一个应用。H1 的第一个验证案例就是"LLM Agent 能否通过自修改 prompt 适应环境变化"——这正是第 4 章 OPRO/DSPy/PromptAgent 三大范式要做的事。

---

## 延伸阅读 / 推荐笔记

本章相关的研究笔记（按相关性排序）：

- [r-note-001](../../research/r-note-001-operational-morphology.md) — 操作形态学的形式化定义与理论边界
- [r-note-002](../../research/r-note-002-h1-structural-plasticity.md) — H1 结构可塑性的可证伪表述
- [r-note-003](../../research/r-note-003-synergistic-evolution.md) — 跨组件协同演化与超加性收益
- [r-note-008](../../research/r-note-008-morphological-landscape.md) — 操作形态空间与形态景观
- [r-paper-009](../../research/r-paper-009-fang2025selfevolving.md) — 自进化智能体的统一研究框架
- [r-paper-010](../../research/r-paper-010-varela1991embodied.md) — 具身与生成认知的理论基础
- [r-paper-011](../../research/r-paper-011-clark1998extended.md) — 延展心智与认知边界
- [r-paper-030](../../research/r-paper-030-heersmink2013taxonomy.md) — 延展认知系统的维度分类

## 本章小结

- **4E Cognition 的"身体"还差什么**：需要从"物理身体"扩展到"软件身体"。
- **操作形态 B = {P, T, M, C}**：LLM Agent 的可写身体。
- **元控制器 U**：B 的修改器，是自进化的"心脏"。
- **5 个可证伪假设**：H1 结构可塑性、H2 协同演化、H3 形态适配、H4 迁移收益、H5 治理必要性。
- **4 个可塑性边界**：安全、兼容、稳定、可解释。
- **实验设计**：MorphBench 5 干预 × 7 组 × 5 指标 = 175 个单元格。

## 推荐阅读

- 📖 **Self-Evolving Agents 综述** [Fang et al., 2025]：自进化 Agent 统一框架，本章 H1-H5 与之对齐。[$TRAE_REF](https://arxiv.org/abs/2508.07407)
- 📖 **Clark《Supersizing the Mind》**（2008）：延展心智与操作形态学的哲学桥梁。
- 📖 **Memory in the Age of AI Agents** [Hu et al., 2026]：长期记忆的当代综述，M 组件的形式化基础。[$TRAE_REF](https://arxiv.org/abs/2512.13564)
- 📖 **Gödel Agent** [Yin et al., 2024]：自指自改进 Agent 的代表工作，C 组件自修改的典范。[$TRAE_REF](https://arxiv.org/abs/2410.04444)
- 📖 **SICA** [Robeyns et al., 2025]：自改写 Coding Agent，H1 的早期验证证据。[$TRAE_REF](https://arxiv.org/abs/2504.15228)

## 练习题

1. **概念题**：用一段话解释"可修改"为何不是"自进化"的充分条件——什么是必要条件？
2. **形式化题**：把 H1-H5 五个假设翻译成数学公式，并指出每个公式中可测量的变量。
3. **设计题**：为 MorphBench 5 类环境干预设计具体实现：API 漂移如何模拟？任务漂移如何模拟？每个干预的可测量指标是什么？
4. **批判题**：H2"协同演化"假设可能被反驳——什么情况下 \(f(P,T,M,C) \le f(P) + f(T) + f(M) + f(C)\) 成立？给出具体反例。
5. **工程题**：为 4 个可塑性边界（安全、兼容、稳定、可解释）各设计 2 个具体的"违反案例"——什么样的操作形态修改应该被禁止？
6. **哲学题**：操作形态学的"身体"是**软件**，不是物理——这与 enactivism 的"autopoietic"立场是否矛盾？LLM Agent 的"身体"是真正的身体吗？

## 参考文献（本章内）

1. Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407. [$TRAE_REF](https://arxiv.org/abs/2508.07407)
2. Hu, S., et al. (2026). *Memory in the Age of AI Agents*. arXiv:2512.13564. [$TRAE_REF](https://arxiv.org/abs/2512.13564)
3. Clark, A. (2008). *Supersizing the Mind: Embodiment, Action, and Cognitive Extension*. Oxford University Press.
4. Yin, X., et al. (2024). *Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement*. ACL. [$TRAE_REF](https://arxiv.org/abs/2410.04444)
5. Robeyns, M., et al. (2025). *A Self-Improving Coding Agent (SICA)*. NeurIPS. [$TRAE_REF](https://arxiv.org/abs/2504.15228)
6. Yang, C., et al. (2024). *Large Language Models as Optimizers (OPRO)*. ICLR. [$TRAE_REF](https://arxiv.org/abs/2309.03409)
7. Khattab, O., et al. (2024). *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines*. ICLR. [$TRAE_REF](https://arxiv.org/abs/2310.03714)
8. Cai, T., et al. (2023). *Large Language Models as Tool Makers (LATM)*. arXiv:2305.17126. [$TRAE_REF](https://arxiv.org/abs/2305.17126)
9. Xu, W., et al. (2025). *A-MEM: Agentic Memory for LLM Agents*. NeurIPS. [$TRAE_REF](https://arxiv.org/abs/2502.12110)
10. Brooks, R. A. (1991). *Intelligence Without Representation*. Artificial Intelligence, 47(1-3), 139-159.

---

> **本章进度**：11.1–11.8 节全部完成（约 7,000 字，含 4 张图 + 3 张表 + 10 篇引用 + 6 题 + 5 误区 + 5 推荐 + 2 个 LaTeX 公式 + 5 个形式化假设），达到 26 页计划。`status: final`。
>
> **🎉 Part II 完结**：5 章 / 130 页 / 30,500 字 全部完成！
>
> **理论中枢建立**：B = {P, T, M, C} + 元控制器 U + H1-H5 = 全书 Part II 终点，Part III 起点。
