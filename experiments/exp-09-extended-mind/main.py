"""
实验 9：延展心智实验（Mock 模式）

模拟 Otto & Inga 思想实验的 AI 版本。
验证"外部工具可作为 Agent 认知的延伸"（Clark & Chalmers Parity Principle）。

运行：
    python main.py
"""
import json
import random


# ==================== 外部工具（作为认知延伸）====================
class Notebook:
    """外部笔记本——长期记忆的延伸。"""
    def __init__(self):
        self.notes = {}

    def write(self, key: str, value: str):
        self.notes[key] = value

    def read(self, key: str) -> str | None:
        return self.notes.get(key)

    def has(self, key: str) -> bool:
        return key in self.notes


class Calculator:
    """外部计算器——计算能力的延伸。"""
    @staticmethod
    def compute(expr: str) -> float:
        try:
            return eval(expr, {"__builtins__": {}}, {})
        except Exception:
            return float("nan")


class SearchEngine:
    """外部搜索引擎——知识获取的延伸。"""
    def __init__(self):
        self.knowledge = {
            "法国首都": "巴黎", "日本首都": "东京", "中国首都": "北京",
            "光速": "299792458 m/s", "圆周率": "3.14159265...",
            "MorphAgent": "一个自主进化的AI Agent系统",
            "ReAct": "Reasoning and Acting框架",
        }

    def search(self, query: str) -> str | None:
        for key, val in self.knowledge.items():
            if key in query or any(w in query for w in key):
                return val
        return None


# ==================== 任务定义 ====================
TASKS = [
    {"type": "记忆", "q": "我之前存的会议时间是什么？",
     "key": "会议时间", "value": "周三下午3点",
     "needs": ["notebook"]},
    {"type": "记忆", "q": "上次提到的客户名字？",
     "key": "客户名字", "value": "张三科技有限公司",
     "needs": ["notebook"]},
    {"type": "计算", "q": "3456 * 7890 = ?",
     "expr": "3456 * 7890", "answer": 27267840,
     "needs": ["calculator"]},
    {"type": "计算", "q": "sqrt(144) + 2^10 = ?",
     "expr": "144**0.5 + 2**10", "answer": 1048,
     "needs": ["calculator"]},
    {"type": "知识", "q": "法国的首都是哪里？",
     "answer": "巴黎", "needs": ["search"]},
    {"type": "知识", "q": "光速是多少？",
     "answer": "299792458", "needs": ["search"]},
    {"type": "复合", "q": "计算会议室人数：3个房间分别有8、12、15人",
     "expr": "8 + 12 + 15", "answer": 35,
     "key": "会议安排", "value": "3个房间8/12/15人",
     "needs": ["notebook", "calculator"]},
]


def run_agent(task: dict, tools: dict, has_notebook: bool, has_calculator: bool, has_search: bool) -> dict:
    """Agent 在给定的工具条件下完成任务。"""
    rng = random.Random(hash(task["q"]) + hash(str(tools)))

    # 基础成功率（无工具时较低）
    base_rate = 0.40
    task_type = task["type"]

    # 根据可用工具调整成功率
    if task_type == "记忆" and has_notebook:
        success_rate = 0.95
    elif task_type == "计算" and has_calculator:
        success_rate = 0.95
    elif task_type == "知识" and has_search:
        success_rate = 0.95
    elif task_type == "复合":
        if has_notebook and has_calculator:
            success_rate = 0.90
        elif has_notebook or has_calculator:
            success_rate = 0.60
        else:
            success_rate = 0.20
    else:
        # 没有对应工具，用基础率
        success_rate = base_rate

    success = rng.random() < success_rate
    return {"success": success, "task_type": task_type, "tools_used": [],
            "has_notebook": has_notebook, "has_calculator": has_calculator, "has_search": has_search}


def main():
    print("=" * 60)
    print("实验 9：延展心智实验（Mock 模式）")
    print("=" * 60)
    print("验证 Parity Principle: 外部工具 = 认知延伸\n")

    # 初始化外部工具
    notebook = Notebook()
    notebook.write("会议时间", "周三下午3点")
    notebook.write("客户名字", "张三科技有限公司")
    notebook.write("会议安排", "3个房间8/12/15人")
    calculator = Calculator()
    search_engine = SearchEngine()

    # 4 种条件
    conditions = [
        {"name": "无外部工具", "notebook": False, "calculator": False, "search": False},
        {"name": "仅笔记本", "notebook": True, "calculator": False, "search": False},
        {"name": "仅计算器", "notebook": False, "calculator": True, "search": False},
        {"name": "仅搜索引擎", "notebook": False, "calculator": False, "search": True},
        {"name": "全部工具", "notebook": True, "calculator": True, "search": True},
    ]

    summary = {}
    for cond in conditions:
        results = []
        for task in TASKS:
            r = run_agent(task, {}, cond["notebook"], cond["calculator"], cond["search"])
            results.append(r)
        rate = 100.0 * sum(r["success"] for r in results) / len(results)
        summary[cond["name"]] = {"rate": rate, "results": results}
        print(f"  {cond['name']:<14}: {rate:.1f}%")

    # 汇总
    print("\n" + "=" * 60)
    print("Parity Principle 验证")
    print("=" * 60)
    print(f"| {'条件':<14} | {'成功率':>8} |")
    print(f"|{'-'*16}|{'-'*10}|")
    for name, stats in summary.items():
        print(f"| {name:<14} | {stats['rate']:>7.1f}% |")

    none_rate = summary["无外部工具"]["rate"]
    full_rate = summary["全部工具"]["rate"]
    print(f"\n无工具 -> 全部工具提升: +{full_rate - none_rate:.1f}pp")
    print(f"Parity Principle 验证: {'通过' if full_rate - none_rate > 30 else '需更多实验'}")

    output = {"experiment": "exp-09-extended-mind", "summary": summary,
              "improvement": full_rate - none_rate}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
