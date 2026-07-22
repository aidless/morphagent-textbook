# 操作形态学：自修改 LLM 智能体的具身认知

> English: *Operational Morphology: The Embodied Cognition of Self-Modifying LLM Agents*

一本关于「自修改 LLM 智能体的操作形态学」的开源教科书。

**v0.8 · 全书 31 章完稿（800 页 / 200,000 字）**

## 仓库结构

```
morphagent-textbook/
├── README.md                # 本文件
├── Book.txt                 # Leanpub 主手稿（31 章合并）
├── LICENSE                  # CC-BY-NC-SA 4.0 全文
├── CONTRIBUTING.md          # 贡献指南
├── CODE_OF_CONDUCT.md       # 行为准则
├── OUTLINE.md               # 全书大纲（31 章详细目录）
├── _config.yml              # Jupyter Book 配置
├── _toc.yml                 # Jupyter Book 目录（31 章）
├── references.bib           # BibTeX 文献库
├── .gitignore               # Git 忽略规则
├── chapters/                # 31 章 Markdown 源文件
│   ├── 01-llm-agent-era.md
│   ├── 02-agent-basics.md
│   ├── ...
│   ├── 25-open-problems.md
│   └── 31-appendix-f-references.md
├── Manuscript/              # Leanpub 出版材料
│   ├── Book.txt             # 合并后的完整手稿（533 KB）
│   ├── Sample.txt           # Leanpub 样章文件
│   └── Description.txt      # Leanpub 书籍描述
├── _build/site/             # 离线 HTML 站点（32 文件）
│   ├── index.html           # 首页
│   ├── chapter-01.html      # 第 1 章
│   ├── ...
│   └── chapter-31.html      # 附录 F
├── experiments/             # 教学实验代码
│   ├── exp-01-baseline/
│   ├── exp-02-pomdp-claim/
│   ├── exp-03-tool-description/
│   ├── exp-04-self-modifying-prompt/
│   └── _shared/
├── research/                # 研究笔记
│   ├── r-note-001-operational-morphology.md
│   ├── INDEX.md
│   └── MILESTONES.md
├── benchmarks/              # 评测基准
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

## 当前状态

**v0.8 — 全书完稿（2026-07-22）**

| Part | 主题 | 章数 | 页数 | 状态 |
|---|---|---|---|---|
| I | 基础：LLM 智能体 | 6 (Ch 1-6) | 140 | ✅ 完成 |
| II | 具身认知与计算形态学 | 5 (Ch 7-11) | 130 | ✅ 完成 |
| III | 自进化系统 | 6 (Ch 12-17) | 168 | ✅ 完成 |
| IV | 系统实现 | 4 (Ch 18-21) | 120 | ✅ 完成 |
| V | 治理、伦理与未来 | 4 (Ch 22-25) | 100 | ✅ 完成 |
| VI | 附录 | 6 (Ch 26-31) | 150 | ✅ 完成 |

**总计**：31 章 / 800 页 / 200,000 字 / 100+ 配图 / 100+ 引用 / 150+ 练习题

## 全书核心概念

- **操作形态（Operational Morphology）**：B = {P, T, M, C}（Prompt / Tool / Memory / Code）— LLM Agent 的「软件身体」
- **元控制器 U**：U(B_t, τ_t, r_t, C) → B_{t+1} — 自修改的决策函数
- **5 大可证伪假说（H1-H5）**：结构可塑性、协同进化、形态适应、迁移收益、治理必要性
- **MorphAgent**：5 子系统参考实现（P / T / M / C / U）
- **MorphBench**：7 组 × 5 干预 × 10 任务 × 3 重复 = 1,050 单元格评测基准
- **可验证自改**：沙箱 + 属性测试 + 形式化验证（SMT/Z3）三重保障

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

### Leanpub 出版

将 `Manuscript/` 目录下的 `Book.txt`、`Sample.txt`、`Description.txt` 上传到 Leanpub 项目即可。

## 写作节奏

- v0.1-v0.4：Part I-II 基础理论与认知科学（2026-07）
- v0.5-v0.6：Part III-IV 自进化系统与工程实现（2026-07）
- v0.7：Part V 治理、伦理与未来（2026-07）
- v0.8：Part VI 附录 + 全书定稿（2026-07）
- 2027-Q4：社区审校 + 配图完善
- 2030-Q3：MIT Press 印刷版

## 许可证

CC-BY-NC-SA 4.0（开源 + 印刷版）

## 联系方式

- 作者：MorphAgent Textbook Author
- 邮箱：`author@morphagent-textbook.org`（待替换为真实邮箱）
- 主页：https://github.com/<待填>/morphagent-textbook
- 通信地址：Open Source Project, GitHub Repository

### 作者署名模板

本书采用 **单作者 + 开放协作** 模式。如果你希望改成其他署名，可以参考以下三种模板：

#### 模板 A · 单作者（当前默认）

```yaml
author: "Your Name"
copyright: "2026, Your Name"
contact:
  email: "you@example.com"
  homepage: "https://yourdomain.com"
```

#### 模板 B · 团队（2-5 人）

```yaml
authors:
  - "Author One"
  - "Author Two"
  - "Author Three"
copyright: "2026, The MorphAgent Group"
contact:
  email: "group@morphagent.org"
  homepage: "https://morphagent.org"
```

#### 模板 C · 实验室 / 研究机构

```yaml
authors:
  - "Your Name"
  - "Your Lab Name"
copyright: "2026, Your Institution"
contact:
  email: "lab@institution.edu"
  homepage: "https://lab.institution.edu"
```
