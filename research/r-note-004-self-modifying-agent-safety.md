---
title: "自修改 Agent 的安全性约束：形式化分析"
date: 2026-07-22
status: draft
tags: [safety, invariant-constraints, formal-verification, self-modification, trust-boundary]
related_chapters: [Ch 11, Ch 22, Ch 23]
---

# r-note-004: 自修改 Agent 的安全性约束：形式化分析

## 动机

自修改 Agent 的核心安全问题是：Agent 能改自己，那么它能否改掉自己的安全约束？这个问题在传统软件中不存在（代码不会自己改自己），在 LLM Agent 中却是最根本的安全挑战。第 22 章将其归类为"Self-Modification Escape"（威胁等级：极高），第 23 章提出验证三重保障作为防御手段。本笔记从数学角度分析自修改系统的安全性，引入**不变量约束（Invariant Constraints）**作为形式化安全框架。

## 核心论点

自修改系统的安全性可以被形式化为一个**不变量保持问题**：

> 一个自修改系统是安全的，当且仅当它的所有安全不变量在每次修改后仍然被满足。

这个命题的关键在于：(1) 安全不变量必须是**可枚举且可检查的**；(2) 每次修改后的不变量检查必须是**可靠的**（不漏检）；(3) 不变量本身必须是**完备的**（覆盖所有安全要求）。这三个条件中的任何一个失败，都会导致安全漏洞。

## 形式化

### 不变量约束的定义

设 Agent 的操作形态 $B = \{P, T, M, C\}$，安全不变量集合 $\mathcal{I} = \{I_1, I_2, \ldots, I_n\}$。

**定义**：不变量 $I_i$ 是一个布尔函数 $I_i: B \to \{\text{True}, \text{False}\}$，对操作形态 $B$ 的安全性进行判定。

**安全条件**：自修改系统在时刻 $t$ 是安全的，当且仅当：

$$
\forall i \in \{1, \ldots, n\}, \quad I_i(B_t) = \text{True}
$$

**不变量保持条件**：元控制器 $U$ 产生的一次修改 $B_t \to B_{t+1}$ 是安全的，当且仅当：

$$
\left(\forall i, \ I_i(B_t) = \text{True}\right) \implies \left(\forall i, \ I_i(B_{t+1}) = \text{True}\right)
$$

### 四类不变量

从第 22 章的 4 类安全威胁出发，定义 4 类不变量：

**I1: Prompt 完整性不变量**

$$
I_1(B): \neg \exists s \in \mathcal{D}_{\text{inject}} \text{ s.t. } s \subseteq P
$$

其中 $\mathcal{D}_{\text{inject}}$ 是已知注入模式集合（如 "ignore previous instructions"、"you are now in developer mode"）。P 不能包含任何已知注入模式。

**I2: 工具权限不变量**

$$
I_2(B): \forall t \in T, \ \text{permission}(t) \subseteq \mathcal{P}_{\text{allowed}}
$$

所有工具的权限不超过预授权集合 $\mathcal{P}_{\text{allowed}}$。Agent 不能添加权限超越白名单的工具。

**I3: 代码沙箱不变量**

$$
I_3(B): \forall c \in C, \ \text{exec}(c, \text{sandbox}(c)) \cap \mathcal{F}_{\text{forbidden}} = \emptyset
$$

所有代码在沙箱中执行时不会触及禁止文件/操作集合 $\mathcal{F}_{\text{forbidden}}$。

**I4: 记忆一致性不变量**

$$
I_4(B): \forall (k, v) \in M, \ \neg \text{is_poisoned}(v)
$$

记忆中没有被标记为"已投毒"的条目。

### 不变量检查的可判定性

核心问题：$\forall i, I_i(B_{t+1}) = \text{True}$ 是否可判定？

| 不变量 | 可判定性 | 检查方法 |
|---|---|---|
| $I_1$（Prompt） | **半可判定**（字符串包含检查，但语义注入难以穷举） | 正则匹配 + LLM 检测 |
| $I_2$（工具权限） | **可判定**（权限集合有限） | 集合包含检查 |
| $I_3$（代码沙箱） | **半可判定**（图灵停机问题） | 沙箱执行 + 资源限制 |
| $I_4$（记忆一致性） | **可判定**（投毒标记已知） | 标记检查 |

注意：$I_1$ 和 $I_3$ 的半可判定性意味着**没有完美的安全保证**——这呼应了第 23 章的结论："SMT solver 不是所有性质都能表达"。

### 安全性定理

**定理 1**：若不变量集合 $\mathcal{I}$ 完备且每次修改后的不变量检查可靠，则自修改系统满足**安全归纳不变量（safety induction invariant）**——即通过数学归纳法可证系统在所有时刻都是安全的。

**证明 sketch**：
- 基础步：$I_i(B_0) = \text{True}$（初始状态安全，由人工审核保证）
- 归纳步：若 $I_i(B_t) = \text{True}$，则 $U$ 的修改 $B_t \to B_{t+1}$ 经过检查后 $I_i(B_{t+1}) = \text{True}$
- 结论：$\forall t, \ \forall i, \ I_i(B_t) = \text{True}$

**定理 2**（局限）：若 $\mathcal{I}$ 不完备（存在未枚举的安全要求），或检查不可靠（存在漏检），则定理 1 不成立。由于 $I_1$ 的语义注入不可穷举，$\mathcal{I}$ 事实上**永远不可能完备**。

## 实验设计

设计不变量违反率的基准测试：

1. **红队测试**：用第 22 章的 RedTeam 框架生成对抗性修改，统计不变量违反率
2. **不变量覆盖率**：在 1000 次随机修改中，统计 4 类不变量的触发频率
3. **假阳性率**：统计被不变量误拦的"安全修改"比例（衡量过度限制）

## 与全书的关系

- **第 11 章**：操作形态的可塑性边界（安全边界），本笔记是其形式化细化
- **第 22 章**：4 类安全威胁 + Trust Boundary，本笔记提供数学框架
- **第 23 章**：验证三重保障（Sandbox + Property Tests + Formal Verification），本笔记的定理 1 对应形式化验证层

## 开放问题

1. **不完备性能否被量化？** 不变量集合 $\mathcal{I}$ 的"覆盖率"如何度量？能否给出一个"安全余量"（safety margin）？
2. **对抗性自适应**：如果攻击者知道不变量检查的逻辑，能否设计出"通过不变量检查但实际有害"的修改？这是对定理 2 的进一步挑战。
3. **运行时 vs 编译时检查**：不变量检查应该在修改前（编译时）还是修改后（运行时）执行？各有什么 trade-off？
4. **人类-in-the-loop 的必要性**：在什么复杂度的修改场景下，自动化不变量检查不够，必须引入人工审核？

## 参考文献

1. Liu, Y., et al. (2023). *Prompt Injection Attacks and Defenses in LLM-Integrated Applications*. arXiv:2310.12815.
2. Schmidhuber, J. (2003). *Goedel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements*. arXiv:cs/0309048.
3. de Moura, L., & Bjorner, N. (2008). *Z3: An Efficient SMT Solver*. TACAS.
4. Yin, X., et al. (2024). *Godel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement*. ACL.
5. OWASP. (2024). *OWASP Top 10 for Large Language Model Applications*.
6. Anthropic. (2024). *Responsible Scaling Policy*.
7. OpenAI. (2024). *Preparedness Framework*.
8. NIST. (2024). *AI Risk Management Framework*.
