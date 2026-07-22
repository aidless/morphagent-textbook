# 实验 1：基线对比

> 状态：可运行
> 目标：对比 4 个代表 Agent 系统的性能基线
> 运行时长：< 1 分钟（mock 模式）/ 30 分钟（真实 LLM 模式）

## 实验设计

### 4 个基线系统

| 系统 | 设计 | 最大步数 | 反思机制 |
|---|---|---|---|
| ReAct | 直接 thought-action 循环 | 5 | 无 |
| Reflexion | ReAct + 失败后反思 | 5 | 有（单次） |
| AutoGPT | 开放式目标分解 | 10 | 无 |
| BabyAGI | 任务队列 + 子任务 | 5 | 无 |

### 10 个测试任务

| ID | 任务 | 期望工具 | 期望答案 |
|---|---|---|---|
| weather-1 | 北京天气 | get_weather | 包含"北京" |
| weather-2 | 上海天气 | get_weather | 包含"上海" |
| weather-3 | 广州天气 | get_weather | 包含"广州" |
| calc-1 | 123+456 | add | 包含"579" |
| calc-2 | 1024×768 | multiply | 包含"786432" |
| calc-3 | π×10 | multiply | 包含"31.4" |
| search-1 | 搜 arXiv LLM Agent | search_arxiv | 包含"arxiv" |
| search-2 | 搜 arXiv Embodied AI | search_arxiv | 包含"embodied" |
| file-1 | 读 /etc/hostname | read_file | （任意） |
| translate-1 | 翻译 Hello World | translate | 包含"你好" |

## 评测指标

- **成功率**：任务完成的比例
- **平均步数**：成功任务平均用了多少步
- **平均 token**：平均消耗的 token 数
- **平均错误恢复**：平均每个任务修复了几次错误

## 运行方式

### Mock 模式（默认，不需要 API key）

```bash
cd experiments/exp-01-baseline
python run.py
```

### 真实 LLM 模式

修改 `run.py` 顶部的 `mock_llm_baseline` 为真实 API：

```python
import openai

def llm(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
```

然后 `python run.py`。预算约 $5。

## 预期结果

| 系统 | 预期成功率 | 预期步数 |
|---|---|---|
| ReAct | 70% | 2-3 |
| Reflexion | 80% | 3-4（带反思） |
| AutoGPT | 60% | 5-8（更多步数） |
| BabyAGI | 75% | 3-4 |

## 输出

- `results.json`：原始结果
- 控制台：综合对比表

## 已知限制

- Mock LLM 只能处理"关键词匹配"，无法处理复杂语义
- 真实 LLM 模式下成功率会更高，但成本也更高
- 没有统计显著性检验（样本量小）
