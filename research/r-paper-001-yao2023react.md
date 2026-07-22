---
note_id: r-paper-001
title: ReAct：思考-行动-观察循环作为操作形态的静态基线（ReAct: Synergizing Reasoning and Acting in Language Models）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 1, Ch 2]
related_papers: [yao2023react, yao2023react, wei2022cot, shinn2023reflexion, schick2023toolformer]
keywords: [ReAct, Thought-Action-Observation, static morphology, frozen B, frozen U, frozen C, substrate]
---

# r-paper-001：ReAct：思考-行动-观察循环作为操作形态的静态基线

> ReAct 是 LLM Agent 时代的第一块奠基石：在它之后才有了"操作形态 B = {P, T, M, C}"这个概念——但 ReAct 本身是**静态形态**（B 在部署后冻结、U 不存在）。

## 1. 论文定位

Yao 等人 2023 年发表的 *ReAct: Synergizing Reasoning and Acting in Language Models*（ICLR 2023）[$TRAE_REF](https://arxiv.org/abs/2210.03629) 是 LLM Agent 范式的奠基性工作。它首次系统地提出"Reason + Act"的交替循环：让 LLM 在每一步先生成一段自然语言推理（**Thought**），再决定调用哪个外部工具（**Action**），再消化工具返回（**Observation**），再进入下一轮 Thought。这一范式在一年内被广泛采用，成为 LangChain、AutoGPT、BabyAGI 等所有后续 Agent 框架的事实循环结构。本书第 1 章把它列为"LLM Agent 四大里程碑"之首。

但本书的理论视角——**操作形态学（Operational Morphology）**——使我们对 ReAct 的兴趣超越了"范式起源"层面。本笔记的核心论点是：**ReAct 不仅是 LLM Agent 的循环结构，它就是操作形态 B = {P, T, M, C} 的最小可执行骨架**。ReAct 暴露了 B 的所有四个组件、并把它们绑定到同一个循环上；但同时，ReAct 自身**没有任何修改 B 的能力**——它是一个**静态形态（static morphology）**：B 在部署时固定，U 不存在。

这一正一反两面共同定义了 ReAct 在本书中的位置：它是"操作形态学要超越的对象"，而不是"操作形态学的实现案例"。

## 2. 核心贡献

ReAct 论文做出三项核心贡献，按重要性排序：

1. **形式化 Thought-Action-Observation 循环**：把 CoT（Chain-of-Thought）推理与 Action 执行耦合到同一个 prompt 模板中，使 LLM 能够在多轮交互中保持"推理链"。这一形式化是后续所有 Agent 循环的祖先。
2. **在四个领域验证 ReAct 优于纯 CoT 或纯 Act**：HotPotQA（多跳问答）、Fever（事实核查）、ALFWorld（具身文本游戏）、WebShop（在线购物）。其中 ALFWorld 与 WebShop 两个具身/交互场景的实验最为关键——它们证明 Thought 不能被省略（Act-only 失败）、Action 不能被省略（CoT-only 失败），只有交替进行才能兼顾推理与执行。
3. **提供 Few-shot Prompt 设计模式**：用 6 条精心设计的 example trajectory 引导 LLM 输出 Thought-Action-Observation 三元组。这个 prompt 模板后来成为 LangChain ReAct Agent、AutoGPT、BabyAGI 等所有 Agent 实现的提示工程基线。

### 2.1 与 Chain-of-Thought（CoT）的边界

ReAct 的关键论断是：**Thought 和 Action 不能分离**。Wei 等人的 CoT 让 LLM 在回答前显式推理；Yao 等人之前的多数工作让 LLM 直接生成 Action（如 Toolformer）。ReAct 通过让 Thought 和 Action 共享同一个 prompt slot、且强制 Thought 出现在 Action 之前，建立了"推理-行动耦合"的原则。这一原则在 2024-2025 年成为 Agent 设计的默认选项。

### 2.2 与 Act-only 的边界

论文对比 ReAct 与 Act-only（让 LLM 直接生成 Action 而不写 Thought），结果显示：
- 在 HotPotQA 上，Act-only 难以处理多跳推理（它会陷入"重复搜索同一实体"的循环）
- 在 ALFWorld 上，Act-only 容易在长视野规划中迷失（它无法把当前观察映射到子目标）

ReAct 通过 Thought 显式暴露 LLM 的"内部状态"——这等价于把 LLM 的隐变量变成可观察、可回溯、可调试的字符串。这一可观察性正是后来 Memory 与 Reflection 能成立的基础。

## 3. 方法细节

### 3.1 ReAct 的形式化

ReAct 把 LLM Agent 的轨迹形式化为一个三元组序列：

$$
\tau = (t_0, a_0, o_0, t_1, a_1, o_1, \ldots, t_T, a_T)
$$

其中：
- \(t_i \in \mathcal{T}\)：第 \(i\) 步的 Thought（自然语言推理）
- \(a_i \in \mathcal{A}\)：第 \(i\) 步的 Action（结构化动作）
- \(o_i \in \mathcal{O}\)：第 \(i\) 步的 Observation（工具返回）

LLM 的输入是 prefix \(x \oplus t_0 \oplus a_0 \oplus o_0 \oplus \ldots \oplus t_i\)，LLM 的输出是 \((a_i, o_i, t_{i+1})\) 的下一段。终止条件是生成 \(a_T = \text{Finish}[\text{answer}]\)。

### 3.2 伪代码实现

```
class ReActAgent:
    def __init__(self, llm, tools, prompt_template, max_steps=10):
        self.llm = llm
        self.tools = tools                  # T
        self.prompt_template = prompt_template  # P
        self.max_steps = max_steps
        self.history = []                   # M (短期, 即 context)
        self.code = self.run_step           # C

    def run_step(self, context):
        # 1. Thought: LLM 推理下一步
        thought = self.llm.generate(
            f"{self.prompt_template}\n"
            f"{context}\n"
            f"Thought:"
        )
        # 2. Action: LLM 决定调用哪个工具
        action_str = self.llm.generate(
            f"{context}\nThought: {thought}\nAction:"
        )
        action = parse_action(action_str)
        # 3. Observation: 执行工具
        if action.name == "Finish":
            observation = action.answer
        else:
            observation = self.tools[action.name](**action.args)
        return thought, action, observation

    def run(self, query):
        ctx = f"Question: {query}\n"
        for step in range(self.max_steps):
            t, a, o = self.run_step(ctx)
            ctx += f"Thought: {t}\nAction: {a}\nObservation: {o}\n"
            if a.name == "Finish":
                return a.answer
        return "FAILED (max steps exceeded)"
```

注意：上面伪代码是**操作形态学的反例**——`self.tools`、`self.prompt_template`、`self.history`、`self.run_step` 在 `__init__` 后全部冻结，没有任何 `U` 函数能修改它们。这就是"静态形态"。

### 3.3 Few-shot Prompt 设计

ReAct 论文的关键工程贡献是**手工设计的 6 条 few-shot example trajectories**。每条 trajectory 展示了 ReAct 应该如何推理与行动，让 LLM 在 inference 时模仿这个模式。这个 prompt 模板后来被 LangChain 几乎原样采用为 `ReAct` Agent 的 default prompt。

### 3.4 推理策略

论文还研究了三种 ReAct 的推理策略变体：
- **ReAct**：仅用 Thought-Action-Observation 循环
- **ReAct + CoT (SC)**：在 ReAct 失败时退回到 CoT 推理，再把 CoT 答案注入下一轮 ReAct
- **ReAct + CoT + Reflection**（后加）：在 ReAct 失败时让 LLM 自反思失败原因，注入下一轮

第三种策略是 Reflexion 论文的前身。

## 4. 操作形态学视角

把 ReAct 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到一个重要的"零阶"分析。

### 4.1 ReAct 中 B 的每个组件

| 组件 | 在 ReAct 中的具体实现 | 修改能力 |
|---|---|---|
| \(P\) | 系统 prompt + 6-shot few-shot example | **冻结**（部署后不可改） |
| \(T\) | 工具字典 `self.tools = {search, lookup, Finish}` | **冻结**（运行时不可增删） |
| \(M\) | `self.history = []`（只追加，不修改） | **冻结**（仅短期 context，不持久） |
| \(C\) | `self.run_step` 函数（推理-行动-观察三步循环） | **冻结**（代码逻辑不可改） |

四个组件全部冻结。这就是"**静态形态**"的精确定义。

### 4.2 ReAct 中 U 的状态

\[
U(B, \tau, r, \mathcal{C}) = \text{undefined}
\]

ReAct **没有元控制器**。不存在任何机制能把 \(\tau, r, \mathcal{C}\) 反馈回 B 的修改。这与第 11 章的"自进化定义"形成鲜明对比：

> **可修改 ≠ 自进化**。能修改 B 但没有效果不算自进化。

ReAct 既**不能修改 B**（缺乏 U），也**没有进化效果**——它是一个彻底冻结的 Agent。

### 4.3 ReAct 是"循环的形态骨架"而非"自进化形态"

我们可以用一个比喻：ReAct 是 LLM Agent 的**循环骨架（loop skeleton）**，但不是**形态（morphology）**。它定义了 Agent 每一步应该做什么（Thought-Action-Observation），但它没定义 Agent 的身体如何在世界中长期演化。

这正是本书第 11 章的切入点：如果我们保持 ReAct 的循环结构不变，但允许 Agent 在循环之外添加一个**U 函数**来周期性地修改 B，Agent 就从"静态形态"变成"动态形态"。Reflexion 是这一转化的第一步（让 U 修改 M），Toolformer 是另一种特殊形态（让 U 在训练阶段修改 T 的"使用模式"）。

### 4.4 ReAct 在 L0-L5 等级中的位置

按本书第 18 章的 Agent 等级：
- **L0 静态 LLM**：无 Agent 循环
- **L1 Tool-using**：能调用工具但无显式推理
- **L2 ReAct Agent**：Thought-Action-Observation 循环（**ReAct 处于此级**）
- **L3 Reflective**：在 L2 基础上加入跨 episode 反思（**Reflexion 处于此级**）
- **L4 Self-Modifying**：在 L3 基础上加入 P/T/M 自修改（OPRO、LATM、A-MEM 等）
- **L5 Self-Evolving**：在 L4 基础上加入 C 自修改 + U（Gödel Agent、SICA 等）

ReAct 是 L2，**L2 没有 U**。

## 5. 实验与结果

ReAct 在 4 个领域做了实验，我们逐个分析与操作形态学的关联：

### 5.1 HotPotQA（多跳问答）

- 数据集：113k Wikipedia-based 多跳问答
- ReAct vs CoT vs Act-only
- 结果：ReAct 在 exact match 上达到 27.4%，优于 CoT-only（25.7%）和 Act-only（20.6%）
- 操作形态学意义：**Thought 提升了 B 中 P 的有效性**（让 LLM 更好地选择工具）。但 Thought 是 prompt 中固定的一段，不是动态修改的 P——它属于"先验内置"，不是"运行时演化"。

### 5.2 Fever（事实核查）

- 数据集：185k claim verification 任务
- ReAct 准确率达到 60.9%，略低于 CoT（64.6%）但显著高于 Act-only（41.7%）
- 操作形态学意义：ReAct 在事实核查这种"需要外部证据"的任务上表现不如纯 CoT——这暗示 Thought 并不总是有效；在某些领域，"少想多做"反而更好。

### 5.3 ALFWorld（具身文本游戏）

- 数据集：25 类具身家务任务（如"把咖啡放到桌上"）
- ReAct 成功率 71%，Act-only 仅 45%
- 操作形态学意义：ReAct 在**需要长视野规划的具身任务**上显著优于 Act-only——Thought 提供了"子目标分解"能力。这是操作形态学意义上"Thought 是 Agent 的内部 T（子目标生成器）"的早期证据。

### 5.4 WebShop（在线购物）

- 数据集：118 万件商品，1.6 万条用户指令
- ReAct 任务成功率 28.7%，Act-only 22.1%，Human 50%
- 操作形态学意义：ReAct 与 Human 之间还有 21.3% 的巨大差距，这部分差距很大程度上来自"工具不足"——ReAct 的 T 只有 search 和 click，而 Human 能"打电话给客服""查论坛""对比多家价格"等。如果允许 ReAct 运行时扩展 T（即 T 自修改），这个差距可能缩小——这就是第 13 章讨论的 LATM/Voyager 范式。

### 5.5 关键实验观察

四个领域的合并数据揭示一条规律：**ReAct 的优势在"需要长视野推理"的领域（ALFWorld）最明显；在"单步可解"的领域（Fever）优势缩小甚至反转**。这条规律与本书 H3 假设（形态适配）一致——不同任务环境演化出不同的 B 结构；但 ReAct 是静态 B，不能适配，这是其根本限制。

## 6. 局限与开放问题

ReAct 的局限可以分为三类：**结构层、数据层、能力层**。这一节是本书对 ReAct 的批判性分析。

### 6.1 结构层局限：Thought 的可靠性

ReAct 假设 LLM 生成的 Thought 是"诚实推理"——但 LLM 可能生成**事后合理化的 Thought**（post-hoc rationalization）。这与第 22 章讨论的"prompt injection"和"alignment faking"直接相关：当 LLM 受到 prompt 注入攻击时，Thought 可能被攻击者控制，使 ReAct 成为攻击的执行器。

更根本的问题是：**Thought 是否是 Agent 的"内部状态"？** 答案是否定的。Thought 只是 LLM 的输出，它没有独立于 LLM 参数的真实性。ReAct 把 Thought 当成可观察的内部状态，但实际上它是 LLM 隐变量的一次采样。这就是为什么 r-note-004 主张"Thought 必须经过验证才能被信任"。

### 6.2 数据层局限：Few-shot Prompt 的脆弱性

ReAct 依赖**手工设计的 6-shot example**。这个 prompt 在 PaLM 540B 上工作良好，但：
- 换到 GPT-4 时需要重新调优（GPT-4 对 prompt 格式更敏感）
- 换到小模型（7B、13B）时效果急剧下降（Reasoning 能力不足）
- 换到非英语任务时 Thought 质量下降

这意味着 **ReAct 的 P 组件是 brittle 的**——一个 prompt 在某个 (model, task, language) 三元组上工作，并不保证它在另一个三元组上工作。这正是第 12 章自修改 P 的动机：**与其人工调优 prompt，不如让 Agent 自己演化 prompt**（OPRO）。

### 6.3 能力层局限：没有跨 episode 记忆

ReAct 的 `self.history` 只在单次 `run()` 内累积，进程结束后清空。Agent 不能"记住上次在 HotPotQA 上学到的推理模式"——每次 `run()` 都是 cold start。

这是 ReAct 最大的局限，也是 **Reflexion** 直接要解决的问题：Reflexion 在 ReAct 之上添加**跨 episode 反思存储**，把每轮的反思作为下一次 prompt 的前缀，从而让 Agent 在多 episode 中持续改进。Reflexion 是操作形态学意义上第一个"修改 M"的元控制器 U——见 r-paper-002。

### 6.4 与现代 Agent 框架的兼容性

ReAct 设计于 2022 年底，那时 Function Calling 协议尚未标准化。ReAct 用自然语言 prompt 让 LLM 输出 `Action: search[...]` 这种字符串，再用正则解析。这导致：
- **解析错误率高**：LLM 输出的格式可能不完全符合 prompt 示例
- **不支持复杂参数**：嵌套 JSON、枚举、变长数组很难用自然语言表达
- **无法与现代 Function Calling 互操作**：2024 年后的 Function Calling 直接生成结构化 JSON，无需 prompt 解析

这一兼容性局限使 ReAct 在生产环境逐渐被 Toolformer-style 训练或 OpenAI Function Calling 取代。但 ReAct 的**循环思想**仍然存活——所有现代 Agent（OpenAI o1 Agents、Claude Computer Use、Replit Agent、Devin 等）的内部循环本质上都是 ReAct。

### 6.5 开放问题

| 问题 | 当前共识 | 本书视角 |
|---|---|---|
| ReAct 是否需要 Thought？ | 在长视野任务上需要 | Thought 应被视为可被 U 调节的 P 组件 |
| ReAct 能否扩展到多 Agent？ | 可以（Multi-Agent ReAct） | 多 Agent 是 B 中 C 的特例（Agent 协作逻辑） |
| ReAct 是否需要持久记忆？ | 是（Reflexion 已证明） | 持久记忆是 M 的自修改 |
| ReAct 能否自演化 B？ | 不能（缺乏 U） | 需要添加元控制器 U 才能进入 L4 |

## 7. 对本书的贡献

ReAct 在本书的理论体系中扮演双重角色：**循环骨架的源头**与**静态形态的代表**。

### 7.1 ReAct 作为循环骨架

本书第 1 章、第 2 章、第 11 章的所有"四元反馈环"图示都继承自 ReAct 的 Thought-Action-Observation 结构。第 17 章的"U 设计"也建立在 ReAct 循环之上——U 是**外加于 ReAct 循环**的元层，它观察 ReAct 循环的输出（轨迹、奖励），然后修改 B。第 18 章 MorphAgent 参考实现的内层循环就是 ReAct 风格的：

```python
# MorphAgent 内层（ReAct 风格）
def inner_loop(self, query):
    ctx = self.P["system"] + "\n" + query
    for _ in range(self.max_inner_steps):
        t, a, o = self._react_step(ctx)
        ctx += f"Thought: {t}\nAction: {a}\nObservation: {o}\n"
        if a.name == "Finish":
            return a.answer
    return self._fallback()
```

外层循环才是 U（修改 B 的元控制器）。**ReAct 是内层，U 是外层**——这一分层是本书架构的基础。

### 7.2 ReAct 作为静态形态代表

本书第 11 章 H1 假设的对比组之一就是"ReAct 风格的静态 B"。具体地：
- 实验组 Frozen（无 U，固定 B）≈ ReAct
- 实验组 Joint-coordinated（完整 U，动态 B）≈ 自进化的 MorphAgent

在 MorphBench 中，ReAct 提供**L2 等级基线**：所有 L4、L5 的自进化 Agent 都应该显著优于 ReAct，否则 H1 假设被反驳。这是 ReAct 在实验设计中的角色。

### 7.3 ReAct 与本书 H1-H5 的关系

| 假设 | ReAct 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | ReAct 无 B 可塑性 | Frozen 基线，提供"无 U"对照 |
| **H2 协同演化** | ReAct 的 P、T、M、C 独立设计但不可修改 | 联合优化基线（如果未来把 P/T/M/C 改为可调） |
| **H3 形态适配** | ReAct 的 B 在所有任务上相同 | 不支持 H3（不支持形态适配） |
| **H4 迁移收益** | ReAct 无跨 episode 记忆 | 不支持 H4（无形态迁移可言） |
| **H5 治理必要性** | ReAct 无 B 修改，无治理需求 | 无验证（无需治理，但也没有自进化能力） |

### 7.4 给读者的关键启示

1. **ReAct 是必要起点**：所有 LLM Agent 的工作都建立在 ReAct 循环之上，理解 ReAct 是理解后续所有工作的前提。
2. **ReAct 不是终点**：ReAct 的"静态形态"是本书要超越的对象。如果一个 Agent 只有 ReAct 循环而没有 U，它就是一个 L2 Agent，不能称为"自进化"。
3. **Thought 是双刃剑**：Thought 提升了 LLM 的推理可观察性，但也成为 LLM 攻击面（prompt injection）。ReAct 的 Thought 不是"安全结构"。
4. **ReAct → Reflexion → LATM 是同一条线**：这三个工作分别对应 B 中 M 和 T 的自修改。它们共同构成从 L2 到 L4 的进化路径。

ReAct 是本书 Part I 的结束（理论起点），也是 Part II（操作形态学）和 Part III（自修改实现）的开始——它定义了我们要扩展的对象，也定义了我们要突破的边界。

## 参考文献

- yao2023react: Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K. R., & Cao, Y. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. [$TRAE_REF](https://arxiv.org/abs/2210.03629)
- yao2023react（重复键为占位以保持 related_papers 数组可索引）：同上。
- wei2022cot: Wei, J., et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models*. NeurIPS 2022.
- shinn2023reflexion: Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS 2023. 见 r-paper-002。
- schick2023toolformer: Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. NeurIPS 2023. 见 r-paper-003。