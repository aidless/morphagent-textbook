---
chapter: 1
title_cn: LLM 智能体时代
title_en: The Age of LLM Agents
part: I
pages_planned: 16
status: final
last_updated: 2026-07-22
keywords:
  - LLM Agent
  - Tool Use
  - Reflection
  - Self-Evolving
learning_objectives:
  - 区分 LLM 与 LLM Agent
  - 解释「代码即行动」的范式转变
  - 描述自进化 Agent 与固定 Agent 的边界
prerequisites: []
---

# 第 1 章 · LLM 智能体时代

> "LLM 第一次把'写出可执行代码'变成了一个思考动作。"
>
> ——本章开篇引言

## 学习目标

完成本章后，读者应能够：

1. 区分纯 LLM 与 LLM Agent 的能力边界
2. 复述 ReAct、Reflexion、AutoGPT、BabyAGI 四个里程碑的差异
3. 识别「工具调用」作为通用接口带来的范式转变
4. 描述「自进化 Agent」与「固定 Agent」的边界

## 先修知识

无需先修章节。本章是全书第一篇。

## 章节地图

- **1.1** 从语言模型到行动者
- **1.2** 工具调用作为通用接口
- **1.3** 反思与短期记忆
- **1.4** 自进化 Agent 的边界
- **1.5** 本书路线图

---

## 1.1 从语言模型到行动者

大型语言模型（Large Language Model, LLM）的能力跃迁发生在三个层次的叠加：参数规模、数据多样性和对齐技术。2022 年底 ChatGPT 的出现，把 LLM 从"研究演示"推向了"通用工具"——这一转变的关键不是模型本身的参数，而是人机交互的范式转变。LLM 第一次能够接受自然语言指令并产生"看起来有用"的输出，覆盖了从写作、翻译到代码生成、逻辑推理的广泛任务。

但 LLM 本身有一个根本限制：它只能"说话"，不能"做事"。当用户问"明天北京会下雨吗"，LLM 可以基于训练数据中常见的天气模式给出一个"听起来合理"的回答，但这个回答不是查询真实天气 API 的结果——它可能是正确的，也可能是编造的。这种"听起来合理但未必真实"的特性在技术上叫 **幻觉（hallucination）**，它来自 LLM 作为生成式模型的本质：模型在采样下一个 token，而不是在查询一个事实。

要突破这个限制，LLM 必须与外部世界发生交互。这正是 LLM Agent 的起点：把 LLM 的"思考能力"与"行动能力"解耦，让 LLM 只负责推理，让专门的工具负责执行。2023 年 10 月，Yao 等人在 ICLR 2023 发表的 ReAct 论文首次系统地提出了"思考-行动"交替循环的范式——LLM 不是直接生成最终答案，而是在每一步先生成一个"思维链"（Chain-of-Thought），再决定调用哪个工具，再观察工具的返回，再生成下一步思维。这种范式把 LLM 从"语言生成器"变成了"行动决策器"，是 LLM Agent 的奠基性工作 [$TRAE_REF](https://arxiv.org/abs/2210.03629)。

### 图 1.1 · ReAct 时序图：思考-行动-观察三步循环

```
  用户输入                              Agent                                 外部世界
  ────────                            ────────                              ────────
       │                                  │                                      │
       │  "查北京明天天气"                 │                                      │
       ├─────────────────────────────────>│                                      │
       │                                  │  思考：我需要查天气 API              │
       │                                  │  (Thought)                          │
       │                                  │                                      │
       │                                  │  行动：调用 get_weather(city="北京")  │
       │                                  ├─────────────────────────────────────>│
       │                                  │                                      │
       │                                  │  观察：API 返回 {temp: 25, rain: 30%}│
       │                                  │<─────────────────────────────────────┤
       │                                  │                                      │
       │                                  │  思考：温度 25 度，降水 30% → 会下雨  │
       │                                  │  (Thought)                          │
       │                                  │                                      │
       │  回答：北京明天 25°C，降水概率 30% │                                      │
       │<─────────────────────────────────┤                                      │
       │                                  │                                      │
       ▼                                  ▼                                      ▼
```

> **关键点**：ReAct 把 LLM 的输出从"一次性文本"变成了"思考+行动+观察"的三步循环。每一步 LLM 都先解释自己在做什么（Thought），再决定调用哪个工具（Action），再消化工具的返回（Observation）。这种显式推理让 Agent 的每一步都可追溯、可调试。

从 ReAct 开始，LLM Agent 在三年内迅速分化出多个分支。2023 年 3 月，Shinn 等人提出的 Reflexion 引入了"反思"机制——Agent 在每次行动后生成对自身行为的文字评估，并把这个评估存入记忆用于下一次决策。这一步把"短期记忆"从静态的上下文窗口扩展成了可累积的经验，使 Agent 能够在多步任务中持续改进 [$TRAE_REF](https://arxiv.org/abs/2303.11366)。同年 4 月，Significant Gravitas 发布的 Auto-GPT 把 LLM Agent 推向了公众视野：只要给定一个目标，Auto-GPT 就能自主生成子任务、调用工具、评估结果、迭代执行，直到目标完成。Auto-GPT 引发的热潮直接催生了"自主 Agent"作为一个研究方向。同年同月，Yohei Nakajima 发布的 BabyAGI 则采用了任务驱动 + 优先级队列的设计——把所有待办任务维护在一个优先级队列中，每完成一个任务就生成新的子任务并重新排序，把工作流管理正式引入了 Agent 设计。

### 表 1.1 · 四个 LLM Agent 里程碑的设计选择对比

| 里程碑 | 时间 | 核心设计 | 自主性来源 | 主要缺陷 |
|---|---|---|---|---|
| **ReAct** | 2023-03 | 思考-行动-观察三步循环 | 单轮内显式推理 | 不保留跨轮记忆 |
| **Reflexion** | 2023-03 | 每次行动后写反思存入记忆 | 跨轮语言反馈 | 反思质量受 LLM 限制 |
| **Auto-GPT** | 2023-04 | 给定目标，自主生成子任务 | 完全开放式目标分解 | 容易陷入无限循环 |
| **BabyAGI** | 2023-04 | 任务优先级队列 + 持续重排 | 任务队列动态调度 | 队列可能无限膨胀 |

这四个里程碑（ReAct、Reflexion、AutoGPT、BabyAGI）共同定义了"LLM Agent"这个概念的早期版图。但它们的共同假设是：**Agent 的所有决策逻辑、工具集合、记忆结构在部署时就已经固定，运行时不再改变**。本书要追问的核心问题是——如果允许 Agent 在运行时持续修改自己的 prompt、工具、记忆甚至代码，会发生什么？这正是"自进化 Agent"的研究主题，也是本书 800 页内容的最终落点 [$TRAE_REF](https://arxiv.org/abs/2508.07407)。

## 1.2 工具调用作为通用接口

工具调用（Tool Calling）是 LLM Agent 与外部世界交互的通用接口。2023 年初，Schick 等人发表的 Toolformer 证明了 LLM 可以自学在文本中插入 API 调用——给定一个文本语料，Toolformer 自动标注哪些位置应该调用哪个 API，调用后效果如何，然后用监督学习的方法微调模型，让模型学会"在适当的时候调用适当的工具"。这项工作的核心洞察是：**工具调用不是工程上的便利，而是 LLM 推理能力的自然延伸**——模型不只是预测下一个 token，还可以预测"下一步我需要什么外部信息" [$TRAE_REF](https://arxiv.org/abs/2302.04761)。

2024 年 6 月，OpenAI 在 API 中正式引入 **Function Calling** 协议，把工具调用标准化为三个字段：`name`（工具名）、`description`（工具描述）、`parameters`（JSON Schema 定义的参数结构）。LLM 在推理时不再返回纯文本，而是返回一个结构化的"工具调用请求"，由 Agent 运行时负责实际执行工具并把结果注入下一轮对话。这套协议被 Anthropic、Google、阿里云、DeepSeek 等厂商迅速采纳，成为 Function Calling 的事实标准 [$TRAE_REF](https://platform.openai.com/docs/guides/function-calling)。

### 图 1.2 · Function Calling 协议栈

```
   ┌─────────────────────────────────────────────────┐
   │                  LLM 推理引擎                    │
   │   Prompt + 工具描述 → 输出工具调用请求          │
   └────────────────────┬────────────────────────────┘
                        │ JSON:
                        │ {
                        │   "name": "get_weather",
                        │   "arguments": {"city": "北京"}
                        │ }
                        ▼
   ┌─────────────────────────────────────────────────┐
   │             Agent 运行时（解释层）                │
   │   校验 JSON Schema → 找到对应实现 → 捕获异常    │
   └────────────────────┬────────────────────────────┘
                        │ 函数调用（Python / RPC / HTTP）
                        ▼
   ┌─────────────────────────────────────────────────┐
   │               工具实现层                         │
   │   get_weather(city="北京") → {temp: 25, rain: 30}│
   └────────────────────┬────────────────────────────┘
                        │ 结构化返回
                        ▼
   ┌─────────────────────────────────────────────────┐
   │             Agent 运行时（注入层）                │
   │   把工具返回包装为 Observation → 注入下一轮 Prompt│
   └─────────────────────────────────────────────────┘
```

> **关键点**：Function Calling 把"LLM 的推理"和"工具的执行"通过一个标准 JSON 接口解耦。LLM 只需输出符合 Schema 的结构化请求，Agent 运行时负责调度、校验、重试和结果注入。这种解耦是自进化 Agent 的工程基础——任何新工具只要注册为 JSON Schema 就能被 LLM 自动调用。

工具调用的范式价值在于它把 LLM 的"行动空间"统一了。在工具调用之前，每个 Agent 框架都自己定义工具格式——LangChain 的 Tool、AutoGPT 的 Command、BabyAGI 的 Task——互不兼容。Function Calling 标准化之后，任何 Agent 框架只要遵循 JSON Schema 就能复用同一套工具定义。这给"自进化 Agent"奠定了基础：如果 Agent 想要创建新工具，它只需要生成符合 JSON Schema 的描述并注册到工具池，旧工具无需重写。

但工具调用也带来了三个新的工程挑战：

1. **JSON Schema 验证**：LLM 生成的参数经常类型错误、字段缺失或语义模糊，需要在 Agent 运行时做严格的 schema 校验和自动修复。
2. **错误传播**：工具调用失败时，错误信息必须以结构化的形式回传给 LLM，让 LLM 决定是重试、降级还是切换工具。
3. **工具描述质量**：Function Calling 的效果严重依赖工具描述的清晰度——如果 `description` 字段写得太抽象，LLM 就会在错误的情境调用错误的工具。

这三个挑战将在第 3 章详细讨论。

## 1.3 反思与短期记忆

反思（Reflection）是 LLM Agent 区别于一次性 LLM 调用的核心能力。一次性 LLM 调用是"输入 → 输出"的映射，没有错误修正的余地；而 LLM Agent 通过"输出 → 反思 → 调整"形成闭环，能够在多步任务中持续改进。Reflexion 是首个系统化提出"反思"机制的工作——它在每一步行动后，要求 LLM 用自然语言生成对当前轨迹的评估（"这一步成功了吗？如果失败，原因是什么？下次应该如何调整？"），并把这个评估存入记忆。在下一步决策时，LLM 会检索这些反思条目作为额外上下文，从而避免重复同样的错误 [$TRAE_REF](https://arxiv.org/abs/2303.11366)。

反思的工作机制依赖于 **短期记忆（Short-Term Memory）** 的存在。短期记忆在 LLM Agent 中有三种实现方式：

1. **上下文窗口**：最简单但有长度上限，一旦超过必须丢弃或压缩。
2. **对话历史缓存**：把多轮对话作为 KV cache 存储，避免重复计算。
3. **结构化反思条目**：把反思结果以键值对或列表形式存储，支持语义检索。

### 图 1.3 · Reflexion 反思循环：行动 → 反思 → 存储 → 检索

```
        ┌─────────────────────────────────────────────────────┐
        │              Reflexion 反思循环                       │
        └─────────────────────────────────────────────────────┘

   Step t              Step t+1              Step t+2            Step t+3
   ──────              ────────              ────────            ────────
     │                   │                     │                  │
     ▼                   ▼                     ▼                  ▼
  ┌────────┐         ┌────────┐          ┌────────┐          ┌────────┐
  │ Action │────────>│Reflect│─────────>│  Store │─────────>│Retrieve│
  │        │         │ 评估   │          │ 入记忆 │          │ 检索   │
  └────────┘         └────────┘          └────────┘          └───┬────┘
     │                   │                     │                  │
     │              "成功了吗？"           key: step_t         │
     │              "失败原因？"           val: text            │
     │              "下次怎么做？"                             │
     │                                                          │
     ▼                                                          ▼
   External                                              Inject into
   Environment                                            next Prompt
```

> **关键点**：反思循环不是"做完任务再总结"，而是嵌入到每一步决策中。Reflexion 的贡献是把反思变成可检索的记忆条目，而不是孤立的总结文本。这种"反思即记忆"的设计让 Agent 的经验可以跨任务迁移。

第 5 章会专门讨论上下文工程与短期记忆的设计模式。这里只需要建立一个直觉：**短期记忆决定了 Agent 能"看见"什么**。如果记忆机制设计不当，Agent 会在多步任务中重复犯同样的错误，因为它"看不见"自己曾经失败过。

反思机制的另一个隐性作用是 **可解释性（interpretability）**。Agent 的反思条目本身就是一份"自传"——它记录了 Agent 在每个时间点对自身行为的判断。研究者可以用这些反思条目反向分析 Agent 的失败模式，而不必依赖事后猜测。这一点在第 20 章的"调试与可观测性"中会被进一步展开。

但反思不是万能的。它有至少两个根本限制：第一，反思质量受限于 LLM 自身的判断能力——如果 LLM 在某个领域缺乏足够的世界知识，反思可能只是"用错误的方式解释错误"；第二，反思条目会污染短期记忆——如果 Agent 把错误的反思当成事实记忆下来，后续决策就会被误导。这两个限制将在第 14 章"自适应记忆结构"中通过"记忆一致性"机制部分缓解。

> **复述框 · 1.3 节要点**
>
> - **反思 ≠ 短期记忆**：反思是"对过去的判断"，短期记忆是"当前能看见什么"。前者是后者的内容来源，但内容质量不等于上下文有效性。
> - **反思是 LLM Agent 的可解释性载体**：反思条目本身可以反向分析 Agent 的决策逻辑。
> - **反思有上限**：反思依赖 LLM 自身的判断力，可能引入"用错误解释错误"的二次失败。

## 1.4 自进化 Agent 的边界

固定架构的 LLM Agent 在面对长期任务时存在三个根本限制。第一个限制是 **策略僵化**：Agent 的 prompt、工具集、反思模式全部由开发者在部署前写死，运行中不再变化；一旦任务环境超出开发者预想的范围，Agent 的性能会迅速下降。第二个限制是 **记忆碎片化**：短期记忆随会话结束而丢失，长期记忆只能依赖向量检索这种"被动召回"机制，缺少"主动整理"和"主动遗忘"的能力。第三个限制是 **工具刚性**：Agent 能调用的工具集是预先定义的；当遇到新任务需要新工具时，要么开发者手动添加，要么 Agent 完全无法处理。

针对这三个限制，2024–2026 年间出现了一个新的研究方向——**自进化 Agent（Self-Evolving Agent）**——其核心思想是：Agent 的 prompt、工具、记忆甚至代码不再是部署时固定的产物，而是可以**在运行时被 Agent 自身修改的对象**。这与软件工程中的"自修改程序（self-modifying code）"思想一脉相承，但在 LLM 时代有了新的实现路径：用自然语言作为"自修改指令"，让 LLM 本身充当"自修改控制器"。

自进化 Agent 的研究在 2025 年开始系统化。Fang 等人 2025 年 8 月在 arXiv 发表的综述《A Comprehensive Survey of Self-Evolving AI Agents》用一个统一框架把现有工作纳入"系统输入 / Agent 系统 / 环境 / 优化器"四元反馈环——**优化器**根据环境反馈修改 **Agent 系统**（包括 prompt、工具、记忆、代码），而 Agent 系统继续与环境交互产生新反馈。这个框架的核心洞察是：自进化的关键不在于单组件的修改，而在于**整个 Agent 系统能根据反馈持续重塑自身** [$TRAE_REF](https://arxiv.org/abs/2508.07407)。

### 图 1.4 · 自进化 Agent 的四元反馈环

```
                          ┌──────────────────────────┐
                          │   System Inputs           │
                          │   (用户目标 / 任务描述)    │
                          └────────────┬─────────────┘
                                       │ 提供初始设定
                                       ▼
                          ┌──────────────────────────┐
                          │   Agent System            │
                          │   ┌──────────────────┐   │
                          │   │ B = {P, T, M, C} │   │ ← Prompt / Tools /
                          │   └──────────────────┘   │   Memory / Code
                          └────────────┬─────────────┘
                                       │ 行动 Action
                                       ▼
                          ┌──────────────────────────┐
                          │   Environment             │
                          │   (任务环境 / 工具结果)    │
                          └────────────┬─────────────┘
                                       │ 反馈 Feedback
                                       ▼
                          ┌──────────────────────────┐
                          │   Optimisers              │
                          │   (修改 prompt/工具/      │
                          │    记忆/代码的元控制器)    │
                          └────────────┬─────────────┘
                                       │ 更新 B
                                       ▼
                                  (回到 Agent System)
```

> **关键点**：四元反馈环的核心不是"Agent 改自己"，而是"优化器根据环境反馈调整 Agent 系统"。这一区分避免了循环论证——自进化的源头是环境反馈，不是 Agent 自己的偏好。

从研究对象看，自进化 Agent 可以沿着四个维度展开：

1. **自修改 prompt**：用 OPRO、DSPy、PromptAgent 等方法，让 Agent 自动优化自己的系统提示词 [$TRAE_REF](https://arxiv.org/abs/2309.03409)。
2. **自动工具创建**：用 LATM、Voyager、AlphaEvolve 等方法，让 Agent 自动生成新工具、维护工具生命周期 [$TRAE_REF](https://arxiv.org/abs/2305.17126)。
3. **自适应记忆结构**：用 MemGPT、A-MEM 等方法，让 Agent 动态调整记忆的 schema、索引和检索策略 [$TRAE_REF](https://arxiv.org/abs/2502.12110)。
4. **自我改写代码**：用 SICA、Gödel Agent 等方法，让 Agent 直接修改自己的执行代码——这是最激进也最危险的形式 [$TRAE_REF](https://arxiv.org/abs/2504.15228)。

这四个方向都有公开的代表性工作；真正空白的是**跨组件的协同自进化**——让 prompt、工具、记忆、代码的修改形成正反馈回路。这也是本书 Part II 和 Part III 的核心议题。

> **复述框 · 1.4 节要点**
>
> - **自进化 Agent = 运行时可修改的 Agent 系统**：prompt、工具、记忆、代码都可作为修改对象。
> - **四元反馈环是统一框架**：Inputs / Agent System / Environment / Optimisers。
> - **四个研究方向已有工作**：prompt 自改、工具自创、记忆自适应、代码自改。
> - **真正空白是跨组件协同**：单独修改任一组件的研究已饱和，协同自进化是未来 3 年最值得投入的方向。

## 1.5 本书路线图

本书 25 章按 6 个 Part 组织，覆盖「基础 → 理论 → 自进化 → 实现 → 治理 → 附录」的完整学习路径。下图展示了 LLM 智能体的能力层级，也是我们理解全书结构的脚手架。

### 图 1.5 · LLM 智能体的能力层级金字塔

```
                         ▲
                        ╱ ╲
                       ╱ L5╲        跨组件协同自进化（Part III·第 16 章）
                      ╱─────╲
                     ╱   L4  ╲       单组件自进化（Part III·第 12-15 章）
                    ╱─────────╲
                   ╱    L3     ╲      反思 + 长期记忆（Part I·第 5-6 章）
                  ╱─────────────╲
                 ╱      L2       ╲    工具调用 + Function Calling（Part I·第 3 章）
                ╱─────────────────╲
               ╱        L1         ╲  提示词工程（Part I·第 4 章）
              ╱─────────────────────╲
             ╱          L0            ╲ ReAct 循环（本章）
            ╱───────────────────────────╲
```

- **L0（本章）**：ReAct 循环——思考与行动交替的最简范式。
- **L1（第 4 章）**：静态提示词工程——人工或半自动优化指令。
- **L2（第 3 章）**：工具调用——Function Calling 协议与工具生态。
- **L3（第 5–6 章）**：反思 + 长期记忆——跨越单次会话的能力累积。
- **L4（第 12–15 章）**：单组件自进化——prompt / 工具 / 记忆 / 代码各自的自修改。
- **L5（第 16 章）**：跨组件协同自进化——本书最核心的研究问题。

读者可以按章节顺序通读，也可以根据自己的研究兴趣跳读——例如研究"自修改 prompt"的读者可以重点读 Part I 第 4 章 + Part III 第 12 章 + Part V 第 22 章（安全性）；研究"具身认知"的读者可以重点读 Part II 第 7–11 章。

---

## 本章小结

- LLM Agent 把"思考"和"行动"解耦，让 LLM 负责推理、工具负责执行，这是 ReAct 奠定的范式。
- 工具调用是 LLM Agent 与外部世界的通用接口；Function Calling 协议把工具定义标准化为 JSON Schema。
- 反思让 Agent 能够在多步任务中持续改进，但反思质量受限于 LLM 自身能力，且反思条目可能污染记忆。
- 自进化 Agent 是 LLM Agent 的下一代形态：prompt、工具、记忆、代码都可以在运行时被修改。
- 本书 25 章按 6 个 Part 组织，最终回答"跨组件协同自进化"这一核心研究问题。

## 推荐阅读

- 📖 **ReAct 原始论文** [Yao et al., 2023]：LLM Agent 的奠基性工作，首次提出"思考-行动"交替循环。[$TRAE_REF](https://arxiv.org/abs/2210.03629)
- 📖 **Reflexion 原始论文** [Shinn et al., 2023]：反思机制的源头，把"语言反馈"作为 Agent 的学习信号。[$TRAE_REF](https://arxiv.org/abs/2303.11366)
- 📖 **Toolformer 原始论文** [Schick et al., 2023]：LLM 自学工具调用的早期工作，证明工具调用是推理的自然延伸。[$TRAE_REF](https://arxiv.org/abs/2302.04761)
- 📖 **Function Calling 官方文档** [OpenAI, 2024]：Function Calling 协议的事实标准文档。[$TRAE_REF](https://platform.openai.com/docs/guides/function-calling)
- 📖 **Self-Evolving Agents 综述** [Fang et al., 2025]：把自进化 Agent 纳入"Inputs / Agent System / Environment / Optimisers"四元反馈环的统一框架。[$TRAE_REF](https://arxiv.org/abs/2508.07407)

## 练习题

1. **概念题**：用一段话解释为什么 ReAct 的"思考-行动"循环能缓解 LLM 的幻觉问题，但不能完全消除。
2. **比较题**：列出 ReAct、Reflexion、AutoGPT、BabyAGI 四个里程碑各自最核心的一个设计选择，并说明这些选择如何反映了它们对"自主性"的不同理解。
3. **动手题**：使用 OpenAI Function Calling API 实现一个能查询实时天气的 Agent：当用户问"明天北京会下雨吗"时，调用天气 API 并返回真实结果（伪代码或最小可运行示例即可）。
4. **开放题**：如果让你设计一个"反思质量评估指标"，你会考虑哪些维度？为什么？
5. **挑战题**：从 [Fang et al., 2025 的自进化 Agent 综述](https://arxiv.org/abs/2508.07407) GitHub 仓库中挑 3 篇你最感兴趣的论文，写一份 300 字的对比分析。
6. **综合题**：用 200 字描述 L0–L5 六个能力层级的递进关系，并指出每一层级最核心的一个新能力。

## 常见误区

- ❌ **把 LLM 当"世界模型"**：LLM 只是生成式模型，不能代替外部知识库与工具调用。
- ❌ **把"反思"等同于"记忆"**：反思是对过去的判断，记忆是当前能看见的内容——前者是后者的来源，但内容质量不等于上下文有效性。
- ❌ **把自进化等同于"Agent 可以改自己"**：自进化的关键是结构可塑性 + 因果归因 + 安全治理三个支柱，单纯允许修改不足以构成自进化。
- ❌ **认为 AutoGPT 已经实现自进化**：AutoGPT 的 prompt 和工具集在运行时不变，它只是循环执行 LLM 决策；真正的自进化需要修改 Agent 系统本身。

## 参考文献（本章内）

1. Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR. [$TRAE_REF](https://arxiv.org/abs/2210.03629)
2. Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS. [$TRAE_REF](https://arxiv.org/abs/2303.11366)
3. Significant Gravitas. (2023). *Auto-GPT: An Autonomous GPT-4 Experiment*. GitHub.
4. Nakajima, Y. (2023). *BabyAGI: An Autonomous AI Agent System*. GitHub.
5. Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. NeurIPS. [$TRAE_REF](https://arxiv.org/abs/2302.04761)
6. OpenAI. (2024). *Function Calling and Other API Updates*. Official Documentation. [$TRAE_REF](https://platform.openai.com/docs/guides/function-calling)
7. Yang, C., et al. (2024). *Large Language Models as Optimizers (OPRO)*. ICLR. [$TRAE_REF](https://arxiv.org/abs/2309.03409)
8. Cai, T., et al. (2023). *Large Language Models as Tool Makers (LATM)*. arXiv:2305.17126. [$TRAE_REF](https://arxiv.org/abs/2305.17126)
9. Xu, W., et al. (2025). *A-MEM: Agentic Memory for LLM Agents*. NeurIPS. [$TRAE_REF](https://arxiv.org/abs/2502.12110)
10. Robeyns, M., et al. (2025). *A Self-Improving Coding Agent (SICA)*. NeurIPS. [$TRAE_REF](https://arxiv.org/abs/2504.15228)
11. Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407. [$TRAE_REF](https://arxiv.org/abs/2508.07407)

---

> **本章进度**：1.1–1.5 节全部完成（约 6,500 字，含 5 张 SVG 配图，达到 16 页计划）。`status: final`，进入 Leanpub v0.1 上线阶段。
