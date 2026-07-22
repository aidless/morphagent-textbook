"""
实验 4：OPRO 风格的自修改 Prompt（Mock 模式）

实现 OPRO 爬山优化 prompt 的简化版。
在 10 个数学任务上对比优化前后的准确率，绘制爬山曲线。

运行：
    python main.py
"""
import re
import json
import random
import statistics


# ==================== 数学任务集 ====================
MATH_TASKS = [
    {"q": "Janet has 3 apples. She gives 1 away and buys 5 more. How many?", "a": 7},
    {"q": "A store sells 4 books for $2 each. Total revenue?", "a": 8},
    {"q": "12 birds on a tree. 5 fly away. How many left?", "a": 7},
    {"q": "4 boxes, each with 3 oranges. Total oranges?", "a": 12},
    {"q": "60 miles in 2 hours. Speed?", "a": 30},
    {"q": "Sara has 20 candies, gives 8 away. Left?", "a": 12},
    {"q": "6 pencils per pack. 5 packs total?", "a": 30},
    {"q": "John is 15, sister is 3 years younger. Sister's age?", "a": 12},
    {"q": "200 pages, 50 per day. Days to finish?", "a": 4},
    {"q": "Pizza cut into 8 slices. 3 eaten. Left?", "a": 5},
]


# ==================== Prompt 模板 ====================
INITIAL_PROMPT = "You are a math tutor. Solve step by step. Question: {q}\nAnswer with a number."

# OPRO 优化方向池（模拟 LLM 生成的候选 prompt 变体）
OPRO_CANDIDATES = [
    "You are an expert mathematician. Extract numbers, identify operations, compute precisely. Question: {q}\nAnswer:",
    "Solve carefully: (1) extract numbers (2) find operations (3) compute. Q: {q}\nFinal answer:",
    "Read the problem. List all numbers. Determine +,-,*,/. Calculate. Q: {q}\nNumber:",
    "Math expert mode. Identify quantities and operations step by step. Question: {q}\nResult:",
    "Analyze: What numbers? What operation? Compute. Question: {q}\nAnswer (number only):",
]


def mock_answer(prompt: str, quality: float) -> str:
    """模拟 LLM 回答数学题。quality 表示 prompt 质量对准确率的影响。"""
    rng = random.Random(hash(prompt) % (2**31))
    if rng.random() < quality:
        # 正确回答：从 prompt 提取题目，直接返回正确答案
        for task in MATH_TASKS:
            if task["q"][:20] in prompt:
                return str(task["a"])
        return "7"  # fallback
    else:
        # 错误回答
        wrong = rng.randint(0, 100)
        return str(wrong)


def extract_number(text: str) -> int | None:
    """从文本提取第一个数字。"""
    m = re.search(r"-?\d+", text.replace(",", ""))
    return int(m.group(0)) if m else None


def evaluate_prompt(prompt_template: str, quality: float) -> float:
    """评估一个 prompt 在全部任务上的准确率。"""
    correct = 0
    for task in MATH_TASKS:
        prompt = prompt_template.format(q=task["q"])
        answer = mock_answer(prompt, quality)
        predicted = extract_number(answer)
        if predicted == task["a"]:
            correct += 1
    return 100.0 * correct / len(MATH_TASKS)


def opro_hill_climbing(initial_prompt: str, iterations: int = 5) -> list:
    """OPRO 爬山：每轮尝试新 prompt，保留更好的。"""
    rng = random.Random(42)
    history = []
    current_prompt = initial_prompt

    # 初始 prompt 质量较低
    base_quality = 0.40
    current_score = evaluate_prompt(current_prompt, base_quality)
    history.append({"iter": 0, "prompt": current_prompt, "score": current_score,
                     "quality": base_quality})
    print(f"  迭代 0: 准确率 {current_score:.1f}%")

    for i in range(1, iterations + 1):
        # 生成候选（从候选池中随机选取）
        candidate = rng.choice(OPRO_CANDIDATES)
        # OPRO 核心思想：每次迭代，prompt 质量提升
        candidate_quality = min(0.98, base_quality + 0.10 * i + rng.uniform(-0.05, 0.05))
        candidate_score = evaluate_prompt(candidate, candidate_quality)

        # 爬山：保留更好的
        if candidate_score > current_score:
            current_prompt = candidate
            current_score = candidate_score
            base_quality = candidate_quality
            print(f"  迭代 {i}: 新 prompt 得分 {candidate_score:.1f}% (接受)")
        else:
            print(f"  迭代 {i}: 候选 {candidate_score:.1f}% (拒绝, 保持 {current_score:.1f}%)")

        history.append({"iter": i, "prompt": current_prompt, "score": current_score,
                         "quality": base_quality, "candidate_score": candidate_score,
                         "accepted": candidate_score > (history[-1]["score"] if history else 0)})

    return history


def print_hill_curve(history: list):
    """打印 ASCII 爬山曲线。"""
    print("\n爬山曲线:")
    max_score = max(h["score"] for h in history)
    for h in history:
        bar_len = int(h["score"] / max_score * 40)
        bar = "#" * bar_len
        print(f"  迭代 {h['iter']}: {bar} {h['score']:.1f}%")


def main():
    print("=" * 60)
    print("实验 4：OPRO 自修改 Prompt（Mock 模式）")
    print("=" * 60)
    print(f"任务数: {len(MATH_TASKS)}, OPRO 迭代轮数: 5\n")

    # Baseline: 静态 prompt
    print("--- 静态 Prompt Baseline ---")
    baseline_score = evaluate_prompt(INITIAL_PROMPT, quality=0.40)
    print(f"  静态 prompt 准确率: {baseline_score:.1f}%\n")

    # OPRO 优化
    print("--- OPRO 爬山优化 ---")
    history = opro_hill_climbing(INITIAL_PROMPT, iterations=5)

    # 结果对比
    initial = history[0]["score"]
    final = history[-1]["score"]
    print(f"\n优化前: {initial:.1f}% -> 优化后: {final:.1f}%")
    print(f"提升: +{final - initial:.1f}pp")
    print_hill_curve(history)

    output = {"experiment": "exp-04-self-modifying-prompt",
              "baseline_score": baseline_score, "final_score": final,
              "improvement": final - initial, "history": history}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
