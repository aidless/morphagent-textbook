# Leanpub 上传操作指引

> 目标：在 15 分钟内，把全书 31 章上传到 Leanpub，生成 PDF / EPUB / 在线网页三格式出版物。

---

## 0. 前置条件

| 条件 | 说明 |
|---|---|
| Leanpub 账号 | 免费注册：https://leanpub.com/users/sign_up |
| Book.txt | `Manuscript/Book.txt`（533 KB，31 章合并） |
| Sample.txt | `Manuscript/Sample.txt`（样章目录） |
| Description.txt | `Manuscript/Description.txt`（书籍描述） |
| Git 仓库 | GitHub 仓库（推荐用 Git-backed 方式） |

---

## 1. 创建 Leanpub 项目（3 分钟）

### 步骤 1.1：新建书籍

打开 https://leanpub.com/new/book ，选择 **"Write a book with a Git repository"**（推荐）或 **"Write a book in Leanpub Flavoured Markdown"**。

### 步骤 1.2：填写基本信息

| 字段 | 填写 |
|---|---|
| Book title | 操作形态学：自修改 LLM 智能体的具身认知 |
| Subtitle | Operational Morphology: The Embodied Cognition of Self-Modifying LLM Agents |
| Author | The MorphAgent Textbook Author |
| Topic | Artificial Intelligence |
| Audience | Graduate / Professional |
| License | CC-BY-NC-SA 4.0 |

---

## 2. 连接 Git 仓库（推荐方式，5 分钟）

### 步骤 2.1：在 Leanpub 绑定 GitHub

进入 Book → Settings → Git Settings，点击 **"Connect to GitHub"**。

### 步骤 2.2：选择仓库

| 字段 | 选择 |
|---|---|
| GitHub user/org | `<你的 GitHub 用户名>` |
| Repository | `morphagent-textbook` |
| Branch | `main`（或 `master`） |
| Manuscript folder | `Manuscript/` |

### 步骤 2.3：确认文件映射

Leanpub 会自动识别以下文件：

| Leanpub 文件 | 对应路径 |
|---|---|
| Book.txt | `Manuscript/Book.txt` |
| Sample.txt | `Manuscript/Sample.txt` |
| Description.txt | `Manuscript/Description.txt` |

> 如果 Leanpub 找不到文件，在 Settings → Manuscript File Paths 手动指定路径。

---

## 3. 手动上传方式（备用，5 分钟）

如果不用 Git 连接，可以直接拖拽上传：

### 步骤 3.1：进入 Manuscript 页面

打开 Book → Manuscript → **"Upload a ZIP file"**

### 步骤 3.2：打包上传

```powershell
cd "C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f557c9ea42441f41e0cda\morphagent-textbook\Manuscript"

# 创建 ZIP
Compress-Archive -Path Book.txt,Sample.txt,Description.txt -DestinationPath manuscript-v08.zip
```

上传 `manuscript-v08.zip` 到 Leanpub。

---

## 4. 配置出版选项（3 分钟）

### 步骤 4.1：设置价格

进入 Book → Pricing：

| 字段 | 建议 |
|---|---|
| Minimum price | $0（读者可免费下载） |
| Suggested price | $19.99 |
| Your revenue | Leanpub 抽成 10%（扣除支付手续费后） |

> 本书采用 CC-BY-NC-SA 4.0 协议，建议设最低价 $0 允许免费获取，同时给愿意支持的读者付费选项。

### 步骤 4.2：设置格式

进入 Book → Formats，勾选：

- ✅ PDF
- ✅ EPUB
- ✅ Online（网页版）

### 步骤 4.3：设置封面

进入 Book → Cover，上传封面图片（推荐 1600×2400 像素）。

如果没有设计好的封面，可用 Leanpub 的在线封面生成器，选择：

- 字体：Noto Sans CJK SC
- 背景色：#1a1a2e（深蓝）
- 标题色：#e0e0e0

---

## 5. 预览与发布（4 分钟）

### 步骤 5.1：点击 Preview

进入 Book → Preview，点击 **"Create Preview"**。

Leanpub 会从 Book.txt 生成完整的 PDF / EPUB / 网页预览。处理时间约 3-5 分钟。

### 步骤 5.2：检查输出

| 检查项 | 说明 |
|---|---|
| 目录 | 确认 31 章全部出现 |
| 页数 | 确认约 800 页 |
| 中文字体 | 确认中文字符正确显示 |
| 代码块 | 确认代码格式正确 |
| 图片 | 确认 ASCII 图表正确渲染 |
| 交叉引用 | 确认章节引用正确 |

### 步骤 5.3：发布

预览检查通过后，点击 **"Publish"**：

| 选项 | 选择 |
|---|---|
| Version | v0.8 |
| Release notes | "全书 31 章完稿：25 章正文 + 6 个附录 / 800 页 / 200,000 字" |
| Notify readers | ✅（通知已订阅读者） |

---

## 6. 发布后配置

### 6.1 更新书籍描述

将 `Manuscript/Description.txt` 的内容粘贴到 Leanpub 的 Description 字段（Book → About → Description）。

### 6.2 设置样章

`Manuscript/Sample.txt` 已配置为包含全部 31 章的目录预览。Leanpub 会根据此文件生成免费样章。

### 6.3 启用读者邮件订阅

Book → Readers → 开启 **"Email me when someone buys or downloads my book"**。

---

## 7. 故障排查

| 问题 | 解决方案 |
|---|---|
| 中文显示为方框 | 在 Book → Settings → Typography 选择支持 CJK 的字体 |
| Book.txt 找不到 | 确认文件在 `Manuscript/` 目录下，且 Git 已推送 |
| 章节顺序错误 | 检查 Book.txt 中的章节排列顺序 |
| 代码块不渲染 | 确保使用 ``` 围栏代码块（Leanpub Flavoured Markdown） |
| 图片不显示 | 检查图片路径是否为相对路径，且文件已上传 |
| LaTeX 公式不渲染 | Leanpub 支持 `$...$` 行内和 `$$...$$` 块级公式 |

---

## 8. Leanpub Markdown 语法速查

Leanpub 使用 LFM（Leanpub Flavoured Markdown），与标准 Markdown 的差异：

| 功能 | 语法 |
|---|---|
| 章节 | `# 标题`（自动编号） |
| 提示框 | `> {tip} 提示内容` |
| 警告框 | `> {warning} 警告内容` |
| 重要框 | `> {important} 重要内容` |
| 讨论 | `> {discussion} 讨论内容` |
| 行间公式 | `$$公式$$` |
| 行内公式 | `$公式$` |
| 代码块 | ` ```python 代码``` ` |
| 表格 | 标准 Markdown 表格语法 |
| 脚注 | `[^1]` + `[^1]: 脚注内容` |

---

## 9. 一页总结（15 分钟发布清单）

```
1. 注册 Leanpub 账号（2 分钟）
   → https://leanpub.com/users/sign_up

2. 创建书籍项目（3 分钟）
   → https://leanpub.com/new/book
   → 选择 Git-backed 方式
   → 填写标题、作者、主题

3. 连接 Git 仓库（5 分钟）
   → Book → Settings → Git Settings
   → 绑定 GitHub 仓库 morphagent-textbook
   → Manuscript folder: Manuscript/

4. 配置出版选项（3 分钟）
   → Pricing: 最低 $0，建议 $19.99
   → Formats: PDF + EPUB + Online
   → Cover: 上传或生成封面

5. 预览并发布（2 分钟）
   → Preview → Create Preview
   → 检查输出 → Publish v0.8
```

---

> **遇到问题？** 在 Leanpub 帮助中心搜索：https://help.leanpub.com/ ，或在 GitHub Issue 用 `[leanpub]` 标签提问。
