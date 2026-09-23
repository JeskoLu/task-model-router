# Usage and limits

Desktop: `$task-model-router 帮我完成……` enables routing and bounded Luna delegation. If GPT-6 Astra is already selected for the task, it handles the main work even when ordinary routing would choose Sol; the skill does not ask to switch back to Sol. This also applies to continuations of that task. A new task follows its current model selection. A Skill cannot switch the running main model or intercept every message. No global model or agent defaults are changed.

Windows PowerShell 7, Python 3 and a signed-in Codex CLI are required for the automatic launcher:

```powershell
$skillRoot = Join-Path $env:CODEX_HOME 'skills/task-model-router'
& "$skillRoot/scripts/route-codex.ps1" -Prompt '解释 Python 列表切片' -WorkingDirectory 'C:/path/to/project'
& "$skillRoot/scripts/route-codex.ps1" -PromptFile 'C:/path/to/request.txt' -ContextFile 'C:/path/to/plan.txt' -WorkingDirectory 'C:/path/to/project' -Sandbox workspace-write
& "$skillRoot/scripts/route-codex.ps1" -Prompt '设计跨服务数据迁移' -RouteOnly
```

Use UTF-8 task files for multiline text. Task text is passed to Codex via stdin, never evaluated as shell syntax. RouteOnly performs one real GPT-6 Sol classification and consumes quota. Explicit `-Model sol` or `-Model astra` skips classification; use `-Model astra` for a one-run Astra override. The launcher is foreground to its caller, and can be run by a background terminal session without opening windows. It does not create a scheduled automation.

Classification uses supplied text/context and an isolated temporary working directory, read-only sandbox and disabled subagents. No project scan is performed during classification; supply a plan when relevant. Tool abstention is an instruction, not a complete tool-level security isolation. Execution retains normal Codex configuration and repository instructions. Availability and client configuration can still block models or subagents. No retry, fallback to a cheaper model, credential extraction or global configuration rewrite occurs.

Exit 0 means Codex process success, not proof that every requested action succeeded. Execution exit codes propagate; routing/validation errors use exit 2. Runtime escalation is a plain-language handoff in the model response, not an automatic resume mechanism. Explicit model overrides are not classifier results: risk is unassessed and luna_batch is null, leaving delegation to the executor. CLI semantic classification and desktop contextual classification use the same policy but may differ when inputs differ. Classification accuracy and quota savings require representative real usage; tests cannot guarantee zero bugs.

Prior-art references: https://learn.chatgpt.com/docs/models ; https://learn.chatgpt.com/docs/agent-configuration/subagents ; https://github.com/lm-sys/RouteLLM ; https://github.com/NVIDIA-NeMo/Switchyard . The project borrows task-level cost, escalation and bounded delegation concepts; no third-party code was copied.
