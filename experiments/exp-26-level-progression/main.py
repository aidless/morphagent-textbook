"""
实验 26：L0->L5 能力等级跃迁（Mock 模式）

定义 MorphAgent 的 6 个能力等级（L0~L5），模拟跃迁过程。
验证等级跃迁的必要条件和阈值。

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 能力等级定义 ====================
LEVELS = {
    "L0": {
        "name": "L0 - 基础响应",
        "description": "单轮问答，无工具调用",
        "thresholds": {
            "reasoning": 0.2, "tool_use": 0.0, "memory": 0.0,
            "self_modify": 0.0, "multi_step": 0.0, "autonomy": 0.0,
        },
    },
    "L1": {
        "name": "L1 - 工具辅助",
        "description": "单轮工具调用，基本记忆",
        "thresholds": {
            "reasoning": 0.4, "tool_use": 0.3, "memory": 0.2,
            "self_modify": 0.0, "multi_step": 0.0, "autonomy": 0.0,
        },
    },
    "L2": {
        "name": "L2 - 多步规划",
        "description": "多步任务规划与执行",
        "thresholds": {
            "reasoning": 0.5, "tool_use": 0.5, "memory": 0.4,
            "self_modify": 0.0, "multi_step": 0.3, "autonomy": 0.1,
        },
    },
    "L3": {
        "name": "L3 - 自适应学习",
        "description": "从反馈中学习并调整策略",
        "thresholds": {
            "reasoning": 0.6, "tool_use": 0.6, "memory": 0.5,
            "self_modify": 0.2, "multi_step": 0.5, "autonomy": 0.3,
        },
    },
    "L4": {
        "name": "L4 - 自我改进",
        "description": "主动修改自身 prompt/工具/策略",
        "thresholds": {
            "reasoning": 0.7, "tool_use": 0.7, "memory": 0.6,
            "self_modify": 0.5, "multi_step": 0.6, "autonomy": 0.5,
        },
    },
    "L5": {
        "name": "L5 - 完全自主",
        "description": "完全自主运行，持续自进化",
        "thresholds": {
            "reasoning": 0.85, "tool_use": 0.8, "memory": 0.7,
            "self_modify": 0.7, "multi_step": 0.8, "autonomy": 0.7,
        },
    },
}

DIMENSIONS = ["reasoning", "tool_use", "memory", "self_modify", "multi_step", "autonomy"]
DIM_LABELS = {
    "reasoning": "推理能力", "tool_use": "工具使用", "memory": "记忆管理",
    "self_modify": "自修改能力", "multi_step": "多步规划", "autonomy": "自主性",
}


def simulate_level_performance(level_key: str) -> dict:
    """模拟某个等级的能力表现。"""
    rng = random.Random(42 + hash(level_key))
    level = LEVELS[level_key]
    thresholds = level["thresholds"]

    performance = {}
    for dim in DIMENSIONS:
        base = thresholds[dim]
        # 表现围绕阈值波动
        perf = max(0, min(1, base + rng.gauss(0.05, 0.08)))
        performance[dim] = perf

    # 计算综合得分
    overall = statistics.mean(performance.values())

    return {
        "level": level_key,
        "name": level["name"],
        "description": level["description"],
        "performance": performance,
        "overall": overall,
    }


def check_promotion(current: dict, next_level_key: str) -> dict:
    """检查是否满足升级条件。"""
    next_level = LEVELS[next_level_key]
    thresholds = next_level["thresholds"]
    performance = current["performance"]

    met = {}
    all_met = True
    for dim in DIMENSIONS:
        required = thresholds[dim]
        actual = performance[dim]
        met[dim] = actual >= required
        if not met[dim]:
            all_met = False

    return {
        "can_promote": all_met,
        "met_conditions": met,
        "gaps": {dim: thresholds[dim] - performance[dim]
                 for dim in DIMENSIONS if performance[dim] < thresholds[dim]},
    }


def main():
    print("=" * 60)
    print("实验 26：L0->L5 能力等级跃迁（Mock 模式）")
    print("=" * 60)
    print(f"等级数: {len(LEVELS)}, 能力维度: {len(DIMENSIONS)}\n")

    level_order = ["L0", "L1", "L2", "L3", "L4", "L5"]

    # 模拟各等级表现
    all_performances = {}
    print("各等级能力表现:")
    for lk in level_order:
        perf = simulate_level_performance(lk)
        all_performances[lk] = perf

        print(f"\n  {perf['name']}: {perf['description']}")
        print(f"    综合得分: {perf['overall']:.1%}")
        for dim in DIMENSIONS:
            bar = "#" * int(perf["performance"][dim] / 100 * 20)
            threshold = LEVELS[lk]["thresholds"][dim]
            print(f"    {DIM_LABELS[dim]:<10}: [{bar:20s}] {perf['performance'][dim]:.1%} "
                  f"(阈值 {threshold:.0%})")

    # 跃迁路径分析
    print("\n" + "=" * 60)
    print("等级跃迁路径分析")
    print("=" * 60)

    progression = []
    current_level = "L0"
    for i in range(5):
        next_level = level_order[i + 1]
        current_perf = all_performances[current_level]
        check = check_promotion(current_perf, next_level)

        # 模拟训练提升
        rng = random.Random(42 + i)
        improvement_needed = not check["can_promote"]

        status = "直接跃迁" if check["can_promote"] else "需要训练"
        print(f"\n  {current_level} -> {next_level}: {status}")

        if check["gaps"]:
            print(f"    能力差距:")
            for dim, gap in check["gaps"].items():
                print(f"      {DIM_LABELS[dim]}: 差 {gap:.1%}")

        if improvement_needed:
            # 训练后提升
            trained_perf = dict(current_perf["performance"])
            for dim, gap in check["gaps"].items():
                trained_perf[dim] = min(1.0, trained_perf[dim] + gap + rng.uniform(0.05, 0.1))
            trained_overall = statistics.mean(trained_perf.values())
            print(f"    训练后综合得分: {trained_overall:.1%}")

        progression.append({
            "from": current_level, "to": next_level,
            "direct": check["can_promote"],
            "gaps": check["gaps"],
        })
        current_level = next_level

    # 等级跃迁汇总表
    print("\n" + "=" * 60)
    print("等级能力矩阵")
    print("=" * 60)
    header = f"| {'等级':<20} | " + " | ".join(f"{DIM_LABELS[d]:>8}" for d in DIMENSIONS) + " | 综合 |"
    print(header)
    sep = f"|{'-'*22}|" + "|".join(f"{'-'*10}" for _ in DIMENSIONS) + "|{'-'*8}|"
    print(sep)
    for lk in level_order:
        perf = all_performances[lk]
        row = f"| {perf['name']:<20} |"
        for dim in DIMENSIONS:
            row += f" {perf['performance'][dim]:>7.1%} |"
        row += f" {perf['overall']:>5.1%} |"
        print(row)

    output = {"experiment": "exp-26-level-progression", "performances": all_performances,
              "progression": progression}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
