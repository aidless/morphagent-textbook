"""
实验 13：Prompt 进化轨迹（Mock 模式）

追踪 Prompt 在多轮 OPRO 优化后的进化轨迹。
每轮生成候选 -> 评估 -> 保留 top-3 -> 下一轮变异。

运行：
    python main.py
"""
import json
import random
import re
import statistics


# ==================== 任务集 ====================
TASKS = [
    {"q": "If 3 cats have 4 kittens each, how many cats total?", "a": 15},
    {"q": "A train travels 120km in 2h. Speed?", "a": 60},
    {"q": "5 apples cost $3.75. Price per apple?", "a": 0.75},
    {"q": "Room is 8m x 6m. Area?", "a": 48},
    {"q": "John has $20, spends $7.50. Left?", "a": 12.5},
    {"q": "Pipe fills tank in 4h, drain in 6h. Net fill time?", "a": 12},
    {"q": "3 workers finish in 6 days. 2 workers?", "a": 9},
    {"q": "Sum of first 10 natural numbers?", "a": 55},
    {"q": "2^8 = ?", "a": 256},
    {"q": "Circle radius 7cm. Circumference? (pi~3.14)", "a": 43.96},
]


# ==================== Prompt 变异 ====================
INITIAL_PROMPT = "You are a math assistant. Answer the question: {q}\nAnswer:"

VARIATION_POOL = [
    "Solve step by step. Q: {q}\nFinal answer:",
    "Think carefully. Extract numbers, find operation, compute. Q: {q}\nResult:",
    "Expert math: identify quantities and operations. {q}\nNumber:",
    "Methodical approach: (1) parse (2) plan (3) calculate. Q: {q}\nAns:",
    "Math solver. Read, extract, compute precisely. {q}\nValue:",
    "Break it down: what numbers? what operation? Q: {q}\nAnswer:",
    "Compute: find all numbers, determine operation order. {q}\nOutput:",
    "Solve: (a) identify (b) calculate (c) verify. Q: {q}\nResult:",
    "Precise math: parse numbers, select operations, execute. {q}\nAnswer:",
    "Analyze the math problem systematically. Q: {q}\nNumeric answer:",
    "Step 1: Read carefully. Step 2: Extract numbers. Step 3: Compute. Q: {q}\nAns:",
    "Focus on numbers and operators. Q: {q}\nCalculate and return number:",
]


def extract_number(text: str) -> float | None:
    m = re.search(r"-?\d+\.?\d*", text.replace(",", ""))
    return float(m.group(0)) if m else None


def mock_evaluate(prompt_template: str, quality: float) -> float:
    """评估 prompt 在全部任务上的准确率。"""
    rng = random.Random(hash(prompt_template) % (2**31))
    correct = 0
    for task in TASKS:
        prompt = prompt_template.format(q=task["q"])
        if rng.random() < quality:
            predicted = extract_number(str(task["a"]))
            correct += (predicted == task["a"] or (predicted and abs(predicted - task["a"]) < 0.1))
    return 100.0 * correct / len(TASKS)


def generate_variants(base_prompt: str, n: int = 5) -> list[str]:
    """从变体池中随机选择 n 个变体。"""
    rng = random.Random(42)
    variants = list(set(VARIATION_POOL) - {base_prompt})
    return rng.sample(variants, min(n, len(variants)))


def prompt_drift(s1: str, s2: str) -> float:
    """计算两个 prompt 之间的漂移（Jaccard 距离）。"""
    w1 = set(s1.split())
    w2 = set(s2.split())
    union = w1 | w2
    if not union:
        return 0.0
    return 1.0 - len(w1 & w2) / len(union)


def evolution_loop(rounds: int = 5, candidates_per_round: int = 5) -> dict:
    """运行完整的 Prompt 进化过程。"""
    rng = random.Random(42)
    history = []
    current_best = INITIAL_PROMPT
    base_quality = 0.30

    for r in range(rounds):
        quality_boost = 0.12 * (r + 1)
        variants = generate_variants(current_best, candidates_per_round)
        # 评估所有变体
        scored = []
        for v in variants:
            q = min(0.98, base_quality + quality_boost + rng.uniform(-0.08, 0.08))
            score = mock_evaluate(v, q)
            drift = prompt_drift(current_best, v)
            scored.append({"prompt": v, "score": score, "quality": q, "drift": drift})

        # 加入当前最优
        cq = min(0.98, base_quality + quality_boost)
        current_score = mock_evaluate(current_best, cq)
        scored.append({"prompt": current_best, "score": current_score,
                      "quality": cq, "drift": 0.0, "is_current_best": True})

        # Top-3
        scored.sort(key=lambda x: -x["score"])
        top3 = scored[:3]

        # 选新的最优
        new_best = top3[0]["prompt"]
        if top3[0]["score"] > current_score:
            current_best = new_best

        round_record = {
            "round": r + 1,
            "top3": [{"score": t["score"], "drift": t["drift"],
                       "prompt_preview": t["prompt"][:60]} for t in top3],
            "best_prompt": current_best[:80],
            "best_score": top3[0]["score"],
        }
        history.append(round_record)
        print(f"  Round {r+1}: top-3 scores = "
              f"{top3[0]['score']:.1f}%, {top3[1]['score']:.1f}%, {top3[2]['score']:.1f}%")

    return {"history": history, "final_prompt": current_best,
            "final_score": history[-1]["best_score"]}


def main():
    print("=" * 60)
    print("实验 13：Prompt 进化轨迹（Mock 模式）")
    print("=" * 60)
    print(f"任务数: {len(TASKS)}, 进化轮数: 5, 每轮候选: 5\n")

    result = evolution_loop(rounds=5, candidates_per_round=5)
    history = result["history"]

    # 进化曲线
    print("\n进化曲线:")
    for h in history:
        bar_len = int(h["best_score"] / 100 * 40)
        bar = "#" * bar_len
        print(f"  R{h['round']}: {bar} {h['best_score']:.1f}%")

    # 统计
    scores = [h["best_score"] for h in history]
    print(f"\n初始准确率: {scores[0]:.1f}% -> 最终: {scores[-1]:.1f}%")
    print(f"总提升: +{scores[-1] - scores[0]:.1f}pp")
    print(f"平均提升/轮: {(scores[-1] - scores[0]) / len(scores):.1f}pp")

    # 漂移
    drifts = []
    for i in range(1, len(history)):
        d = prompt_drift(history[i-1]["best_prompt"], history[i]["best_prompt"])
        drifts.append(d)
    avg_drift = statistics.mean(drifts) if drifts else 0
    print(f"平均 prompt 漂移/轮: {avg_drift:.3f}")

    output = {"experiment": "exp-13-prompt-evolution", **result,
              "initial_score": scores[0], "total_improvement": scores[-1] - scores[0],
              "avg_drift": avg_drift}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
