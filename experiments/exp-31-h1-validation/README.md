# 实验 31：H1 结构可塑性验证 / H1 Structural Plasticity Validation

> 状态：可运行（真实 LLM + 确定性 Mock）  
> 目标：在环境改变后，检验可修改 Prompt 的 Agent 是否比冻结形态 Agent 获得更低的适应后悔值。

## 目的 / Purpose

本实验是操作形态学 H1（Structural Plasticity）的基础实证验证。冻结基线固定
`B = {P_initial, T_fixed, M_empty, C_static}`；自适应处理组保持 T/M/C 不变，允许元控制器
U 以 OPRO 风格的“生成候选 Prompt → 代理评估 → 接受或回滚”过程修改 P。

理论与完整预注册设计见 [`../../research/r-note-002-h1-structural-plasticity.md`](../../research/r-note-002-h1-structural-plasticity.md)。

## 实验设计 / Design

- **10 个标准化任务**：数学、事实搜索、代码执行式计算、格式转换。
- **5 类环境干预**：工具故障、API 签名变化、任务分布漂移、指令变化、输出格式变化。
- **观察窗口**：每个“任务 × 干预”在干预后连续运行 5 步。
- **后悔值**：每步 `r_t = Q*(s,a*) - Q^pi(s,a)`，其中 oracle 质量 `Q*=1`，窗口后悔值为 5 步之和；每个任务的总后悔值汇总五类干预。
- **配对统计**：在相同的 10 个任务上比较 frozen 与 adaptive，使用双侧 Wilcoxon signed-rank exact test。
- **多重比较**：Bonferroni `alpha = 0.05 / 5 = 0.01`。
- **效应量**：配对 Cohen's `d_z = mean(frozen - adaptive) / SD(frozen - adaptive)`；正值表示自适应组更优。
- **共享实现**：Agent 执行使用 `experiments/_shared/agent_loop.py` 的 `react_loop`，成功率汇总复用 `_shared/metrics.py`。

## 运行 / Run

建议使用 Python 3.10+。

```bash
cd experiments/exp-31-h1-validation
python -m pip install -r requirements.txt
python main.py
# 或 / or
python run.py
```

### Mock 模式

未设置 `OPENAI_API_KEY` 时自动使用确定性 Mock：

```bash
python main.py
```

程序会明确打印：`模式：Mock / Mode: MOCK`。Mock 用于验证管线、干预、后悔值计算和统计代码；它不能替代真实模型证据。

### 真实 LLM 模式

设置 API Key 后自动使用 `gpt-4o-mini`：

PowerShell：

```powershell
$env:OPENAI_API_KEY = "your-key"
python main.py
```

macOS/Linux：

```bash
export OPENAI_API_KEY="your-key"
python main.py
```

若缺少 `openai` 包、客户端初始化失败或任一 API 请求失败，程序会丢弃不完整的真实运行并完整回退到 Mock，避免混合真实与模拟观察值。

## 输出 / Output

运行生成 `results.json`，包含：运行模式、模型、两组平均/标准差/逐任务后悔值、Wilcoxon p 值、Cohen's d、H1 判定以及逐步历史。终端同时打印 frozen 与 adaptive 的 ASCII 后悔值条形图和双语统计结论。

## 预期结果与判定 / Expected Result

仅当以下三个预注册条件同时满足时，`h1_supported` 才为 `true`：

1. `adaptive_regret.mean < frozen_regret.mean`；
2. `wilcoxon_p < 0.01`；
3. `cohens_d > 0.5`（本实现的正方向表示 frozen regret 更高）。

真实 LLM 结果才构成 H1 的初步经验性证据；Mock 结果只表明实验实现按预期工作。

## 局限 / Limitations

- 10 个任务和 5 步窗口远小于 r-note-002 建议的 ≥30 次独立重复、≥100 步长视野，统计功效与外部效度有限。
- 处理组仅修改 P，不能验证 T/M/C 联合可塑性，也不能支持 H2 协同演化。
- 任务和工具是标准化微基准，并非真实 Web 搜索、沙箱代码执行或生产 API。
- 质量函数以任务答案和协议合规性为 oracle，不能覆盖开放式答案的语义质量。
- 单模型、单温度设置可能受到模型版本、服务端更新和提示敏感性的影响。
- API 成本、延迟、Prompt 修改成本以及长期震荡/退化未计入 regret。
