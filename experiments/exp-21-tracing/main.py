"""
实验 21：OpenTelemetry 链路追踪（Mock 模式）

模拟分布式链路追踪，分析 Agent 请求在子系统间的调用链。
识别慢 span、错误 span 和关键路径。

运行：
    python main.py
"""
import json
import random
import statistics
import time


# ==================== Span 模型 ====================
class Span:
    """模拟 OpenTelemetry Span。"""

    def __init__(self, name: str, service: str, parent_id: str = None,
                 duration_ms: float = None, status: str = "ok", error_msg: str = None):
        self.span_id = f"span-{random.randint(10000, 99999)}"
        self.trace_id = "trace-00001"
        self.name = name
        self.service = service
        self.parent_id = parent_id
        self.duration_ms = duration_ms or random.uniform(5, 100)
        self.status = status
        self.error_msg = error_msg
        self.children: list[Span] = []
        self.start_time = time.time()
        self.attributes = {}

    def add_child(self, child: "Span"):
        child.parent_id = self.span_id
        child.trace_id = self.trace_id
        self.children.append(child)

    def total_duration(self) -> float:
        """计算该 span（含子 span）的总耗时。"""
        if not self.children:
            return self.duration_ms
        children_max = max(c.total_duration() for c in self.children)
        return self.duration_ms + children_max

    def critical_path(self) -> list[str]:
        """获取关键路径（最长路径）。"""
        path = [self.name]
        if self.children:
            slowest = max(self.children, key=lambda c: c.total_duration())
            path.extend(slowest.critical_path())
        return path

    def find_errors(self) -> list["Span"]:
        """递归查找所有错误 span。"""
        errors = []
        if self.status == "error":
            errors.append(self)
        for c in self.children:
            errors.extend(c.find_errors())
        return errors

    def find_slow_spans(self, threshold_ms: float = 50) -> list["Span"]:
        """递归查找所有慢 span。"""
        slow = []
        if self.duration_ms > threshold_ms:
            slow.append(self)
        for c in self.children:
            slow.extend(c.find_slow_spans(threshold_ms))
        return slow

    def all_spans(self) -> list["Span"]:
        """收集所有 span。"""
        spans = [self]
        for c in self.children:
            spans.extend(c.all_spans())
        return spans

    def to_dict(self) -> dict:
        return {
            "span_id": self.span_id, "name": self.name,
            "service": self.service, "duration_ms": round(self.duration_ms, 2),
            "status": self.status,
            "children": [c.to_dict() for c in self.children],
        }


# ==================== 生成模拟调用链 ====================
def generate_trace(request_type: str) -> Span:
    """根据请求类型生成模拟调用链。"""
    rng = random.Random(42 + hash(request_type))

    root = Span("HTTP Request", "API Gateway", duration_ms=rng.uniform(2, 5))

    # Agent 主处理
    agent = Span("Agent Process", "MorphAgent", duration_ms=rng.uniform(10, 20))
    root.add_child(agent)

    if request_type == "query":
        # 感知层
        perception = Span("Parse Input", "Perception", duration_ms=rng.uniform(5, 15))
        agent.add_child(perception)

        # 记忆检索
        memory = Span("Memory Recall", "Memory", duration_ms=rng.uniform(20, 80))
        agent.add_child(memory)

        # 决策
        decision = Span("Decision Making", "Decision", duration_ms=rng.uniform(15, 30))
        agent.add_child(decision)

        # 工具调用
        tool = Span("Tool Execution", "Execution", duration_ms=rng.uniform(30, 120))
        agent.add_child(tool)

        # 模拟偶尔出错
        if rng.random() < 0.2:
            tool.status = "error"
            tool.error_msg = "Tool timeout"

    elif request_type == "chat":
        perception = Span("Parse Message", "Perception", duration_ms=rng.uniform(5, 10))
        agent.add_child(perception)

        memory = Span("Context Lookup", "Memory", duration_ms=rng.uniform(10, 40))
        agent.add_child(memory)

        gen = Span("Response Generation", "LLM", duration_ms=rng.uniform(50, 200))
        agent.add_child(gen)

        if rng.random() < 0.15:
            gen.status = "error"
            gen.error_msg = "LLM rate limit"

    elif request_type == "tool_call":
        decision = Span("Plan Execution", "Decision", duration_ms=rng.uniform(10, 25))
        agent.add_child(decision)

        # 多工具并行调用
        for i in range(3):
            tool = Span(f"Tool Call #{i+1}", "Execution",
                       duration_ms=rng.uniform(20, 150))
            decision.add_child(tool)
            if i == 1 and rng.random() < 0.25:
                tool.status = "error"
                tool.error_msg = "API error"

    return root


def analyze_trace(trace: Span) -> dict:
    """分析一条完整链路。"""
    all_spans = trace.all_spans()
    errors = trace.find_errors()
    slow = trace.find_slow_spans(threshold_ms=50)
    critical = trace.critical_path()

    return {
        "total_spans": len(all_spans),
        "total_duration_ms": trace.total_duration(),
        "critical_path": critical,
        "critical_path_duration": sum(
            s.duration_ms for s in all_spans if s.name in critical
        ),
        "error_count": len(errors),
        "errors": [{"name": e.name, "msg": e.error_msg} for e in errors],
        "slow_count": len(slow),
        "slow_spans": [{"name": s.name, "duration_ms": round(s.duration_ms, 2)}
                       for s in slow],
    }


def main():
    print("=" * 60)
    print("实验 21：OpenTelemetry 链路追踪（Mock 模式）")
    print("=" * 60)

    request_types = ["query", "chat", "tool_call"]
    all_analyses = {}

    for req_type in request_types:
        trace = generate_trace(req_type)
        analysis = analyze_trace(trace)

        print(f"\n--- 请求类型: {req_type} ---")
        print(f"  Span 总数: {analysis['total_spans']}")
        print(f"  总耗时: {analysis['total_duration_ms']:.1f}ms")
        print(f"  关键路径: {' -> '.join(analysis['critical_path'])}")

        print(f"  慢 Span (>50ms):")
        for s in analysis["slow_spans"]:
            print(f"    - {s['name']}: {s['duration_ms']:.1f}ms")

        if analysis["errors"]:
            print(f"  错误 Span:")
            for e in analysis["errors"]:
                print(f"    - {e['name']}: {e['msg']}")
        else:
            print(f"  错误 Span: 无")

        # 打印调用树
        print(f"  调用树:")
        _print_tree(trace, indent=2)
        all_analyses[req_type] = analysis

    # 汇总
    print("\n" + "=" * 60)
    print("链路追踪汇总")
    print("=" * 60)
    print(f"| {'请求类型':<12} | {'Span数':>8} | {'总耗时':>10} | {'错误':>6} | {'慢Span':>8} |")
    print(f"|{'-'*14}|{'-'*10}|{'-'*12}|{'-'*8}|{'-'*10}|")
    for req_type, analysis in all_analyses.items():
        print(f"| {req_type:<12} | {analysis['total_spans']:>8} | "
              f"{analysis['total_duration_ms']:>9.1f}ms | {analysis['error_count']:>6} | "
              f"{analysis['slow_count']:>8} |")

    total_errors = sum(a["error_count"] for a in all_analyses.values())
    total_slow = sum(a["slow_count"] for a in all_analyses.values())
    print(f"\n总计: {total_errors} 个错误, {total_slow} 个慢 Span")

    output = {"experiment": "exp-21-tracing", "analyses": all_analyses}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("结果已保存到 results.json")


def _print_tree(span: Span, indent: int = 0):
    """递归打印调用树。"""
    prefix = "  " * indent
    status_icon = "[OK]" if span.status == "ok" else "[ERR]"
    print(f"{prefix}{status_icon} {span.name} ({span.duration_ms:.1f}ms) [{span.service}]")
    for child in span.children:
        _print_tree(child, indent + 1)


if __name__ == "__main__":
    main()
