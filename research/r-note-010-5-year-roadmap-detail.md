---
title: "5 年路线图：从 MorphAgent v1.0 到 AGI 就绪"
date: 2026-07-22
status: draft
tags: [roadmap, 5-year-plan, MorphAgent, v1.0, v2.0, v3.0, milestones, AGI-readiness]
related_chapters: [Ch 18, Ch 25]
---

# r-note-010: 5 年路线图：从 MorphAgent v1.0 到 AGI 就绪

## 动机

第 25 章概述了操作形态学从当前到 AGI 的 5 年路线图，但停留在战略层面。本笔记将路线图细化为三个工程阶段（v1.0 实验验证 / v2.0 跨域泛化 / v3.0 治理完备），为每个阶段设定具体的里程碑、交付物和验收标准。路线图不仅指导 MorphAgent 的开发，也是全书的"实践承诺"——我们不只是提出理论，还要交付可运行的系统。

## 核心论点

5 年路线图的三个阶段对应 L0-L5 能力等级（r-note-009）的渐进达成：

1. **v1.0 阶段（2026-2027）**：达到 L3，验证 H1-H3。核心目标是在受控环境中证明"自修改 Agent 确实比固定 Agent 更好"。这是科学验证阶段。
2. **v2.0 阶段（2028-2029）**：达到 L4，验证 H4-H5。核心目标是在多任务环境中证明"自修改的形态可以迁移"且"有治理的自修改是安全的"。这是工程化阶段。
3. **v3.0 阶段（2030-2031）**：达到 L5，实现 AGI 就绪。核心目标是在开放环境中实现"完整的协同自进化 + 完备的治理机制"。这是部署阶段。

关键 nuance：每个阶段的交付物不仅是代码，还包括论文、数据集和评测框架。路线图与 MILESTONES.md 的 36 个月研究计划对齐，但更侧重 MorphAgent 系统本身的版本演进。

## 形式化

### 阶段定义

$$
\text{Phase}_k = (\text{Version}, \text{TargetLevel}, \text{Timeline}, \text{Milestones}, \text{Acceptance})
$$

### v1.0: 实验验证阶段

$$
\text{Phase}_1 = (\text{v1.0}, \text{L3}, 2026\text{-}2027, M_1, A_1)
$$

**里程碑 $M_1$**：

| 编号 | 里程碑 | 时间 | 验收标准 |
|---|---|---|---|
| M1.1 | MorphAgent 骨架 | 2026-08 | 可运行 ReAct Agent（L0），在 SWE-bench Lite 上 resolve rate > 5% |
| M1.2 | 单组件自修改 | 2027-01 | Prompt 自修改（OPRO 集成），在 GSM8K 上提升 > 5%（L2） |
| M1.3 | MorphBench alpha | 2027-04 | 5 类环境干预全部实现，可跑基线实验 |
| M1.4 | H1 验证 | 2027-07 | 在 MorphBench 上，自适应组的适应后悔值显著低于固定组（$p < 0.05$） |
| M1.5 | 跨组件协同 | 2027-10 | 协同优化 P+T 的效果 > 独立优化之和（$S > 1.1$），达到 L3 |
| M1.6 | v1.0 发布 + ICLR 投稿 | 2027-12 | 开源 MorphAgent v1.0 + MorphBench v0.5，ICLR 2027 投稿 |

**验收条件 $A_1$**：

$$
\text{Level}(\text{MorphAgent}_{v1.0}) = (\mathbf{c}^{(3)}, \{P, T\}, 2) \in L_3
$$

### v2.0: 跨域泛化阶段

$$
\text{Phase}_2 = (\text{v2.0}, \text{L4}, 2028\text{-}2029, M_2, A_2)
$$

**里程碑 $M_2$**：

| 编号 | 里程碑 | 时间 | 验收标准 |
|---|---|---|---|
| M2.1 | 全组件自修改 | 2028-03 | P/T/M/C 四组件全部可修改（SICA 集成），达到 L4 |
| M2.2 | 形态迁移验证 | 2028-06 | 跨任务迁移矩阵 $\Gamma$ 的非对角线均值 $> 0$，H4 被支持 |
| M2.3 | 治理框架集成 | 2028-09 | r-note-007 的三层治理机制全部实现，干预阈值 $\tau_{\text{safety}}$ 自动调优 |
| M2.4 | H5 验证 | 2028-12 | 完整治理组的不变量违反率 < 无治理组的 10%（$p < 0.01$） |
| M2.5 | 多环境评测 | 2029-03 | MorphBench v1.0 完成，在编程/数学/客服/数据 4 个领域均验证 |
| M2.6 | v2.0 发布 + NeurIPS 投稿 | 2029-06 | 开源 MorphAgent v2.0 + MorphBench v1.0，NeurIPS 2028 投稿 |

**验收条件 $A_2$**：

$$
\text{Level}(\text{MorphAgent}_{v2.0}) = (\mathbf{c}^{(4)}, \{P, T, M, C\}, 2) \in L_4
$$

### v3.0: 治理完备阶段

$$
\text{Phase}_3 = (\text{v3.0}, \text{L5}, 2030\text{-}2031, M_3, A_3)
$$

**里程碑 $M_3$**：

| 编号 | 里程碑 | 时间 | 验收标准 |
|---|---|---|---|
| M3.1 | 完整治理（$\gamma = 3$） | 2030-03 | 人工审计机制集成，自适应阈值通过红队测试 |
| M3.2 | 长期运行稳定性 | 2030-06 | 1000 步自修改无安全事件（$V = 0$），性能不退化 |
| M3.3 | 开放环境测试 | 2030-09 | 在真实生产环境（非 benchmark）中运行 30 天，无安全事件 |
| M3.4 | 跨 LLM 验证 | 2030-12 | MorphAgent 在 GPT-4、Claude、Llama 3 上均达到 L5 |
| M3.5 | AGI 就绪评估 | 2031-03 | 通过外部独立审计，获得"AGI 就绪"认证 |
| M3.6 | v3.0 发布 | 2031-06 | MorphAgent v3.0 开源，配套教科书完稿 |

**验收条件 $A_3$**：

$$
\text{Level}(\text{MorphAgent}_{v3.0}) = (\mathbf{c}^{(5)}, \{P, T, M, C\}, 3) \in L_5
$$

## 实验设计

### 跨版本对比实验

每个版本发布前进行标准化的跨版本对比：

| 对比维度 | v1.0 vs 基线 | v2.0 vs v1.0 | v3.0 vs v2.0 |
|---|---|---|---|
| 等级 | L0 → L3 | L3 → L4 | L4 → L5 |
| 适应后悔值 | -30% | -20% | -10% |
| 不变量违反率 | N/A → <5% | <5% → <1% | <1% → 0% |
| 跨任务迁移增益 | N/A | +15% | +10% |

### 关键风险与应对

| 风险 | 阶段 | 概率 | 应对 |
|---|---|---|---|
| H1 被反驳（自修改无效） | v1.0 | 低 | 转向"固定形态优化"路线 |
| H4 被反驳（迁移无效） | v2.0 | 中 | 转向"任务特定自修改"路线 |
| LLM 能力天花板 | v2.0 | 中 | 等待下一代 LLM，调整里程碑 |
| 治理成本过高 | v3.0 | 高 | 降低 $\gamma$ 要求，L5 降级为 L4+ |

## 与全书的关系

- **第 25 章**：路线图的来源，本笔记是其工程化细化
- **第 18 章**：MorphAgent 的参考实现，本笔记定义其版本演进路径
- **r-note-009**：L0-L5 等级定义，本笔记的三个阶段对应等级的渐进达成
- **r-note-007**：治理框架，v3.0 阶段的完整治理基于 r-note-007 的三层机制
- **MILESTONES.md**：36 个月研究计划，本笔记的里程碑与之对齐但更侧重 MorphAgent 系统

## 开放问题

1. **AGI 就绪的判定标准**：谁来判定"AGI 就绪"？是否存在客观标准？还是需要行业共识？
2. **路线图的时间不确定性**：LLM 领域变化极快——如果 2028 年出现 AGI 级别的基础模型，v1.0/v2.0 是否还有意义？
3. **开源 vs 闭源的策略选择**：MorphAgent v3.0 是否应该开源？完整治理机制的开源是否会降低安全性（攻击者可研究绕过方法）？
4. **路线图完成后的下一步**：v3.0 之后的第 6-10 年路线图是什么？是维护稳定版本，还是继续向更高等级推进？

## 参考文献

1. Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407.
2. Anthropic. (2024). *Responsible Scaling Policy*.
3. OpenAI. (2024). *Preparedness Framework*.
4. NIST. (2024). *AI Risk Management Framework*.
5. Jimenez, C. E., et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR.
6. Chan, J. S., et al. (2024). *MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering*. ICLR.
7. Schmidhuber, J. (2003). *Goedel Machines: Self-Referential Universal Problem Solvers Making Provably Optimal Self-Improvements*. arXiv:cs/0309048.
