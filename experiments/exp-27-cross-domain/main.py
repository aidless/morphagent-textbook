"""
实验 27：跨领域迁移实验（Mock 模式）

评估 Agent 从源领域到目标领域的知识迁移能力。
测量迁移效率与领域距离的关系。

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 领域定义 ====================
DOMAINS = {
    "code_review": {"name": "代码审查", "features": {"logic": 0.9, "language": 0.7, "security": 0.6, "creativity": 0.2}},
    "math": {"name": "数学推理", "features": {"logic": 0.95, "language": 0.3, "security": 0.1, "creativity": 0.4}},
    "creative": {"name": "创意写作", "features": {"logic": 0.3, "language": 0.9, "security": 0.1, "creativity": 0.95}},
    "data_analysis": {"name": "数据分析", "features": {"logic": 0.8, "language": 0.5, "security": 0.3, "creativity": 0.2}},
    "customer_service": {"name": "客户服务", "features": {"logic": 0.4, "language": 0.8, "security": 0.5, "creativity": 0.5}},
    "legal": {"name": "法律文书", "features": {"logic": 0.7, "language": 0.85, "security": 0.7, "creativity": 0.3}},
    "medical": {"name": "医疗咨询", "features": {"logic": 0.8, "language": 0.6, "security": 0.8, "creativity": 0.2}},
    "education": {"name": "教育辅导", "features": {"logic": 0.6, "language": 0.7, "security": 0.2, "creativity": 0.6}},
}

SOURCE_DOMAINS = ["code_review", "math", "creative"]
TARGET_DOMAINS = ["data_analysis", "customer_service", "legal", "medical", "education"]


def domain_distance(d1: str, d2: str) -> float:
    """计算两个领域间的欧氏距离。"""
    f1 = DOMAINS[d1]["features"]
    f2 = DOMAINS[d2]["features"]
    dims = list(f1.keys())
    dist = sum((f1[d] - f2[d]) ** 2 for d in dims) ** 0.5
    return dist


def simulate_transfer(source: str, target: str, method: str) -> dict:
    """模拟领域迁移。"""
    rng = random.Random(42 + hash(source + target + method))
    dist = domain_distance(source, target)

    # 从头训练的表现（基线）
    scratch_performance = 0.5 + rng.uniform(-0.05, 0.05)

    if method == "direct":
        # 直接迁移：距离越远，表现越差
        transfer_loss = dist * 0.3
        performance = scratch_performance + 0.15 - transfer_loss + rng.uniform(-0.05, 0.05)
    elif method == "finetune":
        # 微调迁移：距离影响较小
        transfer_loss = dist * 0.1
        performance = scratch_performance + 0.25 - transfer_loss + rng.uniform(-0.03, 0.03)
    else:  # scratch
        performance = scratch_performance

    performance = max(0.1, min(0.95, performance))
    training_cost = {"direct": 0.1, "finetune": 0.4, "scratch": 1.0}[method]

    return {
        "source": source, "target": target,
        "method": method,
        "domain_distance": dist,
        "performance": performance,
        "training_cost": training_cost,
    }


def main():
    print("=" * 60)
    print("实验 27：跨领域迁移实验（Mock 模式）")
    print("=" * 60)
    print(f"源领域: {len(SOURCE_DOMAINS)}, 目标领域: {len(TARGET_DOMAINS)}\n")

    # 领域距离矩阵
    print("领域距离矩阵:")
    all_domains = list(DOMAINS.keys())
    header = f"  {'':>14}" + "".join(f" {d[:6]:>8}" for d in all_domains)
    print(header)
    for d1 in all_domains:
        row = f"  {d1[:12]:>14}"
        for d2 in all_domains:
            dist = domain_distance(d1, d2)
            row += f" {dist:>8.2f}"
        print(row)

    # 迁移实验
    methods = [
        ("direct", "直接迁移"),
        ("finetune", "微调迁移"),
        ("scratch", "从头训练"),
    ]

    all_results = {}
    print("\n" + "=" * 50)
    print("迁移实验结果")
    print("=" * 50)

    for source in SOURCE_DOMAINS:
        all_results[source] = {}
        for target in TARGET_DOMAINS:
            dist = domain_distance(source, target)
            print(f"\n  {DOMAINS[source]['name']} -> {DOMAINS[target]['name']} (距离={dist:.2f}):")

            for method_key, method_label in methods:
                result = simulate_transfer(source, target, method_key)
                print(f"    {method_label:<8}: 性能 {result['performance']:.1%}, "
                      f"训练成本 {result['training_cost']:.0%}")
                all_results[source][target] = all_results[source].get(target, {})
                all_results[source][target][method_key] = result

    # 汇总分析
    print("\n" + "=" * 60)
    print("迁移效率汇总（微调迁移 vs 从头训练）")
    print("=" * 60)
    print(f"| {'源->目标':<24} | {'距离':>6} | {'微调':>8} | {'从头':>8} | {'增益':>8} | {'成本节省':>8} |")
    print(f"|{'-'*26}|{'-'*8}|{'-'*10}|{'-'*10}|{'-'*10}|{'-'*10}|")

    total_gain = []
    for source in SOURCE_DOMAINS:
        for target in TARGET_DOMAINS:
            ft = all_results[source][target]["finetune"]
            sc = all_results[source][target]["scratch"]
            gain = ft["performance"] - sc["performance"]
            cost_save = 1.0 - ft["training_cost"]
            src_name = DOMAINS[source]["name"][:6]
            tgt_name = DOMAINS[target]["name"][:6]
            print(f"| {src_name}->{tgt_name:<12} | {ft['domain_distance']:>6.2f} | "
                  f"{ft['performance']:>7.1%} | {sc['performance']:>7.1%} | "
                  f"{gain:>+7.1%} | {cost_save:>7.0%} |")
            total_gain.append((gain, ft["domain_distance"]))

    # 相关性分析
    gains = [g[0] for g in total_gain]
    dists = [g[1] for g in total_gain]
    n = len(gains)
    mean_g = statistics.mean(gains)
    mean_d = statistics.mean(dists)
    cov = sum((g - mean_g) * (d - mean_d) for g, d in total_gain) / n
    std_g = (sum((g - mean_g)**2 for g in gains) / n) ** 0.5
    std_d = (sum((d - mean_d)**2 for d in dists) / n) ** 0.5
    corr = cov / (std_g * std_d) if std_g > 0 and std_d > 0 else 0
    print(f"\n领域距离与迁移增益的相关系数: {corr:.3f}")
    print(f"  负相关: 距离越远，迁移增益越小")

    output = {"experiment": "exp-27-cross-domain", "results": all_results,
              "distance_performance_corr": corr}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
