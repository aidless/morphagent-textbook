---
note_id: r-paper-002
title: Reflexion：通过语言反思实现记忆自修改（Reflexion: Language Agents with Verbal Reinforcement Learning）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 1, Ch 14]
related_papers: [shinn2023reflexion, yao2023react, wei2022cot, sutton1988learning, packer2023memgpt, xu2025amem]
keywords: [Reflexion, verbal reinforcement learning, self-reflection, M self-modification, sliding memory, episodic memory, sparse reward]
---

# r-paper-002：Reflexion：通过语言反思实现记忆自修改

> Reflexion 是第一个在 B = {P, T, M, C} 中实现**M 自修改**的元控制器 U：它让 Agent 把"反思"作为可读、可累积、可注入下一 episode 的语言记忆——这是操作形态学意义上"自进化"的第一块实验性基石。

## 1. 论文定位

Shinn 等人 2023 年发表的 *Reflexion: Language Agents with Verbal Reinforcement Learning*（NeurIPS 2023）[$TRAE_REF](https://arxiv.org/abs/2303.11381) 在 ReAct 之上引入了**跨 episode 的语言反思机制**——让 Agent 在每次任务失败后生成一段自然语言形式的"反思"，并把这段反思存入滑动记忆；在下一次 episode 重试时，把反思注入到 prompt 头部，让 Agent 避免重蹈覆辙。这一简单却深刻的设计使 LLM Agent 首次具备**跨 episode 学习**能力，成为后续所有 L4 等级自修改 Agent（MemGPT、A-MEM、O-Mem、ExpeL 等）的共同祖先。

本书将 Reflexion 定位为**操作形态学 M 自修改的第一例**——这是理解第 14 章"自适应记忆结构"的关键前置。Reflexion 让 B 中的 M 从"不可修改的短期 context"变成"可由 Agent 自身重写的长期记忆"。但 Reflexion 的 U 极为简单：它不修改 P（prompt）、不修改 T（工具）、不修改 C（代码），它**只修改 M**——这既是它的优雅之处，也是它的局限。

论文做出的三个判断被本书第 11 章的形式化框架重新审视：
- "Verbal reinforcement learning"——用自然语言代替数值权重作为 RL 信号，这等价于"在 M 中存储可微调的语言反馈"。
- "Self-reflection"——LLM 对自己轨迹的批判，这是"LLM 即 U"的早期形式。
- "Sliding window memory"——反思存储有容量上限，这是 M 自修改的第一个工程化边界。

## 2. 核心贡献

Reflexion 论文做出三项核心贡献：

1. **形式化 verbal reinforcement learning**：把传统 RL 的"数值奖励 + 梯度更新"替换为"语言反思 + 上下文注入"。Agent 不更新模型参数（gradient-based），而是更新外部记忆（text-based）。这一替换让 LLM Agent 拥有 RL 的"试错-改进"循环而无需反向传播。
2. **在多个 decision-making / reasoning / coding 任务上验证 Reflexion 优于 ReAct**：HumanEval（编程）、LeetcodeHard（算法题）、ALFWorld（具身文本游戏）、HotPotQA（多跳问答）。其中 HumanEval 上 GPT-4 从 76% 提升到 89%（相对提升 17 个百分点），ALFWorld 成功率从 75% 提升到 97%。
3. **展示 self-reflection 的元能力**：Reflexion 的反思生成不是机械的模板填充，而是 LLM 对自己失败轨迹的批判——这暗示 LLM 本身可以作为"元控制器 U"的实现，从而避免了为 U 设计独立模型的开销。

### 2.1 与 ReAct 的边界

Reflexion 直接建立在 ReAct 之上：
- **ReAct**：单 episode 内 Thought-Action-Observation 循环
- **Reflexion**：在 ReAct 之上，跨 episode 添加 Evaluator + Self-Reflection + Memory 三组件

Reflexion 不是 ReAct 的替代品，而是 ReAct 的**外层扩展**——它保留了 ReAct 的内层循环，添加了一个跨 episode 的元层。这一点与本书第 17 章的"内层 ReAct + 外层 U"分层完全一致；Reflexion 是第一个具体的"内-外层"工程实现。

### 2.2 与传统 RL 的边界

| 维度 | 传统 RL | Reflexion |
|---|---|---|
| 反馈信号 | 数值标量奖励 | 自然语言反思 |
| 知识存储 | 神经网络参数 | 文本记忆 |
| 更新机制 | 反向传播 | prompt 注入 |
| 训练成本 | 高（多次梯度更新） | 低（一次 LLM 调用） |
| 可解释性 | 低（权重不可读） | 高（反思可读） |

Reflexion 用"语言反思"代替"梯度更新"——这是一次范式转变。它牺牲了 RL 的收敛保证（语言反思不能保证策略提升），换取了**无需训练**、**可解释**、**跨模型迁移**的优势。

### 2.3 与 chain-of-thought 的边界

CoT 是**单 episode 内的推理展开**（forward chain）。Reflexion 是**跨 episode 的反思循环**（meta-loop over episodes）。两者维度正交：CoT 优化"一次推理的质量"，Reflexion 优化"多 episode 的累积改进"。

## 3. 方法细节

### 3.1 Reflexion 的形式化

Reflexion 在 ReAct 之上引入三组件：(1) **Evaluator**（评估器），(2) **Self-Reflection**（自我反思），(3) **Memory**（滑动记忆）。

完整轨迹：

$$
\tau = \{ (t_i, a_i, o_i) \}_{i=1}^{T}, \quad
\text{reflection} = \rho(\tau), \quad
M_{t+1} = M_t \cup \{\rho(\tau)\}
$$

其中：
- \(\rho\)：Self-Reflection 函数（由 LLM 实现，输入轨迹，输出反思文本）
- \(M_t\)：时刻 \(t\) 的反思记忆集合

下一个 episode 的 prompt 头部：

$$
\text{prompt} = \text{system} \oplus \text{query} \oplus M_t
$$

即把过去所有反思按时间顺序拼到 prompt 头部。

### 3.2 伪代码实现

```python
class ReflexionAgent:
    def __init__(self, llm, env, tools, prompt_template,
                 max_episodes=3, max_inner_steps=10, memory_limit=10):
        self.llm = llm
        self.env = env                       # 环境 E
        self.tools = tools                   # T (冻结)
        self.P = prompt_template             # P (冻结)
        self.max_episodes = max_episodes
        self.max_inner_steps = max_inner_steps
        self.M = []                          # M (可修改, 这是 B 中唯一可变组件)
        self.C = self.run_episode            # C (冻结)

    def self_reflect(self, trajectory, success):
        # U 的核心：让 LLM 反思自己的失败
        if success:
            return None  # 成功则不反思
        reflection_prompt = (
            f"Trajectory:\n{trajectory}\n\n"
            f"Final outcome: FAIL\n\n"
            f"Reflect on what went wrong and how to avoid it next time:"
        )
        return self.llm.generate(reflection_prompt)

    def run_episode(self, query, memory):
        # 内层循环就是 ReAct
        ctx = self.P + "\n" + query
        for m in memory:                       # M 注入 prompt 头部
            ctx += f"\nPrevious reflection: {m}\n"
        trajectory = []
        for step in range(self.max_inner_steps):
            t = self.llm.generate(f"{ctx}\nThought:")
            a = parse_action(self.llm.generate(f"{ctx}\nThought:{t}\nAction:"))
            o = self.tools[a.name](**a.args) if a.name != "Finish" else a.answer
            ctx += f"\nThought:{t}\nAction:{a}\nObservation:{o}\n"
            trajectory.append((t, a, o))
            if a.name == "Finish":
                return trajectory, True, a.answer
        return trajectory, False, None

    def run(self, query):
        for episode in range(self.max_episodes):
            traj, success, answer = self.run_episode(query, self.M)
            if success:
                return answer
            # U 修改 M: 添加反思
            reflection = self.self_reflect(traj, success)
            if reflection:
                self.M.append(reflection)
                # 滑动窗口：保留最近 N 条
                if len(self.M) > self.memory_limit:
                    self.M = self.M[-self.memory_limit:]
        return "FAILED (max episodes exceeded)"
```

伪代码中**唯一被修改的 B 组件是 M**：`self.M.append(reflection)` 和 `self.M = self.M[-self.memory_limit:]`。这正是 Reflexion 的核心贡献——它**首次在 LLM Agent 中实现 M 自修改**。

### 3.3 Self-Reflection 的 prompt 设计

Reflexion 设计了**两类反思 prompt**：
- **Binary classification reflection**："Did the agent succeed? [yes/no]" → "Why did it fail?" → "How to avoid this next time?"
- **Continuous grading reflection**："Score the trajectory from 0-1" → "What are the key issues?" → "Specific improvements?"

论文发现 continuous grading 产生更细致的反思，但 binary 更稳定。

### 3.4 滑动记忆（Sliding Window Memory）

Reflexion 的 M 有**容量上限**（论文默认 1-3 条反思）。原因有两个：
1. **上下文窗口限制**：反思全部拼到 prompt 头部，过多反思会撑爆 context window。
2. **避免噪声累积**：早期反思可能与当前任务无关，过多反思反而干扰 LLM 推理。

滑动窗口是 M 自修改的**第一个工程化约束**——它隐含了"反思的最近 N 条比早期 N 条更重要"的假设。这一假设在某些任务上不成立（例如长视野任务中早期反思可能更有价值），但在大多数 ReAct 任务上成立。

### 3.5 反思的内部结构

论文展示了一条典型的反思：

```
Trajectory:
  Thought: I need to put the tomato in the fridge.
  Action: take tomato from counter
  Observation: You took the tomato.
  Thought: Now I need to find the fridge.
  Action: go to fridge 1
  Observation: You are at fridge 1.
  Thought: Open fridge.
  Action: open fridge 1
  Observation: You opened fridge 1.
  Thought: Put tomato in fridge.
  Action: use tomato with fridge 1
  Observation: Nothing happens. The tomato is not put in.
  Thought: Maybe I need to use the fridge directly.
  Action: put tomato in fridge 1
  Observation: Nothing happens.
  ... (FAIL)

Reflection: I tried to put the tomato in the fridge using two different
actions but neither worked. I should have first inspected the fridge
to understand its state. Next time, I will use `examine fridge` before
attempting to interact with it.
```

这条反思展示了 LLM 的**因果归因能力**：它不只说"我失败了"，而是给出"我应该先用 `examine` 再 `use`"的具体改进策略。这种"具体可执行"的反思是 Reflexion 有效的原因。

## 4. 操作形态学视角

把 Reflexion 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到一个关键论断：**Reflexion 是第一个实现 B 中 M 自修改的 U**。

### 4.1 Reflexion 中 B 的每个组件

| 组件 | 在 Reflexion 中的实现 | 修改能力 |
|---|---|---|
| \(P\) | 系统 prompt + few-shot examples | **冻结** |
| \(T\) | 工具字典 | **冻结** |
| \(M\) | `self.M = []`（反思列表） | **可修改**（U 修改 M） |
| \(C\) | `self.run_episode`、`self.self_reflect` | **冻结** |

**只有一个组件可修改**——这就是 M 自修改的精确定义。

### 4.2 Reflexion 中 U 的状态

\[
U(B, \tau, r, \mathcal{C}) = B' \text{ 其中 } M' = M \cup \{\rho(\tau)\}, \quad P'=P, T'=T, C'=C
\]

更显式地：

\[
B_{t+1} = U(B_t, \tau_t, r_t, \mathcal{C}) \Rightarrow
\begin{cases}
P_{t+1} = P_t \\
T_{t+1} = T_t \\
M_{t+1} = M_t \cup \{\rho(\tau_t)\} \text{ if } r_t = \text{FAIL} \\
C_{t+1} = C_t
\end{cases}
\]

**U 只在 Agent 失败时触发，且只修改 M**。这与第 11 章定义 11.3 的 U 完全兼容——U 是"修改 B 的函数"，Reflexion 是 U 的一种实现（仅修改 M）。

### 4.3 Reflexion 实现了"LLM 即 U"

本书第 17 章强调"U 不必是独立模型"。Reflexion 的 U 是 LLM 本身——它通过 self-reflection prompt 让同一个 LLM 生成反思，再把反思注入 M。这等价于：

> **LLM 的元推理能力（meta-reasoning）= U 的实现机制**。

这是 LLM Agent 时代的关键洞见：**U 不需要单独训练**——只要 LLM 足够强，U 就可以由 LLM 自身承担。Reflexion 证明了这一点。

### 4.4 Reflexion 的 M 自修改是"显式 vs 隐式"

Reflexion 的 M 修改是**显式语言反思**：每条反思都是可读的英文文本。这是与"梯度更新"（隐式修改）的根本区别——在传统 RL 中，权重更新是黑盒；在 Reflexion 中，反思是白盒。

这一可读性带来三个好处：
1. **可审计**：人类可以读反思，知道 Agent 学到了什么。
2. **可注入**：反思可以直接拼到 prompt，被 LLM 立即使用。
3. **可编辑**：人类可以修改反思，纠正 Agent 的错误归因。

但可读性也带来三个坏处：
1. **可能不真实**：LLM 生成的反思可能不是真正的失败原因（post-hoc rationalization）。
2. **可能有害**：反思可能被 prompt injection 攻击，让 Agent 误以为失败是"我应该更小心"而实际上是"工具调用格式错误"。
3. **不可优化**：反思不能用 RL 优化（因为反思是文本而非向量）。

### 4.5 与 L0-L5 等级的关系

- **L2 ReAct**：单 episode 循环
- **L3 Reflexion**：跨 episode 反思 + M 自修改

Reflexion 把 Agent 从 L2 推到 L3。但 L3 仍然不是 L4——因为 L4 要求 **P/T/M/C 四个组件都可修改**。Reflexion 只修改 M，不修改其他三个组件。

### 4.6 与 Verifiability 的张力

第 23 章讨论"可验证自修改"——M 自修改是否需要验证？Reflexion 不验证反思的正确性——LLM 说什么反思就存什么反思。这导致：

1. **错误反思污染 M**：如果 LLM 错误归因（"我应该用 grep"而实际应该用"find"），这条错误反思会被注入下一 episode，使 Agent 持续走错路。
2. **没有版本控制**：反思是线性追加，没有"撤销"机制——错误反思无法被回滚。
3. **没有冲突解决**：新旧反思可能矛盾，但 Reflexion 没有机制处理矛盾。

这些限制推动第 14 章的 A-MEM、O-Mem 等工作——它们在 Reflexion 之上添加**反思验证、版本控制、冲突解决**。

## 5. 实验与结果

Reflexion 在 4 个任务上做了实验：

### 5.1 HumanEval（Python 编程）

- 数据集：164 道 Python 编程题
- GPT-4 baseline：76% pass@1
- + Reflexion：89% pass@1
- 相对提升 17%
- 操作形态学意义：Reflexion 在"代码生成 + 自我测试"循环中，让 Agent 记住"上次为什么测试失败"，下一次生成时规避同类错误。这是 M 自修改在编程任务上的典型效果。

### 5.2 LeetcodeHard（算法竞赛）

- 数据集：100 道 LeetCode Hard 题
- GPT-4 baseline：~40% pass@1
- + Reflexion：~55% pass@1
- 操作形态学意义：算法题需要"尝试不同算法"的策略空间，反思让 Agent 记住"上次用了动态规划但边界条件错了，下次先考虑边界"。

### 5.3 ALFWorld（具身家务）

- 数据集：25 类具身家务任务
- ReAct baseline：75% 成功率
- + Reflexion：97% 成功率
- 相对提升 29%
- 操作形态学意义：ALFWorld 是 ReAct 已经表现不错的领域（71%），Reflexion 在其上达到接近天花板（97%）。这暗示 **Reflexion 在 ReAct 已能完成的领域上效果最强**，因为反思只需要"局部修正"而非"重新设计策略"。

### 5.4 HotPotQA（多跳问答）

- 数据集：113k Wikipedia-based 多跳问答
- GPT-3.5 + ReAct：28% exact match
- + Reflexion：35% exact match
- 相对提升 25%
- 操作形态学意义：在多跳问答中，反思让 Agent 记住"上次搜索路径走了死胡同，下次先检查实体是否存在"。这与 MemGPT 的层次记忆异曲同工。

### 5.5 关键实验观察

四个任务的合并数据揭示：**Reflexion 在"长视野、需要试错"的任务上效果最强；在"短视野、单步可解"的任务上效果有限**。这条规律与本书 H1 假设一致——结构可塑性在动态环境中收益更大，在静态环境中收益有限。

### 5.6 反思长度的消融研究

论文报告：反思长度从 1 句扩展到 3 句提升性能；但扩展到 5 句以上性能下降。原因：
- 太短：反思太粗糙，缺乏具体指导。
- 太长：反思撑爆 context window，反而干扰当前任务。

这一消融研究是 M 自修改**容量约束**的第一份实证——它直接启发了第 14 章 A-MEM 的"动态记忆网络"（不是简单追加，而是按相关性检索）。

## 6. 局限与开放问题

Reflexion 的局限可以分为五类：**反思质量、记忆架构、奖励信号、跨任务、跨模型**。本节是本书对 Reflexion 的批判性分析。

### 6.1 反思质量：LLM 可能生成错误归因

Reflexion 完全依赖 LLM 的 self-reflection 能力。但 LLM 的反思可能不真实：
- **Post-hoc rationalization**：LLM 可能给出一个听起来合理但不是真正原因的反思。
- **Hallucinated reflection**：LLM 可能虚构反思中提到的失败模式（"我调用错了 API"而实际从未调用过该 API）。
- **Self-serving bias**：LLM 倾向于把失败归因于外部（"工具坏了"）而非内部（"我推理错了"）。

这一问题没有在 Reflexion 论文中被严肃讨论，但本书第 23 章"可验证自修改"必须正面回应——**反思必须经过验证才能被存入 M**。

### 6.2 记忆架构：滑动窗口过于简陋

Reflexion 的 M 是简单的**滑动列表**——按时间追加、按容量截断。这带来三个问题：
1. **无优先级**：所有反思等价对待，无法区分"重要反思"和"次要反思"。
2. **无检索**：反思按时间顺序拼到 prompt，无法按"相关性"检索。
3. **无结构**：反思是纯文本，无法被结构化查询。

这三个问题在第 14 章的 A-MEM、O-Mem 中被解决——它们把 M 从"滑动列表"升级为"动态记忆网络"。

### 6.3 奖励信号：只利用二元成败信号

Reflexion 的 U 只在 \(r = \text{FAIL}\) 时触发反思。但很多任务有**连续奖励**（如代码生成的测试通过率、对话的用户满意度）。Reflexion 不能利用连续奖励——它只能"事后知道是否成功"，无法"在线利用奖励信号"。

这一问题推动了**verbal critic** 工作（如 CRITIC、Self-Refine）——它们让 LLM 生成**连续评分**而非二元判断。

### 6.4 跨任务：反思不能跨任务迁移

Reflexion 的 M 在每个任务上是独立的——Agent 不能把"在 HotPotQA 上的反思"迁移到"在 ALFWorld 上"。这与 H4 假设（迁移收益）直接冲突——**Reflexion 不支持形态迁移**。

这一局限推动第 14 章的 ExpeL、O-Mem 等工作——它们让 M 成为"跨任务共享的策略库"。

### 6.5 跨模型：反思依赖 LLM 的元推理能力

Reflexion 假设 LLM 有足够的元推理能力生成有意义的反思。但在 7B、13B 等小模型上，self-reflection 质量急剧下降。这意味着 **Reflexion 只在 GPT-3.5/4 等强模型上有效**，不能简单迁移到小模型。

这一局限推动本书第 12 章"自修改 prompt"的反向思路：**与其用 LLM 生成反思，不如让 U 修改 P**（如 OPRO）——P 的修改不依赖 LLM 的元推理能力。

### 6.6 反思 ≠ 真正的学习

一个更根本的批评：**Reflexion 不是真正的"学习"，是"提示工程"**。Agent 没有改变自己的参数，没有改变自己的策略网络——它只是在 prompt 中加入更多文本。这是元控制器 U 在"语言层面"的修改，而非"参数层面"的修改。

本书第 15 章"自编辑代码"和第 25 章"开放问题"将深入讨论：仅靠语言层面的修改能否实现真正的自进化？或者必须修改 C（代码）才能算自进化？这是 L4 与 L5 等级的分界线。

### 6.7 开放问题表

| 问题 | 当前状态 | 本书视角 |
|---|---|---|
| 反思质量如何验证？ | 未验证 | 第 23 章"可验证自修改" |
| 反思能跨任务迁移吗？ | 不能 | 第 14 章 ExpeL、O-Mem |
| 反思能修改 P/T 吗？ | 不能 | 第 12-13 章 OPRO、LATM |
| 反思能修改 C 吗？ | 不能 | 第 15 章 SICA、Gödel Agent |
| 反思是真正的学习吗？ | 哲学开放 | 第 25 章开放问题 |

## 7. 对本书的贡献

Reflexion 在本书的理论体系中扮演**承上启下**的关键角色：它是 ReAct（r-paper-001）的直接扩展，也是所有 L4 等级 Agent 的共同祖先。

### 7.1 Reflexion 作为 M 自修改的第一例

本书第 11 章 H1 假设"结构可塑性"的第一个具体验证就是 Reflexion。具体地：
- **实验组 Reflexion**：U 修改 M（添加反思）
- **对照组 Frozen-ReAct**：U 不存在
- **预期**：Reflexion 在多 episode 任务上显著优于 Frozen-ReAct

论文中的 ALFWorld 75% → 97% 是 H1 的早期实证。但仅此一例不足以验证 H1——本书需要 r-note-002 中提到的多个验证案例。

### 7.2 Reflexion 与第 14 章的关系

第 14 章"自适应记忆结构"是 Reflexion 思想的全面展开：
- **14.2 MemGPT**：把 M 从"反思列表"升级为"操作系统式层次记忆"
- **14.3 A-MEM**：把 M 从"线性追加"升级为"Zettelkasten 风格动态网络"
- **14.4 O-Mem**：把 M 从"被动存储"升级为"主动用户画像"
- **14.5 Mem0**：把 M 从"研究原型"升级为"工业级抽象"

第 14 章所有这些工作都建立在 Reflexion 的基础上——它们都是"M 自修改"的不同实现。

### 7.3 Reflexion 与本书 H1-H5 的关系

| 假设 | Reflexion 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | Reflexion 让 M 可修改 | **H1 的第一个验证案例** |
| **H2 协同演化** | Reflexion 只修改 M，不修改 P/T/C | 仅修改 M，H2 不可验证 |
| **H3 形态适配** | Reflexion 的 M 反映任务历史 | 间接支持 H3（不同任务产生不同 M） |
| **H4 迁移收益** | Reflexion 的 M 不跨任务迁移 | **反驳 H4**（在多任务设置下） |
| **H5 治理必要性** | Reflexion 无反思验证、无版本控制 | 需要治理（推动 H5） |

### 7.4 Reflexion 与 LLM-as-U 的范式

Reflexion 最重要的一点是：**LLM 自身可以作为 U**。这一范式被后来所有自修改 Agent 采用：
- **OPRO**（修改 P）：LLM-as-U
- **Promptbreeder**（修改 P）：LLM-as-U + 进化算法
- **LATM**（修改 T）：LLM-as-U
- **A-MEM**（修改 M）：LLM-as-U
- **SICA**（修改 C）：LLM-as-U + 代码验证

**LLM-as-U 是本书第 17 章元控制器设计的第一原则**——不需要单独训练 U，只要 LLM 足够强，U 就可以由 LLM 承担。Reflexion 是这一原则的首次证明。

### 7.5 给读者的关键启示

1. **Reflexion 是 M 自修改的最小可行实现**：理解 Reflexion 是理解 MemGPT、A-MEM 等高级记忆系统的前提。
2. **Reflexion 不是 M 自修改的终点**：滑动列表、缺乏验证、无跨任务迁移——这些都是 A-MEM、O-Mem 要解决的问题。
3. **LLM-as-U 是关键范式**：Reflexion 证明 LLM 自身可以作为 U，这大幅降低了自修改 Agent 的工程门槛。
4. **反思 ≠ 学习**：Reflexion 是语言层面的修改，不是参数层面的修改。这一边界决定 L4 与 L5 的差异。

Reflexion 是从 L2（ReAct）到 L3（Reflective）的桥梁，也是从 L3 到 L4（Self-Modifying）的起点——它让 Agent 第一次拥有"跨 episode 记忆"，为后续所有自修改工作铺平了道路。

## 参考文献

- shinn2023reflexion: Shinn, N., Cassano, F., Gopinath, A., Narasimhan, K. R., & Yao, S. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS 2023. [$TRAE_REF](https://arxiv.org/abs/2303.11381)
- yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 见 r-paper-001。
- wei2022cot: Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. NeurIPS 2022.
- sutton1988learning: Sutton, R. S. (1988). *Learning to Predict by the Methods of Temporal Difference*. Machine Learning, 3, 9-44. （传统 RL 与 verbal RL 的对比基础）
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT: Towards LLMs as Operating Systems*. arXiv:2310.06860. （Reflexion 的 M 思想在 OS 风格记忆中的扩展）
- xu2025amem: Xu, W., et al. (2025). *A-MEM: Agentic Memory for LLM Agents*. NeurIPS 2025. （M 自修改的下一阶段：动态网络）