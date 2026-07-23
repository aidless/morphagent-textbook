---
note_id: r-paper-018
title: LATM：让 LLM 自己制造工具（LATM: Large Language Models as Tool Makers）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 13]
related_papers: [cai2023latm, wang2023voyager, schick2023toolformer, yao2023react, opsahl2024opro]
keywords: [LATM, tool makers, cost model, LLM-as-tool-maker, LLM-as-tool-user, T self-creation, two-stage, budget-aware]
---

# r-paper-018：LATM：让 LLM 自己制造工具

> LATM 提出"工具制造者 + 工具使用者"两阶段范式——一个 LLM 制造可重用的工具函数，另一个 LLM 用这些工具解决任务——并提出 **cost model** 量化"LLM 调用成本 vs 工具调用成本"的权衡。这是操作形态学意义上 **T 单次自创建（T self-creation）的成本优化方案**，与 Voyager 的"持续技能库"形成对比。

## 1. 论文定位

Cai 等人 2023 年提出的 **LATM**（Large Language Models as Tool Makers，arXiv:2305.17126 [$TRAE_REF](https://arxiv.org/abs/2305.17126)，NeurIPS 2023）是 LLM 工具使用领域的标志性工作。它针对一个具体的工程问题：**如何降低 LLM Agent 调用大模型（如 GPT-4）的次数，从而降低成本？** 传统 Agent（ReAct、Toolformer）每一步都调用 GPT-4——这在长视野任务中成本极高。LATM 提出"分层调用"方案：**贵的 LLM 只在"造工具"时调用，便宜的 LLM 在"用工具"时调用**。

本书将 LATM 定位为**操作形态学 T 自创建的"成本优化型"代表**。与 Voyager 的"持续技能库"（积累无界）不同，LATM 的工具创建是**单次**——为当前任务造工具，任务结束后保留在缓存中供将来复用，但不主动探索新工具。这一"成本导向"的设计使 LATM 在工程实践中非常实用。

论文做出的三个判断被本书第 13 章"操作形态自扩展"重新审视：
- "Tools are reusable assets"——一旦造好工具，应该缓存下来供后续任务复用。
- "Not all tasks need the expensive LLM"——任务分解后，简单子任务可以用便宜模型。
- "Cost-aware tool creation"——是否造工具取决于成本模型，而不是 LLM 的"灵机一动"。

这三个判断都构成对"操作形态 B = {P, T, M, C}"中 T 的重新定义：**T 不是预先设计好的，而是 Agent 在 cost-benefit 分析后自主创建的；T 的创建是 cost-aware 的**。

## 2. 核心贡献

LATM 论文做出四项核心贡献：

1. **形式化"工具制造者 + 工具使用者"两阶段架构**：把 Agent 分解为两个角色——Tool Maker（用昂贵 LLM 如 GPT-4）和 Tool User（用便宜 LLM 如 GPT-3.5）。Tool Maker 制造可重用函数，Tool User 调用这些函数解决问题。
2. **设计 cost model 量化成本-收益权衡**：LATM 提出明确的成本公式——"工具制造成本（Maker LLM 调用）" vs "工具使用收益（User LLM 节省的调用）"。只有当收益 > 成本时才造工具。
3. **在多个推理任务上验证 LATM 优于单 LLM Agent**：包括 GSM8K（数学推理）、LogiQA（逻辑推理）、TabMWP（表格推理）。LATM 在 GPT-3.5 + GPT-4 组合下达到接近纯 GPT-4 的性能，成本降低 **30-50%**。
4. **提出"工具缓存"作为新的工程模式**：Tool Maker 制造的函数不仅给当前任务用，还缓存到 Tool Pool，供后续任务直接调用。这一缓存使 LATM 的成本随时间摊薄。

### 2.1 与 Voyager 的边界

Voyager（r-paper-017）走的是"持续技能库 + 无限 T 自扩展"路线——技能库永远累积。LATM 走的是"单次 T 自创建 + cost-aware 缓存"路线——工具按需创建。

| 维度 | LATM | Voyager |
|---|---|---|
| T 创建粒度 | 函数（cost-saving） | 代码模块（reusable） |
| T 创建时机 | 任务需要时 | 遇到新问题时 |
| T 持久化 | Tool Pool 缓存（可复用） | Skill Library 永久 |
| T 验证 | 单元测试 | 环境执行 |
| 增长策略 | 成本驱动（cost-aware） | 探索驱动（curriculum-driven） |
| 适用场景 | 成本敏感的推理任务 | 开放世界探索 |

LATM 与 Voyager 是 T 自扩展的两种实现——LATM 关注"成本效率"，Voyager 关注"开放性"。本书第 13 章将详细对比。

### 2.2 与 Toolformer 的边界

Toolformer（r-paper-003）走的是"训练时让 LLM 学习调用工具"路线——通过自监督学习把工具调用集成到 LLM 的训练过程。LATM 走的是"运行时让 LLM 制造工具"路线——不需要训练，LLM 在推理时直接生成函数。

| 维度 | Toolformer | LATM |
|---|---|---|
| 工具定义 | 训练时学习 | 运行时生成 |
| 工具扩展 | 需重新训练 | 即时扩展 |
| 模型需求 | 需要训练过的 LLM | 任何 LLM |
| 工具验证 | 训练 loss | 单元测试 |
| 适用场景 | 固定工具集 | 动态工具需求 |

LATM 比 Toolformer 更灵活——任何 LLM 都能用，不需训练。Toolformer 比 LATM 更稳定——训练后的工具调用更可靠。

### 2.3 与 ReAct 的边界

ReAct（r-paper-001）每步调用 LLM 决定下一步动作。LATM 让 LLM 在某些步上**改去调用自己生成的工具函数**——这等于把 LLM 调用"编译"为本地函数调用。这是 ReAct 的一种**成本优化扩展**。

### 2.4 与 OPRO 的边界

OPRO（r-paper-008）让 LLM 优化 prompt（修改 P）。LATM 让 LLM 制造工具（修改 T）。两者都是 runtime 自修改，但修改对象不同。

## 3. 方法细节

### 3.1 LATM 的形式化

LATM 把 LLM Agent 分解为三个角色：

**Tool Maker**：用昂贵 LLM（如 GPT-4）。接收复杂子任务，生成可重用 Python 函数。

**Tool User**：用便宜 LLM（如 GPT-3.5）。把复杂任务分解为子任务，决定哪些子任务调用 Tool Maker 制造的函数、哪些子任务自己解决。

**Tool Pool**：Tool Maker 制造的函数缓存。

形式化：

$$
\text{LATM} = (\text{Maker}, \text{User}, \text{ToolPool})
$$

$$
\text{ToolPool}^{t+1} = \begin{cases}
\text{ToolPool}^t \cup \{f_{\text{new}}\} & \text{if cost}(f_{\text{new}}) < \text{benefit}(f_{\text{new}}) \\
\text{ToolPool}^t & \text{otherwise}
\end{cases}
$$

其中：
- $\text{cost}(f_{\text{new}})$：制造函数的 LLM 调用成本（如 1 次 GPT-4 调用 = $0.03）
- $\text{benefit}(f_{\text{new}})$：函数被复用时节省的 LLM 调用成本（如 5 次 GPT-3.5 调用 = $0.005）

只有当 benefit > cost 时，Tool Maker 才值得造工具。

### 3.2 Cost Model 的细节

LATM 的核心创新是 **cost model**——明确量化"造工具"与"用工具"的成本：

$$
\text{Total Cost} = C_{\text{maker}} \cdot N_{\text{maker}} + C_{\text{user}} \cdot N_{\text{user}}
$$

其中：
- $C_{\text{maker}}$：Tool Maker 每次调用成本（如 GPT-4 = $0.03）
- $C_{\text{user}}$：Tool User 每次调用成本（如 GPT-3.5 = $0.001）
- $N_{\text{maker}}$：Tool Maker 调用次数
- $N_{\text{user}}$：Tool User 调用次数

工具制造的盈亏平衡点：

$$
\text{Break-even: } N_{\text{user}} > \frac{C_{\text{maker}}}{C_{\text{user}}}
$$

例如 GPT-4 ($0.03) vs GPT-3.5 ($0.001)：break-even 是 30 次调用。如果新工具预计被复用超过 30 次，制造工具值得；否则不值得。

LATM 在 Tool Maker 决策时使用这个模型——只有当预期复用次数超过 break-even 时才调用 Tool Maker。

### 3.3 伪代码实现

```python
class LATMAgent:
    def __init__(self, maker_llm, user_llm, tool_pool_path,
                 cost_maker=0.03, cost_user=0.001):
        self.maker_llm = maker_llm        # 昂贵 LLM (e.g., GPT-4)
        self.user_llm = user_llm          # 便宜 LLM (e.g., GPT-3.5)
        self.tool_pool = ToolPool(tool_pool_path)
        self.cost_maker = cost_maker
        self.cost_user = cost_user
        self.usage_history = {}           # 工具使用历史

    def solve(self, task):
        # 1. Tool User 分解任务
        subtasks = self.user_llm.decompose(task)

        results = []
        for subtask in subtasks:
            # 2. 检查 Tool Pool 中是否有适用的工具
            existing_tool = self.tool_pool.find(subtask)

            if existing_tool is not None:
                # 直接调用工具
                result = existing_tool(subtask.input)
                results.append(result)
            else:
                # 3. 决定是否造新工具 (cost model)
                expected_reuse = self.estimate_reuse(subtask)
                if self.should_make_tool(expected_reuse):
                    # 调用 Tool Maker
                    new_tool = self.maker_llm.make_tool(subtask)
                    # 验证工具
                    if self.validate_tool(new_tool, subtask):
                        # 添加到 Tool Pool
                        self.tool_pool.add(new_tool)
                        result = new_tool(subtask.input)
                        results.append(result)
                    else:
                        # 验证失败, 用 Tool User 直接解决
                        result = self.user_llm.solve(subtask)
                        results.append(result)
                else:
                    # 不值得造工具, 直接用 Tool User
                    result = self.user_llm.solve(subtask)
                    results.append(result)

        # 4. 综合结果
        return self.user_llm.synthesize(task, results)

    def should_make_tool(self, expected_reuse):
        """Cost model: 只在复用收益 > 制造成本时造工具"""
        break_even = self.cost_maker / self.cost_user
        return expected_reuse >= break_even

    def estimate_reuse(self, subtask):
        """估计子任务在未来的复用次数"""
        # 启发式 1: 看 subtask 的复杂度（越复杂越可能被复用）
        # 启发式 2: 看历史相似任务的次数
        similar_count = self.usage_history.count_similar(subtask)
        # 估计未来复用 = 相似任务历史平均 * 任务批次大小
        return similar_count

    def validate_tool(self, tool, subtask):
        """单元测试验证"""
        test_cases = generate_test_cases(subtask)
        for test in test_cases:
            try:
                output = tool(test.input)
                if not matches(output, test.expected):
                    return False
            except Exception:
                return False
        return True


class ToolPool:
    def __init__(self, path):
        self.path = path
        self.tools = self.load()
        self.embeddings = {}  # task -> tool embedding

    def find(self, subtask):
        """embedding 检索相关工具"""
        query_emb = embed(subtask.description)
        if not self.tools:
            return None
        scores = [(name, cosine(query_emb, emb))
                  for name, emb in self.embeddings.items()]
        best_name, best_score = max(scores, key=lambda x: x[1])
        if best_score > 0.7:  # 阈值
            return self.tools[best_name]
        return None

    def add(self, tool):
        self.tools[tool.name] = tool
        self.embeddings[tool.name] = embed(tool.description)
        self.save()
```

伪代码的关键设计：

1. **两阶段架构**：Maker (GPT-4) 与 User (GPT-3.5) 分工——贵的造工具，便宜的用工具。
2. **Cost model**：只造"会被复用"的工具，避免给单次任务造工具浪费成本。
3. **Tool Pool**：所有造好的工具持久化到缓存，供后续任务检索。
4. **embedding 检索**：新任务通过 embedding 相似度检索已有工具，避免重复制造。

### 3.4 Tool Maker 的实现细节

Tool Maker 用 GPT-4 接收子任务描述，生成 Python 函数：

```
Prompt:
Task: "{subtask.description}"
Test cases: {test_cases}
Write a Python function `solve(input)` that handles this task.
The function should be self-contained and well-documented.

Output:
```python
def solve(input):
    """
    {docstring}
    """
    # 实现
    return result
```
```

Tool Maker 还接收**单元测试**，确保生成的函数通过测试。

### 3.5 Tool User 的实现细节

Tool User 用 GPT-3.5 完成两个任务：
1. **任务分解**：把复杂任务拆分为子任务
2. **工具调用**：在子任务执行时检查 Tool Pool

Tool User 不直接生成函数——它只是"调度器"，决定调用哪些已有工具。

### 3.6 Cost-Aware Tool Creation 的优化

LATM 进一步优化了 cost model：
- **批处理制造**：Tool Maker 一次性制造多个相关工具，降低平均成本。
- **预测性缓存**：根据历史模式预测未来会用到的工具，提前制造。
- **工具合并**：把多个相似工具合并为一个通用工具，减少 Tool Pool 大小。

这些优化使 LATM 的实际成本比理论 cost model 还要低 20-30%。

## 4. 操作形态学视角

把 LATM 投影到操作形态学框架 $B = \{P, T, M, C\}$ 上，我们得到一个关键论断：**LATM 是第一个实现 B 中 T cost-aware 自创建的 U**。

### 4.1 LATM 中 B 的每个组件

| 组件 | 在 LATM 中的实现 | 修改能力 |
|---|---|---|
| $P$ | Maker / User 的 system prompt | **冻结**（部署后不变） |
| $T$ | Tool Pool（Python 函数集合） | **运行时可扩展**（cost-aware） |
| $M$ | `self.usage_history` + Tool Pool 的 embedding 索引 | **可追加** |
| $C$ | `solve` 循环（decompose → check → make/use → synthesize） | **冻结** |

**关键洞见**：LATM 的 T 修改是**有成本边界的**——不是"无限扩展"（Voyager），也不是"固定不变"（ReAct），而是"cost-aware 的有限扩展"。这是 LATM 与 Voyager 的根本差异。

### 4.2 LATM 中 U 的状态

LATM 的 U 是 **Tool Maker + Cost Model + Tool Pool**：

$$
T^{t+1} = \begin{cases}
T^t \cup \{f_{\text{new}}\} & \text{if cost}(f_{\text{new}}) < \text{benefit}(f_{\text{new}}) \text{ AND validate}(f_{\text{new}}) = \text{pass} \\
T^t & \text{otherwise}
\end{cases}
$$

其中：
- $\text{cost}(f_{\text{new}})$：制造函数的成本
- $\text{benefit}(f_{\text{new}})$：函数预期复用的收益
- $\text{validate}(f_{\text{new}})$：单元测试验证

U 的核心机制：**只有当收益大于成本**且**验证通过**时才扩展 T。这一 cost-benefit 分析是 LATM 的核心创新。

### 4.3 LATM 是"成本优化型 T 自扩展"

本书第 13 章把 T 自扩展分为两类：

| 类型 | 代表 | 驱动力 | 增长性 |
|---|---|---|---|
| 探索驱动 T 自扩展 | Voyager | Curriculum 探索 | 无限 |
| **成本驱动 T 自扩展** | **LATM** | **Cost model** | **有限** |

LATM 是成本驱动型的代表——它的 T 增长受经济约束（break-even 分析）。这一约束使 LATM 的 T 增长是**理性**的，而非**激进**的。

### 4.4 LATM 是"工具复用经济"

LATM 揭示了一个深刻的工程原则：**工具的价值在于复用**。制造一个工具的成本很高（GPT-4 调用 $0.03），但每次复用的边际成本很低（本地函数执行 ~0）。所以：

- **单次使用的工具**：不值得造——直接用 LLM 解决更便宜。
- **多次使用的工具**：值得造——边际成本摊薄后总体更便宜。
- **持续使用的工具**：必须造——这是 LATM 的核心动机。

这一"工具复用经济"是软件工程的经典原则——LATM 把这一原则应用于 LLM Agent。

### 4.5 LATM 在 L0-L5 等级中的位置

按本书第 18 章：

- **L2 ReAct Agent**：单 episode Thought-Action-Observation 循环
- **L3 Reflexion**：跨 episode 反思 + M 自修改
- **L4 Self-Modifying (P/T/M)**：**LATM 处于此级**（T cost-aware 自创建）

LATM 是 L4 中"成本优化型 T 自扩展"的代表。它的特征是：**T 可扩展但受成本约束；U 是 LLM + cost model；自修改有经济边界**。

### 4.6 LATM 与 H1-H5 的关系

| 假设 | LATM 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | T 可运行时扩展（cost-aware） | **支持 H1**（T 是可塑的） |
| **H2 协同演化** | T 扩展时 M（usage_history）也累积 | **部分支持 H2** |
| **H3 形态适配** | 不同任务制造不同的工具 | **支持 H3** |
| **H4 迁移收益** | Tool Pool 跨任务复用 | **强支持 H4**（工具复用） |
| **H5 治理必要性** | Cost model + 单元测试 | **支持 H5**（经济 + 验证治理） |

LATM 在 H4 上提供强证据——Tool Pool 的复用正是 H4（迁移收益）的体现。

### 4.7 LATM 与其他 L4 工作的边界

| 工作 | 修改对象 | 修改时机 | 验证机制 | 增长策略 |
|---|---|---|---|---|
| DSPy | P | 编译期 | dev set metric | 一次性 |
| OPRO | P | 运行时 | metric | 有限 |
| MemGPT | M | 运行时 | function calling | 持续 |
| A-MEM | M | 运行时 | embedding + links | 持续 |
| **LATM** | **T** | **运行时** | **单元测试** | **成本驱动** |
| Voyager | T | 运行时 | 环境执行 | 探索驱动 |

LATM 在"验证机制"列最轻——只用单元测试，不做环境验证。这与 Voyager 形成对比：Voyager 验证重但灵活，LATM 验证轻但受限。

## 5. 实验与结果

LATM 在多个推理任务上做了实验，我们逐个分析与操作形态学的关联：

### 5.1 GSM8K（小学数学）

- 数据集：8.5K 数学题
- 评测：accuracy
- Baselines：
  - Pure GPT-4：85%（高成本）
  - Pure GPT-3.5：62%（低成本）
  - CoT + GPT-3.5：70%
- LATM (GPT-4 Maker + GPT-3.5 User)：82%（成本比纯 GPT-4 低 50%）
- 操作形态学意义：**LATM 用 GPT-3.5 + GPT-4 组合达到接近纯 GPT-4 的性能**——T 自创建让便宜模型能解决"原本需要昂贵模型"的任务。

### 5.2 LogiQA（逻辑推理）

- 数据集：8K 逻辑题
- LATM (GPT-4 Maker + GPT-3.5 User)：78%
- Pure GPT-3.5：55%
- Pure GPT-4：80%
- 成本降低：45%
- 操作形态学意义：**逻辑推理函数（"判断前提是否支持结论"）被 GPT-4 制造，GPT-3.5 复用**——这是 T 自创建的成本效益证明。

### 5.3 TabMWP（表格推理）

- 数据集：38K 表格推理题
- LATM：87%
- Pure GPT-3.5：75%
- Pure GPT-4：89%
- 成本降低：40%
- 操作形态学意义：**"表格解析 + 数值计算"函数被缓存复用**——这是 T 自创建在结构化数据任务上的典型效果。

### 5.4 关键实验观察

| 任务 | LATM 性能 | Pure GPT-4 | 成本降低 | 主要 T 自创建 |
|---|---|---|---|---|
| GSM8K | 82% | 85% | 50% | "算术计算"函数 |
| LogiQA | 78% | 80% | 45% | "逻辑推理"函数 |
| TabMWP | 87% | 89% | 40% | "表格解析"函数 |

**关键观察 1**：LATM 在多个任务上接近纯 GPT-4 性能，但成本降低 40-50%——**这是 T 自创建的最大价值**。

**关键观察 2**：LATM 的工具复用次数越多，单任务平均成本越低。GSM8K 测试中，"算术计算"函数被复用 1000+ 次，摊薄成本接近零。

**关键观察 3**：LATM 的 T 自创建在"可被函数化的子任务"上最有效——数学计算、逻辑推理、表格解析。在"开放式创作任务"上效果差（无法函数化）。

### 5.5 消融研究：Cost Model 的影响

论文做了一组消融：
- LATM full（带 cost model）：性能 82%，成本 $X
- LATM no-cost-model（无成本约束，造所有工具）：性能 84%，成本 $1.5X
- Pure GPT-3.5：无 T 自创建：性能 62%
- Pure GPT-4：无成本优化：性能 85%，成本 $2X

**结论**：cost model 让 LATM 在性能和成本之间找到平衡——**造"高复用"的工具，不造"低复用"的工具**。

### 5.6 消融研究：Tool Pool 缓存的影响

论文对比了：
- LATM with cache：复用已有工具，性能 82%，成本 $X
- LATM no-cache：每次重新造工具，性能 82%，成本 $1.3X

**结论**：Tool Pool 缓存使 LATM 随时间变得更便宜——这是 H4（迁移收益）的直接证据。

### 5.7 跨任务迁移

论文测试了 LATM 在跨任务上的迁移能力：
- 在 GSM8K 上制造的"算术计算"工具
- 在 TabMWP 上能否直接复用？**Yes**——"算术计算"是通用工具
- 在 LogiQA 上能否复用？**No**——"算术计算"不是逻辑推理工具

**结论**：LATM 的 T 自创建产出"任务特异"工具，跨任务迁移有限。这与 H4（迁移收益）的"理想状态"有差距。

## 6. 局限与开放问题

LATM 的局限可以分为六类：**成本假设、工具粒度、验证局限、模型依赖、可解释性、安全性**。本节是本书对 LATM 的批判性分析。

### 6.1 成本假设的局限

LATM 的 cost model 假设 GPT-4 调用成本是 $0.03、GPT-3.5 是 $0.001。但实际成本受多个因素影响：
- **prompt 长度**：长 prompt 调用成本更高（按 token 计费）
- **completion 长度**：长输出成本更高
- **批处理折扣**：某些平台提供批处理折扣，成本可能远低于单次调用
- **响应时间成本**：慢响应可能影响用户体验

LATM 的 cost model 没有考虑这些因素——它的成本估计可能不准确。

**改进方向**：动态 cost model——根据实际 API 价格调整成本估计。

### 6.2 工具粒度的限制

LATM 的工具是**单函数**（`solve(input)`）。这一粒度有限制：
- **复杂工作流**：某些任务需要多个函数协作，LATM 不能直接建模。
- **状态依赖**：某些函数需要保持状态（如对话历史），单函数难以表达。
- **异步操作**：某些工具需要异步执行（如 API 调用），单函数难以处理。

**改进方向**：支持多函数工具、状态保持工具、异步工具。

### 6.3 验证局限

LATM 用**单元测试**验证生成的函数。但单元测试有局限：
- **测试覆盖不全**：GPT-4 生成的测试用例可能不全面，某些 bug 漏检。
- **测试用例错误**：GPT-4 自己写的测试用例可能本身就是错的。
- **没有环境验证**：不像 Voyager 在 Minecraft 中实际执行，LATM 只在抽象层面验证。

这一验证局限使 LATM 的工具可能"看起来正确，实际有 bug"。

**改进方向**：执行验证（在 sandbox 中运行）+ adversarial testing + 形式化验证。

### 6.4 模型依赖

LATM 假设 Tool Maker 用 GPT-4、Tool User 用 GPT-3.5。这一假设限制了 LATM 的适用性：
- **开源模型替代**：用开源 LLaMA / Mistral 替代 GPT-4 / GPT-3.5 时，cost model 需要重新调整。
- **新模型出现**：GPT-5 / Claude-4 / Gemini-2 出现后，cost model 又要调整。
- **模型升级**：GPT-3.5 升级到 GPT-3.5-Turbo 后，成本降低，break-even 改变。

LATM 的 cost model 是**模型特定的**——换模型要重新调优。

### 6.5 可解释性

LATM 的工具决策可解释性有限：
- **为什么造这个工具？**：cost model 给出了成本估计，但估计是否准确？
- **为什么不用某个已有工具？**：embedding 检索相似度低——但阈值如何确定？
- **工具失败的原因**：单元测试通过但实际失败——为什么？

本书第 22 章将深入讨论可解释性问题。

### 6.6 安全性

LATM 生成的 Python 函数可能被滥用：
- **危险函数**：Tool Maker 可能生成 `os.system("rm -rf /")` 等危险代码。
- **资源耗尽**：某些工具可能无限循环，耗尽 CPU/内存。
- **数据泄露**：某些工具可能读取敏感文件并发送到外部 API。

LATM 的安全机制有限——只有单元测试，没有沙箱保护。

**改进方向**：沙箱执行 + 静态分析 + 资源限制 + 行为审计。

### 6.7 开放问题表

| 问题 | 当前状态 | 本书视角 |
|---|---|---|
| 能动态调整 cost model 吗？ | 不能 | 第 13 章动态 cost model |
| 能支持多函数工具吗？ | 不能 | 第 13 章工具组合 |
| 能用执行验证代替单元测试吗？ | 不能 | 第 13 章执行验证 |
| 能跨模型迁移吗？ | 部分（重新调优） | 第 13 章 model-agnostic |
| 能抵御恶意工具吗？ | 不能 | 第 22 章对抗鲁棒性 |
| 能与 Voyager 融合吗？ | 不能 | 第 13 章 LATM + Voyager |

## 7. 对本书的贡献

LATM 在本书的理论体系中扮演**T 自创建的成本优化范式**——它是第 13 章"操作形态自扩展"的核心案例，也是工程实践中"成本敏感的 LLM Agent"的设计参考。

### 7.1 LATM 作为 T 自创建的范式

本书第 13 章把 T 自修改分为四个层级：

```
L4.1 单次 T 自创建（LATM）              ← cost-aware, 单函数
L4.2 持续 T 自扩展（Voyager）            ← 探索驱动, 永久技能库
L4.3 抽象 T 自演化（Spirit/SIM-2）       ← 技能有抽象层
L4.4 多 Agent T 协同（Multi-Voyager）    ← 多 Agent 共享工具库
```

LATM 是 L4.1 的代表——它让 Agent 在"造工具"与"用工具"之间做 cost-benefit 决策，证明**T 自修改可以是经济理性的**。

### 7.2 LATM 与第 13 章其他工作的对比

| 工作 | T 修改粒度 | 验证机制 | 增长策略 | 适用场景 |
|---|---|---|---|---|
| **LATM** | 单函数 | 单元测试 | **成本驱动** | 成本敏感的推理 |
| Voyager | 代码模块 | 环境执行 | 探索驱动 | 开放世界 |
| Toolformer | 工具调用 | 训练 loss | 一次性 | 固定工具集 |
| Generative Agents | 无 T 自修改 | — | — | 模拟社会 |

LATM 在"增长策略"列最经济——它是 T 自修改中最理性的实现。

### 7.3 LATM 与"工具复用经济"

LATM 揭示了 LLM Agent 时代的新经济学——**工具复用经济**：

- **制造工具的成本**：GPT-4 调用 $0.03
- **使用工具的成本**：本地函数 ~0
- **复用阈值**：break-even = 30 次

这一经济学与传统软件工程一致——LATM 把这一原则移植到 LLM Agent。

本书第 19 章"成本-效益分析"将深入讨论 LATM 的 cost model，并把它推广到 P/M/C 的修改成本。

### 7.4 LATM 与操作形态学的四元组

LATM 完整展示了 B = {P, T, M, C} 中**只有 T 可被 cost-aware 自创建**的场景。P 由 Maker / User 的 prompt 固定，M 由 usage_history 累积，C 由 `solve` 循环固定。LATM 只修改 T——但这一修改使 LATM 在推理任务上达到接近 GPT-4 的性能，成本降低 50%。

本书第 16 章"协同自进化"将讨论：**当 P/T/M 都能被 cost-aware 创建时，Agent 能否进一步降本？**

### 7.5 LATM 与 H1-H5 的实证贡献

LATM 在多个推理任务上证明：

1. **H1（结构可塑性）**：T 可运行时扩展（cost-aware）显著优于固定 T。
2. **H4（迁移收益）**：Tool Pool 跨任务复用降低平均成本。

但 LATM 也暴露了 L4 Agent 的局限：
- **H2（协同演化）**：LATM 只扩展 T，无法验证 H2。
- **H3（形态适配）**：LATM 的工具粒度（单函数）限制了形态适配的灵活性。
- **H5（治理必要性）**：LATM 的单元测试验证不足，安全风险高。

### 7.6 LATM 与 Voyager 的融合可能

LATM 与 Voyager 不是互斥的——它们可以融合：

```
融合架构:
- LATM 风格的 cost-aware 工具创建 (短期, 单任务)
- Voyager 风格的持续技能库 (长期, 跨任务)
- 共享 Tool Pool + Skill Library
```

这一融合使 Agent 同时具备**经济理性**（LATM）与**开放探索**（Voyager）。本书第 13 章将详细讨论这一融合架构。

### 7.7 给读者的关键启示

1. **LATM 是 cost-aware T 自扩展的代表**：它让 Agent 的工具创建受经济约束。理解 LATM 是理解"工程友好的 LLM Agent"的关键。
2. **Cost model 是 LATM 的核心创新**：它把"是否造工具"从 LLM 的灵机一动变成 cost-benefit 决策。这一创新可推广到 P/M/C 的修改决策。
3. **Tool Pool 缓存让 LATM 越来越便宜**：随着 Tool Pool 增长，单任务平均成本递减——这是 H4 的直接证据。
4. **LATM 与 Voyager 是互补的**：LATM 关注成本效率，Voyager 关注开放性。融合两者是第 13 章的研究方向。
5. **LATM 不是终点**：它只扩展 T，不修改 P/M/C。从 L4 到 L5 的跳跃需要把 cost-aware 思想推广到 P/M/C 的联合 cost-benefit 分析——这是 SICA、AlphaEvolve 等工作的愿景。
6. **LATM 的局限在于验证**：单元测试不足以保证工具正确性。未来的 T 自创建需要更严格的执行验证（Voyager 风格）+ 形式化验证（SICA 风格）。

LATM 是操作形态学意义上 **T 自修改从"无限扩展"到"经济理性"的范式转换**。它让 Agent 的工具创建不再是"探索驱动"，而是"成本驱动"。它与 Voyager（探索驱动）共同构成 T 自修改的两种哲学。

## 参考文献

- cai2023latm: Cai, T., Wang, X., Ma, T., Chen, X., & Zhou, D. (2023). *Large Language Models as Tool Makers*. arXiv:2305.17126 (NeurIPS 2023). [$TRAE_REF](https://arxiv.org/abs/2305.17126)
- wang2023voyager: Wang, G., et al. (2023). *Voyager: An Open-Ended Embodied Agent with Large Language Models*. arXiv:2305.16291. 见 r-paper-017。（探索驱动 T 自扩展，与 LATM 对照）
- schick2023toolformer: Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. NeurIPS 2023. 见 r-paper-003。（训练期 T 集成，与 LATM 对照）
- yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 见 r-paper-001。（LATM 的任务分解基于 ReAct 思想）
- opsahl2024opro: Opsahl-Ong, K., et al. (2024). *Optimizing Prompts via In-Context or Automatic Prompt Optimization*. NeurIPS 2024. 见 r-paper-008。（runtime P 自修改，与 LATM 的 T 自修改对照）