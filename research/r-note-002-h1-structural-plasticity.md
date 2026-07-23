---
note_id: r-note-002
title: "H1 假说的实证路径：结构可塑性"
authors: [MorphAgent Textbook Author]
created: 2026-07-22
updated: 2026-07-23
status: final
related_chapters: [Ch 11, Ch 12, Ch 19]
related_papers: [fang2025selfevolving, yang2024opro, khattab2024dspy, robeyns2025sica, yin2024godelagent, jimenez2024swebench, demsar2006statistical, yao2023react, packer2023memgpt, xu2025amem]
keywords: [structural-plasticity, H1, experiment-design, adaptation-regret, operational-morphology, statistical-power, type-I-error, type-II-error, bonferroni, wilcoxon, effect-size]
---

# r-note-002: H1 假说的实证路径：结构可塑性

> H1（结构可塑性）是操作形态学五个可证伪假设中最基础的一条——如果 H1 被反驳，后续的 H2（协同演化）、H3（形态适配）、H4（迁移收益）、H5（治理必要性）都失去了验证前提。本笔记为 H1 设计严格的实证路径：从形式化分解、统计检验选择、效应量预估、边界条件探测四个层面，构造一组"既不会伪阳性、也不会伪阴性"的实验。本笔记同时是第 19 章"MorphBench 评测方法论"的子设计之一，与第 12 章"自修改 prompt"的实证方案共享实验框架。

## 1. 动机：为什么 H1 需要格外严谨的实证设计

H1 的命题看似简单——"能让 Agent 改自己的 prompt/工具/记忆/代码，是否真的有用？"——但其实包含了三个相互交织的子问题：

1. **修改能力本身是否带来优势**：可修改 B 的 Agent 是否优于固定 B 的 Agent？
2. **修改能力的边际收益有多大**：在哪些环境条件下优势最大？哪些条件下优势消失？
3. **修改能力的代价是什么**：是否引入了新的失败模式（退化、震荡、不稳定）？

这三个子问题对应三类实验错误：

| 错误类型 | 在 H1 中的含义 | 严重程度 |
|---|---|---|
| **Type I 错误（伪阳性）** | 错误地拒绝 H0（认为 H1 成立），但实际 H1 不成立 | **极高**：会让学术界相信"自修改有价值"，导致资源错配 |
| **Type II 错误（伪阴性）** | 错误地接受 H0（认为 H1 不成立），但实际 H1 成立 | **高**：会抑制后续研究，错过自修改的潜力 |
| **Type III 错误（"答错问题"）** | 实验设计与 H1 的命题不匹配，得到"看似支持但实际不相关"的结论 | **中**：H1 是关于"期望后悔值"的统计命题，单次实验不能证伪 |

由于 H1 是后续四个假设的逻辑前提，**Type I 错误的成本显著高于 Type II**——一旦 H1 被伪证伪地支持，所有后续实验都将建立在错误前提上。因此 H1 的实验设计采用 **保守主义**：宁可让 β（Type II 错误率）高一些（必要时再补实验），也要让 α（Type I 错误率）极低（Bonferroni 校正后 α ≤ 0.0125）。

此外，H1 的实验设计还必须避开 **Type III 错误**——不能把"修改带来短期性能提升"等同于"H1 成立"。H1 的命题是**长期累积后悔值的统计差异**，而非"每次修改都更优"。本笔记反复强调这一点。

## 2. 核心论点：H1 是一个**统计性、长期性、方向性**命题

H1 的严格陈述：

> **H1（结构可塑性）**：当 LLM Agent 的操作形态 \(B = \{P, T, M, C\}\) 在运行时可被元控制器 \(U\) 修改时，其在 5 类环境干预（API 漂移、任务漂移、资源漂移、记忆冲突、安全干预）下的**期望累积后悔值**显著低于固定 \(B\) 的 Agent。

注意三个关键修饰：

- **"期望"**：H1 是统计性命题，单次实验不能证伪；需要 N 次独立运行后做假设检验。
- **"累积后悔值"**：H1 关心的是长期累积效果，而非单次修改的瞬时效果。
- **"5 类环境干预"**：H1 的成立依赖于环境变化的特定分布；如果环境始终平稳，H1 自然不成立（无修改必要）。

这三点决定了 H1 的实验设计必须：

1. **重复多次**（≥30 次独立运行）以估计期望；
2. **测量长视野**（≥100 步 episode）以累积后悔值；
3. **覆盖多类干预**（5 类均需要测试）以保证 H1 的鲁棒性。

## 3. 形式化分解

沿用第 11 章的形式化框架，H1 可以分解为三个可独立验证的子命题：

### 3.1 子命题 H1a：方向性

$$
H_{1a}: \mathbb{E}[R(B_{\text{adaptive}}, E)] - \mathbb{E}[R(B_{\text{fixed}}, E)] < 0
$$

即修改组的期望累积后悔值严格小于固定组。

### 3.2 子命题 H1b：效应量

$$
H_{1b}: \frac{\mathbb{E}[R(B_{\text{adaptive}}, E)] - \mathbb{E}[R(B_{\text{fixed}}, E)]}{\sigma_{\text{pooled}}} < -0.5
$$

即差异的 Cohen's $d$ 效应量大于 0.5（中等到大效应）。这一阈值来源于 Cohen 1988 的经典判据：$|d| > 0.2$ 为小效应，$|d| > 0.5$ 为中等效应，$|d| > 0.8$ 为大效应。本笔记选择 $d > 0.5$ 作为 H1b 的阈值——因为自修改 Agent 比固定 Agent 复杂得多，如果效应量小于 0.5，则"工程上不值得"采纳自修改架构。

### 3.3 子命题 H1c：鲁棒性

$$
H_{1c}: \text{Proportion}\{e \in E: R(B_{\text{adaptive}}, e) < R(B_{\text{fixed}}, e)\} \geq 0.7
$$

即在至少 70% 的环境干预场景中，修改组的后悔值更低。这一阈值对应 "modified-Pareto majority"——H1 不要求每次都赢，但要求"赢的概率显著高于输"。

### 3.4 综合判定

H1 成立的充分条件：H1a、H1b、H1c 同时成立，且三个独立检验均通过 Bonferroni 校正（$\alpha' = 0.05 / 3 \approx 0.0167$）。

| 子命题 | 检验方法 | 阈值 | 校正后 α |
|---|---|---|---|
| H1a | Wilcoxon 符号秩检验（双侧） | $p < \alpha'$ | 0.0167 |
| H1b | Cohen's $d$ 计算 + bootstrap CI | $d < -0.5$ 且 CI 不含 0 | — |
| H1c | 比例检验（$H_0: p = 0.5$） | $p < \alpha'$ | 0.0167 |

### 3.5 与第 11 章的关系

第 11 章的 H1 形式化是"期望后悔值的差小于 0"——本笔记把它分解为方向 + 效应量 + 鲁棒性三个子命题。这一分解不是"重新定义 H1"，而是**给出 H1 可被实验检验的具体可操作化形式**。第 11 章的 H1 是哲学陈述，本笔记的 H1a/H1b/H1c 是可检验的数学陈述。

## 4. 实验设计：五类环境干预 × 三组实验 × 多重统计校正

### 4.1 五类环境干预（自变量 E 的具体取值）

H1 的环境干预设计借鉴了 r-paper-013 (SWE-bench) 与 r-paper-014 (MLE-bench) 的"环境漂移"思路，但扩展到 LLM Agent 的特定场景：

| 干预类型 | 含义 | 实例 | 操作形态影响 |
|---|---|---|---|
| **API 漂移** | 工具函数签名/返回值变化 | 工具 T 的参数语义改变 | T 必须修改以保持可用性 |
| **任务漂移** | 用户任务的分布偏移 | 从简单查询到复杂多步任务 | P、T 都需修改 |
| **资源漂移** | 计算资源约束变化 | 上下文窗口从 8k → 128k | M 的管理策略需修改 |
| **记忆冲突** | 历史记忆与新事实矛盾 | 用户偏好"喜欢咖啡" → "喜欢茶" | M 必须更新 |
| **安全干预** | 新增安全约束 | 工具白名单变化、新增 PII 过滤规则 | P、T、C 协同修改 |

五类干预对应第 22 章"对抗性场景"的设计——但本章不要求 Agent 主动对抗，只要求它能**适应变化**。

### 4.2 实验组 1：单组件可塑性验证（对应 H1a 的"边际贡献"分解）

**目的**：回答"每种组件单独修改是否有效？"——这是 H1 的"基本案例"。

**设计**：在 5 类环境干预下，对比 5 种配置：

| 配置 | 修改能力 | 修改模式 |
|---|---|---|
| Frozen | 无修改（基线） | — |
| P-only | 仅修改 Prompt | OPRO 优化 P，T/M/C 冻结 |
| T-only | 仅修改 Tool | LATM-style 工具合成，T/P/M/C 冻结 |
| M-only | 仅修改 Memory | A-MEM 修改 M，P/T/C 冻结 |
| C-only | 仅修改 Code | SICA 修改 C，P/T/M 冻结 |

每种配置在 5 类干预下各跑 30 次独立运行（共 5×5×30 = 750 次实验），记录累积后悔值 $R$ 与恢复时间（首次达到 frozen baseline 性能所需的 episode 数）。

**统计检验**：对每种配置 vs Frozen 做 Wilcoxon 符号秩检验（配对设计：相同随机种子下的两组配对）。Bonferroni 校正后 $\alpha = 0.05 / 4 = 0.0125$（4 个单组件组）。

**预期结果**：若 H1 成立，至少 3/4 的单组件组在 $R$ 上显著优于 Frozen，且至少 2/4 的组达到 $d < -0.5$ 的效应量阈值。

**伪结果诊断**：如果只有 1/4 的单组件组显著，则 H1 可能被弱化——说明"修改能力"本身不是 H1 的核心，"联合修改"才是。**这一诊断会直接推动 H2 的研究**。

### 4.3 实验组 2：可塑性速度验证（频率维度）

**目的**：回答"修改越频繁，后悔值越低吗？"——验证 H1 的隐含时间动态假设。

**设计**：控制元控制器 U 的修改频率 $f$：

| 频率设置 | 含义 |
|---|---|
| $f = 1$ | 每步修改一次（最频繁） |
| $f = 5$ | 每 5 步修改一次 |
| $f = 20$ | 每 20 步修改一次 |
| $f = \infty$ | 从不修改（基线 = Frozen） |

在 5 类环境干预下，分别测量累积后悔值 $R(f)$ 与修改收益率 $\rho = \frac{\text{正向修改次数}}{\text{总修改次数}}$。

**预期结果**：存在最优频率 $f^*$，使 $R(f)$ 最小。$f$ 过小（频繁修改）导致震荡——每次修改可能"修正"前一次修改，产生相互抵消；$f$ 过大（稀疏修改）导致反应迟钝——错过干预的早期信号。

**形式化**：

$$
R(f) = R_{\text{intrinsic}} + \alpha \cdot \mathbb{1}[f < f^*] \cdot (\text{震荡}) + \beta \cdot \mathbb{1}[f > f^*] \cdot (\text{迟钝})
$$

其中 $R_{\text{intrinsic}}$ 是不可消除的内在后悔值（环境固有随机性），$\alpha, \beta$ 是震荡与迟钝的惩罚系数。

**理论意义**：这一实验可以估计元控制器 U 的"反应时间常数"——它是操作形态学中"学习率"概念的具体化。

### 4.4 实验组 3：退化案例验证（H1 的反向边界）

**目的**：探测 H1 在何时**不**成立——这是 H1 的"边界条件"研究。

**设计**：专门追踪每次修改后的性能变化 $\Delta V = V(B_{t+1}) - V(B_t)$，统计：

- **正向修改率** $\rho^+$：$\Delta V > 0$ 的修改占比；
- **退化事件分布**：$\Delta V < 0$ 的修改在 5 类干预中的分布；
- **退化幅度分布**：$|\Delta V|$ 在不同修改类型（C 修改 vs M 修改 vs ...）下的分布。

**统计建模**：把 $\Delta V$ 建模为混合分布：

$$
\Delta V \sim \pi \cdot \mathcal{N}(\mu^+, \sigma^2) + (1 - \pi) \cdot \mathcal{N}(\mu^-, \sigma^2)
$$

其中 $\pi$ 是正向修改率，$\mu^+$、$\mu^-$ 分别是正/负向修改的均值。H1 成立要求 $\pi \cdot \mu^+ > |(1 - \pi) \cdot \mu^-|$（期望值非负）。

**何时 H1 可能失败**——边界条件预测：

| 边界条件 | 预测的 H1 表现 | 原因 |
|---|---|---|
| **环境平稳** | H1 退化（修改组可能略差于 Frozen） | 无修改必要，引入的修改本身有成本 |
| **修改频率过高** | H1 退化（震荡） | 元控制器自身成为性能瓶颈 |
| **LLM 元推理能力弱** | H1 退化 | U 不能做出有意义的修改决策 |
| **修改范围过窄** | H1 部分成立（P-only 显著但 T-only 不显著） | 不同组件的可塑性收益不均 |
| **环境漂移过快** | H1 退化（反应跟不上） | U 的反应时间常数 > 环境变化速率 |
| **基线已经接近最优** | H1 退化（修改空间小） | 见 r-note-001 的"天花板"问题 |

**理论意义**：这一实验组把 H1 从"是/否"命题升级为"在什么条件下成立/不成立"的精细命题——这才是科学可证伪的真正含义。

### 4.4.1 伪代码：单次修改的累积后悔值追踪

```python
class H1Experiment:
    def __init__(self, env_type, intervention_timing, intervention_type,
                 intervention_strength, n_episodes=100, n_replicates=30):
        self.env = Environment(env_type=env_type)
        self.intervention_timing = intervention_timing
        self.intervention_type = intervention_type
        self.strength = intervention_strength
        self.n_episodes = n_episodes
        self.n_replicates = n_replicates

    def run_single_replicate(self, agent, seed):
        """一次独立运行, 记录累积后悔值与每次修改的 delta V"""
        rng = np.random.default_rng(seed)
        cumulative_regret = 0.0
        modification_log = []  # [(t, B_t, B_{t+1}, delta_V), ...]

        for t in range(self.n_episodes):
            # 应用干预 (在特定时机)
            if t == self.intervention_timing:
                self.env.apply_intervention(
                    type=self.intervention_type,
                    strength=self.strength
                )

            # Agent 选择动作
            state = self.env.get_state()
            optimal_action = self.env.get_optimal_action(state)
            agent_action = agent.act(state)

            # 单步后悔值
            optimal_value = self.env.get_value(state, optimal_action)
            actual_value = self.env.get_value(state, agent_action)
            step_regret = optimal_value - actual_value
            cumulative_regret += step_regret

            # 如果是 adaptive agent, 记录修改
            if hasattr(agent, 'meta_controller'):
                if agent.meta_controller.should_modify():
                    old_B = agent.snapshot_B()
                    new_B, accepted = agent.meta_controller.modify(
                        feedback=step_regret,
                        env=self.env
                    )
                    if accepted:
                        new_value = self.env.evaluate_B(new_B)
                        delta_V = new_value - agent.value_estimate
                        modification_log.append((t, old_B, new_B, delta_V))

        return cumulative_regret, modification_log

    def analyze_regret_curve(self, regrets):
        """分析累积后悔值曲线的形态"""
        # 累积后悔值的渐近增长率 (sub-linear 意味着 H1 成立)
        final_growth_rate = (regrets[-1] - regrets[-len(regrets)//4]) / (len(regrets)*3//4)

        # 计算恢复时间: 首次回到 frozen baseline 性能所需 episode 数
        frozen_baseline_regret = self.compute_frozen_baseline_regret()
        recovery_time = self.find_recovery_time(regrets, frozen_baseline_regret)

        return {
            "cumulative_regret": regrets[-1],
            "asymptotic_growth_rate": final_growth_rate,
            "recovery_time": recovery_time,
        }
```

### 4.5 统计检检与多重比较校正

H1 的实验涉及多次假设检验，必须做多重比较校正。本笔记选择 Bonferroni 校正（保守）而非 Holm-Bonferroni 或 FDR（更宽松），理由是 H1 是后续四个假设的逻辑前提，Type I 错误的代价极高。

| 检验 | 检验方法 | α 原始 | α 校正 | 备注 |
|---|---|---|---|---|
| 单组件 vs Frozen（4 组） | Wilcoxon 符号秩 | 0.05 | 0.0125 | Bonferroni |
| 频率效应（3 个频率 vs ∞） | Kruskal-Wallis + Dunn | 0.05 | 0.0083 | Bonferroni |
| 退化事件分布（5 类干预） | Chi-squared | 0.05 | 0.01 | Bonferroni |
| 综合 H1a/H1b/H1c 检验 | 三独立检验 | 0.05 | 0.0167 | Bonferroni |

**统计功效分析**：在 $\alpha = 0.0125$、期望 $d = 0.5$、n = 30 次重复下，Wilcoxon 符号秩检验的统计功效约为 0.78。**这一功效略低于 0.80 的常规阈值**——这是为了避免在 LLM 实验上消耗过多算力。如果关键实验的统计功效 < 0.7，应增加重复次数到 n = 50。

### 4.6 与 r-paper-008 / r-paper-009 的对照

- **OPRO**（r-paper-008）只修改 P，且无环境干预——H1 实验设计借鉴 OPRO 的"prompt 优化 pipeline"，但加上了环境干预维度。
- **fang2025selfevolving**（r-paper-009）的综述中提到了"self-evolution under environment shift"，但没有给出具体实验方案。本笔记填补了这一空白。

## 5. 实验预期与效应量预估

### 5.1 H1 成立的预期效应量

参考已有的 LLM 自修改实验数据（H1 已经被部分工作间接支持），预估 H1 的效应量：

| 实验组 | 预期 $d$（Cohen's） | 预期显著性 | 备注 |
|---|---|---|---|
| P-only vs Frozen | $d \in [-0.3, -0.6]$ | 部分显著（受 LLM 能力影响） | OPRO 在 GSM8K 上有约 8-15% 提升 |
| T-only vs Frozen | $d \in [-0.4, -0.7]$ | 大概率显著 | LATM 在工具创建上有 20%+ 提升 |
| M-only vs Frozen | $d \in [-0.5, -0.8]$ | 大概率显著 | A-MEM 在 LoCoMo 上提升 20% |
| C-only vs Frozen | $d \in [-0.6, -1.0]$ | 显著 | SICA 在 HumanEval 上提升 17% |
| Joint (P+T+M+C) vs Frozen | $d \in [-0.8, -1.5]$ | 强显著 | 协同修改预期超过独立 |

**关键预测**：单组件修改的效应量普遍处于中等水平（$d \approx -0.5$），联合修改应达到大效应（$d < -0.8$）。如果联合修改仅达到 $d \approx -0.5$，则说明 H2（协同演化）可能不成立——联合修改没有超过各组件独立修改之和。

### 5.2 Type II 错误的预防

为避免 Type II 错误（漏检真实效应），本笔记采用三个策略：

1. **配对设计**：相同随机种子下的修改组与冻结组配对，显著提升 Wilcoxon 检验的功效。
2. **多任务覆盖**：5 类环境干预各跑 30 次（而非单任务跑 150 次），提升 H1 鲁棒性的统计功效。
3. **效应量 CI 报告**：除 p 值外，报告 Cohen's $d$ 的 95% bootstrap CI——如果 CI 下界包含 $-0.5$，则效应量"至少为中等"。

### 5.3 Type I 错误的预防

为避免 Type I 错误（错误支持 H1），本笔记采用三个策略：

1. **Bonferroni 校正**：把 $\alpha = 0.05$ 校正为 $\alpha = 0.0125$。
2. **预注册（preregistration）**：在实验前公开实验方案、假设、分析计划，避免事后选择性报告（p-hacking）。
3. **跨模型验证**：在 GPT-4 与 Llama-3 上分别跑实验——如果仅在 GPT-4 上支持 H1 而 Llama-3 不支持，则 H1 的稳健性存疑。

## 6. 与本书的关系

### 6.1 与第 11 章的关系

第 11 章是 H1 的理论定义来源。本笔记是 H1 的**实验设计细化**——把第 11 章的哲学陈述转化为可检验的数学命题（H1a/H1b/H1c）和可执行的实验方案。如果本笔记的实验结果与第 11 章的理论预期一致，则第 11 章得到验证；如果不一致，则需要修订第 11 章的 H1 形式化。

### 6.2 与第 12 章的关系

第 12 章"P-only"实验组的实现依据来源于 OPRO（r-paper-008）与 DSPy（Khattab et al. 2024）。本笔记的 P-only 配置直接调用第 12 章的代码实现，并复用其 prompt 优化 pipeline。

### 6.3 与第 19 章的关系

第 19 章"MorphBench 评测方法论"包含 5 干预 × 7 组 × 5 指标的评测框架。本笔记的 3 组实验是 MorphBench 的子集：

- 实验组 1 → MorphBench 的 "P-only / T-only / M-only / C-only" 四组；
- 实验组 2 → MorphBench 的 "frequency sweep"；
- 实验组 3 → MorphBench 的 "regression tracking"。

第 19 章提供了评测的通用工具（H1 实验调用它），本笔记提供 H1 的具体实验配置。

### 6.4 与第 22 章的关系

第 22 章"安全与对抗"提出 4 类安全威胁。本笔记实验组 3 的"安全干预"子组与第 22 章直接相关——当施加安全干预时（如工具白名单变化），H1 是否仍然成立？如果 H1 在安全干预下被弱化，说明修改能力在某些场景下会引入新的风险，需要治理机制。

### 6.5 与第 23 章的关系

第 23 章"可验证自修改"提供验证三重保障（Sandbox + Property Tests + Formal Verification）。本笔记的所有实验都默认开启 Sandbox——H1 的实验组不挑战验证机制（那是 H5 的领域）。第 23 章的验证机制是 H1 实验的"安全前提"。

### 6.6 与其他论文的关系

- **r-paper-001（ReAct）**：提供 Agent 的基础循环，H1 实验的 baseline 配置（Frozen）使用 ReAct。
- **r-paper-002（Reflexion）**：提供 M 修改的第一个例子，H1 实验组 M-only 参考 Reflexion。
- **r-paper-003（Toolformer）**：提供 T 修改的第一个例子，H1 实验组 T-only 参考 Toolformer。
- **r-paper-004（MemGPT）**：提供 M 修改的高级形式，H1 实验组 M-only 也参考 MemGPT。
- **r-paper-005（A-MEM）**：提供 M 修改的"广义"形式（含结构），H1 实验组 M-only 主要参考 A-MEM。
- **r-paper-006（SICA）**：提供 C 修改的代表，H1 实验组 C-only 直接基于 SICA。
- **r-paper-007（Gödel Agent）**：提供 B = {P, T, M, C} 联合修改的代表，H1 实验的 "Joint" 配置参考 Gödel Agent。
- **r-paper-008（OPRO）**：提供 P-only 修改的代表。
- **r-paper-009（selfevolving 综述）**：提供自修改 Agent 的分类学。
- **r-paper-013（SWE-bench）**：提供环境漂移的真实任务。
- **r-paper-014（MLE-bench）**：提供环境漂移的另一种真实任务。

## 7. 开放问题

### 7.1 最优后悔值的下界

Human-oracle（人类专家实时介入）组提供一个上界参考——它的累积后悔值是"理论最优"，但理论下界仍未知。下界可能与环境的 non-stationarity 程度（环境变化的快慢、幅度、可预测性）有关。H1 的真正意义不在于"自适应优于固定"，而在于"自适应是否接近理论下界"。

### 7.2 单组件修改的"天花板"

如果 P-only 的后悔值已经接近 0，则联合优化的边际收益可能很小，H2 可能被弱化。这一边界条件需要在实验中明确探测。

### 7.3 修改频率与 LLM 成本的权衡

更频繁的修改需要更多 LLM 调用。在生产环境中，"成本效益比"是一个重要指标。本笔记没有量化这一权衡——需要进一步引入"cost-adjusted regret"（成本调整后悔值）。

### 7.4 跨 LLM 的泛化性

H1 在 GPT-4 上成立，在 Llama-3、Claude-3 上是否成立？不同 LLM 的元推理能力差异会显著影响 H1 的效应量。如果 H1 仅在强模型上成立，则 H1 的实用性受限。

### 7.5 长视野（> 1000 episode）的稳定性

本笔记的实验设计上限为 100 episode。在生产环境中，Agent 可能运行数千 episode。H1 在长视野下是否仍然成立？是否存在"晚期的退化"？这是 5 年路线图（见 r-note-010）中的关键问题。

### 7.6 与 H5（治理必要性）的张力

H1 默认开启 Sandbox 验证。如果关闭 Sandbox，H1 是否仍然成立？答案是"可能不成立"——没有验证的自修改可能引入灾难性 bug，使后悔值反而更高。**这一假设将在 H5 的实验中得到验证**。

## 8. H1-H5 映射表

| 假设 | H1 的角色 | 检验状态 |
|---|---|---|
| **H1 结构可塑性** | **本笔记的核心** | 待验证（实验方案已设计） |
| **H2 协同演化** | H1 的扩展：联合修改 | 依赖 H1 成立 |
| **H3 形态适配** | H1 的应用：不同环境的修改 | 依赖 H1 成立 |
| **H4 迁移收益** | H1 的延伸：跨任务的修改 | 依赖 H1 成立 |
| **H5 治理必要性** | H1 的前提：无治理的修改 | 与 H1 互为对照 |

## 9. 笔记元信息

- **状态**：final
- **可被引用方式**：`{cite:p}` 风格在第 19 章、第 16 章中引用本笔记作为 MorphBench H1 子实验的设计依据。
- **可被复现方式**：实验代码位于 `experiments/exp-11-morphological-plasticity/` 与 `experiments/exp-18-joint-evolution/`，共享 `_shared/metrics.py` 中的后悔值计算函数。
- **作者注**：本笔记是 H1 实验设计的唯一权威来源。如果未来 H1 实验结果与本笔记的预期不一致，需要同步修改本笔记的预期效应量表与第 11 章的 H1 形式化。

## 参考文献

1. fang2025selfevolving: Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407. 见 r-paper-009。（H1 实验的整体框架参考）
2. yang2024opro: Yang, C., et al. (2024). *Large Language Models as Optimizers (OPRO)*. ICLR. 见 r-paper-008。（P-only 配置的实现基础）
3. khattab2024dspy: Khattab, O., et al. (2024). *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines*. ICLR.（P-only 配置的备选实现）
4. robeyns2025sica: Robeyns, M., et al. (2025). *SICA: Self-Improving Coding Agent*. NeurIPS. 见 r-paper-006。（C-only 配置的直接来源）
5. yin2024godelagent: Yin, X., et al. (2024). *Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement*. arXiv:2410.04444. 见 r-paper-007。（Joint 配置的直接来源）
6. jimenez2024swebench: Jimenez, C. E., et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR. 见 r-paper-013。（环境漂移任务）
7. demsar2006statistical: Demsar, J. (2006). *Statistical Comparisons of Classifiers over Multiple Data Sets*. JMLR, 7, 1-30.（多数据集统计检验方法论）
8. yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR. 见 r-paper-001。（Baseline Agent 架构）
9. packer2023memgpt: Packer, C., et al. (2023). *MemGPT: Towards LLMs as Operating Systems*. arXiv:2310.08560. 见 r-paper-004。（M-only 配置的备选实现）
10. xu2025amem: Xu, W., et al. (2025). *A-MEM: Agentic Memory for LLM Agents*. NeurIPS. 见 r-paper-005。（M-only 配置的主要参考）
11. cohen1988statistical: Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*（效应量阈值的方法论来源）