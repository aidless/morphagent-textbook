"""
实验 17：元控制器评估（Mock 模式）

实现元控制器（Meta-Controller），统一调度 P/T/M/C 四个子系统。
对比有无元控制器的任务完成效率和资源消耗。

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 子系统定义 ====================
SUBSYSTEMS = ["Prompt", "Tool", "Memory", "Cognition"]

# 每个子系统的能力系数（0~1）
SUBSYSTEM_CAPABILITIES = {
    "Prompt":    {"generation": 0.9, "formatting": 0.85, "adaptation": 0.7},
    "Tool":      {"execution": 0.9, "api_call": 0.85, "data_access": 0.8},
    "Memory":    {"recall": 0.8, "store": 0.9, "context": 0.75},
    "Cognition": {"reasoning": 0.9, "planning": 0.85, "decision": 0.8},
}

# 复合任务 -> 需要的子系统及权重
TASKS = [
    {"name": "数据分析报告", "requires": {"Tool": 0.4, "Cognition": 0.3, "Memory": 0.2, "Prompt": 0.1}},
    {"name": "多轮对话客服", "requires": {"Memory": 0.3, "Prompt": 0.3, "Cognition": 0.2, "Tool": 0.2}},
    {"name": "代码生成调试", "requires": {"Cognition": 0.35, "Tool": 0.3, "Prompt": 0.25, "Memory": 0.1}},
    {"name": "知识问答检索", "requires": {"Memory": 0.4, "Tool": 0.25, "Prompt": 0.2, "Cognition": 0.15}},
    {"name": "创意写作辅助", "requires": {"Prompt": 0.45, "Cognition": 0.25, "Memory": 0.2, "Tool": 0.1}},
    {"name": "自动化工作流", "requires": {"Tool": 0.35, "Prompt": 0.25, "Cognition": 0.25, "Memory": 0.15}},
    {"name": "多步推理任务", "requires": {"Cognition": 0.4, "Memory": 0.3, "Prompt": 0.15, "Tool": 0.15}},
    {"name": "实时监控决策", "requires": {"Tool": 0.3, "Cognition": 0.3, "Memory": 0.25, "Prompt": 0.15}},
]


# ==================== 调度策略 ====================
class BaseScheduler:
    """基线调度器（无元控制器，固定调用顺序）。"""
    name = "固定顺序"

    def schedule(self, task: dict) -> dict:
        calls = {s: 1 for s in SUBSYSTEMS}  # 每个子系统固定调用 1 次
        return calls


class MetaController:
    """元控制器（自适应调度）。"""
    name = "元控制器"

    def schedule(self, task: dict) -> dict:
        requires = task["requires"]
        # 按需求权重分配调用次数，重要子系统多调用
        calls = {}
        for s in SUBSYSTEMS:
            weight = requires.get(s, 0.1)
            calls[s] = max(1, round(weight * 10))
        return calls


class RLController:
    """模拟强化学习控制器（从历史中学习最优调度）。"""
    name = "RL 控制器"

    def __init__(self):
        self.q_table: dict[str, dict[str, int]] = {}

    def schedule(self, task: dict) -> dict:
        task_name = task["name"]
        if task_name in self.q_table:
            return dict(self.q_table[task_name])
        # 首次：探索性调度
        requires = task["requires"]
        calls = {}
        for s in SUBSYSTEMS:
            weight = requires.get(s, 0.1)
            calls[s] = max(1, round(weight * 8 + random.Random(hash(task_name + s)).uniform(-1, 1)))
        self.q_table[task_name] = calls
        return calls

    def update(self, task_name: str, calls: dict, reward: float):
        """根据反馈更新 Q 表。"""
        if reward > 0.7:
            self.q_table[task_name] = calls  # 保留好的调度


def simulate_task(task: dict, scheduler, rng: random.Random) -> dict:
    """模拟任务执行。"""
    calls = scheduler.schedule(task)

    # 计算子系统贡献
    total_contribution = 0.0
    total_calls = sum(calls.values())

    for sub_name, call_count in calls.items():
        requires_w = task["requires"].get(sub_name, 0.1)
        capabilities = SUBSYSTEM_CAPABILITIES.get(sub_name, {})
        avg_cap = statistics.mean(capabilities.values()) if capabilities else 0.5
        contribution = requires_w * avg_cap * (call_count / total_calls)
        total_contribution += contribution

    # 加随机性
    success = total_contribution + rng.uniform(-0.1, 0.1)
    success_rate = max(0.0, min(1.0, success))

    return {
        "task": task["name"],
        "success_rate": success_rate,
        "calls": calls,
        "total_calls": total_calls,
    }


def run_experiment(scheduler, label: str) -> list[dict]:
    """用指定调度器运行全部任务。"""
    rng = random.Random(42)
    results = []
    for task in TASKS:
        result = simulate_task(task, scheduler, rng)
        result["scheduler"] = label
        results.append(result)

        # RL 控制器需要更新
        if isinstance(scheduler, RLController) and result["success_rate"] > 0.7:
            scheduler.update(task["name"], result["calls"], result["success_rate"])

    return results


def main():
    print("=" * 60)
    print("实验 17：元控制器评估（Mock 模式）")
    print("=" * 60)
    print(f"任务数: {len(TASKS)}, 子系统: {SUBSYSTEMS}\n")

    schedulers = [
        (BaseScheduler(), "固定顺序"),
        (MetaController(), "元控制器"),
        (RLController(), "RL 控制器"),
    ]

    all_results = {}
    for scheduler, label in schedulers:
        results = run_experiment(scheduler, label)
        avg_success = statistics.mean(r["success_rate"] for r in results)
        avg_calls = statistics.mean(r["total_calls"] for r in results)

        print(f"\n--- {label} ---")
        for r in results:
            print(f"  {r['task']:<12}: 成功率 {r['success_rate']:.1%}, 调用 {r['total_calls']} 次")
            print(f"    调度: {', '.join(f'{k}={v}' for k, v in r['calls'].items())}")
        print(f"  平均成功率: {avg_success:.1%}, 平均调用: {avg_calls:.1f} 次")

        # 调度均衡度
        all_sub_calls = {s: [] for s in SUBSYSTEMS}
        for r in results:
            for s in SUBSYSTEMS:
                all_sub_calls[s].append(r["calls"].get(s, 0))
        balance = {}
        for s in SUBSYSTEMS:
            balance[s] = statistics.mean(all_sub_calls[s])
        variance = statistics.variance(list(balance.values())) if len(balance) > 1 else 0
        print(f"  子系统利用率: {balance}")
        print(f"  利用率方差: {variance:.2f}")

        all_results[label] = {
            "results": results,
            "avg_success": avg_success,
            "avg_calls": avg_calls,
            "variance": variance,
            "balance": balance,
        }

    # 汇总对比
    print("\n" + "=" * 60)
    print("调度策略汇总")
    print("=" * 60)
    print(f"| {'策略':<12} | {'平均成功率':>10} | {'平均调用':>8} | {'均衡度':>8} |")
    print(f"|{'-'*14}|{'-'*12}|{'-'*10}|{'-'*10}|")
    for label, data in all_results.items():
        print(f"| {label:<12} | {data['avg_success']:>9.1%} | {data['avg_calls']:>8.1f} | "
              f"{data['variance']:>8.2f} |")

    baseline = all_results["固定顺序"]["avg_success"]
    meta = all_results["元控制器"]["avg_success"]
    rl = all_results["RL 控制器"]["avg_success"]
    print(f"\n元控制器 vs 固定顺序: +{(meta - baseline):.1%}")
    print(f"RL 控制器 vs 固定顺序: +{(rl - baseline):.1%}")

    output = {"experiment": "exp-17-meta-controller", "results": all_results}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
