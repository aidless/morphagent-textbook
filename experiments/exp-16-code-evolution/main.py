"""
实验 16：代码自进化轨迹（Mock 模式）

模拟代码自进化过程：初始代码 -> 评估 -> 变异 -> 再评估。
追踪代码质量（正确率、复杂度）随进化轮次的变化。

运行：
    python main.py
"""
import json
import random
import re


# ==================== 代码任务定义 ====================
CODE_TASKS = {
    "bubble_sort": {
        "initial_code": (
            "def bubble_sort(arr):\n"
            "    for i in range(len(arr)):\n"
            "        for j in range(len(arr)):\n"       # bug: j range too large
            "            if arr[j] > arr[j+1]:\n"       # bug: index out of range
            "                arr[j], arr[j+1] = arr[j+1], arr[j]\n"
            "    return arr"
        ),
        "test_cases": [
            {"input": [3, 1, 2], "expected": [1, 2, 3]},
            {"input": [5, 4, 3, 2, 1], "expected": [1, 2, 3, 4, 5]},
            {"input": [1], "expected": [1]},
            {"input": [], "expected": []},
            {"input": [2, 1, 3, 1, 4], "expected": [1, 1, 2, 3, 4]},
        ],
    },
    "binary_search": {
        "initial_code": (
            "def binary_search(arr, target):\n"
            "    lo, hi = 0, len(arr)\n"               # bug: hi should be len(arr)-1
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if arr[mid] == target:\n"
            "            return mid\n"
            "        elif arr[mid] < target:\n"
            "            lo = mid + 1\n"
            "        else:\n"                            # bug: should be hi = mid - 1
            "            hi = mid\n"
            "    return -1"
        ),
        "test_cases": [
            {"input": ([1, 3, 5, 7, 9], 5), "expected": 2},
            {"input": ([1, 3, 5, 7, 9], 1), "expected": 0},
            {"input": ([1, 3, 5, 7, 9], 9), "expected": 4},
            {"input": ([1, 3, 5, 7, 9], 6), "expected": -1},
            {"input": ([2, 4], 4), "expected": 1},
        ],
    },
    "count_vowels": {
        "initial_code": (
            "def count_vowels(s):\n"
            "    count = 0\n"
            "    for ch in s:\n"
            "        if ch in 'aeiou':\n"                # bug: missing uppercase
            "            count += 1\n"
            "    return count"
        ),
        "test_cases": [
            {"input": "hello", "expected": 2},
            {"input": "AEIOU", "expected": 5},
            {"input": "xyz", "expected": 0},
            {"input": "OpenAI", "expected": 4},
            {"input": "", "expected": 0},
        ],
    },
}


# ==================== 模拟代码评估 ====================
def evaluate_code(task_name: str, code: str, bug_level: int) -> dict:
    """模拟代码评估。bug_level 0=完美, 1=小bug, 2=大bug."""
    task = CODE_TASKS[task_name]
    rng = random.Random(hash(code) % (2**31))
    passed = 0
    total = len(task["test_cases"])

    for tc in task["test_cases"]:
        # 根据 bug_level 决定通过率
        if bug_level == 0:
            passed += 1
        elif bug_level == 1:
            passed += 1 if rng.random() < 0.6 else 0
        elif bug_level == 2:
            passed += 1 if rng.random() < 0.2 else 0

    # 模拟复杂度
    lines = code.count("\n") + 1
    branches = code.count("if") + code.count("elif") + code.count("else") + code.count("for")
    complexity = max(1, branches)

    return {
        "correctness": 100.0 * passed / total,
        "complexity": complexity,
        "lines": lines,
        "bug_level": bug_level,
    }


# ==================== 变异策略 ====================
MUTATION_STRATEGIES = {
    "random_fix": {
        "name": "随机修复",
        "improvement_rate": 0.15,
        "regression_rate": 0.05,
        "description": "随机尝试修复，可能引入新 bug",
    },
    "directed_fix": {
        "name": "定向修复",
        "improvement_rate": 0.35,
        "regression_rate": 0.02,
        "description": "基于测试反馈定向修复 bug",
    },
    "refactor": {
        "name": "重构优化",
        "improvement_rate": 0.20,
        "regression_rate": 0.10,
        "description": "重构代码，可能改善结构但引入回归",
    },
}


def evolve_code(task_name: str, strategy: str, rounds: int = 10) -> list[dict]:
    """运行代码进化过程。"""
    rng = random.Random(42)
    strategy_info = MUTATION_STRATEGIES[strategy]
    bug_level = 2  # 初始有严重 bug
    history = []

    for r in range(rounds):
        code_variant = f"{task_name}_v{r}_{strategy}"
        result = evaluate_code(task_name, code_variant, bug_level)

        # 决定是否改进
        if rng.random() < strategy_info["improvement_rate"]:
            bug_level = max(0, bug_level - 1)
        if rng.random() < strategy_info["regression_rate"]:
            bug_level = min(2, bug_level + 1)

        history.append({
            "round": r + 1,
            **result,
            "bug_level": bug_level,
        })

    return history


def main():
    print("=" * 60)
    print("实验 16：代码自进化轨迹（Mock 模式）")
    print("=" * 60)
    print(f"任务数: {len(CODE_TASKS)}, 策略数: {len(MUTATION_STRATEGIES)}, 轮数: 10\n")

    all_results = {}

    for task_name in CODE_TASKS:
        print(f"\n{'='*50}")
        print(f"任务: {task_name}")
        print(f"{'='*50}")

        task_results = {}
        for strat_key, strat_info in MUTATION_STRATEGIES.items():
            history = evolve_code(task_name, strat_key, rounds=10)
            final = history[-1]

            print(f"\n  策略: {strat_info['name']} ({strat_info['description']})")
            for h in history:
                bar = "#" * int(h["correctness"] / 100 * 30)
                print(f"    R{h['round']:>2}: [{bar:30s}] {h['correctness']:>5.1f}% "
                      f"(复杂度={h['complexity']}, bug={h['bug_level']})")
            print(f"    最终正确率: {final['correctness']:.1f}%")

            task_results[strat_key] = {
                "history": history,
                "final_correctness": final["correctness"],
            }

        all_results[task_name] = task_results

    # 汇总对比
    print("\n" + "=" * 60)
    print("策略汇总对比")
    print("=" * 60)
    print(f"| {'任务':<16} | {'策略':<10} | {'初始':>8} | {'最终':>8} | {'提升':>8} |")
    print(f"|{'-'*18}|{'-'*12}|{'-'*10}|{'-'*10}|{'-'*10}|")

    for task_name, task_results in all_results.items():
        for strat_key, strat_info in MUTATION_STRATEGIES.items():
            data = task_results[strat_key]
            initial = data["history"][0]["correctness"]
            final = data["final_correctness"]
            print(f"| {task_name:<16} | {strat_info['name']:<10} | {initial:>7.1f}% | "
                  f"{final:>7.1f}% | {final - initial:>+7.1f}% |")

    # 结论
    print("\n结论:")
    print("  - 定向修复（基于测试反馈）收敛最快")
    print("  - 随机修复有较大概率停滞")
    print("  - 重构优化可能引入回归，需谨慎使用")

    output = {"experiment": "exp-16-code-evolution", "results": all_results}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
