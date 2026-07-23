---
note_id: r-note-013
title: 短期记忆 vs 长期记忆的形式化：上下文状态、外部存储与 M 自修改
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 5, Ch 6, Ch 14]
related_papers: [shinn2023reflexion, packer2023memgpt, xu2025amem, yao2023react, sumers2023coala, liu2023lost, r-note-001, r-note-004, r-note-009, r-note-011]
keywords: [short-term memory, long-term memory, context window, vector database, knowledge graph, paging, memory topology, M self-modification]
---

# r-note-013: 短期记忆 vs 长期记忆的形式化：上下文状态、外部存储与 M 自修改

> 短期记忆是当前决策可直接读取的有限工作集，长期记忆是跨步、跨 session 持久化但必须通过检索进入工作集的外部状态；M 自修改的核心不是“存更多”，而是学习何时编码、迁移、检索、合并与遗忘。

## 1. 核心命题

LLM Agent 的“记忆”经常被笼统地理解为聊天历史或向量数据库。这个定义混淆了两个计算性质完全不同的系统：**短期记忆（short-term memory, STM）**位于 context window 内，能被下一次 forward pass 直接读取；**长期记忆（long-term memory, LTM）**位于模型外部，具有持久性与近似无界容量，却只有在检索后才能影响当前决策。

二者的差异不是保存时间长短，而是**访问路径**：

\[
\text{STM}\xrightarrow{\text{direct attention}}\text{action},
\qquad
\text{LTM}\xrightarrow{\text{retrieve}}\text{STM}\xrightarrow{\text{attention}}\text{action}
\]

因此，LTM 中“存在”某条信息不等于 Agent “记得”它。只有当检索策略把相关条目 page-in 到 STM，并且模型能在上下文中正确使用它，记忆才成为行为因果链的一部分。反过来，STM 中的内容也不都应长期化：临时工具输出、失败猜测和不可信网页若无选择地写入 LTM，会把瞬时噪声固化为跨 session 污染。

从操作形态学看，M 不是一个容器，而是一组记忆算子：

\[
M=(M^S,M^L,E,R,K,F,V)
\]

其中 \(E\) 是编码（encode），\(R\) 是检索（retrieve），\(K\) 是巩固/合并（consolidate），\(F\) 是遗忘（forget），\(V\) 是验证与版本化（verify/version）。真正的 M 自修改既可以改变内容，也可以改变这些算子与拓扑。

## 2. 形式化

### 2.1 短期记忆

设模型 context budget 为 \(L\) tokens，短期记忆是时刻 \(t\) 可被模型直接访问的有序序列：

\[
M_t^S=(x_{t,1},\ldots,x_{t,n}),\qquad \sum_i\ell(x_{t,i})\le L
\]

其中条目可以是 system prompt、近期消息、tool observation、计划、检索结果与 scratch state。短期记忆更新为：

\[
M_{t+1}^S=G(M_t^S,o_{t+1},r_t;\rho_t)
\]

\(G\) 是 append、truncate、summarize、priority selection 的组合，\(\rho_t\) 是预算分配策略。朴素滑动窗口使用“最旧先删”，但它忽略信息价值。更合理的选择问题是有限容量 knapsack：

\[
\max_{X\subseteq\mathcal{C}_t}\sum_{x\in X}u_t(x)
\quad\text{s.t.}\quad\sum_{x\in X}\ell(x)\le L
\]

\(u_t(x)\) 由 relevance、recency、authority、uncertainty reduction 与 safety risk 共同决定。短期记忆的三个关键性质是：**低访问延迟、容量硬约束、随 prompt 重建而易失**。

### 2.2 长期记忆

长期记忆是外部持久存储：

\[
M_t^L=(D_t,\mathcal{I}_t,\mathcal{G}_t)
\]

- \(D_t\)：原始或结构化 memory records；
- \(\mathcal{I}_t\)：embedding、关键词、时间、实体等索引；
- \(\mathcal{G}_t\)：可选关系图，如实体边、时间边、因果边、矛盾边。

每条记录定义为：

\[
m_i=(c_i,z_i,p_i,\tau_i,q_i,v_i,\lambda_i)
\]

其中 \(c_i\) 为内容，\(z_i\) 为 embedding，\(p_i\) 为 provenance，\(\tau_i\) 为时间，\(q_i\) 为置信度，\(v_i\) 为版本，\(\lambda_i\) 为链接。检索不是简单 top-k：

\[
R(q,M^L)=\operatorname{TopK}_{m_i}\left[
\alpha\,sim(q,z_i)+\beta\,recency_i+\chi\,authority_i+
\delta\,graph_i-\eta\,risk_i
\right]
\]

检索结果 \(R_t\) 经过 re-ranking、去重、冲突标注和 token 压缩后进入 \(M_t^S\)。长期记忆的三个关键性质是：**持久、容量大、访问间接且依赖检索质量**。

### 2.3 两层记忆的迁移算子

两层系统需要四个基本迁移：

\[
\begin{aligned}
\text{page-in}:&\quad M^L\to M^S,\\
\text{page-out}:&\quad M^S\to M^L,\\
\text{consolidate}:&\quad \{m_i\}\to m^*,\\
\text{forget}:&\quad M^L\to M^L\setminus\{m_j\}.
\end{aligned}
\]

Page-out 不是复制全文，而是决定“什么值得持久化”。可定义写入门：

\[
W(m)=\mathbb{1}[u_{future}(m)-c_{store}(m)-r_{security}(m)>\tau]
\]

只有预期未来价值超过存储、检索噪声与安全风险时才写入。类似地，page-in 的目标不是找最相似文本，而是最大化当前行动价值：

\[
R^*=\arg\max_{R\subseteq M^L,\,\ell(R)\le B}
\mathbb{E}[Q(a\mid M^S\oplus R)]-c(R)
\]

这揭示了 vector similarity 的局限：语义相似只是价值的代理变量，不等于任务相关性，更不等于真实性。

### 2.4 记忆内容、结构与策略的三种自修改

| M 修改层级 | 形式 | 代表 | 操作形态意义 |
|---|---|---|---|
| 内容修改 | \(D_{t+1}=D_t\cup\{m\}\) | Reflexion（r-paper-002） | 写入反思或事实 |
| 位置/层级修改 | \((M^S,M^L)_{t+1}=G(\cdot)\) | MemGPT（r-paper-004） | page-in/page-out 与检索自管理 |
| 拓扑修改 | \(\mathcal{G}_{t+1}=\mathcal{G}_t\cup E_{new}\) | A-MEM（r-paper-005） | 创建 tags、categories、links |
| schema/策略修改 | \((E,R,K,F,V)_{t+1}=U_M(\cdot)\) | 未来 MorphAgent | 修改记忆字段、评分、生命周期 |

严格而言，追加一条文本是最弱的 M 自修改；改变检索与遗忘策略才会改变 Agent “能想起什么”；改变图结构与 schema 则会改变“知识如何组织”。

## 3. 方法细节

### 3.1 两层记忆控制器

```python
class TwoTierMemory:
    def __init__(self, token_budget, vector_store, graph_store):
        self.stm = []
        self.ltm = vector_store
        self.graph = graph_store
        self.token_budget = token_budget
        self.audit_log = []

    def observe(self, event):
        item = normalize(event, keep_provenance=True)
        self.stm.append(item)
        self.stm = budget_select(self.stm, self.token_budget)

    def recall(self, query, k=8):
        dense = self.ltm.search(embed(query), top_k=3*k)
        linked = self.graph.expand(dense, depth=1)
        candidates = deduplicate(dense + linked)
        checked = [verify_record(x) for x in candidates]
        return rerank(checked, query, top_k=k,
                      factors=["relevance", "authority", "recency", "risk"])

    def consolidate(self, episode_result):
        candidates = extract_claims(self.stm)
        for m in candidates:
            if should_persist(m, episode_result) and verify_record(m).ok:
                version = self.ltm.upsert(m)
                self.graph.link(version, infer_relations(version))
                self.audit_log.append(("write", version.id, version.source))

    def forget(self, policy):
        for record in self.ltm.scan():
            if policy.expired(record) or policy.revoked(record):
                self.ltm.tombstone(record.id)
```

此设计明确分离“观察进入 STM”“查询 LTM”“episode 后巩固”“按策略遗忘”。如果 LLM 可以直接调用这些函数，则它是 M 的局部元控制器；如果它还能改写 `should_persist`、reranker 或 graph link types，则进入更高等级的 M 结构自演化。

### 3.2 MemGPT：分页层级而非无限 context

r-paper-004 将 main context、external context 与 archival storage 类比为内存层级，并通过 function calling 让 LLM 自主 `core_memory_append`、`conversation_search`、`archival_memory_insert`。其贡献是把 LTM 的访问变为**Agent 主动系统调用**，不是固定 RAG pipeline。

但 OS 类比不能字面化：context window 没有地址空间、页表与确定性 cache miss；LLM 可能忘记检索、错误检索、过度检索。MemGPT 的三层 schema 也是冻结的，它能管理内容与位置，却不能自行添加“程序记忆层”或改变 retrieval algorithm。因此它是 M 自管理的代表，不是完整 schema 自修改。

### 3.3 A-MEM：从扁平检索到链接拓扑

r-paper-005 将 memory note 定义为内容、时间、tags、category、contextual description 与 links 的组合，并在写入时由 LLM 创建 causal、temporal、thematic、contradictory、supporting 等关系。检索结合 embedding 与 graph traversal，使“词面不相似但关系重要”的记忆也可被召回。

A-MEM 的核心价值不是向量库上再加元数据，而是让 \(\mathcal{G}_t\) 在线变化：

\[
\mathcal{G}_{t+1}=\mathcal{G}_t\cup\text{LLM-Link}(m_{new},R(m_{new}))
\]

代价是链接错误会放大检索污染。错误 hub、过密图、过期矛盾边与攻击性链接都会把一个坏记录传播到多个上下文。因而 link creation 必须有置信度、理由、版本和生命周期，而非永久追加。

### 3.4 具体实例：跨 session 编程助手

用户在 session A 说明“项目只能用 Python 3.10，禁止引入 pandas”；session B 要求修复数据解析。短期记忆只含当前 issue，长期记忆保存项目约束。正确流程是：

1. 识别当前任务涉及依赖与运行环境；
2. 以项目 ID、依赖约束、Python version 检索 LTM；
3. 把“Python 3.10 / no pandas”作为高 authority 条目 page-in；
4. 生成仅用标准库的 patch；
5. 测试通过后把“该项目 CSV 解析使用 `csv` module”写为带 provenance 的 procedural memory；
6. 若用户后来允许 pandas，不覆盖旧记录，而是新建版本并把旧约束标记 superseded。

朴素向量库可能因当前 query 未出现“pandas”而漏检；知识图谱可沿 `project -> dependency_policy` 关系召回。相反，如果旧偏好没有版本化，长期记忆会让 Agent 永久遵循过期约束。

### 3.5 设计权衡表

| 维度 | STM / context window | LTM / vector DB | LTM / knowledge graph |
|---|---|---|---|
| 访问方式 | direct attention | embedding retrieval | entity/relation traversal |
| 延迟 | 低但推理 token 成本高 | 中 | 中高 |
| 容量 | 硬上限 \(L\) | 大 | 大但维护成本高 |
| 顺序信息 | 强 | 弱，需 metadata | 可显式 temporal edge |
| 精确事实 | 受 context 干扰 | 取决于检索与原文 | 取决于抽取与 ontology |
| 跨主题关联 | 仅当前 context | 语义相似为主 | 图路径较强 |
| 更新 | 每轮重建 | upsert/delete | node/edge/version 更新 |
| 可解释性 | 高，可直接阅读 | 中，可查看 top-k | 高，可查看路径；但图可错 |
| 主要失败 | overflow、lost-in-the-middle | miss、false positive、stale item | bad links、hub、ontology drift |
| 攻击面 | prompt injection | memory poisoning | poisoning + link amplification |

最佳系统通常不是三选一，而是 STM + vector recall + selective graph。图不应用于所有内容；只有需要关系推理、冲突追踪和长期实体一致性的条目才值得进入 graph。

## 4. 与本书其他章节/笔记的关系

| 交叉引用 | 本笔记的作用 |
|---|---|
| Ch 5 | 把 context window 定义为有限、直接可访问的 STM |
| Ch 6 | 把 vector DB / KG 定义为需检索介入的 LTM |
| Ch 14 | 把 M 自修改分为内容、迁移、拓扑、schema 四级 |
| r-note-001 | 细化 \(B=\{P,T,M,C\}\) 中 M 的内部结构与算子 |
| r-note-003 | 指出 P 决定记忆规则、T 提供 memory calls、C 实现生命周期，M 不能孤立演化 |
| r-note-004 | 给 memory write、link creation 与 retrieval 增加 provenance、不变量和回滚 |
| r-note-006 | 区分迁移“记忆内容”与迁移“记忆策略/结构” |
| r-note-008 | M topology 是形态景观的一个离散—连续子空间 |
| r-note-009 | 记忆能力与修改权限共同决定 L0-L5，而非容量大小 |
| r-note-011 | STM 是 POMDP belief 的近似载体；LTM 是 belief update 的外部证据库 |
| r-paper-022 | CoALA 将 memory 作为认知架构组件，为多类型记忆提供更广分类 |

### L0-L5 定位

- **L0**：只有 episode 内 context；M 随会话结束而消失。
- **L1**：有外部检索，但 encode/retrieve policy 由开发者冻结。
- **L2**：单组件 M 可改，如 Reflexion 追加反思或 MemGPT 管理内容。
- **L3**：M 与 P/T/C 至少一个组件协同，例如调整 retrieval prompt 与 memory tool。
- **L4**：可修改 M 的结构、link topology、schema 或检索策略，并通过自动验证。
- **L5**：M 与 P/T/C 协同进化，治理等级 \(\gamma=3\)，高风险写入和 schema 变更需要审计。

需要强调：拥有 1TB vector store 不会自动把 Agent 提升到 L2。等级取决于 \(\mu_A\) 中是否包含 M 的运行时修改能力，以及 \(\gamma_A\) 是否支撑安全修改。

## 5. 局限与开放问题

### 5.1 “更长 context”不能消解层级

即使 context window 扩展到百万 tokens，attention 仍有成本与位置偏差；相关事实可能 lost in the middle；跨 session、访问控制、版本与删除仍需外部存储。更长 context 会移动 STM/LTM 边界，但不会取消外部记忆管理问题。

### 5.2 语义相似不等于因果相关

Embedding retrieval 擅长主题相似，却可能错过否定、数字、时间演化与间接约束。知识图谱可补足关系，但依赖 ontology 与关系抽取。混合检索的开放问题是：何时相信 dense score，何时沿 graph，如何校准两者冲突。

### 5.3 写入选择与真实性

用户说出的内容可能是假设、引用、讽刺或恶意注入。工具返回也可能错误。若所有对话都被“记住”，LTM 会成为未经审计的数据湖。应把事实、偏好、计划、反思、程序步骤分型，并为每类设置不同写入门与 TTL。

### 5.4 遗忘是功能而非缺陷

记忆研究常只优化 recall，忽视删除。隐私法规、用户撤回、事实过期、策略更新和噪声控制都要求遗忘。真正的 M 自修改必须能 tombstone、撤销链接、重建索引并证明已删除信息不再被召回。A-MEM 式只追加链接不足以解决生命周期。

### 5.5 评测中的因果混淆

增加 LTM 往往同时增加 prompt tokens、额外 LLM calls 与 hand-crafted retrieval logic。性能提升究竟来自“长期记忆”，还是来自更多计算预算？实验必须做 token/cost-matched baseline，并分别消融 encode、retrieve、graph、consolidate、forget。

### 5.6 记忆安全与身份边界

多用户 Agent 若没有 tenant isolation，检索可能跨用户泄露。Memory poisoning 还能跨 session 持续存在，并经 graph links 扩散。M 的每条记录必须绑定 owner、scope、source、consent、retention 和 access policy；否则“长期记忆”只是长期风险。

## 6. 对操作形态学的贡献与 H1-H5 映射

本笔记把 M 从单一存储组件重写为“有限工作集 + 持久外存 + 迁移/检索/巩固/遗忘/验证算子”。这使 M 自修改具备清晰的深度差异：改内容、改位置、改拓扑、改 schema 不是同一能力。它也说明 M 的性能不可脱离 P/T/C：P 给出记忆政策，T 暴露 memory operations，C 强制预算与权限，M 承载状态。记忆自演化天然是跨组件问题。

| 假设 | 本笔记的作用 | 可检验预测 |
|---|---|---|
| **H1 结构可塑性** | 可修改 encode/retrieve/topology 的 M 应优于固定窗口或固定 RAG | 长视野任务的 adaptation regret 与遗忘错误下降 |
| **H2 协同演化** | P/T/C 与 M 的策略必须联合调整 | 联合优化 memory prompt、tool 与 retrieval 优于独立调参之和 |
| **H3 形态适配** | 对话、编程、客服需要不同层级、TTL 与 graph types | 不同任务形成稳定不同的 M topology |
| **H4 迁移收益** | 可迁移的是 memory procedure 与 validated records，不只是答案 | 跨任务迁移 retrieval/schema 比复制历史对话更有效 |
| **H5 治理必要性** | 持久化与链接放大污染，需要版本、审计、撤销 | 有 provenance/rollback 的 M 违规率低于 append-only M |

最终结论是：**STM 解决“现在能看见什么”，LTM 解决“过去有什么可被重新看见”，M 自修改解决“系统如何改变看见过去的方式”。** 只有把这三层区分开，记忆才从产品功能上升为操作形态。

## 参考文献

1. shinn2023reflexion: Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. 见 r-paper-002。
2. packer2023memgpt: Packer, C., et al. (2023). *MemGPT: Towards LLMs as Operating Systems*. arXiv:2310.08560. 见 r-paper-004。
3. xu2025amem: Xu, W., et al. (2025). *A-MEM: Agentic Memory for LLM Agents*. arXiv:2502.12110. 见 r-paper-005。
4. yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. 见 r-paper-001。
5. sumers2023coala: Sumers, T. R., et al. (2023). *Cognitive Architectures for Language Agents*. 见 r-paper-022。
6. liu2023lost: Liu, N., et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts*. arXiv:2307.03172。
7. r-note-001: 《操作形态学（Operational Morphology）的形式化定义》。
8. r-note-004: 《自修改 Agent 的安全性约束：形式化分析与三层防御》。
9. r-note-009: 《Agent 能力等级 L0-L5 的形式化定义》。
10. r-note-011: 《POMDP 与 LLM Agent 的对应》。
