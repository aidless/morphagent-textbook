# 实验 4：自修改 prompt vs 静态 prompt

> 状态：可运行
> 目标：验证 OPRO 风格的 prompt 自修改 vs 静态 prompt 的提升
> 运行时长：< 1 分钟

## 实验设计

### 4 种 Prompt 策略

| 策略 | 描述 | 期望准确率 |
|---|---|---|
| static | 手工设计的基础 prompt | ~50% |
| dspy_optimized | DSPy 风格的编译器优化 prompt | ~60% |
| opro_iter1 | OPRO 第 1 轮迭代 | ~70% |
| opro_iter3 | OPRO 第 3 轮迭代 | ~80% |

### 10 个 GSM8K 简化测试题

- 加减乘除基础题
- 多步骤问题
- 简单单位转换

## 假设

- **H1**：自修改 prompt（OPRO iter3）准确率显著高于静态 prompt。
- **H2**：自修改 prompt 的提升主要来自"专家角色"和"步骤化"指令。
- **H3**：进一步迭代（iter3 vs iter1）的边际收益递减。

## 指标

- **准确率**：回答正确的比例
- **收敛步数**：达到峰值准确率需要的迭代次数
- **可读性**：最终 prompt 对人类的可理解性（人工评估）

## 运行方式

```bash
cd experiments/exp-04-self-modifying-prompt
python run.py
```

## 预期结果

```
| 策略 | 准确率 | 相对 static 提升 |
|---|---|---|
| static | 50% | 0pp |
| dspy_optimized | 60% | +10pp |
| opro_iter1 | 70% | +20pp |
| opro_iter3 | 80% | +30pp |
```

## 实验方法论说明

本实验是"OPRO 风格"的简化版——不真正让 LLM 优化 prompt，而是预设了 4 个不同质量的 prompt 模板，验证"prompt 质量与准确率"的关系。真实实验需要：
1. 调用 LLM 生成候选 prompt
2. 评估 prompt 在测试集上的准确率
3. 选择 top-K prompt 进入下一轮
4. 迭代直到收敛

## 已知限制

- Mock 模式：没有真实 LLM 调用，无法模拟"自修改"的搜索过程
- 10 个测试题样本量小
- 真实 LLM 实验需要约 $30 预算
- 没有评估 prompt 的可读性
