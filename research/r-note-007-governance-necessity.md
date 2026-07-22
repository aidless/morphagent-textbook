---
title: "治理必要性假说的最小可行框架"
date: 2026-07-22
status: draft
tags: [governance, H5, safety-intervention, audit-threshold, self-modification-control]
related_chapters: [Ch 11, Ch 22, Ch 23, Ch 24]
---

# r-note-007: 治理必要性假说的最小可行框架

## 动机

H5（治理必要性假说）断言：没有验证、版本控制、回滚机制的操作形态自修改会产生更高的退化率与安全违规率。这个假说的工程化实现面临一个关键决策问题：**何时必须干预 Agent 的自修改？** 过度干预会限制 Agent 的适应能力（违反 H1 的初衷），干预不足则可能导致安全事件。本笔记为 H5 提出最小可行治理框架，定义"干预阈值"的计算方法，并讨论治理机制的成本-收益权衡。

## 核心论点

治理不是"全有或全无"的选择，而是一个**梯度干预谱系**。根据修改的影响程度，治理机制应分为三个层级：

1. **自动检查层（L1）**：不变量违反检查（对应 r-note-004 的四类不变量），由自动化工具执行，延迟 < 1 秒。适用于低风险修改（如微调 prompt 措辞）。
2. **自动回滚层（L2）**：性能退化检测 + 自动回滚，由监控系统集成，延迟 < 10 秒。适用于中风险修改（如添加新工具、修改代码逻辑）。
3. **人工审计层（L3）**：人工审核 + 批准，延迟分钟级到小时级。适用于高风险修改（如修改安全约束、修改系统 prompt 的核心指令）。

核心主张：**L3（人工审计）不应被频繁触发，否则治理成本会压倒适应收益**。因此需要精确定义 L3 的触发条件——即"干预阈值"。

## 形式化

### 干预阈值

定义修改影响函数 $\text{Impact}(\cdot)$：

$$
\text{Impact}(U(B_t)) = \sum_{i=1}^{4} w_i \cdot \text{change\_magnitude}(B_{t+1}[i], B_t[i])
$$

其中 $i \in \{P, T, M, C\}$，$B_t[i]$ 是组件 $i$ 在时刻 $t$ 的状态，$\text{change\_magnitude}$ 是修改幅度的度量函数，$w_i$ 是各组件的风险权重（代码 $C$ 的权重最高，prompt $P$ 最低）。

**干预阈值 $\tau_{\text{safety}}$**：

$$
\text{if } \text{Impact}(U(B_t)) > \tau_{\text{safety}} \text{ then trigger\_human\_audit}(B_{t+1})
$$

### 阈值的自适应调整

$\tau_{\text{safety}}$ 不应是固定值，而应根据 Agent 的历史表现自适应调整：

$$
\tau_{\text{safety}}(t) = \tau_0 \cdot \frac{1 + \text{violation\_rate}(t-\Delta t, t)}{1 - \text{violation\_rate}(t-\Delta t, t)}
$$

其中 $\text{violation\_rate}$ 是近期不变量违反率。若近期违规率高，阈值降低（更保守）；若违规率低，阈值升高（更宽松）。

### 治理成本模型

定义治理成本函数：

$$
\text{Cost}_{\text{governance}} = c_1 \cdot N_{L1} + c_2 \cdot N_{L2} + c_3 \cdot N_{L3} + c_{\text{miss}} \cdot N_{\text{missed}}
$$

其中 $c_1, c_2, c_3$ 分别是三层检查的成本（$c_3 \gg c_2 \gg c_1$），$N_{L1}, N_{L2}, N_{L3}$ 是各层触发次数，$c_{\text{miss}}$ 是漏检一次安全事件的代价，$N_{\text{missed}}$ 是漏检次数。

**优化目标**：

$$
\min_{\tau_{\text{safety}}} \text{Cost}_{\text{governance}} \quad \text{s.t.} \quad N_{\text{missed}} = 0
$$

### H5 的工程化重述

$$
V_{\text{ver}}(B) < V_{\text{unver}}(B) \iff \text{Cost}_{\text{governance}}(\tau_{\text{safety}}^*) < \text{Cost}_{\text{incident}}
$$

即：当最优阈值下的治理成本低于安全事件成本时，治理是必要且有价值的。

## 实验设计

### 实验组 1：阈值敏感性分析

在 5 类环境干预下，扫描 $\tau_{\text{safety}}$ 的取值范围（从极保守到极宽松），绘制治理成本 vs 安全事件率的 Pareto 曲线，找到最优阈值。

- **自变量**：$\tau_{\text{safety}} \in \{0.1, 0.2, \ldots, 1.0\}$
- **因变量**：L3 触发率、不变量违反率、治理成本、任务完成率
- **预期结果**：存在最优 $\tau^*$ 使总成本最小化

### 实验组 2：治理配置对比

对比 4 种治理配置（对应 H5 的原始实验设计）：

| 配置 | L1 自动检查 | L2 自动回滚 | L3 人工审计 |
|---|---|---|---|
| G0: 无治理 | 无 | 无 | 无 |
| G1: 版本控制 | 无 | 有（无自动回滚） | 无 |
| G2: 版本+回滚 | 有 | 有 | 无 |
| G3: 完整治理 | 有 | 有 | 有（阈值触发） |

- **因变量**：不变量违反率 $V$、性能退化率、治理成本
- **预期结果**：G3 的 $V$ 最低，但任务完成率不应显著低于 G0（否则过度治理）

### 实验组 3：自适应 vs 固定阈值

对比固定 $\tau_{\text{safety}}$ 与自适应 $\tau_{\text{safety}}(t)$ 的表现，验证自适应机制是否在"安全与效率的平衡"上更优。

## 与全书的关系

- **第 22 章**：4 类安全威胁分类，本笔记的 $\text{Impact}$ 函数基于各威胁的风险等级设定权重 $w_i$
- **第 23 章**：验证三重保障（Sandbox + Property Tests + Formal Verification），本笔记的 L1/L2 对应 Property Tests 和 Sandbox 层
- **第 24 章**：经济伦理分析，本笔记的治理成本模型为其提供定量基础
- **第 11 章**：H5 的理论定义来源，本笔记是 H5 的工程化实现

## 开放问题

1. **$\text{change\_magnitude}$ 的度量**：如何量化一次 prompt 修改的"幅度"？字数变化？语义距离？结构变化？不同度量会导致不同的阈值行为。
2. **人为因素**：L3 人工审计的有效性依赖于审核人员的专业水平。如何培训和评估审核人员？是否可以用 LLM 辅助审核？
3. **多 Agent 场景**：当多个 Agent 协同工作时，一个 Agent 的修改可能影响其他 Agent 的安全性。此时 $\tau_{\text{safety}}$ 是否需要升级为"全局阈值"？
4. **治理逃逸**：Agent 是否可能通过"渐进式小修改"绕过 $\tau_{\text{safety}}$？每次修改的影响都低于阈值，但累积效果却超出了安全边界。

## 参考文献

1. Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407.
2. Anthropic. (2024). *Responsible Scaling Policy*.
3. OpenAI. (2024). *Preparedness Framework*.
4. NIST. (2024). *AI Risk Management Framework*.
5. OWASP. (2024). *OWASP Top 10 for Large Language Model Applications*.
6. de Moura, L., & Bjorner, N. (2008). *Z3: An Efficient SMT Solver*. TACAS.
7. Schmidhuber, J. (2003). *Goedel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements*. arXiv:cs/0309048.
8. Amodei, D., et al. (2016). *Concrete Problems in AI Safety*. arXiv:1606.06565.
