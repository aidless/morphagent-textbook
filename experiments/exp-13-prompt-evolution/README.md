# 实验 13：Prompt 进化轨迹

> 状态：可运行（Mock 模式）
> 目标：追踪 Prompt 在多轮 OPRO 优化后的进化轨迹
> 难度：★★★☆☆
> 预计时间：4 小时

## 实验目的

复现 OPRO 爬山过程，记录每轮的 top-3 prompt 和准确率，绘制完整的进化轨迹。

## 实验步骤

1. 初始化一个基础 prompt
2. 每轮生成 5 个候选 prompt 变体
3. 在 10 个任务上评估每个候选
4. 保留 top-3 并进入下一轮
5. 重复 5 轮，记录完整轨迹

## 评测指标

- 每轮 top-3 prompt 及其准确率
- 全局最优 prompt
- 进化曲线（准确率 vs 轮次）
- prompt 漂移分数

## 运行方式

```bash
cd experiments/exp-13-prompt-evolution
python main.py
```
