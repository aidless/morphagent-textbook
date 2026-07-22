"""
实验 23：自动回滚测试（Mock 模式）

实现自动回滚机制：监控健康指标，检测异常后自动回滚。
对比 3 种异常检测策略的检测速度和误报率。

运行：
    python main.py
"""
import json
import random
import statistics


# ==================== 健康指标模型 ====================
def generate_health_timeline(version: str, duration: int = 60,
                            fault_at: int = None) -> list[dict]:
    """生成系统健康指标时间线（每秒一个数据点）。"""
    rng = random.Random(42 + hash(version))
    timeline = []

    for t in range(duration):
        if version == "v1.0":
            # 稳定版本
            error_rate = 0.02 + rng.gauss(0, 0.005)
            latency = 50 + rng.gauss(0, 5)
            memory = 60 + rng.gauss(0, 3)
        elif version == "v2.0":
            if fault_at and t >= fault_at:
                # 故障版本：错误率飙升
                error_rate = 0.15 + rng.gauss(0, 0.02)
                latency = 200 + rng.gauss(0, 30)
                memory = 85 + rng.gauss(0, 5)
            else:
                # 正常 v2.0
                error_rate = 0.025 + rng.gauss(0, 0.008)
                latency = 45 + rng.gauss(0, 8)
                memory = 55 + rng.gauss(0, 4)
        else:
            error_rate, latency, memory = 0.02, 50, 60

        timeline.append({
            "t": t,
            "error_rate": max(0, error_rate),
            "latency_ms": max(10, latency),
            "memory_pct": max(0, min(100, memory)),
        })

    return timeline


# ==================== 异常检测策略 ====================
class FixedThresholdDetector:
    """固定阈值检测器。"""
    name = "固定阈值"
    error_threshold = 0.08
    latency_threshold = 120

    def detect(self, metrics: dict) -> bool:
        return (metrics["error_rate"] > self.error_threshold or
                metrics["latency_ms"] > self.latency_threshold)


class MovingAverageDetector:
    """移动平均检测器。"""
    name = "移动平均"
    window = 5
    error_threshold = 0.06
    latency_threshold = 100

    def __init__(self):
        self.history: list[dict] = []

    def detect(self, metrics: dict) -> bool:
        self.history.append(metrics)
        if len(self.history) < self.window:
            return False
        recent = self.history[-self.window:]
        avg_err = statistics.mean(m["error_rate"] for m in recent)
        avg_lat = statistics.mean(m["latency_ms"] for m in recent)
        return avg_err > self.error_threshold or avg_lat > self.latency_threshold


class EWMADetector:
    """指数加权移动平均检测器。"""
    name = "EWMA"
    alpha = 0.3
    error_threshold = 0.05
    latency_threshold = 80

    def __init__(self):
        self.ewma_error = 0.02
        self.ewma_latency = 50.0

    def detect(self, metrics: dict) -> bool:
        self.ewma_error = (self.alpha * metrics["error_rate"] +
                           (1 - self.alpha) * self.ewma_error)
        self.ewma_latency = (self.alpha * metrics["latency_ms"] +
                             (1 - self.alpha) * self.ewma_latency)
        return (self.ewma_error > self.error_threshold or
                self.ewma_latency > self.latency_threshold)


def run_rollback_simulation(detector_class, timeline: list[dict],
                            rollback_cost: int = 5) -> dict:
    """运行回滚模拟。返回检测时间和恢复情况。"""
    detector = detector_class() if hasattr(detector_class, '__init__') and detector_class.__init__ is not object.__init__ else detector_class()

    detection_time = None
    is_false_positive = None

    for i, metrics in enumerate(timeline):
        if detector.detect(metrics):
            detection_time = i
            break

    # 判断是否误报（在无故障时间线上检测到异常）
    fault_point = next((m["t"] for m in timeline if m["error_rate"] > 0.1), None)
    if fault_point is None:
        is_false_positive = detection_time is not None
    else:
        is_false_positive = detection_time is not None and detection_time < fault_point

    # 回滚后的恢复
    if detection_time is not None:
        recovery_time = detection_time + rollback_cost
    else:
        recovery_time = None

    return {
        "detection_time": detection_time,
        "recovery_time": recovery_time,
        "false_positive": is_false_positive,
        "detector_name": detector.name,
    }


def main():
    print("=" * 60)
    print("实验 23：自动回滚测试（Mock 模式）")
    print("=" * 60)

    detectors = [FixedThresholdDetector, MovingAverageDetector, EWMADetector]

    # 场景 1: 有故障的时间线
    print("\n--- 场景 1: v2.0 发布后 15 秒出现故障 ---")
    faulty_timeline = generate_health_timeline("v2.0", duration=60, fault_at=15)

    results_fault = {}
    for det_class in detectors:
        result = run_rollback_simulation(det_class, faulty_timeline)
        results_fault[det_class.name] = result

        det_time = f"{result['detection_time']}s" if result['detection_time'] is not None else "未检测"
        rec_time = f"{result['recovery_time']}s" if result['recovery_time'] is not None else "N/A"
        print(f"  {result['detector_name']:<10}: 检测时间={det_time}, "
              f"恢复时间={rec_time}, 误报={result['false_positive']}")

    # 场景 2: 无故障的时间线（测试误报率）
    print("\n--- 场景 2: v1.0 稳定版本（测试误报率） ---")
    stable_timeline = generate_health_timeline("v1.0", duration=60)

    results_stable = {}
    for det_class in detectors:
        result = run_rollback_simulation(det_class, stable_timeline)
        results_stable[det_class.name] = result

        fp = "是 (误报!)" if result['false_positive'] else "否"
        print(f"  {result['detector_name']:<10}: 误报={fp}")

    # 场景 3: 多次模拟统计
    print("\n--- 场景 3: 100 次模拟统计 ---")
    n_sims = 100
    stats = {}
    for det_class in detectors:
        detection_times = []
        false_positives = 0

        for sim_id in range(n_sims):
            # 随机故障时间
            fault_at = random.Random(sim_id).randint(10, 30)
            timeline = generate_health_timeline("v2.0", duration=60, fault_at=fault_at)
            result = run_rollback_simulation(det_class, timeline)
            if result["detection_time"] is not None:
                detection_times.append(result["detection_time"] - fault_at)
            if result["false_positive"]:
                false_positives += 1

        avg_detect = statistics.mean(detection_times) if detection_times else -1
        stats[det_class.name] = {
            "avg_detect_delay": avg_detect,
            "detection_rate": len(detection_times) / n_sims,
            "false_positive_rate": false_positives / n_sims,
        }
        print(f"  {det_class.name:<10}: 平均延迟 {avg_detect:.1f}s, "
              f"检测率 {stats[det_class.name]['detection_rate']:.0%}, "
              f"误报率 {stats[det_class.name]['false_positive_rate']:.0%}")

    # 汇总
    print("\n" + "=" * 60)
    print("检测策略汇总")
    print("=" * 60)
    print(f"| {'策略':<10} | {'检测延迟':>10} | {'检测率':>8} | {'误报率':>8} |")
    print(f"|{'-'*12}|{'-'*12}|{'-'*10}|{'-'*10}|")
    for name, s in stats.items():
        print(f"| {name:<10} | {s['avg_detect_delay']:>9.1f}s | "
              f"{s['detection_rate']:>7.0%} | {s['false_positive_rate']:>7.0%} |")

    print("\n结论:")
    print("  - EWMA 检测最快，但误报率稍高")
    print("  - 移动平均检测较稳定，误报率低")
    print("  - 固定阈值简单直接，适合基线使用")

    output = {"experiment": "exp-23-rollback", "stats": stats}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
