"""
实验 11：形态可塑性测量（Mock 模式）

测量 B（Agent 形态）修改后任务表现的变化幅度。
分别修改 P/T/M/C 四个子系统，计算 Morphological Plasticity Index (MPI)。

运行：
    python main.py
"""
import json
import random


# ==================== 基线 Agent ====================
BASELINE_CONFIG = {
    "P": {"prompt_quality": 0.7, "instruction_clarity": 0.7},
    "T": {"tool_count": 5, "description_quality": 0.7},
    "M": {"memory_size": 10, "recall_accuracy": 0.7},
    "C": {"reasoning_depth": 3, "adaptability": 0.7},
}

# 干预：修改各子系统
INTERVENTIONS = {
    "P_升级": {"P": {"prompt_quality": 0.95, "instruction_clarity": 0.95}},
    "T_升级": {"T": {"tool_count": 10, "description_quality": 0.95}},
    "M_升级": {"M": {"memory_size": 50, "recall_accuracy": 0.95}},
    "C_升级": {"C": {"reasoning_depth": 5, "adaptability": 0.95}},
    "P_降级": {"P": {"prompt_quality": 0.3, "instruction_clarity": 0.3}},
    "T_降级": {"T": {"tool_count": 2, "description_quality": 0.3}},
    "M_降级": {"M": {"memory_size": 3, "recall_accuracy": 0.3}},
    "C_降级": {"C": {"reasoning_depth": 1, "adaptability": 0.3}},
}

# 任务类型及其对各子系统的敏感度
TASK_TYPES = [
    {"name": "推理任务", "sensitivity": {"P": 0.8, "T": 0.2, "M": 0.3, "C": 0.7}},
    {"name": "工具使用", "sensitivity": {"P": 0.3, "T": 0.9, "M": 0.2, "C": 0.4}},
    {"name": "长对话", "sensitivity": {"P": 0.4, "T": 0.2, "M": 0.9, "C": 0.3}},
    {"name": "复杂决策", "sensitivity": {"P": 0.5, "T": 0.3, "M": 0.4, "C": 0.8}},
    {"name": "知识问答", "sensitivity": {"P": 0.6, "T": 0.5, "M": 0.6, "C": 0.3}},
]


def compute_performance(config: dict, task: dict, rng: random.Random) -> float:
    """根据 Agent 配置和任务敏感度计算任务表现。"""
    base_perf = 0.50
    delta = 0.0
    for subsystem in ["P", "T", "M", "C"]:
        if subsystem in config:
            sub = config[subsystem]
            # 用 quality 相关的浮点属性
            sub_values = [v for v in sub.values() if isinstance(v, float) and 0 <= v <= 1]
            if not sub_values:
                sub_values = [0.5]
            sub_quality = sum(sub_values) / len(sub_values)
            # 敏感度加权
            sensitivity = task["sensitivity"].get(subsystem, 0.5)
            delta += (sub_quality - 0.5) * sensitivity * 0.3
    perf = base_perf + delta + rng.uniform(-0.03, 0.03)
    return max(0.0, min(1.0, perf))


def mpi(intervention_name: str, config: dict, baseline_config: dict,
        tasks: list, rng_seed: int = 42) -> dict:
    """计算形态可塑性指数。"""
    rng = random.Random(rng_seed)
    baseline_perfs = []
    modified_perfs = []
    task_results = []

    for task in tasks:
        bp = compute_performance(baseline_config, task, random.Random(rng_seed + hash(task["name"])))
        mp = compute_performance(config, task, random.Random(rng_seed + hash(task["name"]) + 100))
        baseline_perfs.append(bp)
        modified_perfs.append(mp)
        task_results.append({
            "task": task["name"], "baseline": bp, "modified": mp,
            "delta": mp - bp, "abs_delta": abs(mp - bp),
        })

    avg_baseline = sum(baseline_perfs) / len(baseline_perfs)
    avg_modified = sum(modified_perfs) / len(modified_perfs)
    mpi_val = abs(avg_modified - avg_baseline) / max(avg_baseline, 0.01)

    return {"intervention": intervention_name, "mpi": mpi_val,
            "avg_baseline": avg_baseline, "avg_modified": avg_modified,
            "task_results": task_results}


def main():
    print("=" * 60)
    print("实验 11：形态可塑性测量（Mock 模式）")
    print("=" * 60)
    print("测量 B 修改后的任务表现变化幅度\n")

    all_results = []

    # 先跑基线
    rng = random.Random(42)
    baseline_tasks = []
    for task in TASK_TYPES:
        bp = compute_performance(BASELINE_CONFIG, task, random.Random(42 + hash(task["name"])))
        baseline_tasks.append({"task": task["name"], "performance": bp})

    print("--- 基线表现 ---")
    for bt in baseline_tasks:
        print(f"  {bt['task']}: {bt['performance']:.3f}")

    # 跑每种干预
    for intv_name, intv_config in INTERVENTIONS.items():
        merged = {**BASELINE_CONFIG, **intv_config}
        result = mpi(intv_name, merged, BASELINE_CONFIG, TASK_TYPES)
        all_results.append(result)
        direction = "UP" if result["avg_modified"] > result["avg_baseline"] else "DOWN"
        print(f"\n--- {intv_name} (MPI={result['mpi']:.3f}, {direction}) ---")
        for tr in result["task_results"]:
            sign = "+" if tr["delta"] >= 0 else ""
            print(f"  {tr['task']}: {tr['baseline']:.3f} -> {tr['modified']:.3f} ({sign}{tr['delta']:.3f})")

    # 汇总
    print("\n" + "=" * 60)
    print("形态可塑性指数汇总")
    print("=" * 60)
    print(f"| {'干预':<10} | {'MPI':>6} | {'基线':>6} | {'修改后':>6} | {'方向':>4} |")
    print(f"|{'-'*12}|{'-'*8}|{'-'*8}|{'-'*8}|{'-'*6}|")
    for r in all_results:
        d = "UP" if r["avg_modified"] > r["avg_baseline"] else "DOWN"
        print(f"| {r['intervention']:<10} | {r['mpi']:>6.3f} | {r['avg_baseline']:>6.3f} | "
              f"{r['avg_modified']:>6.3f} | {d:>4} |")

    avg_mpi = sum(r["mpi"] for r in all_results) / len(all_results)
    print(f"\n平均 MPI: {avg_mpi:.3f}")
    print(f"验证: MPI > 0 即证明形态修改会影响表现（形态可塑性存在）")

    output = {"experiment": "exp-11-morphological-plasticity", "results": all_results,
              "avg_mpi": avg_mpi}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
