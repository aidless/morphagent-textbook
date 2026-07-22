"""
实验 1：基线对比（真实 OpenAI 模式）

使用 gpt-4o-mini 对比 ReAct / Reflexion / AutoGPT / BabyAGI，并与已有
mock 结果横向比较。真实运行有 5 美元硬预算；缺少依赖或 API key 时会安全跳过。

运行：
    cd exp-01-baseline
    python run.py
"""
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_shared"))

from agent_loop import parse_react_response, react_loop
from metrics import avg_steps, avg_tokens, success_rate

try:
    # 按要求不自动安装。缺失时由 check_openai_environment() 负责优雅降级。
    from openai import OpenAI
except ImportError:
    OpenAI = None


BASE_DIR = Path(__file__).resolve().parent
MODEL = "gpt-4o-mini"
MAX_BUDGET_USD = 5.0
MAX_COMPLETION_TOKENS = 300
RESULTS_REAL_PATH = BASE_DIR / "results_real.json"
MOCK_RESULTS_PATH = BASE_DIR / "results.json"

# gpt-4o-mini 标准文本价格（美元/百万 token）。如果 OpenAI 调价，只需更新此处。
INPUT_USD_PER_MILLION = 0.15
CACHED_INPUT_USD_PER_MILLION = 0.075
OUTPUT_USD_PER_MILLION = 0.60


# ==================== 任务定义 ====================
TASKS = [
    {
        "id": "weather-1",
        "query": "北京今天天气如何？",
        "expected_tool": "get_weather",
        "expected_answer_contains": "北京",
    },
    {
        "id": "calc-1",
        "query": "123 加 456 等于多少？",
        "expected_tool": "add",
        "expected_answer_contains": "579",
    },
    {
        "id": "search-1",
        "query": "搜索 arXiv 上关于 LLM Agent 的最新论文",
        "expected_tool": "search_arxiv",
        "expected_answer_contains": "arxiv",
    },
    {
        "id": "file-1",
        "query": "读 /etc/hostname 文件的内容",
        "expected_tool": "read_file",
        "expected_answer_contains": "",
    },
    {
        "id": "weather-2",
        "query": "上海明天会下雨吗？",
        "expected_tool": "get_weather",
        "expected_answer_contains": "上海",
    },
    {
        "id": "calc-2",
        "query": "1024 乘以 768 等于多少？",
        "expected_tool": "multiply",
        "expected_answer_contains": "786432",
    },
    {
        "id": "search-2",
        "query": "搜索 arXiv 上关于 Embodied AI 的最新论文",
        "expected_tool": "search_arxiv",
        "expected_answer_contains": "embodied",
    },
    {
        "id": "translate-1",
        "query": "把 'Hello World' 翻译成中文",
        "expected_tool": "translate",
        "expected_answer_contains": "你好",
    },
    {
        "id": "weather-3",
        "query": "广州后天天气",
        "expected_tool": "get_weather",
        "expected_answer_contains": "广州",
    },
    {
        "id": "calc-3",
        "query": "圆周率乘以 10 等于多少？",
        "expected_tool": "multiply",
        "expected_answer_contains": "31.4",
    },
]


# ==================== Mock 工具实现 ====================
def get_weather(city: str) -> Dict:
    return {"temp": 25, "rain": 30, "city": city, "unit": "celsius"}


def add(a: float, b: float) -> float:
    return a + b


def multiply(a: float, b: float) -> float:
    return a * b


def search_arxiv(query: str, max_results: int = 5) -> List[Dict]:
    return [{"title": f"Paper on {query}", "authors": ["Author A"], "year": 2026}]


def read_file(path: str) -> str:
    return f"<contents of {path}>"


def translate(text: str, target: str = "zh") -> str:
    return {"Hello World": "你好世界"}.get(text, text)


TOOLS = {
    "get_weather": get_weather,
    "add": add,
    "multiply": multiply,
    "search_arxiv": search_arxiv,
    "read_file": read_file,
    "translate": translate,
}


# ==================== 真实 OpenAI LLM ====================
class BudgetExceededError(RuntimeError):
    """下一次调用可能突破预算时抛出，阻止继续请求 OpenAI。"""


class ReActProtocolError(RuntimeError):
    """模型输出不符合 Thought/Action 协议时抛出。"""


@dataclass
class CostTracker:
    """按 OpenAI 返回的 usage 累计 token 和美元成本，并执行硬预算检查。"""

    max_cost_usd: float = MAX_BUDGET_USD
    total_cost_usd: float = 0.0
    prompt_tokens: int = 0
    cached_prompt_tokens: int = 0
    completion_tokens: int = 0
    stopped: bool = False
    stop_reason: Optional[str] = None

    def ensure_request_allowed(self, prompt: str) -> None:
        """用保守的 token 上界预检，确保下一次请求不会让成本越过预算。"""
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
        """记录一次非流式 Chat Completions 响应，并返回该次美元成本。"""
        if usage is None:
            self.stopped = True
            self.stop_reason = "OpenAI 响应未提供 usage，无法继续可靠执行 5 美元预算。"
            raise RuntimeError(self.stop_reason)

        prompt_tokens = int(getattr(usage, "prompt_tokens", 0) or 0)
        completion_tokens = int(getattr(usage, "completion_tokens", 0) or 0)
        details = getattr(usage, "prompt_tokens_details", None)
        cached_tokens = int(getattr(details, "cached_tokens", 0) or 0)
        uncached_tokens = max(0, prompt_tokens - cached_tokens)
        request_cost = (
            uncached_tokens * INPUT_USD_PER_MILLION
            + cached_tokens * CACHED_INPUT_USD_PER_MILLION
            + completion_tokens * OUTPUT_USD_PER_MILLION
        ) / 1_000_000

        self.prompt_tokens += prompt_tokens
        self.cached_prompt_tokens += cached_tokens
        self.completion_tokens += completion_tokens
        self.total_cost_usd += request_cost

        # 前置最坏成本检查是第一道保险；这里是根据真实 usage 的第二道保险。
        if self.total_cost_usd > self.max_cost_usd:
            self.stopped = True
            self.stop_reason = (
                f"累计花费 ${self.total_cost_usd:.6f} 已超过 ${self.max_cost_usd:.2f}，立即停止。"
            )
            raise BudgetExceededError(self.stop_reason)
        return request_cost


REACT_API_SYSTEM_PROMPT = """You are the LLM inside a ReAct agent loop.
Return exactly two lines and no markdown fences or extra prose:
Thought: <a brief reasoning summary>
Action: {"name": "<one available tool or finish>", "arguments": {<valid JSON arguments>}}
The Action value must be strict JSON with double-quoted keys and strings. Use an available tool when
needed. Only use finish after an observation provides enough information, and put the final answer in
arguments.answer. Always preserve this exact Thought/Action protocol."""


def make_openai_llm(client: Any, tracker: CostTracker) -> Callable[[str], str]:
    """构造供共享 react_loop 使用的 gpt-4o-mini 调用函数。"""

    def real_llm(prompt: str) -> str:
        # 把协议重复放入 system message 和预检 prompt，便于模型保持格式且成本可控。
        budget_prompt = f"{REACT_API_SYSTEM_PROMPT}\n{prompt}"
        tracker.ensure_request_allowed(budget_prompt)
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": REACT_API_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                max_tokens=MAX_COMPLETION_TOKENS,
            )
        except Exception as exc:
            # 认证、网络或配额错误都停止后续任务，避免重复失败请求。
            tracker.stopped = True
            tracker.stop_reason = f"OpenAI API 调用失败：{type(exc).__name__}: {exc}"
            raise RuntimeError(tracker.stop_reason) from exc

        tracker.record_usage(getattr(response, "usage", None))
        content = (response.choices[0].message.content or "").strip()
        thought, action = parse_react_response(content)
        if (
            not content.startswith("Thought:")
            or "Action:" not in content
            or not thought
            or action is None
        ):
            raise ReActProtocolError(
                "gpt-4o-mini 返回了无效 ReAct 格式；要求 Thought: ... 后接 Action: {JSON}。"
            )
        return content

    return real_llm


_ACTIVE_REAL_LLM: Optional[Callable[[str], str]] = None


def mock_llm_baseline(prompt: str) -> str:
    """调用真实 gpt-4o-mini。

    函数名为兼容原实验入口保留；main() 会在环境预检后注入真实 OpenAI 客户端。
    这里不再包含关键词匹配或 mock 响应逻辑。
    """
    if _ACTIVE_REAL_LLM is None:
        raise RuntimeError("真实 LLM 尚未初始化；请通过 main() 运行实验。")
    return _ACTIVE_REAL_LLM(prompt)


def check_openai_environment() -> Tuple[bool, str]:
    """检查可选依赖和密钥，返回可直接打印的可操作提示，不抛异常。"""
    missing = []
    if OpenAI is None:
        missing.append("Python 包 openai>=1.0（当前未安装或版本不兼容）")
    if not os.environ.get("OPENAI_API_KEY", "").strip():
        missing.append("环境变量 OPENAI_API_KEY")

    prerequisites = "真实模式需要：openai>=1.0，以及环境变量 OPENAI_API_KEY。"
    if missing:
        return False, f"{prerequisites}\n当前缺少：{'；'.join(missing)}。"
    return True, prerequisites


def attach_task_cost(result: Dict[str, Any], cost: float) -> Dict[str, Any]:
    """为单任务结果附加稳定的 cost 字段，同时保留 success/trajectory。"""
    result["cost"] = round(max(0.0, cost), 8)
    result.setdefault("success", False)
    result.setdefault("trajectory", [])
    return result


# ==================== 实验运行与评测 ====================
def _used_expected_tool(result: Dict[str, Any], expected_tool: str) -> bool:
    return any(
        step.get("action", {}).get("name") == expected_tool
        for step in result.get("trajectory", [])
        if isinstance(step, dict) and isinstance(step.get("action"), dict)
    )


def evaluate_task_result(task: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
    """统一真实结果的成功定义：完成循环、工具正确，且答案满足期望。"""
    answer = str(result.get("answer") or "")
    expected = task.get("expected_answer_contains", "")
    answer_correct = None if not expected else expected.casefold() in answer.casefold()
    loop_success = bool(result.get("success", False))
    tool_correct = _used_expected_tool(result, task["expected_tool"])

    result["loop_success"] = loop_success
    result["tool_correct"] = tool_correct
    result["answer_correct"] = answer_correct
    result["success"] = loop_success and tool_correct and answer_correct is not False
    return result


def _skipped_result(task: Dict[str, Any], reason: str) -> Dict[str, Any]:
    result = {
        "task_id": task["id"],
        "query": task["query"],
        "success": False,
        "answer": None,
        "trajectory": [{"step": 0, "error": reason, "note": "not executed"}],
        "steps": 0,
        "total_tokens": 0,
    }
    evaluate_task_result(task, result)
    return attach_task_cost(result, 0.0)


def _merge_reflexion_passes(first: Dict[str, Any], second: Dict[str, Any]) -> Dict[str, Any]:
    """保留 Reflexion 两轮的完整轨迹，避免只报告重试结果。"""
    first_trajectory = [dict(step, phase="first_pass") for step in first.get("trajectory", [])]
    second_trajectory = [
        dict(step, phase="reflection_retry") for step in second.get("trajectory", [])
    ]
    merged = dict(second)
    merged["trajectory"] = first_trajectory + second_trajectory
    merged["steps"] = first.get("steps", 0) + second.get("steps", 0)
    merged["total_tokens"] = first.get("total_tokens", 0) + second.get("total_tokens", 0)
    return merged


def run_experiment(
    llm: Callable[[str], str],
    label: str,
    tracker: CostTracker,
    max_steps: int = 5,
    query_prefix: str = "",
    query_suffix: str = "",
    reflexion: bool = False,
) -> List[Dict[str, Any]]:
    """用指定系统运行全部任务；预算或 API 失败后只记录 skipped，不再发请求。"""
    results: List[Dict[str, Any]] = []
    for task in TASKS:
        if tracker.stopped:
            results.append(_skipped_result(task, tracker.stop_reason or "实验已停止"))
            continue

        cost_before = tracker.total_cost_usd
        query = f"{query_prefix}{task['query']}{query_suffix}"
        result = react_loop(query=query, llm=llm, tools=TOOLS, max_steps=max_steps)
        evaluate_task_result(task, result)

        if reflexion and not result["success"] and not tracker.stopped:
            reflection = "上次行动或答案未通过评测。请重新理解任务并选择最匹配的工具。"
            retry = react_loop(
                query=f"{task['query']}（反思提示：{reflection}）",
                llm=llm,
                tools=TOOLS,
                max_steps=max_steps,
            )
            result = _merge_reflexion_passes(result, retry)
            evaluate_task_result(task, result)

        result["task_id"] = task["id"]
        result["query"] = task["query"]
        attach_task_cost(result, tracker.total_cost_usd - cost_before)
        results.append(result)

        error = next(
            (step.get("error") for step in reversed(result["trajectory"]) if step.get("error")),
            None,
        )
        suffix = f"；错误：{error}" if error else ""
        print(
            f"  [{label}] {task['id']}: success={result['success']}, "
            f"cost=${result['cost']:.6f}{suffix}"
        )
    return results


def run_all_real(tracker: CostTracker) -> Dict[str, List[Dict[str, Any]]]:
    """按原实验设置运行四种 Agent 基线，共享同一个 5 美元预算。"""
    systems = [
        ("ReAct", dict(max_steps=5)),
        ("Reflexion", dict(max_steps=5, reflexion=True)),
        ("AutoGPT", dict(max_steps=10, query_prefix="目标：")),
        ("BabyAGI", dict(max_steps=5, query_suffix="（请先查询相关数据再回答）")),
    ]
    output: Dict[str, List[Dict[str, Any]]] = {}
    for index, (name, options) in enumerate(systems, start=1):
        print(f"\n[{index}/4] 真实模型运行 {name}...")
        output[name] = run_experiment(mock_llm_baseline, name, tracker, **options)
        print(
            f"  {name} 完成：成功率 {success_rate(output[name]):.1f}%，"
            f"累计花费 ${tracker.total_cost_usd:.6f}"
        )
    return output


def _load_comparable_mock_results() -> Optional[Dict[str, List[Dict[str, Any]]]]:
    """读取已有 results.json，并按与真实结果相同的成功标准重新评测其副本。"""
    if not MOCK_RESULTS_PATH.exists():
        return None
    try:
        with MOCK_RESULTS_PATH.open("r", encoding="utf-8") as file:
            raw_results = json.load(file).get("results", {})
    except (OSError, json.JSONDecodeError) as exc:
        print(f"警告：无法读取 mock 结果 {MOCK_RESULTS_PATH.name}：{exc}")
        return None

    task_by_id = {task["id"]: task for task in TASKS}
    comparable: Dict[str, List[Dict[str, Any]]] = {}
    for system, records in raw_results.items():
        comparable[system] = []
        for record in records:
            copied = dict(record)
            task = task_by_id.get(copied.get("task_id"))
            if task:
                evaluate_task_result(task, copied)
            comparable[system].append(copied)
    return comparable


def print_mock_real_comparison(real_results: Dict[str, List[Dict[str, Any]]]) -> None:
    """在终端打印 mock vs real 汇总表。"""
    mock_results = _load_comparable_mock_results()
    print("\n" + "=" * 84)
    print("Mock vs Real（gpt-4o-mini）")
    print("=" * 84)
    print("| 系统 | Mock 成功率 | Real 成功率 | Mock 平均步数 | Real 平均步数 | Real 成本 |")
    print("|---|---:|---:|---:|---:|---:|")
    for name in ("ReAct", "Reflexion", "AutoGPT", "BabyAGI"):
        mock = mock_results.get(name, []) if mock_results else []
        real = real_results.get(name, [])
        mock_rate = f"{success_rate(mock):.1f}%" if mock else "N/A"
        mock_steps = f"{avg_steps(mock):.1f}" if mock else "N/A"
        real_cost = sum(float(result.get("cost", 0.0)) for result in real)
        print(
            f"| {name} | {mock_rate} | {success_rate(real):.1f}% | {mock_steps} | "
            f"{avg_steps(real):.1f} | ${real_cost:.6f} |"
        )


def save_real_results(
    real_results: Dict[str, List[Dict[str, Any]]], tracker: CostTracker, elapsed: float
) -> None:
    """保存真实运行元数据和逐任务 cost/success/trajectory。"""
    status = "stopped" if tracker.stopped else "completed"
    if tracker.stop_reason and "预算" in tracker.stop_reason:
        status = "budget_exceeded"
    output = {
        "experiment": "exp-01-baseline",
        "mode": "real",
        "model": MODEL,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "stop_reason": tracker.stop_reason,
        "max_budget_usd": tracker.max_cost_usd,
        "total_cost_usd": round(tracker.total_cost_usd, 8),
        "elapsed_seconds": round(elapsed, 3),
        "usage": {
            "prompt_tokens": tracker.prompt_tokens,
            "cached_prompt_tokens": tracker.cached_prompt_tokens,
            "completion_tokens": tracker.completion_tokens,
        },
        "pricing_usd_per_million_tokens": {
            "input": INPUT_USD_PER_MILLION,
            "cached_input": CACHED_INPUT_USD_PER_MILLION,
            "output": OUTPUT_USD_PER_MILLION,
        },
        "results": real_results,
    }
    with RESULTS_REAL_PATH.open("w", encoding="utf-8") as file:
        json.dump(output, file, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到 {RESULTS_REAL_PATH.name}")


def main() -> None:
    print("=" * 60)
    print(f"实验 1：基线对比（真实模型 {MODEL}）")
    print(f"硬预算上限：${MAX_BUDGET_USD:.2f}")
    print("=" * 60)

    environment_ok, message = check_openai_environment()
    if not environment_ok:
        print("\n[已安全跳过] 无法运行真实 OpenAI 实验。")
        print(message)
        print("PowerShell 示例：$env:OPENAI_API_KEY = 'sk-...'；然后重新运行 python run.py")
        print(f"未创建 {RESULTS_REAL_PATH.name}，现有 mock 结果未被修改。")
        return

    global _ACTIVE_REAL_LLM
    tracker = CostTracker(max_cost_usd=MAX_BUDGET_USD)
    try:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"], timeout=60.0, max_retries=2)
        _ACTIVE_REAL_LLM = make_openai_llm(client, tracker)
    except Exception as exc:
        print(f"\n[已安全跳过] OpenAI 客户端初始化失败：{type(exc).__name__}: {exc}")
        print(message)
        return

    started = time.time()
    real_results = run_all_real(tracker)
    elapsed = time.time() - started
    save_real_results(real_results, tracker, elapsed)
    print_mock_real_comparison(real_results)
    print(f"\n总花费：${tracker.total_cost_usd:.6f} / ${tracker.max_cost_usd:.2f}")
    if tracker.stop_reason:
        print(f"停止原因：{tracker.stop_reason}")


if __name__ == "__main__":
    main()
