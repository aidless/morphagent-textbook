"""
实验 20：MorphBench 迷你版（Mock 模式）

3 个核心任务 x 3 种干预 = 9 个实验点。
测量不同干预对 Agent 表现的影响。

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 基准定义 ====================
BENCH_TASKS = [
    {
        "name": "逻辑推理",
        "description": "多步逻辑推理任务",
        "base_difficulty": 0.6,
        "base_accuracy": 0.45,
    },
    {
        "name": "知识检索",
        "description": "精确事实检索任务",
        "base_difficulty": 0.4,
        "base_accuracy": 0.65,
    },
    {
        "name": "文本生成",
        "description": "结构化文本生成任务",
        "base_difficulty": 0.5,
        "base_accuracy": 0.55,
    },
]

INTERVENTIONS = [
    {"name": "无干预", "code": "none", "boost": 0.0, "description": "基线条件"},
    {"name": "提示增强", "code": "prompt_enhance", "boost": 0.15, "description": "优化 system prompt"},
    {"name": "工具增强", "code": "tool_enhance", "boost": 0.20, "description": "提供外部工具"},
]

TRIALS_PER_CONDITION = 5


def run_trial(task: dict, intervention: dict, trial_id: int) -> dict:
    """运行单次试验。"""
    rng = random.Random(hash(task["name"] + intervention["code"] + str(trial_id)) % (2**31))

    base = task["base_accuracy"] + intervention["boost"]
    # 加随机噪声
    accuracy = max(0.0, min(1.0, base + rng.gauss(0, 0.08)))

    # 质量评分 (1-5)
    quality = max(1, min(5, round(accuracy * 5 + rng.gauss(0, 0.3))))

    # 响应延迟（ms 模拟）
    latency = task["base_difficulty"] * 500 + intervention["boost"] * 200 + rng.uniform(50, 150)

    return {
        "task": task["name"],
        "intervention": intervention["name"],
        "trial": trial_id,
        "accuracy": accuracy,
        "quality": quality,
        "latency_ms": latency,
    }


def cohens_d(group1: list[float], group2: list[float]) -> float:
    """计算 Cohen's d 效应量。"""
    n1, n2 = len(group1), len(group2)
    mean1, mean2 = statistics.mean(group1), statistics.mean(group2)
    var1 = statistics.variance(group1) if n1 > 1 else 0
    var2 = statistics.variance(group2) if n2 > 1 else 0
    pooled_std = ((var1 * (n1 - 1) + var2 * (n2 - 1)) / (n1 + n2 - 2)) ** 0.5 if (n1 + n2) > 2 else 1
    return (mean2 - mean1) / pooled_std if pooled_std > 0 else 0


def main():
    print("=" * 60)
    print("实验 20：MorphBench 迷你版（Mock 模式）")
    print("=" * 60)
    print(f"任务: {len(BENCH_TASKS)}, 干预: {len(INTERVENTIONS)}, "
          f"组合: {len(BENCH_TASKS) * len(INTERVENTIONS)}, 每组: {TRIALS_PER_CONDITION} 次\n")

    # 运行全部实验
    all_trials = []
    results_matrix = {}  # (task, intervention) -> list of accuracies

    for task in BENCH_TASKS:
        for intervention in INTERVENTIONS:
            key = (task["name"], intervention["name"])
            accuracies = []

            for t in range(TRIALS_PER_CONDITION):
                trial = run_trial(task, intervention, t)
                all_trials.append(trial)
                accuracies.append(trial["accuracy"])

            results_matrix[key] = accuracies
            avg_acc = statistics.mean(accuracies)
            avg_quality = statistics.mean(
                run_trial(task, intervention, t)["quality"] for t in range(TRIALS_PER_CONDITION)
            )
            print(f"  {task['name']:<8} x {intervention['name']:<8}: "
                  f"准确率 {avg_acc:.1%}, 质量 {avg_quality:.1f}/5")

    # 按任务分组对比
    print("\n" + "=" * 60)
    print("按任务分组：干预效果分析")
    print("=" * 60)

    baseline_key = "无干预"
    for task in BENCH_TASKS:
        print(f"\n  任务: {task['name']}")
        baseline = results_matrix[(task["name"], baseline_key)]
        for intervention in INTERVENTIONS:
            group = results_matrix[(task["name"], intervention["name"])]
            mean_acc = statistics.mean(group)
            d = cohens_d(baseline, group) if intervention["name"] != baseline_key else 0.0
            delta = mean_acc - statistics.mean(baseline)
            label = f" vs {baseline_key}" if intervention["name"] != baseline_key else ""
            print(f"    {intervention['name']:<10}: {mean_acc:.1%} "
                  f"(d={d:+.2f}, delta={delta:+.1%}){label}")

    # 总体效果
    print("\n" + "=" * 60)
    print("总体干预效果")
    print("=" * 60)
    print(f"| {'干预':<12} | {'平均准确率':>10} | {'vs 基线':>10} |")
    print(f"|{'-'*14}|{'-'*12}|{'-'*12}|")

    for intervention in INTERVENTIONS:
        all_acc = []
        for task in BENCH_TASKS:
            all_acc.extend(results_matrix[(task["name"], intervention["name"])])
        avg = statistics.mean(all_acc)

        if intervention["name"] == baseline_key:
            print(f"| {intervention['name']:<12} | {avg:>9.1%} | {'---':>10} |")
        else:
            baseline_acc = []
            for task in BENCH_TASKS:
                baseline_acc.extend(results_matrix[(task["name"], baseline_key)])
            delta = avg - statistics.mean(baseline_acc)
            d = cohens_d(baseline_acc, all_acc)
            print(f"| {intervention['name']:<12} | {avg:>9.1%} | {delta:>+9.1%} (d={d:.2f}) |")

    print(f"\n共 {len(all_trials)} 次试验完成")

    output = {
        "experiment": "exp-20-morphbench-mini",
        "config": {"tasks": len(BENCH_TASKS), "interventions": len(INTERVENTIONS),
                    "trials_per_condition": TRIALS_PER_CONDITION},
        "results_matrix": {f"{k[0]}|{k[1]}": v for k, v in results_matrix.items()},
    }
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("结果已保存到 results.json")


if __name__ == "__main__":
    main()
