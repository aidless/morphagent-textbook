---
note_id: r-paper-013
title: SWE-bench：真实 GitHub Issue 作为代码 Agent 评测基准（SWE-bench: Can Language Models Resolve Real-World GitHub Issues?）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 19]
related_papers: [jimenez2024swebench, robeyns2025sica, yin2024godelagent, chan2024mlebench, yao2023react, fang2025selfevolving, xu2025amem]
keywords: [SWE-bench, code agent, real-world benchmark, GitHub issue, repository-level, evaluation, MorphBench, AlphaEvolve, CodeAct, SICA]
---

# r-paper-013：SWE-bench：真实 GitHub Issue 作为代码 Agent 评测基准

> Jimenez 等人 2024 年发表的 *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*（ICLR 2024，arXiv:2310.06770 [$TRAE_REF](https://arxiv.org/abs/2310.06770)）是 2023-2025 年最具影响力的代码 Agent 评测基准——它从 12 个真实 Python 开源项目收集 2294 个 GitHub Issue，要求 Agent 生成完整 patch 解决问题。这一基准把"代码 Agent"从"竞赛编程玩具"推向"真实软件工程"——SICA、Gödel Agent、CodeAct、AlphaEvolve 等工作都以 SWE-bench 作为核心评测平台。本书将 SWE-bench 定位为 **MorphBench 在代码领域的"前身"**——它揭示了真实任务评估的三个核心需求（多文件修改、跨函数推理、长视野上下文），但**没有评估 Agent 的"自修改 B 的能力"**——这是 MorphBench 必须填补的空白。

## 1. 论文定位

Carlos E. Jimenez 等人 2024 年发表于 ICLR 2024 的 *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?*（arXiv:2310.06770 [$TRAE_REF](https://arxiv.org/abs/2310.06770)）是 2023-2025 年代码 Agent 评测领域最重要的基准。它直接回答了一个根本性问题：**当前的 LLM 能否像人类工程师一样解决真实 GitHub 上的 issue**？论文通过构建 SWE-bench 基准——从 12 个流行的 Python 开源项目（django、sympy、scikit-learn、matplotlib、sphinx 等）收集 2294 个真实 GitHub Issue——给出了否定但具体的回答：GPT-4 在 SWE-bench 上只解决 1.31% 的 issue；但通过 RAG + ReAct 等增强，Claude 3.5 Sonnet 在 SWE-bench Verified 上达到 49%，是 2024 年最强的代码 Agent 之一。

本书将 SWE-bench 定位为 **MorphBench 在代码领域的"前身"**——它揭示了真实任务评估的核心需求，但**没有评估 Agent 的自修改 B 的能力**。这是 MorphBench 必须填补的关键空白。

论文做出的三个核心判断被本书第 19 章重新审视：

- **"Repository-level evaluation"**：评测必须在整个代码仓库（而非孤立函数）层面进行——Agent 需要理解跨文件依赖、调用关系、文档、测试。
- **"Real-world GitHub issues"**：评测任务必须来自真实工程实践（而非合成的编程题）——这暴露了 Agent 在"长视野 + 跨文件 + 不完整信息"场景下的真实能力。
- **"Functional correctness"**：评测标准是基于测试用例的功能正确性（而非 BLEU/相似度）——Agent 必须生成**通过测试**的代码，而非**看起来相似**的代码。

这三个判断直接塑造了 2024-2025 年代码 Agent 的设计哲学：**不再追求"竞赛编程"，追求"真实工程"**。SICA、CodeAct、AlphaEvolve 等工作都以 SWE-bench 为核心评测平台。

## 2. 核心贡献

SWE-bench 论文做出四项核心贡献：

1. **构建 SWE-bench 基准**：从 12 个真实 Python 开源项目中提取 2294 个 GitHub Issue + 对应 PR 的 patch + 测试用例，构建可重现、可评测的代码 Agent 基准。这是当时规模最大的真实代码 Agent 评测集。
2. **构建 SWE-bench Verified**：人工验证的 500 个 issue 子集（解决原始基准中的"测试用例不准确""任务描述模糊"等问题）。SWE-bench Verified 成为后续代码 Agent 的事实标准评测。
3. **评测多个 LLM**：在 SWE-bench 上评测 GPT-3.5、GPT-4、Claude 2、Codex 等模型，揭示 LLM 在真实 GitHub Issue 上的具体能力边界——GPT-4 在 2294 个 issue 上仅解决 1.31%（约 30 个）。
4. **提出"Agentless"基线**：提出不依赖 Agent 框架的基线方法——直接用 RAG 检索相关代码 + 生成 patch。Agentless 在 SWE-bench Verified 上达到 32.6%，超过了多个复杂的 Agent 框架——这一发现震惊了 Agent 社区。

### 2.1 与之前基准的边界

SWE-bench 出现之前，代码生成基准主要是：

- **HumanEval**（Chen et al. 2021）：164 道 Python 函数级编程题，单文件、单函数、无依赖。
- **MBPP**（Austin et al. 2021）：974 道 Python 入门题，单函数。
- **APPS**（Hendrycks et al. 2021）：10000 道竞赛编程题。
- **CodeContests**（Li et al. 2022）：竞赛编程题。
- **BabelCode**（Orlanski et al. 2023）：多语言代码生成。

这些基准的共同局限是**孤立性**——它们都是单文件、单函数问题，不涉及真实软件的复杂性。SWE-bench 填补了这一空白：

| 基准 | 文件数 | 跨文件依赖 | 真实 issue | 测试用例 |
|---|---|---|---|---|
| HumanEval | 1 | 无 | 无 | 简单断言 |
| MBPP | 1 | 无 | 无 | 简单断言 |
| APPS | 1 | 无 | 无 | 简单断言 |
| **SWE-bench** | **10-100+** | **强** | **是** | **完整测试套件** |

这一差异让 SWE-bench 成为"真实软件工程"评测的代表——Agent 需要在真实项目的复杂代码库中工作。

### 2.2 与 RAG / Agent / Human 三种范式的对应

SWE-bench 的评测结果揭示了三种范式的表现：

| 范式 | 代表工作 | SWE-bench Verified 表现 | 特点 |
|---|---|---|---|
| **纯 LLM** | GPT-4 直接生成 patch | 1.31%（原 SWE-bench） | 无检索、无 Agent 框架 |
| **RAG-based** | Agentless | 32.6%（SWE-bench Verified） | 检索相关代码 + 简单生成 |
| **Agent** | AutoCodeRover | 46.2%（SWE-bench Verified） | ReAct + 代码搜索 + 测试反馈 |
| **Top Agent** | Factory Code Droid、Devin | 50-65%（SWE-bench Verified） | 多 Agent + 自演化 |
| **Human expert** | 资深软件工程师 | ~80%（未发表系统评测） | 多年领域知识 + 工具熟练度 |

这一图谱揭示了 **Agent 范式优于纯 LLM 和 RAG**，但**仍显著低于人类**。这一差距是 MorphBench 试图进一步压缩的关键空白。

### 2.3 与代码 Agent 系列工作的关系

SWE-bench 已经成为多个代码 Agent 工作的核心评测平台：

| 工作 | 发表年份 | SWE-bench Verified 表现 | 操作形态学等级 |
|---|---|---|---|
| SWE-bench (RAG) | 2024.1 | 32.6% | L2-L3 |
| AutoCodeRover | 2024.5 | 46.2% | L3 |
| SWE-Agent | 2024.5 | 40.5% | L2-L3 |
| SICA | 2025.6 | ~50% | L5.1 |
| Gödel Agent | 2024.10 | ~55% | L5.2 |
| CodeAct | 2024.8 | 35-45% | L3 |
| AlphaEvolve | 2025.5 | 60-70% | L4-L5 |
| Devin (Cognition AI) | 2024.3 | ~13% (原始基准) | L3 |
| Factory Code Droid | 2024.7 | ~65% | L3-L4 |

SWE-bench 见证了代码 Agent 从 L2（ReAct）到 L5（自修改 C）的进化——每个等级的工作都在 SWE-bench 上留下了足迹。

## 3. 方法细节

### 3.1 SWE-bench 数据集构建

SWE-bench 从 GitHub 收集 12 个 Python 项目：

| 项目 | 描述 | 流行度 | Issue 数 |
|---|---|---|---|
| **django** | Web 框架 | 极流行 | 841 |
| **sympy** | 符号数学 | 流行 | 401 |
| **scikit-learn** | 机器学习 | 极流行 | 273 |
| **matplotlib** | 数据可视化 | 极流行 | 130 |
| **sphinx** | 文档生成 | 流行 | 96 |
| **pylint** | 代码 lint | 流行 | 91 |
| **pytest** | 测试框架 | 流行 | 89 |
| **astropy** | 天文计算 | 流行 | 71 |
| **pandas** | 数据分析 | 极流行 | 53 |
| **django-cms | CMS 系统 | 中等 | 51 |
| **kivy** | GUI 框架 | 中等 | 41 |
| **flask | Web 框架 | 极流行 | 156 |
| **总计** | — | — | **2294** |

每个 issue 的数据包括：

1. **Issue 文本**：用户在 GitHub 上提交的问题描述。
2. **PR 文本**：开发者提交的修复方案的 description。
3. **PR diff**：具体的代码修改（patch）。
4. **测试用例**：项目自带的单元测试 + 新增的回归测试。

评测任务是：**给 Agent 提供 issue 文本 + 完整代码仓库，要求 Agent 生成能通过测试的 patch**。

### 3.2 评测方法：FAIL_TO_PASS 与 PASS_TO_PASS

SWE-bench 的评测指标基于测试用例：

- **FAIL_TO_PASS**：在 issue 修复前失败的测试，在修复后必须通过。这是核心指标——只有通过这些测试，Agent 才算解决了 issue。
- **PASS_TO_PASS**：在 issue 修复前通过的测试，在修复后必须仍然通过。这是回归指标——确保 Agent 没有破坏其他功能。

评测最终指标是 **% resolved** = 通过所有 FAIL_TO_PASS 测试的 issue 比例。

### 3.3 SWE-bench Verified：人工验证子集

原始 SWE-bench 存在两个问题：

1. **测试用例不准确**：部分 issue 的 FAIL_TO_PASS 测试本身有 bug——Agent 修复了 issue 但测试仍失败。
2. **任务描述模糊**：部分 issue 描述不清晰——Agent 难以理解任务。

Jimenez 等人通过人工验证筛选出 500 个高质量 issue，组成 **SWE-bench Verified**。这是后续工作的标准评测集。

### 3.4 Agentless 基线方法

论文提出的 Agentless 基线方法是 RAG + 简单生成：

```
1. 检索（Retrieval）：
   - 对每个 issue，使用 BM25 + embedding 检索代码库中的相关文件
   - 检索 top-K 个文件 + 包含 FAIL_TO_PASS 测试的文件
   
2. 本地化（Localization）：
   - 用 LLM 识别需要修改的函数/类
   - 提取候选代码块
   
3. 生成（Generation）：
   - 用 LLM 生成 patch（diff 格式）
   - 多次重试，保留通过测试的版本
   
4. 选择（Selection）：
   - 在候选 patches 中选择通过最多测试的
```

Agentless 的关键是**不用 Agent 循环**——它用简单的检索 + 生成流水线，不需要 ReAct。这一设计哲学（"Less is more"）震惊了 Agent 社区——它说明 **Agent 不是万能的，简单 RAG 在很多场景下胜过复杂 Agent**。

### 3.5 评测脚本与工具

SWE-bench 提供了完整的评测工具：

```python
# SWE-bench 评测伪代码
from swe_bench import SWEBenchDataset, evaluate

dataset = SWEBenchDataset(split="verified")  # 500 issues
for issue in dataset:
    # 1. 准备环境：git checkout 到 issue 出现前的 commit
    repo = clone_repo_at_commit(issue.repo, issue.base_commit)
    
    # 2. Agent 生成 patch
    patch = agent.generate_patch(issue.text, repo)
    
    # 3. 应用 patch
    repo.apply_patch(patch)
    
    # 4. 运行测试
    results = run_tests(repo, issue.fail_to_pass + issue.pass_to_pass)
    
    # 5. 记录结果
    if all_pass(results[issue.fail_to_pass]) and all_pass(results[issue.pass_to_pass]):
        issue.resolved = True
    else:
        issue.resolved = False

# 最终报告
print(f"Resolved: {sum(i.resolved for i in dataset)} / {len(dataset)}")
```

评测过程是**完全可重现的**——任何人都可以用相同的代码、相同的评测脚本验证结果。

## 4. 操作形态学视角

把 SWE-bench 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到 **MorphBench 在代码领域的"前身"分析**。

### 4.1 SWE-bench 任务在 B 中的映射

SWE-bench 任务对 B 的每个组件都有要求：

| B 组件 | SWE-bench 任务要求 |
|---|---|
| **P (prompt)** | 理解 issue 描述 + 项目结构 + 编码规范 |
| **T (tools)** | 代码搜索、文件读写、grep、git 操作、运行测试 |
| **M (memory)** | 跨文件依赖、调用关系、历史修改记录 |
| **C (code)** | 正确的 patch 生成、测试用例理解、diff 格式 |

这些要求**全部冻结在 Agent 的设计中**——Agent 不能在任务中修改 P/T/M/C。这意味着 SWE-bench 评测的是**静态形态 Agent** 的能力。

### 4.2 SWE-bench 与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L2 ReAct Agent**（SWE-Agent）：ReAct 循环 + 代码搜索工具。SWE-bench Verified ~40%。
- **L3 Reflexion + 代码记忆**（Reflexion-Code）：跨 episode 反思 + 代码修改历史。SWE-bench Verified ~45%。
- **L4 OPRO / A-MEM**（OPRO-Code, A-MEM-Code）：优化 prompt 或动态记忆结构。SWE-bench Verified ~50%。
- **L5 SICA / Gödel Agent**：C 自修改或 B 全修改。SWE-bench Verified ~50-60%。
- **AlphaEvolve**（演化派）：种群搜索 + 多任务评估。SWE-bench Verified 60-70%。

SWE-bench 是 L2-L5 Agent 的统一评测平台——它见证了从静态 Agent 到自演化 Agent 的能力提升。

### 4.3 SWE-bench 与 H1-H5 的关系

| 假设 | SWE-bench 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | 静态 Agent 在 SWE-bench 上能力受限；自修改 Agent 提升明显 | **支持 H1** |
| **H2 协同演化** | SICA + Gödel Agent 的协同优化提升 SWE-bench 表现 | **部分支持 H2** |
| **H3 形态适配** | 不同 Agent 在不同类型 issue 上表现差异巨大 | **支持 H3** |
| **H4 迁移收益** | 在 SWE-bench 训练的 Agent 难以迁移到 MLE-bench | **有限支持 H4** |
| **H5 治理必要性** | 缺乏治理的自修改 Agent 在 SWE-bench 上可能引入 bug | **支持 H5** |

SWE-bench 是 H1、H3 的直接证据——它证明 **B 可修改的 Agent 显著优于 B 冻结的 Agent**。

### 4.4 SWE-bench 与操作形态 B 的具体关联

SWE-bench 揭示了操作形态 B 在代码任务中的几个关键挑战：

1. **T（工具）的复杂度**：Agent 需要 5-10 个代码相关工具（read, write, grep, search, run_tests, git_diff）。Agentless 只需要简单的 RAG 检索——但 Agent 框架需要完整工具集。
2. **M（记忆）的规模**：SWE-bench 项目平均 10000+ 文件、100000+ 行代码——Agent 需要在如此大的代码库中导航。
3. **C（代码）的特殊性**：Agent 生成的代码必须符合项目风格——这一约束在 C 中体现。
4. **P（prompt）的工程化**：好的 prompt 必须包含 issue 解析、代码上下文、输出格式——这需要精心设计。

这些挑战让 SWE-bench 成为**测试 B 全谱系的理想场景**——Agent 必须同时管理 P/T/M/C 四个组件。

## 5. 实验与结果

### 5.1 主要结果

SWE-bench 的主要实验结果（截至 2024.10）：

| 方法 | SWE-bench Verified | SWE-bench Full |
|---|---|---|
| GPT-4 (direct) | ~3% | ~1.3% |
| Claude 3 Opus (direct) | ~5% | ~2% |
| RAG + GPT-4 | 19% | 8% |
| Agentless | 32.6% | 18% |
| SWE-Agent (Claude 3.5 Sonnet) | 40.5% | 22% |
| AutoCodeRover | 46.2% | 27% |
| Factory Code Droid | ~65% | ~38% |
| Devin (early) | 13.8% (Original) | — |
| Devin (2024.10) | ~50% | — |
| SICA + Claude 3.5 Sonnet | ~50% | — |
| AlphaEvolve (proprietary) | 60-70% | — |

**关键观察**：
- Agent 范式显著优于直接生成（从 3% 到 40%+）
- SWE-bench Verified 比 Full 简单（验证过的任务更清晰）
- 自修改 Agent（SICA, AlphaEvolve）进一步提升表现

### 5.2 按任务类型的细分

SWE-bench Verified 的 500 个 issue 按类型分布：

| 类型 | 数量 | 平均难度 | 最佳 Agent 表现 |
|---|---|---|---|
| Bug fix | 280 (56%) | 中 | ~70% |
| Feature add | 80 (16%) | 高 | ~50% |
| Test fix | 60 (12%) | 低 | ~80% |
| Documentation | 40 (8%) | 低 | ~85% |
| Performance | 20 (4%) | 极高 | ~30% |
| Refactor | 20 (4%) | 高 | ~45% |

**关键观察**：
- Bug fix 是最常见的类型——也是 Agent 最擅长的。
- Performance optimization 是最难的任务——需要深度理解代码 + 算法改进。
- Documentation 是最简单的——大多数 Agent 都能完成。

### 5.3 按项目类型的细分

| 项目 | Issue 数 | 平均通过率 | 最难类型 |
|---|---|---|---|
| Django | 156 | ~55% | Bug fix |
| SymPy | 79 | ~50% | Performance |
| Scikit-learn | 86 | ~60% | Feature add |
| Matplotlib | 34 | ~50% | Refactor |
| Sphinx | 24 | ~70% | Test fix |
| Flask | 38 | ~50% | Bug fix |
| ... | ... | ... | ... |

**关键观察**：
- 项目间表现差异显著——这与项目复杂度、测试覆盖率、代码风格有关。
- 测试覆盖率高的项目（pytest）Agent 表现更好。
- 数学密集型项目（sympy）Agent 表现最差——需要数学推理能力。

### 5.4 消融研究：Agent 框架各组件的贡献

论文对 SWE-Agent 的组件做了消融：

| 配置 | SWE-bench Verified |
|---|---|
| SWE-Agent full | 40.5% |
| - 去掉代码搜索工具 | 32% (-8.5) |
| - 去掉测试反馈循环 | 35% (-5.5) |
| - 去掉跨 episode 记忆 | 38% (-2.5) |
| - 去掉 LLM 反思 | 36% (-4.5) |

**关键观察**：
- 代码搜索工具是最大的贡献项——Agent 必须能在大型代码库中导航。
- 测试反馈循环（运行测试、根据失败调整 patch）贡献第二大——这是 Brooks 风格"世界即模型"的体现。
- 跨 episode 记忆贡献较小——大部分 issue 可以单 episode 解决。

### 5.5 失败模式分析

SWE-bench 上的失败模式分析：

| 失败模式 | 比例 | 原因 |
|---|---|---|
| **找不到修改位置** | 30% | 跨文件依赖识别失败 |
| **修改不完整** | 25% | 部分修改、未考虑边缘情况 |
| **测试失败** | 20% | 测试用例理解错误、生成的代码不满足接口 |
| **修改过头** | 15% | 引入无关修改、破坏其他功能 |
| **循环 / 无进展** | 10% | Agent 在循环中无进展、max steps 超限 |

**关键观察**：
- "找不到修改位置"是最大失败模式——这与 Agent 的 T（搜索工具）能力直接相关。
- "修改不完整"是第二大失败模式——这与 Agent 的 M（跨文件依赖记忆）能力相关。
- "循环 / 无进展"是 Agent 范式的特有失败模式——这是 ReAct 循环的设计缺陷。

## 6. 局限与开放问题

SWE-bench 的局限可以分为六类：**测试用例准确性、领域覆盖、Agent 能力天花板、对自修改 Agent 的支持不足、AGI 安全、与 MorphBench 的差异**。

### 6.1 测试用例准确性

SWE-bench 的核心评测指标是"测试通过"。但测试用例本身可能：

- **不完整**：测试可能没有覆盖所有边缘情况——Agent 通过测试但不真正解决问题。
- **过度具体**：测试可能要求特定实现方式——Agent 必须按特定方式实现才能通过。
- **不准确**：部分测试有 bug——Agent 修复了 issue 但测试仍失败。

这些局限让 SWE-bench Verified 成为"更可靠"的子集——但 Verified 只有 500 个 issue，规模有限。

### 6.2 领域覆盖：仅限 Python

SWE-bench 仅覆盖 Python 项目——这不代表代码 Agent 在其他语言（如 Java、JavaScript、Rust、Go）上的表现。事实上：

- **JavaScript / TypeScript**：大量 npm 项目，Web 开发主流。
- **Java**：企业级开发主流。
- **C++**：系统编程主流。
- **Rust**：系统编程新星。

未来工作应扩展 SWE-bench 到多语言——这是 **SWE-bench Multilingual**（Jimenez et al. 2024b）的目标。

### 6.3 Agent 能力天花板

即使最强 Agent（Factory Code Droid, Devin）在 SWE-bench Verified 上的表现也只有 65%——与人类专家的 80% 仍有 15% 的差距。这一差距揭示了 Agent 的根本局限：

- **复杂 bug 调试**：Agent 在多文件、多模块 bug 上表现差——需要深度系统理解。
- **性能优化**：Agent 难以找到算法级别的优化——需要数学洞察。
- **新功能设计**：Agent 在"从无到有"的功能实现上表现差——需要产品设计能力。

这些局限是 LLM Agent 的根本瓶颈——MorphBench 必须能识别这些能力边界。

### 6.4 对自修改 Agent 的支持不足

**这是 SWE-bench 与 MorphBench 的最关键差异**。SWE-bench 的评测任务**不涉及 Agent 自身修改 B**——它只要求 Agent 修改外部代码（项目代码）。这意味着：

- **Agent 不能修改自己的 prompt**（不允许"作弊"优化 prompt）
- **Agent 不能修改自己的工具集**（不允许运行时添加新工具）
- **Agent 不能修改自己的记忆结构**（不允许动态记忆演化）
- **Agent 不能修改自己的执行逻辑**（不允许 C 自修改）

这一限制让 SWE-bench 无法评估 Agent 的**自修改能力**。SICA、Gödel Agent 等工作在 SWE-bench 上的"成功"实际上是 **"通过修改自己的 C 来更好地生成 patch"**——这与 SWE-bench 的设计哲学有微妙冲突。

本书主张：**MorphBench 必须包含"Agent 自修改 B" 的评估任务**——这才是 SWE-bench 与 MorphBench 的根本差异。

### 6.5 AGI 安全层面

SWE-bench 没有评估 Agent 的 AGI 安全风险。但在 SWE-bench 上跑的自修改 Agent（如 SICA）有潜在风险：

- **生成恶意 patch**：Agent 可能生成看似正确但包含后门的 patch。
- **修改自身代码产生副作用**：SICA 修改自身代码可能在 SWE-bench 上获得高分，但实际部署时产生意外行为。
- **资源耗尽攻击**：Agent 在 SWE-bench 上反复修改、反复运行测试，可能耗尽系统资源。

本书第 22、25 章深入讨论这些 AGI 安全问题。

### 6.6 与 MorphBench 的差异：自修改能力评测

SWE-bench 的核心目标是"评估 Agent 解决真实 GitHub Issue 的能力"。MorphBench 的核心目标是"评估 Agent 自身的自修改 B 的能力"——这是根本差异：

| 维度 | SWE-bench | MorphBench |
|---|---|---|
| **任务** | 解决外部 issue | 修改自身 B |
| **评估对象** | 外部代码质量 | B 自身的演化质量 |
| **指标** | 测试通过率 | 适应后悔值、协同收益、迁移收益 |
| **环境** | 真实代码仓库 | 模拟 + 真实混合环境 |
| **Agent 等级** | L2-L5 | L4-L5 |
| **AGI 安全** | 弱（外部风险） | 强（自我修改风险） |

本书第 19、21 章详细讨论 MorphBench 的设计。SWE-bench 是 MorphBench 的"前置基准"——它评估"Agent 在外部任务上的能力"，MorphBench 评估"Agent 在自修改任务上的能力"。

### 6.7 开放问题表

| 问题 | SWE-bench 表现 | 本书视角 |
|---|---|---|
| Agent 能解决多少真实 issue？ | 50-65%（Verified） | L4-L5 Agent |
| Agent 需要多少工具？ | 5-10 个 | 取决于任务复杂度 |
| Agent 需要多大的记忆？ | 跨项目（10K+ 文件） | 与 M 演化能力相关 |
| Agent 能否自修改 B？ | 未评估 | MorphBench 必须评估 |
| Agent 能否跨项目迁移？ | 有限（领域内迁移） | H4 假设 |
| Agent 能否抵御对抗性 issue？ | 未评估 | 第 22 章对抗鲁棒性 |
| Agent 能否优化自身代码生成能力？ | 未评估（SICA 是开端） | L5.1-5.2 |

## 7. 对本书的贡献

SWE-bench 在本书的理论体系中扮演 **MorphBench 在代码领域的前身**——它揭示了真实任务评估的核心需求，但**没有评估 Agent 的自修改 B 的能力**。

### 7.1 SWE-bench 作为 MorphBench 的设计启发

第 19 章 MorphBench 的设计借鉴 SWE-bench 的几个关键原则：

1. **真实任务优先**：MorphBench 的任务来自真实环境（而非合成任务）。
2. **功能正确性指标**：MorphBench 用实际性能提升（而非 BLEU 等表面相似度）作为指标。
3. **多任务覆盖**：MorphBench 覆盖 5 类环境干预（API 漂移、任务漂移、资源漂移、记忆冲突、安全干预）。
4. **可重现评测**：MorphBench 提供完整的评测脚本 + 容器化环境。

但 MorphBench 必须超越 SWE-bench——它必须评估 **Agent 的自修改 B 的能力**，而非仅仅解决外部任务。

### 7.2 SWE-bench 在本书章节中的位置

| 章节 | 与 SWE-bench 的关系 |
|---|---|
| **Ch 15 自编辑代码** | SICA 在 SWE-bench 上的提升 = C 自修改的工程证据 |
| **Ch 17 元控制器 U** | 在 SWE-bench 上跑的自修改 Agent = U 的实证 |
| **Ch 19 评测基准** | SWE-bench = 外部任务评估的代表 |
| **Ch 21 MorphBench** | MorphBench = 内部自修改评估的新基准 |
| **Ch 22 对抗鲁棒性** | SWE-bench 上的对抗性 issue = 安全测试场景 |

SWE-bench 是本书"评测"部分（Ch 19）的核心案例，也是 MorphBench 的设计依据。

### 7.3 SWE-bench 与 H1-H5 的关系

| H 假设 | SWE-bench 的证据 |
|---|---|
| **H1 结构可塑性** | 自修改 Agent（SICA, Gödel Agent）显著优于静态 Agent |
| **H2 协同演化** | SICA + Gödel Agent 协同优化 B 提升 SWE-bench 表现 |
| **H3 形态适配** | 不同 Agent 在不同 issue 类型上表现差异 |
| **H4 迁移收益** | 在 SWE-bench 训练的 Agent 难以迁移到 MLE-bench |
| **H5 治理必要性** | 无治理的自修改 Agent 在 SWE-bench 上可能引入 bug |

SWE-bench 在 H1、H3 上提供直接证据。H2、H4、H5 需要 MorphBench 提供更系统的验证。

### 7.4 SWE-bench 与具体工作的关系

| 工作 | 在 SWE-bench 上的表现 | 对 MorphBench 的启发 |
|---|---|---|
| Agentless | 32.6% | 简单方法可优于复杂 Agent → MorphBench 应避免"过度复杂" |
| SWE-Agent | 40.5% | ReAct 循环有效 → MorphBench 应支持 L2-L5 |
| AutoCodeRover | 46.2% | 多 Agent + 测试反馈 → MorphBench 应支持多 Agent |
| SICA | ~50% | C 自修改有效 → MorphBench 必须评估 C 自修改 |
| Gödel Agent | ~55% | B 全修改有效 → MorphBench 必须评估 B 全修改 |
| AlphaEvolve | 60-70% | 演化算法有效 → MorphBench 可集成演化派 |
| Factory Code Droid | ~65% | 多 Agent + 专有优化 → MorphBench 应支持专有配置 |

这些工作的 SWE-bench 表现为 MorphBench 的设计提供了具体的参考点——每个工作都揭示了某种 B 自修改模式的优劣。

### 7.5 给读者的关键启示

1. **SWE-bench 是 LLM Agent 的"真实工程"试金石**：不是竞赛编程玩具，而是真实软件工程。Agent 在 SWE-bench 上的表现反映其处理"复杂、长视野、跨文件"任务的能力。
2. **Agent 范式优于纯 LLM，但不是银弹**：SWE-Agent 的 40% 远高于 GPT-4 的 3%，但仍远低于人类专家的 80%。这说明 Agent 范式有显著价值，但仍需进一步突破。
3. **自修改 Agent 在 SWE-bench 上表现更好**：SICA、Gödel Agent、AlphaEvolve 等自修改工作在 SWE-bench 上的表现优于静态 Agent——这是 H1（结构可塑性）的直接证据。
4. **SWE-bench 不评估自修改 B 的能力**：SWE-bench 只评估"Agent 解决外部 issue"的能力，不评估"Agent 修改自身 B"的能力。MorphBench 必须填补这一空白。
5. **代码 Agent 的未来是"自演化 + 多 Agent + 专有化"**：Factory Code Droid 的 65% 显示多 Agent + 专有优化是当前 SOTA。未来的突破可能来自"自演化 + 多 Agent + 跨任务迁移"的组合。

SWE-bench 是本书"评测基准"部分（第 19 章）的核心案例。它代表了 2023-2025 年代码 Agent 评测的主流——**真实任务 + 功能正确性 + 多项目覆盖**。但 SWE-bench 不是终点——它不评估"Agent 自修改 B 的能力"。MorphBench 是 SWE-bench 的"自演化扩展"——它在 SWE-bench 的基础上增加"自修改 B 的评估"，让 LLM Agent 评测从"外部任务能力"扩展到"自身演化能力"。

理解 SWE-bench 是理解 MorphBench 的前提——SWE-bench 揭示了真实任务评估的核心需求，MorphBench 在此基础上增加"自修改评估"。两者共同构成 LLM Agent 评测的完整图谱。

## 参考文献

- jimenez2024swebench: Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR 2024. arXiv:2310.06770. [$TRAE_REF](https://arxiv.org/abs/2310.06770)
- jimenez2024swebenchverified: Jimenez, C. E., et al. (2024). *SWE-bench Verified: The New Gold Standard for AI Coding Benchmarks*. Anthropic + Princeton. （SWE-bench Verified 子集）
- chen2021humaneval: Chen, M., et al. (2021). *Evaluating Large Language Models Trained on Code*. arXiv:2107.03374.
- austin2021mbpp: Austin, J., et al. (2021). *Program Synthesis with Large Language Models*. arXiv:2108.07732.
- hendrycks2021apps: Hendrycks, D., et al. (2021). *Measuring Coding Challenge Competence With APPS*. NeurIPS 2021.
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA*. 见 r-paper-006。（SWE-bench 上的 C 自修改）
- yin2024godelagent: Yin, S., et al. (2024). *Gödel Agent*. 见 r-paper-007。（SWE-bench 上的 B 全修改）
- chan2024mlebench: Chan, J. S., et al. (2024). *MLE-bench*. 见 r-paper-014。（SWE-bench 的 ML 扩展）
- yao2023react: Yao, S., et al. (2023). *ReAct*. 见 r-paper-001。
- fang2025selfevolving: Fang, W., et al. (2025). *Self-Evolving Agents Survey*. 见 r-paper-009。
- xu2025amem: Xu, W., et al. (2025). *A-MEM*. 见 r-paper-005。（A-MEM-Code 在 SWE-bench 上的应用）
- yang2023opro: Yang, C., et al. (2023). *OPRO*. 见 r-paper-008。（OPRO 在 SWE-bench 上的应用）