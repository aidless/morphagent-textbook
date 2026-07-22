# 贡献指南

感谢你愿意为《操作形态学：自修改 LLM 智能体的具身认知》做出贡献。

## 贡献方式

我们欢迎以下形式的贡献：

1. **typo / 错别字修正**：直接 PR 修改对应章节
2. **章节大纲建议**：开 issue 标注 `outline` 标签
3. **实验代码**：开 issue 标注 `experiment` 标签
4. **一般讨论**：开 issue 标注 `discussion` 标签
5. **配图改进**：开 issue 标注 `outline` 标签
6. **翻译**：开 issue 标注 `discussion` 标签讨论
7. **新章节草案**：开 issue 标注 `outline` 标签并与主编对齐

## 提交流程

### 提交 typo 修正（最简单）

1. 直接编辑 `chapters/*.md`
2. 提交 PR，标题前缀 `[typo]` 或 `[fix]`
3. 简述修改位置与原因
4. 主编会在 7 天内 review

### 提交内容性修改

1. 先开 issue 讨论，标注 `outline` 或 `discussion`
2. 等待主编确认（issue 内回复）
3. 在对应章节 file 一个 PR
4. 标题格式：`[Ch XX] 修改主题`
5. PR 内引用对应 issue

### 提交新配图

1. 把图保存为 SVG 或 PNG，文件名 `<章节号>-<编号>-<描述>.<格式>`
2. 放在 `assets/figures/` 对应章节子目录
3. 在章节 Markdown 内引用
4. 图必须有 alt-text

### 提交实验代码

1. 代码放在 `experiments/` 对应子目录
2. 每个实验有独立 `README.md` 说明目标、依赖、运行步骤
3. 包含可重现脚本（固定随机种子、依赖版本）
4. 提交时附实验结果摘要

## 写作约定

### 章节结构

每章必须包含以下结构（详见 `docs/CHAPTER_TEMPLATE.md`）：

```yaml
---
chapter: <编号>
title_cn: <中文标题>
title_en: <English Title>
part: <I/II/III/IV/V>
pages_planned: <计划页数>
status: <outline | draft | final>
last_updated: <YYYY-MM-DD>
keywords: [<关键词列表>]
learning_objectives: [<学习目标列表>]
prerequisites: [<先修章节列表>]
---
```

### 排版规则

- 章节首句直接陈述事实或问题
- 段长：中文 3–8 句，英文 3–6 句
- 引用：行内 `[$TRAE_REF](url)`
- 公式：LaTeX，行内 `$...$` 或块 `$$...$$`
- 代码：完整可运行，最少 5 行
- 配图：每节至少 1 张图，全章 2–4 张
- 复述框：每节 1 个，全章 3–5 个
- 常见误区：全章 1–3 个
- 练习题：5–10 题，含 1 题动手

### 风格约束

- ❌ 不写「本章介绍」「接下来将」「综上所述」
- ❌ 不堆抽象名词（每个段落最多 1 个自创概念）
- ❌ 不用 emoji 装饰
- ✅ 关键概念用粗体（每节 ≤ 3 处）
- ✅ 数据/事实带可点击链接
- ✅ 每次给方法都附「适用场景」「不适用场景」

## 编辑权限

- 主仓库由主编维护
- 所有 PR 需至少 1 位 review 通过
- 重大改动（新增章节、修改大纲）需 2 位 review

## 联系方式

- 邮箱：<待填>
- GitHub Issues：直接开 issue

## 行为准则

参与本项目即表示你同意遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
