# 操作形态学：自修改 LLM 智能体的具身认知

> English: *Operational Morphology: The Embodied Cognition of Self-Modifying LLM Agents*

[![CI](https://github.com/aidless/morphagent-textbook/actions/workflows/build.yml/badge.svg)](https://github.com/aidless/morphagent-textbook/actions/workflows/build.yml)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![GitHub stars](https://img.shields.io/github/stars/aidless/morphagent-textbook?style=social)](https://github.com/aidless/morphagent-textbook/stargazers)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21494231.svg)](https://doi.org/10.5281/zenodo.21494231)
[![GitHub release](https://img.shields.io/github/v/release/aidless/morphagent-textbook)](https://github.com/aidless/morphagent-textbook/releases/tag/v1.0)

一本关于「自修改 LLM 智能体的操作形态学」的开源教科书。

**v1.0 · 全书 31 章正式发布（约 178 页 / 96,742 字）**

- 在线阅读: <https://aidless.github.io/morphagent-textbook/>
- GitHub 仓库: <https://github.com/aidless/morphagent-textbook>
- Zenodo DOI: <https://doi.org/10.5281/zenodo.21494231>
- GitHub Release: <https://github.com/aidless/morphagent-textbook/releases/tag/v1.0>
- ICLR 2027 论文: [research/iclr-2027-submission/paper.md](research/iclr-2027-submission/paper.md)

---

## 统计数据

| 指标 | 数值 |
|---|---|
| 章节数 | 31（25 主章节 + 6 附录） |
| 教学实验 | 31（`experiments/exp-01` … `exp-31`） |
| 研究笔记 | 14（`research/r-note-001` … `r-note-014`） |
| 论文笔记 | 35（`research/r-paper-001` … `r-paper-035`） |
| BibTeX 条目 | 143（`references.bib`） |
| SVG 配图 | 10（`assets/figures/`） |
| 总字数 | 99,281 词当量（CJK 80,787 + EN 18,494，约 183 页） |
| 练习题 | 100+ |
| ASCII 图表 | 75+ |

> 上述计数由 `python scripts/word_count.py` 实测输出，复算方法见「复算」一节。

---

## 全书配图

| 配图 | 文件 | 描述 |
|---|---|---|
| B = {P, T, M, C} 概览 | [b-tuple-overview.svg](assets/figures/b-tuple-overview.svg) | 操作形态四元组结构图 |
| 元控制器循环 | [meta-controller-loop.svg](assets/figures/meta-controller-loop.svg) | U(B_t, tau, r, C) -> B_{t+1} |
| 4E 认知模型 | [4e-cognition-model.svg](assets/figures/4e-cognition-model.svg) | Embodied + Embedded + Enacted + Extended |
| Agent 能力层级 | [agent-levels-l0-l5.svg](assets/figures/agent-levels-l0-l5.svg) | L0 ReAct -> L5 跨组件协同 |
| 形态学景观 | [morphological-landscape.svg](assets/figures/morphological-landscape.svg) | 操作形态可塑性空间 |
| 协同进化 | [synergistic-evolution.svg](assets/figures/synergistic-evolution.svg) | H2 协同演化假说 |
| 迁移学习 | [transfer-learning-agents.svg](assets/figures/transfer-learning-agents.svg) | H3 形态适配与迁移 |
| MorphBench 评测网格 | [morphbench-eval-grid.svg](assets/figures/morphbench-eval-grid.svg) | 7 组 x 5 干预 x 10 任务 |
| 治理框架 | [governance-framework.svg](assets/figures/governance-framework.svg) | 安全、审计、公平性 |
| 验证三重保障 | [verification-triple-guard.svg](assets/figures/verification-triple-guard.svg) | 沙箱 + 属性测试 + SMT |

---

## 仓库结构

```
morphagent-textbook/
├── README.md                # 本文件
├── Book.txt                 # Leanpub 主手稿（31 章合并）
├── LICENSE                  # CC-BY-NC-SA 4.0 全文
├── CONTRIBUTING.md          # 贡献指南
├── CODE_OF_CONDUCT.md       # 行为准则
├── OUTLINE.md               # 全书大纲（31 章详细目录）
├── Manuscript/              # Leanpub 手稿文件
│   ├── Book.txt             # 主手稿（31 章合并）
│   ├── Sample.txt           # Leanpub 样章
│   └── Description.txt      # Leanpub 书籍描述
├── _config.yml              # Jupyter Book 配置
├── _toc.yml                 # Jupyter Book 目录（31 章）
├── references.bib           # BibTeX 文献库（144 条目）
├── .gitignore               # Git 忽略规则
├── chapters/                # 31 章 Markdown 源文件
│   ├── 01-llm-agent-era.md
│   ├── 02-agent-basics.md
│   ├── ...
│   ├── 25-open-problems.md
│   ├── 26-appendix-a-glossary.md
│   ├── 27-appendix-b-mathematics.md
│   ├── 28-appendix-c-tools.md
│   ├── 29-appendix-d-experiments.md
│   ├── 30-appendix-e-exercise-answers.md
│   └── 31-appendix-f-references.md
├── assets/
│   └── figures/             # 10 张 SVG 配图
│       ├── b-tuple-overview.svg
│       ├── meta-controller-loop.svg
│       ├── 4e-cognition-model.svg
│       ├── agent-levels-l0-l5.svg
│       ├── morphological-landscape.svg
│       ├── synergistic-evolution.svg
│       ├── transfer-learning-agents.svg
│       ├── morphbench-eval-grid.svg
│       ├── governance-framework.svg
│       └── verification-triple-guard.svg
├── experiments/             # 30 个教学实验代码
│   ├── exp-01-baseline/
│   ├── exp-02-pomdp-claim/
│   ├── ...
│   ├── exp-30-reproducibility/
│   ├── _shared/
│   └── README.md
├── research/                # 10 篇研究笔记 + ICLR 2027 投稿
│   ├── iclr-2027-submission/
│   │   └── paper.md         # ICLR 2027 论文
│   ├── r-note-001-operational-morphology.md
│   ├── r-note-002-h1-structural-plasticity.md
│   ├── ...
│   ├── r-note-010-5-year-roadmap-detail.md
│   ├── INDEX.md
│   └── MILESTONES.md
├── scripts/                 # 构建与验证脚本
│   ├── build_book.py
│   ├── validate_chapters.py
│   └── word_count.py
├── docs/
│   ├── ROADMAP.md           # 写作路线图
│   └── CHAPTER_TEMPLATE.md  # 章节写作模板
└── .github/
    ├── workflows/
    │   └── build.yml        # GitHub Actions: 自动构建
    ├── ISSUE_TEMPLATE/
    │   ├── typo.md
    │   ├── outline.md
    │   ├── experiment.md
    │   └── discussion.md
    └── PULL_REQUEST_TEMPLATE.md
```

---

## 当前状态

**v1.0 — 正式发布（2026-07-22）**

| Part | 主题 | 章数 | 状态 |
|---|---|---|---|
| I | 基础：LLM 智能体 | 6 (Ch 1-6) | final |
| II | 具身认知与计算形态学 | 5 (Ch 7-11) | final |
| III | 自进化系统 | 6 (Ch 12-17) | final |
| IV | 系统实现 | 4 (Ch 18-21) | final |
| V | 治理、伦理与未来 | 4 (Ch 22-25) | final |
| VI | 附录 | 6 (Ch 26-31) | final |

**总计**：31 章 / 总字数 99,281（词当量：CJK 80,787 + EN 18,494）/ 10 SVG 配图 / 143 BibTeX 条目 / 100+ 练习题 / 75+ ASCII 图表 / 31 教学实验 / 14 研究笔记 / 35 论文笔记

> 计数均来自 `python scripts/word_count.py`（词当量/页数）与目录清单（实验/笔记/BibTeX），非估计。

---

## 全书核心概念

- **操作形态（Operational Morphology）**：B = {P, T, M, C}（Prompt / Tool / Memory / Code）— LLM Agent 的「软件身体」
- **元控制器 U**：U(B_t, tau_t, r_t, C) -> B_{t+1} — 自修改的决策函数
- **5 大可证伪假说（H1-H5）**：结构可塑性、协同进化、形态适应、迁移收益、治理必要性
- **MorphAgent**：5 子系统参考实现（P / T / M / C / U）
- **MorphBench**：7 组 x 5 干预 x 10 任务 x 3 重复 = 1,050 单元格评测基准
- **可验证自改**：沙箱 + 属性测试 + 形式化验证（SMT/Z3）三重保障

---

## 本地构建

### 离线 HTML 站点（推荐）

```bash
pip install markdown pyyaml
python _build_html.py
# 预览：浏览器打开 _build/site/index.html
```

### Jupyter Book（可选）

```bash
pip install jupyter-book
jupyter-book build .
# 预览：浏览器打开 _build/html/index.html
```

> 注意：在 Windows 中文路径下 Jupyter Book 可能遇到 EISDIR 错误，建议使用上面的离线 HTML 构建器。

### 验证章节格式

```bash
python scripts/validate_chapters.py
```

### Leanpub 出版

将 `Manuscript/` 目录下的 `Book.txt`、`Sample.txt`、`Description.txt` 上传到 Leanpub 项目即可。

---

## 证明什么 / 不证明什么（边界声明）

> 诚实性约束（fail-closed 哲学）：以下边界**只陈述仓库内可验证的事实**，超出范围即不声称。

**本书证明 / 提供（可复算）**

- **概念框架**：操作形态四元组 `B = {P, T, M, C}` 与元控制器 `U(B_t, tau_t, r_t, C) -> B_{t+1}` 的**形式化定义**，见 Ch 11、Ch 16、Ch 17 与 [research/iclr-2027-submission/paper.md](research/iclr-2027-submission/paper.md) §2。
- **五个可证伪假说（H1–H5）**：结构可塑性、协同进化、形态适应、迁移收益、治理必要性——每条都有对应的研究笔记（`r-note-002` 至 `r-note-007`、`r-note-010`）与实验骨架（`experiments/`）。
- **评测基准**：MorphBench 的**设计规格**（7 组 × 5 干预 × 10 任务），见 Ch 19 与 [assets/figures/morphbench-eval-grid.svg](assets/figures/morphbench-eval-grid.svg)。
- **参考实现**：MorphAgent 5 子系统（P / T / M / C / U）的**架构说明**，见 Ch 18。

**本书不证明 / 不声称（边界）**

- **不声称已训练出「能自我提升到超越固定架构」的实证 Agent**：ICLR 2027 摘要与 §1 的 "outperforms" 是**设计动机与待验证假说**，不是已测结果。仓库内可复算的 exp-01 基线 mock 结果（`experiments/results.json`）中，ReAct / Reflexion / AutoGPT / BabyAGI 四系统在 10 个 mock 任务上的 success 均为 **0/10**（mock 工具未接入真实 LLM 推理路径，属占位性数据）。因此"outperforms"目前只是**方向性主张**，不是**已证明事实**。
- **不声称实验可跨环境复现**：教学实验以 mock/占位数据为主，真实 LLM 模式需要 `OPENAI_API_KEY` 且受 5 美元硬预算约束（见 `experiments/exp-01-baseline/run.py`），本仓库未提交真实 LLM 运行日志。
- **不声称全书无内容错误**：`scripts/validate_chapters.py` 报告 31/31 章通过、1 处 WARN（`04-prompt-engineering.md` 第 274 行 `hack` 词），WARN 已记录但未消除。
- **不声称「自修改必然安全」**：Ch 22–23 明确把安全性作为**开放问题**与治理框架，提供的是攻击面分级与三重验证（沙箱 + 属性测试 + SMT）的**方法**，不是安全保证。

---

## 复算（Reproduction）

所有关键数字都来自仓库内脚本，重跑即得：

```bash
cd morphagent-textbook

# 1) 字数 / 页数统计（README「统计数据」一节）
python scripts/word_count.py

# 2) 章节格式验证（31/31 通过，1 WARN）
python scripts/validate_chapters.py

# 3) 离线 HTML 构建（31 章 + index）
pip install markdown pyyaml
python _build_html.py
# 产物: _build/site/index.html

# 4) 实验基线数据抽查（exp-01，4 系统 × 10 任务，mock）
python3 -c "import json; d=json.load(open('experiments/results.json')); [print(k, len(v), sum(1 for r in v if r.get('success'))) for k,v in d['results'].items()]"
```

> **说明**：`experiments/results.json` 的 success=0/10 是仓库内**当前可复算的真实数据**，不是笔误。任何声称「outperforms 已被实测」的说法都与这份落盘数据矛盾。

---

## 快速开始（Quick Start）

```bash
git clone https://github.com/aidless/morphagent-textbook.git
cd morphagent-textbook
pip install -r requirements.txt      # markdown, pyyaml, openai

# 构建离线站点（31 章，无网络依赖）
python _build_html.py
# 打开 _build/site/index.html

# 运行教学实验（mock 模式，无需 API key）
cd experiments/exp-01-baseline
python run.py
```

---

## 引用本书

如果你在研究或教学中使用了本书，请按以下格式引用：

```bibtex
@book{morphagent-textbook-2026,
  title     = {操作形态学：自修改 {LLM} 智能体的具身认知},
  author    = {MorphAgent Textbook Author},
  year      = {2026},
  publisher = {Open Source},
  url       = {https://github.com/aidless/morphagent-textbook},
  note      = {v1.0, 31 chapters, 96,742 words}
}
```

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！请遵循以下流程：

1. **报告错别字或内容错误**：使用 `.github/ISSUE_TEMPLATE/typo.md` 模板提交 Issue。
2. **建议大纲改进**：使用 `.github/ISSUE_TEMPLATE/outline.md` 模板提交 Issue。
3. **贡献教学实验**：使用 `.github/ISSUE_TEMPLATE/experiment.md` 模板提交 Issue 或 PR。
4. **发起讨论**：使用 `.github/ISSUE_TEMPLATE/discussion.md` 模板提交 Issue。

提交 PR 前请确保：

- `python scripts/validate_chapters.py` 全部通过（31/31）
- 遵循 `docs/CHAPTER_TEMPLATE.md` 中的格式规范
- 遵守 `CODE_OF_CONDUCT.md` 中的行为准则

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 写作节奏

- v0.1-v0.4：Part I-II 基础理论与认知科学（2026-07）
- v0.5-v0.6：Part III-IV 自进化系统与工程实现（2026-07）
- v0.7：Part V 治理、伦理与未来（2026-07）
- v0.8：Part VI 附录 + 全书定稿（2026-07）
- **v1.0：正式发布（2026-07-22）**
- 2027-Q4：社区审校 + 配图完善
- 2030-Q3：MIT Press 印刷版

---

## 许可证

[CC-BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)（开源 + 印刷版）

---

## 联系方式

- GitHub 仓库: <https://github.com/aidless/morphagent-textbook>
- 在线阅读: <https://aidless.github.io/morphagent-textbook/>
- ICLR 2027 论文: [research/iclr-2027-submission/paper.md](research/iclr-2027-submission/paper.md)
- Issues: <https://github.com/aidless/morphagent-textbook/issues>
