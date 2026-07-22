---
note_id: r-paper-008
title: OPRO：用 LLM 作为黑盒优化器自修改 Prompt（Large Language Models as Optimizers）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 4, Ch 12]
related_papers: [yang2023opro, yao2023react, shinn2023reflexion, packer2023memgpt, yin2024godelagent, khattab2024dspy, cheng2024promptagent, fernando2023promptbreeder, zhou2023l2l, fang2025selfevolving]
keywords: [OPRO, LLM as optimizer, prompt self-modification, P self-modification, black-box optimization, hill climbing on prompts, LLM-as-U, generation 1 prompt evolution]
---

# r-paper-008：OPRO：用 LLM 作为黑盒优化器自修改 Prompt

> OPRO 是把 LLM 当作"prompt 优化器"的开创性工作——它让 LLM 在外部优化循环中作为黑盒优化器，根据历史 (prompt, score) 对持续生成新的 prompt 候选，把 prompt 演化视为一个**自然的字符串优化问题**。这是操作形态学意义上 **P 自修改（P self-modification）第一代**的代表：U 是"LLM 爬山"，B 的修改只发生在 P 维度，T/M/C 完全冻结。理解 OPRO 是理解后续所有 P 自修改工作（DSPy / PromptAgent / Promptbreeder）的起点。

## 1. 论文定位

Yang 等人 2023 年发表的 *Large Language Models as Optimizers*（ICLR 2024，arXiv:2309.03409 [$TRAE_REF](https://arxiv.org/abs/2309.03409)）是 LLM Agent 提示自修改领域的开创性工作。它提出一个简洁但深刻的命题：**让 LLM 作为优化器，根据历史的 (prompt, score) 对生成新的 prompt 候选**，其中 score 是 prompt 在目标任务（如 GSM8K 数学、SPAQ 多步推理、BIG-Bench 任务）上的表现。这一命题把"prompt 优化"重新定义为"在 prompt 字符串空间上的自然语言搜索问题"——LLM 用它对自然语言任务的"元理解"作为优化器。

本书将 OPRO 定位为**P 自修改的第一代（P self-modification generation 1）**——也是 L4 Agent 的代表性工作。在 L0-L5 的 Agent 等级谱系中，OPRO 处于 L4.1：仅修改 P、不修改 T/M/C；U 是"LLM-as-optimizer"；优化目标是单次任务的成功率（无跨 episode 状态）。

论文做出的三个判断被本书第 12 章重新审视：

- **"LLM as optimizer"**：LLM 不仅能作为任务执行者，还能作为优化器。这一双重角色是后续所有 Agent 自修改工作的前提。
- **"Prompt as string, optimization as search"**：把 prompt 优化视为一个**字符串空间的搜索问题**——LLM 通过对 (prompt, score) 历史的反思，生成"看起来会更好"的 prompt。这与传统的 prompt engineering（手工设计）和 prompt tuning（基于梯度的连续优化）形成对比。
- **"Trajectory-level meta-prompt"**：在每次优化迭代中，LLM 看到的不是单个 (prompt, score) 对，而是**所有历史的 (prompt, score) 对及其排序**——LLM 用这个完整轨迹作为输入，生成下一个候选。这是最早的"元提示"（meta-prompt）设计。

这三个判断共同构成"操作形态 B = {P, T, M, C}"中 P 的运行时演化模型：**P 是可被 LLM-as-optimizer 搜索的字符串，B 的其他组件冻结**。

## 2. 核心贡献

OPRO 论文做出四项核心贡献：

1. **形式化"LLM-as-optimizer"框架**：把 prompt 优化视为 LLM 在"历史 (prompt, score) 对集合"上的函数 \(f: \text{history} \to \text{new prompt}\)。这一形式化把"prompt engineering"从手工艺术转化为**搜索算法**——LLM 是搜索算法中的"提议分布"（proposal distribution），score 是"目标函数"。

2. **设计"meta-prompt"构造**：在每次优化迭代中，meta-prompt 包含：
   - 任务描述（如"Solve GSM8K math problems"）
   - 历史的 (prompt, score) 对，按分数**降序排列**（高分在前）
   - 优化指令："Generate a new prompt that is different from all previous prompts and achieves a higher score."
   
   LLM 看到这整个 meta-prompt，输出新 prompt 候选。

3. **在多个 benchmark 上验证 OPRO 优于零样本 CoT 和手工 prompt**：包括 GSM8K（数学推理，74.0% → 80.6%）、BBH（BIG-Bench Hard，多步推理）、MMLU（多任务理解）、Instruction Induction 任务。OPRO 在大多数任务上比手工 prompt 提升 5-15 个百分点。

4. **发现"prompt 演化路径符合分数上曲线"**：OPRO 在多次优化后绘制的 prompt 演化轨迹显示，分数随 iteration 单调上升（虽然单调性不严格），且最优 prompt 往往不是 LLM 在零样本下会生成的——它具有 LLM 自身难以发现的"非直觉"结构（如"先解释问题，再一步步推理"）。

### 2.1 与传统 Prompt Tuning 的边界

传统 prompt tuning（如 Lester et al. 2021, *The Power of Scale for Parameter-Efficient Prompt Tuning*）把 prompt 视为连续的 embedding 序列，用梯度下降优化。但 prompt tuning：
- 需要标注数据（不能用于无标注任务）
- 需要回传梯度到 LLM（限制了 LLM 的可访问性）
- 优化的 prompt 是 embedding 不是字符串（不能迁移到其他 LLM）

OPRO 的 prompt 是**字符串**——这意味着：
- 不需要梯度（可访问任意 LLM）
- 优化的 prompt 可读、可解释、可迁移
- 可以从单 LLM 优化迁移到多 LLM（不同 LLM 优化出不同 prompt，但都能用）

### 2.2 与 ReAct / Reflexion 的边界

ReAct（r-paper-001）的 prompt 是**手工设计的 6-shot example**——P 在部署后冻结；Reflexion（r-paper-002）的 prompt 修改只在**反思文本追加**层面（M 自修改，不是 P 自修改）。OPRO 是第一个把 P 视为**可被优化器搜索**的对象——这与前两者的关键差异是：**P 不再是手工或反射式修改，而是被 LLM-as-optimizer 系统性优化**。

### 2.3 与 MemGPT 的边界

MemGPT（r-paper-004）修改的是 M（记忆），不是 P。OPRO 修改 P，MemGPT 修改 M——两者是 B 中不同维度的自修改代表。从操作形态学看，OPRO 与 MemGPT 是**互不冲突的 L4 工作**：OPRO 是 P 自修改，MemGPT 是 M 自修改，两者结合就是 B 中 P + M 同时修改——这是后续协同自进化的雏形。

### 2.4 与 Gödel Agent 的边界

Gödel Agent（r-paper-007）是 L5.2——它修改整个 B（包括 P），且所有修改需 Z3 验证。OPRO 是 L4.1——它仅修改 P，且无验证机制。OPRO 与 Gödel Agent 之间的关系是**P 自修改的两代**：
- 第一代（OPRO）：LLM-as-optimizer，无验证
- 第二代（Gödel Agent L1）：LLM-as-optimizer + Z3 验证

## 3. 方法细节

### 3.1 OPRO 的形式化

OPRO 把 prompt 优化视为字符串空间上的搜索。设：
- \(\mathcal{P}\)：prompt 字符串空间
- \(\text{score}(p) \in \mathbb{R}\)：prompt \(p\) 在目标任务上的分数（如 accuracy）
- \(\mathcal{H}_k = \{(p_1, s_1), (p_2, s_2), \ldots, (p_k, s_k)\}\)：前 \(k\) 次评估的历史

OPRO 的目标是找到 \(p^* = \arg\max_{p \in \mathcal{P}} \text{score}(p)\)，但因为 \(\mathcal{P}\) 是巨大的字符串空间，OPRO 通过 LLM 提议-真实评估循环逐步逼近 \(p^*\)。

迭代 \(t\) 的 OPRO 流程：
1. **构造 meta-prompt**：把 \(\mathcal{H}_{t-1}\) 按分数降序排入 meta-prompt，再加上"Generate a new prompt..."指令。
2. **采样新 prompt**：LLM-as-optimizer 在 \(T\) 个采样（如 temperature=1.0）中生成新 prompt 候选 \(\{p_t^{(1)}, \ldots, p_t^{(T)}\}\)。
3. **评估**：用每个候选 \(p_t^{(i)}\) 在目标任务的训练集上评估，得到分数 \(s_t^{(i)}\)。
4. **更新历史**：\(\mathcal{H}_t = \mathcal{H}_{t-1} \cup \{(p_t^{(i)}, s_t^{(i)})\}_{i=1}^T\)。
5. **终止或继续**：达到最大迭代次数或分数停止提升。

### 3.2 伪代码实现

```python
class OPROAgent:
    def __init__(self, optimizer_llm, scorer_llm, task, initial_prompts,
                 max_iterations=50, samples_per_iter=8):
        self.optimizer_llm = optimizer_llm  # LLM-as-optimizer
        self.scorer_llm = scorer_llm        # 用于评估的 LLM
        self.task = task                    # 目标任务的训练集与测试集
        self.history = []                   # (prompt, score) 历史
        self.max_iterations = max_iterations
        self.samples_per_iter = samples_per_iter

        # 初始化历史: 给定 initial_prompts，评估它们
        for p in initial_prompts:
            score = self.evaluate_prompt(p)
            self.history.append((p, score))

    def evaluate_prompt(self, prompt):
        # 在 self.task 上评估 prompt，返回平均分数
        # 这里是 U 之外的环境评估
        scores = []
        for example in self.task.train_set:
            output = self.scorer_llm.generate(
                prompt + "\n\n" + example.input
            )
            score = self.task.metric(output, example.target)
            scores.append(score)
        return np.mean(scores)

    def construct_meta_prompt(self):
        # 构造 OPRO meta-prompt
        meta = "Your task is to generate a new prompt that achieves a higher score.\n\n"
        meta += "The following prompts have been evaluated:\n\n"
        # 按分数降序排列
        sorted_history = sorted(self.history, key=lambda x: -x[1])
        for i, (p, s) in enumerate(sorted_history[:10]):  # 取 top-10
            meta += f"[Prompt {i+1}] Score: {s:.4f}\n"
            meta += f"[Prompt {i+1} Text]: {p}\n\n"
        meta += "Generate a new prompt that:\n"
        meta += "1. Is different from all previous prompts.\n"
        meta += "2. Achieves a higher score than the highest-scoring prompt above.\n"
        meta += "Output ONLY the new prompt text, no explanation."
        return meta

    def optimize(self):
        # OPRO 主循环
        for iteration in range(self.max_iterations):
            meta_prompt = self.construct_meta_prompt()

            # LLM-as-optimizer 生成 T 个候选
            new_prompts = []
            for _ in range(self.samples_per_iter):
                new_p = self.optimizer_llm.generate(
                    meta_prompt,
                    temperature=1.0  # 多样性
                )
                new_prompts.append(new_p)

            # 评估新候选
            new_scores = []
            for p in new_prompts:
                s = self.evaluate_prompt(p)
                new_scores.append(s)
                self.history.append((p, s))

            # 检查收敛
            best_score = max(new_scores)
            if best_score > max(s for _, s in self.history[:-len(new_prompts)]):
                # 当前最优未改进，记录但不停止
                pass
            else:
                # 收敛，停止
                if self._check_convergence():
                    break

        # 返回最优 prompt
        best_prompt, best_score = max(self.history, key=lambda x: x[1])
        return best_prompt, best_score

    def _check_convergence(self, patience=5):
        # 简单的收敛检测：最近 patience 次无改进
        # 实现省略
        pass
```

伪代码的核心设计：

1. **LLM-as-optimizer**：`self.optimizer_llm` 独立于 `self.scorer_llm`，允许用不同模型（如 PaLM 2 优化，GPT-4 评估）。
2. **Meta-prompt 历史排序**：`self.construct_meta_prompt` 把历史按分数降序排，让 LLM 看到"什么 prompt 高分、什么 prompt 低分"。
3. **多样性采样**：用 `temperature=1.0` 让 LLM 生成多个不同候选，避免陷入局部最优。
4. **评估-更新分离**：评估由 `self.evaluate_prompt` 外部完成（脱离 LLM-as-optimizer），保证评估与优化解耦——避免 LLM 自评自环。

### 3.3 Meta-prompt 的关键设计

OPRO 论文特别强调 meta-prompt 的设计：

- **按分数排序**：高分在前。这是 LLM 的"模仿学习"——LLM 倾向于模仿前面的（高分）prompt。
- **包含多样化的历史**：避免所有历史都是 top-1 的相似 prompt——OPRO 用 top-10 高分 + 低分样本混合。
- **明确指令**："Generate a new prompt that achieves a higher score"，让 LLM 的目标明确。

这些设计经验是后续所有 LLM-as-optimizer 工作（包括 PromptAgent, Promptbreeder）的基础。

### 3.4 与传统优化的对比

OPRO 的"优化器 = LLM"与传统优化的对比：

| 维度 | 传统优化（梯度下降） | OPRO（LLM-as-optimizer） |
|---|---|---|
| 目标 | 连续参数空间 | 离散字符串空间 |
| 搜索方向 | 梯度 | LLM 的"语言直觉" |
| 评估次数 | 多（每步评估） | 中（每步评估多个候选） |
| 计算成本 | 梯度计算 | LLM 推理 |
| 全局最优性 | 局部最优 | 局部最优（无梯度保证） |

OPRO 没有全局最优性保证——它是一个"在字符串空间上的启发式搜索"。但它在实践中显示出**惊人的有效性**——往往能找到比手工 prompt 更好的解。

## 4. 操作形态学视角

把 OPRO 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 与元控制器 U 上，我们得到三个关键论断。

### 4.1 OPRO 中 B 的每个组件

| 组件 | 在 OPRO 中的实现 | 修改能力 |
|---|---|---|
| \(P\) | 系统 prompt + few-shot examples | **可修改**（OPRO 主循环优化对象） |
| \(T\) | 工具列表（通常是空的，因为 OPRO 用于任务推理而非工具调用） | **冻结** |
| \(M\) | 仅短期 context（任务输入） | **冻结**（无跨 episode 记忆） |
| \(C\) | `self.evaluate_prompt` + LLM 调用 | **冻结**（固定算法逻辑） |

**关键洞见**：OPRO 只修改 P。这是"操作形态学 P 自修改第一代"——它是单组件自修改的经典代表。

### 4.2 OPRO 中 U 的状态

OPRO 的 U 是 **LLM-as-optimizer + 评估-更新循环的组合**：

$$
P_{t+1} = U(P_t, \mathcal{H}_t, \mathcal{C}) = \text{LLM-optimizer}(\text{meta-prompt}(\mathcal{H}_t))
$$

其中 \(\mathcal{H}_t\) 是历史 \((P, \text{score})\) 对的集合，\(\text{meta-prompt}\) 是按分数排序的字符串拼接。

U 的实现包括：
- **LLM-as-optimizer**：核心搜索算子。
- **Meta-prompt 构造**：把历史转化为 LLM 可消化的提示。
- **评估-更新循环**：外部评估器保证分数客观。
- **多样性采样**：通过 temperature 多样化避免局部最优。

OPRO 的 U 是**最简单的 U**——它没有形式验证、没有跨 episode 学习、没有安全机制。这是 L4.1 的标志实现。

### 4.3 OPRO 的 P 自修改级别

本书第 12 章把 P 自修改分为四个子层级：

```
L4.1.1 prompt 工程（手工设计，零级）
L4.1.2 prompt tuning（基于梯度的连续优化）
L4.1.3 OPRO（基于 LLM-as-optimizer 的字符串优化）
L4.1.4 DSPy / TextGrad（基于编译器的程序优化）
L4.1.5 PromptAgent / Promptbreeder（基于搜索/进化的优化）
```

OPRO 是 L4.1.3 的代表——它把 prompt 优化视为字符串空间上的搜索。这是 P 自修改从"无优化"到"自动化优化"的关键跳跃。

### 4.4 OPRO 在 L0-L5 等级中的位置

按本书第 18 章：

- L2 ReAct Agent（r-paper-001）：P 冻结
- L3 Reflexion（r-paper-002）：M 自追加，P 冻结
- **L4.1 Self-Modifying Prompt（OPRO）** ← 本笔记
- L4.2 Self-Modifying Memory（A-MEM, r-paper-005）
- L4.3 Self-Modifying Toolset（LATM, Voyager）
- L5 Self-Evolving（SICA, Gödel Agent）

OPRO 是 L4.1。它仅修改 P，是 L4 中最简单的子等级。

### 4.5 OPRO 与 H1-H5 的关系

| 假设 | OPRO 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | P 可以在优化循环中修改 | **强支持 H1**（P 是可塑的） |
| **H2 协同演化** | 仅修改 P，T/M/C 冻结 | H2 不可验证 |
| **H3 形态适配** | 不同任务优化出不同 prompt | **支持 H3**（不同任务的 P 不同） |
| **H4 迁移收益** | prompt 是字符串，可迁移到其他 LLM | **支持 H4**（prompt 迁移） |
| **H5 治理必要性** | 无 prompt 修改的验证/版本控制 | **需要治理**（推动 H5） |

OPRO 在 H1、H3、H4 上提供证据。H2 上 OPRO 是反例——它表明单组件修改也能有显著效果，但 H2 需要的是**多组件联合修改**，OPRO 不能验证。H5 上 OPRO 暴露了"无验证 P 修改"的潜在风险——一次错误优化可能让 P 退步，且无回滚机制。

## 5. 实验与结果

OPRO 在多个 benchmark 上做了实验，重点是数学推理与多步推理。

### 5.1 GSM8K（数学推理）

- 数据集：8.5K 道小学数学应用题
- 评测：pass@1（一次性解出正确答案的比例）
- baseline：CoT + 8-shot example（手工设计）≈ 71.8%
- OPRO after 50 iterations：**80.6%**
- 相对提升：12.3%
- 操作形态学意义：OPRO 在 GSM8K 上演化出"先列出已知量、再列未知量、再推理"的 prompt 模式——这是手工 prompt 难以发现但实质有效的结构。这是 P 自修改在推理任务上的代表性效果。

### 5.2 BBH（BIG-Bench Hard）

- 数据集：23 个 BIG-Bench 难题（多步推理、日期理解、跟踪乱序物体等）
- 评测：每任务准确率
- baseline：CoT（手工 prompt）≈ 47.0%
- OPRO after 50 iterations：**55.2%**
- 相对提升：17.4%
- 操作形态学意义：BBH 包含**异质任务**——OPRO 在不同子任务上优化出不同 prompt。这暗示 OPRO 的 P 自修改具有**任务依赖性**（task-dependent）。

### 5.3 MMLU（多任务理解）

- 数据集：57 个学科的多选题
- 评测：准确率
- baseline：5-shot CoT ≈ 68.9%
- OPRO after 50 iterations：**73.4%**
- 相对提升：6.5%
- 操作形态学意义：MMLU 上 OPRO 提升较小——因为 MMLU 任务的"prompt 表述"较稳定，搜索空间小。

### 5.4 Instruction Induction

- 数据集：24 个指令归纳任务（生成特定模式文本）
- baseline：手工 prompt 平均 41%
- OPRO after 50 iterations：**61%**
- 相对提升：49%
- 操作形态学意义：Instruction Induction 是 OPRO 最擅长的场景——任务的 prompt 表述空间大，OPRO 的字符串优化能充分探索。

### 5.5 关键实验观察

| 任务 | baseline → OPRO | 主要改进模式 |
|---|---|---|
| GSM8K | 71.8% → 80.6% | 数学推理结构（已知量/未知量分解） |
| BBH | 47.0% → 55.2% | 任务特定推理模板 |
| MMLU | 68.9% → 73.4% | 学科特定的 prompt 风格 |
| Instruction Induction | 41% → 61% | 输出格式与示例设计 |

**关键观察**：OPRO 的提升在**任务 prompt 空间大**的任务（Instruction Induction, GSM8K）上最显著；在**prompt 空间受约束**的任务（MMLU）上提升较小。这暗示 **OPRO 的收益与 prompt 搜索空间大小正相关**。

### 5.6 消融研究

论文做了几组消融：

- **OPRO full**：meta-prompt with history
- **OPRO no-history**：只用 task description 生成新 prompt（等价于手工迭代）
- **OPRO no-sort**：meta-prompt 不按分数排序（随机顺序）
- **OPRO single-sample**：每次迭代只生成 1 个候选（无多样性）

结果显示：
- OPRO full：50 iteration 提升 10-50%（不同任务）
- OPRO no-history：仅提升 1-3%（接近随机搜索）
- OPRO no-sort：提升 5-15%（比 full 低 3-10 个百分点，因 LLM 不善于根据未排序信息学习）
- OPRO single-sample：提升 5-25%（明显下降，因失去多样性）

**结论**：**历史（按分数排序）+ 多样性采样**是 OPRO 的两个关键设计——移除任一项都显著降低效果。

## 6. 与其他 P 自修改工作的对比

P 自修改领域在 OPRO 之后涌现了多个工作（DSPy, PromptAgent, Promptbreeder, TextGrad 等）。本节做关键对比——这是 L4.1 的横向对比，也是 OPRO 在 B 自修改全谱系中的定位。

### 6.1 与 DSPy 的对比

Khattab 等人 2023-2024 年的 **DSPy**（*DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines*）是另一个 P 自修改的代表：

| 维度 | OPRO | DSPy |
|---|---|---|
| **优化对象** | 单个 prompt 字符串 | 整个 pipeline（含多 prompt、多模块） |
| **优化范式** | LLM-as-optimizer + 历史 | 编译器（编译时优化） |
| **修改粒度** | 整体 prompt 文本 | per-module instructions + few-shot |
| **学习信号** | 外部评估分数 | 程序输出与目标的差距 |
| **运行时修改** | 是（每次 inference 可重新优化） | 否（编译时优化，运行时固化） |
| **可验证性** | 无（字符串层面） | 部分（程序可被自动分析） |

DSPy 的核心创新是把 LLM 程序视为可编译对象——它在编译阶段用 teleprompter 算法（基于 bootstrap）优化每个 module 的 prompt 与 few-shot example，运行时不修改。OPRO 则是运行时持续修改 prompt——两者代表了 P 自修改的"编译时"与"运行时"两条路径。

**关键差异：运行时 vs 编译时**：
- OPRO：运行时持续优化（Inference time optimization）
- DSPy：编译时一次优化（Compile time optimization）

OPRO 更灵活（可适应任务变化），DSPy 更稳定（无运行时开销）。

### 6.2 与 PromptAgent 的对比

Cheng 等人 2024 年的 **PromptAgent**（*PromptAgent: Strategic Planning with Language Models Enables Expert-level Prompt Optimization*）用 MCTS（Monte Carlo Tree Search）做 prompt 优化：

| 维度 | OPRO | PromptAgent |
|---|---|---|
| **搜索算法** | LLM-as-optimizer 提议 | MCTS |
| **搜索结构** | 序列（每次一条路径） | 树（多条路径并行） |
| **探索 vs 利用** | 主要靠 temperature | UCB 显式平衡 |
| **可解释性** | 低（无明确搜索路径） | 高（树可被可视化） |
| **计算成本** | 中（每 iteration ~8 LLM 调用） | 高（MCTS 树扩展） |

PromptAgent 把 prompt 优化视为**策略博弈**——它用 MCTS 显式构造搜索树，每个节点是一个 prompt，边是 LLM-as-optimizer 的修改。OPRO 没有显式搜索结构，靠历史 + temperature 自发形成搜索方向。

PromptAgent 在专家级 prompt（如 medical, legal）上超越 OPRO——因为专家级 prompt 的"语义复杂度"高，需要系统性搜索而非启发式搜索。

### 6.3 与 Promptbreeder 的对比

Fernando 等人 2023 年的 **Promptbreeder**（*Promptbreeder: Self-Referential Self-Improvement Via Large Language Models*）用进化算法做 prompt 优化：

| 维度 | OPRO | Promptbreeder |
|---|---|---|
| **搜索算法** | LLM-as-optimizer | 进化算法（种群 + 突变 + 选择） |
| **种群大小** | 每次生成 8 个候选 | 50-100 个种群 |
| **修改维度** | prompt 文本 | prompt + 任务描述 + 突变操作符 |
| **多样性维持** | temperature 采样 | 适应度共享（fitness sharing） |
| **跨任务迁移** | prompt 字符串可迁移 | 进化种群可迁移 |

Promptbreeder 的关键创新是**自指突变（self-referential mutation）**——它让 LLM 同时优化 prompt 与"如何优化 prompt 的策略"（即 mutation operator）。这与 Gödel Agent 的 L4 元控制器修改思想相似，但 Promptbreeder 用进化算法实现而非形式验证。

### 6.4 与 TextGrad 的对比

Yuksekgonul 等人 2024 年的 **TextGrad** 把 prompt 优化视为"基于文本的梯度下降"——它让 LLM 生成"针对 prompt 的批评意见"（即"梯度"），再让另一个 LLM "应用梯度"到 prompt 上：

| 维度 | OPRO | TextGrad |
|---|---|---|
| **优化信号** | 评估分数 | LLM 生成的文本批评 |
| **更新方式** | LLM 重写整个 prompt | LLM 按批评修改 prompt |
| **可解释性** | 低 | 高（批评可被人类阅读） |
| **梯度来源** | 外部评估 | LLM-as-judge |

TextGrad 是 OPRO 与 prompt tuning 的中间形式——它保留"prompt 是字符串"的可读性，但用 LLM 生成的"批评"作为更新方向。

### 6.5 综合对比表

| 维度 | OPRO | DSPy | PromptAgent | Promptbreeder | TextGrad |
|---|---|---|---|---|---|
| **搜索算法** | LLM-as-optimizer | Bootstrap | MCTS | Evolutionary | LLM-as-critic |
| **修改粒度** | 整体 prompt | per-module prompt + few-shot | 整体 prompt | prompt + 任务 + 操作符 | 整体 prompt |
| **运行时 vs 编译时** | 运行时 | 编译时 | 运行时 | 运行时 | 运行时 |
| **可验证性** | 无 | 部分（程序） | 中（MCTS 树） | 无（种群） | 中（批评） |
| **可迁移性** | 高（字符串） | 中（pipeline） | 中（树） | 高（种群） | 高（字符串） |
| **可解释性** | 低 | 中 | 高 | 中 | 高 |
| **与 Gödel Agent 关系** | 第一代 P 修改 | 第二代（程序化） | 并行第一代（搜索结构化） | 并行第一代（进化） | 第一代（批评驱动） |

OPRO 在所有 P 自修改工作中是最简单的——它没有搜索结构、没有编译时优化、没有进化算法。但它的简洁性也是优势：**OPRO 是最容易复现、最容易教学的 P 自修改代表**。后续所有工作都可以视为 OPRO 的某方面深化。

### 6.6 开放问题表

| 问题 | 当前状态 | 本书视角 |
|---|---|---|
| OPRO 能在多任务上同时优化吗？ | 部分（meta-prompt 可容纳多任务） | 第 12 章多任务 P 自修改 |
| OPRO 能与其他 B 组件协同吗？ | 否（仅 P） | 第 16 章 P + M 协同 |
| OPRO 能抵御 prompt injection 吗？ | 不能（OPRO 本身可能被注入） | 第 22 章对抗鲁棒性 |
| OPRO 能跨 LLM 迁移吗？ | 部分（字符串可迁移） | 第 14 章跨模型迁移 |
| OPRO 有无验证机制？ | 无 | 第 23 章可验证 P 自修改（与 Gödel Agent 互补） |

## 7. 对本书的贡献

OPRO 在本书的理论体系中扮演**L4.1 P 自修改第一代的代表**。它是第 12 章"Prompt 自修改"的开端，也是第 16 章"协同自进化"中 P 维度修改的基础。

### 7.1 OPRO 作为 P 自修改的开端

本书第 12 章以 OPRO 为 P 自修改的开端——它的核心贡献是**把 prompt 优化重新定义为 LLM-as-optimizer 搜索**。这一重新定义开启了 2023-2024 年的 P 自修改研究浪潮（DSPy, PromptAgent, Promptbreeder, TextGrad）。

第 12 章以 OPRO 为锚点，把后续工作分类为：
- **运行时优化派**：OPRO, PromptAgent, Promptbreeder, TextGrad（运行时修改 P）
- **编译时优化派**：DSPy（编译时修改 P，运行时不改）
- **形式化优化派**：Gödel Agent L1（运行时 + 形式验证）

OPRO 是"运行时优化派"的起点。

### 7.2 OPRO 与 LLM-as-U 范式

OPRO 是**LLM-as-U 范式的最早实现**——它把 U 定义为"用 LLM 提议新 P 的函数"。这一范式在后续所有 B 自修改工作中被沿用：
- **MemGPT**（r-paper-004）：U 是 LLM-as-memory-manager（提议 M 修改）
- **A-MEM**（r-paper-005）：U 是 LLM-as-memory-organizer（提议 M 结构修改）
- **OPRO**（本笔记）：U 是 LLM-as-prompt-optimizer（提议 P 修改）
- **Gödel Agent L4**（r-paper-007）：U 是 LLM-as-meta-optimizer（提议 U 修改）

OPRO 是 LLM-as-U 的"第一个里程碑"——后续所有 B 自修改工作都借鉴 OPRO 的"用 LLM 作为搜索算子"思想。

### 7.3 OPRO 与 H5（治理必要性）

OPRO 是 H5 的**早期反例**——它完全没有 P 修改的验证/版本控制/回滚机制：

| 治理配置 | OPRO 的表现 | H5 的预期 |
|---|---|---|
| 无治理（OPRO 默认） | 高效率，**但接受退化修改** | $V_{\text{unver}}$ 高 |
| 加验证（OPRO + Z3，类 Gödel Agent L1） | 略低效率，零退化 | $V_{\text{ver}}$ 低 |

OPRO 的局限推动了 H5 研究——**没有验证的 P 自修改是有风险的**。这是后续 PromptAgent 与 Gödel Agent L1 引入验证机制的动机。

### 7.4 OPRO 与第 16 章"协同自进化"

本书第 16 章讨论 P/T/M/C 同时修改的协同自进化。OPRO 是 P 单组件优化的范式——它表明**单组件优化已经能带来显著提升**。这为协同优化提供了"基线"——如果协同优化不能超过单组件优化的简单相加，H2 假设被反驳。

具体地，第 16 章将实验：
- **Joint-P only**（OPRO，仅 P）：基线 1
- **Joint-P + M**（OPRO + A-MEM）：基线 2
- **Joint-P + M + T**（+ LATM 风格工具自修改）：基线 3
- **Joint-coordinated P + M + T + C**（形态协同自进化）：实验组

OPRO 在此作为**最基础的基线**——如果连单独 P 优化都超越不了，更复杂的协同肯定无效。

### 7.5 OPRO 与外部工具生态

OPRO 的最大工程价值是**用同构的 LLM-as-optimizer 接口，与各种 prompt 工程工具链兼容**：
- LangChain 可以把 OPRO 的 meta-prompt 作为 Chain-of-thought 包装为模块。
- LlamaIndex 可以把 OPRO 的元评估与检索提示结合。
- AutoGen 可以把 OPRO 集成到多 Agent 协商。

这一兼容性使 OPRO 在生产环境中被广泛采用——许多公司内部的 A/B 测试平台在借鉴 OPRO 的"通过 prompt 优化提升 LLM 输出"思想。

### 7.6 给读者的关键启示

1. **OPRO 是 P 自修改的第一代起点**：它是"让 LLM 作为优化器"的最早成功实现，所有后续 P 自修改工作都借鉴 OPRO 的"历史 + 多样性采样 + meta-prompt"三件套。
2. **OPRO 不能验证修改**：它的接受修改没有形式验证——这是后续 Gödel Agent L1（运行时 + Z3 验证）与 PromptAgent（MCTS + 显式搜索）发展的动机。
3. **OPRO 是 L4.1 而非 L5**：它仅修改 P，不修改 T/M/C。要达到 P/T/M/C 协同修改（L5.4 协同），需要后续工作的组合（OPRO + A-MEM + LATM + SICA）。
4. **OPRO 与 DSPy 是"运行时 vs 编译时"的两条路径**：两者并非互斥——可以先用 DSPy 编译粗略 prompt，再用 OPRO 在运行时微调。这是第 12 章"两阶段 P 优化"的方向。
5. **OPRO 的简洁是优势**：所有后来的 P 自修改工作（DSPy, PromptAgent, Promptbreeder, TextGrad）都比 OPRO 复杂。理解 OPRO 是理解后续工作的前提。
6. **OPRO 的局限推动了 H5**：OPRO 完全无验证机制，是 H5 假设的反例。这一反例推动了后续工作加入验证层。

OPRO 是从 L3（Reflexion 修改 M）到 L4（P 自修改）的关键跳跃。它让"操作形态 B = {P, T, M, C}"中的第一个组件 P 能够在运行时演化。但 P 自修改不是终点——本书第 16 章将讨论 **P + M + T + C 协同自进化**，这是 L4.4 与 L5.4 的目标。OPRO 是这一协同自进化的"P 维度基础"，与 r-paper-009 的 fang2025selfevolving survey 一起，构成第 16 章协同自进化实验的 P 维度的两条线。

## 参考文献

- yang2023opro: Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q. V., Zhou, D., & Chen, X. (2023). *Large Language Models as Optimizers*. ICLR 2024. arXiv:2309.03409. [$TRAE_REF](https://arxiv.org/abs/2309.03409)
- yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 见 r-paper-001。（OPRO 的起点——ReAct 循环是 P 冻结的代表）
- shinn2023reflexion: Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS 2023. 见 r-paper-002。（M 自修改，与 OPRO 的 P 自修改形成对照）
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT: Towards LLMs as Operating Systems*. arXiv:2310.08560. 见 r-paper-004。（M 自管理的代表，与 OPRO 互补）
- yin2024godelagent: Yin, S., et al. (2024). *Gödel Agent: A Self-Referential Framework for AGI*. arXiv:2410.04444. 见 r-paper-007。（OPRO 的第二代（P 自修改 + Z3 验证），与 OPRO 形成代际对比）
- khattab2024dspy: Khattab, O., et al. (2024). *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines*. ICLR 2024. （P 自修改的"编译时"路径代表）
- cheng2024promptagent: Cheng, M., et al. (2024). *PromptAgent: Strategic Planning with Language Models Enables Expert-level Prompt Optimization*. ICLR 2024.（MCTS-based P 优化）
- fernando2023promptbreeder: Fernando, C., et al. (2023). *Promptbreeder: Self-Referential Self-Improvement Via Large Language Models*. （进化算法 P 优化 + 自指突变）
- zhou2023l2l: Zhou, Y., et al. (2023). *Large Language Models Are Human-Level Prompt Engineers*. ICLR 2023.（与 OPRO 同期的 LLM-as-prompt-engineer 工作）
- fang2025selfevolving: Fang, W., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407. 见 r-paper-009。（综述视角，OPRO 在 B 自修改全谱系中的分类学来源）
