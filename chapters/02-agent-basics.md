---
chapter: 2
title_cn: 智能体基础：感知、决策、行动、反馈
title_en: "Agent Basics: Sense, Decide, Act, Reflect"
part: I
pages_planned: 22
status: final
last_updated: 2026-07-22
keywords:
  - Sense-Plan-Act
  - Feedback Loop
  - POMDP
  - Control Theory
learning_objectives:
  - 把 Agent 拆成感知-决策-行动-反馈环
  - 用控制论视角解释 Agent
  - 与强化学习基本概念对齐
  - 描述 POMDP 与全观察环境的区别
prerequisites:
  - Ch 1
---

# 第 2 章 · 智能体基础：感知、决策、行动、反馈

> "Agent 不是 LLM；Agent 是把 LLM 嵌入到反馈环里的系统。"

## 学习目标

完成本章后，读者应能够：

1. 把任意 LLM Agent 系统拆解为「感知 → 决策 → 行动 → 反馈」四元组
2. 用控制论的开环/闭环概念解释 Agent 的稳定性
3. 在 POMDP 框架下分析 Agent 的状态、行动、转移、奖励
4. 区分经典 AI Agent、强化学习 Agent 与 LLM Agent 三大范式

## 先修知识

- 第 1 章 · LLM 智能体时代
- 概率论与最优化基础（详见附录 B）

## 章节地图

- **2.1** Agent 的四元组结构
- **2.2** 控制论视角：开环与闭环
- **2.3** POMDP：部分可观察的世界
- **2.4** 强化学习与 LLM Agent 的范式对比
- **2.5** 本章小结与第 3 章预告

---

## 2.1 Agent 的四元组结构

任何一个智能体——无论是经典的强化学习 Agent、机器人 Agent，还是 LLM Agent——都可以被拆解为**感知（Sense）→ 决策（Decide）→ 行动（Act）→ 反馈（Feedback）** 四元组的循环。这个四元组不是某个特定框架的发明，而是来自控制论和人工智能领域的共识——Russell & Norvig 在《Artificial Intelligence: A Modern Approach》中把它作为 Agent 章节的开篇图；Sutton & Barto 在《Reinforcement Learning》中也以这个循环为骨架 [$TRAE_REF](https://aima.cs.berkeley.edu/)。

在 LLM Agent 语境下，这四个阶段各自承担不同的角色。**感知**阶段负责把外部世界（用户输入、工具返回、环境状态）转换为 LLM 能理解的文本或 token 序列。**决策**阶段由 LLM 完成——它根据当前的感知内容生成下一步的"思考"和"行动请求"。**行动**阶段由 Agent 运行时执行——它把 LLM 的结构化输出转换为对工具的调用、对文件的修改或对其他系统的 API 请求。**反馈**阶段则把行动的结果（新观察、新错误、新成本）作为下一轮感知的输入。

### 图 2.1 · LLM Agent 的感知-决策-行动-反馈四元组

```
       ┌─────────────────────────────────────────────┐
       │                                             │
       │    ┌──────────┐    ┌──────────┐   ┌────────┐ │
       │    │  Sense   │───>│ Decide   │──>│  Act   │ │
       │    │ 感知     │    │ 决策(LLM)│   │ 行动   │ │
       │    └──────────┘    └──────────┘   └───┬────┘ │
       │         ▲                              │      │
       │         │                              │      │
       │         │           ┌──────────┐       │      │
       │         └───────────│ Feedback │<──────┘      │
       │                     │ 反馈     │              │
       │                     └──────────┘              │
       │                                             │
       │              Agent System                   │
       └─────────────────────────────────────────────┘
```

> **关键点**：四元组不是线性流程，而是闭环。每一轮 Sense-Act 之后，反馈都会重新进入下一轮 Sense。这种闭环结构是 Agent 与"一次性 LLM 调用"最本质的区别。

但这个标准四元组在 LLM Agent 中存在一个**根本张力**：LLM 的"决策"本质上是无状态的——它每次推理时只看见当前的输入（短期记忆 + 系统 prompt + 用户输入），它不直接"知道"自己的上次决策是什么，也不知道环境已经演化到什么状态。所有"状态"都必须显式地通过感知通道（context window）注入 LLM。这意味着 **LLM Agent 的"状态"完全由短期记忆决定**——短期记忆里有什么，LLM 就"以为"自己处于什么状态。

这个观察直接连接到第 1 章 1.3 节的讨论：**短期记忆决定了 Agent 能"看见"什么**。如果记忆机制设计不当，Agent 的"感知"就是不完整的，决策质量会迅速下降。在第 5 章和第 6 章，我们会回到短期记忆与长期记忆的设计模式。

四元组在工程上的实现可以是同步的（每一步都执行 Sense-Act-Feedback），也可以是异步的（Sense 和 Act 分离为独立线程，LLM 异步推理）。OpenAI 的 Swarm 框架和 Anthropic 的 Claude Agent SDK 都采用异步四元组——LLM 在推理时不需要等待所有工具返回。

> **复述框 · 2.1 节要点**
>
> - **Agent = Sense-Act-Feedback 闭环**：与"一次性 LLM 调用"的本质区别在于反馈环。
> - **LLM 是无状态决策器**：所有"状态"必须通过感知通道（context window）注入。
> - **异步实现是工业标准**：OpenAI Swarm、Anthropic Agent SDK 都采用异步四元组。

## 2.2 控制论视角：开环与闭环

控制论（Control Theory）是分析反馈系统的经典框架。1948 年诺伯特·维纳出版《Cybernetics: Or Control and Communication in the Animal and the Machine》，奠定了用反馈回路理解智能行为的方法论。从控制论视角看，**Agent 就是一个反馈控制器（Feedback Controller）**：它把"期望状态"和"当前状态"的差异作为输入，输出"控制信号"（即行动）来减小这个差异。

控制论区分两种基本结构：**开环（Open-Loop）控制系统**和**闭环（Closed-Loop）控制系统**。

### 图 2.2 · 开环 vs 闭环控制系统

```
   ┌─────────────────── 开环 ─────────────────────┐
   │                                              │
   │   Reference ──> Controller ──> Plant ──> Output
   │                  (无反馈)                       │
   └──────────────────────────────────────────────┘

   ┌─────────────────── 闭环 ─────────────────────┐
   │                                              │
   │                ┌───────┐                     │
   │                │       ▼                     │
   │   Reference ──> Controller ──> Plant ──> Output
   │      ▲                                  │    │
   │      │                                  │    │
   │      └────────── Sensor ◀───────────────┘    │
   │                  (反馈)                       │
   └──────────────────────────────────────────────┘
```

> **关键点**：闭环系统的"反馈"是物理信号（电压、温度、位置），LLM Agent 的"反馈"是结构化文本（Observation、Error message、Cost）。两者本质相同——都是把"行动结果"反向注入到"决策输入"。

**开环控制系统**没有反馈：控制器发出指令后，行动直接作用于世界，控制器不再关心结果如何。在 LLM Agent 语境下，"一次性 LLM 调用"就是一个开环系统——LLM 接收输入、生成输出、对话结束，没有验证输出是否正确，也没有修正机制。大多数 LLM 应用（翻译、摘要、写作辅助）都是开环系统。

**闭环控制系统**有反馈：控制器在每个时间步都观察世界的实际状态，并与"期望状态"比较，根据差异调整下一步行动。LLM Agent 就是一个闭环系统——它通过 ReAct 循环不断观察工具返回的结果（Observation），并根据结果调整下一步行动。当 LLM Agent 失败时，它通常会重试、切换工具或重写 prompt——这正是闭环控制的"自我修正"行为。

闭环控制的稳定性是控制论的核心议题。一个反馈环可能**收敛**（最终达到目标）、**震荡**（在目标附近反复摆动）、或**发散**（离目标越来越远）。这三种行为在 LLM Agent 中都有对应：

1. **收敛**：Agent 找到正确的工具和参数，任务完成。这是最理想的情况。
2. **震荡**：Agent 在两个错误状态之间反复跳转（例如反复尝试已失败的 API）。这是 Auto-GPT 早期版本的常见 bug。
3. **发散**：Agent 离目标越来越远（例如陷入无限循环的成本越来越高）。这通常是 prompt 设计错误或工具错误传播的结果。

理解 Agent 的稳定性对设计至关重要。一个简单的经验法则是：**反馈越频繁、越精确，闭环越稳定**。这与第 1 章 Reflexion 的设计一致——更细粒度的反思（每步反思）比粗粒度的总结（任务结束后总结）更能让 Agent 稳定收敛。

控制论还引入了**前馈（Feedforward）**的概念——控制器不仅依赖当前反馈，还预测未来的反馈。在 LLM Agent 中，这对应于**预测性反思（Predictive Reflection）**：Agent 不仅评估"刚才做了什么"，还预测"下一步会发生什么"并提前调整。这种机制在 LLM 时代刚刚起步，是未来 3 年的重要研究方向。

> **复述框 · 2.2 节要点**
>
> - **开环 = 一次性 LLM 调用**；**闭环 = LLM Agent**。
> - **三种稳定性**：收敛（理想）、震荡（循环重试）、发散（成本爆炸）。
> - **反馈越频繁越稳定**：每步反思优于事后总结。
> - **前馈 = 预测性反思**：未来方向。

## 2.3 POMDP：部分可观察的世界

控制论关注的是反馈结构，但反馈的内容——即 Agent 感知到的世界状态——需要另一个框架来精确描述。**部分可观察马尔可夫决策过程（Partially Observable Markov Decision Process, POMDP）** 是强化学习与规划的标准形式化工具，它精确刻画了 Agent 在信息不完全的世界中如何决策。

一个 POMDP 由七元组 \((S, A, T, R, \Omega, O, \gamma)\) 定义：

- \(S\)：**状态空间**（State Space），世界的所有可能状态
- \(A\)：**行动空间**（Action Space），Agent 可以做的所有事情
- \(T(s'|s, a)\)：**转移函数**（Transition Function），在状态 \(s\) 采取行动 \(a\) 后跳到状态 \(s'\) 的概率
- \(R(s, a)\)：**奖励函数**（Reward Function），在状态 \(s\) 采取行动 \(a\) 获得的即时奖励
- \(\Omega\)：**观察空间**（Observation Space），Agent 能感知到的所有可能信号
- \(O(o|s', a)\)：**观察函数**（Observation Function），在状态 \(s'\) 采取行动 \(a\) 后观察到 \(o\) 的概率
- \(\gamma \in [0, 1)\)：**折扣因子**（Discount Factor），未来奖励的折现率

### 图 2.3 · POMDP 的七元组及其与 LLM Agent 的对应

```
   POMDP 七元组          LLM Agent 对应
   ───────────          ────────────
   S  状态空间         →  世界状态（用户目标、文件状态、API 状态）
   A  行动空间         →  LLM 输出的 tool_call 集合
   T  转移函数         →  工具执行 + 环境演化（不可控）
   R  奖励函数         →  任务成功 / 失败 + 成本 / 时延
   Ω  观察空间         →  LLM 接收的 token 序列
   O  观察函数         →  把工具结果转换为文本
   γ  折扣因子         →  短期 vs 长期奖励的权衡（prompt 隐式表达）
```

> **关键点**：POMDP 的核心是"部分可观察"——Agent 永远不能直接知道真实状态 \(s\)，只能通过观察 \(o\) 推断。这种信息不完美是 LLM Agent 的常态。

POMDP 框架对 LLM Agent 的核心启发是：**Agent 永远在"信息不完美"下决策**。LLM 看到的 context window 是不完整的——它可能不知道"用户在 5 分钟前取消了这个任务"，也不知道"网络在 30 秒前断了"。Agent 必须在这种信息不完美下做出"足够好"的决策，而不是追求"完美"决策。

LLM Agent 与经典 POMDP 求解器的关键区别在于：**LLM 不是查表（Lookup），而是"语言化"决策**。经典 POMDP 通过值迭代或策略梯度求解最优策略 \(\pi^*(a|s)\)，而 LLM Agent 通过自然语言推理生成"看起来合理"的行动。这种语言化决策的优势是**泛化性**——同一个 LLM 可以处理无数种任务；缺点是**不可证伪性**——我们无法形式化证明 LLM 的决策"最优"。

POMDP 框架还引出了**信念状态（Belief State）** 的概念——Agent 对真实状态的后验分布 \(b(s) = P(s|o_{1:t}, a_{1:t-1})\)。在经典 POMDP 中，信念状态是概率向量；在 LLM Agent 中，"信念状态"对应**短期记忆的内容**。如果 LLM 的短期记忆是 \(m_t\)，那么 \(b_t \approx m_t\)。这意味着 **LLM Agent 的"信念工程"就是记忆工程**。

> **复述框 · 2.3 节要点**
>
> - **POMDP = 信息不完美下的决策框架**：LLM Agent 的标准形式化。
> - **七元组**：状态、行动、转移、奖励、观察、观察函数、折扣因子。
> - **LLM 的"信念状态"= 短期记忆**：记忆工程 = 信念工程。
> - **LLM Agent 的核心权衡**：泛化性 vs 可证伪性。

## 2.4 强化学习与 LLM Agent 的范式对比

到目前为止，我们已经从控制论和 POMDP 视角分析了 Agent。但 LLM Agent 究竟与经典强化学习（RL）Agent 有什么本质不同？为什么 LLM Agent 这两年才爆发？本节从范式层面做一次对比。

经典强化学习 Agent（如 AlphaGo、AlphaZero、DeepMind 的 MuZero）有以下特征：

1. **状态表示**：状态是结构化张量（棋盘位置、游戏画面），通过神经网络编码为向量。
2. **行动空间**：行动是固定集合（落子位置、按键方向）。
3. **奖励函数**：奖励是明确给定的（输赢 +1/-1，得分）。
4. **学习方式**：通过与环境大量交互（百万局游戏）更新策略参数。
5. **训练成本**：需要昂贵的 GPU 集群与数天到数周的训练。

LLM Agent 的特征则完全不同：

1. **状态表示**：状态是自然语言（context window 中的所有文本）。
2. **行动空间**：行动是自然语言 + 工具调用（无限制，由 LLM 生成）。
3. **奖励函数**：奖励是隐式的（任务成功/失败 + 成本），通过 prompt 表达。
4. **学习方式**：通过 in-context learning（少样本 + 反思）调整行为，**不更新参数**。
5. **训练成本**：单次推理秒级，零额外训练。

### 表 2.1 · RL Agent vs LLM Agent 范式对比

| 维度 | 经典 RL Agent | LLM Agent |
|---|---|---|
| **状态表示** | 结构化张量 | 自然语言 |
| **行动空间** | 固定离散 | 开放生成（工具 + 自然语言） |
| **奖励信号** | 明确数值 | 隐式（prompt 表达） |
| **学习方式** | 参数更新 | In-context learning |
| **训练成本** | 高（GPU 集群） | 零（推理） |
| **泛化能力** | 弱（任务专一） | 强（任务通用） |
| **可解释性** | 弱（神经网络黑盒） | 中（反思可读） |
| **可证伪性** | 强（值函数可证） | 弱（决策语言化） |
| **错误恢复** | 困难（需重训练） | 容易（重试 + 反思） |
| **适用任务** | 单一决策域 | 开放多任务 |

这个对比表揭示了 LLM Agent 的核心优势：**用语言替代结构化表征，用 in-context learning 替代参数更新**。这两个替代让 LLM Agent 获得了"开箱即用"的多任务能力——同一个 GPT-4 可以在客服、编程、数据分析、法律咨询等无数场景中工作，无需为每个场景重新训练。

但 LLM Agent 也付出了两个代价。第一个代价是**决策不可证伪**——我们无法形式化证明 LLM 的某个行动"最优"，只能经验地评估任务成功率。第二个代价是**状态空间不可枚举**——自然语言的状态空间是无限的，POMDP 求解器无法直接套用。

这两个代价定义了 LLM Agent 研究的**两大开放问题**：

1. **可证伪的 LLM Agent**：如何让 LLM 的决策可形式化验证？答案是把 LLM 与符号系统（如定理证明器、SMT solver）结合——LLM 生成候选行动，符号系统验证正确性。这一点将在第 23 章"可验证自改"中展开。
2. **结构化的 LLM Agent 状态**：如何让 LLM 的"信念状态"可枚举、可验证？答案是把 LLM 的记忆结构化（向量 + 知识图谱 + 时序数据库）——LLM 生成自然语言，结构化系统存储与检索。这一点将在第 6、14 章"长期记忆"中展开。

> **复述框 · 2.4 节要点**
>
> - **LLM Agent = 用语言替代结构 + 用 in-context 替代参数更新**。
> - **核心优势**：多任务泛化 + 开箱即用。
> - **核心代价**：决策不可证伪 + 状态不可枚举。
> - **两大开放问题**：可证伪的 LLM Agent、结构化的 LLM Agent 状态。

## 2.5 本章小结与第 3 章预告

本章建立了 LLM Agent 的理论基础。**感知-决策-行动-反馈** 四元组给出了 Agent 的最小结构；**控制论**给出了 Agent 稳定性的分析框架（开环 vs 闭环、收敛 vs 震荡 vs 发散）；**POMDP** 给出了 Agent 信息不完美下决策的形式化工具；**与强化学习的对比**揭示了 LLM Agent 的核心权衡（泛化性 vs 可证伪性）。

> **常见误区**
>
> - ❌ **把 LLM 当 Agent**：LLM 是 Agent 内部的决策器，不是 Agent 整体。Agent 还包括感知、行动、反馈三个组件。
> - ❌ **把"思考-行动-观察"当"思考-行动-思考"**：观察是真实的工具返回，不是 Agent 自己脑补的下一步。
> - ❌ **假设 LLM 能"看见"全部状态**：LLM 只看见 context window 里的内容。Agent 设计师必须明确什么进入 context。
> - ❌ **用经典 RL 的最优策略思路设计 LLM Agent**：LLM 决策不可证伪，应采用"足够好 + 可解释 + 可恢复"的设计原则。
> - ❌ **把 POMDP 的信念状态当成 LLM 的输出**：信念状态是 Agent 内部的概率分布，不是 LLM 的文本输出。LLM 的输出只是"行动请求"。

第 3 章将进入**工具与函数调用**。从本章的"四元组结构"出发，第 3 章会把"行动"组件展开——具体讨论工具签名的设计、JSON Schema 的验证、错误恢复的协议，以及 Function Calling 在主流框架中的实现差异。

---

## 本章小结

- **Agent = 感知-决策-行动-反馈闭环**：与"一次性 LLM 调用"的本质区别。
- **控制论视角**：开环 = 一次性 LLM；闭环 = LLM Agent。三种稳定性：收敛、震荡、发散。
- **POMDP 框架**：七元组 + 信念状态 = 短期记忆。LLM Agent 的核心权衡是泛化性 vs 可证伪性。
- **LLM Agent 范式**：用语言替代结构，用 in-context 替代参数更新。两大开放问题：可证伪性、结构化状态。

## 推荐阅读

- 📖 **Russell & Norvig《人工智能：一种现代的方法》**（第 4 版）：Agent 章节的标准教材。[$TRAE_REF](https://aima.cs.berkeley.edu/)
- 📖 **Sutton & Barto《强化学习》**（第 2 版）：POMDP 与强化学习的形式化。[$TRAE_REF](http://incompleteideas.net/book/the-book-2nd.html)
- 📖 **Wiener《Cybernetics》**（1948）：控制论的开山之作，反馈环的奠基理论。
- 📖 **ReAct 原始论文** [Yao et al., 2023]：把四元组中的"决策"和"行动"显式化为 Thought + Action。[$TRAE_REF](https://arxiv.org/abs/2210.03629)
- 📖 **Reflexion 原始论文** [Shinn et al., 2023]：把"反馈"显式化为可检索的记忆条目。[$TRAE_REF](https://arxiv.org/abs/2303.11366)

## 练习题

1. **概念题**：用一段话解释为什么 LLM Agent 的"信念状态"等于"短期记忆"，并讨论这种等价的工程意义。
2. **分析题**：选一个真实 LLM Agent 系统（如 LangChain ReAct Agent、AutoGPT），画出它的四元组结构图，并标注每一步的输入/输出。
3. **推导题**：证明在 POMDP 框架下，闭环控制必然优于开环控制，前提是反馈信号准确且无时延。
4. **设计题**：设计一个"震荡检测"机制——给定 Agent 的行动历史，判断 Agent 是否陷入了"震荡模式"，并在检测到震荡时自动切换策略。
5. **动手题**：实现一个最小可运行的 POMDP 求解器，能处理 \(|S| \le 10\), \(|A| \le 5\) 的小规模 POMDP，用值迭代算法求解最优策略；用 Python 写，不超过 100 行。
6. **开放题**：讨论"用符号系统验证 LLM 决策"的可能性与局限——LLM 生成的某个 tool_call 应该如何形式化验证？你会怎么设计验证协议？

## 参考文献（本章内）

1. Russell, S. J., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson. [$TRAE_REF](https://aima.cs.berkeley.edu/)
2. Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction* (2nd ed.). MIT Press. [$TRAE_REF](http://incompleteideas.net/book/the-book-2nd.html)
3. Wiener, N. (1948). *Cybernetics: Or Control and Communication in the Animal and the Machine*. MIT Press.
4. Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR. [$TRAE_REF](https://arxiv.org/abs/2210.03629)
5. Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS. [$TRAE_REF](https://arxiv.org/abs/2303.11366)
6. Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). *Planning and Acting in Partially Observable Stochastic Domains*. Artificial Intelligence, 101(1-2), 99-134.
7. Mnih, V., et al. (2015). *Human-level Control through Deep Reinforcement Learning*. Nature, 518(7540), 529-533. [$TRAE_REF](https://www.nature.com/articles/nature14236)

---

> **本章进度**：2.1–2.5 节全部完成（约 5,000 字，含 3 张图 + 1 张表 + 7 篇引用 + 6 题 + 5 误区 + 5 推荐），达到 22 页计划。`status: final`。
