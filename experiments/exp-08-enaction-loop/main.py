"""
实验 8：Enaction 循环实现（Mock 模式）

实现 Varela 的 Enaction 循环：Perception -> Action -> Environment Change -> New Perception。
在模拟网格世界中验证"认知通过行动与环境的耦合循环而产生"。

运行：
    python main.py
"""
import json
import random


# ==================== 模拟环境 ====================
class GridWorld:
    """简单 5x5 网格世界。"""

    def __init__(self, size: int = 5):
        self.size = size
        self.agent_pos = [0, 0]
        self.goal = [size - 1, size - 1]
        self.obstacles = set()
        self.items = {}
        self._place_obstacles()
        self._place_items()

    def _place_obstacles(self):
        random.seed(42)
        for _ in range(5):
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            if pos != (0, 0) and pos != tuple(self.goal):
                self.obstacles.add(pos)

    def _place_items(self):
        self.items = {(1, 1): "钥匙", (3, 2): "地图", (2, 3): "食物"}

    def perceive(self) -> dict:
        """Agent 感知当前环境。"""
        x, y = self.agent_pos
        perception = {
            "position": [x, y],
            "goal_direction": [self.goal[0] - x, self.goal[1] - y],
            "obstacles_nearby": [],
            "items_nearby": [],
        }
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if (nx, ny) in self.obstacles:
                    perception["obstacles_nearby"].append([nx, ny])
                if (nx, ny) in self.items:
                    perception["items_nearby"].append({"pos": [nx, ny], "item": self.items[(nx, ny)]})
        return perception

    def step(self, action: str) -> dict:
        """执行行动，返回环境变化。"""
        x, y = self.agent_pos
        old_pos = [x, y]
        result = {"success": False, "message": "", "picked_up": None}

        if action == "up":
            nx, ny = x, y - 1
        elif action == "down":
            nx, ny = x, y + 1
        elif action == "left":
            nx, ny = x - 1, y
        elif action == "right":
            nx, ny = x + 1, y
        elif action == "pick_up":
            if (x, y) in self.items:
                result["picked_up"] = self.items.pop((x, y))
                result["success"] = True
                result["message"] = f"拾取了 {result['picked_up']}"
            else:
                result["message"] = "这里没有物品"
            return result
        else:
            result["message"] = f"未知行动: {action}"
            return result

        if not (0 <= nx < self.size and 0 <= ny < self.size):
            result["message"] = "撞墙了"
            return result
        if (nx, ny) in self.obstacles:
            result["message"] = "前方有障碍物"
            return result

        self.agent_pos = [nx, ny]
        result["success"] = True
        result["message"] = f"移动到 ({nx}, {ny})"
        return result


# ==================== Enaction 循环 ====================
def enaction_policy(perception: dict, inventory: list) -> str:
    """基于感知选择行动（简单策略）。"""
    # 朝目标方向移动（优先级最高）
    dx, dy = perception["goal_direction"]
    # 如果目标在正右方或正下方，直接走
    if dx > 0:
        return "right"
    if dy > 0:
        return "down"
    if dx < 0:
        return "left"
    if dy < 0:
        return "up"
    # 到达目标附近时尝试拾取
    if perception["items_nearby"]:
        return "pick_up"
    return "right"


def run_enaction_loop(world: GridWorld, max_steps: int = 20) -> list:
    """运行完整的 Enaction 循环。"""
    inventory = []
    trajectory = []

    for step in range(max_steps):
        # 1. Perception
        perception = world.perceive()

        # 2. Decision (基于感知)
        action = enaction_policy(perception, inventory)

        # 3. Action -> Environment Change
        result = world.step(action)

        # 4. New Perception (记录变化)
        new_perception = world.perceive()

        record = {
            "step": step,
            "perception": perception,
            "action": action,
            "environment_response": result,
            "new_perception": new_perception,
            "position": perception["position"],
        }
        if result["picked_up"]:
            inventory.append(result["picked_up"])
            record["inventory"] = list(inventory)

        trajectory.append(record)

        # 到达目标
        if perception["position"] == world.goal:
            break

    return trajectory, inventory


def analyze_trajectory(trajectory: list) -> dict:
    """分析 Enaction 轨迹。"""
    action_counts = {}
    perception_changes = 0
    successful_actions = 0

    for i, step in enumerate(trajectory):
        action_counts[step["action"]] = action_counts.get(step["action"], 0) + 1
        if step["environment_response"]["success"]:
            successful_actions += 1
        # 感知是否因行动而改变
        if i > 0:
            old_p = trajectory[i-1]["perception"]["position"]
            new_p = step["new_perception"]["position"]
            if old_p != new_p:
                perception_changes += 1

    return {
        "total_steps": len(trajectory),
        "successful_actions": successful_actions,
        "perception_changes": perception_changes,
        "action_distribution": action_counts,
        "coupling_ratio": perception_changes / max(len(trajectory) - 1, 1),
    }


def main():
    print("=" * 60)
    print("实验 8：Enaction 循环实现（Mock 模式）")
    print("=" * 60)
    print("验证: 认知通过行动与环境的耦合循环而产生\n")

    # 运行多个场景
    random.seed(42)
    scenarios = [
        {"seed": 42, "size": 5, "desc": "5x5 标准网格"},
        {"seed": 123, "size": 5, "desc": "5x5 随机障碍物"},
        {"seed": 456, "size": 7, "desc": "7x7 大网格"},
        {"seed": 789, "size": 4, "desc": "4x4 小网格"},
        {"seed": 999, "size": 6, "desc": "6x6 中等网格"},
    ]

    all_results = []
    for scenario in scenarios:
        random.seed(scenario["seed"])
        world = GridWorld(size=scenario["size"])
        print(f"\n--- 场景: {scenario['desc']} (seed={scenario['seed']}) ---")
        print(f"  起点: {world.agent_pos}, 目标: {world.goal}")
        print(f"  障碍物: {len(world.obstacles)}, 物品: {list(world.items.values())}")

        trajectory, inventory = run_enaction_loop(world, max_steps=30)
        analysis = analyze_trajectory(trajectory)

        reached_goal = trajectory[-1]["position"] == world.goal
        print(f"  步数: {analysis['total_steps']}, 成功行动: {analysis['successful_actions']}")
        print(f"  感知变化次数: {analysis['perception_changes']}")
        print(f"  行动-感知耦合率: {analysis['coupling_ratio']:.1%}")
        print(f"  到达目标: {'是' if reached_goal else '否'}")
        print(f"  收集物品: {inventory}")
        print(f"  行动分布: {analysis['action_distribution']}")

        all_results.append({
            "scenario": scenario["desc"],
            "analysis": analysis,
            "reached_goal": reached_goal,
            "inventory": inventory,
        })

    # 汇总
    print("\n" + "=" * 60)
    print("Enaction 循环验证汇总")
    print("=" * 60)
    avg_coupling = sum(r["analysis"]["coupling_ratio"] for r in all_results) / len(all_results)
    avg_steps = sum(r["analysis"]["total_steps"] for r in all_results) / len(all_results)
    goals_reached = sum(1 for r in all_results if r["reached_goal"])
    print(f"平均行动-感知耦合率: {avg_coupling:.1%}")
    print(f"平均步数: {avg_steps:.1f}")
    print(f"到达目标: {goals_reached}/{len(all_results)}")
    print(f"\n核心验证: 行动改变了环境 -> 新感知不同于旧感知 -> 形成耦合循环")
    print(f"  耦合率 > 70% 即验证了 Enaction 循环的核心机制")

    output = {"experiment": "exp-08-enaction-loop", "results": all_results,
              "avg_coupling_ratio": avg_coupling, "goals_reached": goals_reached}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
