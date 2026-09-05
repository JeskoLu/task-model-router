[CmdletBinding(DefaultParameterSetName='Text')]
param(
    [Parameter(Mandatory, ParameterSetName='Text')][string]$Prompt,
    [Parameter(Mandatory, ParameterSetName='File')][string]$PromptFile,
    [string]$ContextFile,
    [string]$WorkingDirectory = (Get-Location).Path,
    [ValidateSet('sol','astra')][string]$Model,
    [ValidateSet('read-only','workspace-write')][string]$Sandbox = 'read-only',
    [switch]$RouteOnly
)
$ErrorActionPreference = 'Stop'
$routeArgs = @('-X', 'utf8', (Join-Path $PSScriptRoot 'route_codex.py'), '--cwd', $WorkingDirectory, '--sandbox', $Sandbox)
if ($PSCmdlet.ParameterSetName -eq 'File') { $routeArgs += @('--prompt-file', $PromptFile) }
else { $routeArgs += @('--prompt', $Prompt) }
if ($ContextFile) { $routeArgs += @('--context-file', $ContextFile) }
if ($Model) { $routeArgs += @('--model', $Model) }
if ($RouteOnly) { $routeArgs += '--route-only' }
& python @routeArgs
exit $LASTEXITCODE
