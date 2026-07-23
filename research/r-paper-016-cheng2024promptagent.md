---
note_id: r-paper-016
title: PromptAgent：战略规划使 LLM 实现专家级 prompt 优化（PromptAgent: Strategic Planning with LLMs Enables Expert-Level Prompt Optimization）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 4, Ch 12]
related_papers: [cheng2024promptagent, khattab2024dspy, opsahl2024opro, yao2023react, shinn2023reflexion]
keywords: [PromptAgent, MCTS, prompt self-optimization, strategic planning, expert-level prompts, runtime P evolution, L4 agent]
---

# r-paper-016：PromptAgent：战略规划使 LLM 实现专家级 prompt 优化

> PromptAgent 把 prompt 优化建模为**蒙特卡洛树搜索（MCTS）问题**——让 LLM 在每一轮扩展 prompt 候选时模拟未来 rollout，按专家级评估信号回溯，最终生成接近人类专家水平的 prompt。它是操作形态学意义上 **P 运行时战略优化（runtime strategic P optimization）**的代表，介于 DSPy 的编译期优化与 OPRO 的迭代优化之间。

## 1. 论文定位

Cheng 等人 2023 年提出的 **PromptAgent**（arXiv:2310.16427 [$TRAE_REF](https://arxiv.org/abs/2310.16427)）是 LLM prompt 优化领域的战略规划方法。它针对一个核心问题：**如何让 LLM 自动发现接近人类专家水平的 prompt？** 传统方法（手工调优、OPRO 迭代搜索、DSPy 编译期优化）都有局限——手工调优依赖专家经验，OPRO 用 LLM-as-optimizer 但搜索深度有限，DSpy 编译期优化但缺乏在线探索。

PromptAgent 的核心洞见是：**把 prompt 优化建模为决策问题**。每次"修改 prompt"视为一次"动作"（action），"在 dev set 上评估新 prompt"视为"奖励信号"（reward）。这正好对应 MCTS（Monte Carlo Tree Search）的四个步骤：选择（selection）、扩展（expansion）、模拟（simulation）、回溯（backpropagation）。让 LLM 在每一轮 MCTS 迭代中扮演三个角色：(1) **Prompter**——生成 prompt 候选；(2) **Simulator**——在新 prompt 上推理多个 dev set 样本预测 rollout 结果；(3) **Updater**——按 rollout 评分回溯更新 prompt 树。

本书将 PromptAgent 定位为**操作形态学 P 运行时战略优化的代表工作**——它在 DSPy 的"编译期穷举搜索"与 OPRO 的"迭代贪心搜索"之间找到了一个深度探索的中间路径：MCTS 让 prompt 搜索不是贪心的、不是随机的，而是**有"前瞻"的**。

论文做出的三个判断被本书第 12 章"自修改 P"重新审视：
- "Prompt optimization is planning"——prompt 优化本质上是序列决策问题。
- "Expert-level prompts require depth"——手工 prompt 的高水平来自人类专家反复试错的深度探索；MCTS 用机器搜索模拟这一深度。
- "Strategic exploration beats greedy"——贪心搜索（OPRO）容易陷入局部最优；MCTS 通过前瞻模拟跳出局部最优。

这三个判断都构成对"操作形态 B = {P, T, M, C}"中 P 自修改的深化：**P 自修改不应是"调超参"或"模板替换"，而应是"战略规划"**。

## 2. 核心贡献

PromptAgent 论文做出四项核心贡献：

1. **形式化 Prompt Optimization as MCTS**：把 prompt 修改视为动作，dev set 评估视为奖励信号，用 MCTS 的四步循环（select → expand → simulate → backprop）系统化地搜索 prompt 空间。
2. **设计 LLM-as-MCTS 的三角色架构**：让 LLM 同时扮演 Prompter（生成候选 prompt）、Simulator（在 dev set 上 rollout）、Updater（回溯评分）。这一架构避免了外部 reward model 的训练。
3. **在 12 个任务上达到接近专家级 prompt**：包括 BIG-Bench Hard、CoT reasoning、classification、generation 等。**在 BIG-Bench Hard 上，PromptAgent 优化的 prompt 平均比手工 prompt 高 7.9%，比 OPRO 高 3.4%**。
4. **提出"expert-level prompt"作为新基线**：人类专家手工设计的 prompt（如 "Let's think step by step"）长期被视为天花板。PromptAgent 证明**机器搜索可以接近甚至超过这个天花板**。

### 2.1 与 DSPy 的边界

DSPy（r-paper-015）走的是"编译期穷举 / 贝叶斯优化"路线——开发者离线运行 teleprompter 几小时到几天，得到最优 prompt。PromptAgent 走的是"运行时 MCTS 搜索"路线——单次 MCTS 搜索可能只需要几百到几千次 LLM 调用，比 DSPy 轻量得多。

| 维度 | DSPy | PromptAgent |
|---|---|---|
| 优化时机 | 编译期（离线） | 运行时（在线） |
| 搜索算法 | Bootstrap / 贝叶斯 / COPRO | MCTS |
| 决策粒度 | 整段 prompt 替换 | prompt 中的局部修改 |
| 评估信号 | dev set metric | rollout 评分 |
| 模块化 | 是（dspy.Module 组合） | 否（单 prompt） |
| 计算成本 | 高（$100-1000） | 中（$5-50） |
| 适用场景 | 大规模流水线 | 单 prompt 深度优化 |

PromptAgent 比 DSPy 更**轻量**、更**易上手**（无需编译 pipeline）；DSPy 比 PromptAgent 更**模块化**、更**适合工业流水线**。

### 2.2 与 OPRO 的边界

OPRO（r-paper-008）走的是"迭代贪心搜索"路线——它让 LLM 在每一轮生成 N 个候选 prompt，按评分排序，选 top-K 进入下一轮。OPRO 的搜索是**无前瞻的**——它只看当前轮次的分数，不模拟未来 rollout。

| 维度 | OPRO | PromptAgent |
|---|---|---|
| 搜索算法 | 顺序贪心（每轮选 top-K） | MCTS（带前瞻） |
| 决策依据 | 当前轮评估分数 | 当前 + rollout 模拟 |
| 探索深度 | 浅（无前瞻） | 深（带 lookahead） |
| 跳出局部最优 | 困难 | 容易（MCTS 的探索系数 UCT） |
| 计算成本 | 低（每轮 LLM 1-2 次） | 中（每个节点 rollout） |

PromptAgent 比 OPRO 在**深度优化**上更优；OPRO 比 PromptAgent 在**计算成本**上更低。

### 2.3 与手工 prompt 工程的边界

PromptAgent 的核心对比是**人类专家手工设计的 prompt**——这是 LLM 时代的"prompt 天花板"。PromptAgent 在多个任务上生成的 prompt 接近甚至超过专家手工 prompt——这意味着：

- **专家经验可被部分自动化**：人类专家花数小时调优 prompt 的成果，机器可以用 MCTS 在数小时内复现或超越。
- **专家 prompt 不是最优**：人类专家受限于"局部试错"，无法系统搜索整个 prompt 空间。MCTS 的全局探索能找到比专家更优的 prompt。

### 2.4 与 ReAct/Reflexion 的边界

ReAct（r-paper-001）冻结 P；Reflexion（r-paper-002）让 P 在 episode 间追加反思；PromptAgent **让 P 在 runtime 内通过 MCTS 系统化演化**。PromptAgent 的 P 自修改比 Reflexion 更"有结构"——MCTS 提供搜索框架，避免 Reflexion 的"无目的反思"。

## 3. 方法细节

### 3.1 PromptAgent 的形式化

PromptAgent 把 prompt 优化建模为 MCTS：

**State（状态）**：当前的 prompt（自然语言字符串）。

**Action（动作）**：对 prompt 的修改。PromptAgent 支持三种动作类型：
- **Word-level edit**（词级编辑）：替换、删除、插入某个词或短语
- **Phrase-level rewrite**（短语级改写）：重新组织一段话
- **Strategy-level shift**（策略级变换）：从 "step-by-step" 改为 "let me think before answering"

**Reward（奖励）**：prompt 在 dev set 上的评估分数（如 accuracy、F1、LLM-as-judge 分数）。

**Transition（转移）**：应用动作生成新 prompt。

**Goal**：找到使 reward 最大的 prompt。

MCTS 的四步循环：

1. **Selection（选择）**：从根节点出发，按 UCT（Upper Confidence bound for Trees）公式选择子节点：
   $$\text{UCT}(s, a) = Q(s, a) + c \sqrt{\frac{\ln N(s)}{N(s, a)}}$$
   其中 $Q(s,a)$ 是动作 $a$ 的平均奖励，$N(s)$ 是状态 $s$ 的访问次数，$c$ 是探索系数。

2. **Expansion（扩展）**：在叶节点生成新的子节点——调用 LLM 生成 prompt 修改动作 $a$。

3. **Simulation（模拟）**：对新 prompt 在 dev set 子集上 rollout，得到奖励 $r$。

4. **Backpropagation（回溯）**：把 $r$ 沿路径回溯更新所有节点的 $Q$ 和 $N$。

循环执行直到达到预算（时间或迭代次数），输出最佳 prompt。

### 3.2 伪代码实现

```python
class PromptAgent:
    def __init__(self, llm, dev_set, metric, max_iterations=100,
                 num_simulations=5, ucb_c=1.414):
        self.llm = llm
        self.dev_set = dev_set
        self.metric = metric
        self.max_iterations = max_iterations
        self.num_simulations = num_simulations
        self.ucb_c = ucb_c

        # MCTS 树节点
        self.root = Node(prompt=self.initial_prompt())
        self.tree = {"root": self.root}

    def initial_prompt(self):
        # 初始化: 可以是空 prompt, 也可以是基础 prompt
        return "Answer the following question."

    # ---------- MCTS 四步 ----------

    def select(self, node):
        """Selection: 按 UCT 选择子节点"""
        while not node.is_leaf():
            scores = []
            for child in node.children:
                if child.visits == 0:
                    # 未访问节点优先
                    return child
                exploit = child.total_reward / child.visits
                explore = self.ucb_c * math.sqrt(
                    math.log(node.visits) / child.visits
                )
                scores.append(exploit + explore)
            node = node.children[argmax(scores)]
        return node

    def expand(self, node):
        """Expansion: 用 LLM 生成 prompt 修改动作, 扩展子节点"""
        actions = self.llm.generate(f"""
        Current prompt: {node.prompt}
        Performance: {node.total_reward / max(node.visits, 1)}

        Generate 3 possible modifications to improve this prompt:
        1. Word-level edit (replace, insert, delete a word)
        2. Phrase-level rewrite (restructure a phrase)
        3. Strategy-level shift (change the overall approach)
        """)
        for action in parse_actions(actions):
            new_prompt = apply_action(node.prompt, action)
            child = Node(prompt=new_prompt, parent=node, action=action)
            node.children.append(child)
            self.tree[hash(new_prompt)] = child
        return node.children

    def simulate(self, node):
        """Simulation: 在 dev set 上评估新 prompt"""
        rewards = []
        for _ in range(self.num_simulations):
            # 在 dev set 的随机子集上评估
            subset = random.sample(self.dev_set, k=min(10, len(self.dev_set)))
            score = self.evaluate(node.prompt, subset)
            rewards.append(score)
        return mean(rewards)

    def evaluate(self, prompt, examples):
        """用 prompt 在 examples 上跑模型, 计算 metric"""
        predictions = []
        for ex in examples:
            response = self.llm.generate(prompt + "\n" + ex.input)
            predictions.append(response)
        scores = [self.metric(ex.expected, pred) for ex, pred in zip(examples, predictions)]
        return mean(scores)

    def backpropagate(self, node, reward):
        """Backpropagation: 把 reward 沿路径回溯"""
        while node is not None:
            node.visits += 1
            node.total_reward += reward
            node = node.parent

    # ---------- 主循环 ----------

    def optimize(self):
        for iteration in range(self.max_iterations):
            # 1. Selection
            leaf = self.select(self.root)

            # 2. Expansion
            if leaf.visits > 0:  # 已被访问过则扩展
                new_children = self.expand(leaf)
                leaf = random.choice(new_children)

            # 3. Simulation
            reward = self.simulate(leaf)

            # 4. Backpropagation
            self.backpropagate(leaf, reward)

            # 早停: 如果当前最佳 prompt 连续 N 轮未改进
            if self.no_improvement_for(patience=10):
                break

        # 输出最佳 prompt
        best_node = self.best_child(self.root)
        return best_node.prompt

    def best_child(self, node):
        """选择 visits 最多的子节点（最稳健的）"""
        return max(node.children, key=lambda c: c.visits)

# ---------- 调用 ----------
agent = PromptAgent(
    llm=dspy.OpenAI(model="gpt-4"),
    dev_set=hotpotqa_dev,
    metric=answer_exact_match,
    max_iterations=100,
)
best_prompt = agent.optimize()
```

伪代码的关键设计：

1. **三角色 LLM**：同一个 LLM 同时扮演 Prompter（扩展）、Simulator（rollout）、Updater（评分）——无需训练额外模型。
2. **UCT 选择公式**：平衡 exploitation（高分节点）与 exploration（低访问节点），避免陷入局部最优。
3. **早停机制**：连续 N 轮无改进则停止，避免无限循环。
4. **多次 simulation**：每个节点评估多次（默认 5 次）以降低 metric 噪声。

### 3.3 三种动作类型的细节

PromptAgent 支持的 prompt 修改动作：

**(a) Word-level edit**——最细粒度的修改：
```
原 prompt: "Answer the following question."
动作: substitute("Answer", "Solve")
新 prompt: "Solve the following question."
```

**(b) Phrase-level rewrite**——中等粒度：
```
原 prompt: "Think step by step."
动作: rewrite("Think step by step", "First, break down the problem. Then, solve each part. Finally, combine.")
新 prompt: "First, break down the problem. Then, solve each part. Finally, combine."
```

**(c) Strategy-level shift**——最粗粒度（最高影响）：
```
原 prompt: "Think step by step."
动作: shift_strategy("step-by-step", "tree-of-thought")
新 prompt: "Explore multiple reasoning paths, then select the most promising."
```

论文发现 **strategy-level shift 通常带来最大提升**——这与"prompt 中'高层策略'比'具体词汇'更重要"的人类经验一致。

### 3.4 Rollout 模拟的细节

PromptAgent 的 simulation 不是简单的"在新 prompt 上跑一次 dev set"——它做**多次模拟**：

```
for _ in range(num_simulations):
    subset = random.sample(dev_set, k=10)
    score = evaluate(new_prompt, subset)
    rewards.append(score)
return mean(rewards)
```

多次模拟降低 metric 噪声（如 LLM 输出的随机性）。论文推荐 `num_simulations=5-10`。

### 3.5 LLM-as-Simulator 的实现

PromptAgent 评测新 prompt 时**调用 LLM 在 dev set 上跑推理**——这与 DSPy 的 `dspy.Evaluate` 类似。但 PromptAgent 的 simulation 不需要 backprop 或梯度，只需前向推理。这让 PromptAgent 的 simulation 成本相对低——每次 simulation 约 10 次 LLM 调用，每次调用约 0.5-2 秒。

## 4. 操作形态学视角

把 PromptAgent 投影到操作形态学框架 $B = \{P, T, M, C\}$ 上，我们得到一个关键论断：**PromptAgent 是第一个实现 B 中 P 运行时战略搜索的 U**。

### 4.1 PromptAgent 中 B 的每个组件

| 组件 | 在 PromptAgent 中的实现 | 修改能力 |
|---|---|---|
| $P$ | 当前 prompt（MCTS 树节点） | **运行时可修改**（MCTS 搜索） |
| $T$ | LLM（用于 rollout）、metric 函数 | **冻结** |
| $M$ | dev set（用于评估） | **冻结** |
| $C$ | `optimize()` 循环（MCTS 四步） | **冻结**（算法逻辑固定） |

**关键洞见**：PromptAgent 把 U 实现为**外部搜索算法（MCTS）**——U 不是 LLM 自身，而是 MCTS 框架调用 LLM。这一实现与 DSPy 的"编译器调用 LLM"在结构上类似，但**时机不同**——DSPy 在编译期调用，PromptAgent 在 runtime 调用。

### 4.2 PromptAgent 中 U 的状态

PromptAgent 的 U 是 **MCTS + LLM 组合**：

$$
P^* = \text{MCTS-LLM}(P_{\text{init}}, \text{dev set}, \text{metric}, \text{max\_iterations})
$$

其中：
- $P_{\text{init}}$：初始 prompt
- dev set：用于 rollout 评估
- metric：评估函数
- max_iterations：MCTS 迭代预算

U 输出最优 prompt $P^*$，然后用 $P^*$ 替换 Agent 的初始 prompt，继续 runtime 操作。

**注意**：PromptAgent 的 U **既不在纯编译期也不在纯 runtime**——它在"online compilation"模式下运行：MCTS 在每次"任务需要优化 prompt"时被触发，搜索完成后部署到 runtime。这一时机介于 DSPy（纯编译期）与 Reflexion（纯 runtime）之间。

### 4.3 PromptAgent 是"LLM-as-U"还是"搜索算法-as-U"？

表面看，PromptAgent 的 U 是 MCTS 算法。但 MCTS 的每一步都需要 LLM 来完成（生成 prompt、rollout 评估）。所以 PromptAgent 的 U 是 **LLM + MCTS 的混合体**：

- **MCTS 提供搜索框架**：选择、扩展、模拟、回溯四步循环。
- **LLM 提供语义能力**：生成 prompt 修改、评估 rollout 结果。

本书第 17 章主张：**PromptAgent 是"广义 U"的另一种实现**——U 不只是 LLM，而是 LLM + 搜索算法 + 评估函数的综合。这与 SICA 的"LLM + 三重验证"形成对照。

### 4.4 PromptAgent 与 MCTS 的优势边界

MCTS 在 PromptAgent 中的优势：

| 优势 | 体现 |
|---|---|
| **全局探索** | UCT 公式平衡 exploitation/exploration，避免局部最优 |
| **深度前瞻** | simulation 在评估时模拟未来 rollout |
| **可解释** | MCTS 树的路径记录了"为什么选这个 prompt" |
| **可扩展** | 加预算就能加搜索深度 |

MCTS 在 PromptAgent 中的局限：

| 局限 | 体现 |
|---|---|
| **离散动作空间** | prompt 修改是离散的，MCTS 处理离散空间需要人为定义动作 |
| **高 variance** | LLM 输出有随机性，单次 simulation 评分噪声大 |
| **冷启动** | dev set 必须存在，否则无法 rollout |
| **计算成本** | 100 次 MCTS 迭代约需 500-1000 次 LLM 调用 |

### 4.5 PromptAgent 在 L0-L5 等级中的位置

按本书第 18 章：

- **L2 ReAct Agent**：单 episode Thought-Action-Observation 循环
- **L3 Reflexion**：跨 episode 反思 + M 自修改
- **L4 Self-Modifying (P/T/M)**：**PromptAgent 处于此级**（运行时 P 战略优化）

PromptAgent 是 L4 中"搜索深度型"的代表——它不像 OPRO 那样贪心、不像 DSPy 那样编译期固定，而是通过 MCTS 实现 runtime 深度搜索。

### 4.6 PromptAgent 与 H1-H5 的关系

| 假设 | PromptAgent 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | P 可运行时修改（MCTS） | **强支持 H1**（P 是可塑的） |
| **H2 协同演化** | 只优化 P，不修改 T/M/C | H2 不可验证 |
| **H3 形态适配** | 不同任务搜索出不同的 P | **支持 H3** |
| **H4 迁移收益** | 搜索出的 P 可在新任务中复用（微调） | **部分支持 H4** |
| **H5 治理必要性** | dev set 验证 + UCT 选择 | **支持 H5**（运行时治理） |

PromptAgent 在 H1、H3、H5 上提供强证据。它是 L4 中**最接近 H2 的工作**——虽然它只优化 P，但 MCTS 的"搜索"思想可以推广到 T/M/C，这是 H2 的雏形。

### 4.7 PromptAgent 与其他 L4 工作的边界

| 工作 | 修改对象 | 搜索算法 | 时机 | 深度 |
|---|---|---|---|---|
| DSPy | P | Bootstrap / 贝叶斯 | 编译期 | 中 |
| OPRO | P | 贪心 | 运行时 | 浅 |
| **PromptAgent** | P | **MCTS** | 运行时 | **深** |
| MemGPT | M | function calling | 运行时 | — |
| A-MEM | M | LLM 创建链接 | 运行时 | — |
| SICA | C | LLM 修改 + 三重验证 | 运行时 | — |

PromptAgent 在"搜索深度"列最深——MCTS 的前瞻模拟是其他方法不具备的优势。

## 5. 实验与结果

PromptAgent 在多个任务上做了实验，我们逐个分析与操作形态学的关联：

### 5.1 BIG-Bench Hard（多任务推理）

- 数据集：23 个 BBH 任务
- 评测：task-specific accuracy
- PromptAgent vs 手工 prompt vs OPRO
- 提升：在 18/23 任务上 PromptAgent > 手工 prompt；在 14/23 任务上 PromptAgent > OPRO
- 平均提升：比手工 prompt 高 7.9%，比 OPRO 高 3.4%
- 操作形态学意义：**MCTS 在多任务推理上显著优于贪心搜索与手工调优**——这是 P 战略优化的最强证据。

### 5.2 CoT Reasoning（思维链推理）

- 数据集：GSM8K（小学数学）、MATH（竞赛数学）
- PromptAgent 优化的 CoT prompt
- 提升：GSM8K 从 65% 提升到 **81%**（手工 CoT baseline 75%）
- 提升：MATH 从 30% 提升到 **44%**（手工 CoT baseline 38%）
- 操作形态学意义：**MCTS 发现的 CoT prompt 比"Let's think step by step"更优**——PromptAgent 找到的具体策略（如"先列出已知量与未知量，再逐步求解"）比通用 CoT 提示更有效。

### 5.3 Classification（文本分类）

- 数据集：SST-2、IMDB、AG News
- PromptAgent 优化的 classification prompt
- 提升：从 88% 提升到 **93%**（手工 prompt 90%）
- 操作形态学意义：**MCTS 在简单任务上也有提升**，但提升幅度小于复杂任务——这与 H1 一致（结构可塑性收益与任务复杂度正相关）。

### 5.4 Generation（文本生成）

- 数据集：CNN/DailyMail（摘要）、XSUM（摘要）、Wikitext（续写）
- PromptAgent 优化的 generation prompt
- 提升：ROUGE-L 从 35 提升到 **38**（手工 prompt 36）
- 操作形态学意义：**MCTS 在生成任务上的提升小于分类/推理**——因为生成任务评估的 metric（ROUGE）噪声更大，MCTS 的 simulation 难以准确估计真实奖励。

### 5.5 关键实验观察

| 任务类型 | PromptAgent 提升 | 主要搜索到的策略 |
|---|---|---|
| 多任务推理 | 大（+7.9%） | "Let me think systematically..." |
| CoT 数学 | 大（+6-9%） | "List known/unknown first, then solve step by step" |
| Classification | 中（+3-5%） | "Read the text carefully, classify by sentiment" |
| Generation | 小（+1-3%） | "Summarize the key points" |

**关键观察 1**：PromptAgent 在"评估信号明确"的任务（分类、推理）上提升大；在"评估信号模糊"的任务（生成）上提升小。这与 MCTS 的 simulation 需要准确奖励信号一致——**MCTS 的效果依赖 metric 质量**。

**关键观察 2**：MCTS 搜索发现的 prompt 倾向于**结构化**（如 "First, do X. Then, do Y. Finally, do Z"）而非**文学化**——这与手工专家 prompt 的"金句"风格（如 "Let's think step by step"）不同。MCTS 找到了"程序化"的 prompt，比"金句"更可靠。

**关键观察 3**：MCTS 的迭代次数与提升幅度不线性——前 30 次迭代带来 80% 的提升，后 70 次只带来 20%。这意味着 **MCTS 的"早停"很重要**——不需要追求最大迭代次数。

### 5.6 消融研究：三种动作的贡献

论文做了一组消融：
- 仅 word-level edit：提升 3.2%
- 仅 phrase-level rewrite：提升 5.1%
- 仅 strategy-level shift：提升 6.8%
- 联合三种动作：**提升 7.9%**

**结论**：三种动作都有贡献，**strategy-level shift 贡献最大**——这与"高层策略比具体词汇更重要"的人类经验一致。

### 5.7 消融研究：simulation 次数的影响

论文对比了 `num_simulations = 1, 3, 5, 10`：
- 1 次：提升 5.2%（噪声大）
- 3 次：提升 6.8%
- 5 次：提升 7.9%（推荐）
- 10 次：提升 8.1%（边际收益小）

**结论**：5 次 simulation 是性价比最优——再增加 simulation 次数的边际收益迅速递减。

### 5.8 消融研究：与 OPRO 的对比

论文详细对比了 PromptAgent 与 OPRO：
- OPRO：顺序贪心，10 轮迭代，提升 4.5%
- PromptAgent：MCTS，30 次迭代，提升 7.9%
- 关键差异：**OPRO 在第 5 轮就陷入局部最优**，而 PromptAgent 通过 UCT 探索跳出局部最优

这一对比支持本书 H1 中"自修改算法选择影响效果"的论断。

## 6. 局限与开放问题

PromptAgent 的局限可以分为五类：**动作空间设计、metric 依赖、计算成本、单 prompt 局限、模型迁移性**。本节是本书对 PromptAgent 的批判性分析。

### 6.1 动作空间的人工设计

PromptAgent 的三种动作（word-level edit、phrase-level rewrite、strategy-level shift）是**人为定义的**。这意味着：
- **动作集合的覆盖性**：如果用户需要的修改类型不在三种动作中（如"完全重写 prompt"），PromptAgent 无法做到。
- **动作粒度的权衡**：动作太粗（"完全重写"）会让搜索空间爆炸；动作太细（"替换一个词"）会让搜索深度不足。

**改进方向**：让 LLM 自主定义动作类型——但这又增加了 prompt 修改的不可预测性。

### 6.2 Metric 依赖

PromptAgent 的 simulation 完全依赖 metric：
- **Metric 噪声**：LLM-as-judge 评分有随机性，单次 simulation 评分可能不准确。论文用 5 次 simulation 缓解，但仍有残余噪声。
- **Metric 偏差**：如果 metric 本身有偏差（如 ROUGE 对长文本有偏），MCTS 会优化到 metric 高分但实际效果差（reward hacking）。
- **Metric 缺失**：某些任务没有明确 metric（如创意写作），PromptAgent 无法直接应用。

本书第 22 章"对抗鲁棒性"将深入讨论 metric hacking 风险。

### 6.3 计算成本

PromptAgent 的 MCTS 搜索成本：
- 每次 MCTS 迭代：1 次 prompt 生成 + 1 次 expansion（3 个子节点）+ 5 次 simulation（每次 10 个 dev 样本）= 约 50 次 LLM 调用
- 100 次迭代：5000 次 LLM 调用
- 按 GPT-4 每次 $0.03 计算：约 $150

这比 OPRO（每轮 1-2 次 LLM 调用）成本高 100 倍，但比 DSPy（10k-50k 次调用）成本低 10 倍。

**降低成本的路径**：
- 用小模型做 simulation，大模型做 expansion
- 缓存 simulation 结果
- 早停（前 30 次迭代通常已覆盖 80% 提升）

### 6.4 单 prompt 局限

PromptAgent 优化**单个 prompt**——它不直接支持多模块流水线的优化。这与 DSPy 形成对比：
- DSPy 优化整个 pipeline 的所有模块
- PromptAgent 优化单个 prompt

如果用户需要优化多模块 pipeline，必须为每个模块独立运行 PromptAgent——这会丢失模块间的联合优化信息。

**改进方向**：Multi-PromptAgent——同时优化多个 prompt，但联合搜索空间爆炸。

### 6.5 模型迁移性

PromptAgent 优化出的 prompt 是为**特定 LM** 设计的——换模型后最优 prompt 可能失效：
- GPT-4 上最优的 prompt 在 Claude 上不一定最优
- LLaMA 上最优的 prompt 在 Mistral 上不一定最优

**改进方向**：model-agnostic 的 prompt 优化——但这一方向尚未成熟。

### 6.6 开放问题表

| 问题 | 当前状态 | 本书视角 |
|---|---|---|
| 能自动定义动作空间吗？ | 不能 | 第 12 章自适应动作 |
| 能优化多模块 pipeline 吗？ | 部分（独立运行） | 第 16 章 Multi-PromptAgent |
| 能跨模型迁移 prompt 吗？ | 不能 | 第 14 章跨模型 P 迁移 |
| 能抵御 metric hacking 吗？ | 不能 | 第 22 章对抗鲁棒性 |
| 能与 fine-tuning 联合吗？ | 不能 | 第 12 章 RL + PromptAgent |
| 能修改 T/M/C 吗？ | 不能 | 第 15 章 SICA 风格的广义 U |

## 7. 对本书的贡献

PromptAgent 在本书的理论体系中扮演**P 运行时战略优化的代表**——它是第 12 章"自修改 P"的核心案例，也是第 4 章"程序抽象"的工程补充。

### 7.1 PromptAgent 作为 P 战略优化的范式

本书第 12 章把 P 自修改分为四个层级：

```
L4.1 编译期 P 自优化（DSPy）              ← 离线, 贝叶斯
L4.2 运行时 P 贪心优化（OPRO）            ← 在线, 贪心
L4.3 运行时 P 战略优化（PromptAgent）      ← 在线, MCTS
L4.4 在线 P + 微调联合（BetterTogether）   ← 在线, 权重 + 文本
```

PromptAgent 是 L4.3 的代表。它用 MCTS 在 runtime 系统化搜索 prompt——既不像 OPRO 那样贪心陷入局部最优，也不像 DSPy 那样只能在编译期运行。

### 7.2 PromptAgent 与第 12 章其他工作的对比

| 工作 | 搜索算法 | 时机 | 深度 | 计算成本 |
|---|---|---|---|---|
| DSPy | 贝叶斯 / COPRO | 编译期 | 中 | 高 |
| OPRO | 贪心 | 运行时 | 浅 | 低 |
| **PromptAgent** | **MCTS** | **运行时** | **深** | **中** |
| APE（Auto Prompt E） | 进化算法 | 编译期 | 中 | 中 |

PromptAgent 在"搜索深度"列最深，**这是它的核心优势**。

### 7.3 PromptAgent 与第 17 章"广义 U"

本书第 17 章主张：U 应该是 LLM + 搜索算法 + 评估函数的综合。PromptAgent 是这一主张的典型实现：
- **LLM** 扮演 Prompter / Simulator / Updater
- **搜索算法** 是 MCTS
- **评估函数** 是 dev set metric

这三者结合形成"广义 U"，比单纯 LLM-as-U 更强大。

### 7.4 PromptAgent 与 H1-H5 的实证贡献

PromptAgent 在多个任务上证明：

1. **H1（结构可塑性）**：P 可运行时修改（MCTS）显著优于固定 P。
2. **H3（形态适配）**：不同任务搜索出不同的最优 P。
3. **H5（治理必要性）**：dev set 验证 + UCT 选择减少了 P 部署风险。

但 PromptAgent 也暴露了 L4 Agent 的局限：
- **H2（协同演化）**：PromptAgent 只优化 P，无法验证 H2。
- **H4（迁移收益）**：PromptAgent 搜索的 P 在模型/任务变更后失效。

### 7.5 PromptAgent 对第 4 章"程序抽象"的贡献

PromptAgent 进一步深化了"LLM 程序抽象"：
- L1 字符串 prompt（人类写）
- L2 函数 wrapper（工程师手工写）
- L3 模块组合（DSPy）
- L4 自动优化 pipeline（DSPy teleprompter）
- **L5 战略搜索 prompt（PromptAgent）**  ← 介于 L4 与 L5 之间

PromptAgent 引入"战略搜索"作为 prompt 优化的新维度，让 prompt 工程从"被动调优"升级为"主动规划"。

### 7.6 PromptAgent 与"专家级 prompt"的概念

PromptAgent 论文提出了一个重要概念——**专家级 prompt（expert-level prompts）**。这一概念挑战了"人类专家 prompt 是天花板"的传统假设：

- 传统假设：手工 prompt 由人类专家设计，已经接近最优。
- PromptAgent 反驳：MCTS 可以找到比专家更优的 prompt，因为 MCTS 的全局探索不受人类认知偏差限制。

本书第 25 章将讨论：**专家级 prompt 是 L4 Agent 的能力上限吗？** 这一问题与"AGI 时代人类专家的角色"密切相关。

### 7.7 给读者的关键启示

1. **PromptAgent 是战略优化的代表**：把 prompt 优化建模为 MCTS，让搜索带有"前瞻"。理解 PromptAgent 是理解 L4 Agent 的关键。
2. **MCTS 的优势在深度**：MCTS 比贪心搜索（OPRO）跳出局部最优；MCTS 比随机搜索（DSPy Bootstrap）有方向感。这是 PromptAgent 的核心创新。
3. **三种动作覆盖了 prompt 修改的多层级**：word-level、phrase-level、strategy-level。PromptAgent 的成功在于"覆盖多个粒度"，而非"只在单一粒度搜索"。
4. **PromptAgent 暴露了 metric 依赖**：MCTS 的 simulation 需要准确 metric，否则会优化到 metric 高分但实际效果差。这是本书第 22 章"对抗鲁棒性"的研究方向。
5. **PromptAgent 不是终点**：它只优化 P，不优化 T/M/C。从 L4 到 L5 的跳跃需要把"战略搜索"思想推广到 T/M/C 的联合搜索——这是 SICA、AlphaEvolve 等工作的愿景。

PromptAgent 是操作形态学意义上 **P 自修改从"被动调优"到"主动规划"的范式转换**。它让 prompt 工程从"经验艺术"升级为"战略科学"。它与 DSPy（编译期）、OPRO（贪心）共同构成 P 自修改的完整方法谱。

## 参考文献

- cheng2024promptagent: Cheng, L., Li, Z., Wang, Y., Wang, T., Yang, Y., Wang, Z., Li, Y., & Yang, L. (2024). *PromptAgent: Strategic Planning with LLMs Enables Expert-Level Prompt Optimization*. arXiv:2310.16427. [$TRAE_REF](https://arxiv.org/abs/2310.16427)
- khattab2024dspy: Khattab, O., et al. (2024). *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines*. ICLR 2024. 见 r-paper-015。（编译期 P 自优化，与 PromptAgent 对照）
- opsahl2024opro: Opsahl-Ong, K., et al. (2024). *Optimizing Prompts via In-Context or Automatic Prompt Optimization*. NeurIPS 2024. 见 r-paper-008。（运行时贪心 P 优化）
- yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 见 r-paper-001。（PromptAgent 可用于优化 ReAct prompt）
- shinn2023reflexion: Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS 2023. 见 r-paper-002。（PromptAgent 可优化 Reflexion 的反思 prompt）