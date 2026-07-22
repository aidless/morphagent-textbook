# 实验 11：形态可塑性测量

> 状态：可运行（Mock 模式）
> 目标：测量 B（Agent 形态）修改后任务表现的变化幅度
> 难度：★★★★☆
> 预计时间：6 小时

## 实验目的

验证"操作形态可塑性"——修改 Agent 的形态（Prompt/Tool/Memory）后，
任务表现会发生可测量的变化。

## 实验步骤

1. 定义基线 Agent 配置（P/T/M/C）
2. 分别修改 P、T、M、C 四个子系统
3. 在 5 类任务上测量修改前后的表现变化
4. 计算形态可塑性指数（MPI = |delta_performance| / |delta_config|）

## 评测指标

- **MPI（Morphological Plasticity Index）**: 形态改变导致的表现变化幅度
- **敏感度矩阵**: 每个子系统对每类任务的敏感度

## 预期结果

| 干预 | 敏感任务 | 不敏感任务 | 平均 MPI |
|---|---|---|---|
| 修改 P | 推理类 | 数据类 | 0.3 |
| 修改 T | 工具使用 | 问答 | 0.4 |
| 修改 M | 长对话 | 单轮 | 0.35 |
| 修改 C | 复杂决策 | 简单查询 | 0.25 |

## 运行方式

```bash
cd experiments/exp-11-morphological-plasticity
python main.py
```
