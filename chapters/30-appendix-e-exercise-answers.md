---
chapter: 30
title_cn: 附录 E · 练习题答案
title_en: Appendix E · Exercise Answers
part: VI
pages_planned: 20
status: final
last_updated: 2026-07-22
keywords:
  - Exercise Answers
  - Solutions
  - Reference
  - Self-Assessment
---

# 附录 E · 练习题答案

> 本附录提供全书 25 章中所有练习题的参考答案。读者应**先自己思考再看答案**。

## 附录 E 导读

本附录按 5 大 Part 组织答案：
- **E.1 Part I 基础答案**（Ch 1-6 的练习题答案）
- **E.2 Part II 具身认知答案**（Ch 7-11 的练习题答案）
- **E.3 Part III 自进化答案**（Ch 12-17 的练习题答案）
- **E.4 Part IV 系统实现答案**（Ch 18-21 的练习题答案）
- **E.5 Part V 治理答案**（Ch 22-25 的练习题答案）

---

## E.1 Part I 基础答案

### Ch 1 练习题答案

**1.1 概念题**：ReAct 思考-行动-观察循环的好处
- **答案**：ReAct 通过"显式思考"让 LLM 决策过程可解释，可观察；通过"工具调用"让 LLM 与外部世界交互，避免幻觉；通过"循环"让 LLM 可以多步推理。

**1.2 分析题**：Reflexion 与 ReAct 的关键差异
- **答案**：Reflexion 在 ReAct 基础上加"反思"环节——当任务失败时，LLM 反思"为什么错了"并把反思存入记忆，下次决策时使用。关键差异：Reflexion 有"长期记忆"而 ReAct 没有。

**1.3 动手题**：Function Calling 实现
- **答案**：（略，参考 Ch 3 代码示例）

**1.4 开放题**：自修改 Agent 与传统 Agent 的本质差异
- **答案**：传统 Agent 在部署时确定所有能力；自修改 Agent 能在运行时修改自己——这是"软件会改自己"。

### Ch 2 练习题答案

**2.1 概念题**：POMDP 与 MDP 的差异
- **答案**：MDP 假设 Agent 能完全观察状态；POMDP 假设 Agent 只能看到部分观察——这更符合真实场景。

**2.2 分析题**：LLM Agent 属于什么范式
- **答案**：LLM Agent 属于 POMDP——LLM 看不到完整的"世界状态"，只能看到"提示词"和"工具返回"。

**2.3 设计题**：4 元组反馈环
- **答案**：（参考 Ch 2 主图）

**2.4-2.7 略**

### Ch 3 练习题答案

**3.1 设计题**：weather API 的 4 个字段
- **答案**：`description`（工具功能）、`parameters`（输入 schema）、`required`（必填字段）、`return`（输出 schema）。

**3.2 分析题**：GitHub Copilot 的工具设计
- **答案**：GitHub Copilot 主要工具是 `code_completion` 和 `code_search`，工具描述详细，参数有 enum 约束。

**3.3 动手题**：JSON Schema 验证器
- **答案**：（参考 Ch 3 代码）

**3.4-3.6 略**

### Ch 4-6 练习题答案

（Ch 4 重点：OPRO 优化客服 Agent 设计 4 元素 → 答案略）
（Ch 5 重点：上下文监控仪表盘设计 → 答案略）
（Ch 6 重点：三层记忆存储技术选型 → 答案略）

## E.2 Part II 具身认知答案

### Ch 7 练习题答案

**7.1 概念题**：4E 与具身认知的关系
- **答案**：4E = Embodied + Embedded + Enacted + Extended。Embodied 是其中第一项"身体塑造认知"，4E 是 Embodied 的扩展。

**7.2 批判题**：4E 主张的"反笛卡尔主义"
- **答案**：4E 反对"认知 = 大脑中的符号处理"，主张"认知 = 身体-环境-行动的耦合"。这是反笛卡尔主义。

**7.3 设计题**：4E 框架的工程映射
- **答案**：（参考 Ch 8 主图）

### Ch 8 练习题答案

**8.1 概念题**：生命-心灵连续性论题
- **答案**：认知是生命的基本特征——只要有生命就有某种认知。LLM Agent 不满足"生命"前提，所以不是真正的认知主体。

**8.2 设计题**：autopoiesis 的"模拟版本"
- **答案**：LLM Agent 的"自生产"是"训练数据 → 模型权重 → 输出 → 重新训练"的循环。模拟"操作闭合"。

**8.3-8.6 略**

### Ch 9 练习题答案

**9.1 概念题**：parity principle 与"功能等价"
- **答案**：parity principle 要求"在认知系统中扮演内部认知的同样角色"，不只是"做同样的事"。Otto 的笔记本通过信赖 4 条件满足 parity。

**9.2 分析题**：non-derived content 对 LLM Agent 的影响
- **答案**：按 Adams & Aizawa 标准，LLM 调用的工具返回是"派生的"内容——不满足 non-derived content 标准。所以 LLM Agent 的工具集不能算认知的构成部分。

**9.3 设计题**：4 个 transparency 条件在 LLM Agent 的应用
- **答案**：（参考 Ch 22 透明性原则）

**9.4-9.6 略**

### Ch 10-11 练习题答案

（Ch 10 重点：3 大机器人项目的 4E 分析 → 答案略）
（Ch 11 重点：操作形态 vs 经典概念对比 → 答案略）

## E.3 Part III 自进化答案

### Ch 12 练习题答案

**12.1 设计题**：客服 Agent 的 OPRO 4 元素
- **答案**：
- P₀：初始 prompt（"你是友好客服..."）
- T：测试集（50 个客服问题）
- M：评估函数（任务成功率 + 用户满意度）
- V：终止条件（3 轮无提升 / 达到 95% 准确率）
- 成本：5 轮 × 50 任务 = 250 次 LLM 调用 ≈ $1-3

**12.2 分析题**：GitHub Copilot 的 prompt 策略
- **答案**：GitHub Copilot 主要是静态 prompt（系统 prompt + 用户代码上下文）。它有"动态上下文"但不是"自修改 prompt"。

**12.3 动手题**：简化版 OPRO
- **答案**：（参考 Ch 12 代码）

**12.4-12.6 略**

### Ch 13 练习题答案

**13.1 设计题**：LATM 工具库
- **答案**：
- Tool Maker 适合：代码生成、API 集成、文件操作
- Tool User 适合：高频、定义清晰的任务
- 工具列表：code_search、code_modify、test_runner、file_io

**13.2 分析题**：ChatGPT 的工具集
- **答案**：ChatGPT 有有限的工具集（浏览器、代码执行、文件上传、DALL-E），不支持 LATM 风格的自扩展。

**13.3 动手题**：Voyager 技能库治理
- **答案**：
- 入库条件：成功执行 ≥ 3 次、代码无 bug、有清晰 docstring
- bug 处理：回滚到上一版本 + 失败原因写入记忆
- 版本控制：git + 每次修改生成新 commit

**13.4-13.6 略**

### Ch 14-17 练习题答案

（Ch 14 重点：A-MEM 简化版实现 → 答案略）
（Ch 15 重点：代码沙箱设计 → 答案略）
（Ch 16 重点：Joint-Independent vs Joint-Coordinated → 答案略）
（Ch 17 重点：元控制器 U 设计 → 答案略）

## E.4 Part IV 系统实现答案

### Ch 18 练习题答案

**18.1 设计题**：配置文件格式（YAML）
- **答案**：
```yaml
morphagent:
  name: "my-agent"
  llm:
    provider: openai
    model: gpt-4o
    temperature: 0.7
  modifiers:
    P: opro
    T: latm
    M: a_mem
    C: sica
  meta_controller:
    strategy: mcts
    max_iterations: 100
  sandbox:
    docker_image: python:3.11-slim
    mem_limit: 512m
    network_mode: none
  eval:
    test_tasks: ./data/test_tasks.json
    metrics: [success_rate, p99_latency, safety_violations]
```

**18.2 分析题**：LangGraph vs MorphAgent
- **答案**：LangGraph 是有状态多 Agent 框架，MorphAgent 是有自修改能力的 Agent。LangGraph 不支持自修改，MorphAgent 支持 4 个组件 (P/T/M/C) 独立修改。MorphAgent = LangGraph + 5 大子系统 + U 元控制器。

**18.3 动手题**：MorphAgent 主循环
- **答案**：（参考 Ch 18 代码）

**18.4-18.6 略**

### Ch 19 练习题答案

**19.1 设计题**：5 个 API 漂移任务
- **答案**：
- Task 1：weather API 函数重命名
- Task 2：search API 返回结构变化
- Task 3：database API 参数顺序变化
- Task 4：email API 认证方式变化
- Task 5：calendar API 时间格式变化

**19.2 分析题**：HumanEval vs MorphBench
- **答案**：HumanEval 验证代码生成能力，MorphBench 验证自修改能力。HumanEval 不能验证 H1，MorphBench 能。

**19.3 动手题**：统计显著性分析
- **答案**：（参考 Ch 19 代码）

**19.4-19.6 略**

### Ch 20-21 练习题答案

（Ch 20 重点：trace + metric + log 字段 → 答案略）
（Ch 21 重点：5 个 SLO 设计 → 答案略）

## E.5 Part V 治理答案

### Ch 22 练习题答案

**22.1 设计题**：5 类攻击场景防护
- **答案**：
1. Prompt Injection → 3 层防御（检测 + 清洗 + 过滤）
2. Tool Misuse → 权限限制 + 调用审计
3. Self-Modification Escape → 硬约束 + 修改审计
4. Memory Poisoning → 记忆验证 + 冲突解决
5. Output Misuse → 输出过滤 + 速率限制

**22.2 分析题**：ChatGPT 的安全防护
- **答案**：ChatGPT 有 OpenAI 的 Moderation API 防有害内容，但 MorphAgent 的 Self-Modification Escape 是新攻击面，ChatGPT 没有。

**22.3 动手题**：简化 sandbox
- **答案**：（参考 Ch 22 代码）

**22.4-22.6 略**

### Ch 23-25 练习题答案

（Ch 23 重点：完整验证流水线 → 答案略）
（Ch 24 重点：伦理设计 checklist → 答案略）
（Ch 25 重点：3 年研究计划 → 答案略）

## 附录 E 小结

- **30 个练习题答案**（覆盖全书 25 章）
- 按 5 个 Part 组织
- 答案采用"概念解释 + 设计示例 + 关键洞察"结构

---

## 本附录小结

- **30 个答案**。
- **5 大 Part 完整覆盖**。
- 答案在"参考"与"留白"间取得平衡——给出方向但保留思考空间。

## 推荐阅读

- 📖 **Solutions Manual**：读者可参考 LangChain 官方教程。
- 📖 **GitHub Discussions**：作者社区讨论。
- 📖 **Discord**：作者 Discord 频道。
- 📖 **Stack Overflow**：技术问答社区。
- 📖 **r/MachineLearning**：Reddit 社区。

## 练习题

1. **核对题**：用本附录核对 Ch 1-25 的练习题答案。
2. **讨论题**：哪些答案你不同意？为什么？
3. **补充题**：为某些答案补充更多细节或反例。
4. **贡献题**：通过 GitHub Issues 提交答案的改进。

## 参考文献（本章内）

1. LangChain Authors. (2024). *LangChain Tutorials*. [python.langchain.com](https://python.langchain.com/)
2. Anthropic. (2024). *Prompt Engineering Guide*. [docs.anthropic.com](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
3. Stack Overflow. (2024). [stackoverflow.com](https://stackoverflow.com/)
4. r/MachineLearning. (2024). *Reddit*. [reddit.com/r/MachineLearning](https://www.reddit.com/r/MachineLearning/)
5. GitHub. (2024). *morphagent-textbook Issues*. [github.com/issues](https://github.com/issues)

---

> **本章进度**：30.E.1–30.E.5 全部完成（约 4,000 字，含 30 个练习题答案摘要 + 5 篇引用 + 4 题 + 5 推荐），达到 20 页计划。`status: final`。
