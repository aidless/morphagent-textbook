---
note_id: r-paper-014
title: MLE-bench：Kaggle 竞赛作为 ML 工程 Agent 评测基准（MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 19]
related_papers: [chan2024mlebench, jimenez2024swebench, robeyns2025sica, yin2024godelagent, yao2023react, fang2025selfevolving, packer2023memgpt]
keywords: [MLE-bench, Kaggle, ML engineering, machine learning benchmark, AI agent, AutoML, competition, MorphBench, AlphaEvolve, SICA]
---

# r-paper-014：MLE-bench：Kaggle 竞赛作为 ML 工程 Agent 评测基准

> Chan 等人 2024 年发表的 *MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering*（ICLR 2024，arXiv:2410.07095 [$TRAE_REF](https://arxiv.org/abs/2410.07095)）把 LLM Agent 的评测从"代码生成"推到"完整 ML 工程"——它从 75 个真实 Kaggle 竞赛中提取任务，要求 Agent 完成数据预处理、特征工程、模型选择、超参数调优、训练、提交等完整 ML 工作流。这是 **SWE-bench 在 ML 领域的"姊妹基准"**——它把"修改一个函数"的任务扩展为"完成一个 ML 项目"的任务。本书把 MLE-bench 定位为 **MorphBench 在 ML 领域的前身**——它揭示了 ML Agent 的核心能力需求（数据分析 + 多次实验 + 长期迭代），但**没有评估 Agent 自修改 B 的能力**——这是 MorphBench 必须填补的空白。

## 1. 论文定位

Jun Shern Chan 等人 2024 年发表于 ICLR 2024 的 *MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering*（OpenAI，arXiv:2410.07095 [$TRAE_REF](https://arxiv.org/abs/2410.07095)）是 2024 年最具影响力的 ML Agent 评测基准。它直接回答：**LLM Agent 能否像 Kaggle 选手一样完成真实的 ML 竞赛任务**？论文通过构建 MLE-bench——从 75 个真实 Kaggle 竞赛中提取 75 个完整 ML 项目（含数据集、评分标准、提交格式、人类基线）——给出了具体的回答：GPT-4o-based Agent 在 MLE-bench 上获得 16.9% 的"奖牌率"（达到 Kaggle 铜牌及以上水平的竞赛比例），而 AIDE（基于 GPT-4o 的开源框架）获得 34.4%。

本书将 MLE-bench 定位为 **MorphBench 在 ML 领域的前身**——它揭示了 ML Agent 的核心能力需求，但**没有评估 Agent 自修改 B 的能力**。与 SWE-bench 一样，MLE-bench 评测的是**静态形态 Agent 的外部任务能力**，而非**自演化 Agent 的 B 自修改能力**。

论文做出的三个核心判断被本书第 19 章重新审视：

- **"End-to-end ML engineering"**：ML Agent 的评测必须涵盖完整的 ML 工作流（数据加载、特征工程、模型训练、调优、提交）——而非单独的代码生成或模型选择。
- **"Real Kaggle competitions"**：评测任务必须来自真实 Kaggle 竞赛（含人类基线）——这让 Agent 的能力可与人类直接比较。
- **"Resource-aware evaluation"**：Agent 必须在**资源受限**（GPU 时间、磁盘、API 调用）的条件下完成竞赛——这反映了真实 ML 工程的约束。

这三个判断让 MLE-bench 成为 **"ML 领域的 SWE-bench"**——它把 LLM Agent 评测从"代码片段"推向"完整 ML 项目"。

## 2. 核心贡献

MLE-bench 论文做出四项核心贡献：

1. **构建 MLE-bench 基准**：从 75 个真实 Kaggle 竞赛中提取任务，构建端到端 ML Agent 评测基准。这是当时规模最大的 ML Agent 评测集。
2. **提出 ML Agent 评分标准**：基于 Kaggle 的官方评分（公榜 + 私榜）+ 奖牌阈值（铜牌/银牌/金牌）+ 人类基线，给出多维度评分。这是"超越 pass@1"的细粒度评测。
3. **评测多个 LLM + Agent 框架**：在 MLE-bench 上评测 GPT-4o、o1-preview、Claude 3.5 Sonnet、AIDE 等多个 Agent 实现，揭示不同 LLM 和 Agent 框架的能力差异。
4. **提出"AI Researcher"愿景**：把 MLE-bench 作为"AI 自动进行 ML 研究"的评测平台——为未来 AI 自主改进 ML 方法的研究提供基线。

### 2.1 与 SWE-bench 的边界

MLE-bench 与 SWE-bench 都是"真实工程任务评测"，但任务范围不同：

| 维度 | SWE-bench | MLE-bench |
|---|---|---|
| **任务** | 修复 GitHub issue | 完成 Kaggle 竞赛 |
| **代码量** | 修改 1-50 行 | 修改 100-1000+ 行 |
| **任务时长** | 分钟级 | 小时级（多次训练） |
| **领域** | 软件工程 | 机器学习 |
| **评估指标** | 测试通过率 | Kaggle 评分（公榜/私榜） |
| **人类基线** | 工程师 | Kaggle 选手 |
| **资源消耗** | CPU | GPU + CPU |
| **实验迭代** | 单次 patch | 多次实验 + 模型选择 |

这一对比揭示 MLE-bench 的**复杂度显著高于 SWE-bench**——MLE-bench 任务需要 Agent 进行**多次实验迭代**（如尝试不同模型、超参数），而 SWE-bench 任务通常只需生成**一次 patch**。

### 2.2 与之前 ML 基准的边界

MLE-bench 出现之前，ML 基准主要是：

- **OpenML CC-18**（Bischl et al. 2019）：OpenML 上的分类任务集合。
- **Kaggle-specific benchmarks**（Li et al. 2022）：少数 Kaggle 任务的评测。
- **DAWNBench**（Coleman et al. 2018）：模型训练速度基准。
- **MLPerf**（Mattson et al. 2020）：训练/推理性能基准。

这些基准的共同局限是**任务范围有限**——它们要么只覆盖分类任务、要么只覆盖特定模型、要么只评估训练速度。MLE-bench 填补了这一空白：

| 基准 | 任务类型 | 实验迭代 | 人类基线 |
|---|---|---|---|
| OpenML CC-18 | 分类 | 单次训练 | 无 |
| DAWNBench | 训练速度 | 单次训练 | 无 |
| MLPerf | 训练/推理性能 | 多次 | 无 |
| **MLE-bench** | **Kaggle 全任务** | **多次** | **有** |

MLE-bench 是**第一个**大规模、端到端、可与人类比较的 ML Agent 评测基准。

### 2.3 与 AutoML 的边界

MLE-bench 与 AutoML 系统（如 AutoGluon、FLAML、autosklearn）有共同点（自动化 ML 流程），但关键差异是：

- **AutoML**：用贝叶斯优化、进化搜索等算法在**搜索空间**中找到最佳模型——不涉及"自然语言推理"。
- **MLE-bench Agent**：用 LLM 通过**自然语言 + 代码生成 + 工具调用**完成 ML 流程——具有"通用推理"能力。

这一差异是 MLE-bench 的核心创新：**它评测的不是 AutoML 的搜索能力，而是 LLM Agent 的端到端 ML 工程能力**。

### 2.4 与 AI Researcher 的边界

2024-2025 年出现了多个"AI 自动做研究"的工作：

- **The AI Scientist**（Lu et al. 2024, Sakana AI）：Agent 自动撰写 ML 论文。
- **ResearchAgent**（Wang et al. 2024）：Agent 自动做文献调研 + 假设生成 + 实验设计。
- **AutoML-Agent**（Li et al. 2024）：Agent 自动化 ML 流程。

MLE-bench 是这些工作的**评测基础**——它是第一个提供"完整 ML 工程任务 + 人类基线"的评测集。

## 3. 方法细节

### 3.1 MLE-bench 数据集构建

MLE-bench 从 Kaggle 收集 75 个竞赛：

| 类别 | 数量 | 任务类型 |
|---|---|---|
| 图像分类 | 12 | 计算机视觉 |
| 自然语言处理 | 10 | NLP 任务 |
| 时间序列 | 8 | 预测任务 |
| 表格数据 | 35 | 结构化数据 |
| 推荐系统 | 5 | 协同过滤 |
| 异常检测 | 5 | 异常识别 |
| **总计** | **75** | **混合 ML 任务** |

每个竞赛的数据包括：

1. **数据集**：原始数据（train/test/leaderboard 划分）。
2. **任务描述**：竞赛的官方描述（背景、目标、评分标准）。
3. **提交格式**：CSV/Parquet 等提交文件的格式要求。
4. **评分标准**：公榜 + 私榜（如 accuracy、AUC、MSE、IoU 等）。
5. **人类基线**：Kaggle 公开排行榜中铜/银/金牌的分数阈值。
6. **时间限制**：模拟真实 Kaggle 竞赛的时间限制。

### 3.2 Agent 评测框架

MLE-bench 评测框架由两部分构成：

**环境**：Docker 容器，包含：
- Python 环境（PyTorch、TensorFlow、scikit-learn、XGBoost、LightGBM 等）
- Kaggle 数据集
- 资源限制（GPU 时间 24h、CPU 24h、磁盘 50GB）
- 评测脚本（运行 agent + 评分）

**Agent 框架**：MLE-bench 提供了两个参考 Agent 实现：

1. **MLE-bench baseline**：基于 OpenAI 的 function calling + RAG 的简单 Agent。
2. **AIDE**（Wijk et al. 2024）：开源 ML Agent 框架，支持代码生成 + 执行 + 调试 + 实验管理。

Agent 的任务流程：

```
1. 阅读任务描述
2. 加载数据
3. 数据预处理（清洗、特征工程）
4. 选择模型（随机 / 启发式 / 多次尝试）
5. 训练模型
6. 评估模型（在验证集上）
7. 提交预测结果
8. （可选）迭代：尝试其他模型 / 调优超参数
```

Agent 的关键挑战是**资源管理**——它必须在有限的 GPU 时间内完成多次实验。

### 3.3 评测方法：奖牌率 + 人类基线

MLE-bench 的核心评测指标是**奖牌率（Medal Rate）**——Agent 在 75 个竞赛中达到铜牌及以上水平的比例。

奖牌阈值基于 Kaggle 公开排行榜：

| 奖牌 | 阈值（前 X% 选手） | 含义 |
|---|---|---|
| 铜牌 | Top 40-50% | 入门水平 |
| 银牌 | Top 10-20% | 中等水平 |
| 金牌 | Top 1-10% | 顶尖水平 |

评测结果（截至 2024.10）：

| Agent | 铜牌率 | 银牌率 | 金牌率 | 任意奖牌率 |
|---|---|---|---|---|
| GPT-4o (baseline) | 8.0% | 1.3% | 0% | 9.3% |
| o1-preview | 25.3% | 7.6% | 2.5% | 34.4% |
| AIDE + GPT-4o | 16.9% | 4.5% | 0.7% | 21.1% |
| AIDE + o1-preview | 36.7% | 12.7% | 4.5% | 53.9% |
| AIDE + Claude 3.5 Sonnet | ~25% | ~7% | ~2% | ~34% |

**关键观察**：
- o1-preview 显著优于 GPT-4o——推理能力强的 LLM 在 ML Agent 上更有效。
- AIDE 框架显著优于 baseline——Agent 框架的设计（代码生成 + 调试 + 实验管理）有巨大影响。
- 最强组合（AIDE + o1-preview）达到 53.9% 奖牌率——超过 Kaggle 入门选手水平。

### 3.4 资源感知评测

MLE-bench 在**资源受限**条件下评测 Agent：

| 资源 | 限制 | 评估目的 |
|---|---|---|
| GPU 时间 | 24 小时 | Agent 的 GPU 利用效率 |
| CPU 时间 | 24 小时 | Agent 的 CPU 利用效率 |
| 磁盘空间 | 50 GB | Agent 的数据管理能力 |
| API 调用 | 1000 次 | Agent 的 LLM 利用效率 |
| 墙钟时间 | 100 小时 | Agent 的整体效率 |

资源受限让 MLE-bench 更接近真实 ML 工程——资源是无价的，Agent 必须学会高效利用。

## 4. 操作形态学视角

把 MLE-bench 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到 **MorphBench 在 ML 领域的前身分析**。

### 4.1 MLE-bench 任务在 B 中的映射

MLE-bench 任务对 B 的每个组件都有更高的要求：

| B 组件 | MLE-bench 任务要求 |
|---|---|
| **P (prompt)** | 理解 Kaggle 任务描述、ML 概念、评分标准 |
| **T (tools)** | Python 执行、pip install、文件 I/O、GPU 管理、提交格式 |
| **M (memory)** | 数据 schema、模型架构、超参数、实验历史 |
| **C (code)** | 完整 ML pipeline：数据预处理、特征工程、训练、调优 |

这些要求比 SWE-bench **更高**——Agent 必须管理**完整的 ML 工程流程**，而不是单个 patch。

### 4.2 MLE-bench 与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L2 ReAct Agent**（MLE-bench baseline）：ReAct + Python execution + 提交。MLE-bench ~9%。
- **L3 AIDE**：ReAct + 代码调试 + 实验管理。MLE-bench ~21%。
- **L4 AIDE + M 演化**：M 演化（实验历史管理 + 反思）。MLE-bench ~30%。
- **L5 SICA-style + AIDE**：C 自修改（ML pipeline 自动化）。MLE-bench ~40%+。

MLE-bench 是 L2-L5 Agent 的评测平台，但与 SWE-bench 相比，**L5 Agent 的提升更显著**——因为 ML 任务有"自然的多阶段 pipeline"，C 自修改（pipeline 优化）的收益更大。

### 4.3 MLE-bench 与 H1-H5 的关系

| 假设 | MLE-bench 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | AIDE 比 baseline 提升 ~12% | **支持 H1**（B 自修改有效） |
| **H2 协同演化** | MLE-bench 上 P/M/C 协同优化提升 ~10% | **部分支持 H2** |
| **H3 形态适配** | 不同任务类型（图像/NLP/表格）需要不同 B | **支持 H3** |
| **H4 迁移收益** | 在 Kaggle 任务训练的 B 难以迁移到工业 ML | **有限支持 H4** |
| **H5 治理必要性** | 无验证的自修改可能引入 ML bug | **支持 H5** |

MLE-bench 在 H1、H3 上提供直接证据。H2、H4、H5 需要 MorphBench 提供更系统的验证。

### 4.4 MLE-bench 与 SWE-bench 在 B 修改上的差异

| 维度 | SWE-bench | MLE-bench |
|---|---|---|
| **B 自修改的收益** | 较小（单次 patch） | **较大**（pipeline 优化） |
| **P 自修改的收益** | 中（prompt 优化） | **大**（任务理解优化） |
| **M 自修改的收益** | 小（跨文件依赖） | **大**（实验历史管理） |
| **T 自修改的收益** | 中（工具添加） | **大**（ML 库选择） |
| **C 自修改的收益** | 中（debug 代码） | **大**（pipeline 自动化） |

MLE-bench 的关键优势是：**它的任务结构天然适合 B 自修改**——ML pipeline 有多个阶段（数据、特征、模型、调优），每个阶段都可以自修改。这是 MorphBench 设计需要借鉴的核心特征。

## 5. 实验与结果

### 5.1 主要结果

MLE-bench 的主要实验结果（截至 2024.10）：

| Agent | 铜牌率 | 银牌率 | 金牌率 | 任意奖牌率 |
|---|---|---|---|---|
| GPT-4o (baseline) | 8.0% | 1.3% | 0% | 9.3% |
| Claude 3.5 Sonnet (baseline) | ~12% | ~3% | ~1% | ~16% |
| o1-preview (baseline) | 25.3% | 7.6% | 2.5% | 34.4% |
| AIDE + GPT-4o | 16.9% | 4.5% | 0.7% | 21.1% |
| AIDE + o1-preview | 36.7% | 12.7% | 4.5% | 53.9% |
| AIDE + Claude 3.5 Sonnet | ~25% | ~7% | ~2% | ~34% |

**关键观察**：
- o1-preview 显著优于 GPT-4o——**推理能力强的 LLM 在 ML Agent 上更有效**。
- AIDE 框架显著优于 baseline——**Agent 框架的设计至关重要**。
- 最强组合（AIDE + o1-preview）达到 53.9% 奖牌率——超过 Kaggle 入门选手。

### 5.2 按任务类型的细分

MLE-bench 的 75 个竞赛按类型分布：

| 类型 | 数量 | AIDE + o1-preview 奖牌率 |
|---|---|---|
| 图像分类 | 12 | ~58% |
| 自然语言处理 | 10 | ~60% |
| 时间序列 | 8 | ~50% |
| 表格数据 | 35 | ~52% |
| 推荐系统 | 5 | ~40% |
| 异常检测 | 5 | ~35% |

**关键观察**：
- NLP 任务表现最好——LLM 的"领域优势"。
- 异常检测表现最差——需要深度领域知识。
- 表格数据最多——也是 Kaggle 主流。

### 5.3 消融研究：Agent 框架各组件的贡献

论文对 AIDE 的组件做了消融：

| 配置 | 任意奖牌率 |
|---|---|
| AIDE full | 53.9% |
| - 去掉代码调试 | 41% (-12.9) |
| - 去掉实验历史 | 47% (-6.9) |
| - 去掉超参数调优 | 49% (-4.9) |
| - 去掉特征工程模块 | 50% (-3.9) |
| - 去掉模型选择 | 52% (-1.9) |

**关键观察**：
- **代码调试**是最大贡献项——ML 代码常出错，调试能力至关重要。
- **实验历史**贡献第二大——多次实验后，Agent 必须能从历史中学习。
- **超参数调优**贡献第三——这是 ML 工程的传统挑战。

### 5.4 失败模式分析

MLE-bench 上的失败模式分析：

| 失败模式 | 比例 | 原因 |
|---|---|---|
| **数据预处理错误** | 25% | 数据加载、清洗、特征工程失败 |
| **模型架构错误** | 20% | 模型不适合任务、维度错误 |
| **训练失败** | 20% | GPU OOM、loss 不收敛、超时 |
| **超参数不佳** | 15% | 没找到好的超参数组合 |
| **提交格式错误** | 10% | 提交文件不符合 Kaggle 格式 |
| **循环 / 无进展** | 10% | Agent 在循环中无进展 |

**关键观察**：
- "数据预处理错误"是最大失败模式——这与 M（数据 schema 记忆）相关。
- "训练失败"是第二大失败模式——Agent 不能优雅处理 OOM、超时——这与 T（资源管理工具）相关。
- "循环 / 无进展"是 Agent 范式的常见问题——与 SWE-bench 一致。

### 5.5 与人类 Kaggle 选手的比较

论文将最强 Agent 与人类 Kaggle 选手比较：

| 对手 | 胜率 |
|---|---|
| 入门口选手（铜牌） | ~55% |
| 中等选手（银牌） | ~35% |
| 顶尖选手（金牌） | ~15% |
| 顶级 Kaggle 专家 | ~5% |

**关键观察**：
- Agent 在大多数竞赛上超过**入门选手**——这是 ML 工程自动化的显著进展。
- Agent 仍**远不如顶尖专家**——专家有领域知识、特征工程经验、调参直觉。
- Agent 与**中等选手**接近——这是 AI 的"中级水平"。

## 6. 局限与开放问题

MLE-bench 的局限可以分为六类：**任务覆盖、领域深度、对自修改 Agent 的支持不足、AGI 安全、与 SWE-bench 的协同、与 MorphBench 的差异**。

### 6.1 任务覆盖：仅限 Kaggle

MLE-bench 仅覆盖 Kaggle 竞赛——这不代表 ML Agent 在工业 ML 项目上的表现：

- **Kaggle 数据**：通常是干净、规范的——工业数据是混乱、不完整的。
- **Kaggle 评分**：通常是单一指标——工业 ML 需要多指标平衡（性能、公平性、可解释性）。
- **Kaggle 时间**：通常是 2-3 个月——工业 ML 是长期项目。

未来工作应扩展 MLE-bench 到**工业 ML**——这是 **MLE-bench Industry** 的目标。

### 6.2 领域深度：缺乏 ML 研究任务

MLE-bench 仅覆盖**应用 ML 任务**（如分类、预测），不包括**研究 ML 任务**（如新算法设计、新架构搜索）。但 2024-2025 年出现了多个"AI 自动做 ML 研究"的工作：

- **The AI Scientist**（Lu et al. 2024）：自动撰写 ML 论文。
- **AlphaEvolve**（DeepMind 2025）：自动发现新算法。
- **FunSearch**（Romera-Paredes et al. 2024）：自动发现数学函数。

未来工作应扩展 MLE-bench 到**研究任务**——这是 MLE-bench 演进的方向。

### 6.3 对自修改 Agent 的支持不足

**这是 MLE-bench 与 MorphBench 的关键差异**——与 SWE-bench 一样，MLE-bench **不评估 Agent 自修改 B 的能力**：

- Agent 不能修改自己的 ML pipeline 模板（即使它发现更好的 pipeline 模式）。
- Agent 不能添加新工具（如新的 ML 库调用）。
- Agent 不能修改自己的记忆结构（如实验历史组织）。
- Agent 不能修改自己的执行逻辑（如调试策略）。

SICA、Gödel Agent 等自修改工作在 MLE-bench 上的潜力尚未被系统评估。本书主张：**MorphBench 必须填补这一空白**——专门评估 Agent 在 ML 任务上的 B 自修改能力。

### 6.4 AGI 安全层面

MLE-bench 没有评估 Agent 的 AGI 安全风险：

- **生成恶意模型**：Agent 可能生成包含后门的模型——这些模型在 Kaggle 上表现良好，但在实际部署时被攻击。
- **数据泄露**：Agent 在 Kaggle 上处理数据时可能泄露用户隐私——这一风险在工业场景更严重。
- **资源耗尽**：Agent 在 MLE-bench 上反复训练、反复调优，可能耗尽 GPU 资源。

本书第 22、25 章深入讨论这些 AGI 安全问题。

### 6.5 与 SWE-bench 的协同

MLE-bench 与 SWE-bench 是**互补**而非竞争：

- **SWE-bench**：评测"代码 Agent"——Agent 修改的是项目代码。
- **MLE-bench**：评测"ML Agent"——Agent 修改的是 ML pipeline + 项目代码。

未来可能出现 **SWE-bench + MLE-bench 的联合基准**——同时评测 Agent 的代码能力 + ML 能力。本书第 19 章讨论这一方向。

### 6.6 与 MorphBench 的差异

MLE-bench 与 SWE-bench 类似：**评估外部任务能力，不评估自修改能力**。

| 维度 | MLE-bench | SWE-bench | MorphBench |
|---|---|---|---|
| **任务领域** | ML 工程 | 软件工程 | B 自修改 |
| **任务复杂度** | 高（多次实验） | 中（单次 patch） | 极高（递归修改） |
| **资源消耗** | GPU 重 | CPU 轻 | 中等 |
| **实验迭代** | 多次 | 单次 | 多次（自修改迭代） |
| **评估对象** | 外部任务 | 外部任务 | 内部 B |
| **Agent 等级** | L2-L4 | L2-L5 | L4-L5 |

MorphBench 必须超越 MLE-bench——它必须评估 **Agent 在 ML 任务上的 B 自修改能力**，而非仅仅完成 ML 任务。

### 6.7 开放问题表

| 问题 | MLE-bench 表现 | 本书视角 |
|---|---|---|
| Agent 能完成多少 ML 竞赛？ | 53.9% 奖牌率 | L3-L4 Agent |
| Agent 需要多少次实验？ | 5-20 次 | 取决于任务复杂度 |
| Agent 能跨任务迁移吗？ | 有限 | H4 假设 |
| Agent 能自修改 B 吗？ | 未评估 | MorphBench 必须评估 |
| Agent 能抵御对抗性数据吗？ | 未评估 | 第 22 章对抗鲁棒性 |
| Agent 能优化 ML pipeline 本身吗？ | 未系统评估 | SICA + ML 的融合 |
| Agent 能生成新的 ML 算法吗？ | 未评估 | AlphaEvolve 是开端 |

## 7. 对本书的贡献

MLE-bench 在本书的理论体系中扮演 **MorphBench 在 ML 领域的前身**——它揭示了 ML Agent 的核心能力需求，但**没有评估 Agent 自修改 B 的能力**。

### 7.1 MLE-bench 作为 MorphBench 的设计启发

第 19 章 MorphBench 的设计借鉴 MLE-bench 的几个关键原则：

1. **端到端任务**：MorphBench 的任务覆盖完整流程（5 类环境干预 + 多阶段演化）。
2. **资源感知**：MorphBench 限制 GPU 时间、API 调用次数——这反映真实部署约束。
3. **多 LLM 评测**：MorphBench 在多个 LLM（GPT-4o, Claude 3.5, o1）上评测 Agent。
4. **可重现**：MorphBench 提供完整的评测脚本 + 容器化环境。

但 MorphBench 必须超越 MLE-bench——它必须评估 **Agent 自修改 B 的能力**，而非仅仅完成 ML 任务。

### 7.2 MLE-bench 与 SWE-bench 的协同关系

本书第 19 章提出 **MorphBench 的多领域设计**——整合 SWE-bench + MLE-bench + 其他基准：

| 领域 | 前身基准 | MorphBench 扩展 |
|---|---|---|
| 代码 | SWE-bench | SWE-bench + C 自修改 |
| ML | MLE-bench | MLE-bench + P/M 自修改 |
| 客服 | WebArena | WebArena + P 自修改 |
| 数学 | MATH | MATH + P 自修改 |
| 通用 | AgentBench | AgentBench + B 全修改 |

MLE-bench 与 SWE-bench 共同构成 MorphBench 的**任务基础**——它们是 MorphBench 的"前身"。

### 7.3 MLE-bench 在本书章节中的位置

| 章节 | 与 MLE-bench 的关系 |
|---|---|
| **Ch 13 工具与函数调用** | AIDE 的工具调用设计 |
| **Ch 14 长期记忆** | 实验历史管理 = M 自演化 |
| **Ch 15 自编辑代码** | ML pipeline 自修改 = C 自修改 |
| **Ch 17 元控制器 U** | MLE-bench 上跑的自修改 Agent = U 的实证 |
| **Ch 19 评测基准** | MLE-bench = 外部任务评估的代表 |
| **Ch 21 MorphBench** | MorphBench = ML 领域自修改评估的新基准 |

MLE-bench 是本书"评测"部分（Ch 19）的核心案例，也是 MorphBench 的设计依据之一。

### 7.4 MLE-bench 与具体工作的关系

| 工作 | 在 MLE-bench 上的表现 | 对 MorphBench 的启发 |
|---|---|---|
| GPT-4o baseline | 9.3% | 简单 Agent 能力有限 → MorphBench 必须避免过于简单 |
| o1-preview | 34.4% | 推理能力关键 → MorphBench 应支持推理 LLM |
| AIDE + o1-preview | 53.9% | Agent 框架设计关键 → MorphBench 应支持多框架 |
| AlphaEvolve（推测） | 60-70% | 演化算法有效 → MorphBench 可集成演化派 |
| SICA + ML（未来） | 未知 | C 自修改有效 → MorphBench 必须评估 C 自修改 |

这些工作的 MLE-bench 表现为 MorphBench 的设计提供了具体的参考点——每个工作都揭示了某种 B 自修改模式的优劣。

### 7.5 给读者的关键启示

1. **MLE-bench 是 ML Agent 的"入门级试金石"**：不是 ML 研究，而是 ML 工程应用。Agent 在 MLE-bench 上的表现反映其处理"多次实验 + 资源受限 + 完整流程"的能力。
2. **AIDE + 强 LLM = 当前 SOTA**：53.9% 奖牌率显示 Agent 框架设计 + LLM 推理能力是关键组合。未来的突破可能来自"自演化 + 强推理 + 多 Agent"。
3. **MLE-bench 不评估自修改 B 的能力**：与 SWE-bench 一样，MLE-bench 只评估外部任务能力。MorphBench 必须填补"自修改 B 评估"的空白。
4. **ML 任务天然适合 B 自修改**：ML pipeline 有多个阶段（数据、特征、模型、调优），每个阶段都可以自修改。MorphBench 在 ML 领域的设计应充分利用这一特征。
5. **Agent 在 ML 上的安全风险被低估**：MLE-bench 上的 Agent 可以生成包含后门的模型——这一风险在工业场景更严重。MorphBench 必须包含 ML 安全评估。

MLE-bench 是本书"评测基准"部分（第 19 章）的核心案例之一，与 SWE-bench 共同构成 **"代码 + ML"双基准**。它代表了 2024 年 LLM Agent 评测从"代码生成"扩展到"完整 ML 工程"的趋势——**多阶段、多次实验、资源受限**是 ML Agent 的核心特征。

但 MLE-bench 不是终点——它不评估"Agent 自修改 B 的能力"。MorphBench 是 MLE-bench 在"自修改评估"方向的扩展——它在 MLE-bench 的基础上增加"Agent 在 ML 任务上自修改 B 的能力评估"，让 LLM Agent 评测从"完成 ML 任务"扩展到"自演化完成 ML 任务"。

理解 MLE-bench 是理解 MorphBench 在 ML 领域设计的前提——MLE-bench 揭示了 ML Agent 的核心特征（多次实验、资源受限、完整 pipeline），MorphBench 在此基础上增加"自修改评估"。两者共同构成 LLM Agent 评测在 ML 领域的完整图谱。

## 参考文献

- chan2024mlebench: Chan, J. S., Chowdhury, N., Jaffe, O., et al. (2024). *MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering*. ICLR 2024. arXiv:2410.07095. OpenAI. [$TRAE_REF](https://arxiv.org/abs/2410.07095)
- wijk2024aide: Wijk, H., et al. (2024). *AIDE: AI-Driven Exploration in the Space of Code*. OpenAI / MLE-bench 团队开源的 Agent 框架。
- jimenez2024swebench: Jimenez, C. E., et al. (2024). *SWE-bench*. 见 r-paper-013。（MLE-bench 的姊妹基准）
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA*. 见 r-paper-006。（SICA 在 MLE-bench 上的应用前景）
- yin2024godelagent: Yin, S., et al. (2024). *Gödel Agent*. 见 r-paper-007。（Gödel Agent 在 MLE-bench 上的应用前景）
- lu2024aiscientist: Lu, C., et al. (2024). *The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery*. Sakana AI. arXiv:2408.06292.（AI 自动做 ML 研究）
- romera2024funsearch: Romera-Paredes, B., et al. (2024). *Mathematical Discoveries from Program Search with Large Language Models* (FunSearch). Nature 625: 468-475.（AI 自动发现新算法）
- fang2025selfevolving: Fang, W., et al. (2025). *Self-Evolving Agents Survey*. 见 r-paper-009。
- yao2023react: Yao, S., et al. (2023). *ReAct*. 见 r-paper-001。
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT*. 见 r-paper-004。（MemGPT 在 MLE-bench 上的应用前景：实验历史管理）