"""
实验 19：MorphAgent 5 子系统集成（Mock 模式）

模拟 MorphAgent 五个子系统（感知/决策/执行/记忆/学习）的集成。
对比不同集成拓扑的通信开销和协同效率。

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 子系统定义 ====================
SUBSYSTEM_NAMES = ["Perception", "Decision", "Execution", "Memory", "Learning"]

SUBSYSTEM_ROLES = {
    "Perception": "接收输入，解析任务意图",
    "Decision": "制定执行计划和策略",
    "Execution": "调用工具执行操作",
    "Memory": "存储和检索上下文信息",
    "Learning": "从结果中学习并优化策略",
}

# 子系统处理延迟（毫秒模拟）
SUBSYSTEM_LATENCY = {
    "Perception": 10, "Decision": 25, "Execution": 40,
    "Memory": 15, "Learning": 30,
}


# ==================== 拓扑定义 ====================
TOPOLOGIES = {
    "star": {
        "name": "星型拓扑（Decision 为中心）",
        "center": "Decision",
        "edges": [
            ("Decision", "Perception"), ("Decision", "Execution"),
            ("Decision", "Memory"), ("Decision", "Learning"),
        ],
        "comm_cost": 1.0,
    },
    "ring": {
        "name": "环型拓扑",
        "edges": [
            ("Perception", "Decision"), ("Decision", "Execution"),
            ("Execution", "Memory"), ("Memory", "Learning"),
            ("Learning", "Perception"),
        ],
        "comm_cost": 1.2,
    },
    "full": {
        "name": "全连接拓扑",
        "edges": [
            (a, b) for i, a in enumerate(SUBSYSTEM_NAMES)
            for b in SUBSYSTEM_NAMES[i+1:]
        ],
        "comm_cost": 1.8,
    },
}


# ==================== 任务定义 ====================
INTEGRATION_TASKS = [
    {"name": "用户意图解析", "primary": "Perception", "helpers": ["Memory", "Decision"]},
    {"name": "多步任务规划", "primary": "Decision", "helpers": ["Perception", "Memory", "Execution"]},
    {"name": "工具调用链", "primary": "Execution", "helpers": ["Decision", "Memory"]},
    {"name": "上下文保持对话", "primary": "Memory", "helpers": ["Perception", "Decision"]},
    {"name": "策略自适应", "primary": "Learning", "helpers": ["Memory", "Decision", "Execution"]},
    {"name": "端到端问答", "primary": "Decision", "helpers": ["Perception", "Execution", "Memory", "Learning"]},
]


# ==================== 模拟执行 ====================
def count_messages(task: dict, topology: dict) -> int:
    """计算完成一个任务需要的消息传递数。"""
    primary = task["primary"]
    helpers = task["helpers"]
    edges = topology["edges"]
    messages = 0

    # 主子系统需要协调所有辅助子系统
    for helper in helpers:
        direct = (primary, helper) in edges or (helper, primary) in edges
        if direct:
            messages += 1
        else:
            # 需要中转
            messages += 2  # 至少两跳

    # 辅助子系统之间的协调（部分拓扑需要）
    for i, h1 in enumerate(helpers):
        for h2 in helpers[i+1:]:
            direct = (h1, h2) in edges or (h2, h1) in edges
            if direct and random.Random(hash(task["name"] + h1 + h2)).random() < 0.5:
                messages += 1

    return max(1, messages)


def simulate_integration(task: dict, topology: dict) -> dict:
    """模拟任务在给定拓扑下的执行。"""
    messages = count_messages(task, topology)

    # 计算总延迟
    primary_latency = SUBSYSTEM_LATENCY[task["primary"]]
    helper_latency = sum(SUBSYSTEM_LATENCY[h] for h in task["helpers"][:2])
    comm_latency = messages * 5 * topology["comm_cost"]
    total_latency = primary_latency + helper_latency * 0.5 + comm_latency

    # 成功率与消息数负相关（消息越多越容易出错）
    rng = random.Random(42 + hash(task["name"] + topology["name"]))
    base_success = 0.85
    msg_penalty = messages * 0.03
    success = max(0.3, min(0.98, base_success - msg_penalty + rng.uniform(-0.05, 0.05)))

    return {
        "task": task["name"],
        "messages": messages,
        "latency_ms": total_latency,
        "success_rate": success,
    }


def main():
    print("=" * 60)
    print("实验 19：MorphAgent 5 子系统集成（Mock 模式）")
    print("=" * 60)
    print(f"子系统: {SUBSYSTEM_NAMES}")
    print(f"任务数: {len(INTEGRATION_TASKS)}, 拓扑数: {len(TOPOLOGIES)}\n")

    # 子系统信息
    print("子系统角色:")
    for name, role in SUBSYSTEM_ROLES.items():
        print(f"  {name:<14}: {role} (延迟 {SUBSYSTEM_LATENCY[name]}ms)")
    print()

    all_results = {}

    for topo_key, topo in TOPOLOGIES.items():
        print(f"\n--- {topo['name']} ---")
        print(f"  通信系数: {topo['comm_cost']}")
        print(f"  连接数: {len(topo['edges'])}")

        results = []
        for task in INTEGRATION_TASKS:
            result = simulate_integration(task, topo)
            results.append(result)
            print(f"  {result['task']:<16}: 成功率 {result['success_rate']:.1%}, "
                  f"消息 {result['messages']} 次, 延迟 {result['latency_ms']:.0f}ms")

        avg_success = statistics.mean(r["success_rate"] for r in results)
        avg_latency = statistics.mean(r["latency_ms"] for r in results)
        avg_messages = statistics.mean(r["messages"] for r in results)

        print(f"  平均: 成功率 {avg_success:.1%}, 延迟 {avg_latency:.0f}ms, 消息 {avg_messages:.1f}")

        all_results[topo_key] = {
            "results": results,
            "avg_success": avg_success,
            "avg_latency": avg_latency,
            "avg_messages": avg_messages,
        }

    # 汇总对比
    print("\n" + "=" * 60)
    print("拓扑对比")
    print("=" * 60)
    print(f"| {'拓扑':<24} | {'成功率':>8} | {'延迟(ms)':>10} | {'消息数':>8} |")
    print(f"|{'-'*26}|{'-'*10}|{'-'*12}|{'-'*10}|")
    for topo_key, topo in TOPOLOGIES.items():
        data = all_results[topo_key]
        print(f"| {topo['name']:<24} | {data['avg_success']:>7.1%} | "
              f"{data['avg_latency']:>10.0f} | {data['avg_messages']:>8.1f} |")

    # 综合评分（成功率权重高，延迟权重低）
    print("\n综合评分 (0.6*成功率 - 0.2*延迟/100 - 0.2*消息/10):")
    for topo_key, topo in TOPOLOGIES.items():
        data = all_results[topo_key]
        score = (0.6 * data["avg_success"]
                 - 0.2 * data["avg_latency"] / 200
                 - 0.2 * data["avg_messages"] / 10)
        print(f"  {topo['name']}: {score:.3f}")

    output = {"experiment": "exp-19-morphagent-assemble", "results": all_results}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
