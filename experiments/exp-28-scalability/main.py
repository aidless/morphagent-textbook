"""
实验 28：规模化压力测试（Mock 模式）

测试 MorphAgent 在不同并发量级下的性能表现。
识别系统瓶颈和最大承载能力。

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 负载定义 ====================
LOAD_LEVELS = [10, 50, 100, 500, 1000]

# 系统容量参数
SYSTEM_CAPACITY = {
    "max_concurrent": 100,       # 最大并发处理能力
    "base_latency_ms": 50,       # 基础延迟
    "queue_coefficient": 0.5,    # 排队延迟系数
    "timeout_ms": 5000,           # 超时时间
    "degradation_threshold": 200,# 降级阈值（并发数）
}


def percentile(data: list[float], p: float) -> float:
    """计算百分位数。"""
    if not data:
        return 0.0
    sorted_data = sorted(data)
    idx = int(len(sorted_data) * p / 100)
    return sorted_data[min(idx, len(sorted_data) - 1)]


def simulate_load(concurrent: int) -> dict:
    """模拟一个并发级别的请求处理。"""
    rng = random.Random(42 + concurrent)
    capacity = SYSTEM_CAPACITY
    results = []

    for req_id in range(concurrent):
        # 计算处理延迟
        base = capacity["base_latency_ms"]

        if concurrent <= capacity["max_concurrent"]:
            # 正常处理
            processing_latency = base + rng.gauss(0, base * 0.2)
            queue_latency = concurrent * capacity["queue_coefficient"] * rng.uniform(0.5, 1.5)
        else:
            # 超容量：需要排队
            overflow = concurrent - capacity["max_concurrent"]
            processing_latency = base * (1 + overflow / capacity["max_concurrent"])
            queue_latency = capacity["max_concurrent"] * capacity["queue_coefficient"] + overflow * 3

        total_latency = max(1, processing_latency + queue_latency + rng.uniform(0, 20))

        # 超时判定
        timed_out = total_latency > capacity["timeout_ms"]

        # 成功判定
        if timed_out:
            success = False
        elif concurrent > capacity["degradation_threshold"]:
            # 高负载降级
            success = rng.random() < max(0.7, 1.0 - (concurrent - capacity["degradation_threshold"]) / 1000)
        else:
            success = rng.random() < 0.98

        # 资源使用
        cpu = min(100, 20 + concurrent * 0.06 + rng.uniform(0, 10))
        memory = min(100, 30 + concurrent * 0.04 + rng.uniform(0, 5))

        results.append({
            "req_id": req_id,
            "latency_ms": total_latency,
            "success": success,
            "timed_out": timed_out,
        })

    # 统计
    latencies = [r["latency_ms"] for r in results]
    successes = sum(1 for r in results if r["success"])
    timeouts = sum(1 for r in results if r["timed_out"])

    return {
        "concurrent": concurrent,
        "total_requests": concurrent,
        "success_count": successes,
        "success_rate": successes / concurrent,
        "timeout_count": timeouts,
        "timeout_rate": timeouts / concurrent,
        "p50_latency": percentile(latencies, 50),
        "p95_latency": percentile(latencies, 95),
        "p99_latency": percentile(latencies, 99),
        "avg_latency": statistics.mean(latencies),
        "cpu_usage": min(100, 20 + concurrent * 0.06),
        "memory_usage": min(100, 30 + concurrent * 0.04),
    }


def main():
    print("=" * 60)
    print("实验 28：规模化压力测试（Mock 模式）")
    print("=" * 60)
    print(f"系统容量: 最大并发 {SYSTEM_CAPACITY['max_concurrent']}, "
          f"超时 {SYSTEM_CAPACITY['timeout_ms']}ms\n")

    all_results = []

    for concurrent in LOAD_LEVELS:
        result = simulate_load(concurrent)
        all_results.append(result)

        status = "OK" if concurrent <= SYSTEM_CAPACITY["max_concurrent"] else "OVERLOADED"
        print(f"--- 并发 {concurrent:>5} [{status}] ---")
        print(f"  成功率: {result['success_rate']:.1%} "
              f"(超时: {result['timeout_rate']:.1%})")
        print(f"  延迟: P50={result['p50_latency']:.0f}ms, "
              f"P95={result['p95_latency']:.0f}ms, "
              f"P99={result['p99_latency']:.0f}ms")
        print(f"  资源: CPU={result['cpu_usage']:.0f}%, "
              f"内存={result['memory_usage']:.0f}%")

    # 汇总表
    print("\n" + "=" * 60)
    print("性能汇总")
    print("=" * 60)
    print(f"| {'并发':>6} | {'成功率':>8} | {'超时率':>8} | {'P50':>8} | "
          f"{'P95':>8} | {'P99':>8} | {'CPU':>6} | {'内存':>6} |")
    print(f"|{'-'*8}|{'-'*10}|{'-'*10}|{'-'*10}|{'-'*10}|{'-'*10}|{'-'*8}|{'-'*8}|")
    for r in all_results:
        print(f"| {r['concurrent']:>6} | {r['success_rate']:>7.1%} | "
              f"{r['timeout_rate']:>7.1%} | {r['p50_latency']:>7.0f}ms | "
              f"{r['p95_latency']:>7.0f}ms | {r['p99_latency']:>7.0f}ms | "
              f"{r['cpu_usage']:>5.0f}% | {r['memory_usage']:>5.0f}% |")

    # 瓶颈分析
    print("\n瓶颈分析:")
    baseline = all_results[0]
    peak = all_results[-1]
    latency_degradation = peak["p95_latency"] / baseline["p95_latency"]
    success_degradation = peak["success_rate"] - baseline["success_rate"]
    print(f"  P95 延迟增长: {latency_degradation:.1f}x ({baseline['p95_latency']:.0f} -> {peak['p95_latency']:.0f}ms)")
    print(f"  成功率下降: {success_degradation:+.1%}")
    print(f"  最大并发容量: ~{SYSTEM_CAPACITY['max_concurrent']} (超过后显著降级)")
    print(f"  建议限流阈值: {SYSTEM_CAPACITY['degradation_threshold']} 并发")

    output = {"experiment": "exp-28-scalability", "results": all_results,
              "system_capacity": SYSTEM_CAPACITY}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
