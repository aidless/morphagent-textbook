# 实验 15：记忆自适应

> 状态：可运行（Mock 模式）
> 目标：模拟 MemGPT 风格的记忆自适应管理
> 难度：★★★★☆
> 预计时间：6 小时

## 实验目的

实现简化版 MemGPT，验证记忆管理策略（核心记忆/外部记忆的分页调度）
对长对话成功率的影响。

## 实验步骤

1. 实现核心记忆（有限容量）和外部记忆（无限容量）
2. 实现 3 个核心函数：recall_memory, core_memory_append, core_memory_replace
3. 模拟 20 轮对话，测量不同记忆策略下的任务成功率
4. 对比：固定记忆 vs 自适应记忆 vs 无记忆管理

## 评测指标

- 任务成功率（随对话轮次变化）
- token 消耗（核心记忆越大，消耗越高）
- 关键信息召回率

## 运行方式

```bash
cd experiments/exp-15-memory-adaptation
python main.py
```
