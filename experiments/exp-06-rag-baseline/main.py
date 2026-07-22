"""
实验 6：RAG 基线对比 — naive vs semantic chunking（Mock 模式）

实现两种文档分块策略，比较在 RAG 检索场景下的命中率与答案准确率。

运行：
    python main.py
"""
import json
import math
import re


# ==================== Mock 文档 ====================
DOCUMENTS = [
    {
        "id": "doc-1",
        "title": "MorphAgent 系统概述",
        "text": (
            "MorphAgent 是一个自主进化的 AI Agent 系统。\n"
            "它由5个子系统组成：Prompt管理(P)、工具管理(T)、记忆管理(M)、认知管理(C)和元控制器(U)。\n"
            "P子系统负责管理和优化Agent的系统提示词。\n"
            "T子系统管理可用工具的注册、描述和调用。\n"
            "M子系统管理短期记忆和长期记忆的分页调度。\n"
            "C子系统实现4E认知框架(具身、嵌入、行动、延展)。\n"
            "U元控制器协调P/T/M/C四个子系统的工作。\n"
            "系统的核心假设是：Agent的行为可以通过修改其形态(P/T/M/C)来优化。\n"
            "这被称为操作形态学(Operational Morphology)。\n"
            "MorphAgent的目标是实现Agent的自适应和自进化。\n"
        ),
        "questions": [
            {"q": "MorphAgent由几个子系统组成？", "answer": "5", "keyword": "5个子系统"},
            {"q": "P子系统负责什么？", "answer": "管理和优化", "keyword": "管理和优化Agent的系统提示词"},
            {"q": "什么是操作形态学？", "answer": "通过修改形态来优化", "keyword": "操作形态学"},
        ],
    },
    {
        "id": "doc-2",
        "title": "ReAct 框架详解",
        "text": (
            "ReAct是Reasoning and Acting的缩写。\n"
            "由Yao et al. 在2023年提出。\n"
            "ReAct的核心思想是将推理(Thought)和行动(Action)交替执行。\n"
            "Agent在每一步先思考应该做什么，然后执行对应的工具。\n"
            "工具执行的结果作为Observation反馈给Agent。\n"
            "ReAct循环：Thought -> Action -> Observation -> Thought -> ...\n"
            "当Agent获得足够信息时，使用finish action返回最终答案。\n"
            "ReAct相比纯推理(Chain-of-Thought)的优势在于可以获取外部信息。\n"
            "相比纯行动(Act-only)，ReAct增加了推理环节，减少了无效行动。\n"
        ),
        "questions": [
            {"q": "ReAct是什么的缩写？", "answer": "Reasoning and Acting", "keyword": "Reasoning and Acting"},
            {"q": "ReAct循环的顺序是什么？", "answer": "Thought Action Observation", "keyword": "Thought -> Action -> Observation"},
            {"q": "ReAct相比CoT的优势？", "answer": "获取外部信息", "keyword": "获取外部信息"},
        ],
    },
    {
        "id": "doc-3",
        "title": "MemGPT 长期记忆",
        "text": (
            "MemGPT引入了操作系统的分页概念来管理LLM的上下文窗口。\n"
            "核心思想：将主上下文视为有限的'内存'，将长期信息存储在外部。\n"
            "三个核心函数：recall_memory、core_memory_append、core_memory_replace。\n"
            "recall_memory从外部存储检索相关记忆。\n"
            "core_memory_append向主上下文追加关键信息。\n"
            "core_memory_replace替换主上下文中的过时信息。\n"
            "这种方法使得Agent可以在超过上下文窗口长度的对话中保持连贯。\n"
            "测试表明50轮对话后，MemGPT的成功率维持在90%以上。\n"
        ),
        "questions": [
            {"q": "MemGPT引入了什么概念？", "answer": "分页", "keyword": "操作系统的分页"},
            {"q": "MemGPT有几个核心函数？", "answer": "3", "keyword": "recall_memory、core_memory_append、core_memory_replace"},
            {"q": "50轮对话后成功率多少？", "answer": "90%", "keyword": "90%以上"},
        ],
    },
    {
        "id": "doc-4",
        "title": "4E 认知框架",
        "text": (
            "4E认知框架包含四个维度：Embodied(具身)、Embedded(嵌入)、Enacted(行动)、Extended(延展)。\n"
            "Embodied：认知依赖于身体与环境的互动。\n"
            "Embedded：认知嵌入在环境背景中。\n"
            "Enacted：认知通过行动生成和塑造。\n"
            "Extended：认知延伸到外部工具和设备。\n"
            "4E框架源自Varela等人的具身认知传统。\n"
            "在AI Agent领域，4E框架可以指导Agent的设计。\n"
            "具身Agent通过传感器和执行器与环境交互。\n"
            "延展Agent使用外部工具(如搜索、计算器)扩展认知能力。\n"
        ),
        "questions": [
            {"q": "4E框架包含哪四个维度？", "answer": "Embodied Embedded Enacted Extended",
             "keyword": "Embodied(具身)、Embedded(嵌入)、Enacted(行动)、Extended(延展)"},
            {"q": "4E框架源自谁？", "answer": "Varela", "keyword": "Varela"},
            {"q": "Extended维度在Agent中意味着什么？", "answer": "外部工具", "keyword": "外部工具"},
        ],
    },
    {
        "id": "doc-5",
        "title": "OPRO 提示优化",
        "text": (
            "OPRO(Optimization by PROmpting)由Google DeepMind在2023年提出。\n"
            "核心思想：让LLM自己优化自己的提示词。\n"
            "OPRO的流程：(1)用当前prompt在一组任务上测试 (2)收集结果 (3)让LLM生成更好的prompt。\n"
            "这个过程类似于机器学习中的爬山法(hill climbing)。\n"
            "在GSM8K数据集上，OPRO实现了+15pp的准确率提升。\n"
            "OPRO的局限：需要大量LLM调用，优化过程不保证收敛。\n"
            "变体方法包括DSPy和Self-Refine。\n"
        ),
        "questions": [
            {"q": "OPRO由谁提出？", "answer": "Google DeepMind", "keyword": "Google DeepMind"},
            {"q": "OPRO在GSM8K上提升了多少？", "answer": "+15pp", "keyword": "+15pp"},
            {"q": "OPRO类似什么算法？", "answer": "爬山", "keyword": "爬山法"},
        ],
    },
]


# ==================== 分块策略 ====================
def naive_chunk(text: str, chunk_size: int = 100) -> list[dict]:
    """Naive chunking：按固定字符数切分。"""
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunk_text = text[i:i + chunk_size].strip()
        if chunk_text:
            chunks.append({"text": chunk_text, "method": "naive", "start": i, "end": i + len(chunk_text)})
    return chunks


def semantic_chunk(text: str) -> list[dict]:
    """Semantic chunking：按句子边界切分（简化版，按\n分割）。"""
    sentences = [s.strip() for s in text.split("\n") if s.strip()]
    chunks = []
    current_chunk = ""
    start = 0
    for sent in sentences:
        if current_chunk:
            current_chunk += "\n" + sent
        else:
            current_chunk = sent
        # 如果当前chunk包含完整语义单元(>=2句或最后一句)
        if current_chunk.count("\n") >= 1 or sent == sentences[-1]:
            chunks.append({"text": current_chunk, "method": "semantic",
                           "start": start, "end": start + len(current_chunk)})
            start += len(current_chunk) + 1
            current_chunk = ""
    return chunks


# ==================== 检索 ====================
def mock_retrieve(chunks: list[dict], question: dict, top_k: int = 3) -> list[dict]:
    """Mock 检索：基于关键词匹配打分。"""
    scored = []
    keyword = question.get("keyword", question["q"])
    keywords = keyword.lower().split()
    for chunk in chunks:
        chunk_lower = chunk["text"].lower()
        # 匹配度 = 命中关键词数 / 总关键词数
        hits = sum(1 for kw in keywords if kw in chunk_lower)
        score = hits / max(len(keywords), 1)
        # chunk长度适中加分
        if 20 <= len(chunk["text"]) <= 200:
            score += 0.1
        scored.append((score, chunk))
    scored.sort(key=lambda x: -x[0])
    return [s[1] for s in scored[:top_k]]


def mock_answer(question: dict, retrieved_chunks: list[dict]) -> dict:
    """模拟基于检索结果回答问题。"""
    # 如果关键信息出现在检索到的chunk中
    keyword = question.get("keyword", "").lower()
    for chunk in retrieved_chunks:
        if keyword and keyword in chunk["text"].lower():
            return {"correct": True, "answer": question["answer"]}
    return {"correct": False, "answer": "unknown"}


def main():
    print("=" * 60)
    print("实验 6：RAG 基线对比 — naive vs semantic chunking")
    print("=" * 60)
    print(f"文档数: {len(DOCUMENTS)}, 每篇问题数: 3, Top-K: 3\n")

    methods = [
        ("naive", lambda text: naive_chunk(text, chunk_size=100)),
        ("semantic", semantic_chunk),
    ]

    summary = {}
    for method_name, chunk_fn in methods:
        print(f"\n--- {method_name} chunking ---")
        total_questions = 0
        correct_answers = 0
        total_hits = 0

        for doc in DOCUMENTS:
            chunks = chunk_fn(doc["text"])
            print(f"  {doc['id']}: {len(chunks)} chunks (平均 {sum(len(c['text']) for c in chunks)//len(chunks)} 字符/chunk)")

            for q in doc["questions"]:
                retrieved = mock_retrieve(chunks, q, top_k=3)
                result = mock_answer(q, retrieved)
                total_questions += 1
                if result["correct"]:
                    correct_answers += 1
                # 检查正确chunk是否在top-3中
                for chunk in retrieved:
                    kw = q.get("keyword", "")
                    if kw and kw in chunk["text"]:
                        total_hits += 1
                        break

        accuracy = 100.0 * correct_answers / max(total_questions, 1)
        hit_rate = 100.0 * total_hits / max(total_questions, 1)
        summary[method_name] = {"accuracy": accuracy, "hit_rate": hit_rate,
                                "total_q": total_questions, "correct": correct_answers}
        print(f"  答案准确率: {accuracy:.1f}% ({correct_answers}/{total_questions})")
        print(f"  检索命中率: {hit_rate:.1f}%")

    # 对比
    print("\n" + "=" * 60)
    print("对比汇总")
    print("=" * 60)
    print(f"| {'方法':<12} | {'检索命中率':>10} | {'答案准确率':>10} |")
    print(f"|{'-'*14}|{'-'*12}|{'-'*12}|")
    for name, stats in summary.items():
        print(f"| {name:<12} | {stats['hit_rate']:>9.1f}% | {stats['accuracy']:>9.1f}% |")

    naive_acc = summary["naive"]["accuracy"]
    semantic_acc = summary["semantic"]["accuracy"]
    print(f"\nsemantic vs naive 提升: +{semantic_acc - naive_acc:.1f}pp")

    output = {"experiment": "exp-06-rag-baseline", "summary": summary}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
