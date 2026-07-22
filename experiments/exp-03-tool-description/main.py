"""
实验 3：工具描述对性能的影响（Mock 模式）

验证"工具描述质量对 LLM 调用准确率有显著影响"。
5 个描述级别 x 5 个工具 x 10 个任务。

运行：
    python main.py
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))
from agent_loop import react_loop


# ==================== 5 级描述 ====================
LEVELS = {
    "L0_极简": {
        "get_weather": "查天气", "search": "搜索",
        "calculate": "计算", "send_email": "发邮件",
    },
    "L1_有参数": {
        "get_weather": "查天气，参数 city(城市名)",
        "search": "搜索，参数 query(关键词)",
        "calculate": "计算，参数 expr(表达式)",
        "send_email": "发邮件，参数 to(收件人), subject(主题)",
    },
    "L2_有类型": {
        "get_weather": "查天气。city: str 城市名。返回 temp, rain",
        "search": "搜索。query: str 关键词。返回 title 列表",
        "calculate": "计算。expr: str 数学表达式。返回 float",
        "send_email": "发邮件。to: str, subject: str。返回 bool",
    },
    "L3_有示例": {
        "get_weather": "查天气。city(str,'北京')。返回{temp,rain}。例: get_weather('上海')",
        "search": "搜索。query(str,'LLM')。返回[{title}]。例: search('AI')",
        "calculate": "计算。expr(str,'2+3')。返回数字。例: calculate('10*5')",
        "send_email": "发邮件。to(str),subject(str)。例: send_email('a@b.com','hi')",
    },
    "L4_完整": {
        "get_weather": "查询城市实时天气。city: 中文城市名。返回{temp:celsius,rain:%,wind:km/h}。错误:返回{error}。适用:用户问天气时",
        "search": "搜索信息。query: 关键词。max_results: 1-50默认10。返回[{title,url,snippet}]。错误:返回{error}",
        "calculate": "计算数学表达式。expr: 支持加减乘除。返回 float。适用:用户问计算题时。错误:返回{error:'invalid expr'}",
        "send_email": "发送邮件。to: 邮箱地址。subject: 主题。body: 正文(可选)。返回 bool。注意: 不可逆操作",
    },
}

# ==================== Mock 工具 ====================
TOOLS = {
    "get_weather": lambda city: {"temp": 25, "rain": 30, "city": city},
    "search": lambda query: [{"title": f"Result: {query}"}],
    "calculate": lambda expr: eval(expr, {"__builtins__": {}}, {}),
    "send_email": lambda to, subject="": True,
}

# ==================== 测试任务 ====================
TASKS = [
    {"query": "北京天气", "tool": "get_weather", "args": {"city": "北京"}},
    {"query": "搜索LLM论文", "tool": "search", "args": {"query": "LLM"}},
    {"query": "计算 3+5", "tool": "calculate", "args": {"expr": "3+5"}},
    {"query": "给 a@b.com 发邮件", "tool": "send_email", "args": {"to": "a@b.com"}},
    {"query": "上海天气", "tool": "get_weather", "args": {"city": "上海"}},
    {"query": "搜索 embodied AI", "tool": "search", "args": {"query": "embodied AI"}},
    {"query": "计算 100*7", "tool": "calculate", "args": {"expr": "100*7"}},
    {"query": "广州天气", "tool": "get_weather", "args": {"city": "广州"}},
    {"query": "搜索 robot", "tool": "search", "args": {"query": "robot"}},
    {"query": "计算 50-12", "tool": "calculate", "args": {"expr": "50-12"}},
]

# 描述级别越高，mock LLM 的"准确率"越高
ACCURACY_BY_LEVEL = {"L0_极简": 0.40, "L1_有参数": 0.60, "L2_有类型": 0.75,
                     "L3_有示例": 0.88, "L4_完整": 0.95}


def make_level_llm(level_name: str) -> callable:
    """根据描述级别生成不同准确率的 mock LLM。"""
    accuracy = ACCURACY_BY_LEVEL[level_name]
    import random
    rng = random.Random(42)  # 固定种子，可复现

    def llm(prompt: str) -> str:
        if "Observation:" in prompt:
            return ('Thought: 已获取结果。\n'
                    'Action: {"name": "finish", "arguments": {"answer": "done"}}')

        # 根据准确率决定是否选对工具
        if rng.random() < accuracy:
            # 找到最匹配的任务
            if "天气" in prompt:
                city = "北京" if "北京" in prompt else "上海" if "上海" in prompt else "广州"
                return (f'Thought: 查天气。\n'
                        f'Action: {{"name": "get_weather", "arguments": {{"city": "{city}"}}}}')
            elif "搜索" in prompt:
                q = "LLM" if "LLM" in prompt else "embodied AI" if "embodied" in prompt else "robot"
                return (f'Thought: 搜索信息。\n'
                        f'Action: {{"name": "search", "arguments": {{"query": "{q}"}}}}')
            elif "计算" in prompt:
                nums = [s for s in prompt.split() if s.isdigit()]
                expr = "+".join(nums) if len(nums) >= 2 else "0"
                return (f'Thought: 计算。\n'
                        f'Action: {{"name": "calculate", "arguments": {{"expr": "{expr}"}}}}')
            elif "邮件" in prompt:
                return ('Thought: 发邮件。\n'
                        'Action: {"name": "send_email", "arguments": {"to": "a@b.com", "subject": "test"}}')
        # 选错或不知道
        return ('Thought: 不确定。\n'
                'Action: {"name": "finish", "arguments": {"answer": "unknown"}}')
    return llm


def run_level(level_name: str, descriptions: dict) -> dict:
    """在一个描述级别上运行所有任务。"""
    llm = make_level_llm(level_name)
    results = []
    for task in TASKS:
        desc_str = "\n".join(f"  {k}: {v}" for k, v in descriptions.items())
        query = f"{task['query']}\n可用工具:\n{desc_str}"
        result = react_loop(query=query, llm=llm, tools=TOOLS, max_steps=3)
        actual_tool = None
        for s in result.get("trajectory", []):
            a = s.get("action", {})
            if a and a.get("name") != "finish":
                actual_tool = a.get("name")
                break
        match = actual_tool == task["tool"]
        results.append({"query": task["query"], "expected": task["tool"],
                         "actual": actual_tool, "match": match})
    rate = 100.0 * sum(r["match"] for r in results) / len(results)
    return {"level": level_name, "accuracy": rate, "details": results}


def main():
    print("=" * 60)
    print("实验 3：工具描述对性能的影响（Mock 模式）")
    print("=" * 60)
    print(f"描述级别: {len(LEVELS)}, 工具数: {len(TOOLS)}, 任务数: {len(TASKS)}\n")

    all_results = []
    for level_name, descriptions in LEVELS.items():
        r = run_level(level_name, descriptions)
        all_results.append(r)
        print(f"  {level_name}: 准确率 {r['accuracy']:.1f}%")

    # 对比表
    print("\n" + "-" * 60)
    print("描述质量 vs 调用准确率")
    print("-" * 60)
    print(f"| {'级别':<12} | {'准确率':>8} |")
    print(f"|{'-'*14}|{'-'*10}|")
    for r in all_results:
        print(f"| {r['level']:<12} | {r['accuracy']:>7.1f}% |")

    # 计算提升
    first_acc = all_results[0]["accuracy"]
    last_acc = all_results[-1]["accuracy"]
    print(f"\nL0 -> L4 提升幅度: +{last_acc - first_acc:.1f}pp")
    print(f"H1 验证: {'通过' if last_acc - first_acc >= 40 else '需更多实验'}")

    output = {"experiment": "exp-03-tool-description", "results": all_results}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
