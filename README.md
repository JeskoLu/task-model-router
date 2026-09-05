# Task Model Router

[English](README.md) | [简体中文](README.zh-CN.md)

A Codex skill that routes work between **GPT-6 Astra** and **GPT-5.6 Sol** by the expected cost of reaching a correct result—not by prompt length or nominal per-call cost. It can then delegate bounded, repetitive, low-judgment batches to **GPT-5.6 Luna**.

## Why this exists

A cheaper model is not always cheaper for a long-horizon task. If weak early planning causes wrong turns, restarts, or late rework, the total quota cost can approach—or exceed—the cost of using a stronger planner from the beginning. This skill therefore evaluates:

- uncertainty in early decisions;
- dependency depth and coupling;
- how late errors become visible;
- the cost and blast radius of rework;
- the need to preserve constraints across stages.

Clear, locally verifiable work normally goes to Sol. Work with consequential unknowns, tightly coupled stages, late verification, or expensive recovery goes to Astra. Independent mechanical batches can be assigned to Luna under the selected main model.

## Routing at a glance

| Route | Best fit |
| --- | --- |
| GPT-5.6 Sol | Clear approach, explicit acceptance criteria, local errors, inexpensive verification |
| GPT-6 Astra | Uncertain early choices, deep dependencies, late error discovery, costly rework |
| GPT-5.6 Luna subagent | Concrete, bounded, repetitive reading/extraction/checking with little interpretation |

Task length alone is not a routing signal: a long deterministic batch can stay on Sol, while a short but ambiguous production diagnosis can require Astra.

## Install

Clone the repository into your Codex skills directory:

```powershell
git clone https://github.com/LunarXuan/task-model-router.git "$env:CODEX_HOME/skills/task-model-router"
```

If `CODEX_HOME` is not set, use the `.codex/skills/task-model-router` directory under your user profile. Restart Codex or refresh skill discovery after installation.

## Desktop usage

Invoke the skill explicitly when you want reliable routing:

```text
$task-model-router Plan and implement a migration for these eight services...
```

The skill reports the suggested model, rework risk, and concrete rationale before substantive execution. A skill cannot silently switch the model of an already-running desktop task; if the selection differs, choose the suggested model in the composer and send `continue`.

After the main model is selected, both Astra and Sol apply the same Luna delegation policy. The parent keeps planning, integration, consequential decisions, and final verification.

## CLI usage

Requirements: Windows PowerShell 7, Python 3, and a signed-in Codex CLI.

```powershell
$skillRoot = Join-Path $env:CODEX_HOME 'skills/task-model-router'

& "$skillRoot/scripts/route-codex.ps1" `
  -Prompt 'Explain Python list slicing' `
  -WorkingDirectory 'C:/path/to/project'

& "$skillRoot/scripts/route-codex.ps1" `
  -PromptFile 'C:/path/to/request.txt' `
  -ContextFile 'C:/path/to/plan.txt' `
  -WorkingDirectory 'C:/path/to/project' `
  -Sandbox workspace-write

& "$skillRoot/scripts/route-codex.ps1" `
  -Prompt 'Design a cross-service data migration' `
  -RouteOnly
```

The launcher performs one lightweight semantic classification with Sol, then starts the chosen model. `-Model sol` or `-Model astra` explicitly overrides classification. The default execution sandbox is `read-only`; pass `-Sandbox workspace-write` only when the task is authorized to modify the workspace.

## Test

Local tests use only the Python standard library:

```powershell
python scripts/test_router.py
```

Optional live checks call Codex models and consume quota:

```powershell
python scripts/test_live.py --output live-results.json
```

## Limits

- Routing is qualitative and cannot guarantee zero misclassification or a specific quota saving.
- CLI classification itself consumes Sol quota.
- Model and subagent availability depend on the host and account configuration.
- The launcher does not bypass approvals, sandboxing, authentication, repository instructions, or other safety controls.
- Runtime escalation preserves completed work and returns a handoff; it does not automatically replay side effects.

See [usage notes](references/usage.md), the [routing policy](references/routing-policy.md), and the [Luna delegation policy](references/luna-delegation-policy.md) for details.

## License

[MIT](LICENSE)

## Acknowledgements

Friendly link and thanks: [LINUX DO](https://linux.do/)
