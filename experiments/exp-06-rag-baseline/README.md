# 实验 6：RAG 基线对比

> 状态：可运行（Mock 模式）
> 目标：对比 naive chunking vs semantic chunking 在 RAG 检索质量上的差异
> 难度：★★★☆☆
> 预计时间：3 小时

## 实验目的

实现两种文档分块策略（naive vs semantic），比较它们在 RAG 场景下的检索准确率。

## 实验步骤

1. 实现-naive chunking：按固定字符数切分文档
2. 实现 semantic chunking：按句子边界 + 语义相似度切分
3. 构造 5 篇 mock 文档
4. 对每个文档提出 3 个问题
5. 对比两种分块策略下的检索命中率和答案准确率

## 评测指标

- **检索命中率**：正确 chunk 是否被检索到（Top-3）
- **答案准确率**：最终答案是否正确
- **平均 chunk 质量**：chunk 的大小和语义完整性

## 预期结果

| 分块策略 | 检索命中率 | 答案准确率 |
|---|---|---|
| Naive (200字) | ~65% | ~60% |
| Semantic | ~85% | ~80% |

## 运行方式

```bash
cd experiments/exp-06-rag-baseline
python main.py
```

## 依赖

无需额外依赖（mock 模式）。真实模式可选：sentence-transformers
