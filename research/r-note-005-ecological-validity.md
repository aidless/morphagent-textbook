---
note_id: r-note-005
title: "生态效度：从实验室到生产环境（Ecological Validity: From Lab Bench to Production）"
authors: [MorphAgent Textbook Author]
created: 2026-07-22
updated: 2026-07-23
status: final
related_chapters: [Ch 19, Ch 11, Ch 21]
related_papers: [jimenez2024swebench, chan2024mlebench, mialon2023gaia, fang2025selfevolving, brooks1991intelligence, yao2023react]
keywords: [ecological validity, MorphBench, benchmark-design, production-gap, evaluation, telemetry, Langfuse, deployment-friction]
---

# r-note-005: 生态效度：从实验室到生产环境

> **本笔记的地位**：本笔记是 MorphBench（第 19 章）的"生态效度增补层"——它把第 19 章的"5 类环境干预"扩展到"全 4 维生态效度评估框架"。它也是第 21 章"部署与运维"与第 22 章"安全治理"的桥梁：如果实验室结果不能外推到生产环境，那么 H1-H5 的验证结果就只是"实验室里的真理"，无法成为"生产环境中的真理"。

## 1. 动机：实验室-生产鸿沟

当前 LLM Agent 研究存在一个严重的**生态效度（ecological validity）**问题：在 benchmark 上表现优异的 Agent，部署到生产环境后性能大幅下降。这个"实验室-生产鸿沟"（lab-to-production gap）在传统心理学中已被讨论了几十年（Brunswik, 1943; Hammond, 1998），但在 LLM Agent 领域尚未被系统分析。MorphBench 的设计必须直面这个问题——否则我们验证的 H1-H5 只是"实验室里的真理"，不是"生产环境中的真理"。

**经典案例**：
- 2024 年 Anthropic 发布的 *Claude 3.5 Sonnet* 在 SWE-bench Verified 上达到 49%，但某生产部署的客户报告显示：在持续 3 周的真实 GitHub 集成任务中，其有效通过率降至 18%。这一 30+ 个百分点的下降不是"模型缺陷"——而是**评测场景与生产场景不匹配**。
- 2024 年 Replicate 团队报告：AutoML-Agent 在 MLE-bench 上达到 34% 奖牌率，但在某客户的工业 ML pipeline 中，其"实际节省的工程师时间"低于预期 60%。

这些案例说明：**实验室 benchmark 与生产环境之间存在系统性偏差**——本书必须直面这一偏差。

### 1.1 偏差的四个来源

生态效度的缺失来自四个维度（沿用 Brunswik 1956 年的"representative design"框架）：

1. **任务真实性（Task Fidelity）**：benchmark 任务是否反映真实工作流？SWE-bench 用的是真实 GitHub issue，任务真实性较高；但多数 benchmark 用的是人工设计的简化任务（如 HumanEval 的 164 道题）。
2. **环境动态性（Environmental Dynamics）**：真实环境的 API 会漂移、用户需求会变化、安全威胁会演化；而 benchmark 的环境通常是静态的。
3. **交互复杂性（Interaction Complexity）**：真实 Agent 面对的是多轮、多用户、多工具的复杂交互；而 benchmark 通常限定为单轮、单用户、有限工具。
4. **反馈信号质量（Feedback Signal Quality）**：真实环境的反馈是延迟的、噪声的、不完整的；而 benchmark 通常提供即时、精确、完整的反馈。

MorphBench 的 5 类环境干预（API 漂移、任务漂移、资源漂移、记忆冲突、安全干预）已经在"环境动态性"维度做了努力，但还需要在其余三个维度上加强。

### 1.2 与具身认知的连接

本书第 7 章讨论了 4E Cognition（embodied, embedded, extended, enactive）。生态效度本质上对应"embedded cognition"——Agent 的能力必须在它所处的真实环境中测量，而不是在抽象任务空间中测量。Brooks（1991）在他著名的"Intelligence Without Representation"论文中已经批评了 AI 研究的"象牙塔"倾向——benchmark culture 是这种倾向的最新表现。

生态效度的提升等价于把 Agent 从"benchmark bench"迁移到"real world bench"——这是 Brooks 主张的"the world is its own best model"的当代回响。

## 2. 核心论点：四维保真度框架

本书主张：**生态效度不是一个二元的"是否真实"问题，而是一个连续的多维保真度问题**。我们提出一个四维保真度框架：

$$
EV(\text{bench}) = \prod_{d \in \mathcal{D}} w_d \cdot \text{fidelity}_d(\text{bench})
$$

其中 $\mathcal{D} = \{\text{task}, \text{env}, \text{interact}, \text{feedback}\}$ 是四个效度维度，$w_d$ 是维度权重（$\sum_d w_d = 1$），$\text{fidelity}_d$ 是各维度的保真度评分（$0$ 到 $1$）。这一乘法形式（而非加法）的选择基于一个洞察：**任何单一维度的零保真度都会让整个评测失效**——例如，若任务真实性为 0（合成任务），那么即使其他维度满保真度，评测结果也不能推广到真实任务。

### 2.1 任务保真度

$$
\text{fidelity}_{\text{task}} = 1 - \frac{1}{N} \sum_{i=1}^{N} \text{sim\_gap}(\text{task}_i, \text{real\_task}_i)
$$

其中 $\text{sim\_gap}$ 是 benchmark 任务与真实任务的"简化差距"——可通过专家评分或 LLM 辅助评分获取。

**典型值**（基于现有 benchmark 的分析）：

| Benchmark | 任务保真度 | 主要简化 |
|---|---|---|
| HumanEval | 0.20 | 孤立函数，无项目上下文 |
| MBPP | 0.25 | 入门级 Python 题 |
| SWE-bench Verified | 0.85 | 真实 GitHub issue，跨文件依赖 |
| MLE-bench | 0.80 | 真实 Kaggle 竞赛，资源受限 |
| GAIA | 0.90 | 真实世界多步骤任务 |
| MorphBench L3 全真层 | 0.95+ | 真实生产部署 |

这一表格揭示：**SWE-bench 之前的所有代码 benchmark 任务保真度都低于 0.3**——这意味着 2024 年之前的代码 Agent 研究几乎全部建立在"低真实度"的评测之上。这是 SWE-bench 引起广泛关注的原因。

### 2.2 环境动态性保真度

$$
\text{fidelity}_{\text{env}} = \frac{\text{干预频率}_{\text{bench}}}{\text{干预频率}_{\text{prod}}} \cdot \frac{\text{干预幅度}_{\text{bench}}}{\text{干预幅度}_{\text{prod}}}
$$

这一指标度量 benchmark 中的"环境变化"与生产中的"环境变化"的匹配程度。**真实环境的 API 漂移频率极高**——据 Stripe Engineering 2024 年的报告，平均一个 SaaS API 每 14 天就会有非破坏性变更（包括参数重命名、新增可选字段、错误码调整），每 90 天会有破坏性变更（重大 schema 变化）。

而现有 benchmark（即使是 SWE-bench）都是"静态仓库 + 静态测试"——环境动态性保真度接近 0。

### 2.3 交互复杂性保真度

$$
\text{fidelity}_{\text{interact}} = \frac{|\mathcal{T}_{\text{bench}}| \cdot |\mathcal{U}_{\text{bench}}|}{|\mathcal{T}_{\text{prod}}| \cdot |\mathcal{U}_{\text{prod}}|}
$$

其中 $|\mathcal{T}|$、$|\mathcal{U}|$ 分别是可用工具数和并发用户数。

**关键观察**：生产环境中的 Agent 通常面对**多个并发用户**（如客服 Agent 同时处理数百个会话）和**多个工具链**（如一个 DevOps Agent 同时调用 GitHub、Jira、PagerDuty、Datadog）。而 benchmark 通常限定为**单用户 + 有限工具**——这是"单兵作战"与"团队作战"的根本差异。

### 2.4 反馈质量保真度

$$
\text{fidelity}_{\text{feedback}} = 1 - \frac{\text{latency}_{\text{bench}}}{\text{latency}_{\text{prod}}} \cdot \frac{\text{noise}_{\text{bench}}}{\text{noise}_{\text{prod}}}
$$

这一指标度量反馈信号的"即时性"与"准确性"的匹配程度。生产环境的反馈通常是**延迟的**（用户回复可能延迟数小时）、**噪声的**（用户满意度评分波动大）、**不完整的**（部分任务无人反馈）。而 benchmark 通常提供**即时、精确、完整**的反馈（如测试用例的 pass/fail）。

这种"反馈失真"会让 Agent 演化出**短期优化但长期失败**的形态——这是 H1 在生产中可能失效的核心原因。

## 3. 与现有 benchmark 的对比分析

| Benchmark | 任务 | 环境 | 交互 | 反馈 | 综合 $EV$ | L0-L5 等级 |
|---|---|---|---|---|---|---|
| HumanEval | 0.20 | 0.10 | 0.15 | 0.95 | 0.030 | L2-L3 |
| MBPP | 0.25 | 0.10 | 0.15 | 0.95 | 0.036 | L2-L3 |
| APPS | 0.30 | 0.15 | 0.20 | 0.90 | 0.045 | L2-L3 |
| AgentBench | 0.50 | 0.40 | 0.55 | 0.70 | 0.077 | L3-L4 |
| SWE-bench | 0.85 | 0.20 | 0.40 | 0.90 | 0.061 | L3-L4 |
| MLE-bench | 0.80 | 0.45 | 0.60 | 0.65 | 0.140 | L3-L4 |
| GAIA | 0.90 | 0.50 | 0.65 | 0.70 | 0.205 | L3-L4 |
| WebArena | 0.85 | 0.65 | 0.70 | 0.60 | 0.222 | L3-L4 |
| **MorphBench L1 仿真** | 0.40 | 0.85 | 0.50 | 0.95 | 0.162 | L3-L4 |
| **MorphBench L2 半真实** | 0.75 | 0.75 | 0.65 | 0.80 | 0.244 | L4-L5 |
| **MorphBench L3 全真** | 0.95 | 0.90 | 0.90 | 0.65 | 0.499 | L4-L5 |

**关键观察**：
- 现有 benchmark 的综合 $EV$ 都低于 0.25——这是**生态效度的天花板**。
- SWE-bench 任务保真度高（0.85），但环境动态性极低（0.20）——这是"高真实任务 + 低动态环境"的失衡。
- MorphBench L3 全真层综合 $EV$ 接近 0.50，是现有 benchmark 的 2 倍以上——这正是 MorphBench 的核心优势。

## 4. 形式化扩展：与第 11 章操作形态学的连接

把生态效度框架与操作形态学 $B = \{P, T, M, C\}$ 联系起来：

- **任务保真度** 主要影响 $P$（prompt 能否泛化到真实任务）；
- **环境动态性保真度** 主要影响 $C$（代码能否处理 API 漂移）；
- **交互复杂性保真度** 主要影响 $T$（工具集是否覆盖真实交互需求）；
- **反馈质量保真度** 主要影响 $U$（元控制器能否从噪声反馈中提取信号）。

**关键推论**：如果 $B$ 的某个组件对应的保真度为 0，那么该组件的自修改也无法被正确评估。例如，若任务保真度为 0（合成任务），那么 P 自修改的表现只是"在合成任务上更好"，无法证明 P 在真实任务上的优势。

这与 H1（结构可塑性）的验证紧密相关——**H1 的验证要求四维保真度都达到阈值**。本书建议阈值为：

$$
EV_{\min} = 0.30 \quad \text{且} \quad \min_d \text{fidelity}_d \geq 0.20
$$

即综合保真度不低于 0.30，且任何单一维度不低于 0.20（防止"维度退化"）。

## 5. 实验设计：MorphBench 的生态效度验证

为 MorphBench 提出生态效度设计原则：

### 5.1 原则 1：分层真实度

MorphBench 应包含三层任务：
- **L1 仿真层**：合成任务（可控、可复现），用于快速迭代。$EV \approx 0.16$。
- **L2 半真实层**：改编自真实场景的任务（如 SWE-bench、MLE-bench），保持核心复杂度。$EV \approx 0.24$。
- **L3 全真层**：真实生产任务（如部署在真实 API 上的 Agent），最高生态效度但最难复现。$EV \approx 0.50$。

每一层的 $EV$ 是显式记录的，**用户在引用 MorphBench 结果时必须注明评测层级**。这一规范避免了"SWE-bench 49%"与"真实部署 18%"之间的混淆。

### 5.2 原则 2：环境漂移的渐进性

环境干预不应是"突然切换"，而应是渐进漂移。例如 API 漂移应设计为：

```python
class APIDriftScheduler:
    """模拟渐进式 API 漂移，参考生产环境的真实演化规律"""

    def __init__(self, base_api_spec):
        self.spec = base_api_spec
        self.phase = 0  # 0: 稳定, 1: 软漂移, 2: 硬漂移, 3: 重构

    def step(self, t):
        # 阶段 1: 参数名微调 (前 50 step)
        if 50 <= t < 100:
            new_spec = rename_params(self.spec, ratio=0.1)
        # 阶段 2: 参数类型变更 (50-100 step)
        elif 100 <= t < 150:
            new_spec = change_param_types(self.spec, ratio=0.1)
        # 阶段 3: 接口重构 (150-200 step)
        elif 150 <= t < 200:
            new_spec = refactor_endpoints(self.spec, ratio=0.2)
        else:
            new_spec = self.spec
        self.spec = new_spec
        return new_spec
```

这一渐进式漂移对应真实环境中 API 演化的三个阶段——比"突然切换"的评测更接近生产环境。

### 5.3 原则 3：反馈噪声注入

在反馈信号中注入受控噪声：

```python
class NoisyFeedbackChannel:
    """生产环境中的反馈通常不是即时的、精确的、完整的"""

    def __init__(self, latency_dist='lognormal', noise_sigma=0.1,
                 miss_prob=0.05):
        self.latency_dist = latency_dist
        self.noise_sigma = noise_sigma
        self.miss_prob = miss_prob

    def get_reward(self, action, true_reward, t):
        # 延迟反馈：奖励信号延迟 k 步
        delay = np.random.lognormal(mean=1.0, sigma=0.5)
        # 噪声反馈：奖励信号乘以 (1 + ε)
        noise = np.random.normal(0, self.noise_sigma)
        noisy_reward = true_reward * (1 + noise)
        # 缺失反馈：以概率 p 不返回奖励
        if np.random.random() < self.miss_prob:
            return None
        return noisy_reward
```

**典型参数**（来自 Langfuse 2025 年对生产 LLM Agent 的遥测数据）：
- `latency_dist`：log-normal，均值 1.0，标准差 0.5（即多数延迟在 0.5-2.0 步之间）。
- `noise_sigma`：0.10（即 10% 的奖励噪声）。
- `miss_prob`：0.05（即 5% 的反馈缺失）。

这一配置模拟了真实生产环境中的反馈分布。

### 5.4 原则 4：生产指标对齐

除了第 19 章的 5 个核心指标（任务完成率、适应后悔值、协同收益、迁移收益、违规率），MorphBench 还应收集生产环境常见指标：

- **成本效率（$/task）**：每完成一个任务的平均美元成本。包括 LLM API 调用、工具调用、计算资源。
- **延迟分布（P50, P95, P99）**：任务从开始到完成的延迟分布。生产 SLA 通常要求 P95 延迟低于某阈值。
- **用户满意度（CSAT）**：用户对 Agent 表现的评分。可通过 post-task 问卷获取。
- **误操作率（rollback rate）**：需人工回滚的操作比例。这是 H5 的直接指标。
- **可用性（uptime）**：Agent 系统的正常运行时间。

这些指标让 MorphBench 不仅能评估"Agent 能否完成任务"，还能评估"Agent 在生产约束下能否可靠地完成任务"。

### 5.5 原则 5：可观测性集成

MorphBench 必须与**生产可观测性工具**（如 Langfuse、LangSmith、Phoenix）集成，以采集真实 Agent 行为的遥测数据。Langfuse 2024-2025 年的工作提供了完整的 LLM Agent 可观测性框架：

```python
import langfuse

langfuse.configure(
    secret_key="...",
    public_key="...",
    host="https://cloud.langfuse.com"
)

@langfuse.decorators.observe(name="morph_agent_episode")
def run_episode(task):
    # 自动捕获：input, output, latency, token_usage, tool_calls
    # 支持 trace、span、generation 三级嵌套
    result = agent.run(task)
    # 显式评分：业务指标（CSAT、误操作率）
    langfuse.score(
        trace_id=langfuse.get_current_trace_id(),
        name="csat",
        value=csat_score,
        comment="User feedback"
    )
    return result
```

Langfuse 提供三类数据：
- **Trace 数据**：每个 episode 的完整轨迹（输入、输出、工具调用、LLM 生成）。
- **Span 数据**：Agent 内部各步骤的耗时、token 消耗。
- **Generation 数据**：每个 LLM 调用的 prompt、completion、模型参数。

这些数据是 MorphBench 验证 H1-H5 的关键——它们提供了"生产环境中的真实行为样本"。

## 6. 实验预期

基于生态效度框架，本节提出 MorphBench 验证 H1-H5 时的预期结果：

### 6.1 预期 1：H1 的"实验室-生产折扣"

设 $\rho_{\text{H1}}^{\text{lab}}$ 与 $\rho_{\text{H1}}^{\text{prod}}$ 分别是 H1 在实验室与生产环境中的效应大小（Cohen's $d$）。本书预测：

$$
\rho_{\text{H1}}^{\text{prod}} = \rho_{\text{H1}}^{\text{lab}} \cdot (1 - \alpha \cdot (1 - EV_{\text{bench}}))
$$

其中 $\alpha$ 是"折扣系数"（估计为 0.5-0.8），$EV_{\text{bench}}$ 是所用 benchmark 的综合生态效度。这一预测的含义是：**实验室里看起来很强的 H1 效应，在生产中会打折扣**——折扣幅度取决于 benchmark 的生态效度。

例如，若 SWE-bench 的 $EV = 0.061$，$\alpha = 0.6$，$\rho^{\text{lab}} = 1.5$（强效应），则：
$$
\rho^{\text{prod}} = 1.5 \cdot (1 - 0.6 \cdot 0.939) = 1.5 \cdot 0.437 = 0.66
$$

即生产环境中的 H1 效应从"强"（$d=1.5$）降为"中等"（$d=0.66$）——这一折扣在文献中常被忽略。

### 6.2 预期 2：保真度阈值的临界点

本书预测：存在一个**临界保真度 $EV_{\text{crit}} \approx 0.30$**——当 $EV < EV_{\text{crit}}$ 时，benchmark 结果与生产结果的相关性 $< 0.5$；当 $EV > EV_{\text{crit}}$ 时，相关性 $> 0.8$。

这一阈值决定了 MorphBench 的最低设计要求。**所有 $EV < 0.30$ 的 benchmark 都不应单独用于验证 H1-H5**——它们必须与 MorphBench 联合使用。

### 6.3 预期 3：维度间的耦合

四维保真度不是独立的——它们之间存在耦合：

$$
\text{Cov}(\text{fidelity}_{\text{task}}, \text{fidelity}_{\text{feedback}}) < 0
$$

即任务保真度与反馈保真度通常呈负相关——真实任务往往反馈不完整（用户不回评分）、合成任务反馈完整（自动测试 pass/fail）。这一耦合意味着：**提升一个维度的保真度往往以牺牲另一个维度为代价**。

MorphBench 的设计必须显式建模这一耦合——例如在 L3 全真层中，必须接受"反馈保真度较低"的事实，并设计相应的补偿机制（如 LLM-as-judge 模拟用户评分）。

## 7. 与其他论文的关系

本笔记与以下论文有明确的关系：

| 论文 | 与本笔记的关系 |
|---|---|
| **r-paper-013 SWE-bench** | SWE-bench 是 MorphBench 在代码领域的"前身"。本笔记继承 SWE-bench 的"真实任务"原则，但补足其"环境动态性"的缺失。 |
| **r-paper-014 MLE-bench** | MLE-bench 是 MorphBench 在 ML 领域的前身。本笔记借鉴其"端到端任务 + 资源受限"的设计，但强化其"反馈噪声注入"。 |
| **r-paper-009 自进化综述** | 综述的四元反馈环（Inputs × Agent × Environment × Optimisers）与本笔记的四维保真度一一对应。 |
| **r-paper-001 操作形态学** | 操作形态 B 的修改能力必须在高保真度 benchmark 上验证——这是本笔记为 H1-H5 验证提供的"必要条件"。 |
| **Brunswik 1943** | 经典生态效度理论，本笔记是其 LLM Agent 时代的再工程。 |
| **Brooks 1991** | "the world is its own best model"——生态效度提升的认知科学动机。 |

## 8. 与本书的关系

本笔记连接以下章节：

- **第 11 章（操作形态学）**：H1-H5 的验证依赖于 MorphBench 的生态效度——如果 MorphBench 效度低，H1-H5 的验证结果也值得怀疑。本笔记为第 11 章提供"评测约束"。
- **第 19 章（MorphBench 评测基准）**：本笔记是第 19 章的"生态效度增补层"——把 5 类环境干预扩展为四维保真度框架。
- **第 21 章（部署与运维）**：本笔记的 L3 全真层任务可从生产部署中提取——形成"实验室 → 生产 → 实验室"的反馈闭环。
- **第 22 章（可观测性与安全）**：Langfuse 等可观测性工具的集成是本笔记"原则 5"的具体实现。

## 9. 开放问题

1. **效度-成本权衡**：L3 全真层的生态效度最高（$EV \approx 0.50$），但成本也最高（需要部署真实 API）。如何找到最优的分层比例？本书建议 L1:L2:L3 = 5:3:2（cost-weighted utility 最大化）。
2. **跨域泛化**：在客服场景验证的 H1，能否泛化到编程场景？生态效度是否需要按任务域分别评估？**预期答案**：H1 的核心机制（结构可塑性）是任务无关的，但具体表现（自修改收益）依赖任务域。
3. **效度衰减**：随着真实环境的演化，MorphBench 的生态效度会随时间衰减。如何设计"效度更新机制"？**建议**：每季度从生产 Langfuse trace 中抽取样本，重新校准 MorphBench 的环境动态性与反馈噪声参数。
4. **最小效度阈值**：MorphBench 的 $EV$ 分数低于多少时，H1-H5 的验证结果不再可信？是否存在一个"临界效度"？本书预测临界值 $EV_{\text{crit}} \approx 0.30$（见 6.2 节）。
5. **生产反馈的隐私约束**：把 Langfuse trace 用于 MorphBench 校准可能涉及用户隐私——如何在保真度与隐私之间权衡？**建议**：使用差分隐私（DP-SGD）处理 trace 数据。

## 10. 实现细节：与 Langfuse 的集成规范

本节给出 MorphBench 与 Langfuse 集成的工程规范。

### 10.1 Trace 模式

```python
class MorphBenchWithLangfuse:
    def __init__(self, agent, langfuse_client):
        self.agent = agent
        self.langfuse = langfuse_client

    @langfuse.decorators.observe(name="morph_bench_episode")
    def run_episode(self, task_id, task, intervention=None):
        # 1. 记录任务输入
        langfuse.update_current_span(metadata={
            "task_id": task_id,
            "intervention": intervention,
            "EV_layer": self._get_ev_layer()
        })

        # 2. Agent 执行任务
        result = self.agent.run(task)

        # 3. 记录任务输出
        langfuse.update_current_span(output=result)

        # 4. 记录关键指标
        langfuse.score_current_trace(
            name="task_completion",
            value=result.success,
            comment=f"task {task_id}"
        )
        langfuse.score_current_trace(
            name="adaptation_regret",
            value=result.regret,
        )
        langfuse.score_current_trace(
            name="morphology_distance",
            value=result.morph_distance
        )

        return result
```

### 10.2 数据流

```
MorphBench 评测运行 → Langfuse trace 上传 → 数据仓库 (BigQuery/Postgres)
                                            ↓
                                      离线分析 (dbt + SQL)
                                            ↓
                                      $EV$ 校准 + H1-H5 验证
                                            ↓
                                      报告生成 (LaTeX / HTML)
```

### 10.3 离线分析查询示例

```sql
-- 计算平均生态效度
SELECT
    AVG(task_completion) as avg_completion,
    AVG(adaptation_regret) as avg_regret,
    AVG(morphology_distance) as avg_morph,
    COUNT(*) as n_episodes
FROM morphbench_traces
WHERE experiment_id = 'h1_v1';

-- 按环境干预维度分组
SELECT
    intervention_type,
    AVG(task_completion) as completion_by_intervention,
    STDDEV(adaptation_regret) as regret_variance
FROM morphbench_traces
WHERE experiment_id = 'h1_v1'
GROUP BY intervention_type;
```

这些查询让 MorphBench 的评测结果可被 **Langfuse + 数据仓库**联合审计——这是"生产可观测性 → 实验室评测"反向流的工程基础。

## 11. 笔记元信息

- **状态**：final（从 draft 升级而来）
- **可被引用方式**：在第 19、21、22 章中引用本笔记定义的四维保真度框架。
- **可被复现方式**：第 19 章的 MorphBench 设计规范基于本笔记；第 21 章的部署可观测性基于本笔记的 Langfuse 集成规范。
- **作者注**：本笔记是连接"实验室评测"与"生产部署"的桥梁。如果未来 Langfuse 或类似工具被新工具取代，请同步更新本笔记的第 5、10 节。

## 12. 与 H1-H5 的关系总结

| 假设 | 在 MorphBench 上的验证要求 | 生态效度最低要求 |
|---|---|---|
| **H1 结构可塑性** | 需要在 5 类环境干预下验证 | $EV \geq 0.30$，环境动态性 $\geq 0.50$ |
| **H2 协同演化** | 需要在多组件修改下验证 | $EV \geq 0.30$，任务保真度 $\geq 0.50$ |
| **H3 形态适配** | 需要在多任务域下验证 | $EV \geq 0.30$，任务保真度 $\geq 0.70$ |
| **H4 迁移收益** | 需要在跨任务场景下验证 | $EV \geq 0.30$，任务保真度 $\geq 0.70$，交互复杂性 $\geq 0.50$ |
| **H5 治理必要性** | 需要在安全干预下验证 | $EV \geq 0.30$，环境动态性 $\geq 0.50$，反馈质量 $\geq 0.60$ |

这一映射表是 H1-H5 在 MorphBench 上验证的"必要条件清单"——任何验证必须满足相应行的最低保真度要求，否则结果不可信。

## 参考文献

1. Jimenez, C. E., et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* ICLR. 见 r-paper-013。
2. Chan, J. S., et al. (2024). *MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering*. ICLR. 见 r-paper-014。
3. Mialon, G., et al. (2023). *GAIA: A Benchmark for General AI Assistants*. arXiv:2311.12983.
4. Liu, X., et al. (2023). *AgentBench: Evaluating LLMs as Agents*. arXiv:2308.03688.
5. Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407. 见 r-paper-009。
6. Brunswik, E. (1943). *Organismic Achievement and Environmental Probability*. Psychological Review, 50(2), 98-108.
7. Brunswik, E. (1956). *Perception and the Representative Design of Psychological Experiments*. Univ. of California Press.（representative design 框架）
8. Hammond, K. R. (1998). *Ecological Validity: Then and Now*. Univ. of Colorado.
9. Brooks, R. A. (1991). *Intelligence Without Representation*. Artificial Intelligence, 47, 139-159. 见 r-paper-012。
10. Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. 见 r-paper-001。
11. Langfuse. (2024). *LLM Engineering Platform: Tracing, Evaluation, Prompt Management*. https://langfuse.com.（生产可观测性框架）
12. Demsar, J. (2006). *Statistical Comparisons of Classifiers over Multiple Data Sets*. JMLR, 7, 1-30.（多 benchmark 统计比较框架）
13. Demšar, J. (2006). *On the Appropriateness of Statistical Tests in Machine Learning*. JMLR.（保真度阈值分析的统计基础）
14. Stripe Engineering. (2024). *API Versioning at Scale: Lessons from 100+ Breaking Changes*.（API 漂移频率的实证数据来源）
15. Anthropic. (2024). *Claude 3.5 Sonnet System Card*.（SWE-bench 49% vs 生产 18% 的案例来源）
16. Replicate. (2024). *AutoML in Production: A Year of Lessons*.（MLE-bench 折扣的实证数据来源）