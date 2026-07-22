# 实验代码骨架 — 操作系统形态学

> 目标：提供 4 个**最小可运行**的实验，覆盖全书最核心的研究问题。
> 原则：每个实验 ≤ 200 行 Python，零网络依赖（除调用 LLM API），3 步内可运行。

## 实验目录

```
experiments/
├── README.md                    # 本文件
├── exp-01-baseline/             # 实验 1：基线对比
├── exp-02-pomdp-claim/           # 实验 2：信念状态 ≈ 短期记忆 假设
├── exp-03-tool-description/      # 实验 3：工具描述对调用准确率的影响
├── exp-04-self-modifying-prompt/ # 实验 4：自修改 prompt vs 静态 prompt
└── _shared/                     # 共享工具
    ├── agent_loop.py             # ReAct 循环的最小实现
    ├── metrics.py                # 评测指标
    └── utils.py                  # 配置 + 日志
```

## 实验 1：基线对比（exp-01-baseline）

**目的**：对比 4 个代表 Agent 的性能，建立"基准"基线。

**4 个基线**：
- ReAct（直接 prompt + 工具调用）
- Reflexion（带反思）
- AutoGPT（开放式循环）
- BabyAGI（任务队列）

**指标**：
- 任务成功率
- 平均 token 消耗
- 平均完成步数
- 错误恢复次数

**输入**：10 个标准化任务（如"查北京天气"、"写斐波那契函数"）

**运行**：
```bash
cd exp-01-baseline
python run.py
```

## 实验 2：POMDP 信念状态验证（exp-02-pomdp-claim）

**目的**：验证第 2 章的核心命题——"LLM Agent 的信念状态 = 短期记忆"。

**设计**：
- 构造 5 个不同状态的 POMDP（世界状态、Agent 观察、Agent 行动）
- 让 LLM Agent 在每个 POMDP 上执行 10 步
- 测量：LLM 的行动选择是否与"信念状态"一致？

**指标**：
- 行动合理性得分（0-1）
- 信念一致率

**运行**：
```bash
cd exp-02-pomdp-claim
python run.py
```

## 实验 3：工具描述对调用准确率的影响（exp-03-tool-description）

**目的**：量化第 3 章 3.5 节的论断——"工具描述质量对 LLM 调用准确率有显著影响"。

**设计**：
- 5 个测试工具（天气、搜索、计算、文件操作、邮件）
- 5 个描述级别（极简→极详）
- 3 个 LLM（GPT-4、Claude 3.5、Llama 3.1）
- 每个组合测试 50 次

**指标**：
- 调用准确率
- 首次成功所需的平均调用次数
- 描述完整度与准确率的相关性

**运行**：
```bash
cd exp-03-tool-description
python run.py
```

## 实验 4：自修改 prompt vs 静态 prompt（exp-04-self-modifying-prompt）

**目的**：验证 OPRO 风格的 prompt 自修改 vs 静态 prompt 在 GSM8K 上的提升。

**设计**：
- 基线：手工设计的 prompt
- 处理 1：DSPy 优化
- 处理 2：OPRO 迭代优化
- 处理 3：PE2 反射式优化
- 每个处理在 GSM8K 测试集上跑 100 题

**指标**：
- 准确率
- 收敛所需步数
- 最终 prompt 的可读性（人类评分）

**运行**：
```bash
cd exp-04-self-modifying-prompt
python run.py
```

## 共享工具

### _shared/agent_loop.py

最小可运行的 ReAct 循环：

```python
"""最小 ReAct 循环，用于实验 1-4 的基线。"""
import json
from typing import Callable, Dict, List, Any

def react_loop(
    query: str,
    llm: Callable[[str], str],
    tools: Dict[str, Callable],
    max_steps: int = 10,
) -> Dict[str, Any]:
    """执行 ReAct 循环直到任务完成或达最大步数。"""
    history = [f"User: {query}"]
    trajectory = []
    
    for step in range(max_steps):
        # 1. 思考
        prompt = format_react_prompt(query, history, tools)
        response = llm(prompt)
        
        # 2. 解析
        thought, action = parse_react(response)
        trajectory.append({"step": step, "thought": thought, "action": action})
        
        if action["type"] == "finish":
            return {"success": True, "answer": action["answer"], 
                    "trajectory": trajectory, "steps": step + 1}
        
        # 3. 执行工具
        tool_name = action["name"]
        if tool_name not in tools:
            history.append(f"Observation: Error - tool {tool_name} not found")
            continue
        try:
            result = tools[tool_name](**action["arguments"])
            history.append(f"Observation: {result}")
        except Exception as e:
            history.append(f"Observation: Error - {e}")
    
    return {"success": False, "answer": None, "trajectory": trajectory, "steps": max_steps}
```

### _shared/metrics.py

标准评测指标：

```python
"""评测指标集合。"""

def success_rate(results: List[Dict]) -> float:
    """任务成功率。"""
    return sum(r["success"] for r in results) / len(results)

def avg_steps(results: List[Dict]) -> float:
    """平均完成步数。"""
    return sum(r["steps"] for r in results) / len(results)

def avg_tokens(usage_records: List[int]) -> float:
    """平均 token 消耗。"""
    return sum(usage_records) / len(usage_records)

def action_consistency(trajectories: List[Dict], optimal_actions: List) -> float:
    """行动合理性得分。"""
    correct = sum(1 for t, opt in zip(trajectories, optimal_actions) 
                  if t["action"] == opt)
    return correct / len(trajectories)
```

## 运行要求

- Python 3.10+
- 第三方依赖：openai、anthropic、transformers（可选）
- 环境变量：OPENAI_API_KEY、ANTHROPIC_API_KEY
- 总运行成本：每个实验 < $50

## 实验伦理

- 所有实验使用公开数据集
- 不在评测中包含个人隐私数据
- LLM API 调用有成本上限，超出立即停止
- 失败实验不删除，标注 `status: failed` 保留
