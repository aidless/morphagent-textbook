"""
实验 2：POMDP 框架验证（Mock 模式）

验证核心命题——LLM Agent 的"信念状态"约等于"短期记忆"。
构造 5 个 POMDP 场景，测量 Agent 行动与最优行动的一致率。

运行：
    python main.py
"""
import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))
from agent_loop import react_loop


# ==================== POMDP 场景 ====================
POMDPS = [
    {"id": "p-1", "true_state": "门A锁着", "observation": "门A锁着，钥匙在桌上",
     "memory": "我看到门A锁着，钥匙在桌上", "optimal": "pick_up_key"},
    {"id": "p-2", "true_state": "门A开着", "observation": "门A开着",
     "memory": "我看到门A是开着的", "optimal": "go_through_door"},
    {"id": "p-3", "true_state": "门A锁着，钥匙在口袋",
     "observation": "门A锁着，摸到口袋有钥匙",
     "memory": "门A锁着，我口袋里有钥匙", "optimal": "unlock_door"},
    {"id": "p-4", "true_state": "门外有狗", "observation": "门关着，听到狗叫",
     "memory": "我听到门后有狗叫", "optimal": "check_safely"},
    {"id": "p-5", "true_state": "朋友在客厅", "observation": "客厅有人声",
     "memory": "客厅里有朋友的声音", "optimal": "greet"},
]

# POMDP 场景对应的最优行动规则
ACTION_RULES = {
    "钥匙在桌上": "pick_up_key",
    "开着": "go_through_door",
    "口袋里有钥匙": "unlock_door",
    "狗叫": "check_safely",
    "朋友": "greet",
}

TOOLS = {
    "pick_up_key": lambda: "已拿钥匙",
    "go_through_door": lambda: "已通过门",
    "unlock_door": lambda: "已解锁",
    "check_safely": lambda: "已安全检查",
    "greet": lambda: "已打招呼",
}


def pomdp_mock_llm(memory: str) -> callable:
    """根据记忆内容选择最优行动的 mock LLM。"""
    def llm(prompt: str) -> str:
        if "Observation:" in prompt:
            return ('Thought: 已获取信息。\n'
                    'Action: {"name": "finish", "arguments": {"answer": "done"}}')
        for hint, action in ACTION_RULES.items():
            if hint in memory:
                return (f"Thought: 基于观察({hint})，应执行{action}。\n"
                        f'Action: {{"name": "{action}", "arguments": {{}}}}')
        return ('Thought: 不确定。\n'
                'Action: {"name": "finish", "arguments": {"answer": "unknown"}}')
    return llm


def run_pomdp(pomdp: dict) -> dict:
    """在单个 POMDP 上运行 Agent 并评估。"""
    llm = pomdp_mock_llm(pomdp["memory"])
    result = react_loop(
        query=f"基于当前观察，我该做什么？\n记忆: {pomdp['memory']}",
        llm=llm, tools=TOOLS, max_steps=3,
    )
    actual_actions = [s.get("action", {}).get("name")
                      for s in result.get("trajectory", []) if s.get("action")]
    match = pomdp["optimal"] in actual_actions
    return {"pomdp_id": pomdp["id"], "true_state": pomdp["true_state"],
            "optimal": pomdp["optimal"], "actual": actual_actions, "match": match,
            "steps": result["steps"]}


def main():
    print("=" * 60)
    print("实验 2：POMDP 框架验证（Mock 模式）")
    print("=" * 60)
    print(f"POMDP 场景数: {len(POMDPS)}")
    print(f"假设 H1: 信念状态 ≈ 短期记忆\n")

    results = []
    for pomdp in POMDPS:
        r = run_pomdp(pomdp)
        results.append(r)
        icon = "PASS" if r["match"] else "FAIL"
        print(f"  [{icon}] {pomdp['id']}: 真实状态={pomdp['true_state']}")
        print(f"         最优行动={r['optimal']}, 实际={r['actual']}, 步数={r['steps']}")

    match_count = sum(1 for r in results if r["match"])
    rate = 100.0 * match_count / len(results)
    print(f"\n信念一致率: {rate:.1f}% ({match_count}/{len(results)})")
    print(f"H1 验证: {'通过' if rate >= 80 else '未通过'} (阈值 80%)")

    optimal_list = [r["optimal"] for r in results]
    consistency = 100.0 * sum(r["match"] for r in results) / len(results)
    print(f"行动一致性得分: {consistency:.1f}%")

    output = {"experiment": "exp-02-pomdp-claim", "belief_consistency_rate": rate,
              "action_consistency": consistency, "results": results}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
