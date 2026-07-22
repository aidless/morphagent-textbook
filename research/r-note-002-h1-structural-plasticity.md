---
title: "H1 假说的实证路径：结构可塑性"
date: 2026-07-22
status: draft
tags: [structural-plasticity, H1, experiment-design, adaptation-regret, operational-morphology]
related_chapters: [Ch 11, Ch 12, Ch 19]
---

# r-note-002: H1 假说的实证路径：结构可塑性

## 动机

操作形态学的五个可证伪假设中，H1（结构可塑性）是最基础的——它回答的问题是："让 Agent 能修改自己的 prompt/工具/记忆/代码，到底有没有用？"如果 H1 被反驳，后续的 H2（协同演化）、H3（形态适配）、H4（迁移收益）、H5（治理必要性）都失去了验证前提。因此，H1 的实验设计必须格外严谨，避免"伪阳性"（Type I error）和"伪阴性"（Type II error）。

## 核心论点

H1 的核心陈述是：**可修改操作形态的 Agent，在环境变化下的适应后悔值显著低于固定操作形态的 Agent**。这不是"修改一定更好"的绝对断言，而是一个统计性命题——在足够多的环境变化场景中，自适应 Agent 的期望后悔值更低。

关键 nuance：H1 不要求"每次修改都带来提升"，只要求"长期来看，有修改能力的 Agent 累积后悔值更低"。单次修改失败（退化）是允许的，只要元控制器 U 的整体策略是收敛的。

## 形式化

沿用第 11 章的形式化：

设 $R(B, E) = \sum_{t=0}^{T} [\max_{a^*} Q^*(s_t, a^*) - Q^{B_t}(s_t, a_t)]$ 为累计后悔值。

$$
H_1: \mathbb{E}[R(B_{\text{adaptive}}, E)] < \mathbb{E}[R(B_{\text{fixed}}, E)]
$$

其中 $B_{\text{adaptive}}$ 指元控制器 $U$ 可修改 $B$ 的配置，$B_{\text{fixed}}$ 指 $U$ 被禁用的配置。

**可操作化分解**：H1 的验证需要回答三个子问题：

1. **方向性**：$\mathbb{E}[R_{\text{adaptive}}] - \mathbb{E}[R_{\text{fixed}}] < 0$ 是否成立？
2. **效应量**：差异量级是否具有实际意义（Cohen's $d > 0.5$）？
3. **鲁棒性**：在多少比例的环境干预场景中该方向成立？

## 实验设计

为 H1 设计 3 组实验，分别验证不同层面的结构可塑性：

### 实验组 1：单组件可塑性验证

对比 Frozen（基线）与 4 个单组件修改组（Prompt-only、Tool-only、Memory-only、Code-only），在 5 类环境干预下分别测量适应后悔值。这是 H1 的"基本案例"验证——每种组件单独修改是否有效？

- **自变量**：修改模式（Frozen / P-only / T-only / M-only / C-only）
- **因变量**：适应后悔值 $R(B, E)$、恢复时间
- **控制变量**：LLM 模型、任务集合、环境干预强度
- **统计检验**：Wilcoxon 符号秩检验，Bonferroni 校正后 $\alpha = 0.05/4 \approx 0.0125$
- **预期结果**：若 H1 成立，至少 3/4 的单组件组在后悔值上显著优于 Frozen

### 实验组 2：可塑性速度验证

H1 的隐含假设是"修改越快，后悔值越低"。本实验控制元控制器 U 的修改频率（每 1 步 / 每 5 步 / 每 20 步修改一次），观察后悔值与修改频率的关系。

- **自变量**：修改频率 $f \in \{1, 5, 20\}$（步/修改）
- **因变量**：适应后悔值 $R$、修改收益率（正向修改占比）
- **预期结果**：存在最优修改频率 $f^*$；过于频繁导致震荡（$R$ 上升），过于稀疏导致来不及适应（$R$ 上升）

### 实验组 3：退化案例验证

H1 不排除"修改后性能退化"的可能性。本实验专门追踪每次修改后的性能变化方向，统计"正向修改率"和"退化事件"的特征。

- **自变量**：环境干预类型（5 类）
- **因变量**：每次修改后的 $\Delta V = V(B_{t+1}) - V(B_t)$
- **分析**：退化事件的触发条件是什么？哪些干预类型最容易导致退化？

## 与全书的关系

- **第 11 章**：H1 的理论定义来源，本笔记是 H1 的实验设计细化
- **第 12 章**：Prompt-only 实验组的实现依据（OPRO / DSPy / PromptAgent）
- **第 19 章**：MorphBench 的 5 干预 x 7 组 x 5 指标框架，本笔记的 3 组实验在其内
- **第 22-23 章**：实验组 3 的退化案例分析与安全约束直接相关

## 开放问题

1. **最优后悔值的下界是什么？** Human-oracle 组提供了一个上界参考，但理论下界仍未知——可能与环境的 non-stationarity 程度有关。
2. **单组件修改的"天花板"在哪里？** 如果 Prompt-only 的后悔值已经接近 0，联合优化的边际收益可能很小——H2 可能被弱化。
3. **修改频率与 LLM 成本的权衡**：更频繁的修改需要更多 LLM 调用，这个成本是否值得？需要引入"成本效益比"指标。
4. **跨 LLM 的泛化性**：H1 在 GPT-4 上成立，在 Llama 3 上是否成立？不同 LLM 的可塑性差异多大？

## 参考文献

1. Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407.
2. Yang, C., et al. (2024). *Large Language Models as Optimizers (OPRO)*. ICLR.
3. Khattab, O., et al. (2024). *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines*. ICLR.
4. Robeyns, M., et al. (2025). *A Self-Improving Coding Agent (SICA)*. NeurIPS.
5. Yin, X., et al. (2024). *Godel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement*. ACL.
6. Jimenez, C. E., et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR.
7. Demsar, J. (2006). *Statistical Comparisons of Classifiers over Multiple Data Sets*. JMLR, 7, 1-30.
