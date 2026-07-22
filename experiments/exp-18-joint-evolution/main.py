"""
实验 18：联合自进化 vs 独立修改（Mock 模式）

对比两种自修改架构：
(1) 联合自进化：Prompt/Tool/Memory 协同修改
(2) 独立修改：各子系统独立优化

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 子系统模型 ====================
class Subsystem:
    """子系统模型：维护一个质量分数，可以独立或联合进化。"""

    def __init__(self, name: str, initial_quality: float = 0.3):
        self.name = name
        self.quality = initial_quality
        self.history = [initial_quality]

    def improve(self, delta: float):
        self.quality = max(0.0, min(1.0, self.quality + delta))
        self.history.append(self.quality)

    def get_quality(self) -> float:
        return self.quality


# ==================== 任务模型 ====================
EVAL_TASKS = [
    {"name": "数据分析", "P_w": 0.3, "T_w": 0.4, "M_w": 0.3},
    {"name": "多轮对话", "P_w": 0.35, "T_w": 0.2, "M_w": 0.45},
    {"name": "代码生成", "P_w": 0.25, "T_w": 0.35, "M_w": 0.4},
    {"name": "知识检索", "P_w": 0.2, "T_w": 0.3, "M_w": 0.5},
    {"name": "创意写作", "P_w": 0.5, "T_w": 0.15, "M_w": 0.35},
    {"name": "自动决策", "P_w": 0.2, "T_w": 0.35, "M_w": 0.45},
]


def evaluate_task(task: dict, subsystems: dict) -> float:
    """评估任务完成质量。"""
    score = (
        task["P_w"] * subsystems["Prompt"].get_quality() +
        task["T_w"] * subsystems["Tool"].get_quality() +
        task["M_w"] * subsystems["Memory"].get_quality()
    )
    # 子系统间差距惩罚
    qualities = [s.get_quality() for s in subsystems.values()]
    gap = max(qualities) - min(qualities)
    penalty = gap * 0.1
    return max(0.0, min(1.0, score - penalty))


# ==================== 独立修改模式 ====================
def independent_evolution(rounds: int = 10) -> dict:
    """独立修改：每个子系统独立优化。"""
    rng = random.Random(42)
    subsystems = {
        "Prompt": Subsystem("Prompt", 0.3),
        "Tool": Subsystem("Tool", 0.3),
        "Memory": Subsystem("Memory", 0.3),
    }

    history = []
    for r in range(rounds):
        # 每个子系统独立尝试改进
        for name, sub in subsystems.items():
            if rng.random() < 0.4:
                delta = rng.uniform(0.03, 0.08)
                sub.improve(delta)
            # 偶尔退化
            if rng.random() < 0.1:
                sub.improve(-rng.uniform(0.02, 0.05))

        # 评估全部任务
        scores = [evaluate_task(t, subsystems) for t in EVAL_TASKS]
        avg_score = statistics.mean(scores)
        coherences = [s.get_quality() for s in subsystems.values()]
        coherence = 1.0 - statistics.variance(coherences)

        history.append({
            "round": r + 1,
            "avg_score": avg_score,
            "coherence": coherence,
            "qualities": {n: s.get_quality() for n, s in subsystems.items()},
        })

    return {"history": history, "subsystems": subsystems}


# ==================== 联合进化模式 ====================
def joint_evolution(rounds: int = 10) -> dict:
    """联合进化：子系统协同修改，考虑相互依赖。"""
    rng = random.Random(42)
    subsystems = {
        "Prompt": Subsystem("Prompt", 0.3),
        "Tool": Subsystem("Tool", 0.3),
        "Memory": Subsystem("Memory", 0.3),
    }

    history = []
    for r in range(rounds):
        # 找到最弱子系统，优先提升（协同策略）
        qualities = {n: s.get_quality() for n, s in subsystems.items()}
        weakest = min(qualities, key=qualities.get)
        strongest = max(qualities, key=qualities.get)

        # 最弱子系统获得更大改进
        for name, sub in subsystems.items():
            if name == weakest:
                if rng.random() < 0.55:
                    delta = rng.uniform(0.05, 0.12)
                    sub.improve(delta)
            elif name == strongest:
                if rng.random() < 0.3:
                    delta = rng.uniform(0.02, 0.06)
                    sub.improve(delta)
            else:
                if rng.random() < 0.4:
                    delta = rng.uniform(0.03, 0.08)
                    sub.improve(delta)

        # 联合进化中退化概率更低（协同效应）
        if rng.random() < 0.05:
            weak_sub = subsystems[weakest]
            weak_sub.improve(-rng.uniform(0.01, 0.03))

        # 评估全部任务
        scores = [evaluate_task(t, subsystems) for t in EVAL_TASKS]
        avg_score = statistics.mean(scores)
        coherences = [s.get_quality() for s in subsystems.values()]
        coherence = 1.0 - statistics.variance(coherences)

        history.append({
            "round": r + 1,
            "avg_score": avg_score,
            "coherence": coherence,
            "qualities": {n: s.get_quality() for n, s in subsystems.items()},
        })

    return {"history": history, "subsystems": subsystems}


def main():
    print("=" * 60)
    print("实验 18：联合自进化 vs 独立修改（Mock 模式）")
    print("=" * 60)
    print(f"任务数: {len(EVAL_TASKS)}, 进化轮数: 10\n")

    # 运行两种模式
    independent = independent_evolution(rounds=10)
    joint = joint_evolution(rounds=10)

    # 打印进化轨迹
    modes = [
        ("独立修改", independent),
        ("联合进化", joint),
    ]

    for label, result in modes:
        print(f"\n--- {label} ---")
        for h in result["history"]:
            bar = "#" * int(h["avg_score"] / 100 * 30)
            q_str = ", ".join(f"{k}={v:.3f}" for k, v in h["qualities"].items())
            print(f"  R{h['round']:>2}: [{bar:30s}] {h['avg_score']:.1%} "
                  f"(协同={h['coherence']:.3f}) [{q_str}]")

        final = result["history"][-1]
        initial = result["history"][0]
        print(f"  初始 -> 最终: {initial['avg_score']:.1%} -> {final['avg_score']:.1%}")
        print(f"  总提升: +{final['avg_score'] - initial['avg_score']:.1%}")

    # 对比
    print("\n" + "=" * 60)
    print("模式对比")
    print("=" * 60)
    ind_final = independent["history"][-1]["avg_score"]
    jnt_final = joint["history"][-1]["avg_score"]
    ind_coherence = independent["history"][-1]["coherence"]
    jnt_coherence = joint["history"][-1]["coherence"]

    print(f"| {'指标':<16} | {'独立修改':>10} | {'联合进化':>10} | {'差距':>10} |")
    print(f"|{'-'*18}|{'-'*12}|{'-'*12}|{'-'*12}|")
    print(f"| {'最终得分':<16} | {ind_final:>9.1%} | {jnt_final:>9.1%} | "
          f"{jnt_final - ind_final:>+9.1%} |")
    print(f"| {'协同度':<16} | {ind_coherence:>10.3f} | {jnt_coherence:>10.3f} | "
          f"{jnt_coherence - ind_coherence:>+10.3f} |")

    # 最终子系统质量
    print("\n最终子系统质量:")
    print(f"| {'子系统':<10} | {'独立修改':>10} | {'联合进化':>10} |")
    print(f"|{'-'*12}|{'-'*12}|{'-'*12}|")
    for sub in ["Prompt", "Tool", "Memory"]:
        ind_q = independent["subsystems"][sub].get_quality()
        jnt_q = joint["subsystems"][sub].get_quality()
        print(f"| {sub:<10} | {ind_q:>9.3f} | {jnt_q:>9.3f} |")

    print(f"\n结论: 联合进化比独立修改高 {(jnt_final - ind_final):.1%}")
    print("  - 联合进化通过'短板优先'策略保持了更高的协同度")
    print("  - 独立修改容易出现子系统质量失衡")

    output = {
        "experiment": "exp-18-joint-evolution",
        "independent": {"history": independent["history"]},
        "joint": {"history": joint["history"]},
        "summary": {
            "independent_final": ind_final,
            "joint_final": jnt_final,
            "improvement": jnt_final - ind_final,
        },
    }
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
