"""
实验 12：自创生模拟（Mock 模式）

模拟 Maturana & Varela 的 Autopoiesis 概念。
实现一个由组件和过程组成的自创生系统，验证自我维持、自我修复、自我生产。

运行：
    python main.py
"""
import json
import random
from dataclasses import dataclass, field


@dataclass
class Component:
    """自创生系统的组件。"""
    name: str
    health: float = 1.0  # 0=损坏, 1=健康
    production_cost: float = 0.1  # 生产该组件需要的能量
    critical: bool = False  # 是否是关键组件


@dataclass
class AutopoieticSystem:
    """自创生系统。"""
    name: str
    components: dict[str, Component] = field(default_factory=dict)
    energy: float = 1.0
    alive: bool = True
    step_count: int = 0
    self_repairs: int = 0
    self_productions: int = 0

    def add_component(self, comp: Component):
        self.components[comp.name] = comp

    def health_score(self) -> float:
        """系统整体健康度。"""
        if not self.components:
            return 0.0
        return sum(c.health for c in self.components.values()) / len(self.components)

    def production_process(self):
        """自生产：消耗能量，修复/生产组件。"""
        self.self_productions += 1
        self.energy -= 0.05  # 维持消耗

        for name, comp in self.components.items():
            if comp.health < 0.5 and self.energy > comp.production_cost:
                # 自修复
                comp.health = min(1.0, comp.health + 0.3)
                self.energy -= comp.production_cost
                self.self_repairs += 1
            elif comp.health < 1.0 and self.energy > comp.production_cost * 0.5:
                # 维护
                comp.health = min(1.0, comp.health + 0.1)
                self.energy -= comp.production_cost * 0.3

    def boundary_process(self):
        """边界维护：抵抗外部扰动。"""
        self.energy -= 0.02
        # 移除损坏的组件
        to_remove = [n for n, c in self.components.items() if c.health <= 0]
        for n in to_remove:
            del self.components[n]

        # 检查关键组件
        for n, c in self.components.items():
            if c.critical and c.health <= 0:
                self.alive = False

    def step(self, perturbation: float = 0.0):
        """一个时间步。"""
        self.step_count += 1
        # 外部扰动
        if perturbation > 0:
            for comp in self.components.values():
                comp.health -= perturbation * random.random()

        # 自创生过程
        self.production_process()
        self.boundary_process()

        # 能量恢复（模拟"代谢"）
        self.energy = min(1.0, self.energy + 0.08)

        # 检查存活
        if not self.components:
            self.alive = False
        if self.energy <= 0:
            self.alive = False


def create_standard_system(name: str) -> AutopoieticSystem:
    """创建一个标准自创生系统。"""
    system = AutopoieticSystem(name=name, energy=1.0)
    system.add_component(Component("membrane", health=1.0, production_cost=0.15, critical=True))
    system.add_component(Component("metabolism", health=1.0, production_cost=0.12, critical=True))
    system.add_component(Component("producer", health=1.0, production_cost=0.10, critical=False))
    system.add_component(Component("repair_unit", health=1.0, production_cost=0.08, critical=False))
    system.add_component(Component("sensor", health=1.0, production_cost=0.06, critical=False))
    return system


def run_simulation(system: AutopoieticSystem, perturbation: float, max_steps: int = 50) -> dict:
    """运行自创生模拟。"""
    history = []
    for _ in range(max_steps):
        if not system.alive:
            break
        system.step(perturbation)
        history.append({
            "step": system.step_count,
            "alive": system.alive,
            "health": system.health_score(),
            "energy": system.energy,
            "component_count": len(system.components),
        })
    return {
        "system": system.name,
        "perturbation": perturbation,
        "survived": system.alive,
        "steps": system.step_count,
        "final_health": system.health_score(),
        "final_energy": system.energy,
        "self_repairs": system.self_repairs,
        "self_productions": system.self_productions,
        "history": history,
    }


def main():
    print("=" * 60)
    print("实验 12：自创生模拟（Mock 模式）")
    print("=" * 60)
    print("模拟 Maturana & Varela 的 Autopoiesis 概念\n")

    # 不同扰动强度
    perturbations = [
        ("无扰动", 0.00),
        ("弱扰动", 0.05),
        ("中等扰动", 0.15),
        ("强扰动", 0.30),
        ("极强扰动", 0.50),
    ]

    all_results = []
    for label, pert in perturbations:
        random.seed(42)
        system = create_standard_system(f"System-{label}")
        result = run_simulation(system, pert, max_steps=50)
        result["label"] = label
        all_results.append(result)

        status = "SURVIVED" if result["survived"] else "DIED"
        print(f"  [{status}] {label} (perturbation={pert:.2f})")
        print(f"    存活步数: {result['steps']}, 最终健康: {result['final_health']:.3f}, "
              f"最终能量: {result['final_energy']:.3f}")
        print(f"    自修复次数: {result['self_repairs']}, 自生产次数: {result['self_productions']}")

    # 汇总
    print("\n" + "=" * 60)
    print("自创生能力验证")
    print("=" * 60)
    print(f"| {'扰动级别':<12} | {'存活':>6} | {'步数':>4} | {'最终健康':>8} | {'修复次数':>8} |")
    print(f"|{'-'*14}|{'-'*8}|{'-'*6}|{'-'*10}|{'-'*10}|")
    for r in all_results:
        s = "Yes" if r["survived"] else "No"
        print(f"| {r['label']:<12} | {s:>6} | {r['steps']:>4} | "
              f"{r['final_health']:>8.3f} | {r['self_repairs']:>8} |")

    survived_perturbations = [r["perturbation"] for r in all_results if r["survived"]]
    max_survived = max(survived_perturbations) if survived_perturbations else 0
    print(f"\n系统最高承受扰动: {max_survived:.2f}")
    print(f"\n核心验证:")
    print(f"  - 自生产: 系统消耗能量生产/修复组件 ({all_results[0]['self_productions']} 次生产)")
    print(f"  - 自修复: 组件损坏后被自动修复 ({all_results[0]['self_repairs']} 次修复)")
    print(f"  - 自维持: 无扰动时系统持续存活 ({'是' if all_results[0]['survived'] else '否'})")
    print(f"  - 鲁棒性: 扰动增大时系统逐渐失效 (阈值 ~{max_survived:.2f})")

    output = {"experiment": "exp-12-autopoiesis-simulation", "results": all_results,
              "max_survived_perturbation": max_survived}
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到 results.json")


if __name__ == "__main__":
    main()
