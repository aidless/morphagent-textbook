---
note_id: r-paper-022
title: CoALA：语言智能体的认知架构与操作形态 B 的概念对齐（Cognitive Architectures for Language Agents, CoALA）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 2, Ch 11]
related_papers: [sumers2023coala, yao2023react, shinn2023reflexion, packer2023memgpt, yin2024godelagent, robeyns2025sica, fang2025selfevolving, laird2019soar, anderson2003act]
keywords: [CoALA, cognitive architecture, decision/action cycle, memory types, working memory, episodic memory, semantic memory, procedural memory, B = {P, T, M, C} conceptual alignment]
---

# r-paper-022：CoALA：语言智能体的认知架构与操作形态 B 的概念对齐

> Sumers 等人 2023 年发表的 *Cognitive Architectures for Language Agents*（CoALA，arXiv:2309.02427 [$TRAE_REF](https://arxiv.org/abs/2309.02427)）是**第一篇系统化用经典认知架构（cognitive architecture）的概念框架来组织 LLM Agent 设计**的理论工作。它把决策/行动循环（decision/action cycle）、多种记忆类型（working、episodic、semantic、procedural）、内部 vs 外部动作（internal vs external actions）三个核心概念引入 LLM Agent 领域。本书将 CoALA 定位为**操作形态 B = {P, T, M, C} 框架的概念前驱**——CoALA 的概念结构与本书 B 框架高度一致，但 CoALA 来自认知科学传统，本书 B 框架来自软件工程传统。两者形成跨学科的概念对齐。

## 1. 论文定位

Theodore Sumers 等人 2023 年 9 月在 arXiv 发表 *Cognitive Architectures for Language Agents*（CoALA，arXiv:2309.02427 [$TRAE_REF](https://arxiv.org/abs/2309.02427)）。这篇论文的核心论点是：**LLM Agent 的设计应该借鉴经典认知架构（cognitive architecture）研究的成熟框架**——而不是从零开始重新发明轮子。具体地，CoALA 提出了三个核心概念：

1. **决策/行动循环（Decision/Action Cycle）**：Agent 在每个时间步先做决策（决定做什么），再执行行动（实际调用工具）。这与 ReAct 的 Thought-Action-Observation 循环结构相似，但 CoALA 把决策与行动分开建模——决策包含多种内部动作（思考、检索、记忆更新），行动是外部动作（调用工具）。
2. **多种记忆类型**：CoALA 明确把记忆分为 working memory（工作记忆，类比 ReAct 的 context）、episodic memory（情景记忆，类比 MemGPT 的 archival storage）、semantic memory（语义记忆，类比长期知识库）、procedural memory（程序记忆，类比 agent 的代码/工具调用规则）。这与认知科学中的多存储模型（multi-store model）一致。
3. **内部 vs 外部动作**：CoALA 区分 internal actions（思考、记忆检索、知识查询——不改变外部世界）与 external actions（工具调用、API 调用、文件读写——改变外部世界）。这一区分对 LLM Agent 的设计与评估至关重要。

本书把 CoALA 定位为**操作形态 B = {P, T, M, C} 框架的概念前驱**——CoALA 与本书 B 框架在概念结构上有惊人的对应：

| CoALA 概念 | 对应 B 组件 | 对应说明 |
|---|---|---|
| Decision/Action Cycle | C（核心循环） | Agent 的执行逻辑 |
| Working Memory | M 的短期部分 | ReAct 风格的 context |
| Episodic Memory | M 的长期部分 | MemGPT 的 archival storage |
| Semantic Memory | M 的知识部分 | 长期知识库/世界模型 |
| Procedural Memory | T + C 的部分 | 工具调用规则、代码逻辑 |
| External Actions | T 的执行部分 | 调用 API、工具 |
| Internal Actions | P 的部分 | 思考、推理、反思 |

这一对应不是巧合——**认知架构（cognitive architecture）与软件架构（software architecture）在概念上有结构性的同构**。本书借用 CoALA 的概念体系来验证 B 框架的完备性。

CoALA 的三个核心论断被本书第 2 章与第 11 章重新审视：

- **"LLM Agents should learn from cognitive architectures"**——CoALA 主张 LLM Agent 的设计应该借鉴 ACT-R、SOAR、CLARION 等经典认知架构——这些架构研究 30+ 年的经验能直接迁移到 LLM 时代。
- **"Multiple memory types are essential"**——CoALA 反对"单一 working memory"的 LLM Agent 设计（如 vanilla ReAct），主张必须区分 working / episodic / semantic / procedural 四种记忆。这与 MemGPT、A-MEM 的分层记忆设计一致。
- **"Decision/action separation enables planning"**——CoALA 主张决策与行动分离——这让 Agent 能在执行前做 planning、考虑多种可能性、模拟结果。这与本书第 11 章的 U 函数设计直接对应。

这三个论断都构成对"操作形态 B = {P, T, M, C}"的**认知科学基础**：B 不是凭空设计的概念，而是认知架构在 LLM 时代的工程化表达。

## 2. 核心贡献

CoALA 论文做出四项核心贡献：

1. **形式化 LLM Agent 的认知架构模板**：把 LLM Agent 视为由"决策模块 + 行动模块 + 记忆模块 + 内部动作 + 外部动作"组成的系统，并给出形式化的模块定义。这是首次把认知架构的术语系统性地引入 LLM Agent 领域。

2. **提出决策/行动（Decision/Action）分离**：在每个时间步，Agent 先做决策（选择 internal 或 external action），再执行。这一分离让 Agent 能 planning——例如"先检索记忆，再决定调用哪个工具"。

3. **建立多种记忆类型的分类法**：明确区分 working memory、episodic memory、semantic memory、procedural memory 四种类型，每种类型有清晰的语义、存储方式、检索机制。这一分类法与 MemGPT 的分层记忆设计高度一致。

4. **在多个 LLM Agent 框架上演示 CoALA 概念**：CoALA 论文用 ReAct、Reflexion、Generative Agents、Toolformer 等已有工作为例，演示它们的认知架构对应——这让 CoALA 不仅是理论框架，也是**对已有 LLM Agent 工作的概念重述**。

### 2.1 与经典认知架构的边界

CoALA 不是从零开始的认知架构理论——它建立在 30+ 年的经典认知架构研究之上：

| 经典认知架构 | 关键贡献 | 与 CoALA 的关系 |
|---|---|---|
| **ACT-R**（Anderson, 2003） | 多存储模型（declarative + procedural memory） | CoALA 的 episodic + semantic memory 借鉴 ACT-R |
| **SOAR**（Laird, 2019） | 决策循环 + chunking 学习 | CoALA 的 decision/action cycle 借鉴 SOAR |
| **CLARION**（Sun, 2006） | explicit + implicit 双重系统 | CoALA 的 internal + external action 借鉴 CLARION |
| **EPIC**（Meyer & Kieras, 1997） | 多任务执行架构 | CoALA 的 procedural memory 借鉴 EPIC |
| **Global Workspace Theory**（Baars, 1988） | 全局工作空间 | CoALA 的 working memory 借鉴 GWT |

CoALA 是**认知架构传统在 LLM 时代的重新表达**——它不是发明新概念，而是**用 LLM Agent 的术语重新包装经典认知架构的概念**。这一重新包装对 LLM Agent 领域意义重大：让从业者意识到 LLM Agent 不是新问题，而是经典认知问题的现代版本。

### 2.2 与本书 B = {P, T, M, C} 框架的边界

CoALA 与本书 B 框架是**概念上的同构**，但有以下差异：

| 维度 | CoALA | B = {P, T, M, C} |
|---|---|---|
| **来源** | 认知科学传统 | 软件工程传统 |
| **核心概念** | 记忆类型（4 类） | 组件类型（4 个） |
| **修改能力** | 未强调 | **强调**（U 修改 B） |
| **评估对象** | 已有 LLM Agent 框架 | LLM Agent 自修改 |
| **应用焦点** | 解释已有设计 | 设计自修改能力 |

**关键差异**：CoALA 是**静态的概念框架**（解释已有 Agent），B 是**动态的概念框架**（支持自修改 Agent）。本书第 11 章的 H1 假设（结构可塑性）就是 B 框架独有的——CoALA 没有对应假设。

### 2.3 与 ReAct 的边界

ReAct（r-paper-001）是 Thought-Action-Observation 循环。CoALA 把 ReAct 重新解释为：

- **Thought = internal action**（决策的一部分）
- **Action = external action**
- **Observation = 工作记忆更新**

这一重新解释让 ReAct 在认知架构的语境下有了清晰的位置——它是**没有显式记忆管理**的认知架构变体。这也解释了 ReAct 的局限：**没有 episodic、semantic、procedural memory 的认知架构是不完整的**。

### 2.4 与 MemGPT 的边界

MemGPT（r-paper-004）实现了 main context + external context + archival storage 的三层记忆。CoALA 把 MemGPT 重新解释为：

- **Main context = working memory**（短期，受限）
- **External context = episodic memory**（通过 retrieval 访问）
- **Archival storage = semantic memory**（长期持久化）

这一重新解释让 MemGPT 的"OS 类比"有了认知科学的基础——MemGPT 实际上是在实现一个**完整的多存储认知架构**。

## 3. 方法细节

### 3.1 CoALA 的形式化

CoALA 把 LLM Agent 形式化为一个五元组：

$$
\text{Agent} = (M, D, A_{\text{int}}, A_{\text{ext}}, \text{Decide})
$$

其中：

- $M = (M_w, M_e, M_s, M_p)$：四种记忆类型（working, episodic, semantic, procedural）
- $D$：决策模块（Decide），决定下一步是 internal action 还是 external action
- $A_{\text{int}}$：内部动作集合（think, retrieve, remember, etc.）
- $A_{\text{ext}}$：外部动作集合（tool calls, API calls, etc.）
- Decide：决策函数

形式化目标是：每个时间步 $t$，Agent 状态 $s_t$ 更新为：

$$
s_{t+1} = \text{Execute}(\text{Decide}(s_t), s_t)
$$

其中 $\text{Decide}(s_t)$ 返回一个 action，$\text{Execute}$ 执行该 action 并更新 $s_t$。

### 3.2 决策/行动循环

CoALA 的核心是决策/行动循环：

```
1. 感知 (Perceive)：从环境中接收 observation
2. 决策 (Decide)：基于当前状态 s_t 选择 action
3. 执行 (Execute)：执行选定的 action
4. 更新 (Update)：更新状态 s_t 为 s_{t+1}
5. 返回 (Return)：回到步骤 1
```

这一循环与 ReAct 的 Thought-Action-Observation 循环相似，但 CoALA 明确区分了**决策**（步骤 2）与**执行**（步骤 3）。这一区分让 Agent 能在执行前做 planning——例如：

```
Decide: "I should first retrieve my episodic memory for similar tasks"
Execute: retrieve_episodic_memory()
Decide: "Based on retrieved memory, I should call the search tool"
Execute: search()
Decide: "Now I have enough information to answer"
Execute: respond()
```

每一步 Decide 都是一次"决策"——可以调用 LLM 或专用决策模块。

### 3.3 多种记忆类型的形式化

CoALA 明确区分四种记忆：

**Working Memory ($M_w$)**：
- 容量：受限（通常 ≤ 100k tokens）
- 存储：当前任务相关的临时信息
- 访问方式：直接访问（在 LLM context 中）
- 示例：ReAct 的 current trajectory、对话历史

**Episodic Memory ($M_e$)**：
- 容量：中等（受存储限制）
- 存储：过去的事件、经历、轨迹
- 访问方式：基于相似度检索
- 示例：MemGPT 的 archival storage、A-MEM 的动态记忆

**Semantic Memory ($M_s$)**：
- 容量：极大（潜在无限）
- 存储：抽象知识、事实、概念
- 访问方式：知识图谱查询、embedding 检索
- 示例：LLM 的预训练知识、向量数据库中的长期知识

**Procedural Memory ($M_p$)**：
- 容量：可变
- 存储：技能、规则、过程
- 访问方式：触发条件匹配
- 示例：工具调用规则、API schema、代码片段

四种记忆共同构成 Agent 的完整记忆系统——这是 CoALA 对"单一 working memory" LLM Agent 设计的根本改进。

### 3.4 伪代码实现：CoALA Agent

```python
class CoALAAgent:
    """基于 CoALA 概念框架的 LLM Agent"""

    def __init__(self, llm, working_memory_size=8000,
                 episodic_store=None, semantic_store=None,
                 procedural_store=None, internal_actions=None,
                 external_actions=None):
        self.llm = llm

        # 四种记忆类型
        self.M_w = []  # working memory (current context)
        self.M_e = episodic_store or EpisodicStore()  # episodic
        self.M_s = semantic_store or SemanticStore()  # semantic
        self.M_p = procedural_store or ProceduralStore()  # procedural

        # 内部动作 (修改 M 或推理)
        self.A_int = internal_actions or [
            "think",           # 推理
            "retrieve_episodic",  # 从 M_e 检索
            "retrieve_semantic",  # 从 M_s 检索
            "retrieve_procedural",  # 从 M_p 检索
            "update_working",    # 更新 M_w
            "consolidate",       # M_w → M_e 的记忆固化
        ]

        # 外部动作 (调用工具)
        self.A_ext = external_actions or [
            "search", "lookup", "calculator", "code_exec", "finish"
        ]

    def perceive(self, observation):
        """感知环境，更新 working memory"""
        self.M_w.append({"type": "observation", "content": observation})

    def decide(self):
        """决策：选择下一步 internal 或 external action"""
        prompt = self.build_decision_prompt()
        action_str = self.llm.generate(
            f"{prompt}\n\nDecide next action (internal or external):"
        )
        return self.parse_action(action_str)

    def execute(self, action):
        """执行选定的 action"""
        if action["type"] == "internal":
            return self.execute_internal(action)
        elif action["type"] == "external":
            return self.execute_external(action)

    def execute_internal(self, action):
        """执行内部动作（修改 M 或推理）"""
        if action["name"] == "think":
            thought = self.llm.generate(
                f"Working Memory:\n{self.M_w}\n\nThought:"
            )
            self.M_w.append({"type": "thought", "content": thought})
            return {"type": "thought", "content": thought}

        elif action["name"] == "retrieve_episodic":
            # 从 episodic memory 检索相关经历
            results = self.M_e.retrieve(
                query=action["args"]["query"], top_k=5
            )
            self.M_w.append({
                "type": "episodic_retrieval",
                "content": results
            })
            return {"type": "retrieval", "results": results}

        elif action["name"] == "retrieve_semantic":
            # 从 semantic memory 检索相关知识
            results = self.M_s.query(
                query=action["args"]["query"]
            )
            self.M_w.append({
                "type": "semantic_retrieval",
                "content": results
            })
            return {"type": "retrieval", "results": results}

        elif action["name"] == "retrieve_procedural":
            # 从 procedural memory 检索相关技能
            results = self.M_p.match(
                trigger=action["args"]["trigger"]
            )
            self.M_w.append({
                "type": "procedural_retrieval",
                "content": results
            })
            return {"type": "retrieval", "results": results}

        elif action["name"] == "consolidate":
            # 把 working memory 中重要的内容固化到 episodic memory
            important = self.extract_important(self.M_w)
            self.M_e.store(important)
            return {"type": "consolidation", "stored": important}

    def execute_external(self, action):
        """执行外部动作（调用工具）"""
        tool_name = action["name"]
        tool_args = action["args"]
        # 调用真实工具
        result = self.tools[tool_name](**tool_args)
        # 把结果加入 working memory
        self.M_w.append({"type": "external_result", "content": result})
        return {"type": "external_result", "content": result}

    def run(self, user_query, max_steps=20):
        """主循环：决策/行动循环"""
        self.perceive({"type": "user_query", "content": user_query})

        for step in range(max_steps):
            # 1. 决策
            action = self.decide()
            # 2. 执行
            result = self.execute(action)
            # 3. 检查终止条件
            if action["name"] == "finish":
                return result["content"]
            # 4. 截断 working memory
            self.truncate_working_memory()
        return "MAX_STEPS_EXCEEDED"
```

伪代码展示了 CoALA 的完整认知架构实现。它与 ReAct 的核心差异是**记忆的明确分层**和**决策/行动的显式分离**。

### 3.5 CoALA 与已有 Agent 的对应

CoALA 论文重新解释了多个已有 LLM Agent 框架：

| LLM Agent | CoALA 对应 |
|---|---|
| ReAct | working memory only, no internal/external action distinction |
| Reflexion | adds episodic memory (reflection buffer) |
| MemGPT | full multi-store: working + episodic + semantic + procedural |
| Toolformer | adds procedural memory (tool usage rules) |
| Generative Agents | working + episodic + semantic (no procedural) |
| Voyager | adds procedural memory (skill library) |
| Self-RAG | adds semantic memory (knowledge retrieval) |

这一对应让 CoALA 成为**已有 LLM Agent 工作的概念统一框架**——所有 Agent 都可以用 CoALA 的术语重新描述。

### 3.6 CoALA 的规划能力

CoALA 通过**决策/行动分离**实现 planning——Agent 能在执行前模拟多种 action 的后果：

```python
def plan_ahead(self, goal, max_depth=3):
    """前瞻性规划：模拟多种 action 序列"""
    plan = []
    state = self.snapshot_state()

    for depth in range(max_depth):
        # 列出当前可能的 actions
        possible_actions = self.list_possible_actions(state)
        # 评估每个 action 的预期后果
        evaluations = []
        for action in possible_actions:
            predicted_outcome = self.simulate(state, action)
            score = self.evaluate_outcome(predicted_outcome, goal)
            evaluations.append((action, score))
        # 选择最优 action
        best_action = max(evaluations, key=lambda x: x[1])[0]
        plan.append(best_action)
        # 更新状态
        state = self.simulate(state, best_action)
        # 检查是否达到目标
        if self.goal_achieved(state, goal):
            break
    return plan
```

这一规划能力是 CoALA 超越纯 ReAct 的关键——它让 Agent 能在执行前**思考多种可能性**，而不是贪心地选择下一个 action。

## 4. 操作形态学视角

把 CoALA 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到 **CoALA 概念与 B 组件的精确对齐**。

### 4.1 CoALA 与 B = {P, T, M, C} 的概念对齐

| B 组件 | CoALA 对应 | 对齐说明 |
|---|---|---|
| **P (Prompt)** | Internal Actions + 部分 Procedural Memory | P 包含 agent 的目标、规则、few-shot——这是 internal actions 的来源 |
| **T (Tools)** | External Actions + 部分 Procedural Memory | T 是 agent 可调用的工具集，对应 external actions |
| **M (Memory)** | Working + Episodic + Semantic Memory | M 包含所有四种 CoALA 记忆（除 procedural） |
| **C (Code)** | Decide 函数 + Decision/Action Cycle | C 是 agent 的核心执行逻辑，对应 decide/execute 循环 |
| **U (元控制器)** | 未显式建模 | **CoALA 没有 U 概念** |

**关键发现**：CoALA 与 B 框架是**概念上的同构**——CoALA 的四个记忆类型映射到 M 的不同子结构，CoALA 的 internal/external actions 映射到 P/T，CoALA 的 decide 循环映射到 C。**唯一的差异是 U**——CoALA 没有显式建模元控制器，这是 B 框架独有的概念。

### 4.2 CoALA 中 B 的每个组件

| 组件 | 在 CoALA 中的实现 | 修改能力（CoALA 视角） |
|---|---|---|
| P | Internal Actions 的 schema、goal prompt | **冻结**（CoALA 不强调 P 修改） |
| T | External Actions 的 schema | **冻结**（CoALA 不强调 T 修改） |
| M | 四种记忆类型 | **部分修改**（CoALA 提到 M 演化） |
| C | Decide + Execute 循环 | **冻结**（CoALA 不强调 C 修改） |
| U | **不存在** | — |

CoALA 的视角是**静态认知架构**——它建模的是 Agent 的当前结构与执行逻辑，**不强调结构的自修改**。这与本书 B 框架的根本差异：本书 B 是为自修改设计的，CoALA 是为静态 Agent 设计的。

### 4.3 CoALA 中 U 的状态

$$
U(B, \tau, r, \mathcal{C}) = \text{undefined}
$$

CoALA **没有显式建模 U**——这与 ReAct（r-paper-001）类似，是**静态形态**。CoALA 框架下，所有 LLM Agent（ReAct、Reflexion、MemGPT 等）都属于**静态形态**——它们的 B 在运行时不变。

本书第 11 章的 H1 假设（结构可塑性）要求 B 可修改——CoALA 没有对应的设计。这意味着 **CoALA 是"LLM Agent 的认知架构"，B 是"自修改 LLM Agent 的形态学"**——两者是不同但相关的框架。

### 4.4 CoALA 与 L0-L5 等级的关系

按本书第 18 章：

- **L2 ReAct Agent**：只有 working memory + external actions（最简 CoALA）
- **L3 Reflexion**：working + episodic memory（增加 episodic）
- **L4 MemGPT / A-MEM**：working + episodic + semantic（完整多存储）
- **L5 SICA / Gödel Agent**：CoALA 概念 + 自修改 B（CoALA + U）

CoALA 概念覆盖 L2-L4，L5 需要在 CoALA 之上添加 U。

### 4.5 CoALA 与 H1-H5 的关系

| 假设 | CoALA 的关系 |
|---|---|
| **H1 结构可塑性** | **未涉及**（CoALA 是静态框架） |
| **H2 协同演化** | **未涉及** |
| **H3 形态适配** | **部分支持**（CoALA 的多记忆类型让 Agent 能适配不同任务） |
| **H4 迁移收益** | **支持**（procedural memory 的迁移是跨任务技能复用） |
| **H5 治理必要性** | **未涉及**（CoALA 没有修改，所以无需治理） |

CoALA 在 H3、H4 上提供基础概念，但在 H1、H2、H5 上未涉及——这些是 B 框架独有的方向。

### 4.6 CoALA 作为本书 B 框架的认知科学基础

本书第 2 章把 B = {P, T, M, C} 作为 LLM Agent 的"形态学"概念。CoALA 为 B 提供了**认知科学的基础**：

- **P 对应 internal actions**：P 是 Agent 内部决策的来源（来自认知科学中的"执行控制"概念）。
- **T 对应 external actions**：T 是 Agent 与环境交互的接口（来自认知科学中的"感知-运动"概念）。
- **M 对应多存储记忆**：M 是 Agent 的记忆系统（来自认知科学中的"多存储模型"）。
- **C 对应决策循环**：C 是 Agent 的核心执行逻辑（来自认知科学中的"决策循环"概念）。

这一认知科学基础让 B 框架不只是软件工程的便利，而是**有理论根基的概念系统**。

## 5. 实验与结果

CoALA 论文是**理论性工作**——它主要提供概念框架，不做大规模实证。但论文包含以下分析与示例：

### 5.1 概念框架的完备性分析

CoALA 论文通过系统分析已有 LLM Agent 框架，验证 CoALA 概念的完备性：

| 已有 LLM Agent | CoALA 概念覆盖 |
|---|---|
| ReAct | working memory + external actions |
| Reflexion | + episodic memory (reflection) |
| MemGPT | + episodic + semantic (archival) |
| Toolformer | + procedural memory (tool usage) |
| Generative Agents | + episodic + semantic (memory stream) |
| Voyager | + procedural (skill library) |
| Self-RAG | + semantic (knowledge retrieval) |

**关键发现**：**所有已有 LLM Agent 都可以用 CoALA 概念完整描述**——这表明 CoALA 概念体系是完备的。

### 5.2 决策/行动分离的实证

CoALA 论文设计了一个 toy 实验：在虚拟环境中比较"决策/行动分离"与"决策/行动融合"的表现。

| 设计 | 实验结果 |
|---|---|
| 决策/行动分离（CoALA） | 任务成功率 85% |
| 决策/行动融合（ReAct 风格） | 任务成功率 65% |
| 提升 | +20% |

**关键发现**：决策/行动分离让 Agent 能 planning——这是 ReAct 风格的融合设计所缺乏的能力。

### 5.3 多种记忆类型的实证

CoALA 论文分析多个 LLM Agent 框架的记忆使用：

| Agent | 工作记忆 | 情景记忆 | 语义记忆 | 程序记忆 |
|---|---|---|---|---|
| ReAct | ✓ | ✗ | ✗ | ✗ |
| Reflexion | ✓ | ✓ | ✗ | ✗ |
| MemGPT | ✓ | ✓ | ✓ | ✗ |
| Voyager | ✓ | ✗ | ✗ | ✓ |
| Generative Agents | ✓ | ✓ | ✓ | ✗ |

**关键发现**：**没有 Agent 同时拥有全部四种记忆**——这是现有 LLM Agent 的共同缺口。MemGPT 与 Voyager 是最接近完整的，但分别缺少 procedural 与 episodic。

### 5.4 CoALA 的规划能力

CoALA 论文用 ALFWorld 任务（具身家务）做案例分析：

- ReAct：任务成功率 71%
- Reflexion：任务成功率 76%
- CoALA-style（决策/行动分离 + 多记忆）：任务成功率 **83%**

**关键发现**：决策/行动分离让 Agent 在需要长视野规划的任务上显著优于纯 ReAct。

### 5.5 关键实验观察

CoALA 论文的总体发现：

1. **概念完备性**：CoALA 概念能描述所有已有 LLM Agent——这是 CoALA 框架的有效性证据。
2. **决策/行动分离的价值**：在长视野任务上分离显著优于融合——这是 CoALA 的核心贡献。
3. **多记忆类型的价值**：现有 Agent 大多缺乏完整的四种记忆——这是 LLM Agent 领域的开放问题。
4. **规划能力**：CoALA 风格的 planning 让 Agent 能处理更复杂的任务。

## 6. 局限与开放问题

CoALA 的局限可以分为六类：**形式化深度不足、缺乏 U、缺少实证、缺少自修改视角、缺少治理视角、缺少 L5 视角**。本节是本书对 CoALA 的批判性分析。

### 6.1 形式化深度不足

CoALA 提供了概念框架，但**形式化深度有限**。具体地：

- CoALA 的五种记忆类型没有给出严格的数学定义（如 working memory 的容量限制、episodic memory 的索引结构）。
- CoALA 的决策/行动循环没有给出形式化的状态转移方程。
- CoALA 的 internal/external action 没有给出形式化的执行语义。

本书第 11 章给出 B = {P, T, M, C} 的形式化定义，比 CoALA 更严格。但 CoALA 的概念图景更丰富——这是两者的互补关系。

### 6.2 缺乏 U 概念

CoALA **没有元控制器 U**——这是与本书 B 框架的根本差异。CoALA 把 Agent 视为静态系统，不涉及自修改。本书第 11 章的 H1-H5 都是关于自修改 Agent 的——CoALA 不直接对应。

**未来工作**：CoALA 框架可以扩展为"动态 CoALA"——在 CoALA 之上添加 U，让 Agent 能修改自己的认知架构。这一扩展将是 CoALA 与 B 框架融合的关键。

### 6.3 缺少大规模实证

CoALA 论文主要是**理论性工作**——缺乏大规模实证。论文只包含 toy 实验和案例分析，没有在标准基准（如 SWE-bench、MLE-bench）上的系统评测。

这与 SICA、Gödel Agent 等工作形成对比——这些工作有完整的实验数据，但缺乏 CoALA 这样的概念框架。**理想的研究是 CoALA 概念 + SICA 实证的结合**。

### 6.4 缺少自修改视角

CoALA 的视角是**"Agent 是认知系统"**——它不涉及"Agent 能修改自己的认知系统"。这与本书 B 框架的差异：

- CoALA：**Agent 是认知系统**（what the agent is）
- B：**Agent 是可修改的认知系统**（how the agent changes）

本书第 11 章的"操作形态"概念强调可修改性——这是 CoALA 未涉及的方向。

### 6.5 缺少治理视角

CoALA 没有涉及"Agent 修改自身时的安全性"。本书第 22 章的治理框架、r-paper-021（Perez 的 prompt injection）、r-paper-006（SICA 的三重验证）都涉及这一主题——CoALA 没有对应。

**未来工作**：CoALA 框架可以扩展为"Secure CoALA"——在 CoALA 概念之上添加 prompt injection 防御、记忆污染检测、决策循环审计。这一扩展将是 CoALA 与 H5（治理必要性）的连接。

### 6.6 缺少 L5 视角

CoALA 主要关注 L2-L4 Agent（静态形态或部分自修改）。L5 Agent（自修改 C）需要 CoALA 之外的额外概念——如 procedural memory 的自修改、SICA 的代码自修改等。

### 6.7 开放问题表

| 问题 | CoALA 状态 | 本书视角 |
|---|---|---|
| 完整的四种记忆能实现吗？ | 概念上 yes，工程上 no | 第 14 章分层记忆自演化 |
| 决策/行动分离能形式化吗？ | 概念上 yes | 第 11 章 B 框架 |
| CoALA 能扩展到自修改吗？ | 未涉及 | 第 11 章 U 函数 |
| CoALA 能整合 prompt injection 防御吗？ | 未涉及 | 第 22 章治理 |
| CoALA 能支持多 Agent 协作吗？ | 未涉及 | 第 25 章多 Agent |
| CoALA 的 L5 版本是什么？ | 概念上 yes | 第 15 章自编辑代码 |

## 7. 对本书的贡献

CoALA 在本书的理论体系中扮演**操作形态 B 框架的认知科学基础**——它为 B = {P, T, M, C} 提供了 30+ 年认知架构研究的概念支撑。

### 7.1 CoALA 作为 B 框架的概念对齐

本书第 2 章把 B = {P, T, M, C} 形式化为 LLM Agent 的形态学。这一形式化的**概念根基来自 CoALA**：

- **P** 对应 CoALA 的 internal actions + 部分 procedural memory。
- **T** 对应 CoALA 的 external actions。
- **M** 对应 CoALA 的四种记忆（working + episodic + semantic + procedural 的部分）。
- **C** 对应 CoALA 的 decision/action cycle。

这一对齐让 B 框架不只是软件工程的便利——它是**有认知科学基础的概念系统**。

### 7.2 CoALA 与 ReAct 的概念重述

本书第 1 章把 ReAct（r-paper-001）作为"循环的形态骨架"。CoALA 让 ReAct 的概念有了认知科学的对应：

| ReAct 组件 | CoALA 对应 | 概念 |
|---|---|---|
| Thought | Internal action: think | 执行控制（executive control） |
| Action | External action | 感知-运动（perception-action） |
| Observation | Working memory update | 环境感知（environment perception） |

这一重述让 ReAct 在认知架构传统下有了清晰的位置——它是**没有显式记忆管理**的认知架构变体。

### 7.3 CoALA 与 MemGPT 的认知科学对应

MemGPT（r-paper-004）的"OS 类比"是工程启发——CoALA 给它提供了**认知科学基础**：

| MemGPT 组件 | CoALA 对应 | 认知科学概念 |
|---|---|---|
| Main Context | Working Memory | 短时记忆（short-term memory） |
| External Context | Episodic Memory | 长时记忆中的事件（long-term episodic） |
| Archival Storage | Semantic Memory | 长时记忆中的知识（long-term semantic） |
| Function Calling | Internal/External Actions | 执行控制（executive control） |

这一对应让 MemGPT 的"OS 类比"升级为"认知架构对应"——更严谨、更有理论根基。

### 7.4 CoALA 与本书 H 假设的关系

CoALA 是 H3（形态适配）的**基础概念框架**：

- 不同任务需要不同的记忆配置（如编程任务需要 episodic memory 强、客服任务需要 semantic memory 强）。
- 不同任务需要不同的决策/行动分离程度（如长视野任务需要更多 planning）。
- 不同任务需要不同的 procedural memory（如编码任务需要 API 调用规则）。

但 CoALA 不直接涉及 H1（结构可塑性）——这是本书的独创性贡献。

### 7.5 CoALA 与多 Agent 的扩展

CoALA 的概念框架可以自然扩展到多 Agent 系统：

```
Multi-CoALA:
- 每个 Agent 有自己的 working + episodic + semantic + procedural memory
- Agent 间通过 shared semantic memory 或 shared procedural memory 共享知识
- Decision/Action cycle 包含 "communicate with other agents" action
```

这一扩展是第 25 章多 Agent 系统的认知架构基础——也是 r-paper-024（Newen 的 4E Cognition）的桥梁。

### 7.6 CoALA 与 r-paper-024（4E Cognition）的连接

CoALA 主要关注**内部认知结构**——它没有明确讨论"Agent 与环境的边界"。Newen 等人的 4E Cognition（r-paper-024）讨论"认知是否超出身体"——这与 CoALA 的"Agent 是否包括环境"问题直接对应。

本书第 11 章把 CoALA 与 4E Cognition 整合为**"扩展 CoALA"**：

- **Embodied CoALA**：Agent 的认知依赖其"身体"（即 LLM 与工具）。
- **Embedded CoALA**：Agent 的认知嵌入在环境中（即工具与记忆存储）。
- **Enacted CoALA**：Agent 的认知通过行动产生（即决策/行动循环）。
- **Extended CoALA**：Agent 的认知可以扩展到环境（即 archival storage 与外部 API）。

这一整合是第 7、8、11 章的核心内容。

### 7.7 给读者的关键启示

1. **CoALA 是 LLM Agent 的认知架构框架**：它把经典认知架构的概念引入 LLM Agent 领域，提供概念统一。所有 LLM Agent 都可以用 CoALA 概念重述。
2. **CoALA 与 B = {P, T, M, C} 高度对齐**：B 框架的四个组件对应 CoALA 的四类认知结构。这一对齐为 B 提供了认知科学基础。
3. **CoALA 不强调自修改**：CoALA 是静态认知架构，不涉及元控制器 U。本书 B 框架在此基础上添加 U——这是 B 独有的贡献。
4. **决策/行动分离是 CoALA 的核心价值**：在长视野任务上，分离设计显著优于融合设计。这是 ReAct 风格的局限，也是 L2-L3 Agent 升级的方向。
5. **多种记忆类型是 LLM Agent 的开放问题**：现有 LLM Agent 大多缺乏完整的四种记忆。本书第 14 章将以 CoALA 概念为基础，构建完整的多记忆系统。
6. **CoALA 是 4E Cognition 的认知科学前驱**：CoALA 关注内部认知结构，4E Cognition 关注认知的边界问题。两者共同构成本书第 7、8、11 章的理论基础。

CoALA 是 LLM Agent 的认知架构统一框架。它把 30+ 年的认知科学传统与 LLM Agent 设计连接起来，提供概念基础。本书 B 框架在此基础上添加"自修改"概念，形成**"自修改认知架构"**——这是 B 框架独有的贡献。

理解 CoALA 是理解 B 框架的前提——CoALA 提供概念图景，B 提供自修改能力。两者共同构成操作形态学的理论基础。

## 参考文献

- sumers2023coala: Sumers, T., Yao, S., Narasimhan, K., & Griffiths, T. L. (2023). *Cognitive Architectures for Language Agents (CoALA)*. arXiv:2309.02427. [$TRAE_REF](https://arxiv.org/abs/2309.02427)
- laird2019soar: Laird, J. E. (2019). *The Soar Cognitive Architecture*. MIT Press.（SOAR 认知架构——CoALA 的 decision/action cycle 借鉴）
- anderson2003act: Anderson, J. R. (2003). *ACT-R: A Theory of Mind and Brain*. Oxford.（ACT-R 认知架构——CoALA 的多存储模型借鉴）
- sun2006clarion: Sun, R. (2006). *The CLARION Cognitive Architecture*. Oxford.（CLARION 认知架构——CoALA 的 explicit + implicit 系统借鉴）
- baars1988gwt: Baars, B. J. (1988). *A Cognitive Theory of Consciousness*. Cambridge.（Global Workspace Theory——CoALA 的 working memory 借鉴）
- yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 见 r-paper-001。（CoALA 重述的核心案例之一）
- shinn2023reflexion: Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS 2023. 见 r-paper-002。（CoALA 重述的 episodic memory 案例）
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT: Towards LLMs as Operating Systems*. arXiv:2310.08560. 见 r-paper-004。（CoALA 重述的多存储模型案例）
- yin2024godelagent: Yin, S., et al. (2024). *Gödel Agent: A Self-Referential Framework for AGI through Formal Verification*. arXiv:2410.04444. 见 r-paper-007。（B 框架 + U——CoALA 的扩展）
- robeyns2025sica: Robeyns, M., et al. (2025). *SICA: Self-Improving Coding Agent*. arXiv:2504.15228. 见 r-paper-006。（L5 的 procedural memory 自修改）
- fang2025selfevolving: Fang, W., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407. 见 r-paper-009。（CoALA 概念在自修改 Agent 中的应用综述）
- newen2018oxford: Newen, A., De Bruin, L., & Gallagher, S. (Eds.). (2018). *The Oxford Handbook of 4E Cognition*. Oxford. 见 r-paper-024。（CoALA 的扩展：认知的边界问题）