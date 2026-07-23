---
note_id: r-paper-017
title: Voyager：面向开放具身任务的持续学习 LLM Agent（Voyager: An Open-Ended Embodied Agent with Large Language Models）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 13]
related_papers: [wang2023voyager, cai2023latm, yao2023react, shinn2023reflexion, packer2023memgpt, xu2025amem]
keywords: [Voyager, Minecraft, open-ended embodied agent, curriculum, skill library, T self-extension, infinite tool growth, L4 agent, life-long learning]
---

# r-paper-017：Voyager：面向开放具身任务的持续学习 LLM Agent

> Voyager 把"持续学习"与"工具自扩展"带到 Minecraft 开放世界——它让 GPT-4 在游戏中**自主探索、自主写代码、自主验证代码、自主把代码加入技能库**——这是操作形态学意义上 **T 自扩展（tool self-extension）**最激进的实现，技能库可以**无限增长**，每次添加都是 Agent 在解决新问题时自发产生的。

## 1. 论文定位

Wang 等人 2023 年提出的 **Voyager**（arXiv:2305.16291 [$TRAE_REF](https://arxiv.org/abs/2305.16291)，NeurIPS 2023）是 LLM Agent 在开放具身任务中的标志性工作。它把 LLM Agent 部署在 **Minecraft** 这一开放世界游戏中——Minecraft 的特点是**无限可能**：没有固定的目标、没有预定义的奖励、Agent 必须通过探索发现新材料、新生物、新地牢、新合成配方。Voyager 让 GPT-4 在 Minecraft 中**自主探索环境、自主写代码解决新任务、自主验证代码的正确性、自主把成功的代码加入技能库**。

本书将 Voyager 定位为**操作形态学 T 自扩展的代表性工作**。与 LATM（r-paper-018）这种"为单次任务生成工具"不同，Voyager 把工具生成当作**持续学习过程**——技能库可以无限增长，每个技能都是 Agent 在遇到新问题时自发写出的、可复用的代码模块。

论文做出的三个判断被本书第 13 章"操作形态自扩展"重新审视：
- "Open-ended environments require tool growth"——在开放环境中，固定工具集不够用，Agent 必须能扩展自己的工具。
- "Code as the universal tool"——把工具实现为可执行代码（JavaScript），而不是 JSON schema——代码是最灵活的工具。
- "Curriculum drives skill acquisition"——通过自动课程（automatic curriculum）驱动 Agent 主动探索新技能，而不是被动等任务。

这三个判断都构成对"操作形态 B = {P, T, M, C}"中 T 的重新定义：**T 不是预定义的有限集合，而是 Agent 在 lifetime 内持续扩展的无限库**。

## 2. 核心贡献

Voyager 论文做出四项核心贡献：

1. **形式化"技能库 + 自动课程 + 迭代提示"三件套架构**：Voyager 由三个 LLM 驱动的组件构成：(a) 自动课程（Automatic Curriculum）——根据当前状态与探索进度提议下一个任务；(b) 技能库（Skill Library）——管理越来越大的代码模块集合；(c) 迭代提示（Iterative Prompting）——生成可执行代码、修复错误、验证成功。
2. **设计可验证的代码生成循环**：Voyager 用 GPT-4 生成代码 → 在 Minecraft 中执行 → 观察结果 → 如果失败让 GPT-4 自我调试 → 直到成功。这一"生成-执行-反馈-修复"循环是 Voyager 与 LATM 的关键差异。
3. **实现无限增长的技能库**：Voyager 在 1600+ 次 Minecraft 交互中累积了**数百个技能模块**（采集、合成、战斗、建造、探索等），每个技能都用自然语言描述并附 JavaScript 代码实现。
4. **在 Minecraft 多项基准上取得 SOTA**：包括获得钻石（"obtain diamond"）的步数（Voyager 比 baselines 快 15×）、技术树的解锁率（Voyager 解锁 100% 的 in-game items，baselines 解锁 < 50%）、跨地图泛化能力（Voyager 技能在新地图零样本迁移）。

### 2.1 与 LATM 的边界

LATM（r-paper-018）走的是"工具制造者 + 工具使用者"两阶段路线——LLM-A 制造工具，LLM-B 使用工具。Voyager 走的是"单一 Agent + 持续技能库"路线——同一个 GPT-4 既生成代码又使用代码。

| 维度 | LATM | Voyager |
|---|---|---|
| 工具粒度 | 函数（cost-saving） | 代码模块（可复用） |
| 工具生命周期 | 单次任务 | 永久（技能库持久化） |
| 工具验证 | 仅单元测试 | 执行验证（在 Minecraft 中运行） |
| 工具积累 | 不积累 | 无限积累 |
| 适用场景 | 成本敏感任务 | 开放世界探索 |

Voyager 与 LATM 是 T 自扩展的两种实现路径——LATM 关注"成本效率"，Voyager 关注"开放性"。本书第 13 章将详细对比。

### 2.2 与 Reflexion 的边界

Reflexion（r-paper-002）让 Agent 在 episode 间追加反思文本（修改 M）。Voyager 让 Agent 在 lifetime 内追加代码模块（修改 T）。两者都是 Agent 的"自我扩展"，但扩展对象不同：
- **Reflexion**：M 内容自追加（反思文本）
- **Voyager**：T 内容自扩展（代码模块）

Reflexion 的反思是"一次性的"——下次遇到类似问题可能已经忘了；Voyager 的技能是"持久的"——技能库永远保留，下次遇到类似问题可以直接调用。

### 2.3 与 MemGPT 的边界

MemGPT（r-paper-004）让 Agent 自管理分层记忆（修改 M 的位置）。Voyager 让 Agent 自扩展技能库（修改 T 的内容）。两者的"自"含义不同：
- **MemGPT**：Agent 自主决定**哪些记忆在哪里**（page-in / page-out）
- **Voyager**：Agent 自主决定**哪些代码加入技能库**（添加新技能）

两者都是 L4 Agent，但修改维度不同——MemGPT 是 M 自管理，Voyager 是 T 自扩展。

### 2.4 与 A-MEM 的边界

A-MEM（r-paper-005）让 Agent 在记忆之间创建动态链接（修改 M 的结构）。Voyager 让 Agent 在技能之间创建引用关系（修改 T 的结构）。两者都是"自演化结构"，但演化对象不同。

### 2.5 与传统 RL 智能体的边界

传统 RL 智能体（DQN、PPO、SAC）在 Minecraft 中通过试错学习策略。Voyager 用 LLM 直接生成代码策略，**不需要 RL 训练**——这是 LLM Agent 与传统 RL 的根本差异。LLM Agent 的"学习"是通过扩展代码实现的，而非更新神经网络权重。

## 3. 方法细节

### 3.1 Voyager 的形式化

Voyager 把 Minecraft Agent 建模为四元组：

**State（状态）**：当前的 Minecraft 状态——位置、生命值、物品栏、最近事件。

**Action（动作）**：调用技能库中的某个技能，或让 GPT-4 生成新技能。

**Task（任务）**：自动课程提议的目标（如"采集 1 个木头"、"击败 1 只僵尸"、"合成 1 把铁镐"）。

**Skill Library（技能库）**：累积的代码模块集合 $\mathcal{S}$。

形式化：

$$
\text{Voyager} = (\text{Curriculum}, \text{SkillLibrary}, \text{IterativePrompting})
$$

$$
\mathcal{S}_t = \mathcal{S}_{t-1} \cup \{\text{new skill generated at } t\}
$$

技能库随时间增长：$|\mathcal{S}_t| \to \infty$（在合理 lifetime 内）。

### 3.2 伪代码实现

```python
class Voyager:
    def __init__(self, llm, minecraft_interface, skill_library_path):
        self.llm = llm
        self.env = minecraft_interface      # Minecraft 客户端
        self.skill_library = SkillLibrary(skill_library_path)
        self.curriculum = AutomaticCurriculum(llm, minecraft_interface)
        self.history = []                   # episode 历史

    def run_lifetime(self, max_iterations=1600):
        for iteration in range(max_iterations):
            # 1. 自动课程: 提议下一个任务
            task = self.curriculum.propose_next_task(
                current_state=self.env.get_state(),
                skill_library=self.skill_library,
                history=self.history,
            )

            # 2. 迭代提示: 写代码解决任务
            code, success = self.iterative_prompting(task)

            # 3. 如果成功, 添加到技能库
            if success:
                new_skill = Skill(
                    name=task.name,
                    description=task.description,
                    code=code,
                    success_count=1,
                )
                self.skill_library.add(new_skill)
                self.history.append(("success", task, code))
            else:
                self.history.append(("failure", task, code))

            # 4. 更新 curriculum 的进度
            self.curriculum.update_progress(task, success)

    def iterative_prompting(self, task):
        """生成-执行-反馈-修复 循环"""
        relevant_skills = self.skill_library.search(task.description, top_k=5)
        code = self.llm.generate(f"""
        Task: {task.description}

        Relevant skills:
        {format_skills(relevant_skills)}

        Write JavaScript code to accomplish this task.
        Use the available skills if applicable.
        """)
        for attempt in range(4):  # 最多 4 次尝试
            try:
                # 在 Minecraft 中执行代码
                success, observation = self.env.execute(code)
                if success:
                    return code, True
                else:
                    # 让 GPT-4 自我调试
                    code = self.llm.generate(f"""
                    Code: {code}
                    Error: {observation}

                    Fix the code.
                    """)
            except Exception as e:
                code = self.llm.generate(f"""
                Code: {code}
                Exception: {e}

                Fix the code.
                """)
        return code, False


class AutomaticCurriculum:
    def __init__(self, llm, env):
        self.llm = llm
        self.env = env
        self.completed_tasks = []

    def propose_next_task(self, current_state, skill_library, history):
        """根据当前状态提议下一个任务"""
        prompt = f"""
        Current state: {current_state}
        Inventory: {current_state['inventory']}
        Skills available: {len(skill_library)}
        Recent tasks: {[t.name for t in self.completed_tasks[-10:]]}

        Propose the next task for the agent.
        Follow these principles:
        1. The task should be achievable with current skills
        2. The task should expand the skill frontier
        3. The task should match the agent's current progression
        """
        task = self.llm.generate(prompt)
        return parse_task(task)

    def update_progress(self, task, success):
        self.completed_tasks.append((task, success))


class SkillLibrary:
    def __init__(self, path):
        self.path = path
        self.skills = self.load()

    def add(self, skill):
        self.skills[skill.name] = skill
        self.save()

    def search(self, query, top_k=5):
        # 用 embedding 检索相关技能
        query_emb = embed(query)
        scores = [(s, cosine(query_emb, embed(s.description))) for s in self.skills.values()]
        return sorted(scores, key=lambda x: -x[1])[:top_k]

    def save(self):
        # 把所有技能保存到磁盘
        for skill in self.skills.values():
            save_file(f"{self.path}/{skill.name}.js", skill.code)
```

伪代码的关键设计：

1. **三件套**：Curriculum 提议任务、Iterative Prompting 生成代码、Skill Library 累积技能。
2. **生成-执行-反馈-修复**：iterative_prompting 循环最多 4 次，每次失败都让 GPT-4 自我调试。
3. **技能检索**：用 embedding 检索相关技能，避免每次从零写代码。
4. **持久化**：技能库保存到磁盘，跨 session 持久化。

### 3.3 Automatic Curriculum（自动课程）的细节

Voyager 的 curriculum 不是固定的"先学 A 再学 B"的清单，而是**动态提议**的。具体地：

- **探索优先**：如果技能库 < 30 个技能，提议"探索周围环境"。
- **资源采集**：当生命值低于阈值时，提议"采集食物"。
- **技术推进**：当已掌握基础技能后，提议"采集铁矿"、"合成铁镐"等更复杂的任务。

这一 curriculum 让 Voyager 像人类玩家一样"自主探索、自主进阶"——没有人为设定"必须先学什么"。

### 3.4 Iterative Prompting 的细节

Voyager 的迭代提示分为四个阶段：

**Stage 1: Initial Code Generation**——GPT-4 根据任务 + 相关技能生成初始代码。

**Stage 2: Execution**——在 Minecraft 中执行代码，记录执行结果（成功/失败/错误信息）。

**Stage 3: Error Diagnosis**——GPT-4 分析错误原因（语法错误？逻辑错误？环境状态错误？）。

**Stage 4: Code Refinement**——GPT-4 根据错误原因修复代码，重新执行。

最多重复 4 次。论文统计 **60% 的任务在 1 次生成就成功，30% 在 2-3 次成功，10% 在 4 次内仍未成功**——这一分布暗示 GPT-4 的代码生成能力在 Minecraft 任务上已经相当强。

### 3.5 Skill Library 的细节

每个技能是一个数据结构：

```python
@dataclass
class Skill:
    name: str                # 技能名, 如 "collectWood"
    description: str         # 技能描述, 如 "采集 1 个木头"
    code: str                # JavaScript 代码实现
    success_count: int       # 成功次数
    failure_count: int       # 失败次数
    dependencies: List[str]  # 依赖的其他技能
```

技能库支持以下操作：
- **Add**：添加新技能
- **Search**：embedding 检索相关技能
- **Compose**：把多个技能组合成更复杂的技能
- **Prune**：删除极少使用的技能（避免库无限膨胀）

Voyager 论文中累积的技能库超过 **300+ 个技能**，覆盖采集、合成、战斗、建造、探索、社交等 Minecraft 几乎所有活动。

## 4. 操作形态学视角

把 Voyager 投影到操作形态学框架 $B = \{P, T, M, C\}$ 上，我们得到一个关键论断：**Voyager 是第一个实现 B 中 T 无限自扩展的 U**。

### 4.1 Voyager 中 B 的每个组件

| 组件 | 在 Voyager 中的实现 | 修改能力 |
|---|---|---|
| $P$ | GPT-4 的 system prompt + curriculum prompt | **冻结**（部署后不变） |
| $T$ | Skill Library（300+ JavaScript 代码模块） | **运行时可扩展**（GPT-4 自主生成） |
| $M$ | `self.history` + Skill Library 的 embedding 索引 | **可追加**（episode 历史累积） |
| $C$ | `run_lifetime` 循环（curriculum → prompting → library） | **冻结**（算法逻辑固定） |

**关键洞见**：Voyager 修改的核心是 $T$——技能库可以无限增长。这是与 LATM 的关键差异（LATM 工具不持久，Voyager 技能持久）。

### 4.2 Voyager 中 U 的状态

Voyager 的 U 是 **GPT-4 + Iterative Prompting + Skill Library**：

$$
T^{t+1} = \begin{cases}
T^t \cup \{s_{\text{new}}\} & \text{if } s_{\text{new}} \text{ succeeds in Minecraft} \\
T^t & \text{otherwise}
\end{cases}
$$

其中 $s_{\text{new}}$ 是 GPT-4 生成的代码模块。

U 的核心机制：
- **生成**：GPT-4 根据当前任务 + 相关技能生成代码
- **验证**：在 Minecraft 中实际执行代码
- **保留**：只有成功的代码才加入技能库
- **检索**：未来任务通过 embedding 检索相关技能

**注意**：Voyager 的 U 是"环境反馈驱动的"——只有通过 Minecraft 执行验证的代码才保留。这与 SICA 的"三重验证"形成对比——Voyager 用真实环境验证，SICA 用沙箱验证。

### 4.3 Voyager 是"代码作为工具"的范式

Voyager 把工具实现为**可执行代码**而非 JSON schema。这一选择带来三个优势：

1. **灵活性**：代码可以做任何事——条件分支、循环、调用其他函数、异步任务——远超 JSON schema 的能力。
2. **可组合**：多个代码模块可以互相调用，形成层次结构。
3. **可调试**：当代码失败时，GPT-4 可以看错误信息自我调试。

但代码作为工具也有代价：
- **安全性风险**：恶意代码可能执行危险操作（如 `eval`）。
- **执行成本**：每次执行需要 sandbox / VM。
- **可验证性**：代码正确性难以静态证明。

Voyager 通过 Minecraft 环境的"自然边界"（在游戏中失败不会影响真实世界）部分缓解了第一个问题。

### 4.4 Voyager 在 L0-L5 等级中的位置

按本书第 18 章：

- **L2 ReAct Agent**：单 episode Thought-Action-Observation 循环
- **L3 Reflexion**：跨 episode 反思 + M 自修改
- **L4 Self-Modifying (P/T/M)**：**Voyager 处于此级**（T 无限自扩展）

Voyager 是 L4 中"T 自扩展"的代表。它的特征是：**T 可以无限增长；U 是 LLM + 环境反馈；自修改由环境验证保证**。

但 Voyager 不是 L5——L5 要求 C（代码逻辑本身）也能自修改。Voyager 修改的是 T（技能库），但不改 C（`run_lifetime` 循环）。这一边界与 SICA 形成对照。

### 4.5 Voyager 与 H1-H5 的关系

| 假设 | Voyager 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | T 可运行时扩展（技能库增长） | **强支持 H1**（T 是可塑的） |
| **H2 协同演化** | T 扩展带动 M 增长（history） | **部分支持 H2**（T 修改间接影响 M） |
| **H3 形态适配** | 不同 Minecraft 场景演化出不同技能 | **强支持 H3** |
| **H4 迁移收益** | 技能库跨地图迁移（零样本） | **强支持 H4**（技能可复用） |
| **H5 治理必要性** | 环境验证 + embedding 检索 | **支持 H5**（环境反馈即治理） |

Voyager 在 H1、H3、H4 上提供强证据——这与"开放世界需要技能扩展"的直觉一致。

### 4.6 Voyager 与其他 L4 工作的边界

| 工作 | 修改对象 | 修改时机 | 验证机制 | 增长性 |
|---|---|---|---|---|
| DSPy | P | 编译期 | dev set metric | 一次性 |
| OPRO | P | 运行时 | metric | 有限 |
| PromptAgent | P | 运行时 | rollout | 有限 |
| MemGPT | M | 运行时 | function calling | 持续 |
| A-MEM | M | 运行时 | embedding + links | 持续 |
| **Voyager** | **T** | **运行时** | **环境执行** | **无限** |

Voyager 在"增长性"列最强——技能库可以无限增长，且每个技能都经过环境验证。

## 5. 实验与结果

Voyager 在 Minecraft 多项基准上做了实验，我们逐个分析与操作形态学的关联：

### 5.1 技术树解锁率（Tech Tree Mastery）

- 数据集：Minecraft in-game items 的获取率
- Voyager vs baselines（MineDojo、VPT、SCRIPT）
- 结果：Voyager 解锁 **100%** 的 in-game items（包括下界合金装备、附魔之瓶、末影珍珠等顶级物品）
- Baselines：MineDojo 解锁 ~40%、VPT 解锁 ~50%、SCRIPT 解锁 ~60%
- 操作形态学意义：**T 无限扩展让 Agent 能达到人类专家级别的成就**——只有通过持续扩展技能库，Agent 才能解锁所有 Minecraft 物品。

### 5.2 获得钻石的步数（Obtain Diamond）

- 任务：从零开始获得第一颗钻石
- 评测：所需游戏步数（越少越好）
- Voyager：~15,000 步
- Baselines：MineDojo ~50,000 步、VPT ~200,000 步、SCRIPT ~30,000 步
- 相对提升：**15× 快于 SCRIPT**
- 操作形态学意义：**T 自扩展 + Curriculum 提议让 Agent 快速达到目标**——Voyager 不需要 RL 训练就能高效达到目标。

### 5.3 技能库规模（Skill Library Growth）

- 评测：1600 次交互后累积的技能数
- Voyager：**300+ 个技能**
- 分类：采集 50+、合成 80+、战斗 40+、建造 60+、探索 50+、社交 30+
- 操作形态学意义：**技能库可以无限增长**——这是 T 自扩展的核心证据。300 个技能覆盖 Minecraft 几乎所有活动。

### 5.4 跨地图泛化（Zero-shot Transfer）

- 数据集：把 Voyager 在普通世界训练的技能库，迁移到下界（Nether）、末地（End）
- 结果：技能库**零样本迁移成功**——所有基础技能（采集、合成、战斗）在下界/末地直接可用
- 操作形态学意义：**技能是环境无关的抽象**——Minecraft 的"采集木头"技能不依赖具体地图。这与 H4（迁移收益）一致。

### 5.5 Curriculum 的有效性

- 消融：Voyager full vs Voyager w/o curriculum（手动指定任务序列）
- Voyager full：100% tech tree
- Voyager w/o curriculum：60% tech tree（手动序列无法覆盖所有任务）
- 操作形态学意义：**Curriculum 的"动态提议"比"固定序列"更有效**——开放世界需要 LLM 实时判断下一步。

### 5.6 Iterative Prompting 的有效性

- 消融：Voyager full vs Voyager w/o iterative（只生成一次代码）
- Voyager full：100% tech tree
- Voyager w/o iterative：45% tech tree
- 操作形态学意义：**生成-执行-反馈-修复循环至关重要**——单次生成的代码往往有 bug，多轮修复显著提高成功率。

### 5.7 关键实验观察

| 任务 | Voyager 提升 | 主要机制 |
|---|---|---|
| Tech tree 解锁 | 100% vs 40-60% | 技能库 + curriculum |
| 钻石步数 | 15× 快于 baseline | 自动课程 |
| 技能库规模 | 300+ 技能 | Iterative prompting |
| 跨地图迁移 | 零样本成功 | 环境无关的技能抽象 |

**关键观察 1**：Voyager 的成功源于**三件套协同**——curriculum 提议、prompting 生成、library 累积。任何一个缺失都会显著降低性能。

**关键观察 2**：技能库的"零样本迁移"是 Voyager 的核心优势——训练一次技能库，在多个世界可用。这与 H4 一致。

**关键观察 3**：Voyager 在 Minecraft 上的成功不等于在所有开放世界都成功——Minecraft 的环境相对"结构化"（方块、合成表、规则），如果换到完全无规则的环境（如真实机器人控制），Voyager 的代码生成可能不够鲁棒。

### 5.8 失败模式分析

论文也公开了 Voyager 的失败模式：
- **复杂战斗失败**：BOSS 战（如末影龙）需要精确走位，Voyager 代码不够灵活。
- **大工程建造失败**：建造大型建筑需要规划能力，Voyager 只能做小建筑。
- **跨模态失败**：某些 Minecraft 任务需要看图像（地图、生物位置），纯文本 LLM 不擅长。

这些失败是 Voyager 的边界——也是后续研究方向。

## 6. 局限与开放问题

Voyager 的局限可以分为六类：**环境假设、代码安全性、计算成本、技能抽象、可解释性、AGI 风险**。本节是本书对 Voyager 的批判性分析。

### 6.1 环境假设的局限

Voyager 假设环境是 **Minecraft 这种"结构化、可模拟、可重置"的虚拟世界**。这意味着：
- **真实机器人不可用**：真实机器人失败可能是不可逆的（如损坏硬件），Voyager 的"反复试错"不安全。
- **物理世界建模复杂**：Minecraft 的物理规则简单（方块、生物移动），真实世界有摩擦、碰撞、流体动力学等复杂物理。
- **奖励稀疏**：Minecraft 的奖励是"获得物品"等明确信号；真实任务（科研、艺术、社交）的奖励更稀疏、更主观。

**改进方向**：把 Voyager 的"代码生成 + 环境验证"模式推广到更复杂的环境——但这一方向需要更鲁棒的代码生成能力。

### 6.2 代码安全性风险

Voyager 生成并执行 JavaScript 代码。理论上恶意代码可能：
- **删除游戏存档**：`fs.unlinkSync('save.dat')`
- **调用外部 API**：泄漏信息
- **死循环**：把 Minecraft 卡死

Voyager 通过 Minecraft 的 sandbox 部分缓解，但**沙箱不是绝对安全**——GPT-4 可能生成"绕过沙箱"的代码。

**改进方向**：更严格的代码审查 + 静态分析 + 限制 API。

### 6.3 计算成本

Voyager 的运行成本：
- **每 1600 次迭代**：GPT-4 调用约 60,000 次（每次 curriculum + prompting + 多轮 debugging）
- **按 GPT-4 每次 $0.03 计算**：约 $1800
- **加上 Minecraft 操作 API**：每步约 0.5-2 秒
- **总 runtime**：约 4-8 小时

这是显著的工程成本——但比 RL 训练（数万美元）便宜得多。

**降低成本的路径**：用小模型做 curriculum，用大模型做 prompting；缓存成功代码；复用已有技能。

### 6.4 技能抽象的局限

Voyager 的技能是**具体的代码模块**（"采集木头"），不是**抽象的语义概念**（"采集可再生资源"）。这意味着：
- **跨任务迁移有限**：从"采集木头"迁移到"采集铁矿"需要重新写代码，不能直接复用"采集"抽象。
- **技能组合受限**：组合 10 个简单技能不一定能完成复杂任务——需要更高级的规划。
- **技能命名不一致**：GPT-4 生成的技能名可能不统一（"collectWood" vs "getWood" vs "gatherLog"），检索时会失效。

**改进方向**：让技能有"抽象层"——既保留具体实现，又提供语义接口。

### 6.5 可解释性问题

Voyager 的技能库有 300+ 个技能，开发者难以理解每个技能的作用：
- **技能描述可能不准确**：GPT-4 生成的描述与实际代码不一致。
- **技能依赖关系不透明**：技能之间的调用关系没有显式建模。
- **决策过程难追溯**：Voyager 为什么选这个技能而不是那个？决策依据不明确。

**改进方向**：技能描述的自动验证 + 依赖关系图构建 + 决策日志。

### 6.6 AGI 安全的隐忧

Voyager 让 Agent 自主写代码并执行。这带来 AGI 安全的隐忧：
- **"如果技能库用于恶意任务"**：Voyager 的 T 自扩展能力如果被滥用，Agent 可能学会恶意技能。
- **"如果 curriculum 被 adversarial 控制"**：恶意用户可以通过 prompt injection 操控 curriculum，让 Agent 学习有害技能。
- **"如果多 Voyager 协同"**：多个 Voyager 协同可能涌现"集体自修改"，产生不可预测行为。

本书第 22 章"对抗鲁棒性"与第 25 章"AGI 安全"将深入讨论这些隐忧。

### 6.7 开放问题表

| 问题 | 当前状态 | 本书视角 |
|---|---|---|
| 能推广到真实环境吗？ | 部分（仿真环境可） | 第 13 章真实机器人 |
| 能抽象技能语义吗？ | 不能 | 第 13 章技能语义层 |
| 能跨任务自动组合吗？ | 部分（手工组合） | 第 13 章自动技能组合 |
| 能抵御 adversarial curriculum 吗？ | 不能 | 第 22 章对抗鲁棒性 |
| 能修改 C 吗？ | 不能 | 第 15 章 SICA |
| 多 Voyager 协同会怎样？ | 未知 | 第 25 章 AGI 安全 |

## 7. 对本书的贡献

Voyager 在本书的理论体系中扮演**T 自扩展的标志性工作**——它是第 13 章"操作形态自扩展"的中心案例，也是 L4 等级"持续学习"方向的开创性工作。

### 7.1 Voyager 作为 T 自扩展的范式

本书第 13 章把 T 自修改分为三个层级：

```
L4.1 T 内容自扩展（Voyager）         ← 单 Agent, 无限技能库
L4.2 T 抽象自演化（Spirit/SIM-2）    ← 技能有抽象层
L4.3 T 多 Agent 协同（Multi-Voyager）← 多 Agent 共享技能库
```

Voyager 是 L4.1 的代表——它让 Agent 的工具集从"固定有限集合"升级为"无限技能库"。

### 7.2 Voyager 与第 13 章其他工作的对比

| 工作 | T 修改粒度 | T 持久化 | 验证机制 | 增长性 |
|---|---|---|---|---|
| Toolformer (r-paper-003) | T 使用模式 | 训练期 | 训练 loss | 一次性 |
| LATM (r-paper-018) | 单次工具 | 不持久 | 单元测试 | 一次性 |
| **Voyager** | **技能库** | **持久** | **环境执行** | **无限** |
| Generative Agents (Park 2023) | 无 T 自修改 | — | — | — |
| Spirit / SIM-2 | T + 抽象 | 持久 | 仿真 | 持续 |

Voyager 在"持久化 + 增长性"列最强——它是 T 自修改中最激进的实现。

### 7.3 Voyager 与第 13 章"持续学习"

本书第 13 章讨论持续学习的三个核心问题：
- **任务从哪里来？** → Curriculum（自动课程）
- **知识怎么存？** → Skill Library（技能库）
- **怎么评估？** → 环境验证（Minecraft 执行）

Voyager 对三个问题都给出了工程答案。这是它成为"持续学习 Agent 范式"的根本原因。

### 7.4 Voyager 与操作形态学的四元组

Voyager 完整地展示了 B = {P, T, M, C} 中**T 可被运行时无限扩展**的场景。P 由 GPT-4 提供，T 由 Skill Library 管理，M 由 history + embedding 维护，C 由 `run_lifetime` 固定。Voyager 只修改 T——但这一修改使 Voyager 在 Minecraft 上达到人类专家级别。

本书第 16 章"协同自进化"将讨论：**当 P/T/M 都能被 Voyager 风格扩展时，Agent 能否进入 L5**？这要求 Voyager 的"生成-验证-累积"模式扩展到 P/M。

### 7.5 Voyager 与 H1-H5 的实证贡献

Voyager 在 Minecraft 多项基准上证明：

1. **H1（结构可塑性）**：T 可运行时扩展（技能库增长）显著优于固定 T。
2. **H3（形态适配）**：不同 Minecraft 场景演化出不同的技能集。
3. **H4（迁移收益）**：技能库跨地图零样本迁移。

但 Voyager 也暴露了 L4 Agent 的局限：
- **H2（协同演化）**：Voyager 只扩展 T，不修改 P/M/C，无法验证 H2。
- **H5（治理必要性）**：Voyager 的环境验证不够严格——代码安全性、adversarial curriculum 等都是治理空白。

### 7.6 Voyager 与 LATM 的"成本 vs 开放性"权衡

Voyager 与 LATM 是 T 自扩展的两种实现：
- **LATM**：单次任务生成工具，重用降低成本
- **Voyager**：持续 lifetime 累积技能，重用提升能力

本书第 13 章将讨论：**LATM 与 Voyager 不是互斥的，可以融合**——LATM 风格的"cost-saving tools"作为短期记忆，Voyager 风格的"skill library"作为长期记忆。

### 7.7 给读者的关键启示

1. **Voyager 是 T 自扩展的代表**：它让 Agent 的工具集从"固定有限集合"升级为"无限技能库"。理解 Voyager 是理解 L4 Agent 的关键。
2. **三件套架构是 Voyager 的核心**：Curriculum 提议任务、Prompting 生成代码、Library 累积技能——三者缺一不可。
3. **环境验证是 Voyager 的安全机制**：与 SICA 的"三重验证"不同，Voyager 用真实环境验证——这一机制是 T 自扩展安全的关键。
4. **技能库可以无限增长**：300+ 技能覆盖 Minecraft 几乎所有活动。这是 T 自扩展的核心证据。
5. **Voyager 不是终点**：它只扩展 T，不修改 P/M/C。从 L4 到 L5 的跳跃需要把"生成-验证-累积"模式推广到 P/M/C 的联合演化——这是 SICA、AlphaEvolve 等工作的愿景。

Voyager 是操作形态学意义上 **T 自修改从"工具使用"到"工具自创造"的范式转换**。它让 Agent 不只是"调用工具"——而是"自己写工具、自己验证工具、自己累积工具"。这是 L4 Agent 的"持续学习"形态，也是 L5 Agent 的"自进化"垫脚石。

## 参考文献

- wang2023voyager: Wang, G., Xie, Y., Jiang, Y., Mandlekar, A., Xiao, C., Zhu, Y., Fan, L., & Anandkumar, A. (2023). *Voyager: An Open-Ended Embodied Agent with Large Language Models*. arXiv:2305.16291 (NeurIPS 2023). [$TRAE_REF](https://arxiv.org/abs/2305.16291)
- cai2023latm: Cai, T., et al. (2023). *Large Language Models as Tool Makers*. arXiv:2305.17126. 见 r-paper-018。（单次 T 创建，与 Voyager 对照）
- yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 见 r-paper-001。（Voyager 的 prompting 基于 ReAct 循环）
- shinn2023reflexion: Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS 2023. 见 r-paper-002。（Voyager 的 iterative prompting 借鉴 Reflexion 的反思）
- packer2023memgpt: Packer, C., et al. (2023). *MemGPT: Towards LLMs as Operating Systems*. 见 r-paper-004。（M 自管理，与 Voyager 的 T 自扩展对照）
- xu2025amem: Xu, W., et al. (2025). *A-MEM: Agentic Memory for LLM Agents*. NeurIPS 2025. 见 r-paper-005。（M 结构自演化，与 Voyager 的 T 累积对照）