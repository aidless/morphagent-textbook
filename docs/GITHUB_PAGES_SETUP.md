# GitHub Pages 部署指引

> 目标：在 30 分钟内，把全书 31 章 / 800 页内容部署到 `https://<你的 GitHub 用户名>.github.io/morphagent-textbook/`，任何人通过浏览器即可阅读。

---

## 0. 前置条件（5 分钟）

| 条件 | 说明 |
|---|---|
| GitHub 账号 | 免费注册：https://github.com/join |
| Git 安装 | Windows：https://git-scm.com/download/win |
| Python 3.10+ | 用于 jupyter-book 构建 |
| 30 分钟空闲 | 一次性部署，之后自动 |

---

## 1. 创建 GitHub 仓库（2 分钟）

### 步骤 1.1：新建仓库

打开 https://github.com/new ，填写：

| 字段 | 填写 |
|---|---|
| Repository name | `morphagent-textbook` |
| Description | "An open-source textbook on self-modifying LLM agents" |
| Public / Private | **Public**（开源协议要求） |
| Add README | ✅ 勾选（不要勾选 Add .gitignore） |
| License | None（我们已有 LICENSE 文件） |

### 步骤 1.2：不要初始化 .gitignore

因为我们仓库根目录已经有 `.gitignore`。如果 GitHub 创建时也勾选了 Add .gitignore，后续会有冲突。

**截图位置**：在 https://github.com/new 页面的右侧栏。

---

## 2. 推送本地仓库（5 分钟）

### 步骤 2.1：打开 PowerShell 终端

按 `Win + X`，选择「Windows PowerShell」。

### 步骤 2.2：进入项目目录

```powershell
cd "C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f557c9ea42441f41e0cda\morphagent-textbook"
```

### 步骤 2.3：初始化 git 并提交

```powershell
git init
git add .
git commit -m "v0.8: 全书31章完稿 (25章正文+6附录/800页/200,000字)"
```

### 步骤 2.4：连接 GitHub 远程仓库

把 `<你的 GitHub 用户名>` 替换为你的真实用户名：

```powershell
git remote add origin https://github.com/<你的 GitHub 用户名>/morphagent-textbook.git
git branch -M main
git push -u origin main
```

### 步骤 2.5：弹出登录窗口

第一次 push 时会弹出 GitHub 登录窗口。用 Personal Access Token（PAT）登录。

**生成 PAT**：https://github.com/settings/tokens/new

权限范围：
- ✅ `repo`（完整仓库权限）
- ✅ `workflow`（GitHub Actions 权限）

生成后复制 token，回到 PowerShell 粘贴为密码。

---

## 3. 启用 GitHub Pages（3 分钟）

### 步骤 3.1：进入 Pages 设置

打开 https://github.com/`<你的 GitHub 用户名>`/morphagent-textbook/settings/pages

### 步骤 3.2：选择部署源

| 字段 | 选择 |
|---|---|
| Source | **Deploy from a branch** |
| Branch | **gh-pages** / **(root)** |
| 路径 | `/` (root) |

> ⚠️ 注意：本仓库的 `.github/workflows/build.yml` 已经预设使用 `peaceiris/actions-gh-pages@v4` 自动部署到 `gh-pages` 分支。你只需要选 `gh-pages` 分支即可。

### 步骤 3.3：保存并等待

点击 **Save**。页面会刷新显示"Your site is ready to be published at..."

---

## 4. 检查 GitHub Actions 构建（10 分钟）

### 步骤 4.1：查看 Actions 运行状态

打开 https://github.com/`<你的 GitHub 用户名>`/morphagent-textbook/actions

你应该看到两个 workflow：

- **build-book**：build Jupyter Book 并部署
- 状态徽章：✅ 绿色 = 成功，❌ 红色 = 失败

### 步骤 4.2：如果构建失败

点击失败的工作流，查看报错日志。常见错误：

| 报错 | 解决 |
|---|---|
| `ModuleNotFoundError: No module named 'jupyter_book'` | 在 workflow 中加 `pip install jupyter-book` |
| `ERROR: File 'chapters/XX.md' not found` | 检查文件名拼写 |
| `ERROR: Duplicate label` | 给重复的 figure 加唯一编号 |

### 步骤 4.3：构建成功后

回到 Pages 设置页面，应该显示：

> ✅ Your site is live at `https://<你的 GitHub 用户名>.github.io/morphagent-textbook/`

---

## 5. 自定义域名（可选，5 分钟）

如果你有自己的域名，可以绑定。

### 步骤 5.1：修改 `CNAME`

在仓库根目录创建 `CNAME` 文件，内容是你的域名：

```
morphagent.yourdomain.com
```

### 步骤 5.2：在域名服务商添加 DNS

添加 CNAME 记录：

| 主机记录 | 记录类型 | 记录值 |
|---|---|---|
| `morphagent` | CNAME | `<你的 GitHub 用户名>.github.io.` |

### 步骤 5.3：启用 HTTPS

回到 GitHub Pages 设置，勾选 **Enforce HTTPS**。

---

## 6. 故障排查速查表

| 问题 | 解决方案 |
|---|---|
| 页面 404 | 检查 gh-pages 分支是否存在；等待 5 分钟后重试 |
| 页面 CSS 丢失 | 检查 `_config.yml` 的 `html` 配置；不要禁用 CSS |
| 中文显示乱码 | 检查 `_config.yml` 的 `language: zh_CN` |
| 图表不显示 | 检查 `_config.yml` 的 `execute.execute_notebooks: "off"` |
| 链接失效 | 用 `grep -r "TODO" chapters/` 检查 |

---

## 7. 部署后必做：分享给第一批读者

### 7.1 发到 3 个社区

- **Twitter / X**：#AI #LLM #Agents 标签
- **机器之心 / 量子位**：联系编辑申请转载
- **知乎**：写一篇 500 字介绍，挂上链接
- **B 站 / YouTube**：录一段 5 分钟导览视频

### 7.2 收集反馈

- 在仓库开 4 类 issue：typo / outline / experiment / discussion
- 邀请 5 位试用读者，每人送一本署名纸质版（如果将来出版）

### 7.3 监控指标

| 指标 | 工具 |
|---|---|
| 网站访问量 | Google Analytics |
| GitHub Stars | GitHub Insights |
| Leanpub 销量 | Leanpub Dashboard |
| 邮件订阅 | GitHub Watch |

---

## 8. 一页总结（30 分钟部署清单）

```powershell
# 1. 创建 GitHub 仓库（2 分钟）
# 打开 https://github.com/new 创建 morphagent-textbook 仓库

# 2. 本地提交并推送（5 分钟）
cd "C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f557c9ea42441f41e0cda\morphagent-textbook"
git init
git add .
git commit -m "v0.8: 全书31章完稿 (25章正文+6附录/800页/200,000字)"
git remote add origin https://github.com/<你的用户名>/morphagent-textbook.git
git push -u origin main

# 3. 启用 GitHub Pages（3 分钟）
# 进入 Settings → Pages → Source: gh-pages / root

# 4. 等待构建（10 分钟）
# 查看 https://github.com/<你的用户名>/morphagent-textbook/actions

# 5. 验证上线（5 分钟）
# 浏览器打开 https://<你的用户名>.github.io/morphagent-textbook/
```

---

## 9. 进一步阅读

- **Jupyter Book 官方文档**：https://jupyterbook.org/
- **GitHub Pages 官方文档**：https://docs.github.com/en/pages
- **peaceiris/actions-gh-pages**：https://github.com/peaceiris/actions-gh-pages
- **CC-BY-NC-SA 协议说明**：https://creativecommons.org/licenses/by-nc-sa/4.0/

---

> **遇到问题？** 在 GitHub Issue 用 `discussion` 标签开一个新问题，标题前缀 `[deployment]`，我会协助你排查。
