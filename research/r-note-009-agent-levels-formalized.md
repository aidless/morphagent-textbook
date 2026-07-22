---
title: "Agent 能力等级 L0-L5 的形式化定义"
date: 2026-07-22
status: draft
tags: [agent-levels, capability-vector, L0-L5, MorphAgent, formalization, governance-level]
related_chapters: [Ch 11, Ch 18, Ch 22]
---

# r-note-009: Agent 能力等级 L0-L5 的形式化定义

## 动机

第 18 章将 LLM Agent 的能力分为 L0（ReAct）到 L5（协同自进化）六个等级。这个分级在直觉上是清晰的，但缺乏形式化定义——一个 Agent 到底"在什么意义上"属于 L2 而非 L1？等级跃迁的条件是什么？如果没有精确的形式化定义，等级评估就依赖于主观判断，实验对比也缺乏统一标准。本笔记为 L0-L5 建立形式化定义，引入能力向量、修改能力指标和治理等级三个维度，并给出等级跃迁的充分必要条件。

## 核心论点

Agent 能力等级不应仅看"能做什么"，而应看"能改什么"和"改的治理水平"。三个维度缺一不可：

1. **能力向量**（能做什么）：Agent 在任务执行层面的能力，包括推理、工具使用、记忆管理等。
2. **修改能力**（能改什么）：Agent 对自身操作形态的修改权限和修改范围，从"完全不能改"到"能改全部四组件"。
3. **治理等级**（改的约束）：Agent 自修改时的安全保障水平，从"无治理"到"完整治理"。

核心主张：**等级跃迁是能力向量、修改能力和治理等级三者的联合跃迁，单一维度的提升不足以构成等级跃迁**。一个 L3 Agent 不能仅仅因为"推理能力更强"就升到 L4——它必须在修改能力和治理等级上也达到 L4 的标准。

## 形式化

### 能力等级的定义

$$
\text{Level}(A) = (\mathbf{c}_A, \mu_A, \gamma_A)
$$

其中：
- $\mathbf{c}_A = (c_{\text{reason}}, c_{\text{tool}}, c_{\text{memory}}, c_{\text{plan}}, c_{\text{reflect}}) \in [0,1]^5$ 是能力向量
- $\mu_A \subseteq \{P, T, M, C\}$ 是修改能力（Agent 可修改的组件子集）
- $\gamma_A \in \{0, 1, 2, 3\}$ 是治理等级（0=无，1=版本控制，2=自动验证+回滚，3=完整治理）

### 六个等级的形式化

| 等级 | 名称 | 能力向量 $\mathbf{c}_A$ | 修改能力 $\mu_A$ | 治理等级 $\gamma_A$ |
|---|---|---|---|---|
| L0 | ReAct | $c_{\text{tool}} > 0.5$, 其余任意 | $\emptyset$（不能修改） | N/A（无修改需求） |
| L1 | 检索增强 | $c_{\text{memory}} > 0.5$, $c_{\text{tool}} > 0.5$ | $\emptyset$ | N/A |
| L2 | 单组件自修改 | 任一 $c_i > 0.7$ | $|\mu_A| = 1$（仅修改一个组件） | $\gamma_A \geq 1$ |
| L3 | 多组件自修改 | 至少两个 $c_i > 0.7$ | $|\mu_A| \geq 2$ | $\gamma_A \geq 2$ |
| L4 | 系统级自修改 | $\min(\mathbf{c}_A) > 0.7$ | $\mu_A = \{P, T, M, C\}$（全部组件） | $\gamma_A \geq 2$ |
| L5 | 协同自进化 | $\min(\mathbf{c}_A) > 0.8$ | $\mu_A = \{P, T, M, C\}$ | $\gamma_A = 3$ |

### 等级跃迁条件

从 $L_k$ 跃迁到 $L_{k+1}$ 的充分必要条件：

$$
\text{Level}(A) \in L_{k+1} \iff \mathbf{c}_A \succeq \mathbf{c}^{(k+1)} \wedge \mu_A \supseteq \mu^{(k+1)} \wedge \gamma_A \geq \gamma^{(k+1)}
$$

其中 $\succeq$ 表示逐元素大于等于，$\mathbf{c}^{(k+1)}$、$\mu^{(k+1)}$、$\gamma^{(k+1)}$ 是等级 $k+1$ 的最低要求。

**特别注意**：L4 到 L5 的跃迁是最关键的——它要求治理等级从 2 升到 3（引入人工审计），这对应 r-note-007 的干预阈值机制。

### MorphAgent 的目标等级

MorphAgent（第 18 章）的设计目标是 **L5**：

$$
\text{Level}(\text{MorphAgent}) = (\mathbf{c}^*, \{P, T, M, C\}, 3)
$$

其中 $\mathbf{c}^*$ 的所有分量 $> 0.8$。

## 实验设计

### 实验组 1：等级评估协议

为每个等级设计标准化的评估协议：

| 等级 | 评估任务 | 通过标准 |
|---|---|---|
| L0 | SWE-bench Lite | resolve rate > 10% |
| L1 | MLE-bench（需检索外部资料） | resolve rate > 15% |
| L2 | 自修改 prompt 实验（r-exp-004） | 修改后性能 > 基线 + 5% |
| L3 | 跨组件协同实验（r-note-003 设计） | 协同度 $S > 1.2$ |
| L4 | 5 类环境干预全部通过 | 适应后悔值 < Frozen 的 50% |
| L5 | 长期运行（1000 步）无安全事件 | 违规率 $V = 0$ |

### 实验组 2：等级跃迁难度评估

追踪一个 Agent 从 L0 到 L5 的跃迁过程：
- 每个等级需要多少修改轮次才能达到下一等级？
- 哪个跃迁最难？（推测 L3→L4 最难，因为需要全组件修改能力）
- 各等级的"驻留时间"分布如何？

### 实验组 3：等级与任务性能的关系

分析等级与任务性能的相关性：
- 同一任务在不同等级 Agent 上的性能差异
- 是否存在"等级收益递减"（L4→L5 的边际收益小于 L0→L1）？

## 与全书的关系

- **第 18 章**：MorphAgent 参考实现，本笔记为其能力等级提供形式化基础
- **第 11 章**：操作形态 $B = \{P, T, M, C\}$，本笔记的修改能力 $\mu_A$ 直接基于操作形态的组件
- **第 22 章**：安全威胁分类，本笔记的治理等级 $\gamma_A$ 与安全约束的严格程度对应
- **r-note-007**：治理最小可行框架，本笔记的 $\gamma_A = 3$（完整治理）对应 r-note-007 的 L1+L2+L3 三层机制

## 开放问题

1. **等级的连续性 vs 离散性**：L0-L5 是离散的 6 个等级，但实际能力可能是连续的。是否需要更细粒度的子等级（如 L2.5）？
2. **跨 LLM 的等级差异**：同一架构在不同 LLM 上能达到的最高等级是否不同？GPT-4 可能达到 L5，Llama 3 是否只能达到 L3？
3. **等级退化**：Agent 是否会从高等级退化到低等级？（例如环境变化导致修改能力失效）。如何检测和预防退化？
4. **等级的社会含义**：L5 Agent 的部署是否需要特殊的伦理审查？不同等级 Agent 的法律责任如何划分？

## 参考文献

1. Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407.
2. Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR.
3. Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS.
4. Jimenez, C. E., et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR.
5. Chan, J. S., et al. (2024). *MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering*. ICLR.
6. Anthropic. (2024). *Responsible Scaling Policy*.
7. OpenAI. (2024). *Preparedness Framework*.
