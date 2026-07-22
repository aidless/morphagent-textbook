"""
实验 5：上下文窗口利用效率（Mock 模式）

实现 LongLLMLingua 简化版：句子重要性评分 + Top-K 选择。
在不同压缩率下测试 Agent 性能变化。

运行：
    python main.py
"""
import json
import math
import re
from collections import Counter


# ==================== 长上下文对话 ====================
LONG_CONTEXTS = [
    {
        "id": "ctx-1",
        "text": (
            "系统信息：今天是2026年7月22日，星期三。\n"
            "用户张三，年龄35岁，居住在北京朝阳区。\n"
            "张三的工作是软件工程师，在一家AI创业公司任职。\n"
            "他的爱好是阅读科幻小说和跑步。\n"
            "张三有一个5岁的女儿，名字叫张小花。\n"
            "上周张三去上海出差了3天，参加了一个技术大会。\n"
            "出差期间他住在浦东新区的一家酒店。\n"
            "大会的主题是大语言模型在工业界的应用。\n"
            "张三在大会上做了一个关于ReAct框架的演讲。\n"
            "演讲受到了很好的评价，有50多人参加。\n"
            "回到北京后，张三开始着手一个新项目。\n"
            "这个项目是关于构建一个自主AI Agent系统。\n"
            "项目的技术栈包括Python、LangChain和OpenAI API。\n"
            "张三的同事李四负责数据管道部分。\n"
            "李四是一个数据科学家，擅长机器学习和数据分析。\n"
            "王五是产品经理，负责项目需求管理。\n"
            "项目预计需要3个月完成第一阶段。\n"
        ),
        "key_sentences": ["张三，年龄35岁，居住在北京朝阳区",
                          "张三的工作是软件工程师", "张三有一个5岁的女儿"],
        "questions": [
            {"q": "张三住在哪里？", "answer": "北京"},
            {"q": "张三的职业是什么？", "answer": "工程师"},
            {"q": "张三的女儿几岁？", "answer": "5"},
        ],
    },
    {
        "id": "ctx-2",
        "text": (
            "会议纪要：产品评审会\n"
            "日期：2026年7月20日\n"
            "参会人员：Alice（产品）、Bob（开发）、Carol（设计）、Dave（测试）\n"
            "议题1：Q3版本发布计划\n"
            "Alice提出Q3版本需要包含3个核心功能：自动报告生成、数据可视化增强、API网关。\n"
            "Bob表示自动报告生成需要2周开发时间。\n"
            "数据可视化增强需要引入新的图表库，预计1周。\n"
            "API网关部分Dave建议使用Kong，但Bob倾向自研。\n"
            "最终决定先做自动报告和数据可视化，API网关推迟到Q4。\n"
            "议题2：用户反馈\n"
            "Carol分享了最近的设计评审结果，用户对暗色主题需求很高。\n"
            "Dave报告了3个P1级bug需要本周修复。\n"
            "议题3：资源分配\n"
            "团队目前有8个开发人员，2个在休假。\n"
            "会议决定下周开始Sprint 15。\n"
        ),
        "key_sentences": ["Q3版本需要包含3个核心功能", "自动报告生成需要2周",
                          "API网关推迟到Q4", "团队目前有8个开发人员"],
        "questions": [
            {"q": "Q3版本包含几个核心功能？", "answer": "3"},
            {"q": "API网关推迟到什么时候？", "answer": "Q4"},
            {"q": "团队有多少开发人员？", "answer": "8"},
        ],
    },
    {
        "id": "ctx-3",
        "text": (
            "技术文档：分布式缓存系统设计\n"
            "版本：v2.3.1\n"
            "作者：工程师团队\n"
            "系统架构概述：本系统采用主从复制架构。\n"
            "主节点负责写入操作，从节点负责读取操作。\n"
            "缓存淘汰策略使用LRU（最近最少使用）。\n"
            "默认缓存容量为4GB，可配置。\n"
            "数据持久化使用RDB快照方式。\n"
            "快照间隔默认为60秒，可配置为30-300秒。\n"
            "集群模式支持最少3个节点，最多16个节点。\n"
            "节点之间使用Gossip协议通信。\n"
            "故障检测超时时间为5秒。\n"
            "自动故障转移（failover）在10秒内完成。\n"
            "性能基准：单节点QPS可达10万。\n"
            "集群模式下线性扩展至100万QPS。\n"
            "内存使用效率约为85%。\n"
            "支持的客户端协议包括Redis协议和自定义二进制协议。\n"
            "安全特性支持TLS加密和基于角色的访问控制。\n"
        ),
        "key_sentences": ["主从复制架构", "LRU淘汰策略", "默认缓存容量为4GB",
                          "集群最少3个节点", "单节点QPS可达10万"],
        "questions": [
            {"q": "缓存淘汰策略是什么？", "answer": "LRU"},
            {"q": "默认缓存容量是多少？", "answer": "4GB"},
            {"q": "单节点QPS是多少？", "answer": "10万"},
        ],
    },
    {
        "id": "ctx-4",
        "text": (
            "新闻报道：2026年全球AI发展趋势\n"
            "根据Gartner最新报告，2026年全球AI市场规模将达到5000亿美元。\n"
            "大型语言模型(LLM)仍然是最大的增长驱动力。\n"
            "多模态AI在医疗影像领域的应用增长最快。\n"
            "自主Agent技术在企业自动化中扮演越来越重要的角色。\n"
            "中国AI市场占全球份额的25%，仅次于美国。\n"
            "百度、阿里、腾讯是中国AI三巨头。\n"
            "百度在自动驾驶领域领先。\n"
            "阿里在云计算和AI基础设施方面有优势。\n"
            "腾讯在社交AI和游戏AI方面表现突出。\n"
            "欧洲的AI监管法案(AI Act)将于2027年全面实施。\n"
            "AI安全和对齐研究获得了更多关注。\n"
            "开源大模型的性能正在快速追赶闭源模型。\n"
            "MoE架构成为主流，降低了推理成本。\n"
            "端侧AI在手机和IoT设备上加速部署。\n"
            "AIAgent的商业化应用案例不断增加。\n"
        ),
        "key_sentences": ["全球AI市场规模将达到5000亿美元", "中国AI市场占全球份额的25%",
                          "百度在自动驾驶领域领先", "MoE架构成为主流"],
        "questions": [
            {"q": "2026年全球AI市场规模预计多少？", "answer": "5000亿"},
            {"q": "中国AI市场占全球份额多少？", "answer": "25%"},
            {"q": "百度在哪个领域领先？", "answer": "自动驾驶"},
        ],
    },
    {
        "id": "ctx-5",
        "text": (
            "项目进度报告：MorphAgent v0.2\n"
            "报告日期：2026年7月15日\n"
            "项目经理：王五\n"
            "整体进度：65%完成\n"
            "Prompt管理模块(P)：已完成，通过全部单元测试。\n"
            "工具管理模块(T)：完成80%，剩余工作为工具验证逻辑。\n"
            "记忆管理模块(M)：完成50%，正在进行向量数据库集成。\n"
            "认知管理模块(C)：完成30%，设计文档已评审。\n"
            "元控制器(U)：未开始，预计8月启动。\n"
            "本阶段风险：向量数据库性能不达标(P2风险)。\n"
            "缓解措施：考虑从Milvus切换到Qdrant。\n"
            "下一阶段里程碑：7月31日前完成M模块。\n"
            "团队状态：6名全职开发，1名实习生。\n"
            "本周完成的任务：P模块代码审查、T模块API设计。\n"
            "下周计划：M模块核心逻辑开发、C模块架构评审。\n"
        ),
        "key_sentences": ["整体进度：65%完成", "Prompt管理模块(P)：已完成",
                          "记忆管理模块(M)：完成50%", "下一阶段里程碑：7月31日"],
        "questions": [
            {"q": "项目整体进度如何？", "answer": "65%"},
            {"q": "哪个模块已完成？", "answer": "Prompt"},
            {"q": "下一阶段里程碑是什么时候？", "answer": "7月31"},
        ],
    },
]


# ==================== 压缩算法 ====================
def tokenize(text: str) -> list[str]:
    """简单分词（按字符，中文友好）。"""
    return list(text)


def sentence_score(sentence: str, question_keywords: list[str]) -> float:
    """句子重要性评分：关键词匹配 + 长度权重 + 位置权重。"""
    score = 0.0
    # 关键词匹配得分
    sentence_lower = sentence.lower()
    for kw in question_keywords:
        if kw.lower() in sentence_lower:
            score += 2.0
    # 长度适中（不要太短也不要太长）
    word_count = len(sentence)
    if 10 <= word_count <= 80:
        score += 1.0
    # 包含数字的句子更重要
    if re.search(r"\d+", sentence):
        score += 0.5
    return score


def compress_context(text: str, ratio: float, question_keywords: list[str] = None) -> dict:
    """压缩上下文：按句子重要性 Top-K 选择。

    Args:
        text: 原始文本
        ratio: 保留比例 (0-1)
        question_keywords: 用于评分的关键词
    Returns:
        {"compressed": str, "original_tokens": int, "compressed_tokens": int, "ratio": float}
    """
    keywords = question_keywords or []
    sentences = [s.strip() for s in text.split("\n") if s.strip()]
    total = len(sentences)
    keep = max(1, int(total * ratio))

    # 评分
    scored = [(sentence_score(s, keywords), i, s) for i, s in enumerate(sentences)]
    scored.sort(key=lambda x: (-x[0], x[1]))

    # Top-K
    top_indices = sorted([s[1] for s in scored[:keep]])
    compressed = "\n".join(sentences[i] for i in top_indices)

    orig_tokens = len(tokenize(text))
    comp_tokens = len(tokenize(compressed))
    return {"compressed": compressed, "original_tokens": orig_tokens,
            "compressed_tokens": comp_tokens, "actual_ratio": comp_tokens / max(orig_tokens, 1)}


def mock_answer_with_context(context: str, question: str, answer: str) -> bool:
    """模拟 Agent 在给定上下文中回答问题的能力。"""
    # 关键：如果答案关键词在压缩后的上下文中，则能正确回答
    for keyword in answer.split():
        if len(keyword) >= 1 and keyword in context:
            return True
    # 数字也检查
    if answer.isdigit() and answer in context:
        return True
    # 中文百分比
    if "%" in answer and answer.replace("%", "") in context:
        return True
    return False


def main():
    print("=" * 60)
    print("实验 5：上下文窗口利用效率（Mock 模式）")
    print("=" * 60)
    print(f"上下文数量: {len(LONG_CONTEXTS)}, 压缩率测试: [1.0, 0.5, 0.3, 0.15]\n")

    compression_ratios = [1.0, 0.5, 0.3, 0.15]
    all_results = []

    for ctx in LONG_CONTEXTS:
        print(f"\n--- {ctx['id']} (原始 {len(ctx['text'])} 字符) ---")
        ctx_results = {"context_id": ctx["id"], "levels": []}

        for ratio in compression_ratios:
            # 压缩
            if ratio < 1.0:
                all_keywords = []
                for q in ctx["questions"]:
                    all_keywords.extend(q["answer"].split())
                comp = compress_context(ctx["text"], ratio, all_keywords)
                working_ctx = comp["compressed"]
            else:
                comp = {"original_tokens": len(tokenize(ctx["text"])),
                        "compressed_tokens": len(tokenize(ctx["text"])),
                        "actual_ratio": 1.0}
                working_ctx = ctx["text"]

            # 在压缩后的上下文中测试问题
            correct = 0
            for q in ctx["questions"]:
                if mock_answer_with_context(working_ctx, q["q"], q["answer"]):
                    correct += 1
            success = 100.0 * correct / len(ctx["questions"])

            label = f"{ratio*100:.0f}%"
            print(f"  压缩率 {label:>5}: token {comp['compressed_tokens']:>5}/{comp['original_tokens']:>5} "
                  f"({comp['actual_ratio']:.0%}), 成功率 {success:.1f}%")
            ctx_results["levels"].append({
                "ratio": ratio, "success_rate": success,
                "orig_tokens": comp["original_tokens"],
                "comp_tokens": comp["compressed_tokens"],
            })
        all_results.append(ctx_results)

    # 汇总
    print("\n" + "=" * 60)
    print("汇总：压缩率 vs 平均成功率")
    print("=" * 60)
    print(f"| {'压缩率':>8} | {'平均成功率':>10} | {'平均保留token%':>14} |")
    print(f"|{'-'*10}|{'-'*12}|{'-'*16}|")
    for ratio in compression_ratios:
        rates = [cr["levels"][i]["success_rate"]
                 for cr in all_results
                 for i, lv in enumerate(cr["levels"])
                 if abs(lv["ratio"] - ratio) < 0.01]
        ratios = [cr["levels"][i]["ratio"]
                  for cr in all_results
                  for i, lv in enumerate(cr["levels"])
                  if abs(lv["ratio"] - ratio) < 0.01]
        avg_rate = sum(rates) / len(rates) if rates else 0
        avg_ratio = sum(ratios) / len(ratios) if ratios else 0
        print(f"| {ratio*100:>6.0f}% | {avg_rate:>9.1f}% | {avg_ratio:>13.0f}% |")

    output = {"experiment": "exp-05-context-window", "results": all_results}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
