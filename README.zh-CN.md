# 任务模型路由器（Task Model Router）

[English](README.md) | [简体中文](README.zh-CN.md)

这是一个 Codex Skill：它不按任务字数或单次调用价格粗略选模，而是按“正确完成任务的预期总成本”，在 **GPT-6 Astra** 与 **GPT-5.6 Sol** 之间分流；选定主模型后，还可把边界清楚、重复机械、判断负担低的批量工作委派给 **GPT-5.6 Luna**。

## 为什么需要它

较便宜的模型不一定能让长程任务更省额度。如果初期规划失误导致走弯路、重新开始或后期大面积返工，总消耗可能接近甚至超过一开始使用更强规划模型的成本。因此，本 Skill 会判断：

- 早期关键选择是否存在不确定性；
- 依赖链是否深且耦合；
- 错误是否要到后期才暴露；
- 返工范围和恢复成本；
- 是否需要跨阶段持续维持多项约束。

路径清晰、错误局部且便于验证的工作通常交给 Sol；早期决策影响广、未知因素关键、验证滞后或返工昂贵的工作交给 Astra。无论主模型是哪一个，都可以继续把合适的机械批次交给 Luna。

## 分流速览

| 路由 | 适用任务 |
| --- | --- |
| GPT-5.6 Sol | 方法明确、验收标准清楚、错误局部、验证便宜 |
| GPT-6 Astra | 早期选择不确定、依赖深、错误暴露晚、返工代价高 |
| GPT-5.6 Luna 子智能体 | 范围明确、可独立完成、重复读取/提取/检查且解释负担低 |

任务长度本身不是依据：很长的确定性批处理仍可使用 Sol；很短但复现条件未知的生产故障也可能需要 Astra。

## 安装

将仓库克隆到 Codex 的 Skills 目录：

```powershell
git clone https://github.com/LunarXuan/task-model-router.git "$env:CODEX_HOME/skills/task-model-router"
```

如果没有设置 `CODEX_HOME`，请使用用户目录下的 `.codex/skills/task-model-router`。安装后重启 Codex 或刷新 Skill 发现。

## 桌面端使用

需要可靠触发时，显式调用：

```text
$task-model-router 为这八个服务规划并实施迁移……
```

Skill 会在实质执行前给出建议模型、返工风险和具体依据。Skill 无法静默切换一个已经运行中的桌面任务模型；如果建议与当前选择不同，请在输入框中选择建议模型，再发送“继续”。

主模型选定后，Astra 和 Sol 都会执行相同的 Luna 委派策略。主模型仍负责规划、整合、关键判断和最终验证。

## CLI 使用

要求：Windows PowerShell 7、Python 3，以及已登录的 Codex CLI。

```powershell
$skillRoot = Join-Path $env:CODEX_HOME 'skills/task-model-router'

& "$skillRoot/scripts/route-codex.ps1" `
  -Prompt '解释 Python 列表切片' `
  -WorkingDirectory 'C:/path/to/project'

& "$skillRoot/scripts/route-codex.ps1" `
  -PromptFile 'C:/path/to/request.txt' `
  -ContextFile 'C:/path/to/plan.txt' `
  -WorkingDirectory 'C:/path/to/project' `
  -Sandbox workspace-write

& "$skillRoot/scripts/route-codex.ps1" `
  -Prompt '设计跨服务数据迁移' `
  -RouteOnly
```

启动器会先用 Sol 做一次轻量语义分类，再启动选中的模型。`-Model sol` 或 `-Model astra` 可显式覆盖分类。执行默认使用 `read-only` 沙盒；只有任务确实获准修改工作区时，才传入 `-Sandbox workspace-write`。

## 测试

本地测试只使用 Python 标准库：

```powershell
python scripts/test_router.py
```

可选的真实分类测试会调用 Codex 模型并消耗额度：

```powershell
python scripts/test_live.py --output live-results.json
```

## 边界与限制

- 分流是定性判断，不能保证零误判，也不承诺固定比例的额度节省。
- CLI 分类本身会消耗 Sol 额度。
- 模型与子智能体是否可用，取决于宿主和账号配置。
- 启动器不会绕过审批、沙盒、认证、仓库指令或其他安全措施。
- 运行中升级会保留已完成工作并输出交接信息，不会自动重放已有副作用。

更多细节见[使用说明](references/usage.md)、[路由策略](references/routing-policy.md)和 [Luna 委派策略](references/luna-delegation-policy.md)。

## 许可证

[MIT](LICENSE)

## 致谢

友链感谢：[LINUX DO](https://linux.do/)
