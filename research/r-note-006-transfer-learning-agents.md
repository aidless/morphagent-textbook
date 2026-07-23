---
note_id: r-note-006
title: "迁移学习在自修改 Agent 中的应用：操作形态迁移 vs 行为迁移（Transfer Learning in Self-Modifying Agents: Morphology Transfer vs Behavior Transfer）"
authors: [MorphAgent Textbook Author]
created: 2026-07-22
updated: 2026-07-23
status: final
related_chapters: [Ch 11, Ch 12, Ch 16, Ch 19]
related_papers: [xu2025amem, robeyns2025sica, yin2024godelagent, fang2025selfevolving, yao2023react, yang2023opro, pan2010transfer, taylor2009rltransfer]
keywords: [transfer-learning, morphological-transfer, behavior-transfer, H4, learn-to-learn, in-context adaptation, cross-task, self-modifying-agent]
---

# r-note-006: 迁移学习在自修改 Agent 中的应用

> **本笔记的地位**：本笔记为 H4（迁移收益假说）建立**操作形态学框架**——把传统迁移学习（model weight transfer）扩展为**操作形态迁移（B transfer）**与**行为迁移（behavior transfer）**两类。同时，本笔记把"形态迁移"与 A-MEM 的"链接迁移"（r-paper-005）、SICA 的"代码自修改迁移"（r-paper-006）建立显式映射——这是把 H4 从"假说"变成"可工程验证的指标"的关键步骤。

## 1. 动机：传统迁移学习 vs 操作形态迁移

传统迁移学习（Transfer Learning）研究的是"在任务 A 上训练的模型参数如何迁移到任务 B"（Pan & Yang, 2010; Taylor & Stone, 2009）。LLM Agent 的自修改引入了一个新的迁移维度——不是模型权重迁移，而是**操作形态迁移（operational morphology transfer）**。Agent 在任务 A 中演化出了修改后的 $B' = U(B, \tau_A, r_A, \mathcal{C})$，这个 $B'$ 是否在任务 B 上仍然比原始的 $B_{\text{base}}$ 更好？

H4（迁移收益假说）断言答案是肯定的，且收益超过"直接记忆任务 A 答案"的简单复制。本笔记为 H4 建立迁移框架，引入"形态迁移"（Morphological Transfer）概念，并讨论跨任务迁移的边界条件。

**关键澄清**：本书区分两种"迁移"——这是后续所有讨论的基础：

- **形态迁移（Morphology Transfer）**：把任务 A 演化出的 $B' = (P', T', M', C')$ **整体**迁移到任务 B。这是"能力层面的迁移"——$B'$ 是 Agent 在 A 上"磨练出的形态"。
- **行为迁移（Behavior Transfer）**：把任务 A 中**最优的行为轨迹** $\tau_A^* = \{a_1^*, o_1^*, \ldots, a_T^*, o_T^*\}$ 复制到任务 B 的记忆中。这是"内容层面的迁移"——直接利用 A 的答案。

H4 严格断言的是**形态迁移优于行为迁移**——这是"能力 > 内容"的体现。这一断言如果成立，将改变 LLM Agent 的训练范式：**应该演化能力，而非记忆答案**。

### 1.1 与元学习的关系

形态迁移与元学习（meta-learning，learning to learn）有深刻联系。本书主张：**形态迁移 = 操作形态学版本的元学习**。

在元学习中，"学习算法"是固定的（如 MAML、Reptile），目标是找到一个好的"初始化参数 $\theta_0$"使得在新任务上 fine-tuning 成本最低。在操作形态迁移中，"学习算法"是 U，目标是找到一个好的"$B_0$"使得在新任务上演化成本最低。

两者都是"在任务分布上学习'如何学习'"——但形态迁移比元学习更灵活：它能修改 B 的所有组件（P/T/M/C），而元学习通常只修改参数 $\theta$。这一灵活性是 L5 Agent 的核心优势。

### 1.2 与 in-context learning 的边界

In-context learning（ICL）是另一种"任务适应"机制——Agent 通过在 prompt 中放入 few-shot example 来适应新任务，而不需要修改任何参数或形态。形态迁移与 ICL 的关键差异：

- **ICL**：任务特定知识放在 prompt 中，跨任务不持久。修改 $P$ 但每次任务都重新加载。
- **形态迁移**：任务特定知识内化到 $B = \{P, T, M, C\}$ 中，跨任务持久。修改的形态可被新任务直接复用。

本书主张：**形态迁移与 ICL 是互补的，而非竞争**。在任务 A 演化出的 $B'$ 可作为任务 B 的 ICL "种子"——$B'$ 中的 few-shot examples 是高质量的（因为它们来自实际成功经验），可以作为新任务的 in-context 演示。这是 H4 的强化版本。

## 2. 核心论点：形态迁移的机制

形态迁移的核心论点是：**在任务 A 的环境反馈下演化出的操作形态 $B'$，包含了超越任务特定知识的通用适应能力**。这些通用适应能力表现为：

1. **更高效的 prompt 结构**：更好的指令格式（如"先解释问题，再一步步推理"）、更精准的角色定义（如"你是 Kaggle 顶级选手"）。
2. **更精炼的工具集**：删除了任务 A 特有但对任务 B 也无用的冗余工具（如在 Python 任务中删除 Java 工具），保留了通用工具（如文件读取、网络搜索）。
3. **更优化的记忆 schema**：更高效的检索策略（如 A-MEM 风格的图结构比 list 结构更适合多主题）、更好的记忆压缩。
4. **更鲁棒的代码模块**：更好的错误处理（如沙箱、异常恢复）、更通用的抽象（如把"Python 函数调用"抽象为"语言无关的函数调用"）。

**关键 nuance**：形态迁移 ≠ 知识迁移。知识迁移是"把任务 A 的答案记住并在任务 B 中复用"，形态迁移是"把在任务 A 中磨练出的'如何学习和适应'的能力迁移到任务 B"。前者是内容层面的，后者是能力层面的。H4 断言后者更有价值。

### 2.1 形态迁移的四个层次

本书把形态迁移分为四个层次（按"通用性"递增）：

| 层次 | 描述 | 例子 | 通用性 |
|---|---|---|---|
| **L1 组件内迁移** | 修改单个组件的"内部参数"，跨任务复用 | OPRO 演化出的 prompt 在多个数学任务上复用 | 低 |
| **L2 组件间迁移** | 多个组件的协同修改，跨任务复用 | A-MEM 的链接结构 + OPRO 的 prompt 协同 | 中 |
| **L3 架构迁移** | 修改 B 的"架构"（如把 ReAct 改成 ToT），跨任务复用 | SICA 修改 helper function 模式 | 中高 |
| **L4 元架构迁移** | 修改 U 本身（即"如何生成修改"），跨任务复用 | Gödel Agent 修改 L4 元控制器 | 高 |

H4 在 L1-L2 上已经被部分验证（OPRO、A-MEM）；在 L3-L4 上是开放问题。本节后续展开 L3-L4 的实验设计。

### 2.2 形态迁移的边界条件

形态迁移不是万能的——它有边界条件：

1. **任务相似性**：迁移收益与任务相似度正相关。极端情况——任务 A 是"客服对话"，任务 B 是"代码生成"——形态迁移可能为负（见第 5 节"负迁移"）。
2. **形态稳定性**：$B'$ 必须是"稳定的最优形态"——若 $B'$ 在任务 A 上尚未收敛就迁移，可能把"中间形态"误认为"通用形态"。
3. **可分性**：$B'$ 的修改必须可以"拆解"——任务特定的部分（如 A 的特定 prompt 措辞）应被识别并剥离，只迁移通用部分。

## 3. 形式化

### 3.1 迁移增益

定义迁移增益（Transfer Gain）：

$$
\Delta_{\text{perf}} = \text{perf}(B', \text{task}_{\text{new}}) - \text{perf}(B_{\text{base}}, \text{task}_{\text{new}})
$$

其中 $B' = U(B_{\text{base}}, \tau_A, r_A, \mathcal{C})$ 是在任务 A 中演化出的操作形态。

### 3.2 H4 的形式化重述

$$
\Delta_{\text{perf}} > \alpha \cdot \text{memory}(A) + \epsilon
$$

其中 $\alpha \cdot \text{memory}(A)$ 是直接记忆任务 A 答案在新任务上的贡献（$\alpha$ 是记忆利用系数，通常很小），$\epsilon$ 是统计显著性阈值。

**H4 严格陈述**：形态迁移增益 $\Delta_{\text{perf}}$ 大于直接记忆 A 答案的增益 $\alpha \cdot \text{memory}(A)$，且这一差异具有统计显著性（$p < 0.05$）。

### 3.3 形态迁移矩阵

定义形态迁移矩阵 $\Gamma$，刻画不同任务之间的形态迁移效果：

$$
\Gamma_{ij} = \Delta_{\text{perf}}(B^{(i)}, \text{task}_j)
$$

其中 $B^{(i)}$ 是在任务 $i$ 中演化出的操作形态。$\Gamma$ 是一个 $N \times N$ 矩阵（$N$ 个任务），对角线元素为 0（同一任务无迁移），非对角线元素衡量跨任务迁移增益。

**性质分析**：

- 若 $\Gamma$ 接近对称矩阵，说明形态迁移是双向的（任务 A 对 B 的增益 ≈ 任务 B 对 A 的增益）。
- 若 $\Gamma$ 的行均值 $> 0$，说明任务 $i$ 的演化形态具有"通用性"。
- 若 $\Gamma$ 的列均值 $> 0$，说明任务 $j$ 容易从其他任务的形态中获益（"可迁移友好"任务）。

### 3.4 迁移衰减函数

定义迁移衰减函数，描述迁移增益随任务距离的变化：

$$
\Delta_{\text{perf}}(d) = \Delta_{\max} \cdot e^{-\lambda \cdot d(B^{(i)}, B^{*(j)})}
$$

其中 $d(B^{(i)}, B^{*(j)})$ 是任务 $i$ 的演化形态与任务 $j$ 的最优形态之间的距离，$\lambda$ 是衰减系数。

**形态距离 $d(\cdot, \cdot)$ 的度量**：

$$
d(B_1, B_2) = \sum_{i \in \{P, T, M, C\}} w_i \cdot \text{component\_distance}(B_1[i], B_2[i])
$$

其中：
- $\text{component\_distance}(P_1, P_2)$：prompt 的语义距离（用 sentence embedding cosine distance）。
- $\text{component\_distance}(T_1, T_2)$：工具集合的 Jaccard 距离（$1 - |T_1 \cap T_2|/|T_1 \cup T_2|$）。
- $\text{component\_distance}(M_1, M_2)$：记忆 schema 的结构距离（拓扑距离 + 内容距离）。
- $\text{component\_distance}(C_1, C_2)$：代码的 AST 距离。

这一形式化让"任务距离"成为可量化的对象——为 H4 的实验设计提供基础。

### 3.5 形式化映射：$f(M_A) \to M_B$

更形式化地，形态迁移是一个函数 $f: M_A \to M_B$，其中 $M_A$ 是任务 A 的"形态空间"（包括 $B^{(A)}$ 及其演化轨迹），$M_B$ 是任务 B 的形态空间。本书区分三种 $f$：

1. **直接迁移（direct transfer）**：$f(B^{(A)}) = B^{(A)}$——直接把 A 的形态当作 B 的初始形态。
2. **抽象迁移（abstract transfer）**：$f(B^{(A)}) = \text{abstraction}(B^{(A)})$——把 A 的形态抽象为通用模板，再应用到 B。
3. **条件迁移（conditional transfer）**：$f(B^{(A)}, \text{task}_B) = \text{condition}(B^{(A)}, \text{task}_B)$——根据 B 的任务特征，挑选 A 的部分形态迁移。

直接迁移最简单但通用性最差；抽象迁移最通用但实现复杂；条件迁移在两者之间。H4 在不同 $f$ 下有不同表现——实验设计应分别测试。

## 4. 实验设计

### 4.1 实验组 1：成对迁移验证

选择 4 个任务域（编程、数学推理、客服对话、数据分析），形成 $4 \times 3 = 12$ 个跨任务迁移方向。对每个方向测量 $\Delta_{\text{perf}}$，填充 $4 \times 4$ 的迁移矩阵 $\Gamma$。

- **自变量**：源任务域（4 个）、目标任务域（4 个）。
- **因变量**：迁移增益 $\Delta_{\text{perf}}$、任务完成率、修改次数。
- **控制变量**：LLM 模型、演化步数、任务难度。
- **统计检验**：单样本 $t$ 检验，检验 $\Delta_{\text{perf}} > 0$ 是否在 12 个方向上均成立。

**预期结果**：$\Gamma$ 应呈现"聚类结构"——相似任务之间的迁移增益大于不相似任务。即：
- 编程 ↔ 数据分析：迁移增益高（都是结构化输出）。
- 编程 ↔ 客服对话：迁移增益低（输出形式差异大）。
- 数学推理 ↔ 数据分析：迁移增益中等（都需要精确推理）。

### 4.2 实验组 2：形态迁移 vs 知识迁移

对比三种迁移策略：(1) 形态迁移（直接用 $B'$ 执行新任务）；(2) 知识迁移（把任务 A 的记忆条目复制到新任务的 $M$ 中）；(3) 无迁移（用 $B_{\text{base}}$ 执行新任务）。

- **预期结果**：若 H4 成立，迁移策略 (1) 的增益 > 迁移策略 (2) 的增益 > 无迁移。
- **关键对比**：(1) vs (2) 直接检验"形态迁移 > 知识迁移"。

这一实验组是 H4 的**核心检验**——它把"形态迁移 vs 知识迁移"明确对比，回答"是迁移能力还是迁移答案"的问题。

### 4.3 实验组 3：迁移效率曲线

追踪 $B'$ 在新任务上继续演化时的学习曲线，比较：
- 从 $B_{\text{base}}$ 开始的演化曲线（冷启动）。
- 从 $B'$ 开始的演化曲线（热启动 / 迁移启动）。

预期：迁移启动的曲线更陡、收敛更快、最终性能更高。

```python
class TransferLearningCurveExperiment:
    """测量形态迁移对学习曲线的影响"""

    def __init__(self, task_A, task_B, agent_factory):
        self.task_A = task_A
        self.task_B = task_B
        self.agent_factory = agent_factory

    def run(self, n_steps=200):
        results = {"cold_start": [], "warm_start": []}

        # 冷启动：从 B_base 开始
        agent_cold = self.agent_factory.create_base_agent()
        # 在 A 上不演化（控制变量）
        for step in range(n_steps):
            metrics = agent_cold.step(self.task_B.sample())
            results["cold_start"].append(metrics)

        # 形态迁移：在 A 上演化 100 步，得到 B'
        agent_warm = self.agent_factory.create_base_agent()
        for _ in range(100):
            agent_warm.step(self.task_A.sample())
        B_prime = agent_warm.snapshot()  # B' = 演化后的形态

        # 热启动：从 B' 开始
        agent_warm_start = self.agent_factory.create_agent_from_snapshot(B_prime)
        for step in range(n_steps):
            metrics = agent_warm_start.step(self.task_B.sample())
            results["warm_start"].append(metrics)

        # 计算：迁移增益 = warm_start[-1] - cold_start[-1]
        # 收敛速度 = argmin |warm_start - cold_start| 之间的差
        return results
```

### 4.4 实验组 4：跨任务迁移的负迁移分析

任务域差异过大时，形态迁移可能为负。本实验组测量：

$$
\Delta_{\text{perf}}^{\text{negative}} = \text{perf}(B', \text{task}_B) - \text{perf}(B_{\text{base}}, \text{task}_B) < 0
$$

**预期结果**：负迁移出现在"形态距离 $d(B^{(A)}, B^{*(B)})$ 大于阈值 $d_{\text{crit}}$"的场景。例如：在客服任务上演化出的 $B'$ 包含大量"对话管理"逻辑，迁移到编程任务可能引入无关代码。

**反迁移机制**：负迁移的解决方案是"形态剪枝"——在迁移前剥离任务特定的部分：

```python
def prune_morphology(B_prime, target_task, llm):
    """用 LLM 评估 B' 的每个修改是否对 target_task 有用"""
    useful_components = []
    for component, change in B_prime.changes.items():
        # 询问 LLM：这一修改对 target_task 有用吗？
        prompt = f"""
        Target task: {target_task}
        Component: {component}
        Change description: {change}
        Is this change useful for the target task? Answer Yes/No.
        """
        is_useful = llm.generate(prompt).strip().startswith("Yes")
        if is_useful:
            useful_components.append((component, change))
    # 返回剪枝后的形态
    return B_prime.apply_changes(useful_components)
```

这一机制对应"迁移学习中的 domain adaptation"——在迁移前过滤掉对目标任务有害的部分。

## 5. 与现有工作的关系

### 5.1 与 A-MEM 的"链接迁移"对照

A-MEM（r-paper-005）的 M 自演化产生了一种特殊的"迁移模式"——**链接迁移（link transfer）**。A-MEM 在任务 A 中形成的"note + links"网络，部分链接是任务特定的（如"用户喜欢咖啡"），部分是通用的（如"用户偏好 = 主题相关"）。当 A-MEM 迁移到任务 B 时：

- 任务特定的链接（如"咖啡"）应被剥离。
- 通用链接（如"主题相关"）应被保留。

本书主张：**A-MEM 的链接迁移是形态迁移的子集**——它只迁移 M 的结构，不迁移 P/T/C。但 A-MEM 揭示了形态迁移的一个关键洞见：**LLM 可以自主决定哪些修改是任务特定的、哪些是通用的**——这是 LLM 元推理能力的新维度。

A-MEM 的 `analyze_links` 函数（见 r-paper-005 伪代码）已经隐含了"链接分类"机制——它把链接分为 causal、temporal、thematic、contradictory、supporting 五类。本书建议扩展这一分类，加入"task-specific" vs "task-general"维度，让 A-MEM 能自动剪枝。

### 5.2 与 SICA 的"代码自修改迁移"对照

SICA（r-paper-006）的 C 自修改产生了一种特殊的形态迁移——**代码自修改迁移（code-self-mod transfer）**。SICA 在编码任务 A 中演化出的 $C_{\text{mod}}$，包含 A 特有的 helper function（如"针对 GitHub API 的 patch 生成器"），也包含通用 helper（如"通用调试函数"）。

当 SICA 迁移到编码任务 B 时：

- 任务特定的 helper（如 GitHub 特定函数）应被剥离或重写。
- 通用 helper（如调试、测试生成）应被保留。

SICA 的 `verify_safety` 函数（沙箱 + 行为不变性 + 突变测试）保证了迁移的代码在 B 上仍保持行为等价——但这不能保证 B 上的任务表现更好。

**关键差异**：SICA 的迁移是**安全性优先**——它通过行为不变性保证"迁移不破坏 B"，但不保证"迁移提升 B"。形态迁移的目标是**性能优先**——它追求"迁移提升 B"。

本书建议 SICA-style + morphology-style 的混合方案：先用 SICA 的安全验证保证迁移可行，再用 morphology-style 的剪枝机制提升迁移收益。

### 5.3 与 Gödel Agent 的"L4 元迁移"对照

Gödel Agent（r-paper-007）的 L4 元控制器 U 自修改是一种更高级的形态迁移——**元迁移（meta-transfer）**。Gödel Agent 修改 U 本身（即"如何生成修改"），让"修改能力"也跨任务迁移。

例如：在 WebShop 上演化出的 U（已习惯于"如何修改工具调用策略"），迁移到 ALFWorld 时仍能加速"如何修改反思策略"——这是"如何修改"本身的迁移。

元迁移是 H4 在 L5.2 等级的扩展——H4 不仅要求 B 的组件可迁移，还要求 U（修改器本身）可迁移。本书预测元迁移的收益是非线性的：在多任务序列上累积的 $U^{(T)}$ 显著优于单任务演化。

### 5.4 与 OPRO 的"Prompt 迁移"对照

OPRO（r-paper-008）的 P 自修改产生了一种最常见的形态迁移——**prompt 迁移（prompt transfer）**。OPRO 在任务 A 上优化出的 prompt $P^*$ 在任务 B 上的表现是否仍好？

OPRO 的实验显示：$P^*$ 在**相似任务**（如 GSM8K → MATH）上的迁移效果好，但在**不相似任务**（如 GSM8K → 客服对话）上的迁移效果差。这与本书的"形态距离衰减"预测一致。

OPRO 的迁移是**P-only 形态迁移**——它只迁移 B 中的 P 维度，不迁移 T/M/C。本书主张 P-only 迁移是 H4 在 L4.1 等级的"特例"，完整 H4 需要 L4-L5 的多组件迁移。

## 6. 与本书的关系

本笔记连接以下章节：

- **第 11 章（操作形态学）**：H4 的理论定义来源，本笔记是 H4 的实验设计细化。H4 的形式化（$\Delta_{\text{perf}} > \alpha \cdot \text{memory}(A) + \epsilon$）来自 r-note-001。
- **第 12 章（Prompt 自修改）**：OPRO 是形态迁移的一种实现路径——L1 组件内迁移的代表。
- **第 14 章（长期记忆与 A-MEM）**：A-MEM 的链接迁移是 M 自演化的迁移特例。r-paper-005 中的链接类型系统可扩展为"task-specific vs task-general"维度。
- **第 15 章（自编辑代码）**：SICA 的代码自修改迁移是 C 自修改的迁移特例。r-paper-006 的安全验证可与本笔记的形态剪枝结合。
- **第 16 章（跨组件协同自进化）**：跨组件协同演化出的 $B'$ 具有更高的迁移潜力（协同形态更通用）。
- **第 17 章（元控制器 U）**：Gödel Agent 的 L4 元迁移是 H4 在 L5.2 的扩展。
- **第 19 章（MorphBench）**：MorphBench 的多任务评测能力为形态迁移提供评测基础——H4 的验证需要 MorphBench 的任务多样性。

## 7. 开放问题

1. **负迁移（Negative Transfer）的条件**：什么情况下 $\Delta_{\text{perf}} < 0$？任务域差异过大是否导致形态迁移反而有害？负迁移的边界在哪里？**预期答案**：当 $d(B^{(A)}, B^{*(B)}) > d_{\text{crit}}$ 时，负迁移显著。$d_{\text{crit}}$ 需要通过实验标定。
2. **迁移的组件特异性**：四个组件 $P, T, M, C$ 中，哪个组件的迁移增益最大？推测 prompt 的迁移性最高（指令格式通用），工具的迁移性最低（任务特定性强）。**待实验验证**。
3. **累积迁移**：连续在多个任务上演化后的 $B'''$ 是否比单次迁移的 $B'$ 更好？迁移收益是否可累积？**预期答案**：累积迁移有"边际收益递减"——前几次累积显著，后续趋近饱和。
4. **与元学习的关系**：形态迁移是否可以被视为一种元学习（meta-learning）？$B'$ 是否相当于"学习到的学习策略"？**预期答案**：形态迁移是"在 B 空间上的元学习"——U 是"学习算法"，$B_0$ 是"初始参数"。
5. **跨 LLM 迁移**：$B'$ 在 LLM-A 上演化，是否能迁移到 LLM-B（不同 LLM）？这是"跨模型迁移"问题。**预期答案**：部分可迁移——P 是 LLM 相关的（不同 LLM 偏好不同 prompt），T/M/C 是 LLM 无关的。
6. **迁移的可解释性**：能否解释"为什么 $B'$ 在任务 B 上表现更好"？需要可解释性技术（如 LLM-as-judge、注意力可视化）。

## 8. 实现细节：形态迁移的工程实现

### 8.1 形态序列化

为了让 $B'$ 可被"打包迁移"，需要序列化形态：

```python
class MorphologySerializer:
    """序列化 B = {P, T, M, C} 为可迁移的格式"""

    def serialize(self, B):
        return {
            "P": B.P.to_dict(),          # prompt 文本 + few-shot examples
            "T": [tool.schema for tool in B.T],  # 工具 schema 列表
            "M": B.M.to_dict(),          # 记忆结构（笔记 + 链接 + 标签）
            "C": B.C.to_source_code(),  # 代码（如果是 self-modifying agent）
            "metadata": {
                "task_origin": B.task_origin,
                "evolution_steps": B.evolution_steps,
                "performance_metrics": B.metrics,
                "version": B.version_hash,  # 用于版本管理
            }
        }

    def deserialize(self, blob):
        return Morphology(
            P=Prompt.from_dict(blob["P"]),
            T=[Tool.from_schema(s) for s in blob["T"]],
            M=Memory.from_dict(blob["M"]),
            C=Code.from_source(blob["C"]),
            metadata=blob["metadata"]
        )
```

这一序列化让 $B'$ 可以被版本化、共享、压缩、加密——为大规模形态迁移（如多任务累积）提供基础设施。

### 8.2 形态剪枝算法

```python
def morphology_pruning(B_prime, target_task, llm, threshold=0.5):
    """剪枝 B_prime 中对 target_task 无用的修改"""
    pruned = B_prime.clone()
    for component_name in ["P", "T", "M", "C"]:
        original = pruned[component_name]
        # 询问 LLM：每个修改是否对 target_task 有用？
        useful = []
        for change in original.changelog:
            utility = llm_score_change(change, target_task, llm)
            if utility > threshold:
                useful.append(change)
        pruned[component_name] = original.apply_changes(useful)
    return pruned
```

### 8.3 累积迁移的多任务调度

```python
class CumulativeMorphologyTransfer:
    """在多个任务上累积形态迁移"""

    def __init__(self, agent_factory, task_sequence):
        self.agent_factory = agent_factory
        self.task_sequence = task_sequence  # [task_A, task_B, task_C, ...]
        self.transfer_log = []

    def run(self, steps_per_task=100):
        # 从 base 开始
        agent = self.agent_factory.create_base_agent()
        cumulative_B = agent.snapshot()

        for i, task in enumerate(self.task_sequence):
            # 在当前任务上演化
            for step in range(steps_per_task):
                agent.step(task.sample())

            # 评估是否迁移上一次的累积形态
            if i > 0:
                agent.load_snapshot(cumulative_B)
                # 然后继续在当前任务上演化

            # 更新累积形态
            cumulative_B = agent.snapshot()
            self.transfer_log.append({
                "task_index": i,
                "task": task.name,
                "B_snapshot": cumulative_B.serialize(),
                "performance": agent.evaluate(task.test_set())
            })

        return self.transfer_log
```

这一实现让"在 N 个任务序列上演化"成为可执行的实验——为"累积迁移是否优于单次迁移"提供数据。

## 9. 笔记元信息

- **状态**：final（从 draft 升级而来）
- **可被引用方式**：在第 11、12、14、15、16、19 章中引用本笔记定义的形态迁移框架。
- **可被复现方式**：第 16 章的协同自进化实验基于本笔记的累积迁移实现；第 19 章的 MorphBench 多任务评测基于本笔记的形态迁移矩阵。
- **作者注**：本笔记是 H4 的"工程化翻译"——把抽象的"迁移收益"假说转化为可测量的指标（$\Delta_{\text{perf}}$、$\Gamma$ 矩阵、衰减函数）。

## 10. 与 H1-H5 的关系总结

| 假设 | 与形态迁移的关系 | 验证手段 |
|---|---|---|
| **H1 结构可塑性** | 形态迁移建立在 H1 之上——H1 保证 $B'$ 是可被修改的 | MorphBench L1 仿真层 |
| **H2 协同演化** | 多组件协同形态迁移比单组件迁移收益更高 | 实验组 4 |
| **H3 形态适配** | 不同任务形成不同的最优形态，迁移矩阵 $\Gamma$ 非对角 | 实验组 1 |
| **H4 迁移收益** | **本笔记的核心**——形态迁移 > 知识迁移 | 实验组 2、3 |
| **H5 治理必要性** | 形态迁移需要治理（避免负迁移、累积漂移） | 跨任务安全审计 |

**关键洞察**：H4 与 H2、H3 紧密耦合——H4 假设形态迁移有效（基于 H1），但具体效果取决于 H2（协同优化）和 H3（任务差异）。三者共同构成"迁移理论"的三角。

## 参考文献

1. Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407. 见 r-paper-009。
2. Pan, S. J., & Yang, Q. (2010). *A Survey on Transfer Learning*. IEEE TKDE, 22(10), 1345-1359.（传统迁移学习综述）
3. Taylor, M. E., & Stone, P. (2009). *Transfer Learning for Reinforcement Learning Domains: A Survey*. JMLR, 10, 1633-1685.（RL 迁移学习综述）
4. Yang, C., et al. (2024). *Large Language Models as Optimizers (OPRO)*. ICLR. 见 r-paper-008。
5. Khattab, O., et al. (2024). *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines*. ICLR.（DSPy 的迁移能力）
6. Yin, X., et al. (2024). *Godel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement*. ACL. 见 r-paper-007。（L4 元迁移）
7. Xu, W., et al. (2025). *A-MEM: Agentic Memory for LLM Agents*. NeurIPS 2025. 见 r-paper-005。（M 链接迁移）
8. Robeyns, M., et al. (2025). *SICA: Self-Improving Coding Agent*. NeurIPS 2025. 见 r-paper-006。（C 自修改迁移）
9. Finn, C., Abbeel, P., & Levine, S. (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks* (MAML). ICML.（元学习的代表）
10. Snell, J., Swersky, K., & Zemel, R. (2017). *Prototypical Networks for Few-shot Learning*. NeurIPS.（few-shot learning 与元学习）
11. Thrun, S., & Pratt, L. (1998). *Learning to Learn*. Kluwer.（learning to learn 的经典教材）
12. Caruana, R. (1997). *Multitask Learning*. Machine Learning, 28(1), 41-75.（多任务学习，与累积迁移相关）
13. Yosinski, J., et al. (2014). *How Transferable Are Features in Deep Neural Networks?* NeurIPS.（神经网络特征迁移性）
14. Kirkpatrick, J., et al. (2017). *Overcoming Catastrophic Forgetting in Neural Networks*. PNAS.（防止负迁移：EWC）