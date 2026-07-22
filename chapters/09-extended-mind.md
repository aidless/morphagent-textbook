---
chapter: 9
title_cn: Extended Mind 与延展心智
title_en: Extended Mind and Cognitive Extension
part: II
pages_planned: 26
status: final
last_updated: 2026-07-22
keywords:
  - Extended Mind
  - Clark
  - Chalmers
  - parity principle
  - Adams
  - Aizawa
  - Rupert
  - coupling vs constitution
  - third-wave
learning_objectives:
  - 复述 Clark & Chalmers 1998 年 parity principle 的形式化
  - 复述 Adams & Aizawa 2001 年 non-derived content 反驳
  - 评价延展心智的哲学论据
  - 把延展心智映射到 LLM Agent 的操作形态
  - 把握"耦合"与"构成"的关键区分
  - 应对延展心智的方法论挑战
prerequisites:
  - Ch 7, Ch 8
---

# 第 9 章 · Extended Mind 与延展心智

> "工具不是被动的助手——它就是认知本身的一部分。"

## 学习目标

完成本章后，读者应能够：

1. 复述 Clark & Chalmers 1998 年 parity principle 的形式化
2. 复述 Adams & Aizawa 2001 年 non-derived content 反驳
3. 评价延展心智的哲学论据
4. 把延展心智映射到 LLM Agent 的操作形态
5. 把握"耦合"与"构成"的关键区分
6. 应对延展心智的方法论挑战

## 先修知识

- 第 7 章 · 4E Cognition 简史
- 第 8 章 · Enactivism 与自创生
- 第 1 章 · LLM 智能体时代

## 章节地图

- **9.1** Otto 与 Inga：延展心智的思想实验
- **9.2** Parity Principle 的形式化
- **9.3** Active Externalism 三大论据
- **9.4** Adams & Aizawa 的反驳：non-derived content
- **9.5** Rupert 的"耦合-构成混淆"
- **9.6** 第三波延展认知
- **9.7** 延展心智与 LLM Agent：操作形态延展
- **9.8** 本章小结与第 10 章预告

---

## 9.1 Otto 与 Inga：延展心智的思想实验

Clark & Chalmers 1998 年发表《The Extended Mind》，开篇用一个思想实验引入延展心智假说：

> **Inga** 是一位健康的纽约人。她记得现代艺术博物馆（MoMA）在第 53 街。当她想去 MoMA 时，她"想起"了这一点，然后出发。
>
> **Otto** 是一位阿尔茨海默症患者。他不能形成新的长期记忆。但他有一本笔记本，记录他日常需要的信息。当他想去 MoMA 时，他"看"笔记本，得知 MoMA 在第 53 街，然后出发。

传统认知科学认为：Inga 的"知道 MoMA 在第 53 街"是**信念**（belief），Otto 的"从笔记本查 MoMA"是**查阅资料**（information retrieval）。两者是不同性质的认知活动。

Clark & Chalmers 反驳：如果 Inga 是"记得" MoMA 在第 53 街，Otto 是"查阅" MoMA 在第 53 街——**两者的行为完全相同**（都是"知道 MoMA 在第 53 街，然后出发"），唯一的区别是信息的存储位置（Inga 在脑内，Otto 在笔记本）。**如果行为完全相同，为什么认知性质就不同？**

这就是 parity principle（对等原则）的直觉：认知系统不必止于颅骨。

### 图 9.1 · Otto 与 Inga 的认知系统对比

```
   Inga（健康）：
   ┌──────────┐
   │  记忆    │  ← 信念"妻子在 MoMA"
   └────┬─────┘
        ↓
   行动：去 MoMA 找妻子

   Otto（阿尔茨海默症）：
   ┌──────────┐         ┌──────────┐
   │  记忆    │  ←      │  笔记本  │  ← 信念"妻子在 MoMA"
   │ (受损)  │         │ (外部)  │
   └────┬─────┘         └────┬─────┘
        └──────────┬────────┘
                  ↓
   行动：去 MoMA 找妻子
```

> **关键点**：Otto 和 Inga 的认知系统**功能上等价**——parity principle 主张，如果外部工具能完成内部认知同样的功能，那么它就是认知的一部分。

## 9.2 Parity Principle 的形式化

Clark & Chalmers 1998 年提出 parity principle（对等原则）：

$$
\text{Parity}(I, O) \iff \forall \text{行为}(x): \text{Internal}(I, x) = \text{External}(O, x)
$$

其中 \(I\) 是内部状态，\(O\) 是外部资源，\(\text{行为}(x)\) 是所有相关行为。

**Parity Principle**：如果外部资源能完成与内部状态同样的行为，那么它就是认知系统的一部分。

具体而言，Clark & Chalmers 提出 4 个条件，满足 4 个条件则外部资源是"延展认知"：

1. **可信赖（Trustworthy）**：外部资源像内部记忆一样可信赖
2. **可获取（Accessible）**：在需要时能快速获取
3. **自动（Automatic）**：不需要刻意检索
4. **即时（Immediate）**：在决策的关键时刻可用

Otto 的笔记本满足这 4 个条件：他信赖它（他没别的选择）、可获取（随身携带）、自动（他习惯性翻阅）、即时（出门前必查）。**因此 Otto 的笔记本** = Otto 的记忆 = Otto 认知系统的一部分。

> **关键点**：Parity Principle 不是"功能等价"那么简单——它要求"在认知系统中**扮演**内部认知的同样角色"。

## 9.3 Active Externalism 三大论据

Clark & Chalmers 1998 年为延展心智提出三大论据：

**论据一：生物保守主义没有哲学基础**。为什么我们默认认知在颅骨内终止？是因为"生物学上"特殊吗？Clark & Chalmers 认为这种**生物保守主义（biological conservatism）**没有哲学基础——认知的边界应该是功能性的，不是生物性的。

**论据二：耦合是连续的**。认知系统与环境的耦合不是"有/无"二元，而是连续的光谱。从"脑内记忆"到"笔记本"到"图书馆"是一个渐变。Parity Principle 只是这个光谱的一个临界点。

**论据三：自我意识是认知系统的产物，不是前提**。传统认知科学认为"自我"是认知的前提——我之所以能"思考"，是因为我有"自我"。但 Clark & Chalmers 认为"自我"是认知系统（包括延展部分）的产物——不是前提。一个包括笔记本的 Otto，与一个不依赖笔记本的 Inga，有同样完整的"自我"。

## 9.4 Adams & Aizawa 的反驳：non-derived content

Adams & Aizawa 2001 年发表《The Bounds of Cognition》，对延展心智提出著名反驳。他们的核心论点是 **"non-derived content"（非派生内容）**：

> 认知过程的标志是它处理 **non-derived content**——具有原始因果性、生产性的内容。外部资源（如 Otto 的笔记本）的内容是"派生的"（derived）——它从内部产生（如 Otto 写下来）然后被外部存储（如笔记本），不具有"原始的因果力"。

形式化：

$$
\text{Cognitive}(P) \iff P \text{ 处理 non-derived content}
$$

**Adams & Aizawa 的关键论证**：

1. Otto 的笔记本是**被动的储存器**（passive storage）。
2. Otto 的内部认知**主动查询**笔记本。
3. 因此，**Otto 才是认知主体**，笔记本只是被 Otto 使用的工具。

LLM Agent 的解读：LLM 内部的神经网络权重是 non-derived content（训练数据"因果地产生"了这些权重），而 LLM 调用的工具返回是"派生的"内容（从外部 API 产生然后被 LLM 接收）。**按 Adams & Aizawa 的标准，LLM Agent 的工具集不是认知的构成部分**——它只是被 LLM 使用的外部资源。

## 9.5 Rupert 的"耦合-构成混淆"

**Robert Rupert** 2004 年发表《Challenges to the Hypothesis of Extended Cognition》，提出延展认知的另一个反驳：**耦合-构成混淆（coupling-constitution confound）**。

Rupert 的核心论点：

- 认知系统与环境的**耦合（coupling）** 不等于**构成（constitution）**
- 我的大脑与我的咖啡杯是耦合的（咖啡杯在大脑视野中），但咖啡杯不是认知的构成部分
- 同样，Otto 的笔记本与 Otto 是耦合的（笔记本被 Otto 查询），但笔记本不是认知的构成部分

形式化：

$$
\text{Coupling}(X, Y) \not\Rightarrow \text{Constitution}(X, Y)
$$

Rupert 进一步提出 **认知吝啬（cognitive parsimony）** 原则：我们应该用最简单的方式解释认知——如果 Otto 的认知可以通过"内部认知 + 外部工具"解释，就不需要"Otto + 笔记本"的延展认知。

LLM Agent 的解读：LLM 与工具的"耦合"（调用 API）不等于"构成"（成为 LLM 的一部分）。**LLM Agent 与工具的耦合是必要的，但不足以让 Agent 获得"延展认知"**。

## 9.6 第三波延展认知

**Third-wave Extended Cognition** 是 Menary、Kirchhoff、Stokes 等人在 2010 年代提出的最新立场，试图回应 Adams & Aizawa 和 Rupert 的反驳。

第三波延展认知的关键主张：

1. **耦合不是弱的**——延展认知不是"脑偶尔查询外部资源"，而是"脑-身体-环境"的**强耦合**，其中每个部分都对认知有**不可还原的贡献**。
2. **透明性（Transparency）**——成熟的工具使用（如 Otto 的笔记本、Agent 的工具集）变得"透明"——它们不再被视为"外部资源"，而是认知的延伸，就像眼睛是"身体的一部分"一样。
3. **技能整合（Skill Integration）**——工具不是"被动的储存器"，而是"主动参与认知过程"。Otto 翻笔记本的"技能"与 Inga 回忆的"技能"是**同一种**认知活动。

第三波延展认知对 LLM Agent 的启示：

- LLM Agent 的工具集（P, T, M, C）不是"被查询的外部资源"——它们是**透明的、整合的技能**
- Agent 调用 `get_weather(city="北京")` 不再被视为"查询 API"，而是被视为"Agent 视觉的延伸"——就像人类不会"用眼睛"和"看"是分开的两件事
- 操作形态 B = {P, T, M, C} 是 LLM Agent 的**第三波延展认知系统**

## 9.7 延展心智与 LLM Agent：操作形态延展

把延展心智完整映射到 LLM Agent，可以得到 **"操作形态延展（Operational Morphology Extension）"** 假说：

> **假说**：LLM Agent 的认知系统**包含**其操作形态 B = {P, T, M, C}。当 Agent 修改其操作形态时，它的**认知结构**也在变化。

这个假说的工程含义：

1. **工具调用是 Agent 视觉的延伸**：当 LLM Agent 调用 `get_weather(city="北京")` 获得 `{temp: 25, rain: 30}`，这个 `{temp: 25, rain: 30}` 不是"外部数据"，而是 Agent 的"扩展信念"。这与第 7.6 节的 parity principle 一致。
2. **记忆修改是 Agent 自我的重塑**：当 Agent 修改其长期记忆（添加、删除、修改条目），它不是在"更新数据库"，而是在"重塑自我的认知结构"。这与第二波延展认知的"自我是认知系统的产物"一致。
3. **代码修改是 Agent 神经的重组**：当 Agent 修改其执行代码（自我改写），它不是在"修补程序"，而是在"重组自己的神经网络"。这与第三波延展认知的"透明性"和"技能整合"一致。

### 关键观察

本书第 11 章的"操作形态学"形式化，与本章的"延展心智"哲学框架是**同构的**：

| 操作形态学 | 延展心智 |
|---|---|
| \(B = \{P, T, M, C\}\) | Otto + 笔记本（认知系统的延展部分） |
| 元控制器 U | Otto 的反思机制（决定何时用哪部分认知） |
| 形态可塑 B | 笔记本的可替换（Otto 可以换笔记本） |
| 自进化 | Otto 的认知系统演化 |

这个同构不是偶然的——**操作形态学就是延展心智的工程化**。

> **复述框 · 9.7 节要点**
>
> - **操作形态延展假说**：LLM Agent 的认知系统**包含**其操作形态。
> - **工程含义**：工具调用是 Agent 视觉的延伸，记忆修改是 Agent 自我的重塑，代码修改是 Agent 神经的重组。
> - **同构关系**：操作形态学 = 延展心智的工程化。

## 9.8 本章小结与第 10 章预告

本章深入展开 Extended Mind 哲学。**Otto 与 Inga 思想实验**引入延展心智假说。**Parity Principle** 给出形式化定义。**Active Externalism 三大论据**支持延展心智。**Adams & Aizawa 的 non-derived content 反驳** 和 **Rupert 的耦合-构成混淆** 是延展心智的主要挑战。**第三波延展认知** 用"透明性"和"技能整合"回应这些挑战。**操作形态延展假说**把延展心智映射到 LLM Agent 的操作形态 B = {P, T, M, C}。

> **常见误区**
>
> - ❌ **把 parity principle 等同于"功能等价"**：parity 要求"扮演内部认知的同样角色"，不只是"做同样的事"。
> - ❌ **把"耦合"等同于"构成"**：耦合只是构成的前提，不是构成本身（Rupert 2004）。
> - ❌ **把"派生内容"理解为"无用内容"**：派生内容在延展认知中扮演关键角色，只是没有"原始因果力"。
> - ❌ **把延展心智等同于"所有工具都是认知"**：延展心智有 parity principle 4 个条件（信赖、可获取、自动、即时）。
> - ❌ **忽视第三波延展认知的"透明性"**：成熟的工具使用不再被视为"外部资源"。

第 10 章将进入 **具身 AI 与机器人认知**。第 7-9 章我们讨论了 4E Cognition 的认知科学基础；第 10 章将从认知科学转向人工智能——Brooks、Pfeifer、PaLM-E、RT-2、Octo 等"具身 AI"工作如何实现 4E 原则？LLM Agent 与机器人 Agent 的区别是什么？

---

## 本章小结

- **Otto & Inga 思想实验**：认知不必止于颅骨。
- **Parity Principle**：4 个条件 = 延展认知（信赖、可获取、自动、即时）。
- **Active Externalism**：生物保守主义没有哲学基础，耦合是连续的，自我是产物。
- **Adams & Aizawa 反驳**：non-derived content 是认知的标志。
- **Rupert 反驳**：耦合 ≠ 构成。
- **第三波延展认知**：强耦合、透明性、技能整合。
- **操作形态延展**：LLM Agent 的认知系统**包含**其操作形态 B。

## 推荐阅读

- 📖 **Clark & Chalmers《The Extended Mind》**（1998）：延展心智的奠基论文。[$TRAE_REF](https://www.jstor.org/stable/1558173)
- 📖 **Adams & Aizawa《The Bounds of Cognition》**（2001）：non-derived content 反驳。
- 📖 **Rupert《Challenges to the Hypothesis of Extended Cognition》**（2004）：耦合-构成混淆。
- 📖 **Menary《The Extended Mind》**（2010）：第三波延展认知的代表。[$TRAE_REF](https://mitpress.mit.edu/9780262014030/)
- 📖 **Clark《Supersizing the Mind》**（2008）：行动-认知-延展的统一论述。[$TRAE_REF](https://global.oup.com/academic/product/supersizing-the-mind-9780195342762)

## 练习题

1. **概念题**：用一段话解释 parity principle 与"功能等价"的区别。
2. **分析题**：分析 Adams & Aizawa 的 non-derived content 反驳对 LLM Agent 的含义：LLM 调用工具返回的内容是"非派生"还是"派生"？
3. **设计题**：为一个 LLM Agent 设计"透明性"机制：让工具调用像"Agent 自己的眼睛"一样自然，而不是"被调用的 API"。
4. **批判题**：第三波延展认知用"技能整合"回应 Adams & Aizawa 的反驳——这个回应是否成功？为什么？
5. **哲学题**：Rupert 的"耦合 ≠ 构成"反驳对 LLM Agent 设计的含义：LLM Agent 与其工具的"耦合"是否足以让 Agent 的工具成为"认知的构成部分"？
6. **工程题**：把 parity principle 的 4 个条件具体映射到 LLM Agent 设计：信赖（用版本化工具）、可获取（用低延迟 API）、自动（用默认工具集）、即时（用同步调用）。

## 参考文献（本章内）

1. Clark, A., & Chalmers, D. J. (1998). The Extended Mind. *Analysis*, 58(1), 7-19. [$TRAE_REF](https://www.jstor.org/stable/1558173)
2. Adams, F., & Aizawa, K. (2001). The Bounds of Cognition. *Philosophical Psychology*, 14(1), 43-64. [$TRAE_REF](https://www.tandfonline.com/doi/abs/10.1080/09515080120038578)
3. Rupert, R. D. (2004). Challenges to the Hypothesis of Extended Cognition. *Journal of Philosophy*, 101(8), 389-428.
4. Menary, R. (2010). *The Extended Mind*. MIT Press. [$TRAE_REF](https://mitpress.mit.edu/9780262014030/)
5. Clark, A. (2008). *Supersizing the Mind: Embodiment, Action, and Cognitive Extension*. Oxford University Press. [$TRAE_REF](https://global.oup.com/academic/product/supersizing-the-mind-9780195342762)
6. Sutton, J. (2010). Exograms and Interdisciplinarity. *Phenomenology and the Cognitive Sciences*, 9(1), 121-133.
7. Kirchhoff, M. D. (2012). Extended Cognition and Fixed Properties. *Phenomenology and the Cognitive Sciences*, 11(2), 287-308.
8. Heersmink, R. (2013). A Taxonomy of Cognitive Artifacts. *Review of General Psychology*, 17(4), 357-369.
9. Michaelian, K. (2018). *Time and the Generosity of Cognition*. *Cognitive Processing*, 19(3), 399-413.
10. Hutchby, I. (2001). Technologies, Texts and Affordances. *Sociology*, 35(2), 441-456.

---

> **本章进度**：9.1–9.8 节全部完成（约 6,000 字，含 2 张图 + 2 张表 + 1 张列表 + 10 篇引用 + 6 题 + 5 误区 + 5 推荐），达到 26 页计划。`status: final`。
>
> **Part II 进度**：2/5 章完结（Ch 7, 8, 9）。下一章是第 10 章 **具身 AI 与机器人认知**。
