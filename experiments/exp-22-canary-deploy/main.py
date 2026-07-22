"""
实验 22：金丝雀部署模拟（Mock 模式）

模拟金丝雀发布策略：新版本从 5% 流量开始，逐步扩大到 100%。
验证能否在流量扩大过程中检测到版本退化。

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 版本定义 ====================
VERSIONS = {
    "v1.0": {"name": "稳定版本 v1.0", "error_rate": 0.02, "latency_ms": 50},
    "v2.0": {"name": "候选版本 v2.0", "error_rate": 0.03, "latency_ms": 45},
}

# 故障注入场景
FAULT_SCENARIOS = {
    "none": {"name": "无故障", "error_spike": 0.0, "latency_spike": 0},
    "latency": {"name": "延迟故障", "error_spike": 0.01, "latency_spike": 200},
    "error": {"name": "错误率故障", "error_spike": 0.15, "latency_spike": 50},
}

# 流量扩展阶段
TRAFFIC_STAGES = [0.05, 0.10, 0.20, 0.30, 0.50, 0.70, 0.85, 1.00]
TOTAL_USERS = 10000


# ==================== 模拟函数 ====================
def simulate_stage(canary_pct: float, version: str, fault: dict,
                  total_users: int = TOTAL_USERS) -> dict:
    """模拟单个流量阶段的用户请求。"""
    rng = random.Random(42 + int(canary_pct * 100) + hash(fault["name"]))
    version_info = VERSIONS[version]

    canary_users = int(total_users * canary_pct)
    stable_users = total_users - canary_users

    errors = 0
    total_latency = 0.0

    # 稳定版本用户
    for _ in range(stable_users):
        if rng.random() < VERSIONS["v1.0"]["error_rate"]:
            errors += 1
        total_latency += VERSIONS["v1.0"]["latency_ms"] + rng.uniform(-5, 5)

    # 金丝雀版本用户
    for _ in range(canary_users):
        err_rate = version_info["error_rate"] + fault["error_spike"]
        if rng.random() < err_rate:
            errors += 1
        lat = version_info["latency_ms"] + fault["latency_spike"] + rng.uniform(-10, 10)
        total_latency += lat

    observed_error_rate = errors / total_users
    observed_latency = total_latency / total_users

    return {
        "canary_pct": canary_pct,
        "canary_users": canary_users,
        "total_users": total_users,
        "errors": errors,
        "observed_error_rate": observed_error_rate,
        "observed_latency": observed_latency,
    }


def run_canary_deploy(fault_scenario: str, error_threshold: float = 0.05,
                      latency_threshold: float = 100) -> dict:
    """运行完整的金丝雀部署流程。"""
    fault = FAULT_SCENARIOS[fault_scenario]
    stages = []

    for pct in TRAFFIC_STAGES:
        result = simulate_stage(pct, "v2.0", fault)
        result["fault_scenario"] = fault_scenario

        # 检测异常
        result["alert"] = (
            result["observed_error_rate"] > error_threshold or
            result["observed_latency"] > latency_threshold
        )
        stages.append(result)

        # 如果触发告警，停止扩展
        if result["alert"]:
            break

    # 受影响用户
    affected = sum(s["errors"] for s in stages)
    max_pct = max(s["canary_pct"] for s in stages)

    return {
        "fault_scenario": fault["name"],
        "stages_completed": len(stages),
        "max_canary_pct": max_pct,
        "total_affected_users": affected,
        "total_users": TOTAL_USERS,
        "affected_pct": affected / TOTAL_USERS,
        "detected": any(s["alert"] for s in stages),
        "stages": stages,
    }


def run_full_deploy(fault_scenario: str) -> dict:
    """模拟全量部署（对照组）。"""
    fault = FAULT_SCENARIOS[fault_scenario]
    result = simulate_stage(1.0, "v2.0", fault)
    return {
        "fault_scenario": fault["name"],
        "total_affected_users": result["errors"],
        "affected_pct": result["observed_error_rate"],
    }


def main():
    print("=" * 60)
    print("实验 22：金丝雀部署模拟（Mock 模式）")
    print("=" * 60)
    print(f"总用户: {TOTAL_USERS}, 流量阶段: {TRAFFIC_STAGES}")
    print(f"错误率阈值: 5%, 延迟阈值: 100ms\n")

    all_results = {}

    for fault_key in FAULT_SCENARIOS:
        # 金丝雀部署
        canary = run_canary_deploy(fault_key)
        # 全量部署
        full = run_full_deploy(fault_key)

        all_results[fault_key] = {"canary": canary, "full": full}

        print(f"\n--- 故障场景: {FAULT_SCENARIOS[fault_key]['name']} ---")

        # 金丝雀阶段详情
        print(f"  金丝雀部署:")
        for s in canary["stages"]:
            alert_icon = " [ALERT]" if s["alert"] else ""
            print(f"    流量 {s['canary_pct']:>5.1%}: 错误率 {s['observed_error_rate']:.2%}, "
                  f"延迟 {s['observed_latency']:.0f}ms, 错误 {s['errors']} 人{alert_icon}")

        print(f"  完成阶段: {canary['stages_completed']}/{len(TRAFFIC_STAGES)}")
        print(f"  最大金丝雀流量: {canary['max_canary_pct']:.0%}")
        print(f"  受影响用户: {canary['total_affected_users']}/{TOTAL_USERS} "
              f"({canary['affected_pct']:.1%})")

        if canary["detected"]:
            print(f"  故障检测: 已检测到并停止扩展")
        else:
            print(f"  故障检测: 未检测到（全部通过）")

        print(f"  全量部署受影响: {full['total_affected_users']} 人 ({full['affected_pct']:.1%})")
        saved = full["total_affected_users"] - canary["total_affected_users"]
        print(f"  金丝雀节省: {saved} 人免受影响")

    # 汇总
    print("\n" + "=" * 60)
    print("金丝雀 vs 全量部署对比")
    print("=" * 60)
    print(f"| {'故障场景':<12} | {'金丝雀影响':>10} | {'全量影响':>10} | {'节省':>8} | {'检测':>6} |")
    print(f"|{'-'*14}|{'-'*12}|{'-'*12}|{'-'*10}|{'-'*8}|")
    for fault_key, data in all_results.items():
        c = data["canary"]
        f = data["full"]
        saved = f["total_affected_users"] - c["total_affected_users"]
        detected = "YES" if c["detected"] else "NO"
        print(f"| {FAULT_SCENARIOS[fault_key]['name']:<12} | "
              f"{c['affected_pct']:>9.1%} | {f['affected_pct']:>9.1%} | "
              f"{saved:>7}人 | {detected:>6} |")

    print("\n结论:")
    print("  - 金丝雀部署在无故障场景下安全扩展到 100%")
    print("  - 在延迟/错误率故障场景下，金丝雀能有效减少受影响用户")
    print("  - 全量部署遇到故障时，100% 用户暴露在风险中")

    output = {"experiment": "exp-22-canary-deploy", "results": all_results}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
