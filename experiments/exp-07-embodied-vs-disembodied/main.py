"""
实验 7：具身 vs 非具身 Agent 对比（Mock 模式）

验证"具身 Agent 在物理交互任务上优于非具身 Agent"。
5 类任务 x 2 种 Agent = 10 组对比。

运行：
    python main.py
"""
import json
import random


# ==================== 任务定义 ====================
TASKS = [
    # 导航类（具身优势大）
    {"type": "导航", "q": "前方有障碍物，如何绕过？", "answer": "转向",
     "embodied_advantage": 0.50},
    {"type": "导航", "q": "找到从A点到B点的最短路径", "answer": "路径规划",
     "embodied_advantage": 0.40},
    # 物理推理类
    {"type": "物理推理", "q": "如果把杯子推到桌子边缘会怎样？", "answer": "掉落",
     "embodied_advantage": 0.35},
    {"type": "物理推理", "q": "这个箱子太重搬不动，怎么办？", "answer": "用工具/滑轮",
     "embodied_advantage": 0.30},
    # 空间理解类
    {"type": "空间理解", "q": "房间里有3个物体，描述它们的位置关系", "answer": "空间描述",
     "embodied_advantage": 0.35},
    {"type": "空间理解", "q": "判断两个物体之间的距离", "answer": "距离估算",
     "embodied_advantage": 0.30},
    # 工具使用类
    {"type": "工具使用", "q": "用锤子钉钉子需要几步？", "answer": "步骤描述",
     "embodied_advantage": 0.25},
    {"type": "工具使用", "q": "如何安全地切开一个纸箱？", "answer": "使用美工刀",
     "embodied_advantage": 0.20},
    # 纯文本类（非具身可能更好）
    {"type": "纯文本", "q": "总结这篇论文的主要贡献", "answer": "摘要",
     "embodied_advantage": -0.10},
    {"type": "纯文本", "q": "翻译以下英文段落", "answer": "翻译",
     "embodied_advantage": -0.05},
]


def embodied_agent(task: dict) -> dict:
    """具身 Agent：有感知/行动接口，在物理任务上表现更好。"""
    base_rate = 0.75
    bonus = task["embodied_advantage"]
    rate = min(0.95, base_rate + bonus)
    rng = random.Random(hash(task["q"]) + 1000)
    success = rng.random() < rate
    steps = rng.randint(2, 5) if success else rng.randint(3, 8)
    return {"success": success, "steps": steps, "agent": "embodied",
            "has_perception": True, "has_action": True}


def disembodied_agent(task: dict) -> dict:
    """非具身 Agent：纯文本推理，在物理任务上较弱。"""
    base_rate = 0.75
    bonus = 0  # 非具身没有额外的物理能力
    rate = min(0.95, base_rate + bonus)
    rng = random.Random(hash(task["q"]) + 2000)
    success = rng.random() < rate
    steps = rng.randint(3, 7) if success else rng.randint(5, 10)
    return {"success": success, "steps": steps, "agent": "disembodied",
            "has_perception": False, "has_action": False}


def run_comparison():
    """运行全部对比实验。"""
    results = []
    for task in TASKS:
        emb = embodied_agent(task)
        dis = disembodied_agent(task)
        results.append({"task_type": task["type"], "question": task["q"],
                        "embodied": emb, "disembodied": dis})
    return results


def main():
    print("=" * 60)
    print("实验 7：具身 vs 非具身 Agent 对比（Mock 模式）")
    print("=" * 60)
    print(f"任务数: {len(TASKS)}, 任务类型: 5\n")

    results = run_comparison()

    # 按类型汇总
    task_types = sorted(set(r["task_type"] for r in results))
    type_summary = {}
    for tt in task_types:
        type_results = [r for r in results if r["task_type"] == tt]
        emb_rate = 100.0 * sum(r["embodied"]["success"] for r in type_results) / len(type_results)
        dis_rate = 100.0 * sum(r["disembodied"]["success"] for r in type_results) / len(type_results)
        type_summary[tt] = {"embodied": emb_rate, "disembodied": dis_rate,
                            "diff": emb_rate - dis_rate}

    # 打印每个任务
    for r in results:
        emb_status = "PASS" if r["embodied"]["success"] else "FAIL"
        dis_status = "PASS" if r["disembodied"]["success"] else "FAIL"
        print(f"  [{r['task_type']}] {r['question'][:35]}")
        print(f"    具身: {emb_status} ({r['embodied']['steps']}步)")
        print(f"    非具身: {dis_status} ({r['disembodied']['steps']}步)")

    # 汇总表
    print("\n" + "=" * 60)
    print("按任务类型汇总")
    print("=" * 60)
    print(f"| {'任务类型':<10} | {'具身 Agent':>10} | {'非具身 Agent':>12} | {'差异':>6} |")
    print(f"|{'-'*12}|{'-'*12}|{'-'*14}|{'-'*8}|")
    for tt in task_types:
        s = type_summary[tt]
        print(f"| {tt:<10} | {s['embodied']:>9.1f}% | {s['disembodied']:>11.1f}% | {s['diff']:>+5.1f}pp |")

    # 总体
    all_emb = 100.0 * sum(r["embodied"]["success"] for r in results) / len(results)
    all_dis = 100.0 * sum(r["disembodied"]["success"] for r in results) / len(results)
    print(f"\n总体: 具身 {all_emb:.1f}% vs 非具身 {all_dis:.1f}% (差异 {all_emb-all_dis:+.1f}pp)")

    # 物理任务 vs 非物理任务
    physical_types = {"导航", "物理推理", "空间理解", "工具使用"}
    phys_emb = [r["embodied"]["success"] for r in results if r["task_type"] in physical_types]
    phys_dis = [r["disembodied"]["success"] for r in results if r["task_type"] in physical_types]
    text_emb = [r["embodied"]["success"] for r in results if r["task_type"] not in physical_types]
    text_dis = [r["disembodied"]["success"] for r in results if r["task_type"] not in physical_types]
    p_emb_rate = 100.0 * sum(phys_emb) / len(phys_emb) if phys_emb else 0
    p_dis_rate = 100.0 * sum(phys_dis) / len(phys_dis) if phys_dis else 0
    t_emb_rate = 100.0 * sum(text_emb) / len(text_emb) if text_emb else 0
    t_dis_rate = 100.0 * sum(text_dis) / len(text_dis) if text_dis else 0
    print(f"\n物理任务: 具身 {p_emb_rate:.1f}% vs 非具身 {p_dis_rate:.1f}%")
    print(f"文本任务: 具身 {t_emb_rate:.1f}% vs 非具身 {t_dis_rate:.1f}%")

    output = {"experiment": "exp-07-embodied-vs-disembodied",
              "type_summary": type_summary,
              "overall": {"embodied": all_emb, "disembodied": all_dis},
              "physical": {"embodied": p_emb_rate, "disembodied": p_dis_rate},
              "text_only": {"embodied": t_emb_rate, "disembodied": t_dis_rate},
              "results": results}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
