# Luna delegation

Both Astra and Sol MUST delegate a qualifying independent batch when the host provides Luna subagents and the main agent has useful independent work to do. Default one worker; use up to two for disjoint batches within host limits. Reuse the existing worker for related follow-ups. Avoid delegating a single trivial command, duplicating completed reads, or having the parent re-read all returned material.

Specify model=gpt-5.6-luna, reasoning_effort=low (medium for bounded synthesis), and minimal context. If the host requires fork_turns=none or a bounded history to override models, comply. Do not select a custom role which pins another model or max effort; explicit generic model selection is preferred. Verify spawn metadata where available. If Luna is unavailable, report it and handle locally, without claiming delegation occurred.

Send goal, exact input scope, allowed read/check actions, completion criteria and a compact result format: facts + file/line references + commands and exit codes + uncertainties. Include relevant permissions and constraints; do not copy full parent history. Do not delegate the main agent's required reading of skill instructions. Worker must not spawn workers recursively, expand scope, install packages, publish, delete, modify files or issue external writes. Command length is not evidence of safety; tests may also write files or contact services, so only use checks appropriate to the authorization.

Use a read-only sandbox when the host supports per-worker sandbox controls. Otherwise state read-only as a task constraint, NOT as a technically enforced sandbox. Preserve host protections. If ownership includes shared files, explain that other agents may be working and no edits may be reverted.

On unclear results or reasoning beyond extraction, return the unresolved question to the parent instead of speculative retries. The parent assesses evidence and spot-checks consequential findings, retains architectural/security decisions and final acceptance. Do not spend more on blanket repeated review than the batch saves.
