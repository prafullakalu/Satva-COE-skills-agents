<#
 Installs the Satva skills into Claude Code.
   .\install.ps1                      # all skills -> ~\.claude\skills   (available in every project)
   .\install.ps1 -Project             # all skills -> .\.claude\skills   (this project only)
   .\install.ps1 -Only satva-guide-gif,satva-doc
   .\install.ps1 -Target D:\my\skills # any other folder
 Re-running upgrades in place. Files removed from a newer version are NOT deleted from an old install.
#>
param([string]$Target = (Join-Path $HOME ".claude\skills"), [switch]$Project, [string[]]$Only)
$ErrorActionPreference = "Stop"
if ($Project) { $Target = Join-Path (Get-Location) ".claude\skills" }
$src = Join-Path $PSScriptRoot "skills"
New-Item -ItemType Directory -Force $Target | Out-Null
foreach ($d in Get-ChildItem $src -Directory) {
  if ($Only -and ($Only -notcontains $d.Name)) { continue }
  $dest = Join-Path $Target $d.Name
  New-Item -ItemType Directory -Force $dest | Out-Null
  Copy-Item -Path (Join-Path $d.FullName "*") -Destination $dest -Recurse -Force   # contents, never the folder itself
  Write-Host "installed  $($d.Name)  ->  $dest"
}
Write-Host "`nDone. Restart Claude Code (or start a new session) so it picks the skills up."
