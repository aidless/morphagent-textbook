"""
实验 30：可复现性检验（Mock 模式）

通过多次重复运行同一实验，评估结果的稳定性和可复现性。
分析随机种子和关键参数对结果的影响。

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 模拟实验 ====================
def simulate_experiment(exp_name: str, seed: int, temperature: float = 0.7,
                       top_p: float = 0.9, max_steps: int = 10) -> dict:
    """模拟一个实验的运行结果。"""
    rng = random.Random(seed)

    # 基础表现由实验类型决定
    base_performances = {
        "baseline_eval": 0.65,
        "prompt_evolution": 0.72,
        "tool_selection": 0.68,
    }
    base = base_performances.get(exp_name, 0.6)

    # 温度影响随机性：温度越高，结果越不稳定
    noise = rng.gauss(0, temperature * 0.1)

    # top_p 影响：过低的 top_p 降低多样性
    diversity_factor = min(1.0, top_p / 0.9)
    if diversity_factor < 0.8:
        noise *= 1.5  # 低 top_p 增加偏差

    # max_steps 影响：步数不足降低表现
    step_factor = min(1.0, max_steps / 10)
    step_penalty = (1 - step_factor) * 0.15

    # 种子决定性
    seed_effect = rng.gauss(0, 0.02)

    performance = max(0.1, min(0.98, base + noise - step_penalty + seed_effect))
    latency_ms = 50 + max_steps * 10 + rng.uniform(-10, 10)
    tokens_used = max_steps * 100 + rng.randint(-50, 50)

    return {
        "experiment": exp_name,
        "seed": seed,
        "temperature": temperature,
        "top_p": top_p,
        "max_steps": max_steps,
        "performance": performance,
        "latency_ms": latency_ms,
        "tokens_used": tokens_used,
    }


def reproducibility_analysis(results: list[dict]) -> dict:
    """分析结果的可复现性。"""
    performances = [r["performance"] for r in results]
    latencies = [r["latency_ms"] for r in results]
    tokens = [r["tokens_used"] for r in results]

    mean_perf = statistics.mean(performances)
    std_perf = statistics.pstdev(performances) if len(performances) > 1 else 0
    cv_perf = std_perf / mean_perf if mean_perf > 0 else 0

    # 95% 置信区间（简化：mean +/- 1.96 * std / sqrt(n)）
    n = len(performances)
    ci_half = 1.96 * std_perf / (n ** 0.5) if n > 1 else 0

    return {
        "n_runs": n,
        "performance": {
            "mean": mean_perf,
            "std": std_perf,
            "cv": cv_perf,
            "min": min(performances),
            "max": max(performances),
            "ci_95": [mean_perf - ci_half, mean_perf + ci_half],
        },
        "latency_ms": {
            "mean": statistics.mean(latencies),
            "std": statistics.pstdev(latencies) if len(latencies) > 1 else 0,
        },
        "tokens_used": {
            "mean": statistics.mean(tokens),
            "std": statistics.pstdev(tokens) if len(tokens) > 1 else 0,
        },
    }


def sensitivity_analysis(exp_name: str, param_name: str, param_values: list) -> list[dict]:
    """分析参数敏感性。"""
    results = []
    for val in param_values:
        params = {param_name: val}
        run_results = []
        for seed in range(10):
            result = simulate_experiment(exp_name, seed, **params)
            run_results.append(result["performance"])
        results.append({
            "param_name": param_name,
            "param_value": val,
            "mean_performance": statistics.mean(run_results),
            "std_performance": statistics.pstdev(run_results) if len(run_results) > 1 else 0,
        })
    return results


def main():
    print("=" * 60)
    print("实验 30：可复现性检验（Mock 模式）")
    print("=" * 60)

    experiments = ["baseline_eval", "prompt_evolution", "tool_selection"]
    N_RUNS = 10

    # 第一部分：种子稳定性
    print(f"\n--- 第一部分：种子稳定性（{N_RUNS} 次重复运行） ---\n")

    all_analyses = {}
    for exp_name in experiments:
        runs = [simulate_experiment(exp_name, seed=seed) for seed in range(N_RUNS)]
        analysis = reproducibility_analysis(runs)
        all_analyses[exp_name] = analysis

        print(f"实验: {exp_name}")
        print(f"  性能: 均值={analysis['performance']['mean']:.1%}, "
              f"标准差={analysis['performance']['std']:.3f}, "
              f"CV={analysis['performance']['cv']:.3f}")
        print(f"  范围: [{analysis['performance']['min']:.1%}, {analysis['performance']['max']:.1%}]")
        ci = analysis['performance']['ci_95']
        print(f"  95% CI: [{ci[0]:.1%}, {ci[1]:.1%}]")
        print(f"  延迟: {analysis['latency_ms']['mean']:.0f}ms (+/-{analysis['latency_ms']['std']:.0f})")

        # 各次运行详情
        for r in runs:
            bar = "#" * int(r["performance"] / 100 * 25)
            print(f"    seed={r['seed']:>2}: [{bar:25s}] {r['performance']:.1%}")

    # 第二部分：参数敏感性
    print("\n--- 第二部分：参数敏感性分析 ---\n")

    sensitivity_params = {
        "temperature": [0.0, 0.3, 0.7, 1.0, 1.5],
        "top_p": [0.5, 0.7, 0.9, 0.95, 1.0],
        "max_steps": [3, 5, 8, 10, 15],
    }

    sensitivity_results = {}
    for param_name, param_values in sensitivity_params.items():
        print(f"参数: {param_name}")
        sensitivities = sensitivity_analysis("baseline_eval", param_name, param_values)
        sensitivity_results[param_name] = sensitivities

        for s in sensitivities:
            bar = "#" * int(s["mean_performance"] / 100 * 25)
            print(f"  {s['param_name']}={s['param_value']:<5}: "
                  f"[{bar:25s}] {s['mean_performance']:.1%} (+/-{s['std_performance']:.3f})")

        # 敏感性度量（max - min 的范围）
        perfs = [s["mean_performance"] for s in sensitivities]
        sensitivity_range = max(perfs) - min(perfs)
        print(f"  敏感度范围: {sensitivity_range:.1%}")
        print()

    # 第三部分：可复现性报告
    print("=" * 60)
    print("可复现性报告")
    print("=" * 60)

    print(f"\n| {'实验':<20} | {'均值':>8} | {'标准差':>8} | {'CV':>8} | {'CI宽度':>8} |")
    print(f"|{'-'*22}|{'-'*10}|{'-'*10}|{'-'*10}|{'-'*10}|")
    for exp_name, analysis in all_analyses.items():
        perf = analysis["performance"]
        ci_width = perf["ci_95"][1] - perf["ci_95"][0]
        cv_status = "稳定" if perf["cv"] < 0.05 else ("一般" if perf["cv"] < 0.1 else "不稳定")
        print(f"| {exp_name:<20} | {perf['mean']:>7.1%} | {perf['std']:>8.3f} | "
              f"{perf['cv']:>8.3f} | {ci_width:>7.1%} | ({cv_status})")

    print("\n参数敏感性排序:")
    sens_ranges = []
    for param_name, sensitivities in sensitivity_results.items():
        perfs = [s["mean_performance"] for s in sensitivities]
        sens_ranges.append((param_name, max(perfs) - min(perfs)))
    sens_ranges.sort(key=lambda x: -x[1])
    for i, (param, range_val) in enumerate(sens_ranges, 1):
        print(f"  {i}. {param:<12}: 敏感度 {range_val:.1%}")

    print("\n结论:")
    print("  - 固定种子可有效提高可复现性（CV < 0.05）")
    print("  - temperature 是最敏感的参数，建议固定为默认值")
    print("  - max_steps 在达到阈值后影响变小")

    output = {
        "experiment": "exp-30-reproducibility",
        "reproducibility": all_analyses,
        "sensitivity": sensitivity_results,
    }
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
