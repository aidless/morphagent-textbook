---
note_id: r-note-003
title: "P/T/M/C 协同进化的理论框架"
authors: [MorphAgent Textbook Author]
created: 2026-07-22
updated: 2026-07-23
status: final
related_chapters: [Ch 11, Ch 16, Ch 19]
related_papers: [fang2025selfevolving, yang2024opro, cai2023latm, xu2025amem, robeyns2025sica, yin2024godelagent, khattab2024dspy, yao2023react, packer2023memgpt, shinn2023reflexion]
keywords: [synergy, H2, cross-component, coordination-function, meta-controller, superadditivity, combinatorial-optimization, joint-coordinated, joint-independent, coupling-matrix]
---

# r-note-003: P/T/M/C 协同进化的理论框架

> H2（协同演化假设）断言：联合修改 P/T/M/C 四组件的效果超过各组件独立优化效果的简单相加。这是一个**超加性（superadditivity）**命题——本质上等于"操作形态的联合修改空间中存在跨组件的相关结构"。本笔记从组合优化理论、信息论、演化生物学三个角度为 H2 建立理论框架，定义协同度评分函数 S(B)，并构造 Joint-Coordinated vs Joint-Independent 两组对照实验来验证 H2。本笔记是第 16 章"跨组件协同自进化"的理论基石，也是 r-paper-007 (Gödel Agent) 与 r-paper-006 (SICA) 的协同维度解读。

## 1. 动机：为什么协同不是"理所当然"的

直观上，似乎"联合修改所有组件"一定优于"独立优化每个组件"——但这一直觉在组合优化理论中是**错误的**。著名的 **No Free Lunch Theorem**（Wolpert 1996）指出，没有哪种搜索算法在所有问题域上都优于其他算法；**协同策略的有效性高度依赖于组件间的耦合结构**。

具体到操作形态学 $B = \{P, T, M, C\}$：

- 如果 P、T、M、C 互相独立（即修改 P 不影响 T 的最优选择），那么联合修改等价于独立修改——**没有协同空间**。
- 如果 P、T、M、C 强耦合（即修改 P 必须配套修改 T），那么独立修改可能产生"次优解"——**协同空间巨大**。

H2 的本质是：操作形态 B 的四个组件之间存在**非平凡的耦合结构**，独立优化会忽略这种结构，导致次优解。这是 H1（结构可塑性）的"深度版"——H1 关心"修改能力是否有用"，H2 关心"修改是否需要联合进行"。

## 2. 核心论点：协同是**耦合结构 + 协调机制**的产物

H2 的理论基础来自三个领域：

### 2.1 系统论：耦合结构的本体论

操作形态 $B = \{P, T, M, C\}$ 的四个组件不是孤立的对象，而是**互相塑造的耦合系统**：

- **P ↔ T**：Prompt 中声明的工具签名必须与 T 中实际可调用的工具匹配。如果 U 修改了 T 添加新工具，P 必须相应更新（声明新工具）。
- **P ↔ M**：Prompt 中引用的记忆内容（如 few-shot examples）必须与 M 中实际存储的一致。如果 M 删除了某些记忆条目，P 中引用这些条目的 few-shot 会失效。
- **T ↔ M**：工具调用产生的输出可能被存入 M。如果工具签名改变，存储在 M 中的旧输出可能无法被正确解析。
- **C ↔ (P, T, M)**：C 是执行机制，必须与 P、T、M 协同。如果 C 是 ReAct 循环，T 必须是 function-calling 兼容的；如果 C 是 Plan-then-Execute，M 必须支持长视野规划。

这些耦合关系意味着：**修改一个组件可能"打破"与其他组件的协议**——这就是协同的核心动机。

### 2.2 强化学习：多优化器冲突的解决

如果四个组件各自被一个独立的元控制器（$U_P$、$U_T$、$U_M$、$U_C$）优化，这些优化器可能**互相冲突**：

- $U_P$ 加长了 prompt 以提高准确性，但 $U_M$ 删除了相关记忆条目导致上下文缺失；
- $U_T$ 删除了一个工具以减少干扰，但 $U_C$ 的反思机制依赖这个工具的输出；
- $U_C$ 修改了核心循环的子函数，但 $U_P$ 的 few-shot examples 引用了旧子函数的输出格式。

独立优化器无法感知这些冲突——它们各自追求"局部最优"，但总体上可能是次优的。**统一元控制器 U**（协同策略）能感知冲突，并做出"局部次优但全局更优"的修改决策。

### 2.3 演化生物学：多性状协同演化（pleiotropy）

生物体的多个性状不是独立演化的，而是受到 **pleiotropy（基因多效性）** 的约束——单个基因同时影响多个性状。这导致：

- **多效性约束**：修改"性状 X"必然影响"性状 Y"——独立选择 X 的最优基因型可能破坏 Y。
- **协同适应**：在长期演化中，多个性状会形成**协同适应（coadapted traits）**——它们"配合"得最好，因为它们一起被自然选择优化。

操作形态 B 的四个组件类似于生物体的多个性状：P、T、M、C 是被同一个 Agent 的目标共同选择的——它们应当演化出"协同适应"的稳态。**H2 实际上是 H3（形态适配）的微观机制**——不同环境选择不同的协同适应形态。

### 2.4 H2 的反命题

H2 的可能反面（如果 H2 被反驳，意义重大）：

- **"独立可加性"**：操作形态 B 的修改可以分解为独立组件的修改之和——联合修改只是"碰巧有效"，没有"协同结构"贡献。
- **"冲突为主"**：四个组件之间冲突多于耦合——联合修改可能反而比独立修改更差（因为 U 难以处理所有冲突）。
- **"天花板效应"**：单组件修改已经接近性能上界——联合修改无空间。

H2 的反驳将动摇操作形态学的工程基础——意味着"操作形态"概念本身需要重新审视。

## 3. 形式化

### 3.1 协同度评分函数 S(B)

H2 的核心可操作化形式是**协同度评分函数 $S(B)$**：

$$
S(B_t) = \frac{V(P_t, T_t, M_t, C_t) - V(P_0, T_0, M_0, C_0)}{\sum_{X \in \{P,T,M,C\}} [V(X_t, \cdot_{-X}) - V(X_0, \cdot_{-X})]}
$$

其中：
- $V(P_t, T_t, M_t, C_t)$ 是当前操作形态 B 在时刻 $t$ 的总体性能；
- $V(X_t, \cdot_{-X})$ 是仅修改组件 $X$ 而保持其他组件在初始值的性能；
- 分子是**联合修改的总收益**；
- 分母是**各组件独立修改收益之和**。

**判定准则**：

| $S$ 值 | 解读 | H2 状态 |
|---|---|---|
| $S > 1$ | 超加性（协同存在） | **H2 成立** |
| $S = 1$ | 加性（独立） | H2 被弱化（独立优化足够） |
| $S < 1$ | 次加性（冲突为主） | H2 被反驳 |

### 3.2 协同度的动态模型

$S$ 不是常数——它随时间变化（因为 B 在演化）。设 $S(t)$ 的时间导数为：

$$
\frac{dS}{dt} = \alpha \cdot \text{coupling\_strength}(B_t) - \beta \cdot \text{conflict\_rate}(U_P, U_T, U_M, U_C)
$$

其中：
- $\alpha$ 是耦合增益系数——组件耦合越强，$S$ 增长越快；
- $\beta$ 是优化器冲突惩罚系数——独立优化器越多，$S$ 增长越慢。

**关键预测**：存在两种极限：
- **强耦合 + 协同 U**：$S(t)$ 增长最快，H2 强成立；
- **弱耦合 + 独立 U**：$S(t)$ 接近 1，H2 弱成立；
- **强耦合 + 独立 U**：$S(t)$ 衰减甚至变成 $S < 1$，H2 被反驳。

### 3.3 耦合矩阵 Λ

定义组件间的耦合矩阵 $\Lambda$：

$$
\Lambda = \begin{pmatrix}
1 & \lambda_{PT} & \lambda_{PM} & \lambda_{PC} \\
\lambda_{TP} & 1 & \lambda_{TM} & \lambda_{TC} \\
\lambda_{MP} & \lambda_{MT} & 1 & \lambda_{MC} \\
\lambda_{CP} & \lambda_{CT} & \lambda_{CM} & 1
\end{pmatrix}
$$

其中 $\lambda_{XY} \in [-1, 1]$ 表示组件 $X$ 的修改对组件 $Y$ 的性能影响强度：

| $\lambda_{XY}$ 范围 | 含义 |
|---|---|
| $[0.7, 1]$ | 强耦合（X 修改必须配套修改 Y） |
| $[0.3, 0.7)$ | 中耦合（X 修改通常需要修改 Y） |
| $[-0.3, 0.3]$ | 弱耦合（X 修改基本不影响 Y） |
| $[-1, -0.3)$ | 强负耦合（X 修改会破坏 Y） |

**关键判据**：

- 若 $\Lambda$ 接近单位矩阵，说明组件独立，H2 倾向不成立；
- 若 $\Lambda$ 有显著非对角元素，说明组件耦合，H2 倾向成立；
- 若 $\Lambda$ 有显著负元素，说明存在破坏性耦合（独立修改可能引发"互毁"）。

**耦合矩阵的估计方法**：对每个组件进行"单因素扰动"——仅修改 P，保持 T/M/C 不变，观察其他组件的性能变化。例如：$\lambda_{PT}$ 通过"修改 P 后，T 在相同任务上的性能变化率"来估计。

### 3.4 协同优化的数学结构

H2 的形式化问题等价于一个**组合优化问题**：

$$
\max_{B \in \mathcal{B}} V(B) \quad \text{subject to } B \in \text{reachable}(B_0, U, T)
$$

其中 $\mathcal{B}$ 是所有可能的操作形态空间，reachable 是元控制器 U 在 T 步内可达的状态集合。

独立优化的搜索策略：

$$
B^* = \arg\max_{P} V(P, T_0, M_0, C_0) \cup \arg\max_{T} V(P^*, T, M_0, C_0) \cup \ldots
$$

协同优化的搜索策略：

$$
B^* = \arg\max_{B} V(P, T, M, C)
$$

协同优化的搜索空间是 $\mathcal{B} = \mathcal{P} \times \mathcal{T} \times \mathcal{M} \times \mathcal{C}$，维度远高于独立优化。这导致：

- **协同搜索更彻底**（考虑更多组合）；
- **协同搜索成本更高**（元控制器需要评估更多候选）；
- **协同搜索的回报是非线性的**（可能发现独立优化无法达到的"组合性最优解"）。

这与**组合拍卖理论**（combinatorial auction theory）中的"complementarity"概念同构——如果组件之间是互补品（complements），联合出价远高于独立出价之和；如果是替代品（substitutes），联合出价接近独立出价之和。

### 3.5 与组合优化理论的连接

H2 的命题可以重新表述为：

> **操作形态 B 的组件之间存在组合性互补（combinatorial complementarity）**，使得联合价值 $\geq$ 独立价值之和。

这一命题在以下领域有类似研究：

- **Feature selection**：相关特征联合选比独立选更有效（Guyon & Elisseeff 2003）；
- **Hyperparameter optimization**：某些超参数组合有非线性协同（Bergstra & Bengio 2012）；
- **Neural architecture search**：分层架构的组合选择（Zoph & Le 2017）；
- **Multi-task learning**：相关任务联合训练比独立训练更有效（Caruana 1997）。

这些领域的共同结论是：**协同效应的存在性高度依赖于问题的结构**。H2 不是"普适真理"，而是"在某些条件下成立"——这与 H1 的"边界条件"研究对应。

## 4. 实验设计

H2 的验证需要构造两组**对照实验**：

### 4.1 实验配置

| 实验配置 | 元控制器 | 优化策略 | 协同度预期 |
|---|---|---|---|
| **Frozen** | 无 | 不修改 | $S = 1$（基线） |
| **Independent-P** | OPRO | 独立优化 P（其他冻结） | $S$ 未定义（仅修改 P） |
| **Independent-T** | LATM | 独立优化 T | $S$ 未定义 |
| **Independent-M** | A-MEM | 独立优化 M | $S$ 未定义 |
| **Independent-C** | SICA | 独立优化 C | $S$ 未定义 |
| **Independent-All** | 四个独立 U | 各组件独立优化 | $S \leq 1$ |
| **Coordinated** | 统一 U | 协同优化全部 | $S > 1$（H2 预测） |

**核心对比**：Independent-All vs Coordinated。若 Coordinated 的 $S > 1$ 且显著高于 Independent-All，则 H2 被支持。

### 4.2 Joint-Coordinated 实验组设计

统一元控制器 U 的协同优化策略：

```python
class CoordinatedUC:
    def __init__(self, llm, frozen_components):
        self.llm = llm
        self.frozen = frozen_components  # 通常 L0 冻结
        self.coupling_matrix = np.zeros((4, 4))  # 估计的耦合矩阵

    def propose_modification(self, B_t, feedback):
        """协同修改: 提议一个联合修改 (delta_P, delta_T, delta_M, delta_C)"""
        # 1. 分析当前 B 的瓶颈
        bottleneck = self.diagnose_bottleneck(B_t, feedback)

        # 2. 基于瓶颈, 提议联合修改
        # 注意: 协同修改必须考虑组件间的耦合, 不是各自优化
        prompt = f"""
        当前操作形态 B:
          P = {B_t.P}
          T = {B_t.T}
          M = {B_t.M}
          C = {B_t.C}

        最近反馈: {feedback}
        估计的耦合矩阵: {self.coupling_matrix}

        提议一个联合修改 (P, T, M, C 都可改), 必须:
        1. 保持组件间的协议一致 (T 的工具签名与 P 中的声明匹配)
        2. 避免冲突 (不要让 P 的引用指向 M 已删除的条目)
        3. 同时考虑所有组件, 而不是只优化一个
        """
        delta_B = self.llm.generate(prompt)
        return parse_modification(delta_B)

    def update_coupling_estimate(self, old_B, new_B, delta_V):
        """根据每次修改的结果, 更新耦合矩阵的估计"""
        # 通过单因素扰动估计耦合强度
        # (实际实现中, 这是一个在线学习过程)
        pass
```

### 4.3 Joint-Independent 实验组设计

四个独立元控制器的非协同优化策略：

```python
class IndependentUs:
    def __init__(self, u_p, u_t, u_m, u_c):
        self.u_p = u_p  # 优化 P
        self.u_t = u_t  # 优化 T
        self.u_m = u_m  # 优化 M
        self.u_c = u_c  # 优化 C

    def propose_modifications(self, B_t, feedback):
        """独立修改: 每个 U 只优化自己的组件"""
        delta_P = self.u_p.propose(B_t.P, feedback)
        delta_T = self.u_t.propose(B_t.T, feedback)
        delta_M = self.u_m.propose(B_t.M, feedback)
        delta_C = self.u_c.propose(B_t.C, feedback)
        return delta_P, delta_T, delta_M, delta_C

    def apply_modifications(self, B_t, deltas):
        """独立应用修改, 可能产生冲突"""
        # 注意: 这里四个修改独立应用, 不做冲突检查
        new_P = apply_P(B_t.P, deltas[0])
        new_T = apply_T(B_t.T, deltas[1])
        new_M = apply_M(B_t.M, deltas[2])
        new_C = apply_C(B_t.C, deltas[3])
        return B(new_P, new_T, new_M, new_C)
```

### 4.4 协同度的计算

实验完成后，协同度 $S$ 的计算：

$$
S = \frac{V_{\text{coordinated}}^{\text{final}} - V_{\text{frozen}}}{V_{\text{independent}}^{\text{final}} - V_{\text{frozen}}}
$$

其中 $V_{\text{coordinated}}^{\text{final}}$ 是 Coordinated 组在 50 episode 后的最终性能，$V_{\text{independent}}^{\text{final}}$ 是 Independent-All 组在 50 episode 后的最终性能。

**H2 成立判定**：$S > 1$ 且 $S$ 的 95% bootstrap CI 不包含 1。

### 4.5 统计检验与功效分析

- **样本量**：30 次独立运行（per configuration），共 30 × 6 = 180 次实验。
- **统计检验**：Mann-Whitney U 检验（Independent-All vs Coordinated）。
- **多重比较校正**：Bonferroni 校正 $\alpha = 0.05 / 3 \approx 0.0167$（3 个核心比较）。
- **预期效应量**：参考 r-paper-006 (SICA) 与 r-paper-007 (Gödel Agent) 的经验，Coordinated vs Independent-All 的预期效应量 $d \in [0.3, 0.7]$。

### 4.6 与 r-paper-005 / r-paper-006 / r-paper-007 的对照

- **r-paper-005 (A-MEM)**：仅修改 M，且 M 的修改是"独立"的（不与其他组件协同）。这暗示 A-MEM 在 H2 框架下属于 Independent-M 组。
- **r-paper-006 (SICA)**：仅修改 C（且有限制范围）。SICA 是 Independent-C 的代表。
- **r-paper-007 (Gödel Agent)**：同时修改 P/T/M/U——这是**唯一直接实现 Coordinated 策略**的工作。Gödel Agent 的实验数据是 H2 的最强支持证据。

关键预测：如果 Gödel Agent 的实验结果（r-paper-007 §5）在 4 个任务上的提升（22%-62%）显著高于各 Independent 配置的提升之和，则 H2 被支持。

## 5. 实验预期与"何时 H2 可能失败"

### 5.1 H2 成立的预期效应量

| 任务类型 | 预期 S | 预期显著性 | 理由 |
|---|---|---|---|
| **强耦合任务**（如编码 + 工具调用 + 长视野记忆） | $S > 1.5$ | 强显著 | 组件间强耦合，协同搜索空间大 |
| **弱耦合任务**（如简单查询任务） | $S \approx 1.0$ | 不显著 | 组件间弱耦合，独立优化足够 |
| **冲突任务**（如 prompt 优化与 tool 优化方向相反） | $S < 1.0$ | H2 反驳 | 独立 U 反而更稳定 |

### 5.2 H2 的边界条件

H2 不是普适真理——它在以下条件下可能不成立：

| 边界条件 | 预测的 H2 表现 | 原因 |
|---|---|---|
| **LLM 元推理能力弱** | $S \approx 1.0$ | U 无法处理多组件协调 |
| **元控制器 U 训练不充分** | $S < 1.0$ | U 的协调能力差于"独立 + 人工合并" |
| **组件间无耦合** | $S \approx 1.0$ | 协同空间为空 |
| **组件间强冲突** | $S < 1.0$ | U 难以找到全局协调解 |
| **耦合结构未知** | $S \approx 1.0$ | U 无法利用耦合结构 |

### 5.3 S 上界的理论分析

理论上 $S$ 的最大值受限于：
1. **LLM 能力天花板**——U 必须在 LLM 的推理能力范围内；
2. **组合空间规模**——B 的可能形态数 $\prod_{X} |\mathcal{X}|$ 是有限的；
3. **环境信号噪声**——U 必须能从反馈中分辨"协同的收益"与"噪声"。

这三个上限共同决定了 $S$ 的工程可达值。在现有 LLM 能力下，$S$ 的工程上界预估为 $[1.0, 2.0]$——超过 2.0 的 $S$ 可能需要更强的元推理能力或更丰富的反馈信号。

## 6. 与本书的关系

### 6.1 与第 11 章的关系

第 11 章是 H2 的理论定义来源。本笔记是 H2 的**形式化与实验细化**——把第 11 章的"超加性"概念转化为可测量的 $S$ 函数，并设计 Joint-Coordinated vs Joint-Independent 的对照实验。如果本笔记的实验支持 H2，第 11 章的形式化得到验证；如果不支持，需要修订 H2 的命题。

### 6.2 与第 16 章的关系

第 16 章"跨组件协同自进化"是 H2 的**主要应用场景**——它包含具体的协同策略（顺序优化、并行协调、协商博弈）与实验设置。本笔记的 Joint-Coordinated 设计是第 16 章的核心实验之一，第 16 章的协同优化算法直接调用本笔记的框架。

### 6.3 与第 19 章的关系

第 19 章"MorphBench"评测框架包含 "Joint-Independent vs Joint-Coordinated" 的对比实验组。这一对比正是 H2 的核心检验。本笔记提供 H2 的形式化（$S$ 函数、耦合矩阵），第 19 章提供评测工具。

### 6.4 与其他论文的关系

- **r-paper-005 (A-MEM)**：A-MEM 是 M-only Independent 工作的代表。它修改 M 但不修改其他组件——这暗示 H2 在 A-MEM 框架下不可验证，因为没有 Joint 配置的对比。
- **r-paper-006 (SICA)**：SICA 是 C-only 工作。在 H2 框架下属于 Independent-C。但 SICA 修改的 C 可能"间接触发"其他组件的修改——这是 H2 的边界情况。
- **r-paper-007 (Gödel Agent)**：Gödel Agent 是 Coordinated 工作的代表——它同时修改 P/T/M/U。Gödel Agent 的实验数据是 H2 的直接证据。如果 Gödel Agent 的表现优于 Independent 配置之和，H2 被支持。
- **r-paper-008 (OPRO)**：P-only Independent 工作的代表。
- **r-paper-009 (selfevolving 综述)**：提供协同演化的分类学。
- **r-paper-002 (Reflexion)**：M-only Independent 工作的早期代表。

## 7. 开放问题

### 7.1 耦合矩阵的对称性

$\lambda_{XY}$ 是否等于 $\lambda_{YX}$？如果不对称，意味着"修改 P 对 T 的影响"不同于"修改 T 对 P 的影响"——这种不对称性对协同策略有重要启示。例如：P 修改可能比 T 修改"成本更高"（需要更多 LLM 调用），那么优化策略应当倾向于少修改 P、多修改 T。

### 7.2 S 的理论上限

$S$ 的最大值是多少？是否受限于 LLM 的能力天花板？理论上 $S$ 可以任意大（如果 B 的修改空间足够大），但实际工程中受限于搜索效率与元控制器能力。

### 7.3 协同策略的学习

统一元控制器 U 如何学习到"最优协同策略"？这是一个**元学习（meta-learning）**问题——U 不仅要学"如何修改 B"，还要学"如何在 P、T、M、C 之间分配修改预算"。这一学习过程需要什么类型的训练数据？

### 7.4 部分协同

当只有 2-3 个组件被协同优化时，$S$ 的行为如何？是否存在"最小协同集合"——比如"P+T 是关键，T+M 弱协同，P+M 强协同"——这一结构可以通过耦合矩阵的子矩阵分析得出。

### 7.5 协同与对抗的平衡

如果 U 是协同的，但环境有对手（adversarial），U 应该协同还是分散？这一博弈论问题与第 22 章"对抗鲁棒性"直接相关。

### 7.6 跨任务迁移的协同结构

不同任务下的 $\Lambda$ 是否相似？如果某些任务的 $\Lambda$ 共享结构，那么 U 可以通过元学习"迁移协同策略"——这是 H4（迁移收益）在协同维度的延伸。

## 8. H1-H5 映射表

| 假设 | H2 的角色 | 检验状态 |
|---|---|---|
| **H1 结构可塑性** | H2 的前提：单组件修改有意义 | 依赖 H1 成立 |
| **H2 协同演化** | **本笔记的核心** | 待验证（实验方案已设计） |
| **H3 形态适配** | H2 的应用：不同环境的耦合结构 | 依赖 H2 成立 |
| **H4 迁移收益** | H2 的延伸：跨任务的协同迁移 | 依赖 H2 成立 |
| **H5 治理必要性** | H2 的对照：协同 vs 治理 | 互为补充（协同可能减少治理负担） |

## 9. 笔记元信息

- **状态**：final
- **可被引用方式**：`{cite:p}` 风格在第 16 章、第 19 章中引用本笔记作为协同度评分函数 $S$ 的形式化基础。
- **可被复现方式**：实验代码位于 `experiments/exp-18-joint-evolution/`，使用 `_shared/metrics.py` 中的 $S$ 计算函数。
- **作者注**：本笔记是 H2 的形式化与实验设计的唯一权威来源。如果未来 H2 实验结果与本笔记的预期不一致，需要同步修改 $S$ 的形式化与第 11 章的 H2 命题。

## 参考文献

1. fang2025selfevolving: Fang, J., et al. (2025). *A Comprehensive Survey of Self-Evolving AI Agents*. arXiv:2508.07407. 见 r-paper-009。（H2 实验的整体框架参考）
2. yang2024opro: Yang, C., et al. (2024). *Large Language Models as Optimizers (OPRO)*. ICLR. 见 r-paper-008。（P-only Independent 配置的实现基础）
3. cai2023latm: Cai, T., et al. (2023). *Large Language Models as Tool Makers (LATM)*. arXiv:2305.17126。（T-only Independent 配置的实现基础）
4. xu2025amem: Xu, W., et al. (2025). *A-MEM: Agentic Memory for LLM Agents*. NeurIPS. 见 r-paper-005。（M-only Independent 配置的实现基础）
5. robeyns2025sica: Robeyns, M., et al. (2025). *SICA: Self-Improving Coding Agent*. NeurIPS. 见 r-paper-006。（C-only Independent 配置的实现基础）
6. yin2024godelagent: Yin, X., et al. (2024). *Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement*. arXiv:2410.04444. 见 r-paper-007。（Coordinated 配置的实现基础，H2 最强证据）
7. khattab2024dspy: Khattab, O., et al. (2024). *DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines*. ICLR。（P-only Independent 的备选实现）
8. yao2023react: Yao, S., et al. (2023). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR. 见 r-paper-001。（Baseline Agent 架构）
9. packer2023memgpt: Packer, C., et al. (2023). *MemGPT: Towards LLMs as Operating Systems*. arXiv:2310.08560. 见 r-paper-004。（M-only Independent 的备选实现）
10. shinn2023reflexion: Shinn, N., et al. (2023). *Reflexion: Language Agents with Verbal Reinforcement Learning*. NeurIPS 2023. 见 r-paper-002。（M-only Independent 的早期代表）
11. wolpert1996nfl: Wolpert, D. H. (1996). *The Lack of A Priori Distinctions Between Learning Algorithms*. Neural Computation, 8(7), 1341-1390.（No Free Lunch Theorem，协同策略有效性的理论边界）
12. caruana1997multitask: Caruana, R. (1997). *Multitask Learning*. Machine Learning, 28(1), 41-75.（多任务协同学习的理论基础）
13. guyon2003intro: Guyon, I., & Elisseeff, A. (2003). *An Introduction to Variable and Feature Selection*. JMLR, 3, 1157-1182.（特征组合互补性的方法论）