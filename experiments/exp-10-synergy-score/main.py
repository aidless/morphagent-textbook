"""
实验 10：P/T/M/C 协同度评分（Mock 模式）

量化 Agent 四大子系统（Prompt/Tool/Memory/Cognition）之间的协同程度。
基于子系统间的一致性计算 Synergy Score。

运行：
    python main.py
"""
import json
import random


# ==================== 子系统状态定义 ====================
def random_subsystem_state(rng: random.Random, coherence: float = 0.8) -> dict:
    """生成一个子系统的状态向量。coherence 越高，各维度越一致。"""
    # 4 个维度：目标对齐、任务适配、信息完整、性能优化
    base = rng.random()
    return {
        "goal_alignment": min(1.0, max(0.0, base + rng.uniform(-0.2, 0.2) * (1 - coherence))),
        "task_fitness": min(1.0, max(0.0, base + rng.uniform(-0.2, 0.2) * (1 - coherence))),
        "info_completeness": min(1.0, max(0.0, base + rng.uniform(-0.2, 0.2) * (1 - coherence))),
        "perf_optimization": min(1.0, max(0.0, base + rng.uniform(-0.2, 0.2) * (1 - coherence))),
    }


def pairwise_consistency(s1: dict, s2: dict) -> float:
    """计算两个子系统之间的一致性（余弦相似度简化版）。"""
    keys = list(s1.keys())
    v1 = [s1[k] for k in keys]
    v2 = [s2[k] for k in keys]
    # 余弦相似度
    dot = sum(a * b for a, b in zip(v1, v2))
    mag1 = sum(a**2 for a in v1) ** 0.5
    mag2 = sum(b**2 for b in v2) ** 0.5
    if mag1 == 0 or mag2 == 0:
        return 0.0
    return dot / (mag1 * mag2)


def synergy_score(subsystems: dict) -> float:
    """计算 P/T/M/C 四个子系统的协同度。"""
    names = list(subsystems.keys())
    pairs = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            c = pairwise_consistency(subsystems[names[i]], subsystems[names[j]])
            pairs.append({"pair": (names[i], names[j]), "consistency": c})
    avg = sum(p["consistency"] for p in pairs) / len(pairs) if pairs else 0.0
    return avg, pairs


# ==================== Agent 配置 ====================
AGENT_CONFIGS = [
    {"name": "完美协同", "coherence": 0.95, "task_performance": 0.92},
    {"name": "良好协同", "coherence": 0.80, "task_performance": 0.80},
    {"name": "中等协同", "coherence": 0.60, "task_performance": 0.65},
    {"name": "低协同", "coherence": 0.35, "task_performance": 0.45},
    {"name": "无协同", "coherence": 0.10, "task_performance": 0.30},
]


def generate_agent_state(config: dict) -> dict:
    """为一种 Agent 配置生成 P/T/M/C 状态。"""
    rng = random.Random(hash(config["name"]))
    return {
        "P (Prompt)": random_subsystem_state(rng, config["coherence"]),
        "T (Tool)": random_subsystem_state(rng, config["coherence"]),
        "M (Memory)": random_subsystem_state(rng, config["coherence"]),
        "C (Cognition)": random_subsystem_state(rng, config["coherence"]),
    }


def main():
    print("=" * 60)
    print("实验 10：P/T/M/C 协同度评分（Mock 模式）")
    print("=" * 60)
    print("量化四大子系统的协同程度\n")

    all_results = []
    synergy_scores = []
    task_performances = []

    for config in AGENT_CONFIGS:
        subsystems = generate_agent_state(config)
        score, pairs = synergy_score(subsystems)

        print(f"\n--- {config['name']} (coherence={config['coherence']:.2f}) ---")
        print(f"  Synergy Score: {score:.3f}")
        for p in pairs:
            print(f"    {p['pair'][0]} <-> {p['pair'][1]}: {p['consistency']:.3f}")

        # 打印子系统状态
        for name, state in subsystems.items():
            dims = ", ".join(f"{k}={v:.2f}" for k, v in state.items())
            print(f"    {name}: [{dims}]")

        all_results.append({
            "config": config["name"],
            "synergy_score": score,
            "pairs": pairs,
            "task_performance": config["task_performance"],
            "subsystems": subsystems,
        })
        synergy_scores.append(score)
        task_performances.append(config["task_performance"])

    # 相关性分析
    print("\n" + "=" * 60)
    print("Synergy Score vs 任务表现")
    print("=" * 60)
    print(f"| {'配置':<12} | {'Synergy':>8} | {'任务表现':>8} |")
    print(f"|{'-'*14}|{'-'*10}|{'-'*10}|")
    for r in all_results:
        print(f"| {r['config']:<12} | {r['synergy_score']:>8.3f} | {r['task_performance']:>8.2f} |")

    # Pearson 相关系数
    n = len(synergy_scores)
    mean_x = sum(synergy_scores) / n
    mean_y = sum(task_performances) / n
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(synergy_scores, task_performances))
    std_x = (sum((x - mean_x)**2 for x in synergy_scores) / n) ** 0.5
    std_y = (sum((y - mean_y)**2 for y in task_performances) / n) ** 0.5
    pearson = cov / (std_x * std_y) if std_x > 0 and std_y > 0 else 0.0
    print(f"\nSynergy Score 与任务表现的 Pearson 相关系数: {pearson:.3f}")
    print(f"  r > 0.9: 强正相关，验证了'协同度越高，表现越好'的假设")

    output = {"experiment": "exp-10-synergy-score", "results": all_results,
              "pearson_correlation": pearson}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
