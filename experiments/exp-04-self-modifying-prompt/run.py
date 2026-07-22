"""
实验 4：自修改 prompt vs 静态 prompt（真实 OpenAI 模式）

使用 gpt-4o-mini 验证 OPRO 风格的 prompt 自修改 vs 静态 prompt 的效果。
4 策略 × 10 题（GSM8K 简化）= 40 次评估。

运行：
    cd exp-04-self-modifying-prompt
    python run.py
"""
import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

BASE_DIR = Path(__file__).resolve().parent
MODEL = "gpt-4o-mini"
MAX_BUDGET_USD = 5.0
MAX_COMPLETION_TOKENS = 500
RESULTS_REAL_PATH = BASE_DIR / "results_real.json"
MOCK_RESULTS_PATH = BASE_DIR / "results.json"

INPUT_USD_PER_MILLION = 0.15
OUTPUT_USD_PER_MILLION = 0.60


# ==================== GSM8K 简化测试集 ====================
GSM8K_SAMPLE = [
    {"question": "Janet has 3 apples. She gives 1 to her friend and buys 5 more. How many apples does she have now?", "answer": 7},
    {"question": "A store sells 4 books for $2 each. How much money does the store make?", "answer": 8},
    {"question": "There are 12 birds on a tree. 5 fly away. How many are left?", "answer": 7},
    {"question": "Tom has 4 boxes. Each box has 3 oranges. How many oranges in total?", "answer": 12},
    {"question": "A car travels 60 miles in 2 hours. What is its speed?", "answer": 30},
    {"question": "Sara has 20 candies. She gives 8 to her brother. How many are left?", "answer": 12},
    {"question": "A pack has 6 pencils. How many pencils in 5 packs?", "answer": 30},
    {"question": "John is 15 years old. His sister is 3 years younger. How old is his sister?", "answer": 12},
    {"question": "A book has 200 pages. Mary reads 50 pages per day. How many days to finish?", "answer": 4},
    {"question": "A pizza is cut into 8 slices. 3 are eaten. How many are left?", "answer": 5},
]


# ==================== 4 种 Prompt 策略 ====================
PROMPTS = {
    "static": (
        "You are a math tutor. Solve the following problem step by step.\n"
        "Question: {question}\n"
        "Answer with a single number at the end."
    ),
    "dspy_optimized": (
        "Carefully analyze the math word problem. Identify quantities, "
        "operations, and compute the final answer.\n"
        "Question: {question}\n"
        "Reasoning: [step by step]\n"
        "Final Answer: [single number]"
    ),
    "opro_iter1": (
        "You are an expert mathematician. Use the fewest steps to solve:\n"
        "Question: {question}\n"
        "Compute and give only the numerical answer."
    ),
    "opro_iter3": (
        "You are an expert mathematician specialized in elementary word problems. "
        "For each problem: (1) extract numbers, (2) identify operations, "
        "(3) compute. Be precise. Show only the final number.\n"
        "Question: {question}\n"
        "Answer:"
    ),
}


# ==================== 真实 OpenAI LLM ====================
class BudgetExceededError(RuntimeError):
    pass


@dataclass
class CostTracker:
    max_cost_usd: float = MAX_BUDGET_USD
    total_cost_usd: float = 0.0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    stopped: bool = False
    stop_reason: Optional[str] = None

    def ensure_request_allowed(self, prompt: str) -> None:
        input_token_upper_bound = len(prompt.encode("utf-8"))
        worst_case_cost = (
            input_token_upper_bound * INPUT_USD_PER_MILLION
            + MAX_COMPLETION_TOKENS * OUTPUT_USD_PER_MILLION
        ) / 1_000_000
        if self.total_cost_usd + worst_case_cost > self.max_cost_usd:
            self.stopped = True
            self.stop_reason = (
                f"预算保护已触发：已花费 ${self.total_cost_usd:.6f}，"
                f"下一次请求最坏需 ${worst_case_cost:.6f}，"
                f"上限为 ${self.max_cost_usd:.2f}。"
            )
            raise BudgetExceededError(self.stop_reason)

    def record_usage(self, usage: Any) -> float:
        if usage is None:
            self.stopped = True
            self.stop_reason = "OpenAI 响应未提供 usage。"
            raise RuntimeError(self.stop_reason)
        prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
        completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
        request_cost = (
            prompt_tokens * INPUT_USD_PER_MILLION
            + completion_tokens * OUTPUT_USD_PER_MILLION
        ) / 1_000_000
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.total_cost_usd += request_cost
        if self.total_cost_usd > self.max_cost_usd:
            self.stopped = True
            self.stop_reason = f"累计花费 ${self.total_cost_usd:.6f} 已超 ${self.max_cost_usd:.2f}。"
            raise BudgetExceededError(self.stop_reason)
        return request_cost


def make_openai_llm(client: Any, tracker: CostTracker) -> Callable[[str], str]:
    def real_llm(prompt: str) -> str:
        tracker.ensure_request_allowed(prompt)
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=MAX_COMPLETION_TOKENS,
            )
        except Exception as exc:
            tracker.stopped = True
            tracker.stop_reason = f"OpenAI API 调用失败：{type(exc).__name__}: {exc}"
            raise RuntimeError(tracker.stop_reason) from exc
        tracker.record_usage(getattr(response, "usage", None))
        return (response.choices[0].message.content or "").strip()
    return real_llm


_ACTIVE_REAL_LLM: Optional[Callable[[str], str]] = None


def mock_llm(prompt: str) -> str:
    """真实 LLM 占位符，由 main() 注入。"""
    if _ACTIVE_REAL_LLM is None:
        raise RuntimeError("真实 LLM 尚未初始化；请通过 main() 运行实验。")
    return _ACTIVE_REAL_LLM(prompt)


def check_openai_environment() -> Tuple[bool, str]:
    missing = []
    if OpenAI is None:
        missing.append("Python 包 openai>=1.0")
    if not os.environ.get("OPENAI_API_KEY", "").strip():
        missing.append("环境变量 OPENAI_API_KEY")
    prereq = "真实模式需要：openai>=1.0，以及环境变量 OPENAI_API_KEY。"
    if missing:
        return False, f"{prereq}\n当前缺少：{'；'.join(missing)}。"
    return True, prereq


def extract_number(text: str) -> Optional[int]:
    """从模型输出中提取第一个整数。"""
    import re
    m = re.search(r"-?\d+", text.replace(",", ""))
    if m:
        try:
            return int(m.group(0))
        except ValueError:
            return None
    return None


# ==================== 实验运行 ====================
def run_strategy_real(
    strategy_name: str,
    prompt_template: str,
    llm: Callable[[str], str],
    tracker: CostTracker,
) -> Dict[str, Any]:
    results = []
    for problem in GSM8K_SAMPLE:
        if tracker.stopped:
            results.append({
                "question": problem["question"],
                "expected": problem["answer"],
                "actual": None,
                "correct": False,
                "skipped": True,
            })
            continue

        cost_before = tracker.total_cost_usd
        full_prompt = prompt_template.format(question=problem["question"])
        response = llm(full_prompt)
        predicted = extract_number(response)
        correct = predicted == problem["answer"]

        result = {
            "question": problem["question"],
            "expected": problem["answer"],
            "actual": predicted,
            "raw_response": response[:200],
            "correct": correct,
        }
        results.append(result)
        result["cost"] = round(tracker.total_cost_usd - cost_before, 8)

    return {
        "strategy": strategy_name,
        "accuracy": 100.0 * sum(r["correct"] for r in results) / len(results),
        "cost": round(tracker.total_cost_usd, 8),
        "results": results,
    }


def run_all_real(tracker: CostTracker, llm: Callable[[str], str]) -> Dict[str, Any]:
    output = {}
    for name, template in PROMPTS.items():
        if tracker.stopped:
            output[name] = {
                "strategy": name,
                "accuracy": 0.0,
                "cost": 0.0,
                "results": [],
                "skipped": True,
            }
            continue
        print(f"  跑 {name}...")
        output[name] = run_strategy_real(name, template, llm, tracker)
    return output


def print_comparison(real_results: Dict[str, Any]) -> None:
    print("\n" + "=" * 60)
    print("Prompt 策略对比（真实 LLM）")
    print("=" * 60)
    print("\n| 策略 | 准确率 | 累计成本 |")
    print("|---|---|---|")
    for name in PROMPTS:
        r = real_results.get(name, {})
        print(f"| {name} | {r.get('accuracy', 0):.1f}% | ${r.get('cost', 0):.6f} |")


def save_real_results(real_results: Dict[str, Any], tracker: CostTracker, elapsed: float) -> None:
    status = "stopped" if tracker.stopped else "completed"
    if tracker.stop_reason and "预算" in tracker.stop_reason:
        status = "budget_exceeded"
    output = {
        "experiment": "exp-04-self-modifying-prompt",
        "mode": "real",
        "model": MODEL,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": status,
        "stop_reason": tracker.stop_reason,
        "max_budget_usd": tracker.max_cost_usd,
        "total_cost_usd": round(tracker.total_cost_usd, 8),
        "elapsed_seconds": round(elapsed, 3),
        "usage": {
            "prompt_tokens": tracker.prompt_tokens,
            "completion_tokens": tracker.completion_tokens,
        },
        "results": real_results,
    }
    with RESULTS_REAL_PATH.open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到 {RESULTS_REAL_PATH.name}")


def main() -> None:
    print("=" * 60)
    print(f"实验 4：自修改 prompt vs 静态 prompt（真实模型 {MODEL}）")
    print(f"硬预算上限：${MAX_BUDGET_USD:.2f}")
    print("=" * 60)

    env_ok, message = check_openai_environment()
    if not env_ok:
        print("\n[已安全跳过] 无法运行真实 OpenAI 实验。")
        print(message)
        print("PowerShell 示例：$env:OPENAI_API_KEY = 'sk-...'")
        return

    global _ACTIVE_REAL_LLM
    tracker = CostTracker(max_cost_usd=MAX_BUDGET_USD)

    try:
        client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            timeout=60.0,
            max_retries=2,
        )
        _ACTIVE_REAL_LLM = make_openai_llm(client, tracker)
    except Exception as exc:
        print(f"\n[已安全跳过] OpenAI 客户端初始化失败：{type(exc).__name__}: {exc}")
        return

    started = time.time()
    real_results = run_all_real(tracker, mock_llm)
    elapsed = time.time() - started

    save_real_results(real_results, tracker, elapsed)
    print_comparison(real_results)

    print(f"\n总花费：${tracker.total_cost_usd:.6f} / ${tracker.max_cost_usd:.2f}")
    if tracker.stop_reason:
        print(f"停止原因：{tracker.stop_reason}")


if __name__ == "__main__":
    main()
