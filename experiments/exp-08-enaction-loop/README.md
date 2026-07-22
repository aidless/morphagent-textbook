# 实验 8：Enaction 循环实现

> 状态：可运行（Mock 模式）
> 目标：实现并验证 Enaction（行动生成）循环
> 难度：★★★☆☆
> 预计时间：4 小时

## 实验目的

实现 Varela 提出的 Enaction 循环：Perception -> Action -> Environment Change -> New Perception。
验证"认知通过行动与环境的耦合循环而产生"。

## 实验步骤

1. 实现模拟环境（简单网格世界）
2. 实现 Agent 的感知-行动循环
3. 运行 5 个场景，记录完整的 Enaction 轨迹
4. 分析循环中"行动如何改变感知"的模式

## 预期结果

- 能观察到 Agent 的行动确实改变了环境状态
- 新的感知依赖于之前行动的结果
- 形成完整的 Perception-Action 耦合循环

## 运行方式

```bash
cd experiments/exp-08-enaction-loop
python main.py
```
