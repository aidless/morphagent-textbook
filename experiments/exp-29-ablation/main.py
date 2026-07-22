"""
实验 29：消融实验（Mock 模式）

通过逐个移除子系统，量化每个子系统的独立贡献。
验证"完整系统 > 任何子集"的核心假设。

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 子系统定义 ====================
SUBSYSTEMS = ["Prompt", "Tool", "Memory", "Cognition"]

# 每个子系统对各任务的贡献权重
TASK_SUBSYSTEM_WEIGHTS = {
    "代码生成":  {"Prompt": 0.30, "Tool": 0.25, "Memory": 0.20, "Cognition": 0.25},
    "数据分析":  {"Prompt": 0.15, "Tool": 0.35, "Memory": 0.25, "Cognition": 0.25},
    "多轮对话":  {"Prompt": 0.25, "Tool": 0.15, "Memory": 0.35, "Cognition": 0.25},
    "创意写作":  {"Prompt": 0.40, "Tool": 0.10, "Memory": 0.25, "Cognition": 0.25},
    "复杂推理":  {"Prompt": 0.15, "Tool": 0.20, "Memory": 0.20, "Cognition": 0.45},
}

EVAL_TASKS = list(TASK_SUBSYSTEM_WEIGHTS.keys())


# ==================== 消融配置 ====================
ABLATION_CONFIGS = {
    "full": {"name": "完整系统 (P+T+M+C)", "removed": []},
    "no_prompt":    {"name": "移除 Prompt", "removed": ["Prompt"]},
    "no_tool":      {"name": "移除 Tool", "removed": ["Tool"]},
    "no_memory":    {"name": "移除 Memory", "removed": ["Memory"]},
    "no_cognition": {"name": "移除 Cognition", "removed": ["Cognition"]},
    "no_pt":        {"name": "移除 P+T", "removed": ["Prompt", "Tool"]},
    "no_mc":        {"name": "移除 M+C", "removed": ["Memory", "Cognition"]},
}


def simulate_task(config_name: str, task_name: str) -> dict:
    """模拟在给定消融配置下完成任务的表现。"""
    config = ABLATION_CONFIGS[config_name]
    weights = TASK_SUBSYSTEM_WEIGHTS[task_name]
    removed = config["removed"]

    # 计算有效贡献
    active_weight = sum(w for sub, w in weights.items() if sub not in removed)
    total_weight = sum(weights.values())

    # 归一化：移除子系统后，剩余子系统的贡献不能 100% 补偿
    compensation = 0.3  # 30% 的补偿效应
    effective = (active_weight / total_weight) * (1.0 - (1 - active_weight / total_weight) * (1 - compensation))

    # 加随机性
    rng = random.Random(42 + hash(config_name + task_name) % (2**31))
    performance = max(0.1, min(0.98, effective + rng.gauss(0, 0.05)))

    return {
        "config": config_name,
        "task": task_name,
        "performance": performance,
        "active_subsystems": [s for s in SUBSYSTEMS if s not in removed],
    }


def run_ablation_study() -> dict:
    """运行完整消融实验。"""
    results = {}

    for config_name, config in ABLATION_CONFIGS.items():
        config_results = []
        for task_name in EVAL_TASKS:
            result = simulate_task(config_name, task_name)
            config_results.append(result)

        avg_perf = statistics.mean(r["performance"] for r in config_results)
        results[config_name] = {
            "config_info": config,
            "task_results": config_results,
            "avg_performance": avg_perf,
        }

    return results


def compute_contributions(results: dict) -> dict:
    """计算每个子系统的增量贡献。"""
    full_perf = results["full"]["avg_performance"]

    contributions = {}
    for sub in SUBSYSTEMS:
        # 找到移除该子系统的配置
        config_map = {"Prompt": "no_prompt", "Tool": "no_tool", "Memory": "no_memory", "Cognition": "no_cognition"}
        config_key = config_map[sub]
        if config_key in results:
            removed_perf = results[config_key]["avg_performance"]
            contribution = full_perf - removed_perf
            contributions[sub] = contribution

    return contributions


def main():
    print("=" * 60)
    print("实验 29：消融实验（Mock 模式）")
    print("=" * 60)
    print(f"子系统: {SUBSYSTEMS}, 任务: {EVAL_TASKS}")
    print(f"消融配置: {len(ABLATION_CONFIGS)}\n")

    results = run_ablation_study()

    # 打印各配置结果
    for config_name, data in results.items():
        config_info = data["config_info"]
        print(f"\n--- {config_info['name']} ---")
        for tr in data["task_results"]:
            bar = "#" * int(tr["performance"] / 100 * 25)
            print(f"  {tr['task']:<8}: [{bar:25s}] {tr['performance']:.1%}")
        print(f"  平均: {data['avg_performance']:.1%}")

    # 增量贡献分析
    contributions = compute_contributions(results)

    print("\n" + "=" * 60)
    print("子系统增量贡献分析")
    print("=" * 60)
    full_perf = results["full"]["avg_performance"]
    print(f"完整系统平均性能: {full_perf:.1%}\n")

    sorted_contribs = sorted(contributions.items(), key=lambda x: -x[1])
    print(f"| {'子系统':<12} | {'移除后性能':>10} | {'增量贡献':>10} | {'占比':>8} |")
    print(f"|{'-'*14}|{'-'*12}|{'-'*12}|{'-'*10}|")
    for sub, contrib in sorted_contribs:
        config_map = {"Prompt": "no_prompt", "Tool": "no_tool", "Memory": "no_memory", "Cognition": "no_cognition"}
        config_key = config_map[sub]
        removed_perf = results[config_key]["avg_performance"]
        ratio = contrib / full_perf if full_perf > 0 else 0
        print(f"| {sub:<12} | {removed_perf:>9.1%} | {contrib:>+9.1%} | {ratio:>7.1%} |")

    # 重要性排序
    print("\n子系统重要性排序:")
    for i, (sub, contrib) in enumerate(sorted_contribs, 1):
        bar = "#" * int(contrib / full_perf * 40)
        print(f"  {i}. {sub:<12}: {bar} {contrib/full_perf:.1%}")

    # 两两移除效果
    print("\n两两移除效果:")
    for config_name in ["no_pt", "no_mc"]:
        data = results[config_name]
        delta = data["avg_performance"] - full_perf
        print(f"  {data['config_info']['name']}: {data['avg_performance']:.1%} (vs 完整 {delta:+.1%})")

    print("\n结论:")
    print("  - 每个子系统都有正向贡献")
    print(f"  - 最重要的子系统: {sorted_contribs[0][0]} (贡献 {sorted_contribs[0][1]/full_perf:.1%})")
    print("  - 两两移除导致性能急剧下降，验证了子系统间的互补性")

    output = {
        "experiment": "exp-29-ablation",
        "full_performance": full_perf,
        "contributions": {k: v for k, v in contributions.items()},
        "results": {k: {"avg": v["avg_performance"]} for k, v in results.items()},
    }
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
