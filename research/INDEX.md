# 研究索引

> 用途：所有研究笔记的元数据索引，作为研究进度仪表盘。
> 维护规则：每写一篇笔记，添加一行；状态改变时更新。

## 笔记清单

> 命名规范：`r-note-{number}-{slug}.md`、`r-paper-{number}-{slug}.md`、`r-exp-{number}-{slug}.md`、`r-debate-{number}-{slug}.md`

### 概念笔记（Concept Note）

| ID | 标题 | 状态 | 字数 | 相关章节 |
|---|---|---|---|---|
| **r-note-001** | **操作形态学的形式化定义** | **final** | **~3,000** | **Ch 11, 16, 17** |
| **r-note-002** | **H1 假说的实证路径：结构可塑性** | **draft** | **~800** | **Ch 11, 12, 19** |
| **r-note-003** | **P/T/M/C 协同进化的理论框架** | **draft** | **~800** | **Ch 11, 16, 19** |
| **r-note-004** | **自修改 Agent 的安全性约束：形式化分析** | **draft** | **~800** | **Ch 11, 22, 23** |
| **r-note-005** | **生态效度：从实验室到生产环境** | **draft** | **~800** | **Ch 19, 11, 21** |
| **r-note-006** | **迁移学习在自修改 Agent 中的应用** | **draft** | **~800** | **Ch 11, 12, 16, 19** |
| **r-note-007** | **治理必要性假说的最小可行框架** | **draft** | **~800** | **Ch 11, 22, 23, 24** |
| **r-note-008** | **操作形态景观：B 空间的拓扑分析** | **draft** | **~800** | **Ch 11, 16, 17** |
| **r-note-009** | **Agent 能力等级 L0-L5 的形式化定义** | **draft** | **~800** | **Ch 11, 18, 22** |
| **r-note-010** | **5 年路线图：从 MorphAgent v1.0 到 AGI 就绪** | **draft** | **~800** | **Ch 18, 25** |
| (待写) | POMDP 与 LLM Agent 的对应 | idea | 0 | Ch 2 |
| (待写) | 工具调用的三层结构 | idea | 0 | Ch 3 |

### 论文笔记（Paper Note）

| ID | 标题 | 状态 | 字数 | bib-key |
|---|---|---|---|---|
| (待写) | ReAct 原始论文 | idea | 0 | yao2023react |
| (待写) | Reflexion 原始论文 | idea | 0 | shinn2023reflexion |
| (待写) | Toolformer 原始论文 | idea | 0 | schick2023toolformer |
| (待写) | MemGPT 原始论文 | idea | 0 | packer2023memgpt |
| (待写) | A-MEM 原始论文 | idea | 0 | xu2025amem |
| (待写) | SICA 原始论文 | idea | 0 | robeyns2025sica |
| (待写) | Gödel Agent 原始论文 | idea | 0 | yin2024godelagent |
| (待写) | OPRO 原始论文 | idea | 0 | yang2023opro |
| (待写) | Self-Evolving Agents 综述 | idea | 0 | fang2025selfevolving |
| (待写) | The Embodied Mind（Varela） | idea | 0 | varela1991embodied |
| (待写) | The Extended Mind（Clark & Chalmers） | idea | 0 | clark1998extended |
| (待写) | Intelligence Without Representation（Brooks） | idea | 0 | brooks1991intelligence |
| (待写) | SWE-bench 原始论文 | idea | 0 | jimenez2024swebench |
| (待写) | MLE-bench 原始论文 | idea | 0 | chan2024mlebench |

### 实验笔记（Experiment Note）

| ID | 标题 | 状态 | 字数 | 实验目录 |
|---|---|---|---|---|
| r-exp-001 | 基线对比 4 个 Agent | draft | 见 `exp-01-baseline/run.py` | exp-01-baseline |
| r-exp-002 | POMDP 信念状态验证 | draft | 见 `exp-02-pomdp-claim/run.py` | exp-02-pomdp-claim |
| r-exp-003 | 工具描述对调用准确率的影响 | draft | 见 `exp-03-tool-description/run.py` | exp-03-tool-description |
| r-exp-004 | 自修改 prompt vs 静态 prompt | draft | 见 `exp-04-self-modifying-prompt/run.py` | exp-04-self-modifying-prompt |
| r-exp-005 | 操作形态学的可证伪假设验证 | idea | 0 | (待建) |
| r-exp-006 | MorphBench 五类环境干预 | idea | 0 | (待建) |
| r-exp-007 | 跨组件协同自进化 | idea | 0 | (待建) |

### 争论笔记（Debate Note）

| ID | 主题 | 状态 | 字数 | 相关章节 |
|---|---|---|---|---|
| r-debate-001 | 工具何时成为身体 | idea | 0 | Ch 9, 11 |
| r-debate-002 | 自修改代码是否应被允许 | idea | 0 | Ch 15, 22 |
| r-debate-003 | 4E vs Radical Enactivism 的方法论分歧 | idea | 0 | Ch 8 |

## 状态图例

- `idea`：灵感阶段，尚未动笔
- `draft`：草稿阶段，已开始撰写
- `final`：定稿阶段，可被章节引用
- `abandoned`：放弃，移入 `_archive/`

## 进度统计

| 状态 | 笔记数 |
|---|---|
| idea | 18 |
| draft | 13 |
| **final** | **1** |
| abandoned | 0 |
| **总计** | **32** |

## 月度更新记录

- **2026-07-22**：初始化 INDEX，创建 4 个实验目录，编写 4 个实验骨架
- **2026-07-22**：完成 r-note-001（操作形态学形式化定义，~3,000 字，final）
- **2026-07-22**：创建 r-note-002（H1 结构可塑性实证路径）、r-note-003（P/T/M/C 协同进化框架）、r-note-004（自修改安全性形式化分析）、r-note-005（生态效度），各 ~800 字，draft
- **2026-07-22**：创建 r-note-006（形态迁移与迁移学习）、r-note-007（治理必要性最小框架）、r-note-008（操作形态景观拓扑分析）、r-note-009（L0-L5 等级形式化）、r-note-010（5 年路线图细化），各 ~800 字，draft
- (待续)
