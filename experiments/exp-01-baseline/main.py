"""
实验 1：ReAct 基线 Agent（Mock 模式）

实现一个最简 ReAct Agent，包含 Thought + Action + Observation 循环。
提供 3 个工具（search、calc、weather），在 5 个任务上测试。

运行：
    python main.py
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))
from agent_loop import react_loop
from metrics import success_rate, avg_steps, avg_tokens, summary_table


# ==================== 工具定义 ====================
def get_weather(city: str) -> dict:
    """查询城市天气（mock）。"""
    weather_db = {"北京": {"temp": 28, "rain": 20}, "上海": {"temp": 31, "rain": 60},
                  "广州": {"temp": 33, "rain": 80}}
    return weather_db.get(city, {"temp": 25, "rain": 10, "city": city})


def calculate(expression: str) -> float:
    """计算数学表达式（mock，仅支持简单运算）。"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return float(result)
    except Exception:
        return 0.0


def search(query: str) -> list:
    """搜索信息（mock）。"""
    db = {
        "LLM Agent": [{"title": "ReAct: Synergizing Reasoning and Acting", "year": 2023}],
        "Embodied AI": [{"title": "Embodied Agent Survey", "year": 2024}],
    }
    for key, val in db.items():
        if key.lower() in query.lower():
            return val
    return [{"title": f"Generic result for '{query}'", "year": 2025}]


TOOLS = {"get_weather": get_weather, "calculate": calculate, "search": search}

# ==================== 测试任务 ====================
TASKS = [
    {"query": "北京今天天气如何？", "expected_answer": "北京"},
    {"query": "123 加 456 等于多少？", "expected_answer": "579"},
    {"query": "搜索 LLM Agent 最新论文", "expected_answer": "LLM"},
    {"query": "上海明天会下雨吗？", "expected_answer": "上海"},
    {"query": "200 乘以 3 等于多少？", "expected_answer": "600"},
]

# ==================== Mock LLM ====================
def mock_llm(prompt: str) -> str:
    """Mock LLM：根据 prompt 关键词选择合适的工具并返回 ReAct 格式。"""
    lower = prompt.lower()

    # 已经有 Observation 了，直接 finish
    if "Observation:" in prompt:
        obs_line = ""
        for line in prompt.split("\n"):
            if line.startswith("Observation:"):
                obs_line = line
                break
        return (
            f"Thought: 我已获得足够信息。\n"
            f'Action: {{"name": "finish", "arguments": {{"answer": "{obs_line[:120]}"}}}}'
        )

    # 天气任务
    for city in ["北京", "上海", "广州"]:
        if city in prompt:
            return (
                f"Thought: 用户问{city}天气，需要调用 get_weather。\n"
                f'Action: {{"name": "get_weather", "arguments": {{"city": "{city}"}}}}'
            )

    # 搜索任务
    if "搜索" in prompt or "search" in lower:
        kw = "LLM Agent" if "LLM" in prompt else "Embodied AI"
        return (
            f"Thought: 用户要搜索信息，使用 search 工具。\n"
            f'Action: {{"name": "search", "arguments": {{"query": "{kw}"}}}}'
        )

    # 计算任务
    if "加" in prompt or "乘" in prompt or "等于" in prompt:
        nums = [s for s in prompt.split() if s.isdigit()]
        if len(nums) >= 2:
            if "加" in prompt:
                expr = f"{nums[0]} + {nums[1]}"
            else:
                expr = f"{nums[0]} * {nums[1]}"
            return (
                f"Thought: 用户问计算题，使用 calculate 工具。\n"
                f'Action: {{"name": "calculate", "arguments": {{"expression": "{expr}"}}}}'
            )

    return (
        "Thought: 无法确定该做什么。\n"
        'Action: {"name": "finish", "arguments": {"answer": "unknown"}}'
    )


def evaluate(result: dict, task: dict) -> bool:
    """判断任务是否成功完成。"""
    answer = str(result.get("answer", "") or "")
    return result.get("success", False) and task["expected_answer"] in answer


def main():
    print("=" * 60)
    print("实验 1：ReAct 基线 Agent（Mock 模式）")
    print("=" * 60)
    print(f"\n工具列表: {list(TOOLS.keys())}")
    print(f"任务数量: {len(TASKS)}\n")

    results = []
    for task in TASKS:
        result = react_loop(query=task["query"], llm=mock_llm, tools=TOOLS, max_steps=5)
        result["query"] = task["query"]
        passed = evaluate(result, task)
        result["passed"] = passed
        results.append(result)
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {task['query'][:40]}")
        print(f"    -> steps={result['steps']}, tokens={result['total_tokens']}, "
              f"answer={str(result.get('answer',''))[:60]}")

    # 汇总
    passed_list = [r for r in results if r["passed"]]
    print("\n" + "-" * 60)
    print(f"成功率: {success_rate(results):.1f}% ({len(passed_list)}/{len(results)})")
    print(f"平均步数: {avg_steps(results):.1f}")
    print(f"平均 token: {avg_tokens(results):.0f}")
    print("\n" + summary_table(results))

    output = {"experiment": "exp-01-baseline", "results": results,
              "success_rate": success_rate(results)}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
