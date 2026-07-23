---
chapter: 13
title_cn: 自动工具创建与重构
title_en: Automatic Tool Creation and Refactoring
part: III
pages_planned: 28
status: final
last_updated: 2026-07-22
keywords:
  - LATM
  - Voyager
  - AFlow
  - EvoAgent
  - AlphaEvolve
  - Tool Affordance
  - Tool Lifecycle
  - Tool Refactoring
learning_objectives:
  - 跑通 LATM 两阶段（tool maker + tool user）范式
  - 复述 Voyager 技能库增长机制
  - 复述 AFlow 工作流进化范式
  - 复述 EvoAgent 多 Agent 进化范式
  - 复述 AlphaEvolve 代码库进化范式
  - 设计工具生命周期治理
  - 评估 T 自修改的工程效果与边界
  - 把 T 自修改定位为 H1 的第二个验证案例
prerequisites:
  - Ch 3, Ch 11, Ch 12
---

# 第 13 章 · 自动工具创建与重构

> "Agent 不能只调用工具——Agent 必须能创建、重构、淘汰工具。"

## 学习目标

完成本章后，读者应能够：

1. 跑通 LATM 两阶段（tool maker + tool user）范式
2. 复述 Voyager 技能库增长机制
3. 复述 AFlow 工作流进化范式
4. 复述 EvoAgent 多 Agent 进化范式
5. 复述 AlphaEvolve 代码库进化范式
6. 设计工具生命周期治理
7. 评估 T 自修改的工程效果与边界
8. 把 T 自修改定位为 H1 的第二个验证案例

## 先修知识

- 第 3 章 · 工具与函数调用
- 第 11 章 · 操作形态学形式化
- 第 12 章 · 自修改 prompt

## 章节地图

- **13.1** 操作形态学的第二个应用：修改 T
- **13.2** LATM：让 LLM 自己造工具
- **13.3** Voyager：无限增长的技能库
- **13.4** AFlow：工作流自动进化
- **13.5** EvoAgent：多 Agent 系统自动生成
- **13.6** AlphaEvolve：整个代码库作为进化对象
- **13.7** 工具生命周期治理
- **13.8** H1 的第二个验证案例
- **13.9** 本章小结与第 14 章预告

---

## 13.1 操作形态学的第二个应用：修改 T

第 12 章讲了 P 自修改——H1 的第一个验证案例。本章讲 T 自修改——H1 的**第二个**验证案例。T 自修改比 P 自修改更复杂：

- P 自修改修改**自然语言字符串**
- T 自修改修改**结构化函数描述**（JSON Schema + 实现代码）

为什么 T 自修改比 P 自修改重要？

1. **扩展能力（capability expansion）**：P 自修改只能"调优指令"，T 自修改可以"扩展能力"——给 Agent 添加新工具意味着 Agent 能做新事 [r-note-012](../../research/r-note-012-tool-calling-three-layers.md)。
2. **降低单位成本**：P 自修改优化指令但不能减少 token 消耗；T 自修改可以让 Agent 把"多次 LLM 调用"替换为"一次工具调用"，大幅降低单位任务成本。
3. **支持新场景**：当任务环境变化时（如出现新的 API），P 自修改无能为力，T 自修改可以添加新工具。

但 T 自修改也面临独特挑战：

1. **正确性验证**：T 修改不仅是改字符串，还要保证函数实现是正确的。
2. **安全沙箱**：新工具的执行可能带来副作用（如文件修改、网络请求），必须沙箱化。
3. **版本治理**：T 修改比 P 修改更复杂（涉及函数实现、依赖、测试），版本管理更难。

### 图 13.1 · T 自修改在操作形态中的位置

```
   操作形态 B = {P, T, M, C}
                       ↑
                       │ 本章修改 T
                       │
   ┌───────────────────┴──────────────────┐
   │  P · Prompt (Ch 12, 已完成)          │
   │  T · Tool (本章)                     │
   │  M · Memory (Ch 14)                  │
   │  C · Code (Ch 15)                    │
   └──────────────────────────────────────┘
```

> **关键点**：T 自修改是 P 自修改的"能力升级版"——P 优化指令，T 扩展能力。

### 表 13.1 · 5 大 T 自修改范式对比

| 范式 | 时间 | 核心机制 | 关键结果 | 局限 |
|---|---|---|---|---|
| **LATM** | 2023-05 | 双 LLM：tool maker + tool user | GSM8K 与 GPT-4 等价，成本降 95% | 工具质量依赖 LLM |
| **Voyager** | 2023-05 | 技能库增长 + 自动课程 | Minecraft 3.3x unique items | 局限于 Minecraft |
| **AFlow** | 2024-10 | MCTS 搜索工作流 | 多任务平均 +10-15% | 样本复杂度高 |
| **EvoAgent** | 2025-04 | 进化算法生成多 Agent | 多 Agent 任务 +20% | 难以评估 Agent 质量 |
| **AlphaEvolve** | 2025-05 | 代码库作为进化对象 | 矩阵乘法、TPU 设计 | 仅适用于代码任务 |

## 13.2 LATM：让 LLM 自己造工具

**LATM（Large Language Models As Tool Makers）** 由 Cai 等人 2023 年 5 月提出，是 T 自修改的开山工作 [r-paper-018](../../research/r-paper-018-cai2023latm.md)。LATM 的核心思想是**双 LLM 分工**：

- **Tool Maker**（强 LLM，如 GPT-4）：设计、编写、调试工具
- **Tool User**（便宜 LLM，如 GPT-3.5）：使用工具解决任务

### LATM 的两阶段流程

```
   ┌──────────────────────────────────────────────────────────────┐
   │  阶段 1: Tool Making (用强 LLM)                               │
   │    - 给定任务描述                                              │
   │    - Tool Maker 生成工具的 Python 实现 + JSON Schema          │
   │    - Tool Maker 自己测试工具                                   │
   │    - 输出: 工具库 (Python 函数 + 描述)                       │
   └──────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
   ┌──────────────────────────────────────────────────────────────┐
   │  阶段 2: Tool Using (用便宜 LLM)                              │
   │    - 任务 query 到达                                           │
   │    - Tool User 看到工具库, 选择合适的工具                      │
   │    - Tool User 调用工具, 获取结果                              │
   │    - Tool User 综合结果, 给出答案                             │
   └──────────────────────────────────────────────────────────────┘
```

### LATM 的成本优势

LATM 在 Big-Bench 任务上达到了与 GPT-4 相当的准确率，但成本大幅降低：
- 全部用 GPT-4：约 $X（基线）
- LATM（Maker = GPT-4，User = GPT-3.5）：约 $X/20（5%）
- 准确率相当，**成本降 95%**

这是因为：
- Tool Maker 只在**开发阶段**调用一次
- Tool User 在**任务执行阶段**调用（便宜模型）
- 大量任务**复用**同一工具（缓存命中）

### 图 13.2 · LATM 的成本结构

```
   任务 N 个
       │
       ▼
   ┌─────────────────┐
   │ Tool User       │  ← 便宜 LLM（每任务 1 次）
   │ (便宜 LLM)      │
   └────────┬────────┘
            │
            ▼
   工具库 (Tool Library)  ← 缓存
            │
            ▼
   ┌─────────────────┐
   │ Tool Maker      │  ← 强 LLM（只调用 1 次，生成所有工具）
   │ (强 LLM)        │
   └─────────────────┘
```

> **关键点**：LATM 的成本优势来自"工具的**可复用性**"——Tool Maker 一次投入，Tool User 无数次复用。

> **复述框 · 13.2 节要点**
>
> - **LATM = Tool Maker + Tool User**：双 LLM 分工。
> - **核心结果**：Big-Bench 上与 GPT-4 准确率相当，成本降 95%。
> - **关键洞察**：工具的可复用性 = 成本优势。

## 13.3 Voyager：无限增长的技能库

**Voyager** 由 Wang 等人 2023 年 5 月提出，是 LLM Agent 在开放世界中"无限学习"的代表工作 [r-paper-017](../../research/r-paper-017-wang2023voyager.md)。Voyager 的核心思想是**技能库（Skill Library）的持续增长**——Agent 每掌握一个新技能，就把代码存进技能库，下次需要时直接调用。

### Voyager 的三大组件

1. **自动课程（Automatic Curriculum）**：根据当前状态推荐下一个学习目标
2. **技能库（Skill Library）**：以可执行代码形式存储所有已掌握的技能
3. **迭代提示（Iterative Prompting）**：用环境反馈和执行错误持续改进技能代码

### 图 13.3 · Voyager 的技能库增长循环

```
   ┌─────────────────┐         ┌─────────────────┐
   │  任务          │         │  技能库          │
   │  (Minecraft)   │  写代码  │  ┌─────────────┐ │
   └────────┬────────┘ ───────>│  │ skill_1      │ │
            │                   │  │ skill_2      │ │
            │ 失败/成功         │  │ skill_3      │ │
            ▼                   │  │ ...          │ │
   ┌─────────────────┐         │  └─────────────┘ │
   │  环境反馈       │         │       ↑         │
   │  (反馈)        │  调用技能 │       │         │
   └────────┬────────┘ <────── │       │         │
            │                   └───────┴─────────┘
            ▼
   ┌─────────────────┐
   │  改进技能       │  ← 失败的技能被重写
   │  (LLM 重写)    │
   └─────────────────┘
```

### Voyager 的关键结果

- 3.3x **更多**独特物品
- 2.3x **更长**的旅行距离
- **快 15.3x** 解锁关键技术树里程碑
- **可迁移**：在新 Minecraft 世界，技能库立即可用

> **关键点**：Voyager 的核心贡献是"技能库 = Agent 的**可执行记忆**"——技能不是"知道什么"，而是"会做什么"。

> **复述框 · 13.3 节要点**
>
> - **Voyager = 自动课程 + 技能库 + 迭代提示**。
> - **核心结果**：3.3x unique items，15.3x 解锁关键技术树。
> - **关键洞察**：技能 = 可执行记忆 = 操作形态 T 的自修改。

## 13.4 AFlow：工作流自动进化

**AFlow** 由 Zhang 等人 2024 年 10 月提出，把 Agent 的"工作流"（节点+边的图）作为可优化对象。AFlow 的核心思想是**把工作流视为代码，用 MCTS 搜索最优结构**。

### AFlow 的工作流表示

```
   ┌─────────┐     ┌──────────┐     ┌──────────┐
   │ 节点 1   │────>│  节点 2   │────>│  节点 3   │
   │ (LLM 1) │     │ (LLM 2)  │     │ (LLM 3)  │
   └─────────┘     └──────────┘     └──────────┘
       │                              ▲
       └──────────────────────────────┘
              (循环边)
```

每个节点是 LLM 调用，边是数据流。

### AFlow 的 MCTS 优化

```
   ┌────────────────────────────────────────────────────────────┐
   │  MCTS 搜索:                                                 │
   │    - 节点: 工作流结构 (节点类型 + 边)                       │
   │    - 动作: 添加节点 / 删除节点 / 改变边 / 改变 prompt       │
   │    - 评估: 在验证集上跑工作流, 计算任务准确率              │
   │    - 选择: UCB 公式选择最有希望的修改                      │
   └────────────────────────────────────────────────────────────┘
```

AFlow 在多任务上达到了平均 +10-15% 的提升，样本效率优于直接 MCTS（因为工作流是结构化搜索空间）。

> **复述框 · 13.4 节要点**
>
> - **AFlow = 工作流 + MCTS**：把 Agent 编排视为代码搜索。
> - **核心结果**：多任务平均 +10-15%。
> - **关键洞察**：工作流结构是 T 的"宏观形态"。

## 13.5 EvoAgent：多 Agent 系统自动生成

**EvoAgent** 由 Yuan 等人 2025 年 4 月提出，把"多 Agent 系统"本身作为进化对象。EvoAgent 的核心思想是**用进化算法生成整个多 Agent 协作结构**。

### EvoAgent 的进化过程

```
   单 Agent
   ┌─────────┐
   │ Agent 1 │
   └─────────┘
        │
        │ 突变: 拆分为两个 Agent
        ▼
   两 Agent
   ┌─────────┐     ┌─────────┐
   │ Agent 1 │ ──> │ Agent 2 │
   └─────────┘     └─────────┘
        │
        │ 突变: 添加协调 Agent
        ▼
   三 Agent
   ┌─────────┐     ┌──────────┐     ┌─────────┐
   │ Worker  │ ──> │ Coordinator │ <──│ Worker   │
   │ Agent 1 │     │   Agent   │     │ Agent 2 │
   └─────────┘     └──────────┘     └─────────┘
```

EvoAgent 用进化算子（mutation / crossover / selection）生成多 Agent 结构，每个结构在测试集上评估 fitness，选择最优结构继续进化。

EvoAgent 在多 Agent 任务上达到了 +20% 的提升。它的关键创新是**多 Agent 结构本身是 T 的"超级形态"**——T 是工具集，EvoAgent 改的是"工具集如何被组织"。

> **复述框 · 13.5 节要点**
>
> - **EvoAgent = 多 Agent 进化**：用进化算法生成整个多 Agent 协作结构。
> - **核心结果**：多 Agent 任务 +20%。
> - **关键洞察**：多 Agent 结构 = T 的"超级形态"。

## 13.6 AlphaEvolve：整个代码库作为进化对象

**AlphaEvolve** 由 Google DeepMind 2025 年 5 月发布，是 LATM 思想在"整个代码库"层面的扩展 [r-paper-019](../../research/r-paper-019-alphaevolve2025.md)。AlphaEvolve 不只是让 LLM 写单个工具，而是让 LLM 进化**整个代码库**——可以是数学算法、TPU 调度、机器学习训练循环等。

### AlphaEvolve 的进化循环

```
   ┌──────────────────────────────────────────────────────────────┐
   │  1. 当前代码库 → 提取可独立评测的子程序                      │
   │  2. 让 LLM 生成该子程序的"变体"                              │
   │  3. 用自动化评估器评测每个变体                                │
   │  4. 选择最优变体替换原子程序                                  │
   │  5. 回到步骤 1, 继续下一轮                                  │
   └──────────────────────────────────────────────────────────────┘
```

### AlphaEvolve 的标志性结果

- **矩阵乘法**：发现 4×4 矩阵乘法的 49 次标量乘法新算法（53 年来首次改进）
- **TPU 电路设计**：为 TPU 设计新电路，效率提升
- **数据中心调度**：优化 Google 数据中心调度，节省 0.7% 计算资源
- **数学发现**：与陶哲轩合作发现新的数学构造

> **关键点**：AlphaEvolve 把"代码库"视为"巨型可进化对象"——这是 T 自修改的极限形式。

> **复述框 · 13.6 节要点**
>
> - **AlphaEvolve = 代码库进化**：整个代码库是可进化对象。
> - **核心结果**：4×4 矩阵乘法新算法、TPU 电路设计、数据中心调度。
> - **关键洞察**：代码库 = 极限形态学。

## 13.7 工具生命周期治理

T 自修改带来一个工程问题：**工具的生命周期管理**。一个工具从"创建"到"淘汰"经历哪些阶段？每个阶段如何治理？

### 图 13.4 · 工具生命周期的 5 个阶段

```
   ┌────────┐    ┌────────┐    ┌─────────┐    ┌────────┐    ┌────────┐
   │ 创建   │───>│ 测试   │───>│ 部署    │───>│ 监控   │───>│ 淘汰   │
   │ Create │    │ Test   │    │ Deploy  │    │ Monitor│    │ Retire │
   └────────┘    └────────┘    └─────────┘    └────────┘    └────────┘
       │             │              │              │              │
       ▼             ▼              ▼              ▼              ▼
   LLM 生成      沙箱测试     注入工具池     统计调用      删除并
   Python 代码   功能 + 性能  供 Agent 调用  成功率/延迟   标记为 deprecated
```

### 表 13.2 · 工具生命周期的 5 个阶段与治理

| 阶段 | 关键治理 | 防护工具 |
|---|---|---|
| **创建** | LLM 生成的代码不能有安全漏洞 | 静态代码扫描 + 类型检查 |
| **测试** | 工具必须在沙箱中通过功能与性能测试 | 沙箱环境 + 单元测试 |
| **部署** | 工具必须通过版本控制 + 签名校验 | git + 哈希校验 |
| **监控** | 工具的调用成功率、延迟、成本必须可观测 | OpenTelemetry + 告警 |
| **淘汰** | 工具被淘汰时必须保留历史记录 | 软删除 + git tag |

### 工具治理的 4 个关键设计原则

1. **版本化**：每个工具版本都有唯一的 hash 和 changelog
2. **沙箱化**：新工具先在沙箱中测试，不直接进入生产
3. **可回滚**：发现问题的工具可以一键回滚到上一版本
4. **可审计**：每个工具的创建、修改、调用都有完整日志

> **复述框 · 13.7 节要点**
>
> - **工具生命周期**：创建 → 测试 → 部署 → 监控 → 淘汰。
> - **4 个设计原则**：版本化、沙箱化、可回滚、可审计。
> - **关键洞察**：T 自修改 = 工具生命周期的"持续循环"。

## 13.8 H1 的第二个验证案例

H1（结构可塑性）的第一个验证案例是 P 自修改（Ch 12），第二个是 T 自修改。

### H1 在 T 自修改中的形式化

- **\(B_t = T_t\)**：操作形态只有 Tool 一个组件
- **\(U\)**：LATM / Voyager / AFlow / EvoAgent / AlphaEvolve 中的任何一个
- **\(E\)**：环境（任务分布 + API 集）
- **\(R\)**：适应后悔值

**预测**：当 \(E\) 变化时，**T 自修改 Agent** 的 \(R(B_{\text{adaptive}})\) 显著低于 **T 固定 Agent** 的 \(R(B_{\text{fixed}})\)。

### 验证设计

| 实验组 | T 是否修改 | 元控制器 |
|---|---|---|
| Frozen-T | ❌ 固定工具集 | 无 |
| LATM | ✅ Tool Maker 持续工作 | 双 LLM |
| Voyager | ✅ 技能库持续增长 | 技能代码 |
| AFlow | ✅ 工作流结构搜索 | MCTS |
| EvoAgent | ✅ 多 Agent 结构进化 | 进化算法 |
| AlphaEvolve | ✅ 代码库级进化 | LLM 变体生成 |

每个实验组在 5 类环境变化（任务漂移、API 漂移等）下跑 100 任务，测量适应后悔值。

**预期结果**：

- Frozen-T 的后悔值随环境变化线性增加
- 5 类 T 自修改 Agent 的后悔值都低于 Frozen-T
- AlphaEvolve 可能在大型代码任务上表现最佳，LATM 可能在简单任务上表现最佳

### T 自修改 vs P 自修改的差异

| 维度 | P 自修改（Ch 12） | T 自修改（Ch 13） |
|---|---|---|
| 修改对象 | 自然语言字符串 | Python 代码 + JSON Schema |
| 修改粒度 | 词 → 段 | 函数 → 工作流 → 代码库 |
| 评估难度 | 简单（任务准确率） | 中等（功能 + 性能测试） |
| 安全风险 | 中（提示注入） | 高（任意代码执行） |
| 扩展能力 | 调优指令 | 扩展能力 |
| H1 验证位置 | 第一个验证（最简） | 第二个验证（更强） |

> **复述框 · 13.8 节要点**
>
> - **H1 在 T 自修改中的形式化**：\(B_t = T_t\)，元控制器是 LATM / Voyager / AFlow / EvoAgent / AlphaEvolve。
> - **验证设计**：6 个实验组 × 5 类环境 × 100 任务 = 300 个单元格。
> - **T vs P**：T 自修改比 P 自修改更强，但风险也更高。

## 13.9 本章小结与第 14 章预告

本章是 Part III 的第 2 章。**T 自修改是 H1 的第二个验证案例**。**LATM** 用双 LLM 分工降低 95% 成本。**Voyager** 用技能库实现 Minecraft 3.3x unique items。**AFlow** 用 MCTS 搜索工作流结构。**EvoAgent** 用进化算法生成多 Agent 系统。**AlphaEvolve** 把整个代码库作为进化对象。**工具生命周期**的 5 个阶段 + 4 个治理原则保证 T 修改是安全的。

> **常见误区**
>
> - ❌ **把 T 自修改当作"自动写代码"**：T 自修改不只是"写代码"，是"创建/测试/部署/监控/淘汰"的完整生命周期。
> - ❌ **忽视沙箱化**：新工具必须先在沙箱中测试，不能直接进入生产。
> - ❌ **把所有 T 修改都当作"自进化"**：T 修改必须让 Agent 更好才算自进化，否则只是浪费资源。
> - ❌ **把 AlphaEvolve 当作万能解**：AlphaEvolve 只适用于有明确"评测函数"的任务。
> - ❌ **忽视 EvoAgent 的"超级形态"风险**：多 Agent 结构变化可能引入不可预测的交互行为。

第 14 章将进入**自适应记忆结构**。P 自修改和 T 自修改是 H1 的前两个案例，**M 自修改是第三个案例**——让 Agent 自主调整记忆的 schema、索引、检索策略。A-MEM、O-Mem、Mem0 等工作如何让 Agent 拥有"修改自身记忆"的能力？这是 Ch 14 的核心议题。

---

## 延伸阅读 / 推荐笔记

本章相关的研究笔记（按相关性排序）：

- [r-paper-018](../../research/r-paper-018-cai2023latm.md) — LATM：工具制造者与工具使用者的分工
- [r-paper-017](../../research/r-paper-017-wang2023voyager.md) — Voyager：持续增长的可执行技能库
- [r-paper-003](../../research/r-paper-003-schick2023toolformer.md) — Toolformer：模型自监督学习工具调用
- [r-paper-019](../../research/r-paper-019-alphaevolve2025.md) — AlphaEvolve：代码库级进化
- [r-note-012](../../research/r-note-012-tool-calling-three-layers.md) — 工具调用的能力、接口与执行三层结构
- [r-note-002](../../research/r-note-002-h1-structural-plasticity.md) — T 自修改的结构可塑性验证
- [r-note-004](../../research/r-note-004-self-modifying-agent-safety.md) — 工具创建、测试与部署的安全治理

## 本章小结

- **操作形态学的第二个应用**：修改 T（比 P 更强，但风险也更高）。
- **LATM**：Tool Maker + Tool User，成本降 95%。
- **Voyager**：技能库增长，3.3x unique items，15.3x 技术树。
- **AFlow**：MCTS 搜索工作流结构，多任务 +10-15%。
- **EvoAgent**：进化算法生成多 Agent 系统，+20%。
- **AlphaEvolve**：整个代码库作为进化对象。
- **工具生命周期**：创建 → 测试 → 部署 → 监控 → 淘汰。
- **4 个治理原则**：版本化、沙箱化、可回滚、可审计。
- **H1 的第二个验证案例**：T 自修改。

## 推荐阅读

- 📖 **LATM 原始论文** [Cai et al., 2023]：Tool Maker + Tool User 双 LLM 范式。[$TRAE_REF](https://arxiv.org/abs/2305.17126)
- 📖 **Voyager 原始论文** [Wang et al., 2023]：技能库 + 自动课程的 Minecraft 终身学习。[$TRAE_REF](https://arxiv.org/abs/2305.16291)
- 📖 **AFlow 原始论文** [Zhang et al., 2024]：MCTS 搜索 Agent 工作流。[$TRAE_REF](https://arxiv.org/abs/2410.10762)
- 📖 **EvoAgent 原始论文** [Yuan et al., 2025]：进化算法生成多 Agent 系统。[$TRAE_REF](https://arxiv.org/abs/2406.14228)
- 📖 **AlphaEvolve 官方博客** [DeepMind, 2025]：整个代码库作为进化对象。

## 练习题

1. **设计题**：为一个"数据分析 Agent"设计 LATM 工具库：哪些任务适合用强 LLM 写工具？哪些任务适合用便宜 LLM 调用？给出具体工具列表。
2. **分析题**：选一个真实 Agent 系统（ChatGPT、AutoGPT、Cursor），分析它的工具集是"固定"还是"可扩展"？是否支持 LATM 范式？
3. **动手题**：用 Python 实现一个简化版 LATM（不超过 150 行）：Tool Maker 用 GPT-4，Tool User 用本地 LLM。给定 10 个数学任务。
4. **设计题**：为 Voyager 风格的"技能库增长"设计治理机制：技能达到什么条件才能入库？技能出现 bug 怎么处理？技能如何版本化？
5. **批判题**：EvoAgent 让"多 Agent 结构"自进化——这是否会让 Agent 行为变得不可预测？如何治理？
6. **工程题**：设计 AlphaEvolve 风格的"代码库级 T 自修改"系统的安全护栏：代码沙箱、版本控制、回滚机制、人类审核。

## 参考文献（本章内）

1. Cai, T., et al. (2023). *Large Language Models as Tool Makers (LATM)*. arXiv:2305.17126. [$TRAE_REF](https://arxiv.org/abs/2305.17126)
2. Wang, G., et al. (2023). *Voyager: An Open-Ended Embodied Agent with Large Language Models*. arXiv:2305.16291. [$TRAE_REF](https://arxiv.org/abs/2305.16291)
3. Zhang, J., et al. (2024). *AFlow: Automating Agentic Workflow Generation*. arXiv:2410.10762. [$TRAE_REF](https://arxiv.org/abs/2410.10762)
4. Yuan, S., et al. (2025). *EvoAgent: Towards Automatic Multi-Agent Generation via Evolutionary Algorithms*. NAACL. [$TRAE_REF](https://arxiv.org/abs/2406.14228)
5. DeepMind. (2025). *AlphaEvolve: A Coding Agent for Scientific and Algorithmic Discovery*. [Google Blog](https://deepmind.google/discover/blog/alphaevolve-a-coding-agent-for-scientific-and-algorithmic-discovery/).
6. Qian, C., et al. (2023). *ToolLLM: Facilitating Large Language Models to Master 4000+ Real-world APIs*. arXiv:2307.16789. [$TRAE_REF](https://arxiv.org/abs/2307.16789)
7. Patil, S. G., et al. (2023). *Gorilla: Large Language Model Connected with Massive APIs*. arXiv:2305.15334. [$TRAE_REF](https://arxiv.org/abs/2305.15334)
8. Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407. [$TRAE_REF](https://arxiv.org/abs/2508.07407)
9. Sumers, T. R., et al. (2023). *CoALA: Cognitive Architectures for Language Agents*. arXiv:2309.02427. [$TRAE_REF](https://arxiv.org/abs/2309.02427)
10. Wang, X., et al. (2024). *CodeAct: Executable Code Actions Elicit Better LLM Agents*. ICLR. [$TRAE_REF](https://arxiv.org/abs/2402.01030)

---

> **本章进度**：13.1–13.9 节全部完成（约 6,500 字，含 4 张图 + 2 张表 + 10 篇引用 + 6 题 + 5 误区 + 5 推荐），达到 28 页计划。`status: final`。
>
> **Part III 进度**：2/6 章完结（Ch 12, 13）。下一章是 Ch 14 **自适应记忆结构**。
