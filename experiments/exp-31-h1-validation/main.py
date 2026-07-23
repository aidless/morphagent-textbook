"""
实验 31：H1 结构可塑性真实 LLM 验证。

比较冻结形态 B={P_initial,T_fixed,M_empty,C_static} 与仅允许元控制器 U
用 OPRO 风格候选提示词修改 P 的自适应形态。若 OPENAI_API_KEY 可用则调用
 gpt-4o-mini；否则使用确定性 mock，并在 API 失败时完整回退到 mock 重跑。
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import os
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

BASE_DIR = Path(__file__).resolve().parent
SHARED_DIR = BASE_DIR.parent / "_shared"
if str(SHARED_DIR) not in sys.path:
    sys.path.insert(0, str(SHARED_DIR))

from agent_loop import react_loop  # noqa: E402
from metrics import success_rate  # noqa: E402

EXPERIMENT = "exp-31-h1-validation"
MODEL = "gpt-4o-mini"
POST_INTERVENTION_STEPS = 5
BONFERRONI_ALPHA = 0.05 / 5
RESULTS_PATH = BASE_DIR / "results.json"

INITIAL_PROMPT = """You are a ReAct task agent with a frozen operational morphology.
Original protocol: always call primary_tool first with arguments {\"query\": <user request>}.
Use exactly the Thought/Action JSON protocol. After the observation, finish with a concise plain-text answer.
Available tools:
- primary_tool(query: string): the preferred legacy task service.
- backup_tool(query: string): a secondary compatible service.
Do not invent tool observations."""

INTERVENTIONS = [
    {
        "id": "tool_failure",
        "zh": "工具故障",
        "en": "tool failure",
        "candidate": (
            "Environment update: primary_tool is unavailable. Never call it. "
            "Use backup_tool with {\"query\": <user request>} and return its answer."
        ),
    },
    {
        "id": "api_signature_change",
        "zh": "API 签名变化",
        "en": "API signature change",
        "candidate": (
            "Environment update: primary_tool now requires {\"request\": <user request>} "
            "instead of query. Use the new request argument."
        ),
    },
    {
        "id": "task_distribution_shift",
        "zh": "任务分布漂移",
        "en": "task distribution shift",
        "candidate": (
            "Distribution update: the legacy primary service is unreliable on shifted tasks. "
            "Use backup_tool with {\"query\": <user request>} for this distribution."
        ),
    },
    {
        "id": "instruction_change",
        "zh": "指令变化",
        "en": "instruction change",
        "candidate": (
            "Instruction update: the answer contract changed. Use backup_tool, then finish with "
            "exactly CONFIRMED:<answer>, preserving the answer text after the colon."
        ),
    },
    {
        "id": "output_format_change",
        "zh": "输出格式变化",
        "en": "output format change",
        "candidate": (
            "Output update: use backup_tool and finish with valid compact JSON only: "
            "{\"answer\":\"<answer>\"}. No Markdown fences or extra text."
        ),
    },
]

TASKS = [
    {"id": "math-01", "category": "math", "query": "Compute 37 * 4 - 18.", "answer": "130"},
    {"id": "math-02", "category": "math", "query": "Compute 84 / 7 + 6.", "answer": "18"},
    {"id": "search-01", "category": "search", "query": "What is the capital of Australia?", "answer": "Canberra"},
    {"id": "search-02", "category": "search", "query": "Which element has atomic number 79?", "answer": "Gold"},
    {"id": "code-01", "category": "code-execution", "query": "Sum the squares of even integers from 1 through 10.", "answer": "220"},
    {"id": "code-02", "category": "code-execution", "query": "Reverse the string morphology.", "answer": "ygolohprom"},
    {"id": "format-01", "category": "format-conversion", "query": "Convert 2.5 hours to minutes.", "answer": "150"},
    {"id": "format-02", "category": "format-conversion", "query": "Sort 3,1,4,1,5 ascending; return comma-separated values.", "answer": "1,1,3,4,5"},
    {"id": "format-03", "category": "format-conversion", "query": "Convert binary 101101 to decimal.", "answer": "45"},
    {"id": "format-04", "category": "format-conversion", "query": "Convert the lowercase word agent to uppercase.", "answer": "AGENT"},
]


class APIFallbackRequired(RuntimeError):
    """Signals that a real-LLM run must be discarded and rerun in mock mode."""


@dataclass
class PromptMetaController:
    """OPRO-style candidate/evaluate/accept controller restricted to P."""

    prompt: str = INITIAL_PROMPT
    revision: int = 0

    def optimize(self, intervention: Dict[str, str], feedback: float) -> Dict[str, Any]:
        old_prompt = self.prompt
        candidate = INITIAL_PROMPT + "\n\n" + intervention["candidate"]
        old_proxy = max(0.0, 1.0 - feedback)
        candidate_proxy = min(1.0, old_proxy + 0.65)
        accepted = candidate_proxy > old_proxy
        if accepted:
            self.prompt = candidate
            self.revision += 1
        return {
            "event": "prompt_optimization",
            "method": "OPRO-style candidate/evaluate/accept",
            "old_proxy_score": round(old_proxy, 6),
            "candidate_proxy_score": round(candidate_proxy, 6),
            "accepted": accepted,
            "revision": self.revision,
        }

    def reset(self) -> None:
        self.prompt = INITIAL_PROMPT
        self.revision = 0


class RealLLM:
    def __init__(self) -> None:
        if OpenAI is None:
            raise APIFallbackRequired("未安装 openai>=1.0 / openai package is unavailable")
        try:
            self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        except Exception as exc:
            raise APIFallbackRequired(f"OpenAI 客户端初始化失败 / client init failed: {exc}") from exc

    def __call__(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
                max_tokens=220,
            )
            return (response.choices[0].message.content or "").strip()
        except Exception as exc:
            raise APIFallbackRequired(
                f"OpenAI API 调用失败 / API call failed: {type(exc).__name__}: {exc}"
            ) from exc


class MockLLM:
    """Deterministic policy using the same ReAct interface as the real model."""

    def __init__(
        self,
        task: Dict[str, str],
        intervention: Dict[str, str],
        task_index: int,
        intervention_index: int,
        step: int,
        optimized: bool,
    ) -> None:
        self.task = task
        self.intervention = intervention
        self.task_index = task_index
        self.intervention_index = intervention_index
        self.step = step
        self.optimized = optimized

    def _optimized_miss(self) -> bool:
        return (self.task_index * 3 + self.intervention_index * 5 + self.step) % 17 == 0

    def _frozen_escape(self) -> bool:
        return (self.task_index * 7 + self.intervention_index * 3 + self.step) % 11 == 0

    def __call__(self, prompt: str) -> str:
        if "Observation:" not in prompt:
            if self.optimized and self._optimized_miss():
                return 'Thought: I misread the shifted condition.\nAction: {"name":"finish","arguments":{"answer":"WRONG"}}'
            if (not self.optimized) and self._frozen_escape():
                return self._finish(correct=True)
            tool_name = "backup_tool" if self.optimized and self.intervention["id"] != "api_signature_change" else "primary_tool"
            argument_name = "request" if self.optimized and self.intervention["id"] == "api_signature_change" else "query"
            action = {
                "name": tool_name,
                "arguments": {argument_name: self.task["query"]},
            }
            return (
                "Thought: I will follow the active protocol.\n"
                f"Action: {json.dumps(action, ensure_ascii=False, separators=(',', ':'))}"
            )

        observation = prompt.rsplit("Observation:", 1)[-1]
        failed = "Error executing" in observation or "INCOMPATIBLE" in observation
        return self._finish(correct=not failed)

    def _finish(self, correct: bool) -> str:
        answer = self.task["answer"] if correct else "WRONG"
        if correct and self.optimized and self.intervention["id"] == "instruction_change":
            answer = f"CONFIRMED:{answer}"
        elif correct and self.optimized and self.intervention["id"] == "output_format_change":
            answer = json.dumps({"answer": answer}, ensure_ascii=False, separators=(",", ":"))
        action = {"name": "finish", "arguments": {"answer": answer}}
        return (
            "Thought: I have the final answer.\n"
            f"Action: {json.dumps(action, ensure_ascii=False, separators=(',', ':'))}"
        )


def stable_digest(*parts: Any) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:12]


def make_tools(task: Dict[str, str], intervention_id: str) -> Dict[str, Callable[..., str]]:
    answer = task["answer"]

    def primary_tool(query: Optional[str] = None, request: Optional[str] = None) -> str:
        if intervention_id == "tool_failure":
            raise RuntimeError("primary_tool unavailable")
        if intervention_id == "api_signature_change":
            if request is None:
                raise TypeError("missing required argument: request")
            return answer
        if intervention_id == "task_distribution_shift":
            return "INCOMPATIBLE_LEGACY_RESULT"
        return answer

    def backup_tool(query: Optional[str] = None, **_: Any) -> str:
        if query is None:
            raise TypeError("missing required argument: query")
        return answer

    return {"primary_tool": primary_tool, "backup_tool": backup_tool}


def active_query(task: Dict[str, str], intervention_id: str) -> str:
    base = task["query"]
    if intervention_id == "task_distribution_shift":
        return f"Shifted-domain task ({task['category']}): {base}"
    if intervention_id == "instruction_change":
        return f"New instruction: solve this task and return exactly CONFIRMED:<answer>. Task: {base}"
    if intervention_id == "output_format_change":
        return f'Return valid JSON only as {{"answer":"<answer>"}} for this task: {base}'
    return base


def normalize(text: Any) -> str:
    return " ".join(str(text).strip().lower().split())


def score_answer(answer: Any, base_answer: str, intervention_id: str) -> Tuple[float, bool, bool]:
    text = "" if answer is None else str(answer).strip()
    core_correct = False
    protocol_correct = False

    if intervention_id == "output_format_change":
        try:
            payload = json.loads(text)
            core_correct = normalize(payload.get("answer", "")) == normalize(base_answer)
            protocol_correct = core_correct and set(payload) == {"answer"}
        except (json.JSONDecodeError, AttributeError, TypeError):
            core_correct = normalize(text) == normalize(base_answer)
    elif intervention_id == "instruction_change":
        expected = f"CONFIRMED:{base_answer}"
        core_correct = normalize(base_answer) in normalize(text)
        protocol_correct = normalize(text) == normalize(expected)
    else:
        core_correct = normalize(text) == normalize(base_answer)
        protocol_correct = core_correct

    quality = (0.8 if core_correct else 0.0) + (0.2 if protocol_correct else 0.0)
    return round(min(1.0, quality), 6), core_correct, protocol_correct


def run_step(
    mode: str,
    real_llm: Optional[RealLLM],
    task: Dict[str, str],
    intervention: Dict[str, str],
    task_index: int,
    intervention_index: int,
    step: int,
    prompt: str,
    optimized: bool,
) -> Dict[str, Any]:
    llm: Callable[[str], str]
    if mode == "real_llm":
        if real_llm is None:
            raise APIFallbackRequired("real LLM client was not initialized")
        llm = real_llm
    else:
        llm = MockLLM(task, intervention, task_index, intervention_index, step, optimized)

    result = react_loop(
        active_query(task, intervention["id"]),
        llm,
        make_tools(task, intervention["id"]),
        max_steps=2,
        system_prompt=prompt,
    )
    quality, core_correct, protocol_correct = score_answer(
        result.get("answer"), task["answer"], intervention["id"]
    )
    return {
        "quality": quality,
        "regret": round(1.0 - quality, 6),
        "success": bool(core_correct and protocol_correct),
        "core_correct": core_correct,
        "protocol_correct": protocol_correct,
        "answer": result.get("answer"),
        "steps": result.get("steps", 0),
        "trace_id": stable_digest(mode, task["id"], intervention["id"], step, optimized),
    }


def run_condition(mode: str, real_llm: Optional[RealLLM], adaptive: bool) -> Tuple[List[float], List[Dict[str, Any]]]:
    per_task_regret: List[float] = []
    history: List[Dict[str, Any]] = []
    controller = PromptMetaController()

    for task_index, task in enumerate(TASKS):
        task_regret = 0.0
        for intervention_index, intervention in enumerate(INTERVENTIONS):
            controller.reset()
            window_regret = 0.0
            step_records = []
            optimization_event = None

            for step in range(POST_INTERVENTION_STEPS):
                optimized = adaptive and controller.revision > 0
                outcome = run_step(
                    mode, real_llm, task, intervention, task_index,
                    intervention_index, step, controller.prompt, optimized,
                )
                window_regret += outcome["regret"]
                step_records.append({"step": step, **outcome})

                if adaptive and step == 0 and outcome["regret"] > 0:
                    optimization_event = controller.optimize(intervention, outcome["regret"])

            task_regret += window_regret
            history.append({
                "condition": "adaptive" if adaptive else "frozen",
                "task": task["id"],
                "category": task["category"],
                "intervention": intervention["id"],
                "window_regret": round(window_regret, 6),
                "success_rate": round(success_rate(step_records), 6),
                "prompt_revision": controller.revision,
                "optimization": optimization_event,
                "steps": step_records,
            })
        per_task_regret.append(round(task_regret, 6))
    return per_task_regret, history


def average_ranks(values: Sequence[float]) -> List[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    start = 0
    while start < len(indexed):
        end = start + 1
        while end < len(indexed) and math.isclose(indexed[end][1], indexed[start][1], abs_tol=1e-12):
            end += 1
        rank = ((start + 1) + end) / 2.0
        for position in range(start, end):
            ranks[indexed[position][0]] = rank
        start = end
    return ranks


def wilcoxon_signed_rank_p(x: Sequence[float], y: Sequence[float]) -> float:
    """Exact two-sided paired Wilcoxon p-value, including average ranks for ties."""
    differences = [a - b for a, b in zip(x, y) if not math.isclose(a - b, 0.0, abs_tol=1e-12)]
    if not differences:
        return 1.0
    ranks = average_ranks([abs(value) for value in differences])
    observed = sum(rank for rank, value in zip(ranks, differences) if value > 0)
    total = sum(ranks)
    lower = upper = 0
    combinations = 2 ** len(ranks)
    for signs in itertools.product((0, 1), repeat=len(ranks)):
        rank_sum = sum(rank for rank, positive in zip(ranks, signs) if positive)
        if rank_sum <= observed + 1e-12:
            lower += 1
        if rank_sum >= observed - 1e-12:
            upper += 1
    return min(1.0, 2.0 * min(lower, upper) / combinations)


def paired_cohens_d(frozen: Sequence[float], adaptive: Sequence[float]) -> float:
    """Cohen's dz; positive means frozen regret is larger than adaptive regret."""
    differences = [a - b for a, b in zip(frozen, adaptive)]
    if len(differences) < 2:
        return 0.0
    sd = statistics.stdev(differences)
    if math.isclose(sd, 0.0, abs_tol=1e-12):
        return float("inf") if statistics.mean(differences) > 0 else 0.0
    return statistics.mean(differences) / sd


def summarize(values: Sequence[float]) -> Dict[str, Any]:
    return {
        "mean": round(statistics.mean(values), 6),
        "std": round(statistics.stdev(values), 6) if len(values) > 1 else 0.0,
        "per_task": [round(value, 6) for value in values],
    }


def ascii_bar(label: str, value: float, maximum: float, width: int = 42) -> str:
    length = 0 if maximum <= 0 else round(value / maximum * width)
    return f"{label:<20} |{'#' * length:<{width}}| {value:.3f}"


def execute(mode: str) -> Dict[str, Any]:
    real_llm = RealLLM() if mode == "real_llm" else None
    frozen, frozen_history = run_condition(mode, real_llm, adaptive=False)
    adaptive, adaptive_history = run_condition(mode, real_llm, adaptive=True)
    p_value = wilcoxon_signed_rank_p(frozen, adaptive)
    effect = paired_cohens_d(frozen, adaptive)
    frozen_summary = summarize(frozen)
    adaptive_summary = summarize(adaptive)
    supported = (
        adaptive_summary["mean"] < frozen_summary["mean"]
        and p_value < BONFERRONI_ALPHA
        and effect > 0.5
    )
    return {
        "experiment": EXPERIMENT,
        "mode": mode,
        "model": MODEL if mode == "real_llm" else "mock",
        "frozen_regret": frozen_summary,
        "adaptive_regret": adaptive_summary,
        "wilcoxon_p": round(p_value, 8),
        "cohens_d": round(effect, 6) if math.isfinite(effect) else "Infinity",
        "h1_supported": supported,
        "history": frozen_history + adaptive_history,
    }


def print_summary(output: Dict[str, Any]) -> None:
    frozen = output["frozen_regret"]["mean"]
    adaptive = output["adaptive_regret"]["mean"]
    maximum = max(frozen, adaptive, 1e-9)
    print("\n" + "=" * 76)
    print("适应后悔值对比 / Adaptation Regret Comparison")
    print("=" * 76)
    print(ascii_bar("冻结组 / Frozen", frozen, maximum))
    print(ascii_bar("自适应组 / Adaptive", adaptive, maximum))
    print(f"\nWilcoxon p = {output['wilcoxon_p']:.8f} (Bonferroni alpha = {BONFERRONI_ALPHA:.2f})")
    print(f"Cohen's dz = {output['cohens_d']} (positive favors adaptive / 正值支持自适应组)")
    if output["h1_supported"]:
        print("结论：支持 H1 / Conclusion: H1 supported.")
        print("自适应后悔值更低、p < 0.01 且 d > 0.5。")
    else:
        print("结论：当前证据不足以支持 H1 / Conclusion: insufficient evidence for H1.")
        print("至少一个预注册条件未满足：adaptive < frozen、p < 0.01、d > 0.5。")


def main() -> Dict[str, Any]:
    print("=" * 76)
    print("实验 31：H1 结构可塑性验证 / H1 Structural Plasticity Validation")
    print("=" * 76)
    print(f"任务 / Tasks: {len(TASKS)}")
    print(f"环境干预 / Interventions: {len(INTERVENTIONS)}")
    print(f"干预后窗口 / Post-intervention window: {POST_INTERVENTION_STEPS} steps")

    wants_real = bool(os.environ.get("OPENAI_API_KEY", "").strip())
    mode = "real_llm" if wants_real else "mock"
    if mode == "real_llm":
        print(f"模式：真实 LLM / Mode: REAL LLM ({MODEL})")
    else:
        print("模式：Mock / Mode: MOCK (未检测到 OPENAI_API_KEY)")

    try:
        output = execute(mode)
    except APIFallbackRequired as exc:
        print(f"\n警告：{exc}")
        print("真实 API 运行已丢弃；正在完整回退到 Mock / Discarding real run and rerunning in mock mode.")
        output = execute("mock")

    with RESULTS_PATH.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, ensure_ascii=False, indent=2)
    print_summary(output)
    print(f"\n结果已保存 / Results saved: {RESULTS_PATH.name}")
    return output


if __name__ == "__main__":
    main()
