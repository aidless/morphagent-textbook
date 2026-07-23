---
note_id: r-note-012
title: 工具调用的三层结构：语法、语义与执行边界
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 3, Ch 13]
related_papers: [yao2023react, schick2023toolformer, cai2023latm, wang2023voyager, codeact2024, r-note-001, r-note-003, r-note-004, r-note-009]
keywords: [tool calling, JSON Schema, intent matching, parameter binding, sandbox, retry, tool protocol, T self-modification]
---

# r-note-012: 工具调用的三层结构：语法、语义与执行边界

> 一次可靠的 tool call 不是“模型输出一段 JSON”，而是语法契约、语义决策与受控执行三个层次连续成功；T 自修改只有同时维护这三层不变量，才是能力扩展而不是攻击面扩展。

## 1. 动机

工具调用常被压缩为一个接口示例：向模型提供 function schema，模型返回函数名与参数，宿主程序执行函数。这个描述只覆盖最表面的 serialization。生产中的失败却分布在三个性质不同的层次：模型可能生成不合法 JSON；也可能生成合法 JSON 但选错工具或绑定错参数；即使前两步正确，执行仍可能超时、越权、产生不可逆副作用或返回对抗性内容。

本笔记提出**工具调用三层模型**：

1. **Syntax layer**：工具如何被声明、调用如何被序列化、输出如何被解析；
2. **Semantic layer**：用户意图如何匹配工具，参数如何从上下文绑定，结果如何解释；
3. **Execution layer**：调用如何在权限、预算、幂等、重试、沙箱和审计约束下真正执行。

该分层不是文档组织技巧，而是故障定位与 T 自修改治理的基础。语法正确不蕴含语义正确，语义正确也不蕴含执行安全。形式化地，一次调用成功需要三者合取：

\[
\text{Success}(x,c)=S_{syn}(c)\land S_{sem}(x,c)\land S_{exec}(c)
\]

其中 \(x\) 是任务上下文，\(c\) 是候选调用。任何只优化一个层次的系统都会把错误转移到下一层。

## 2. 概念框架与形式化

### 2.1 工具对象

定义工具 \(t\) 为七元组：

\[
t=(n,\Sigma_{in},\Sigma_{out},\phi,\mathcal{P},\epsilon,\kappa)
\]

- \(n\)：名称与 namespace；
- \(\Sigma_{in}\)：输入 schema；
- \(\Sigma_{out}\)：输出 schema；
- \(\phi\)：自然语言语义说明与适用条件；
- \(\mathcal{P}\)：所需权限集合；
- \(\epsilon\)：副作用模型，如 read-only、write、external-send；
- \(\kappa\)：成本与资源模型，包括延迟、token、金额、rate limit。

传统 function calling 经常只暴露 \((n,\Sigma_{in},\phi)\)，忽略输出契约、权限、副作用与成本。对于只读天气查询，这个简化尚可；对于付款、删除文件、发送邮件或运行代码，它会把最重要的执行语义留在协议之外。

### 2.2 Syntax layer：可解析性与契约一致性

语法层验证调用 \(c=(n,args)\) 是否属于协议语言 \(\mathcal{L}_{proto}\)，并满足输入 schema：

\[
S_{syn}(c)=[c\in\mathcal{L}_{proto}]\land[args\models\Sigma_{in}(n)]
\]

它包括 JSON well-formedness、required fields、type、enum、range、additionalProperties、函数名是否存在，以及 provider 特定 envelope。语法层的职责是把概率性文本输出变成确定性 abstract syntax tree（AST）。

```python
def validate_syntax(call, registry):
    if not is_valid_json(call.raw):
        return Reject("malformed_json")
    if call.name not in registry:
        return Reject("unknown_tool")
    errors = jsonschema_validate(
        call.arguments, registry[call.name].input_schema
    )
    if errors:
        return Repair(errors)  # 只修结构，不猜业务意图
    return Accept(call)
```

**典型失败模式**：缺逗号、字段名幻觉、字符串/数字错型、漏填 required、输出自然语言包裹 JSON、并行调用 ID 丢失、provider envelope 不兼容、schema 漂移。重要原则是：语法 repair 只能恢复结构，不能悄悄改变业务含义。例如把非法日期转换为“今天”不是语法修复，而是未经授权的语义猜测。

### 2.3 Semantic layer：意图匹配与参数绑定

给定任务上下文 \(x\)、工具集合 \(T\)，语义层选择工具并绑定参数：

\[
t^*=\arg\max_{t\in T\cup\{\varnothing\}}U(t\mid x,B)
\]

\[
args^*=\operatorname{Bind}(x,\Sigma_{in}(t^*),\phi_{t^*})
\]

其中 \(\varnothing\) 表示“不调用工具”。效用可分解为：

\[
U(t\mid x)=\alpha R_{task}-\beta C_{cost}-\chi R_{risk}-\delta U_{uncertainty}
\]

语义正确要求：(1) 工具 precondition 满足；(2) 与用户 intent 匹配；(3) 所有参数有证据来源；(4) 单位、时区、身份和作用域正确；(5) 不该调用时能够 abstain。它不是 schema validation 能解决的问题。

```python
def bind_semantics(intent, tool, context):
    args, evidence = {}, {}
    for field in tool.input_schema.required:
        value, source = resolve(field, intent, context)
        if value is UNKNOWN:
            return AskClarification(field)
        args[field] = normalize_unit_and_scope(field, value)
        evidence[field] = source
    if not tool.precondition(args, context):
        return Reject("precondition_failed")
    return BoundCall(tool.name, args, provenance=evidence)
```

**典型失败模式**：选错同名工具、把联系人姓名绑定到错误账户、城市同名消歧失败、把摄氏度当华氏度、把“下周五”绑定到错误时区、遗漏隐含约束、过度调用、工具描述注入、工具太多造成 attention dilution。最危险的语义错误通常是“JSON 完美但对象错了”。

### 2.4 Execution layer：副作用、隔离与恢复

执行层把经过语法和语义检查的调用提交到真实系统。定义执行上下文：

\[
\mathcal{E}=(sandbox,identity,capability,budget,deadline,retry,audit)
\]

安全执行要求：

\[
S_{exec}(c)=Auth(c)\land Budget(c)\land Isolated(c)\land Recoverable(c)
\]

其中 `Recoverable` 对只读调用意味着可重试；对写调用意味着幂等、补偿事务或人工确认。执行器必须区分 deterministic error、transient error、policy error 和 semantic rejection，不能把所有失败都交给 LLM 盲目重试。

```python
def execute(call, policy):
    assert policy.authorize(call.tool, call.arguments)
    key = idempotency_key(call)
    if side_effecting(call) and not call.confirmed:
        return NeedConfirmation(preview(call))
    try:
        return sandbox.run(
            call, timeout=policy.timeout,
            network=policy.egress_allowlist,
            filesystem=policy.fs_scope,
            idempotency_key=key,
        )
    except TransientError as err:
        return retry_with_backoff(call, err, max_attempts=policy.max_retries)
    except PolicyViolation as err:
        audit_security_event(call, err)
        return Reject("policy_violation")
```

**典型失败模式**：timeout、rate limit、重复付款、部分写入、sandbox escape、secret leakage、SSRF、错误重试引发调用风暴、工具返回携带间接 prompt injection、异常被转成“成功字符串”。执行层必须把 tool output 当作不可信 observation，而不是更高优先级的 instruction。

### 2.5 三层错误矩阵

| 症状 | Syntax | Semantics | Execution | 正确处理 |
|---|---|---|---|---|
| JSON 缺字段 | 失败 | 未判定 | 未执行 | schema-guided repair |
| 合法调用错误客户账户 | 通过 | 失败 | 不应执行 | clarification / entity confirmation |
| 合法且意图正确但越权 | 通过 | 通过 | 失败 | policy deny，不重试 |
| HTTP 429 | 通过 | 通过 | transient failure | backoff、预算内重试 |
| 写操作已成功但 response 丢失 | 通过 | 通过 | 状态未知 | idempotency lookup，禁止重复提交 |
| 工具结果含“ignore previous” | 通过 | 调用本身可正确 | output 不可信 | taint + content isolation |
| schema 更新后旧字段仍输出 | 失败 | 可能正确 | 未执行 | version negotiation / adapter |

三层日志也应分离：syntax log 记录 parser/schema；semantic log 记录候选工具、置信度与参数 provenance；execution log 记录身份、权限、attempt、side effect 和结果。只有这样才能区分“模型不会用工具”和“工具服务不可用”。

## 3. 方法细节与协议比较

### 3.1 端到端调用状态机

```text
User intent
   ↓
Candidate tool selection ── low confidence → clarify / no-tool
   ↓
Argument binding + provenance
   ↓
Protocol serialization
   ↓
Schema validation ── invalid → bounded repair
   ↓
Policy / permission / budget check ── deny → stop
   ↓
Dry-run or confirmation (side-effecting only)
   ↓
Sandboxed execution
   ↓
Typed result validation
   ↓
Observation isolation + interpretation
   ↓
Commit / compensate / retry / finish
```

该顺序揭示一个常见反模式：先让模型生成 JSON，再在执行失败后反复“让模型修一下”。这种流程把 semantic ambiguity 与 permission denial 错当 syntax problem，可能反复提交副作用。更可靠的设计是在 serialization 前完成 intent、entity、scope 与 confirmation。

### 3.2 OpenAI、Anthropic、Google 协议比较

三家协议都能表达“模型请求调用工具、客户端执行、结果回送”的基本循环，但 envelope、role、并行调用与 schema 支持随版本演化。下表比较的是**抽象设计面**，不是某一日期的字段级兼容承诺；具体实现应锁定 provider API version。

| 维度 | OpenAI tool/function calling | Anthropic tool use | Google Gemini function calling |
|---|---|---|---|
| 工具声明 | name + description + JSON-like parameters | name + description + input_schema | function declarations + schema |
| 模型输出 | tool call object，带 arguments 与 call id | `tool_use` content block，带 id/input | function call part，name/args |
| 结果回送 | tool role / call id 对齐 | `tool_result` 对应 tool_use id | function response part |
| 并行调用 | 支持，需正确关联 IDs | content blocks 可表达多个调用 | 支持程度依 SDK/模型版本 |
| 语法约束 | structured output 可增强 | schema 约束 input | schema 驱动参数生成 |
| 执行责任 | 客户端 | 客户端 | 客户端 |
| 共同空白 | 权限、副作用、幂等、补偿、信任等级通常需应用层补齐 |

协议差异主要在 syntax layer；semantic 与 execution layer 仍由开发者负责。声称“采用某 provider function calling 就解决工具安全”是类别错误：provider 负责模型与客户端之间的表示契约，不负责你的账户选择、审批政策、事务补偿或 sandbox。

### 3.3 Toolformer 与三层模型

r-paper-003 Toolformer 通过自监督数据构造和 fine-tuning 学会何时插入 API call。它优化了 syntax pattern 与部分 semantic selection：训练 loss 筛选“调用是否帮助后续预测”。但工具集合与实现固定，execution layer 基本被假设可靠。

| 层 | Toolformer 覆盖 | 未解决问题 |
|---|---|---|
| Syntax | 学习 API call token pattern | 新 schema 需重训，跨协议弱 |
| Semantics | 学习何时调用与参数生成 | perplexity improvement 不等于用户 intent/安全 |
| Execution | 执行结果拼回文本 | 缺权限、重试、对抗输出治理 |

因此 Toolformer 是“T 使用模式学习”，不是完整 T 自修改。它证明 LLM 可内化调用习惯，却没有让 Agent 运行时添加工具或治理副作用。

### 3.4 LATM 与三层模型

r-paper-018 LATM 用昂贵 Tool Maker 生成函数、便宜 Tool User 复用，并通过 cost model 与单元测试决定是否进入 Tool Pool。它直接扩展 T，但三层成熟度不均：

- Syntax：生成函数签名并注册，需 schema adapter；
- Semantics：embedding 匹配子任务与已有工具，存在误路由；
- Execution：单元测试是最低验证，但不能替代 sandbox、权限与 adversarial tests。

LATM 的 break-even 逻辑说明工具不应无界增长，但经济收益不是安全证据。一个高复用恶意工具在 cost model 下反而更容易被保留。故 acceptance condition 应从：

\[
benefit(t)>cost(t)
\]

扩展为：

\[
benefit(t)>cost(t)\land V_{syn}(t)\land V_{sem}(t)\land V_{exec}(t)
\]

### 3.5 T 自修改的事务化协议

设工具集合在版本 \(k\) 为 \(T_k\)，元控制器提出修改 \(\Delta T\)。安全更新为：

\[
T_{k+1}=\operatorname{Commit}(T_k,\Delta T)
\]

仅当：

\[
I_{compat}\land I_{meaning}\land I_{permission}\land I_{runtime}\land I_{rollback}
\]

全部成立。分别表示旧调用兼容、语义契约明确、权限不扩张或获批准、沙箱/属性测试通过、可回滚。

```python
def modify_tool_registry(registry, proposal):
    candidate = registry.fork()
    candidate.apply(proposal)

    checks = [
        schema_backward_compatible(candidate),
        semantic_contract_review(candidate),
        permission_delta_approved(candidate),
        sandbox_tests_pass(candidate),
        adversarial_output_tests_pass(candidate),
        rollback_plan_exists(candidate),
    ]
    if not all(checks):
        return registry  # reject atomically

    staged = canary_deploy(candidate, traffic=0.01)
    if staged.error_rate > threshold or staged.policy_violations > 0:
        staged.rollback()
        return registry
    return staged.promote()
```

这使 T 自修改类似数据库 migration，而不是把一段模型生成代码直接 `exec()`。

## 4. 与本书其他章节/笔记的关系

| 交叉引用 | 本笔记提供的连接 |
|---|---|
| Ch 3 | 将 function calling 从 JSON 技巧提升为三层协议栈 |
| Ch 13 | 给自动工具创建、重构、删除定义完整验收条件 |
| r-note-001 | 细化 \(B=\{P,T,M,C\}\) 中 T 的内部结构 |
| r-note-003 | T 修改会迫使 P 更新描述、M 更新经验、C 更新 adapter，体现 H2 |
| r-note-004 | permission invariant、sandbox 与 rollback 约束 execution layer |
| r-note-008 | 工具数量、schema、permission 与 cost 共同构成 T 的形态空间 |
| r-note-009 | 静态工具使用是 L0/L1；运行时 T 修改进入 L2+，全 B 修改才是 L4/L5 |
| r-paper-001 | ReAct 提供 Thought–Action–Observation，但 action parser 只是 syntax 起点 |
| r-paper-003 | Toolformer 覆盖训练期调用模式，未运行时扩展 T |
| r-paper-017 | Voyager 以环境执行验证技能，补足部分 execution layer |
| r-paper-018 | LATM 提供 cost-aware T 创建，但需加强权限与沙箱 |
| r-paper-020 | CodeAct 用 executable code 扩大 action expressiveness，也扩大 execution attack surface |

### L0-L5 定位

- **L0**：使用预定义工具，T 与协议冻结；重点是三层基础可靠性。
- **L1**：增加工具检索或更大 registry，但仍无自修改。
- **L2**：可修改一个 T 维度，如 description、schema 或新增工具；至少版本控制。
- **L3**：T 与 P/M/C 协同修改，并有自动验证与回滚。
- **L4**：可修改 T 的声明、语义路由和执行实现，需全栈 canary 与权限治理。
- **L5**：P/T/M/C 联合演化且 \(\gamma=3\)，高风险工具变更必须人工审计。

## 5. 局限与开放问题

### 5.1 层间边界不是绝对的

某些错误跨层。例如单位错误可以编码为 schema enum（syntax），也可以留给语义归一化；permission 可以写入 schema annotation，也由执行 policy 强制。分层的目的不是唯一归类，而是确保每项约束至少有一个**确定性强制点**。自然语言 description 不能是唯一强制点。

### 5.2 开放世界语义不可完备

工具 intent 无法穷举。用户可能暗示、反讽、缺少上下文，多个工具可能同样合理。Semantic layer 的目标应包括 calibrated abstention 与 clarification，而非强制 100% 自动调用。工具选择 benchmark 只测 top-1 accuracy 会奖励过度自信。

### 5.3 自动 repair 的风险

结构化输出 repair 提高成功率，却可能掩盖模型不确定性。修复字段名通常安全；自动补账户、金额、收件人则危险。需要定义 repair boundary：只允许等价语法变换，不允许改变 intent-bearing values。

### 5.4 并行工具调用与事务

并行 call 可降延迟，却产生依赖、竞态与部分失败。两个只读搜索可并行；“创建订单”和“扣款”必须有顺序、事务 ID 与补偿。未来协议需要显式 DAG、precondition 和 commit semantics，而不仅是 call list。

### 5.5 跨 provider 可移植性

JSON Schema 子集、nullability、enum、parallel calls 与 result envelope 可能不同。通用 tool IR 需要 adapter 与 conformance tests。否则“换模型”会变成隐式 T 修改，导致原本可靠的参数绑定与错误处理退化。

### 5.6 工具返回的信任问题

工具执行成功不代表输出真实、安全或适合作为指令。网页搜索、邮件、数据库字段都可能被攻击者控制。Execution layer 应返回 typed result + provenance + trust label，P 必须规定 tool result 是 data。此问题直接连接 r-note-014 的 T poisoning 与 r-paper-021 的 indirect injection。

## 6. 对操作形态学的贡献与 H1-H5 映射

本笔记把 T 从“函数列表”扩展为三层操作形态：可表达的调用语言、任务到调用的语义映射、调用到现实副作用的执行机制。由此，新增工具不必然扩大有效行动空间；只有三层都通过，才真正获得可靠 capability。T 自修改也不再等于 registry append，而是合同、路由与执行的事务化演化。

| 假设 | 本笔记的作用 | 可检验预测 |
|---|---|---|
| **H1 结构可塑性** | 运行时 T 修改扩大或重塑 action space | API 漂移下 adaptive T 的恢复时间与 regret 更低 |
| **H2 协同演化** | T 变更需联动 P 描述、M 经验、C adapter | 协同 migration 优于独立更新后拼接 |
| **H3 形态适配** | 不同领域需要不同 registry、权限与执行策略 | 领域特异 T 在安全—性能前沿上优于最大工具集 |
| **H4 迁移收益** | 可迁移的是语义合同与执行 policy，不仅是 schema | 跨 provider IR + adapter 优于复制 prompt 示例 |
| **H5 治理必要性** | schema validation 不足，必须权限、sandbox、canary、rollback | 全三层治理的违规率低于 syntax-only 系统 |

最终结论是：**工具调用不是一个模型特性，而是一条跨越概率生成与确定性执行的系统边界。** 把 JSON 输出率当作 tool-use 能力，会系统性高估 Agent；把执行成功率当作安全，会忽视错对象与越权；把能创建函数当作 T 自进化，会忽视验证与回滚。三层同时成立，T 才是可用的操作形态。

## 参考文献

1. schick2023toolformer: Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. NeurIPS. 见 r-paper-003。
2. cai2023latm: Cai, T., et al. (2023). *Large Language Models as Tool Makers*. arXiv:2305.17126. 见 r-paper-018。
3. yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR. 见 r-paper-001。
4. wang2023voyager: Wang, G., et al. (2023). *Voyager: An Open-Ended Embodied Agent with Large Language Models*. 见 r-paper-017。
5. codeact2024: Wang, X., et al. (2024). *Executable Code Actions Elicit Better LLM Agents*. 见 r-paper-020。
6. OpenAI. *Function Calling / Tools Documentation*. 具体实现需锁定 API version。
7. Anthropic. *Tool Use Documentation*. 具体实现需锁定 API version。
8. Google. *Gemini Function Calling Documentation*. 具体实现需锁定 API version。
9. r-note-001: 《操作形态学（Operational Morphology）的形式化定义》。
10. r-note-004: 《自修改 Agent 的安全性约束：形式化分析与三层防御》。
11. r-note-009: 《Agent 能力等级 L0-L5 的形式化定义》。
12. r-note-014: 《自修改系统的攻击面分级》。
