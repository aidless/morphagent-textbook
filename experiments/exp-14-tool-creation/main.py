"""
实验 14：自动工具创建（Mock 模式）

模拟 Agent 根据任务失败自动识别缺失工具、创建新工具并验证的过程。
核心流程：失败检测 -> 需求分析 -> 工具创建 -> 验证 -> 迭代。

运行：
    python main.py
"""
import json
import random


# ==================== 初始工具 ====================
INITIAL_TOOLS = {
    "get_weather": {"desc": "查询天气", "fn": lambda city: {"temp": 25, "city": city}},
    "calculate": {"desc": "数学计算", "fn": lambda expr: eval(expr, {"__builtins__": {}}, {})},
    "search": {"desc": "信息搜索", "fn": lambda q: [{"title": f"Result: {q}"}]},
}

# ==================== 任务集（部分任务需要尚未创建的工具）====================
TASKS = [
    {"q": "北京天气", "needs": "get_weather", "args": {"city": "北京"},
     "expected": "北京"},
    {"q": "计算 3+5", "needs": "calculate", "args": {"expr": "3+5"},
     "expected": "8"},
    {"q": "搜索 AI 论文", "needs": "search", "args": {"query": "AI"},
     "expected": "AI"},
    {"q": "翻译 hello 到中文", "needs": "translate", "args": {"text": "hello", "to": "zh"},
     "expected": "你好"},
    {"q": "汇总销售额", "needs": "aggregate", "args": {"data": [100, 200, 150]},
     "expected": "450"},
    {"q": "生成随机密码", "needs": "generate_password", "args": {"length": 12},
     "expected": "password"},
    {"q": "格式化日期", "needs": "format_date", "args": {"date": "2026-07-22"},
     "expected": "2026"},
    {"q": "发邮件给 test@test.com", "needs": "send_email",
     "args": {"to": "test@test.com", "subject": "hi"},
     "expected": "test"},
]

# 新工具模板（Agent 会"发明"这些工具）
TOOL_TEMPLATES = {
    "translate": {"desc": "翻译文本", "fn": lambda text, to="zh": {"hello": "你好"}.get(text, text)},
    "aggregate": {"desc": "数据聚合", "fn": lambda data: sum(data)},
    "generate_password": {"desc": "生成随机密码",
                          "fn": lambda length=12: "xK9" + "mZ" * (length // 2)},
    "format_date": {"desc": "格式化日期", "fn": lambda date: date},
    "send_email": {"desc": "发送邮件", "fn": lambda to, subject="": {"sent": True, "to": to}},
}


def run_task(task: dict, tools: dict) -> dict:
    """在给定工具集上运行单个任务。"""
    needed = task["needs"]
    if needed not in tools:
        return {"success": False, "reason": f"缺少工具: {needed}",
                "task": task["q"], "needed_tool": needed}
    try:
        tool = tools[needed]
        fn = tool["fn"] if isinstance(tool, dict) else tool
        result = fn(**task["args"])
        expected = task["expected"]
        result_str = str(result)
        success = expected in result_str
        return {"success": success, "result": result_str[:100],
                "task": task["q"], "used_tool": needed}
    except Exception as e:
        return {"success": False, "reason": str(e), "task": task["q"],
                "needed_tool": needed}


def analyze_failures(results: list) -> list[str]:
    """分析失败原因，返回需要的工具列表。"""
    needed_tools = set()
    for r in results:
        if not r["success"] and "needed_tool" in r:
            needed_tools.add(r["needed_tool"])
    return sorted(needed_tools)


def create_tool(tool_name: str) -> dict:
    """模拟 Agent 创建新工具。"""
    if tool_name in TOOL_TEMPLATES:
        template = TOOL_TEMPLATES[tool_name]
        return {"name": tool_name, "desc": template["desc"], "fn": template["fn"],
                "source": "auto_created"}
    return {"name": tool_name, "desc": f"自动创建的{tool_name}工具",
            "fn": lambda **kw: f"mock result for {tool_name}", "source": "auto_created"}


def auto_tool_creation_loop(tools: dict, tasks: list, max_iterations: int = 5) -> dict:
    """自动工具创建循环。"""
    history = []
    current_tools = dict(tools)

    for iteration in range(max_iterations):
        # 运行所有任务
        results = [run_task(t, current_tools) for t in tasks]
        success_count = sum(r["success"] for r in results)
        success_rate = 100.0 * success_count / len(results)

        record = {
            "iteration": iteration + 1,
            "tools": list(current_tools.keys()),
            "tool_count": len(current_tools),
            "results": [{"task": r["task"], "success": r["success"],
                         "reason": r.get("reason", "")} for r in results],
            "success_rate": success_rate,
            "created_this_round": [],
        }

        # 分析失败
        needed = analyze_failures(results)
        if not needed:
            print(f"  迭代 {iteration+1}: 成功率 {success_rate:.1f}% (全部通过)")
            history.append(record)
            break

        # 创建缺失工具
        for tool_name in needed:
            if tool_name not in current_tools:
                new_tool = create_tool(tool_name)
                current_tools[tool_name] = new_tool
                record["created_this_round"].append(tool_name)
                print(f"  迭代 {iteration+1}: 创建工具 '{tool_name}'")

        print(f"    成功率: {success_rate:.1f}% (工具数: {len(current_tools)})")
        history.append(record)

    return {"history": history, "final_tools": list(current_tools.keys()),
            "final_tool_count": len(current_tools)}


def main():
    print("=" * 60)
    print("实验 14：自动工具创建（Mock 模式）")
    print("=" * 60)
    print(f"初始工具: {list(INITIAL_TOOLS.keys())}")
    print(f"任务数: {len(TASKS)}\n")

    result = auto_tool_creation_loop(INITIAL_TOOLS, TASKS, max_iterations=5)
    history = result["history"]

    # 对比
    print("\n" + "=" * 60)
    print("自动工具创建效果")
    print("=" * 60)

    initial_rate = history[0]["success_rate"]
    final_rate = history[-1]["success_rate"]
    print(f"初始成功率: {initial_rate:.1f}% -> 最终: {final_rate:.1f}%")
    print(f"提升: +{final_rate - initial_rate:.1f}pp")
    print(f"初始工具数: {history[0]['tool_count']} -> 最终: {result['final_tool_count']}")
    print(f"新创建工具: {result['final_tool_count'] - history[0]['tool_count']}")

    # 每轮详情
    print(f"\n| {'迭代':>4} | {'工具数':>6} | {'成功率':>8} | {'新创建工具':>16} |")
    print(f"|{'-'*6}|{'-'*8}|{'-'*10}|{'-'*18}|")
    for h in history:
        created = ", ".join(h["created_this_round"]) if h["created_this_round"] else "-"
        print(f"| {h['iteration']:>4} | {h['tool_count']:>6} | {h['success_rate']:>7.1f}% | {created:>16} |")

    output = {"experiment": "exp-14-tool-creation", **result,
              "initial_success_rate": initial_rate, "final_success_rate": final_rate}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
