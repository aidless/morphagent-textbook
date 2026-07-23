---
note_id: r-note-011
title: POMDP 与 LLM Agent 的对应：从信念状态到操作形态策略改进
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 2, Ch 17]
related_papers: [yao2023react, shinn2023reflexion, packer2023memgpt, xu2025amem, fang2025selfevolving, r-note-001, r-note-002, r-note-009, r-exp-002]
keywords: [POMDP, belief state, short-term memory, policy refinement, meta-controller, non-Markovian, LLM agent, operational morphology]
---

# r-note-011: POMDP 与 LLM Agent 的对应：从信念状态到操作形态策略改进

> POMDP 为 LLM Agent 提供了一个有用但不完备的控制论骨架：短期记忆可近似信念状态，LLM 输出可视为行动，工具返回构成观察，而操作形态自修改则是对策略类本身的在线改写。

## 1. 核心命题

LLM Agent 并不直接接触“世界状态”。它看到的是用户消息、网页片段、工具返回、记忆检索结果与执行错误；这些观察可能不完整、带噪声、被延迟，甚至被对抗性污染。因此，把 Agent 形式化为完全可观察的 Markov Decision Process（MDP）会掩盖最关键的工程事实：Agent 必须根据有限历史推断当前情境，并在不确定性下行动。

本笔记的核心命题是：**一个具备工具与短期记忆的 LLM Agent，可以近似建模为 POMDP 控制器；但这种对应只在状态表示、时间边界和策略稳定性被明确约束时成立。** 其工程映射为：

| POMDP 元素 | LLM Agent 对应物 | 关键保留意见 |
|---|---|---|
| latent state \(s_t\) | 用户真实意图、环境状态、工具内部状态 | 通常不可直接观测，且可能随外部系统异步变化 |
| observation \(o_t\) | 用户输入、tool feedback、检索片段、错误码 | 可能包含不可信指令或摘要损失 |
| belief \(b_t\) | short-term memory / working context 的状态估计 | context 是文本，不天然是归一化概率分布 |
| action \(a_t\) | LLM 输出：回复、函数调用、代码 patch、记忆写入 | 自然语言输出常同时承担行动与内部表征 |
| policy \(\pi\) | 模型、system prompt、tool schema、控制循环的组合 | 不等于模型权重本身，而由整个 \(B=\{P,T,M,C\}\) 实现 |
| reward \(r_t\) | 成功信号、测试通过率、成本、安全违规惩罚 | 经常稀疏、延迟、由代理指标构造 |

“belief state ≈ short-term memory”必须理解为**功能同构**而不是数学恒等。短期记忆的功能是压缩历史、保留与行动有关的信息；POMDP belief 的功能是给出隐藏状态的后验分布。两者只有在短期记忆足以支撑下一步决策时才近似等价。

## 2. 形式化

### 2.1 标准 POMDP

有限 POMDP 定义为七元组：

\[
\mathcal{P}=(\mathcal{S},\mathcal{A},\mathcal{O},\mathcal{T},\Omega,R,\gamma)
\]

其中 \(\mathcal{S}\) 是隐藏状态空间，\(\mathcal{A}\) 是行动空间，\(\mathcal{O}\) 是观察空间；\(\mathcal{T}(s'\mid s,a)\) 为状态转移概率；\(\Omega(o\mid s',a)\) 为观察模型；\(R(s,a)\) 为奖励；\(\gamma\in[0,1)\) 为折扣因子。Agent 不知道 \(s_t\)，只能维护 belief：

\[
b_t(s)=\Pr(s_t=s\mid h_t),\qquad h_t=(o_0,a_0,o_1,\ldots,a_{t-1},o_t)
\]

采取行动 \(a_t\) 并获得观察 \(o_{t+1}\) 后，Bayesian belief update 为：

\[
b_{t+1}(s')=\eta\,\Omega(o_{t+1}\mid s',a_t)\sum_{s\in\mathcal{S}}\mathcal{T}(s'\mid s,a_t)b_t(s)
\]

其中 \(\eta\) 是归一化常数。POMDP 的目标是寻找 policy \(\pi(a\mid b)\)，最大化：

\[
J(\pi)=\mathbb{E}_{\pi}\left[\sum_{t=0}^{\infty}\gamma^tR(s_t,a_t)\right]
\]

Belief-MDP 将部分可观察问题转换为连续 belief 空间上的完全可观察问题。对 LLM Agent 而言，这一转换的价值不在于求精确最优解，而在于迫使设计者区分：**真实状态、可见证据、内部状态估计、行动和反馈**。

### 2.2 从 belief 到短期记忆

设 Agent 的短期记忆为文本或结构化对象 \(m_t^{S}\)，由压缩器 \(g\) 从历史生成：

\[
m_t^{S}=g(h_t;P_t,M_t,C_t)
\]

再由解释器 \(q_\theta\) 将其映射为隐式 belief：

\[
\hat b_t(s)=q_\theta(s\mid m_t^{S})
\]

实际行动由：

\[
a_t\sim\pi_{B_t}(a\mid m_t^{S},o_t),\qquad B_t=\{P_t,T_t,M_t,C_t\}
\]

产生。这里 \(q_\theta\) 通常不会显式输出概率。它可能只输出一句摘要：“门似乎锁着，钥匙可能在桌上”。因此可用**决策充分性**代替分布等价：若对所有可行动作，其期望价值排序基本一致，则 \(m_t^S\) 是 belief 的充分近似：

\[
\arg\max_a Q(\hat b_t,a)=\arg\max_a Q(b_t,a)
\]

这比“文本记忆就是概率分布”更严格，也更可检验。它允许摘要遗漏与当前行动无关的细节，但不能遗漏改变动作排序的信息。

### 2.3 三种 belief update 实现

| 更新方式 | 形式 | 适用情形 | 失败点 |
|---|---|---|---|
| 显式 Bayes | 使用 \(\mathcal{T},\Omega\) 计算后验 | 状态小、模型已知 | 开放环境中模型通常未知 |
| LLM 摘要更新 | \(m_{t+1}=\text{LLM}(m_t,a_t,o_{t+1})\) | 对话、网页与混合文本 | 无归一化、易被注入、可能遗忘 |
| 混合更新 | 符号状态 + LLM 自由文本 | 工作流、诊断、规划 | schema 设计与文本对齐成本高 |

推荐使用混合更新：把关键变量（权限、预算、任务阶段、事实置信度）保存在 typed state 中，把难以枚举的信息保存在自由文本中。

```python
@dataclass
class BeliefState:
    task: str
    hypotheses: list[tuple[str, float]]
    verified_facts: dict[str, str]
    pending_questions: list[str]
    budget_left: float
    trace_summary: str


def update_belief(b, action, observation, transition_model, llm):
    predicted = transition_model.predict(b, action)
    trusted, untrusted = split_by_provenance(observation)
    posterior = bayes_update(predicted.hypotheses, trusted)
    proposal = llm.summarize(predicted, untrusted)
    proposal = validate_against_schema(proposal)
    return merge(posterior, proposal, preserve_provenance=True)
```

关键不是让 LLM“记住更多”，而是让更新函数保留 provenance、矛盾与置信度。若把 tool observation 无条件拼入 context，Agent 得到的不是 belief update，而是“最近输入覆盖状态”的脆弱缓存。

### 2.4 映射到 \(B=\{P,T,M,C\}\)

POMDP policy 不应只映射为 base LLM。实际策略由四个组件联合实现：

\[
\pi_{B}(a\mid b)=\pi(a\mid b;P,T,M,C)
\]

- \(P\) 决定目标解释、推理格式和指令优先级；
- \(T\) 决定可用行动集合及其参数化；
- \(M\) 决定历史如何被压缩、检索与注入；
- \(C\) 决定循环、重试、终止与验证逻辑。

因而 H1“结构可塑性”可以重写为**policy-class refinement**。元控制器 \(U\) 根据轨迹和奖励修改 \(B\)：

\[
B_{k+1}=U(B_k,\tau_k,r_k,\mathcal{C}),
\qquad \Pi_{k+1}=\{\pi_{B_{k+1}}\}
\]

这不是普通 POMDP 内的单步 action，而是跨 episode 改变 policy 的元动作。更准确的模型是双时间尺度系统：内层在固定 \(B_k\) 下行动，外层根据 episode 反馈修改 \(B_k\)。

\[
\begin{aligned}
&\text{inner: } a_t\sim\pi_{B_k}(a\mid b_t),\\
&\text{outer: } B_{k+1}=U(B_k,\tau^{(k)},R^{(k)})
\end{aligned}
\]

如果把两层混在同一 POMDP 中，就会错误地把“调用搜索工具”和“改写搜索工具协议”视为同类动作。后者改变未来行动空间，应建模为 meta-POMDP、Bayes-adaptive POMDP 或非平稳控制问题。

## 3. 方法细节与实验设计

### 3.1 具体实例：故障诊断 Agent

假设 Agent 排查 API 失败。隐藏状态为 \(S=\{\text{auth},\text{rate-limit},\text{schema-drift},\text{network}\}\)。第一次观察是 HTTP 400，belief 可能为：

\[
b_0=(0.15,0.10,0.60,0.15)
\]

Agent 调用 `inspect_schema`，工具返回“字段 `user_id` 已改为 `account_id`”。更新后 \(b_1(\text{schema-drift})\) 接近 1，Agent 生成 patch。若 patch 成功，内层策略完成任务；若多个 episode 都遇到相同漂移，外层 \(U\) 可修改 \(T\) 的 schema 或 \(C\) 的兼容层。这说明 observation 既更新短期 belief，也可累积为形态修改证据。

### 3.2 与传统 RL、MDP 和 ReAct 的比较

| 维度 | MDP / 传统 RL | POMDP | ReAct（r-paper-001） | 操作形态 Agent |
|---|---|---|---|---|
| 状态可见性 | 假设 \(s_t\) 可见 | 只见 \(o_t\) | 只见文字 observation | 只见多源观察并维护 M |
| 状态表示 | 数值 state | 概率 belief | prompt 中的轨迹 | typed state + context + long-term M |
| 策略学习 | 参数更新、value/policy gradient | belief policy | 通常冻结模型、prompt 驱动 | \(U\) 可修改 P/T/M/C |
| 奖励 | 频繁或可模拟 | 可延迟 | 常见成功/失败 | 性能、成本、安全多目标 |
| 平稳性 | 通常假设平稳 | 通常假设平稳 | 工具与网页可变化 | B 与环境都可能变化 |
| 可验证性 | 有成熟理论 | 精确解昂贵 | 轨迹可读但非概率校准 | 修改需版本、验证与回滚 |

ReAct 的 Thought–Action–Observation 循环与 POMDP filter–act 循环结构相似，但 Thought 不是 belief 的可靠序列化。它可能包含臆测、策略说明、计划和事实，且这些类别没有被类型系统分隔。r-paper-002 Reflexion 把失败摘要写入 M，扩展了跨 episode 状态；r-paper-004 MemGPT 用分页保持历史；r-paper-005 A-MEM 用链接拓扑提供结构化关联。它们都在增强 belief approximation，但没有自动获得 POMDP 的概率语义。

### 3.3 exp-02-pomdp-claim 的证据边界

`experiments/exp-02-pomdp-claim/` 构造了五个门、钥匙、狗与客厅的微型场景，向 mock LLM 提供 `memory_prompt`，比较实际行动与预设最优行动。`results.json` 记录 belief consistency 与 action consistency 均为 100%。该结果只能证明：**在确定性关键词策略下，行动是给定记忆文本的函数**。它不能证明：

1. Agent 对隐藏状态维护了概率分布；
2. 记忆更新符合 Bayes rule；
3. 不完整或错误 belief 下仍能校准不确定性；
4. LLM 的成功来自 belief，而非关键词到动作的硬编码；
5. 五个样本具有统计外推性。

更严格的后续实验应设置 factorial design：完整记忆、缺失记忆、矛盾记忆、顺序扰动、对抗 observation 五组；比较显式 Bayes、结构化 state、自由文本摘要和无记忆 baseline。指标至少包括 action accuracy、negative log-likelihood、Brier score、belief calibration error 与 cumulative regret。特别要区分“belief 错但碰巧行动对”的 lucky wrong。

```python
for env_seed in seeds:
    trajectory = sample_hidden_state_process(env_seed)
    for memory_mode in ["none", "text", "typed", "bayes"]:
        agent = build_agent(memory_mode)
        for corruption in ["clean", "missing", "contradictory", "injected"]:
            result = evaluate(agent, trajectory, corruption)
            log(result.action_accuracy, result.brier, result.regret)
```

## 4. 与本书其他章节/笔记的关系

| 交叉引用 | 本笔记提供的连接 |
|---|---|
| Ch 2 | 将“Agent 循环”从可观察状态机提升为部分可观察决策过程 |
| Ch 17 | 将元控制器 \(U\) 定义为跨 episode 的 policy refinement，而非普通 action selector |
| r-note-001 | \(B=\{P,T,M,C\}\) 是策略实现载体；B 修改即策略类改变 |
| r-note-002 | H1 可用 adaptation regret 比较 adaptive-B 与 frozen-B |
| r-note-003 | P/T/M/C 联合修改对应 belief、action space 与 transition handler 的协同重构 |
| r-note-004 | 不可信 observation 会污染 belief；安全不变量约束更新与策略修改 |
| r-note-008 | morphology landscape 可视为 policy-class landscape，而非单一参数空间 |
| r-note-009 | L0-L1 主要执行固定策略；L2-L5 逐步获得修改策略实现的权限 |
| r-paper-001 | ReAct 提供 observation-action 轨迹，但不保证 belief calibration |
| r-paper-004/005 | MemGPT 与 A-MEM 分别增强 belief 的时间跨度和关系结构 |
| r-paper-023 | GAIA 可作为部分可观察、长视野工具任务的外部评测环境 |

### L0-L5 定位

- **L0**：固定 ReAct policy，历史只在当前 context 中；可视为无显式 belief filter 的 POMDP controller。
- **L1**：引入检索与外部 M，改善观察覆盖，但 \(B\) 仍冻结。
- **L2**：修改单一组件，例如优化 P 或 M；相当于局部 policy refinement。
- **L3**：修改至少两个组件，可同时改变 belief representation 与 action selection。
- **L4**：修改完整 \(B\)，对应 system-level policy-class search。
- **L5**：在治理等级 \(\gamma=3\) 下协同修改 \(B\)，必须审计 belief 更新、策略变化和安全约束。

## 5. 局限与开放问题

### 5.1 LLM 的非 Markov 性

POMDP 要求给定当前隐藏状态和行动，下一状态与更早历史条件独立；belief 是历史的充分统计量。LLM Agent 常违反这一条件：基础模型参数包含训练语料先验；采样器有随机状态；provider 可能更新模型；tool service 有未暴露 session；long-term memory 检索依赖整个数据库；context truncation 的方式依赖历史长度。于是两个表面相同的 \(m_t^S\) 可能产生不同结果。

可把状态扩展为：

\[
\tilde s_t=(s_t,\theta_t,B_t,D_t,z_t)
\]

其中 \(\theta_t\) 是模型版本，\(D_t\) 是长期记忆库，\(z_t\) 是服务与采样器隐状态。但扩展后状态几乎不可枚举，POMDP 的解释力上升、可求解性下降。POMDP 在此更像**分析语言**，不是可直接求精确解的算法说明。

### 5.2 Observation 不是被动感知

传统 POMDP 中 observation 由 \(\Omega\) 生成；Agent 工具调用却主动选择观察通道。搜索词、SQL query 与文件路径决定看见什么，形成 active perception。更复杂的是 observation 可能携带 prompt injection，既报告世界又试图修改 policy。因此需要带 provenance 的 observation model，而不能把所有 tool feedback 视为同可信度数据。

### 5.3 Reward 与真实目标错位

LLM Agent 常用“测试通过”“用户点赞”“LLM-as-judge 分数”作为 reward。元控制器若据此修改 \(B\)，可能优化代理指标并引发 reward hacking。Policy refinement 的可行性不等于目标正确性。H1 的性能收益必须与 H5 的违规率联合报告。

### 5.4 Belief 的可解释性与校准

自然语言摘要可读，却不一定校准；向量表示紧凑，却难以审计；显式概率可评估，却难覆盖开放状态空间。开放问题是构造“typed hypothesis + textual rationale + calibrated probability + provenance”的统一 belief schema，并验证其跨模型稳定性。

## 6. 对操作形态学的贡献与 H1-H5 映射

本笔记把操作形态学从“组件清单”推进为“部分可观察控制系统的可写策略实现”。主要贡献有三点：第一，明确 M 的短期部分承担 belief approximation；第二，明确 T 定义 action space，工具返回定义 observation channel；第三，把 \(U\) 的 B 修改解释为双时间尺度 policy refinement。由此，结构可塑性的收益可以用 regret 衡量，治理风险可以用 belief corruption 与 policy drift 衡量。

| 假设 | 本笔记的作用 | 可检验预测 |
|---|---|---|
| **H1 结构可塑性** | B 自修改被定义为 POMDP policy refinement | 环境漂移后 adaptive-B 的 adaptation regret 低于 frozen-B |
| **H2 协同演化** | P/T/M/C 分别改变目标解释、行动空间、belief、控制流 | 联合修改应优于只优化 belief 或只优化 action selector |
| **H3 形态适配** | 不同 observation noise 与任务结构需要不同 belief schema 和 T | 高噪声环境演化出更强 provenance/verification |
| **H4 迁移收益** | belief update rule 与工具策略可跨相似任务迁移 | 迁移结构应优于仅迁移历史答案 |
| **H5 治理必要性** | belief pollution 会通过 U 固化为长期 policy drift | 有验证、版本与回滚的 B 修改违规率更低 |

最终结论是：**POMDP 对应成立于功能层，不成立于字面层。** 短期记忆不是天然 belief，LLM 输出也不是天然最优 action；只有当状态压缩、来源追踪、不确定性表达和修改治理被工程化后，POMDP 才从类比变成可证伪模型。

## 参考文献

1. Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). *Planning and Acting in Partially Observable Stochastic Domains*. Artificial Intelligence.
2. Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press.
3. yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR. 见 r-paper-001。
4. shinn2023reflexion: Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS. 见 r-paper-002。
5. packer2023memgpt: Packer, C., et al. (2023). *MemGPT: Towards LLMs as Operating Systems*. arXiv:2310.08560. 见 r-paper-004。
6. xu2025amem: Xu, W., et al. (2025). *A-MEM: Agentic Memory for LLM Agents*. arXiv:2502.12110. 见 r-paper-005。
7. fang2025selfevolving: Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. 见 r-paper-009。
8. r-note-001: 《操作形态学（Operational Morphology）的形式化定义》。
9. r-note-002: 《H1 假说的实证路径：结构可塑性》。
10. r-note-009: 《Agent 能力等级 L0-L5 的形式化定义》。
11. r-exp-002: `experiments/exp-02-pomdp-claim/`，POMDP 信念状态验证实验与 `results.json`。
