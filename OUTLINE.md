# 操作形态学：自修改 LLM 智能体的具身认知 — 全书大纲（25 章 × 800 页）

> 英文书名：*Operational Morphology: The Embodied Cognition of Self-Modifying LLM Agents*
> 目标页数：800 ± 30 页（标准研究生用教科书）
> 出版模式：先 Leanpub / Jupyter Book，再 MIT Press
> 许可证：CC-BY-NC-SA 4.0（开源 + 印刷版）
> 仓库主页：`README.md`

## 全书结构总览

| Part | 标题 | 章数 | 起始章 | 起始页 | 页数 |
|---|---|---|---|---|---|
| I | 基础：LLM 智能体 | 6 | 1 | 1 | 140 |
| II | 具身认知与计算形态学 | 5 | 7 | 141 | 130 |
| III | 自进化系统 | 6 | 12 | 271 | 160 |
| IV | 系统实现 | 4 | 18 | 431 | 120 |
| V | 治理、伦理与未来 | 4 | 22 | 551 | 100 |
| VI | 附录 | 6 | A | 651 | 150 |

---

## Part I · 基础：LLM 智能体（140 页）

### 第 1 章 · LLM 智能体时代（16 页）

- **学习目标**：(1) 区分 LLM 与 LLM Agent；(2) 解释「代码即行动」的范式转变；(3) 描述自进化 Agent 与固定 Agent 的边界
- **核心知识点**：LLM、Agent、Tool Use、Reflection、Memory；ReAct、Reflexion、AutoGPT、BabyAGI
- **配图清单**：(1.1) LLM 与 Agent 边界图；(1.2) 工具调用时序图；(1.3) 智能体能力层级金字塔
- **章末练习**：5 题（其中 1 题动手调用 OpenAI Function Calling）

### 第 2 章 · 智能体基础（22 页）

- **学习目标**：(1) 把 Agent 拆成感知-决策-行动-反馈环；(2) 用控制论视角解释 Agent；(3) 与强化学习基本概念对齐
- **核心知识点**：感知、行动、反馈、控制论、POMDP、partial observability
- **配图清单**：(2.1) Agent 四元组结构图；(2.2) 与 POMDP 对应图；(2.3) 反馈环分类
- **常见误区**：把 LLM 当「世界模型」
- **章末练习**：6 题

### 第 3 章 · 工具与函数调用（22 页）

- **学习目标**：(1) 设计工具签名；(2) 处理 JSON Schema 验证；(3) 实现错误恢复
- **核心知识点**：OpenAI Function Calling、Toolformer、JSON Schema、错误传播
- **配图清单**：(3.1) Function Calling 协议栈；(3.2) 错误恢复决策树；(3.3) 工具描述质量雷达图
- **章末练习**：5 题 + 1 个动手实现小工具

### 第 4 章 · 提示词工程：从静态到动态（22 页）

- **学习目标**：(1) 区分静态 prompt 与可优化 prompt；(2) 跑通 OPRO、DSPy、PromptAgent 三种范式；(3) 评估 prompt 优化效果
- **核心知识点**：APE、OPRO、DSPy、PromptAgent、PromptBreeder、meta-prompt
- **配图清单**：(4.1) 静态 vs 动态 prompt 时间线；(4.2) OPRO 迭代搜索图；(4.3) DSPy 编译流水线
- **常见误区**：把 prompt 优化等同于超参数搜索
- **章末练习**：5 题 + 1 题用 DSPy 实现 GSM8K 优化

### 第 5 章 · 上下文工程与短期记忆（22 页）

- **学习目标**：(1) 计算 token 预算；(2) 压缩长上下文；(3) 实现 chunking 与分层摘要
- **核心知识点**：token 预算、压缩算法、LongLLMLingua、chunking、摘要
- **配图清单**：(5.1) 上下文压缩栈；(5.2) chunking 与检索融合示意图
- **章末练习**：5 题

### 第 6 章 · 长期记忆与检索增强（36 页）

- **学习目标**：(1) 区分事实、经验、工作三类记忆；(2) 实现 MemGPT 风格分层记忆；(3) 选合适评测（LoCoMo、PERSONAMEM）
- **核心知识点**：MemGPT、MemoryBank、ReadAgent、A-MEM、O-Mem、Mem0、时序 KG、HIPPO 风格
- **配图清单**：(6.1) 三类记忆金字塔；(6.2) MemGPT 换页示意；(6.3) A-MEM Zettelkasten 链接图；(6.4) 长期记忆评测雷达
- **章末练习**：6 题 + 1 题实现 A-MEM 风格记忆系统

---

## Part II · 具身认知与计算形态学（130 页）

### 第 7 章 · 4E Cognition 简史（26 页）

- **学习目标**：(1) 区分 Embodied / Embedded / Enacted / Extended；(2) 解释 Gibson、Clark、Chemero、Newen 四代谱系；(3) 评估「4E」是否可被实证
- **核心知识点**：Gibson affordance、Clark scaffolded cognition、Chemero radical embodied、Newen handbook
- **配图清单**：(7.1) 4E 谱系图；(7.2) Gibson affordance 与工具融合
- **章末练习**：5 题

### 第 8 章 · Enactivism 与自创生（26 页）

- **学习目标**：(1) 复述 Varela/Thompson/Rosch enaction 命题；(2) 比较 autopoietic vs sensorimotor enactivism；(3) 评价 Hutto & Myin 激进生成论
- **核心知识点**：autopoiesis、enaction、sense-making、autopoietic enactivism、sensorimotor enactivism、radical enactivism
- **配图清单**：(8.1) 自创生闭环；(8.2) enaction 三代谱系；(8.3) sense-making 边界
- **章末练习**：5 题

### 第 9 章 · Extended Mind 与延展认知（26 页）

- **学习目标**：(1) 复述 parity principle；(2) 复述 Adams & Aizawa 反例；(3) 评价「工具何时算身体」
- **核心知识点**：parity principle、coupled-system hypothesis、non-derived content、cognitive bloatware、Heersmink 分类、Menary 三联表示
- **配图清单**：(9.1) Otto/Inga 对比；(9.2) parity principle 决策树；(9.3) 认知人工物层级
- **常见误区**：把「使用工具」等同于「延展身体」
- **章末练习**：6 题

### 第 10 章 · 具身 AI 与机器人认知（26 页）

- **学习目标**：(1) 复述 Brooks subsumption；(2) 解释 Pfeifer「形态决定智能」；(3) 评估 embodied foundation models
- **核心知识点**：subsumption、Pfeifer morphology、Soft Robotics、PaLM-E、RT-2、Octo、π₀
- **配图清单**：(10.1) subsumption 层级；(10.2) 形态决定智能示意；(10.3) embodied foundation model 时间线
- **章末练习**：5 题

### 第 11 章 · 当工具成为身体：操作形态假说（26 页）

- **学习目标**：(1) 给出操作形态的形式化定义；(2) 与第 8、9 章区分；(3) 提出可证伪假说
- **核心知识点**：Operational Morphology、可写形态层 \(B=\{P,T,M,C\}\)、元控制器 \(U\)、Structural Plasticity
- **配图清单**：(11.1) Agent 闭环大图；(11.2) \(B\) 的可写形态示意；(11.3) 元控制器 U 的输入输出
- **常见误区**：把 prompt 优化当成具身
- **章末练习**：6 题

---

## Part III · 自进化系统（160 页）

### 第 12 章 · 自修改提示词（24 页）

- **学习目标**：(1) 跑通 OPRO、PE2、PromptAgent；(2) 评估自修改 prompt 的安全性
- **核心知识点**：OPRO、PE2、PromptAgent、PromptBreeder、EvoPrompt、CoALA、反思式 meta-prompt
- **配图清单**：(12.1) 提示词自修改时间线；(12.2) 反思式元提示词决策图
- **章末练习**：5 题 + 1 题复现 OPRO

### 第 13 章 · 自动工具创建与重构（28 页）

- **学习目标**：(1) 实现 LATM 闭环；(2) 实现 Voyager 技能库；(3) 设计工具生命周期治理
- **核心知识点**：Toolformer、LATM、Voyager、AlphaEvolve、MUSE-Autoskill、AFlow、EvoAgent、CRITIC
- **配图清单**：(13.1) 工具创建流水线；(13.2) 技能库依赖图；(13.3) AlphaEvolve 进化循环
- **章末练习**：6 题

### 第 14 章 · 自适应记忆结构（30 页）

- **学习目标**：(1) 实现 Zettelkasten 风格记忆；(2) 实现 schema 自适应；(3) 处理记忆冲突与遗忘
- **核心知识点**：MemGPT、MemoryBank、A-MEM、O-Mem、Mem0、LangMem、参数化记忆、LoRA 记忆
- **配图清单**：(14.1) A-MEM 动态链接图；(14.2) 记忆 schema 自适应示意；(14.3) 参数化记忆 vs 外部记忆
- **章末练习**：6 题

### 第 15 章 · 自我改写代码（30 页）

- **学习目标**：(1) 实现 SICA 风格的代码自修改；(2) 设计沙箱；(3) 评估安全性
- **核心知识点**：Self-Debug、Self-Repair、CodeAct、SICA、Gödel Agent、AlphaEvolve、Darwin Gödel Machine
- **配图清单**：(15.1) SICA 编辑自身系统代码示意；(15.2) 沙箱策略对比；(15.3) Gödel Agent 递归自改进
- **常见误区**：忽视 Gödel 机器的「证明改后更好」要求
- **章末练习**：6 题

### 第 16 章 · 协同自进化：跨组件耦合（24 页）

- **学习目标**：(1) 描述四元反馈环；(2) 设计 Joint-independent vs Joint-coordinated；(3) 量化协同收益
- **核心知识点**：Self-Evolving Agents Survey、Memory in the Age of AI Agents、跨组件耦合、协同效应
- **配图清单**：(16.1) 四元反馈环大图；(16.2) 协同 vs 独立收益曲线
- **章末练习**：5 题

### 第 17 章 · 元控制器设计（24 页）

- **学习目标**：(1) 选择合适的元控制器（MCMC / 进化 / 贝叶斯）；(2) 设计人类反馈回路；(3) 评估收敛速度
- **核心知识点**：MCTS、进化算法、贝叶斯优化、人类反馈、安全约束集、版本化
- **配图清单**：(17.1) 元控制器三种实现对比；(17.2) 人类反馈回路
- **章末练习**：5 题

---

## Part IV · 系统实现（120 页）

### 第 18 章 · MorphAgent 参考实现（30 页）

- **学习目标**：(1) 跑通端到端系统；(2) 部署到本地与云端；(3) 用 OpenTelemetry 追踪
- **核心知识点**：参考实现、代码骨架、Prompt Engine、Tool Manager、Memory Store、Code Sandbox、Meta Controller
- **配图清单**：(18.1) MorphAgent 系统架构图；(18.2) 五大子系统时序；(18.3) 部署拓扑
- **章末练习**：5 题 + 1 题完整部署

### 第 19 章 · 评测方法学（28 页）

- **学习目标**：(1) 区分任务级 vs 形态级评测；(2) 跑 SWE-bench、MLE-bench、GAIA；(3) 设计 MorphBench
- **核心知识点**：SWE-bench、MLE-bench、GAIA、WebArena、AgentBench、MLAgentBench、MorphBench
- **配图清单**：(19.1) 评测分类矩阵；(19.2) MorphBench 五类干预
- **章末练习**：6 题

### 第 20 章 · 调试与可观测性（30 页）

- **学习目标**：(1) 设计修改因果归因；(2) 用 Langfuse / OpenTelemetry；(3) 实现轨迹回放
- **核心知识点**：trace、span、因果归因、反事实干预、可观测性、轨迹回放
- **配图清单**：(20.1) trace 模型；(20.2) 因果归因决策树
- **章末练习**：5 题

### 第 21 章 · 部署与运维（32 页）

- **学习目标**：(1) 设计灰度与影子流量；(2) 设定 SLO；(3) 实现一键回滚
- **核心知识点**：灰度发布、影子流量、SLO、回滚、配置管理、密钥管理
- **配图清单**：(21.1) 灰度发布曲线；(21.2) SLO 监控面板；(21.3) 回滚决策树
- **章末练习**：6 题

---

## Part V · 治理、伦理与未来（100 页）

### 第 22 章 · 安全性与对抗鲁棒性（28 页）

- **学习目标**：(1) 列出 5 类自修改安全威胁；(2) 设计 prompt 注入防御；(3) 评估修改失控
- **核心知识点**：prompt injection、tool 越权、自改失控、形式化验证、SMT solver、灰度回滚
- **配图清单**：(22.1) 安全威胁分类；(22.2) 攻击树；(22.3) 防御层次
- **章末练习**：6 题

### 第 23 章 · 可验证自改（24 页）

- **学习目标**：(1) 复述 Gödel 机器思想；(2) 集成 SMT solver；(3) 设计可证明改进流程
- **核心知识点**：Gödel 机器、SMT、形式化验证、可证明改进、可验证智能体
- **配图清单**：(23.1) Gödel 机器流程；(23.2) SMT 验证管线
- **章末练习**：5 题

### 第 24 章 · 经济、伦理与社会影响（24 页）

- **学习目标**：(1) 评估责任归属；(2) 分析知识产权；(3) 评估就业影响
- **核心知识点**：责任归属、知识产权、就业影响、AI 治理框架
- **配图清单**：(24.1) 责任归属矩阵；(24.2) 治理框架图
- **章末练习**：5 题

### 第 25 章 · 开放问题与未来工作（24 页）

- **学习目标**：(1) 列出 10 个开放问题；(2) 给出跨学科研究议程；(3) 描述 5 年展望
- **核心知识点**：跨组件协同、参数化记忆、可解释性、人机协同自改、跨域迁移
- **配图清单**：(25.1) 开放问题矩阵；(25.2) 跨学科研究议程
- **章末练习**：5 题

---

## Part VI · 附录（150 页）

### 附录 A · 术语表（中英对照，24 页）

- 收录全书所有核心术语，配英文/拉丁文/拼音三栏
- 按 Part 分组
- 配套索引页

### 附录 B · 数学基础（30 页）

- 概率论、最优化、信息论、控制论基础
- 每节配 3 个练习题

### 附录 C · 工具与库速查（28 页）

- DSPy、LangGraph、MemGPT、A-MEM、AgentBench、SWE-bench、MLE-bench
- 每个工具配最小可运行示例

### 附录 D · 教学实验清单（28 页）

- 30 个分章节的实验，含评分标准

### 附录 E · 练习题答案（24 页）

- 每章练习题答案 + 评分标准

### 附录 F · 参考文献（16 页）

- 按章节分组的关键文献
- 每篇配 1–2 句「为什么读这篇」

---

## 与原始 100 页框架的映射

| 100 页框架章节 | 教科书对应 |
|---|---|
| 第 1 章 选题立场 | Part I 第 1 章 + Part II 第 11 章 |
| 第 2 章 4E 与 Enactivism | Part II 第 7–10 章 |
| 第 3 章 文献矩阵 | Part III 第 12–16 章 |
| 第 4 章 形式化 | Part II 第 11 章 + Part III 第 17 章 |
| 第 5 章 系统 | Part IV 第 18 章 |
| 第 6 章 Benchmark | Part IV 第 19 章 |
| 第 7 章 实验 | Part IV 第 19 章末尾 + 附录 D |
| 第 8 章 安全 | Part V 第 22–23 章 |
| 第 9 章 讨论 | Part V 第 25 章 |
| 第 10 章 局限 | Part V 第 25 章 + 附录 D |
