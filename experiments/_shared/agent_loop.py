"""
最小可运行的 ReAct 循环。

供实验 1-4 共用的基线实现。
所有实验都应基于这个循环构建，避免重复造轮子。

使用方法：
    from agent_loop import react_loop
    result = react_loop(query, llm, tools)
"""
import json
import re
from typing import Callable, Dict, List, Any, Optional


def react_loop(
    query: str,
    llm: Callable[[str], str],
    tools: Dict[str, Callable],
    max_steps: int = 10,
    system_prompt: Optional[str] = None,
) -> Dict[str, Any]:
    """执行 ReAct 循环直到任务完成或达最大步数。

    Args:
        query: 用户查询
        llm: 接受 prompt 返回 response 的函数
        tools: 工具字典，name -> callable
        max_steps: 最大执行步数
        system_prompt: 可选的系统提示词

    Returns:
        dict with keys: success, answer, trajectory, steps, total_tokens
    """
    default_system = (
        "You are a helpful AI assistant. Use the following format:\n"
        "Thought: <your reasoning>\n"
        "Action: {\"name\": \"<tool_name>\", \"arguments\": {...}}\n"
        "When you have the answer, use:\n"
        "Action: {\"name\": \"finish\", \"arguments\": {\"answer\": \"<your answer>\"}}\n"
        f"Available tools: {', '.join(tools.keys())}"
    )
    history = [f"System: {system_prompt or default_system}"]
    history.append(f"User: {query}")
    trajectory = []
    total_tokens = 0

    for step in range(max_steps):
        # 1. 构建 prompt 并调用 LLM
        prompt = "\n".join(history)
        try:
            response = llm(prompt)
            total_tokens += len(prompt.split()) + len(response.split())
        except Exception as e:
            trajectory.append({"step": step, "error": str(e)})
            break

        # 2. 解析 LLM 输出
        thought, action = parse_react_response(response)
        if action is None:
            # LLM 没有生成有效 action，强制 finish
            trajectory.append({"step": step, "thought": thought, "action": None,
                               "note": "no valid action, forcing finish"})
            return {
                "success": False,
                "answer": thought,
                "trajectory": trajectory,
                "steps": step + 1,
                "total_tokens": total_tokens,
            }

        trajectory.append({"step": step, "thought": thought, "action": action})
        history.append(f"Thought: {thought}")
        history.append(f"Action: {json.dumps(action, ensure_ascii=False)}")

        # 3. 处理 finish action
        if action.get("name") == "finish":
            return {
                "success": True,
                "answer": action.get("arguments", {}).get("answer", ""),
                "trajectory": trajectory,
                "steps": step + 1,
                "total_tokens": total_tokens,
            }

        # 4. 执行工具
        tool_name = action.get("name")
        tool_args = action.get("arguments", {})
        if tool_name not in tools:
            error_msg = f"Tool '{tool_name}' not found. Available: {list(tools.keys())}"
            history.append(f"Observation: {error_msg}")
            continue

        try:
            result = tools[tool_name](**tool_args)
            result_str = str(result)
            history.append(f"Observation: {result_str}")
        except Exception as e:
            error_msg = f"Error executing {tool_name}: {e}"
            history.append(f"Observation: {error_msg}")

    return {
        "success": False,
        "answer": None,
        "trajectory": trajectory,
        "steps": max_steps,
        "total_tokens": total_tokens,
    }


def parse_react_response(response: str) -> tuple:
    """解析 LLM 的 ReAct 输出。

    Returns:
        (thought, action) tuple. action 是 dict 或 None（解析失败时）。
    """
    thought = ""
    action = None

    # 提取 Thought：找 Thought: 到 Action: 之间的内容
    thought_match = re.search(r"Thought:\s*(.+?)\s*Action:", response, re.DOTALL)
    if thought_match:
        thought = thought_match.group(1).strip()

    # 提取 Action：用括号配对算法找到最外层 {...}
    action_idx = response.find("Action:")
    if action_idx != -1:
        # 找第一个 {
        start = response.find("{", action_idx)
        if start != -1:
            depth = 0
            in_string = False
            escape = False
            for i in range(start, len(response)):
                c = response[i]
                if escape:
                    escape = False
                    continue
                if c == "\\":
                    escape = True
                    continue
                if c == '"':
                    in_string = not in_string
                if not in_string:
                    if c == "{":
                        depth += 1
                    elif c == "}":
                        depth -= 1
                        if depth == 0:
                            try:
                                action = json.loads(response[start:i+1])
                            except json.JSONDecodeError:
                                pass
                            break

    return thought, action


def format_react_prompt(query: str, history: List[str], tools: Dict[str, Callable]) -> str:
    """格式化 ReAct prompt（实验 1-4 共用）。"""
    return "\n".join(history)


# ==================== 示例：用一个 mock LLM 测试 ====================
if __name__ == "__main__":
    # 模拟工具
    tools = {
        "get_weather": lambda city: {"temp": 25, "rain": 30, "city": city},
        "add": lambda a, b: a + b,
    }

    # 模拟 LLM（直接返回预设响应）
    def mock_llm(prompt):
        return (
            "Thought: I need to look up the weather.\n"
            'Action: {"name": "get_weather", "arguments": {"city": "北京"}}'
        )

    result = react_loop("北京明天天气如何？", mock_llm, tools, max_steps=5)
    print(json.dumps(result, ensure_ascii=False, indent=2))
