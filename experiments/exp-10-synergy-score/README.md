# 实验 10：P/T/M/C 协同度评分

> 状态：可运行（Mock 模式）
> 目标：量化 Agent 四大子系统（Prompt/Tool/Memory/Cognition）的协同程度
> 难度：★★★☆☆
> 预计时间：3 小时

## 实验目的

实现一个 Synergy Score 算法，量化 Agent 的 P/T/M/C 四个子系统之间的协同程度。

## 实验步骤

1. 定义 P/T/M/C 四个子系统的状态表示
2. 实现协同度评分算法（基于子系统间的一致性）
3. 在 5 个 Agent 配置上计算 Synergy Score
4. 分析协同度与任务表现的相关性

## 评分公式

Synergy = avg(pairwise_consistency(P,T), pairwise_consistency(P,M),
             pairwise_consistency(P,C), pairwise_consistency(T,M),
             pairwise_consistency(T,C), pairwise_consistency(M,C))

## 运行方式

```bash
cd experiments/exp-10-synergy-score
python main.py
```
