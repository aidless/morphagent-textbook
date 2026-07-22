"""
评测指标集合。

供实验 1-4 共用。
所有实验的指标计算都应通过这个模块，便于横向对比。
"""
from typing import List, Dict, Any
import statistics


def success_rate(results: List[Dict]) -> float:
    """任务成功率（百分比）。"""
    if not results:
        return 0.0
    return 100.0 * sum(r.get("success", False) for r in results) / len(results)


def avg_steps(results: List[Dict]) -> float:
    """平均完成步数。"""
    if not results:
        return 0.0
    return statistics.mean(r.get("steps", 0) for r in results)


def avg_tokens(results: List[Dict]) -> float:
    """平均 token 消耗。"""
    if not results:
        return 0.0
    return statistics.mean(r.get("total_tokens", 0) for r in results)


def recovery_count(results: List[Dict]) -> float:
    """平均错误恢复次数。"""
    if not results:
        return 0.0
    counts = []
    for r in results:
        traj = r.get("trajectory", [])
        recoveries = sum(1 for step in traj 
                          if "Observation" in str(step) and "Error" in str(step))
        counts.append(recoveries)
    return statistics.mean(counts) if counts else 0.0


def action_consistency(trajectories: List[Dict], optimal_actions: List[str]) -> float:
    """行动合理性得分：LLM 的行动与最优行动的一致率。"""
    if not trajectories or not optimal_actions:
        return 0.0
    correct = 0
    for traj, opt_action in zip(trajectories, optimal_actions):
        actions = [t.get("action", {}).get("name") for t in traj if t.get("action")]
        if opt_action in actions:
            correct += 1
    return 100.0 * correct / len(trajectories)


def tool_call_accuracy(predicted_calls: List[Dict], expected_calls: List[Dict]) -> float:
    """工具调用准确率：参数完全匹配的比例。"""
    if not expected_calls:
        return 0.0
    correct = 0
    for pred, exp in zip(predicted_calls, expected_calls):
        if (pred.get("name") == exp.get("name") and
            pred.get("arguments") == exp.get("arguments")):
            correct += 1
    return 100.0 * correct / len(expected_calls)


def first_success_step(trajectory: List[Dict]) -> int:
    """首次成功步数（用于首次成功率分析）。"""
    for step in trajectory:
        if step.get("action", {}).get("name") == "finish":
            return step.get("step", -1) + 1
    return -1


def prompt_drift_score(prompts_history: List[str]) -> float:
    """Prompt 漂移分数：连续两个 prompt 的编辑距离 / 平均长度。

    用于评估自修改 prompt 是否"稳定"——稳定系统漂移分数应该随时间收敛。
    """
    if len(prompts_history) < 2:
        return 0.0
    drifts = []
    for i in range(1, len(prompts_history)):
        prev, curr = prompts_history[i-1], prompts_history[i]
        # 简化的编辑距离：Jaccard 距离
        prev_words = set(prev.split())
        curr_words = set(curr.split())
        if not prev_words and not curr_words:
            continue
        jaccard = 1.0 - len(prev_words & curr_words) / len(prev_words | curr_words)
        drifts.append(jaccard)
    return statistics.mean(drifts) if drifts else 0.0


def summary_table(results: List[Dict], groupby: str = None) -> str:
    """生成 Markdown 格式的评测结果表。"""
    if not results:
        return "No results."
    
    lines = ["| Metric | Value |", "|---|---|"]
    lines.append(f"| 总任务数 | {len(results)} |")
    lines.append(f"| 成功率 | {success_rate(results):.1f}% |")
    lines.append(f"| 平均步数 | {avg_steps(results):.1f} |")
    lines.append(f"| 平均 token | {avg_tokens(results):.0f} |")
    lines.append(f"| 平均错误恢复 | {recovery_count(results):.1f} |")
    return "\n".join(lines)


if __name__ == "__main__":
    # 测试
    sample_results = [
        {"success": True, "steps": 3, "total_tokens": 100, "trajectory": []},
        {"success": False, "steps": 10, "total_tokens": 500, "trajectory": []},
        {"success": True, "steps": 5, "total_tokens": 200, "trajectory": []},
    ]
    print(summary_table(sample_results))
