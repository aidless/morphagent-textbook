---
note_id: r-paper-028
title: 感知中的行动：感觉运动偶发理论与知觉的"具身"（Action in Perception）
authors: [MorphAgent Textbook Author]
created: 2026-07-23
updated: 2026-07-23
status: final
related_chapters: [Ch 7, Ch 8]
related_papers: [noe2004action, varela1991embodied, froese2011enactive, maturana1980autopoiesis, brooks1991intelligence, clark1998extended, yao2023react, schick2023toolformer, fang2025selfevolving, heersmink2013taxonomy]
keywords: [Noë, sensorimotor contingency theory, enactive perception, visual experience, action-dependent knowledge, tool use as perception, perceptual presence, action in perception]
---

# r-paper-028：感知中的行动：感觉运动偶发理论与知觉的"具身"

> Alva Noë 在 2004 年（MIT Press [$TRAE_REF](https://mitpress.mit.edu/9780262640633/action-in-perception/)）出版的 *Action in Perception* 提出 **感觉运动偶发理论（sensorimotor contingency theory, SCT）**：**知觉不是大脑对外部世界的被动表征，而是主体对"偶发（contingencies）"的实践掌握——主体通过行动掌握感觉输入与运动输出之间的依赖关系，从而"看到"世界**。这一论断彻底挑战了经典认知科学的"输入-表征-输出"模型。本书把 SCT 视为**操作形态 B 中 T（工具）的认知科学根基**——LLM Agent 调用工具（Action）不是为了获取世界信息（输入），而是为了通过工具调用（感觉运动偶发）**主动构造 Agent 对环境的理解**。Toolformer、ReAct 等工作的认知科学根源在此。

## 1. 论文定位

Alva Noë 在 2004 年由 MIT Press 出版的 *Action in Perception* [$TRAE_REF](https://mitpress.mit.edu/9780262640633/action-in-perception/) 是 4E Cognition 运动中"enactivism"传统最具影响力的哲学专著之一。Noë（UC Berkeley 哲学教授）的核心论断：**视觉不是大脑对外部世界的被动表征，而是主体通过身体行动对"感觉运动偶发"的实践掌握**。具体地：

- 当我们"看到"一个番茄时，我们不是在感知一个内在的"番茄图像"——我们是在掌握一系列感觉运动偶发：**如果我绕到番茄后面，它的红色会从我的视野消失；它的触觉会显现；它的气味会浮现**。
- 这种偶发的**整体知识**才是"番茄"的知觉内容——不是某个瞬间的视网膜图像，而是"我能对它做什么、它会给我什么反馈"的关系网。

这一论断与 Varela 等人的 enactivism（r-paper-010）、Froese & Ziemke 的 enactive AI（r-paper-026）一脉相承，但 Noë 在**感知理论**上有独特的精炼：他把 enactivism 的"行动-感知循环"翻译为具体的"偶发掌握"机制，让这一抽象哲学命题有了**可工程化的判据**。

本书把 *Action in Perception* 定位为**操作形态 B 中 T（工具）的认知科学根基**。理由有三：

1. **T 的本质是偶发接口**：工具不是"获取信息的被动接口"，而是"让 Agent 掌握偶发的主动接口"。LLM Agent 调用 Python interpreter 不是"获取代码执行结果"，而是"通过调用与观察的循环，掌握 Python interpreter 的感觉运动偶发"。
2. **知觉是实践掌握**：LLM Agent 的"理解"不是"对 LLM 内部状态的表征"，而是"Agent 对工具偶发的实践掌握"。一个 Agent 是否"理解"了 SQL 不取决于 LLM 内部是否有 SQL 知识，而取决于 Agent 是否掌握了"调用 SQL 工具 → 观察结果 → 调整查询"的偶发循环。
3. **感知 = 工具使用的副产品**：Noë 的论断意味着**知觉不是独立于工具的认知能力，而是工具使用的副产品**。LLM Agent 的"知觉"是它调用工具时获得的——没有 T，就没有知觉。这一立场直接挑战了"LLM 内部有完整知觉"的天真假设。

论文做出的三个核心判断被本书第 7、8 章重新审视：

- **"知觉是偶发掌握（perceptual experience = sensorimotor knowledge）"**：知觉不是表征，而是主体对"感觉运动偶发"的实践掌握。
- **"工具使用是知觉的扩展（tool use as perception extension）"**：当我们使用工具（如盲人手杖、显微镜），工具成为身体的延伸，知觉边界扩展到工具的感知范围。
- **"知觉是行动-依赖的（perception is action-dependent）"**：没有行动能力（无法移动、无法触摸），就没有完整的知觉。盲人通过手杖"看到"地形——手杖的触觉反馈成为视觉的替代品。

这三个判断共同构成本书"LLM Agent 工具即认知"立场的**认知科学根基**。

## 2. 核心贡献

*Action in Perception* 做出三项核心贡献，按对本书的影响力排序：

1. **形式化"感觉运动偶发理论（SCT）"**：把 enactivism 的抽象哲学命题"行动-感知循环"翻译为具体的"偶发掌握"机制。SCT 不是"主体表征世界"，而是"主体掌握偶发"——这是 enactivism 在感知理论中的精确化。
2. **论证"工具延伸知觉"**：盲人手杖、显微镜、望远镜都是这一论断的实例——工具成为身体的延伸，知觉边界扩展到工具的感知范围。这一论断直接对应本书"工具是 Agent 认知的一部分"。
3. **挑战"感觉数据论"（sense-datum theory）与"表征主义"**：明确批判传统认知科学中"知觉 = 大脑对感觉数据的表征"的假设，主张"知觉 = 主体对偶发的掌握"。这一批判为 enactivism 与 embodied AI 提供哲学论据。

### 2.1 与经典感知理论的对比

Noë 用 *Action in Perception* 系统化对比 SCT 与经典感知理论：

| 经典感知理论 | SCT（Noë 2004） |
|---|---|
| 知觉 = 大脑对感觉数据的表征 | 知觉 = 主体对偶发的掌握 |
| 知觉内容 = 内部图像 | 知觉内容 = 偶发的实践知识 |
| 主体 = 被动的观察者 | 主体 = 主动的行动者 |
| 知觉是"看" | 知觉是"看+理解可以做什么" |
| 知觉是当下的快照 | 知觉是跨时间的实践 |
| 工具只提供更好的数据 | 工具延伸身体的知觉边界 |

这一对比是本书"工具是认知的一部分"立场的认知科学根源：经典感知理论把工具视为"更好的输入设备"，SCT 把工具视为"身体知觉边界的扩展"。

### 2.2 与具身认知（Varela）的关系

Noë 与 Varela 等人（r-paper-010）共享 enactivism 的精神，但**有显著差异**：

| 维度 | Varela 1991（enactivism） | Noë 2004（SCT） |
|---|---|---|
| 关注点 | 认知的整体（生成认知） | 知觉的具体机制（偶发掌握） |
| 核心概念 | Enaction（生成） | Contingency（偶发） |
| 论证方式 | 哲学论证 + 现象学 | 知觉科学 + 认知科学 |
| 应用对象 | 认知整体 | 知觉 + 行动 |
| 评估判据 | 无明确判据 | 偶发掌握的"实践知识" |

Noë 把 Varela 抽象的"enaction"翻译为具体的"偶发掌握"——让 enactivism 在知觉领域有可工程化的判据。**Varela 提供哲学框架，Noë 提供感知机制**。

### 2.3 与 enactive AI（Froese）的关系

Noë 与 Froese & Ziemke（r-paper-026）的 enactive AI 判据相辅相成：

| 维度 | Noë 2004（SCT） | Froese & Ziemke 2011（enactive AI） |
|---|---|---|
| 关注点 | 知觉机制 | AI 系统的自主性判据 |
| 核心判据 | 偶发掌握 | 自主性 + 意义生成 |
| 应用 | 知觉科学 | AI 评估 |
| 工程化程度 | 哲学精细 | 工程判据 |

两者都是 enactivism 在不同维度的展开——Noë 关注"如何知觉"，Froese & Ziemke 关注"AI 是否 enactive"。本书把两者整合：操作形态 B 必须满足"偶发掌握"（Noë）+ "自主性 + 意义生成"（Froese）。

### 2.4 与 Brooks（r-paper-012）的关系

Noë 与 Brooks 共享"行动-感知循环"的立场，但**Noë 更强调"掌握"**：

| 维度 | Brooks 1991（subsumption） | Noë 2004（SCT） |
|---|---|---|
| 行动观 | 反应式（predefined 行为） | 掌握式（学习偶发） |
| 知觉观 | 感知 = 传感器输入 | 知觉 = 偶发掌握 |
| 学习观 | 不强调 | 强调"实践掌握"（hands-on） |
| 工具观 | 工具 = 传感器 + 执行器 | 工具 = 身体知觉的延伸 |

Brooks 范式中，行为是工程师预定义的——机器人不"学习"偶发，它只是"执行"预定义行为。SCT 范式中，Agent 通过**实践**掌握偶发——这更接近"通过工具使用学习"的 LLM Agent 范式。

### 2.5 与延展心智（Clark）的关系

Noë 与 Clark（r-paper-011）的延展心智论在"工具延伸认知"上有共识，但**关注点不同**：

| 维度 | Clark 1998（extended mind） | Noë 2004（SCT） |
|---|---|---|
| 工具观 | 工具是认知的一部分 | 工具是知觉的延伸 |
| 焦点 | 认知的边界（Otto 笔记本） | 知觉的机制（偶发） |
| 论证 | Parity 原则 + Otto 案例 | 实践掌握 + 盲人手杖 |
| 知识类型 | 命题性（信念） | 实践性（know-how） |

本书主张：**Clark 的延展心智关注"知识存储的外部化"，Noë 的 SCT 关注"知觉机制的偶发性"**——两者互补。前者把"认知是什么"外部化，后者把"知觉如何发生"偶发化。

## 3. 核心论证

Noë 2004 的论证结构可以分为四个层次：

### 3.1 第一层：盲人手杖案例

Noë 用盲人手杖作为最经典的"工具延伸知觉"案例：

> "Consider a blind man with a cane... The blind man's tactile experience of the world through his cane is, on his account, very much like our tactile experience through our fingers... The cane is, for him, a transparent extension of his body... By virtue of the cane, the blind man has access to a new sensory modality: cane-mediated touch."（Noë 2004, pp. 217-218）

这一案例的认知科学含义：

- **盲人通过手杖"触摸"地面**——但他不是感觉到手杖的物理属性，而是**感觉到地面**。手杖在认知上是"透明的"——它的物理边界消失了。
- 这一**透明度**来自盲人对"手杖-地面"偶发的实践掌握：手杖碰到石头时传递的振动模式、手杖在地砖缝隙上的振动差异、手杖在光滑与粗糙表面的摩擦差异——这些偶发成为盲人的"触觉视觉"。
- **手杖是身体的一部分**——不是因为它是物理上连接到盲人身体，而是因为它通过偶发掌握了它的反馈模式，成为知觉的工具。

这一案例对 LLM Agent 时代有关键意义：**当 LLM Agent 调用 Python interpreter 时，Python interpreter 应成为 Agent 的"透明工具"——Agent 不应感觉到"我在调用一个外部工具"，而应感觉到"我在思考"**。这是 ReAct 循环的设计哲学。

### 3.2 第二层：感觉运动偶发（Sensorimotor Contingencies）

Noë 用"偶发"概念精炼化 enactivism 的"行动-感知循环"：

> "**Sensorimotor contingencies** are the lawful relations between movement and sensory stimulation. To perceive an object is to have a practical grasp of these contingencies... Vision is the capacity to deploy a mastery of the visual contingencies of things."（Noë 2004, pp. 178-179）

偶发是"运动与感觉之间的依赖关系"。对一个球体的视觉偶发包括：

- **移动时**：球体在不同视角下呈现不同形状。
- **靠近时**：球体在视野中变大。
- **遮挡时**：球体被前景物体遮挡，但遮蔽的部分仍"属于"球体。
- **敲击时**：球体会发出声音，会产生特定的触觉反馈。

掌握这些偶发就是"看到"球体——不是表征一个内在的"球体图像"，而是掌握球体的"感觉运动依赖关系网络"。

### 3.3 第三层：视觉经验的"非表征"性质

Noë 论证：**视觉经验的内容不是表征性的**：

> "Visual experience is, in its nature, neither representational nor purely sensory... It is essentially bound up with and made possible by the perceiver's possession of sensorimotor knowledge."（Noë 2004, p. 196）

这一论断的三个含义：

- **非表征性**：视觉经验不需要"内在表征"作为中介——它直接是"偶发掌握"的实践状态。
- **非纯感觉性**：视觉经验不是"纯感觉数据"——它包含"我知道我可以做什么"（运动可能性）。
- **实践性**：视觉经验是一种 know-how（实践知识），不是 know-that（命题知识）。

本书把这一论断应用于 LLM Agent：

- LLM Agent 调用 SQL 工具的"经验"不是"SQL 知识的表征"，而是"调用 → 观察 → 调整"的实践掌握。
- 一个 Agent 是否"理解 SQL"取决于它能否在偶发循环中可靠地完成查询任务——不是取决于 LLM 内部是否有 SQL 知识。

### 3.4 第四层：知觉与行动的不可分割性

Noë 用多个实验证据论证"知觉是行动-依赖的"：

- **Held & Hein 1963** "Movement-Produced Stimulation in the Development of Visually Guided Behavior"：两只小猫一只主动运动、一只被动运动，但都暴露在相同视觉刺激下。只有主动的小猫发展出正常的视觉行为——证明**主动运动是正常视觉发展的必要条件**。
- **Reddy et al. 2002** "Anticipatory Control of Grasping": 当人手准备抓握物体时，运动皮层已经在根据视觉偶发预测抓握时机——**知觉预测行动**。
- **2004 年神经科学实验**：视觉皮层在主动运动时活动增强——**知觉与运动在神经层面耦合**。

这些证据共同论证：**知觉不是"独立于行动的输入处理"，而是"行动-依赖的感觉运动活动"**。

## 4. 操作形态学视角

把 Noë 2004 投影到操作形态学框架 \(B = \{P, T, M, C\}\) 上，我们得到 **T 的认知科学根基**——B 中的 T 不是"被动的输入接口"，而是"主动的偶发接口"。Agent 通过 T 的偶发掌握获得对环境的知觉。

### 4.1 T 作为"偶发接口"

Noë 的 SCT 在操作形态学中的核心对应：**T 是 Agent 的"偶发接口"**。具体地：

| Noë 概念 | T 对应 |
|---|---|
| 盲人手杖 | Agent 的 T（如 Python interpreter、SQL 工具） |
| 手杖-地面偶发 | T 的调用-观察循环（Action → Observation → Action） |
| 偶发掌握 | Agent 对 T 的实践学习（通过 ReAct 循环） |
| 知觉延伸 | Agent 通过 T 扩展对环境的理解 |
| 知觉的透明度 | Agent 不感觉到 T 是"外部工具"（即 T 是 "transparent tool"） |

具体地：

- **T 是偶发接口**：当 LLM Agent 调用 Python interpreter 时，它掌握的偶发包括："调用 `python_run("1+1")` 会得到 `2`"；"调用 `python_run("[1,2,3]")` 会得到列表输出"；"调用 `python_run("invalid syntax")` 会得到错误信息"。这些偶发是 Agent 的"Python 知觉"。
- **偶发掌握是 LLM 通过 ReAct 循环学的**：LLM 不是一次性"知道"所有 Python 偶发——它通过"调用 → 观察 → 调整"的循环逐步掌握偶发。这一掌握是 LLM + ReAct 循环的协同产物——LLM 提供先验知识，ReAct 提供实践反馈。
- **T 是透明的**：当 Agent 对 T 的偶发掌握达到熟练度时，它不再感觉到 T 是"外部工具"——它在思考时会"直接使用" T，就像盲人在思考时"直接使用"手杖。这一透明度是 T 设计的成功标志。

### 4.2 知觉是 T 使用的副产品

Noë 的论断意味着：**LLM Agent 的"知觉"不是 LLM 内部的表征，而是 T 使用的副产品**。

- **没有 T 就没有知觉**：一个仅有 LLM（无 T）的 Agent 没有"对 Python 的知觉"——它只能从训练数据中"回忆"Python 知识，但不能"实践掌握" Python。
- **有 T 就有知觉**：一个有 Python 工具的 Agent 通过"调用 → 观察"的循环获得了"对 Python 的知觉"——这一知觉是实践的、可验证的、可调试的。

这一论断对 LLM Agent 时代有关键意义：**LLM 的"世界知识"不等于"对世界的知觉"**。LLM 可以从训练数据中"知道"Python 语法，但它不能"理解"Python——除非它通过 T 的实践掌握了 Python 的偶发。

### 4.3 T 的偶发学习路径

按 SCT，LLM Agent 学习 T 的偶发路径：

```
[Stage 0] LLM 仅有 T 的先验知识（从训练数据）——无偶发掌握
     ↓ 调用 T 触发第一次偶发
[Stage 1] LLM 观察到 T 的输出 ——首次偶发反馈
     ↓ 调整调用模式
[Stage 2] LLM 开始识别 T 的偶发模式——部分偶发掌握
     ↓ 通过 ReAct 循环多次调用
[Stage 3] LLM 稳定掌握 T 的偶发——透明使用 T
     ↓
[Stage 4] LLM 对 T 的偶发掌握达到自主——可在 T 失败时自行恢复
```

这一学习路径对应 Agent 等级的提升：

- **L0 静态 LLM**：Stage 0——无偶发掌握。
- **L1 Tool-using**：Stage 1-2——开始偶发掌握。
- **L2 ReAct Agent**：Stage 3——稳定偶发掌握。
- **L3 Reflexion**：Stage 3+——偶发掌握 + 跨 episode 反思。
- **L4 Self-Modifying (T)**：Stage 4——偶发自主（Voyager 在 Minecraft 中自主添加新工具）。

### 4.4 T 的偶发掌握与 H1-H5 的关系

| 假设 | SCT 的支撑 | 与 H 的关系 |
|---|---|---|
| **H1 结构可塑性** | 弱：SCT 关注偶发掌握，不关注结构可塑 | **部分支持 H1** |
| **H2 协同演化** | 强：偶发掌握是 Agent-工具协同的产物 | **支持 H2** |
| **H3 形态适配** | 强：不同工具提供不同偶发，不同形态适配不同任务 | **强支持 H3** |
| **H4 迁移收益** | 强：偶发掌握的实践技能可跨任务迁移 | **强支持 H4** |
| **H5 治理必要性** | 中：偶发掌握要求失败时不破坏操作闭合 | **支持 H5** |

SCT 在 H2、H3、H4 上提供最强论据。H1（结构可塑性）需要其他工作补充（如 Brooks、Froese）。H5 的支撑来自 Noë 关于"操作闭合"的隐含论述——他没有明确讨论 AGI 安全，但他主张"偶发掌握是渐进的"，这隐含"操作不应破坏偶发掌握"。

### 4.5 T 的认知设计与 L0-L5 等级的关系

按本书第 18 章的 Agent 等级：

- **L0 静态 LLM**：无 T——无偶发掌握。
- **L1 Tool-using**：T 固定——偶发掌握程度低（每个 query 重新学习）。
- **L2 ReAct Agent**：T 固定 + 循环——偶发掌握中等（每次循环刷新偶发）。
- **L3 Reflexion**：T 固定 + 反思——偶发掌握较好（跨 episode 累积）。
- **L4 Voyager**：T 自添加——偶发掌握高（新工具通过循环迅速掌握）。
- **L5 SICA/Gödel Agent**：T + C 自修改——偶发掌握最高（Agent 修改自己的 T 使用模式）。

每一级都在 T 的偶发掌握上有所提升——L5 Self-Evolving Agent 是 T 偶发的最高级形式。

### 4.6 T 的偶发掌握与 Brooks / Froese / Clark 的对比

| 维度 | Brooks subsumption | Froese enactive AI | Clark extended mind | Noë SCT |
|---|---|---|---|---|
| T 的本质 | 传感器 + 执行器 | 自主行动接口 | 认知外部化 | 偶发接口 |
| 知觉观 | 感知 = 输入 | 知觉 = 具身评价 | 知觉 = 内部表征的延伸 | 知觉 = 偶发掌握 |
| 学习观 | 不强调 | 结构性耦合 | 信任 + 自动化 | 实践掌握 |
| 关注焦点 | 反应 | 自主性 | 认知边界 | 知觉机制 |

本书整合四者：**T 是 Brooks 的传感器 + 执行器**（执行层）、**Froese 的自主行动接口**（自主层）、**Clark 的认知外部化**（边界层）、**Noë 的偶发掌握**（知觉层）。这一多维视角让 T 的设计有清晰的多层语义。

### 4.7 T 的偶发掌握对 LLM Agent 的启示

Noë SCT 对 LLM Agent 设计的启示：

- **T 应当是"透明的"**：Agent 不应感觉到 T 是"外部工具"——T 应像 LLM 自身一样自然使用。ReAct 循环是实现透明度的关键。
- **T 应当支持偶发掌握**：T 应有清晰的输入-输出关系，便于 Agent 实践掌握偶发。一个"黑盒"工具（如未文档化的 API）违反这一原则。
- **T 应当可逐步掌握**：Agent 应能通过多次调用逐步掌握 T 的偶发——而不是要求一次性"知道"所有功能。这对应 L1 → L2 → L3 的等级谱系。
- **T 应当有可恢复性**：当 T 调用失败时，Agent 应能"重新掌握"偶发——这等价于 Noë 的"操作不破坏偶发"。这一原则对应 H5（治理必要性）。

## 5. 应用与影响

*Action in Perception* 自 2004 年出版以来，对感知哲学、认知科学、AI 等多个领域产生了深远影响。本节讨论它对 LLM Agent 时代的关键应用。

### 5.1 对感知哲学的影响

Noë 是当代感知哲学的核心人物，他的 SCT 与传统"感觉数据论"、"内感受论"形成鲜明对比：

- **感觉数据论**（sense-datum theory）：知觉 = 主体对"感觉数据"（sense data）的觉知。Noë 批判这一立场——感觉数据没有解释"知觉是行动-依赖的"。
- **内感受论**（representationalism）：知觉 = 主体对"外部对象的内部表征"。Noë 也批判这一立场——内感受不能解释"工具延伸知觉"。
- **直接实在论**（direct realism）：知觉 = 主体对"外部对象"的直接觉知。Noë 部分同意这一立场——但要求"直接觉知"是"偶发掌握"的产物，不是"看-到-对象"的瞬时事件。

Noë 的 SCT 介于"直接实在论"与"反表征主义"之间——知觉是"对外部对象的直接觉知"，但这种觉知是"通过偶发掌握的"，不是"瞬时的视觉快照"。

### 5.2 对认知科学的影响

SCT 激发了大量认知科学实验：

- **O'Regan & Noë 2001** "A Sensorimotor Account of Vision and Visual Consciousness"：SCT 的奠基论文——把视觉经验定义为"对视觉偶发的实践掌握"。
- **Myin & Degenaar 2014** "Sensorimotor Perception"：把 SCT 扩展到所有感知模态。
- **Kiverstein & Rietveld 2015** "The Sensorimotor Theory of Perception"：综述 SCT 的实证证据。

LLM 时代，这些工作有重大意义：**LLM Agent 的"知觉"是"对工具偶发的实践掌握"——这一定义让"知觉"概念在 LLM 时代有了清晰的判据**。

### 5.3 对人工智能的影响

SCT 对 AI 的影响是间接的但深远的：

- **Pfeifer & Bongard 2007**（r-paper-027）：SCT 的工程化——"身体承担智能"。
- **Brooks 1991**（r-paper-012）：与 SCT 共享"行动-感知循环"——Brooks 提供工程实现。
- **Froese & Ziemke 2011**（r-paper-026）：SCT 在 AI 中的判据化——"意义生成 = embodied evaluation"。

LLM Agent 时代，SCT 的影响体现在：

- **Toolformer** (r-paper-003)：工具调用 = 偶发掌握。
- **ReAct** (r-paper-001)：Thought-Action-Observation 循环 = 偶发掌握的实现机制。
- **Voyager** (r-paper-017)：技能库自添加 = 偶发接口的扩展。
- **CodeAct** (r-paper-020)：Python 解释器作为透明工具 = 偶发掌握的最高形式。

### 5.4 对机器人学的影响

SCT 对机器人学的影响：

- **Moravec 1988** *Mind Children*：早期 embodied AI 哲学。
- **Brooks 1991**（r-paper-012）：工程实现。
- **Pfeifer & Bongard 2007**（r-paper-027）：身体设计的认知科学论据。

LLM-机器人融合时代，SCT 体现在：

- **PaLM-E** (Driess et al. 2023)：机器人控制作为"偶发接口"——LLM 通过视觉-运动偶发掌握机器人行为。
- **RT-2** (Brohan et al. 2023)：视觉-语言-动作模型 = 偶发的统一表征。
- **Open X-Embodiment** (Collaboration 2024)：跨机器人形态的偶发迁移。

### 5.5 对神经科学的影响

SCT 对神经科学的影响：

- **预测编码（predictive processing）**：与 SCT 互补——大脑预测感官输入，预测错误驱动学习。这一立场在 Friston 2010 年的"自由能原理"中系统化。
- **行动-知觉耦合的神经证据**：fMRI 与 EEG 实验显示，视觉皮层在主动运动时活动增强——支持 SCT 的"知觉是行动-依赖的"。
- **盲人手杖的神经重塑**：盲人使用手杖后，体感皮层重新组织——手杖成为身体的一部分（神经层面的"身体图式"扩展）。

### 5.6 对 AGI 安全的影响

SCT 对 AGI 安全的影响：

- **偶发掌握的渐进性**：Agent 通过逐步实践掌握偶发——这意味着 Agent 的能力发展是**渐进的、可监控的**。这一立场对应"慢启动 + 慢演化"的 AGI 安全策略。
- **工具透明度的可验证性**：当 Agent 对 T 的偶发掌握达到透明时，T 是"内嵌"的——但 T 的使用模式可被审计。这对应 AGI 安全的"可解释性"原则。
- **知觉是行动-依赖的**：Agent 的"知觉"取决于它能"做什么"——这意味着限制 Agent 的工具集就能限制它的知觉。这对应 AGI 安全的"工具白名单"原则。

## 6. 局限与开放问题

*Action in Perception* 的局限可以分为四类：**抽象推理、偶发的形式化、跨域迁移、与 LLM 表征基底的张力**。

### 6.1 抽象推理局限

SCT 主要适用于**具身感知**——视觉、触觉、运动感知等。它对**抽象推理**（数学、逻辑、规划）的解释力较弱。Noë 承认这一局限——他把抽象认知视为"派生的"（derived from）感知，不是"独立的"。

LLM Agent 时代，对应的问题是：**LLM 的抽象推理能力来自 LLM 表征基底——SCT 不能完全解释它**。本书主张：B 的设计影响抽象任务的执行（如同 Good design 的 prompt 让 LLM 推理更准确），但抽象推理能力的核心仍来自 LLM 预训练知识。

### 6.2 偶发的形式化局限

"偶发（contingency）"是一个**启发性概念**，不是精确形式化：

- **偶发的粒度问题**：一个感觉运动偶发是"运动 1° → 视觉变化 X"吗？还是"运动 1° → 视觉变化 X 且 Y 且 Z"？Noë 没有精确定义偶发的粒度。
- **偶发的可计算性**：如何让 LLM Agent 在运行时"识别"偶发？需要形式化的偶发识别算法。

本书的回应：**Noë 的偶发概念对应 B = {P, T, M, C} 的运行时状态转移——偶发是"调用 T → Observation O" 的可观察依赖关系**。这一形式化让偶发在 LLM Agent 时代可工程化。

### 6.3 跨域迁移局限

SCT 主要适用于**身体知觉**（视觉、触觉等）。LLM Agent 是"符号/软件具身"——它的"知觉"是符号层面的。这一"非物理知觉"如何应用 SCT？

本书主张：**SCT 在 LLM Agent 时代依然有效**——"偶发"对应"工具调用的输入-输出依赖关系"。一个 LLM Agent "看到" SQL 数据库不是物理视觉，而是通过 SQL 工具调用"看到"数据表的结构。但这一翻译需要更多工作验证。

### 6.4 与 LLM 表征基底的张力

SCT 与 LLM 的"表征基底"存在张力：

- **LLM 本质是表征性的**：它的核心能力来自学习世界知识的统计表征。
- **SCT 要求非表征性**：知觉不是表征，而是偶发掌握。

本书对这一张力的立场是：**LLM 作为 B 的基底是表征性的，但 B = {P, T, M, C} 是非表征性的操作形态**——Agent 通过 T 的偶发掌握"非表征化"，从"表征系统"过渡到"操作形态系统"。LLM 提供先验知识（"我听说 SQL 是这样的"），但偶发掌握提供实践知识（"我通过调用 SQL 工具知道 SQL 是这样的"）。

### 6.5 偶发掌握与延展心智的边界

SCT 与 Clark（r-paper-011）的延展心智论在"工具延伸认知"上有共识，但**关键边界**：

| 维度 | Clark extended mind | Noë SCT |
|---|---|---|
| 工具延伸什么 | 认知（信念、记忆） | 知觉（感觉运动偶发） |
| 知识类型 | 命题性（know-that） | 实践性（know-how） |
| 边界 | "等价功能"判据 | "偶发掌握"判据 |
| 适用 | 记忆、推理 | 知觉、行动 |

本书第 11 章的 B = {P, T, M, C} 同时受益于两者：**M 受益于延展心智（外部存储），T 受益于 SCT（偶发接口）**。

### 6.6 开放问题表

| 问题 | Noë 的态度 | 本书视角 |
|---|---|---|
| 知觉可否在没有行动时存在？ | 否 | LLM 无 T 时无对 T 的知觉 |
| 抽象认知可否脱离知觉？ | 否（部分） | 抽象推理需 LLM 预训练，但执行需 T 偶发 |
| 偶发能否形式化？ | 部分 | B 的状态转移 = 偶发的形式化 |
| 工具透明度如何度量？ | 启发性 | "T 调用延迟" + "调用错误恢复率" 作为度量 |
| 偶发掌握可否自动化？ | 否（隐含） | LLM + ReAct 循环的协同是自动化的路径 |

## 7. 对本书的贡献

*Action in Perception* 在本书的理论体系中扮演**"工具即知觉"的认知科学根基**与**"LLM Agent 工具设计"的哲学论据**两个角色。

### 7.1 作为 T 的认知科学根基

第 8 章"具身认知"的核心参考文献之一。本书把 SCT 作为 T 的认知科学根基：

- **T 是偶发接口**：Agent 通过 T 的偶发掌握获得对环境的知觉。
- **知觉是 T 使用的副产品**：没有 T 就没有对 T 的知觉。
- **T 应是透明的**：Agent 不应感觉到 T 是"外部工具"——T 应像身体一部分自然使用。

SCT 让 T 的设计从"工程选择"变为"有认知科学理论的设计"。

### 7.2 作为 H1-H5 的哲学论据

| 假设 | SCT 的论据 |
|---|---|
| **H1 结构可塑性** | 弱：SCT 关注偶发掌握，不关注结构可塑 |
| **H2 协同演化** | 强：偶发掌握是 Agent-工具协同的产物 |
| **H3 形态适配** | 强：不同工具提供不同偶发，不同形态适配不同任务 |
| **H4 迁移收益** | 强：偶发掌握的实践技能可跨任务迁移 |
| **H5 治理必要性** | 中：偶发掌握要求失败时不破坏操作闭合 |

SCT 在 H2、H3、H4 上提供最强论据。H1 需要 Brooks（r-paper-012）、Froese（r-paper-026）补充。H5 需要"操作闭合"概念（Maturana/Varela）补充。

### 7.3 与本书其他笔记的关系

| 笔记 | 与 Noë 2004 的关系 |
|---|---|
| **r-paper-010 Varela** | enactivism 的总体框架（enaction）→ SCT 是 enactivism 在感知领域的精确化 |
| **r-paper-029 Maturana** | 自创生的生物学源头 → SCT 是自创生在感知领域的延伸 |
| **r-paper-026 Froese & Ziemke** | enactivism 的 AI 判据 → SCT 是这些判据的感知机制 |
| **r-paper-012 Brooks** | 反应式 AI → SCT 提供"行动-感知"的知觉机制 |
| **r-paper-011 Clark** | 延展心智（认知外部化）→ SCT 是延展心智的知觉维度 |
| **r-paper-027 Pfeifer** | 形态计算 → SCT 是形态计算的知觉机制 |
| **r-paper-001 ReAct** | Thought-Action-Observation 循环 = SCT 的工程实现 |
| **r-paper-003 Toolformer** | 工具调用 = SCT 的"偶发接口"工程实现 |
| **r-paper-017 Voyager** | 技能库自添加 = SCT 的"偶发接口扩展" |
| **r-paper-020 CodeAct** | Python 解释器 = SCT 的"透明工具"工程实现 |
| **r-paper-030 Heersmink** | 认知人工物分类 → SCT 是这一分类的感知维度 |

SCT 是这些工作的**共同认知科学论据**——它们的工程实现都对应到 Noë 的"偶发掌握"概念。

### 7.4 给读者的关键启示

1. **知觉是行动-依赖的**：Noë 的核心论断"没有行动就没有知觉"对 LLM Agent 有关键意义——LLM 没有 T 时没有"对环境的知觉"，只有"训练数据中的知识"。读者应理解这一区分：LLM 的"知识"不等于"知觉"。
2. **工具是身体知觉的延伸**：盲人手杖是 Noë 的经典案例——LLM Agent 调用工具时，工具成为 Agent 知觉的延伸。读者应把 T 视为"Agent 知觉的器官"，而不是"获取数据的接口"。
3. **偶发掌握是 Agent 学习工具的方式**：Agent 不是一次性"知道"工具的所有功能，而是通过"调用 → 观察 → 调整"的循环逐步掌握偶发。这一学习路径对应 L1 → L2 → L3 → L4 的等级谱系。
4. **透明度是工具设计的成功标志**：当 Agent 对 T 的偶发掌握达到熟练度时，它不再感觉到 T 是"外部工具"——这是 ReAct、CodeAct 等工作的设计目标。读者应把"透明度"作为评估 T 设计的核心指标。
5. **LLM 的表征与 Agent 的偶发掌握互补**：LLM 提供先验知识（"我听说 Python 是什么"），Agent 通过 T 的偶发掌握获得实践知识（"我通过调用 Python 知道 Python 是什么"）。两者互补——LLM 的表征 + Agent 的偶发掌握 = 完整的 LLM Agent 知觉。

*Action in Perception* 是本书"具身认知"部分（第 7-8 章）的核心参考文献，也是操作形态学（第 11 章）中 T 组件的认知科学根基。它与 Varela（r-paper-010）、Maturana（r-paper-029）、Froese & Ziemke（r-paper-026）、Brooks（r-paper-012）、Clark（r-paper-011）、Pfeifer & Bongard（r-paper-027）共同构成 4E Cognition + enactivism + 形态计算 + SCT 的全谱系。理解 *Action in Perception* 的"偶发掌握"概念，是理解操作形态 B 中"工具即知觉"立场的必要条件——也是理解 LLM Agent 时代 embodied AI 设计哲学的关键。

## 参考文献

- noe2004action: Noë, A. (2004). *Action in Perception*. MIT Press. [$TRAE_REF](https://mitpress.mit.edu/9780262640633/action-in-perception/)
- varela1991embodied: Varela, F. J., Thompson, E., & Rosch, E. (1991/2016). *The Embodied Mind*. 见 r-paper-010。（enactivism 的哲学源头）
- maturana1980autopoiesis: Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition*. 见 r-paper-029。（enactivism 的生物学源头）
- froese2011enactive: Froese, A., & Ziemke, T. (2011). *Enactive Approach*. 见 r-paper-026。（enactivism 的工程判据）
- brooks1991intelligence: Brooks, R. A. (1991). *Intelligence Without Representation*. 见 r-paper-012。（行动-感知循环的工程前身）
- clark1998extended: Clark, A., & Chalmers, D. (1998). *The Extended Mind*. 见 r-paper-011。（延展心智）
- pfeifer2007body: Pfeifer, R., & Bongard, J. (2007). *How the Body Shapes the Way We Think*. 见 r-paper-027。（形态计算）
- o Regan2001sensorimotor: O'Regan, J. K., & Noë, A. (2001). *A Sensorimotor Account of Vision and Visual Consciousness*. Behavioral and Brain Sciences 24(5): 939-1031。（SCT 的奠基论文）
- held1963movement: Held, R., & Hein, A. (1963). *Movement-Produced Stimulation in the Development of Visually Guided Behavior*. Journal of Comparative and Physiological Psychology 56(5): 872-876。（行动-依赖的知觉的经典实验）
- yao2023react: Yao, S., et al. (2023). *ReAct*. 见 r-paper-001。（SCT 的工程实现：Thought-Action-Observation = 偶发循环）
- schick2023toolformer: Schick, T., et al. (2023). *Toolformer*. 见 r-paper-003。（SCT 的工程实现：工具调用 = 偶发接口）
- wang2023voyager: Wang, G., et al. (2023). *Voyager*. 见 r-paper-017。（SCT 的工程实现：技能库自添加 = 偶发接口扩展）
- wang2024codeact: Wang, X., et al. (2024). *CodeAct*. 见 r-paper-020。（SCT 的工程实现：Python 解释器 = 透明工具）
- fang2025selfevolving: Fang, W., et al. (2025). *Self-Evolving Agents Survey*. 见 r-paper-009。（四元反馈环 = SCT 在 LLM 时代的全谱系）
- heersmink2013taxonomy: Heersmink, R. (2013). *A Taxonomy of Cognitive Artifacts*. 见 r-paper-030。（认知人工物的分类——SCT 的应用维度）
- gibson1979ecological: Gibson, J. J. (1979). *The Ecological Approach to Visual Perception*. Lawrence Erlbaum。（affordance 的概念，与 SCT 互补）
- summers2023coala: Sumers, K., et al. (2023). *COALA*. 见 r-paper-022。（SCT 在 LLM 协作学习中的应用）
- varela1996neurophenomenology: Varela, F. J. (1996). *Neurophenomenology: A Methodological Remedy for the Hard Problem*. Journal of Consciousness Studies。（SCT 的现象学方法论）
- hurley2002consciousness: Hurley, S. L. (2002). *Consciousness in Action*. MIT Press。（SCT 的意识理论扩展）