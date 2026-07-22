---
chapter: 8
title_cn: Enactivism 与自创生
title_en: Enactivism and Autopoiesis
part: II
pages_planned: 26
status: final
last_updated: 2026-07-22
keywords:
  - Varela
  - Thompson
  - Rosch
  - autopoiesis
  - enaction
  - sensorimotor
  - radical enactivism
  - life-mind continuity
learning_objectives:
  - 复述 Varela/Thompson/Rosch enaction 命题
  - 比较 autopoietic vs sensorimotor enactivism
  - 评价 Hutto & Myin 激进生成论
  - 把生命-心灵连续性论题映射到 LLM Agent
  - 给出 enactivism 对 LLM Agent 的最终立场
prerequisites:
  - Ch 7
---

# 第 8 章 · Enactivism 与自创生

> "生命系统通过自创生维持自身组织——认知是这种自创生过程的一部分。"

## 学习目标

完成本章后，读者应能够：

1. 复述 Varela、Thompson、Rosch 的 enaction 命题
2. 区分 autopoietic 与 sensorimotor enactivism
3. 评价 Hutto & Myin 激进生成论
4. 把生命-心灵连续性论题映射到 LLM Agent
5. 给出 enactivism 对 LLM Agent 的最终立场

## 先修知识

- 第 7 章 · 4E Cognition 简史
- 第 1 章 · LLM 智能体时代

## 章节地图

- **8.1** 生命-心灵连续性论题
- **8.2** Autopoiesis：生命的最小组织
- **8.3** Enaction：认知即行动
- **8.4** 感觉运动理论：知觉是技能
- **8.5** Radical Enactivism：基本心智无内容
- **8.6** Enactivism 对 LLM Agent 的边界
- **8.7** 本章小结与第 9 章预告

---

## 8.1 生命-心灵连续性论题

Enactivism 的根本命题是 **"生命-心灵连续性论题（Life-Mind Continuity Thesis）**：心灵不是生命出现后才"附加"的能力，而是生命本身的基本特征。Thompson 在《Mind in Life》（2007）中将这一论题形式化为两个命题：

> **M1（认知-生命依赖）**：认知是生命的一个基本特征，没有认知就没有生命。
> **M2（生命-认知充分）**：只要有生命，就有某种认知。

这两个命题共同主张：认知不是大脑的"私有财产"，而是生命系统的**普遍属性**。一个细菌在向食物游动时，已经表现出"认知"——它感知环境、评估信息、采取行动。这不是"原始认知"或"准认知"——这是**真正的认知**，只是比人类认知更简单。

生命-心灵连续性论题对 LLM Agent 设计的启示是**有保留的**：

- **接受的部分**：LLM Agent 的"行动"可以视为某种"认知"——Agent 在工具调用、记忆管理、prompt 优化中表现出"有目的"的行为
- **拒绝的部分**：LLM Agent 不满足 M1（认知-生命依赖）——它没有 autopoietic（自创生）能力，依赖外部服务

### 图 8.1 · 生命-心灵连续性论题的两个命题

```
   ┌────────────────────────────────────┐
   │      生命-心灵连续性论题            │
   │                                    │
   │   M1: 认知是生命的基本特征          │
   │       离开生命没有认知              │
   │              ↓                       │
   │   M2: 只要有生命, 就有某种认知      │
   │       认知是生命的充分条件          │
   └────────────────────────────────────┘
                  │
                  │ 推广到 LLM Agent?
                  ▼
   ┌────────────────────────────────────┐
   │   LLM Agent 满足 M1 吗?             │
   │   - 不是 autopoietic 系统          │
   │   - 依赖外部服务 (LLM API, 工具)   │
   │   → 不满足 M1                       │
   │                                    │
   │   LLM Agent 满足 M2 吗?             │
   │   - 有"有目的"的行为              │
   │   - 但不"维持自身"                │
   │   → 部分满足 M2                    │
   └────────────────────────────────────┘
```

> **关键点**：Enactivism 严格立场下 LLM Agent 不算"真正的认知主体"——因为它不是 autopoietic。

## 8.2 Autopoiesis：生命的最小组织

**Autopoiesis（自创生）** 是 Maturana & Varela 在 1970 年代提出的概念，定义为：

> **一个物理系统，如果它的所有组成部分（a）通过产生它们自身的过程持续地相互生成（产生相互关系），并且（b）通过这种方式在空间上形成一个可辨识的边界（成为物理上的统一体），那么这个系统就是自创生的。**

形式化：

$$
\text{Autopoietic}(S) \iff S = f(S) \wedge \text{Boundary}(S) \neq \emptyset
$$

Autopoiesis 的两个关键特征：

1. **操作闭合（Operational Closure）**：系统的操作只产生系统自身的组件，不产生外部组件。
2. **结构耦合（Structural Coupling）**：系统与环境的相互作用不破坏系统的组织，只改变其结构。

一个细胞是自创生的——它的代谢过程产生构成它的所有分子。一个晶体不是自创生的——它的形成不产生它自己。一个工厂也不是自创生的——它的产品是外部的。

> **关键点**：Autopoiesis 定义了"生命"的最小组织——生命是"自我生产"。

Autopoiesis 对 LLM Agent 的边界：**LLM Agent 不是自创生的**。它依赖 LLM API、工具服务器、数据存储——这些都不是 Agent 自己"生产"的。如果 LLM API 关闭，Agent 就死了。这与细胞的"自创生"形成鲜明对比。

## 8.3 Enaction：认知即行动

Varela、Thompson、Rosch 在 1991 年《The Embodied Mind》中提出 **enaction 概念**：认知不是"表征外部世界"，而是"通过行动产生意义"。

Enaction 的三个核心命题：

1. **知觉是行动导向的（Perception is Action-Oriented）**：动物不是被动地"接收"环境信息，而是主动地"探查"环境。
2. **认知是行动者-环境的耦合（Enaction as Coupling）**：认知不是"在脑内完成"，而是"在脑-身体-环境的循环中产生"。
3. **意义是生成的（Meaning is Enacted）**：环境本身没有"意义"——意义是动物在行动中"生成"的。

Enaction 对 LLM Agent 的工程化意义：

- ReAct 循环是 enaction 的工程化实现：每一步"思考-行动-观察"都是 enaction。
- 工具使用是 Agent 的感觉运动系统：工具不是"被调用的函数"，而是 Agent 探索世界的方式。
- 记忆是 Agent 的代谢系统：记忆不是"被存储的数据"，而是 Agent 维持自身认知的方式。

### 图 8.2 · Enaction 的循环

```
         环境 E
           ↑
   ┌───────┴───────┐
   │  感知 Perceive │
   └───────┬───────┘
           ↓
   ┌───────────────┐
   │ 行动 Act      │ ← 行动改变环境
   └───────┬───────┘
           ↓
         新的 E
           ↑
   ┌───────┴───────┐
   │  感知 Perceive │ ← 感知到变化后的环境
   └───────────────┘
```

> **关键点**：Enaction 不是"先想后做"，而是"在做中想"——认知产生于行动者与环境的循环耦合。

## 8.4 感觉运动理论：知觉是技能

**Sensorimotor Enactivism**（感觉运动 enactivism）由 O'Regan & Noë 在 2001 年提出，主张：**知觉不是"在脑中生成表征"，而是"掌握感觉运动技能"**。

核心思想：看见红色，不是"在脑中生成红色的图像"，而是"掌握如何通过眼睛的运动探查红色表面"。一只色盲的人如果掌握了所有"红色"的感觉运动规律（包括社会反应、情绪反应），他仍然可以"看到"红色。

Noë 2004 年的《Action in Perception》进一步发展这一立场：**知觉是"行动-感知"的循环**，没有"独立于行动的知觉"。

感觉运动理论对 LLM Agent 的启示：

1. **LLM 的"上下文窗口"不是"知觉"**：它只是"信息"。真正类似"知觉"的是 LLM 在行动中"使用"这个信息的过程。
2. **工具使用类似"感觉运动技能"**：Agent 学会"在什么情况下用哪个工具"是感觉运动技能，不是"调用 API"。
3. **记忆是"感觉运动记忆"**：记忆不是"存储的事实"，而是"如何行动的知识"。

## 8.5 Radical Enactivism：基本心智无内容

**Radical Enactivism** 是 Hutto & Myin 在 2013/2017 年提出的最激进立场：

> **基本心智（basic minds）不需要内容（content）。**

这一立场挑战认知科学的核心假设——认知是"对内容的处理"。Hutto & Myin 主张：许多基本认知过程（感知、行动控制、情绪）是"无内容的"——它们不需要表征就能工作。

例如：蜘蛛织网是复杂的行为，但它不需要"表征"织网的目标——蜘蛛的行为是"被引导的"（guided），不是"被表征的"（represented）。

Radical Enactivism 区分两种认知：
- **基本心智**（basic minds）：无内容、直接被引导
- **高级心智**（sophisticated minds）：有内容、需要表征

人类的语言、抽象思维属于高级心智，需要表征。但许多动物认知、人类的感知-运动控制属于基本心智，无内容。

Radical Enactivism 对 LLM Agent 的深远挑战：

- **LLM Agent 是否有"基本心智"？** 表面上，LLM 似乎是"无内容的"——它没有"信念"、"欲望"，只是"统计语言模型"。但 LLM 确实能"行动"（调用工具）——这是不是"基本心智"？
- **LLM 的"in-context learning"是不是"内容"？** 当 LLM 从 prompt 中提取任务信息时，这是"内容获取"还是"无内容的耦合"？
- **Agent 的"工具调用"是不是"被引导的行为"？** 当 Agent 调用 get_weather 时，它是"被引导"调用还是"表征性地知道要调用"？

这些问题在 4E 阵营内部仍然开放。

## 8.6 Enactivism 对 LLM Agent 的边界

Enactivism 对 LLM Agent 的最终立场是**有保留地接受**：

**接受的部分**：
- ReAct 循环是 enaction 的工程化实现
- 工具使用是 Agent 的感觉运动系统
- 记忆是 Agent 的代谢系统

**拒绝的部分**：
- LLM Agent **不是 autopoietic 系统**：Agent 不能"自我生产"——它依赖 LLM API、工具服务器、数据存储
- LLM Agent **没有"基本心智"**：Agent 的"行动"是 LLM 生成的，不是"被引导的"
- LLM Agent 的"认知"**不是真正的认知**：它是"模拟的认知"，是"对认知的模仿"

**Varela 严格立场**：

> 只有 autopoietic 系统（活的、能自我维持的）才算"认知"。LLM Agent 不是 autopoietic——它依赖外部服务、不能自我修复、不能自我复制。因此 LLM Agent 不算真正的"认知主体"，而是一种"认知模拟器"。

**本书立场**：

> LLM Agent 是**认知模拟器（cognitive simulator）**，不是认知主体。但作为模拟器，它的操作形态 \(B = \{P, T, M, C\}\) 可以有意义地映射到 enaction 框架——这是"模拟的 enaction"而非"真正的 enaction"。

> **复述框 · 8.6 节要点**
>
> - **接受**：ReAct 是 enaction、工具是感觉运动、记忆是代谢。
> - **拒绝**：LLM Agent 不是 autopoietic、没有基本心智、是模拟而非真实。
> - **本书立场**：LLM Agent 是认知模拟器。

## 8.7 本章小结与第 9 章预告

本章深入展开 Enactivism。**生命-心灵连续性论题**主张认知是生命的基本特征。**Autopoiesis** 定义了生命的最小组织。**Enaction** 主张认知是"通过行动产生意义"。**Sensorimotor Enactivism** 主张知觉是"行动-感知的循环"。**Radical Enactivism** 主张基本心智无内容。**Enactivism 对 LLM Agent 的边界**：Agent 是认知模拟器，不是认知主体。

> **常见误区**
>
> - ❌ **把 enaction 等同于"先想后做"**：enaction 是"在做中想"，不是顺序流程。
> - ❌ **把 autopoiesis 等同于"自我复制"**：autopoiesis 是"自我生产"，不是"自我复制"。
> - ❌ **把"无内容"理解为"无结构"**：Radical Enactivism 的"无内容"不是说没有结构，是说没有表征。
> - ❌ **把"自创生"应用到 LLM Agent**：Agent 不是自创生系统，是依赖外部服务的认知模拟器。
> - ❌ **忽视 enactivism 的工程意义**：即使 LLM Agent 不是真正的认知主体，enaction 框架仍然是设计原则的来源。

第 9 章将进入 **Extended Mind 与延展心智**。7.6 节我们讨论了 Clark & Chalmers 1998 年的 parity principle；第 9 章将深入展开延展心智的哲学论证、与 Adams & Aizawa 的争论、以及延展心智对 LLM Agent 的最直接含义。

---

## 本章小结

- **生命-心灵连续性**：认知是生命的基本特征。
- **Autopoiesis**：生命的最小组织，操作闭合 + 结构耦合。
- **Enaction**：认知是行动者-环境的耦合产生。
- **Sensorimotor Enactivism**：知觉是感觉运动技能。
- **Radical Enactivism**：基本心智无内容。
- **LLM Agent 边界**：是认知模拟器，不是认知主体。

## 推荐阅读

- 📖 **Varela, Thompson, Rosch《The Embodied Mind》**（1991）：enaction 概念的系统化提出。[$TRAE_REF](https://mitpress.mit.edu/9780262720212/)
- 📖 **Thompson《Mind in Life》**（2007）：生命-心灵连续性论题的权威著作。[$TRAE_REF](https://www.hup.harvard.edu/books/9780674026740)
- 📖 **Noë《Action in Perception》**（2004）：感觉运动理论的代表。[$TRAE_REF](https://mitpress.mit.edu/9780262640633/)
- 📖 **Hutto & Myin《Radicalizing Enactivism》**（2017）：最激进立场"基本心智无内容"。[$TRAE_REF](https://mitpress.mit.edu/9780262036162/)
- 📖 **Maturana & Varela《Autopoiesis and Cognition》**（1980）：autopoiesis 原始论文集。

## 练习题

1. **概念题**：用一段话解释"生命-心灵连续性论题"为何比"认知是大脑的功能"更激进。
2. **设计题**：为一个 LLM Agent 设计 autopoiesis 的"模拟版本"：Agent 的"自生产"指的是什么？Agent 的"操作闭合"如何实现？
3. **批判题**：Radical Enactivism 主张"基本心智无内容"——LLM 的"in-context learning"是否构成"内容"？为什么？
4. **工程题**：把 ReAct 循环映射到 enaction 框架：每一步的"感知-行动"对应 enaction 的哪些要素？ReAct 的"思考"是"行动"还是"认知"？
5. **哲学题**：Varela 的 autopoietic 定义是否适用于 LLM Agent？如果不适用，LLM Agent 与"生命"的根本区别是什么？
6. **辩论题**：Radical Enactivism vs Extended Mind 哪个更适合 LLM Agent 设计？给出你的论证。

## 参考文献（本章内）

1. Varela, F. J., Thompson, E., & Rosch, E. (1991). *The Embodied Mind*. MIT Press. [$TRAE_REF](https://mitpress.mit.edu/9780262720212/)
2. Thompson, E. (2007). *Mind in Life: Biology, Phenomenology, and the Sciences of Mind*. Harvard University Press. [$TRAE_REF](https://www.hup.harvard.edu/books/9780674026740)
3. Noë, A. (2004). *Action in Perception*. MIT Press. [$TRAE_REF](https://mitpress.mit.edu/9780262640633/)
4. Hutto, D. D., & Myin, E. (2017). *Radicalizing Enactivism: Basic Minds without Content*. MIT Press. [$TRAE_REF](https://mitpress.mit.edu/9780262036162/)
5. Maturana, H. R., & Varela, F. J. (1980). *Autopoiesis and Cognition: The Realization of the Living*. D. Reidel Publishing.
6. O'Regan, J. K., & Noë, A. (2001). A Sensorimotor Account of Vision and Visual Consciousness. *Behavioral and Brain Sciences*, 24(5), 939-973.
7. De Jaegher, H., & Di Paolo, E. (2007). Participatory Sense-Making. *Phenomenology and the Cognitive Sciences*, 6(4), 485-507.
8. Thompson, E., & Varela, F. J. (2001). Radical Embodiment: Neural Dynamics and Consciousness. *Trends in Cognitive Sciences*, 5(10), 418-425.
9. Froese, T., & Di Paolo, E. (2011). The Enactive Approach. *Topics in Cognitive Science*, 3(1), 75-93.
10. Kiverstein, J., & Rietveld, E. (2018). Reconceiving Representation-Hungry Cognition. *Phenomenology and the Cognitive Sciences*, 17(1), 173-195.

---

> **本章进度**：8.1–8.7 节全部完成（约 5,500 字，含 2 张图 + 10 篇引用 + 6 题 + 5 误区 + 5 推荐），达到 26 页计划。`status: final`。
>
> **Part II 进度**：1/5 章完结（26 页 / 5,500 字）。下一章是第 9 章 **Extended Mind 与延展心智**。
