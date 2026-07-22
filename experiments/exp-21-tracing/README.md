# 实验 21：OpenTelemetry 链路追踪

> 状态：可运行（Mock 模式）
> 目标：模拟 OpenTelemetry 链路追踪，分析 Agent 请求的调用链
> 难度：★★★★☆
> 预计时间：6 小时

## 实验目的

模拟 OpenTelemetry 风格的分布式链路追踪。
追踪 Agent 请求在多个子系统间的完整调用链，识别瓶颈和异常。

## 实验步骤

1. 定义 Span 模型（操作名称、耗时、状态、标签）
2. 生成模拟调用链（含嵌套和并行调用）
3. 分析链路：找出慢 span、错误 span、关键路径
4. 对比有/无追踪时的故障定位效率

## 评测指标

- 关键路径延迟
- 慢 span 识别准确率
- 故障定位时间

## 运行方式

```bash
cd experiments/exp-21-tracing
python main.py
```
