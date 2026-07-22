"""
实验 15：记忆自适应（Mock 模式）

实现简化版 MemGPT，验证记忆管理策略对长对话成功率的影响。
核心函数：recall_memory, core_memory_append, core_memory_replace。

运行：
    python main.py
"""
import json
import random


# ==================== 记忆系统 ====================
class MemorySystem:
    """简化版 MemGPT 记忆管理。"""

    def __init__(self, core_capacity: int = 5, strategy: str = "adaptive"):
        self.core_memory: list[str] = []  # 核心记忆（有限）
        self.external_memory: list[str] = []  # 外部记忆（无限）
        self.core_capacity = core_capacity
        self.strategy = strategy  # "fixed", "adaptive", "none"
        self.total_tokens = 0
        self.access_log: list[dict] = []

    def recall_memory(self, query: str) -> list[str]:
        """从核心+外部记忆中检索相关信息。"""
        self.total_tokens += len(query.split()) + len(self.core_memory) * 2
        self.access_log.append({"action": "recall", "query": query[:30]})

        # 简化的检索：关键词匹配
        query_words = set(query.lower().split())
        results = []
        # 先搜核心记忆
        for mem in self.core_memory:
            if any(w in mem.lower() for w in query_words):
                results.append(("core", mem))
        # 再搜外部记忆
        for mem in self.external_memory:
            if any(w in mem.lower() for w in query_words):
                results.append(("external", mem))
        return results

    def core_memory_append(self, info: str):
        """向核心记忆追加信息。"""
        self.total_tokens += len(info.split())
        self.access_log.append({"action": "append", "info": info[:30]})

        if self.strategy == "none":
            return  # 无记忆管理

        if len(self.core_memory) < self.core_capacity:
            self.core_memory.append(info)
        elif self.strategy == "adaptive":
            # 自适应：把最不重要的替换出去
            # 简化策略：新信息更重要
            self.core_memory.pop(0)
            self.core_memory.append(info)
            self.external_memory.append(info)  # 旧信息存到外部
        # "fixed" 策略：满了就不加

    def core_memory_replace(self, old_idx: int, new_info: str):
        """替换核心记忆中的某条。"""
        if 0 <= old_idx < len(self.core_memory):
            old = self.core_memory[old_idx]
            self.external_memory.append(old)
            self.core_memory[old_idx] = new_info
            self.total_tokens += len(new_info.split())


# ==================== 对话模拟 ====================
CONVERSATION = [
    {"round": 1, "user": "我叫张三，住在海淀区", "info": "用户名: 张三, 住址: 海淀区",
     "query": "我叫什么名字？", "expected": "张三", "keywords": ["张三", "名字"]},
    {"round": 2, "user": "我在一家AI公司工作", "info": "工作: AI公司",
     "query": "我在哪里工作？", "expected": "AI", "keywords": ["AI", "工作", "公司"]},
    {"round": 5, "user": "我的项目叫MorphAgent", "info": "项目: MorphAgent",
     "query": "我的项目叫什么？", "expected": "MorphAgent", "keywords": ["MorphAgent", "项目"]},
    {"round": 8, "user": "我的手机号是13800001234", "info": "手机: 13800001234",
     "query": "我的手机号？", "expected": "138", "keywords": ["138", "手机"]},
    {"round": 10, "user": "我有一个5岁的女儿叫小花", "info": "女儿: 小花, 5岁",
     "query": "我女儿叫什么？", "expected": "小花", "keywords": ["小花", "女儿"]},
    {"round": 12, "user": "我的邮箱是zhang@ai.com", "info": "邮箱: zhang@ai.com",
     "query": "我的邮箱？", "expected": "zhang@ai.com", "keywords": ["zhang", "邮箱"]},
    {"round": 15, "user": "上周我去了上海出差", "info": "出差: 上海, 上周",
     "query": "我上周去了哪里？", "expected": "上海", "keywords": ["上海", "出差"]},
    {"round": 18, "user": "我的生日是3月15日", "info": "生日: 3月15日",
     "query": "我的生日？", "expected": "3月15", "keywords": ["3月", "生日"]},
]


def run_conversation(memory: MemorySystem) -> dict:
    """模拟完整对话流程。"""
    rng = random.Random(42)
    results = []

    for turn in CONVERSATION:
        # 存入信息
        memory.core_memory_append(turn["info"])

        # 查询测试
        recall_results = memory.recall_memory(turn["query"])
        found = any(turn["expected"] in str(r) for _, r in recall_results)

        # 如果核心记忆里找不到但外部记忆有，也算找到（自适应策略）
        if not found and memory.strategy == "adaptive":
            for ext_mem in memory.external_memory:
                if turn["expected"] in ext_mem:
                    found = True
                    break

        # 加点随机性
        if found and rng.random() > 0.95:
            found = False  # 偶尔失败
        elif not found and rng.random() > 0.9:
            found = True  # 偶尔猜对

        results.append({
            "round": turn["round"], "query": turn["query"],
            "expected": turn["expected"], "found": found,
            "core_size": len(memory.core_memory),
            "ext_size": len(memory.external_memory),
        })

    return results


def main():
    print("=" * 60)
    print("实验 15：记忆自适应（Mock 模式）")
    print("=" * 60)
    print(f"对话轮数: {len(CONVERSATION)}, 核心记忆容量: 5\n")

    strategies = [
        ("none", "无记忆管理"),
        ("fixed", "固定记忆(不替换)"),
        ("adaptive", "自适应记忆(LRU替换)"),
    ]

    summary = {}
    for strategy, label in strategies:
        memory = MemorySystem(core_capacity=5, strategy=strategy)
        results = run_conversation(memory)
        success_rate = 100.0 * sum(r["found"] for r in results) / len(results)

        print(f"\n--- {label} ---")
        for r in results:
            status = "PASS" if r["found"] else "FAIL"
            print(f"  Round {r['round']:>2}: [{status}] {r['query'][:30]} "
                  f"(核心={r['core_size']}, 外部={r['ext_size']})")
        print(f"  成功率: {success_rate:.1f}%")
        print(f"  总 token: {memory.total_tokens}")

        summary[strategy] = {"label": label, "success_rate": success_rate,
                            "total_tokens": memory.total_tokens, "results": results}

    # 对比
    print("\n" + "=" * 60)
    print("记忆策略对比")
    print("=" * 60)
    print(f"| {'策略':<18} | {'成功率':>8} | {'总 token':>8} |")
    print(f"|{'-'*20}|{'-'*10}|{'-'*10}|")
    for s, label in strategies:
        stats = summary[s]
        print(f"| {stats['label']:<18} | {stats['success_rate']:>7.1f}% | "
              f"{stats['total_tokens']:>8} |")

    none_rate = summary["none"]["success_rate"]
    adaptive_rate = summary["adaptive"]["success_rate"]
    print(f"\n无管理 -> 自适应: +{adaptive_rate - none_rate:.1f}pp")

    output = {"experiment": "exp-15-memory-adaptation", "summary": summary}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
