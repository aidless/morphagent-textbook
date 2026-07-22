"""
Offline HTML builder for the MorphAgent Textbook.
Converts all Markdown chapters into a static HTML site.
Requires: pip install markdown pyyaml
"""
import os
import re
import yaml
from pathlib import Path
from markdown import markdown

ROOT = Path(__file__).parent
CHAPTERS_DIR = ROOT / "chapters"
BUILD_DIR = ROOT / "_build" / "site"

# ------------------------------------------------------------------
# Extract YAML frontmatter + body from a .md file
# ------------------------------------------------------------------
def split_frontmatter(text: str):
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1])
            except Exception:
                meta = {}
            body = parts[2].strip()
            return meta, body
    return {}, text

# ------------------------------------------------------------------
# Build navigation data from all chapters
# ------------------------------------------------------------------
chapters = []
for f in sorted(CHAPTERS_DIR.glob("*.md")):
    text = f.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text)
    num = meta.get("chapter", 0)
    title = meta.get("title_cn", f.stem)
    part = meta.get("part", "")
    chapters.append({
        "file": f.name,
        "stem": f.stem,
        "num": num,
        "title": title,
        "part": part,
        "body": body,
    })

# Sort by chapter number
chapters.sort(key=lambda x: x["num"])

# ------------------------------------------------------------------
# HTML template
# ------------------------------------------------------------------
CSS = """
:root {
  --bg: #fafafa;
  --fg: #1a1a1a;
  --muted: #555;
  --accent: #2563eb;
  --code-bg: #f4f4f4;
  --border: #ddd;
  --sidebar-bg: #f0f0f0;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #111;
    --fg: #eee;
    --muted: #aaa;
    --accent: #60a5fa;
    --code-bg: #1e1e1e;
    --border: #333;
    --sidebar-bg: #1a1a1a;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Noto Sans CJK SC", "WenQuanYi Micro Hei", "PingFang SC", "Microsoft YaHei", sans-serif;
  background: var(--bg);
  color: var(--fg);
  line-height: 1.75;
}
.layout {
  display: flex;
  max-width: 1400px;
  margin: 0 auto;
}
.sidebar {
  width: 280px;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--border);
  padding: 1.5rem;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
.sidebar h2 {
  font-size: 1rem;
  margin: 0 0 1rem;
  color: var(--accent);
}
.sidebar ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.sidebar li {
  margin: 0.25rem 0;
}
.sidebar a {
  color: var(--muted);
  text-decoration: none;
  font-size: 0.9rem;
  display: block;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
}
.sidebar a:hover, .sidebar a.active {
  background: var(--accent);
  color: #fff;
}
.main {
  flex: 1;
  padding: 2rem 3rem;
  max-width: 900px;
}
h1, h2, h3, h4 {
  font-weight: 600;
  margin-top: 2rem;
  margin-bottom: 1rem;
}
h1 { font-size: 2rem; border-bottom: 2px solid var(--accent); padding-bottom: 0.5rem; }
h2 { font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3rem; }
h3 { font-size: 1.25rem; }
p { margin: 0.8rem 0; }
pre {
  background: var(--code-bg);
  padding: 1rem;
  border-radius: 6px;
  overflow-x: auto;
  font-size: 0.9rem;
}
code {
  background: var(--code-bg);
  padding: 0.15rem 0.35rem;
  border-radius: 3px;
  font-family: "SF Mono", "Fira Code", Consolas, monospace;
  font-size: 0.9em;
}
pre code { padding: 0; background: none; }
blockquote {
  margin: 1rem 0;
  padding: 0.5rem 1rem;
  border-left: 4px solid var(--accent);
  background: rgba(37,99,235,0.05);
  color: var(--muted);
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1rem 0;
}
th, td {
  border: 1px solid var(--border);
  padding: 0.5rem;
  text-align: left;
}
th { background: var(--sidebar-bg); }
ul, ol { margin: 0.5rem 0; padding-left: 1.5rem; }
img { max-width: 100%; height: auto; }
a { color: var(--accent); }
.nav-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}
.nav-top a {
  color: var(--accent);
  text-decoration: none;
}
@media (max-width: 900px) {
  .layout { flex-direction: column; }
  .sidebar { width: 100%; height: auto; position: relative; border-right: none; border-bottom: 1px solid var(--border); }
  .main { padding: 1rem; }
}
"""

def render_sidebar(active_stem: str):
    links = []
    current_part = None
    for ch in chapters:
        if ch["part"] and ch["part"] != current_part:
            current_part = ch["part"]
            links.append(f'<li style="margin-top:1rem;font-weight:bold;color:var(--accent);">Part {current_part}</li>')
        cls = "active" if ch["stem"] == active_stem else ""
        links.append(f'<li><a class="{cls}" href="chapter-{ch["num"]:02d}.html">{ch["num"]}. {ch["title"]}</a></li>')
    return "\n".join(links)

def build_page(ch, prev_ch, next_ch):
    sidebar = render_sidebar(ch["stem"])
    body_html = markdown(
        ch["body"],
        extensions=["fenced_code", "tables", "toc"],
    )
    prev_link = f'<a href="chapter-{prev_ch["num"]:02d}.html">← {prev_ch["num"]}. {prev_ch["title"]}</a>' if prev_ch else ""
    next_link = f'<a href="chapter-{next_ch["num"]:02d}.html">{next_ch["num"]}. {next_ch["title"]} →</a>' if next_ch else ""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{ch["num"]}. {ch["title"]} — 操作形态学</title>
<style>{CSS}</style>
</head>
<body>
<div class="layout">
<nav class="sidebar">
<h2><a href="index.html" style="color:var(--accent);text-decoration:none;">操作形态学</a></h2>
<ul>{sidebar}</ul>
</nav>
<main class="main">
<div class="nav-top">{prev_link}<a href="index.html">目录</a>{next_link}</div>
<h1>{ch["num"]}. {ch["title"]}</h1>
{body_html}
<div class="nav-top" style="margin-top:3rem;border-top:1px solid var(--border);padding-top:1rem;">{prev_link}<a href="index.html">目录</a>{next_link}</div>
</main>
</div>
</body>
</html>"""

# ------------------------------------------------------------------
# Copy assets (figures) to build dir
# ------------------------------------------------------------------
import shutil
ASSETS_SRC = ROOT / "assets" / "figures"
ASSETS_DST = BUILD_DIR / "assets" / "figures"
if ASSETS_SRC.exists():
    if ASSETS_DST.exists():
        shutil.rmtree(ASSETS_DST)
    shutil.copytree(ASSETS_SRC, ASSETS_DST)
    print(f"Copied {len(list(ASSETS_DST.glob('*.svg')))} SVG figures to build dir")

# ------------------------------------------------------------------
# Generate chapter pages
# ------------------------------------------------------------------
BUILD_DIR.mkdir(parents=True, exist_ok=True)
for i, ch in enumerate(chapters):
    prev_ch = chapters[i-1] if i > 0 else None
    next_ch = chapters[i+1] if i < len(chapters)-1 else None
    html = build_page(ch, prev_ch, next_ch)
    out = BUILD_DIR / f"chapter-{ch['num']:02d}.html"
    out.write_text(html, encoding="utf-8")
    print(f"Built {out.name}")

# ------------------------------------------------------------------
# Generate index page
# ------------------------------------------------------------------
toc_parts = {}
for ch in chapters:
    part = ch["part"] or "其他"
    toc_parts.setdefault(part, []).append(ch)

toc_html = ""
for part, items in toc_parts.items():
    toc_html += f'<h2>Part {part}</h2>\n<ul>\n'
    for ch in items:
        toc_html += f'<li><a href="chapter-{ch["num"]:02d}.html">{ch["num"]}. {ch["title"]}</a></li>\n'
    toc_html += '</ul>\n'

index_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>操作形态学：自修改 LLM 智能体的具身认知</title>
<style>{CSS}</style>
</head>
<body>
<div class="layout">
<nav class="sidebar">
<h2><a href="index.html" style="color:var(--accent);text-decoration:none;">操作形态学</a></h2>
<ul>{render_sidebar("")}</ul>
</nav>
<main class="main">
<h1>操作形态学：自修改 LLM 智能体的具身认知</h1>
<p><strong>Operational Morphology: The Embodied Cognition of Self-Modifying LLM Agents</strong></p>
<p>一本开源的研究生级教科书，覆盖 LLM 智能体从「工具」到「自进化体」的全部路程。</p>
<p>全书共 <strong>31 章</strong>（25 章正文 + 6 个附录），约 <strong>178 页</strong>，<strong>96,742 字</strong>。</p>
<hr>
{toc_html}
</main>
</div>
</body>
</html>"""

index_path = BUILD_DIR / "index.html"
index_path.write_text(index_html, encoding="utf-8")
print(f"Built {index_path.name}")
print(f"\nDone! {len(chapters)} chapters + index generated in {BUILD_DIR}")
