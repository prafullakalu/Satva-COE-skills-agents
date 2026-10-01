<#
 Installs the Satva skills (and optionally agents) into Claude Code.
 Skills live nested by department in this repo (skills\<dept>\<group>\<skill>); Claude Code needs them flat,
 so each skill folder is copied to <target>\<skill-name>.
   .\install.ps1                          # all skills -> ~\.claude\skills   (every project)
   .\install.ps1 -Dept accounting,seo     # only those departments (accounting marketing seo satva general)
   .\install.ps1 -Only xero-bank-reconciliation,satva-doc
   .\install.ps1 -Agents                  # also agents -> ~\.claude\agents  (honours -Dept)
   .\install.ps1 -Project                 # into .\.claude\skills (and .\.claude\agents) for this project only
   .\install.ps1 -Target D:\my\skills     # skills there; agents go to its sibling "agents" folder
   .\install.ps1 -List                    # show what is available, install nothing
 Re-running upgrades in place. Files removed from a newer version are NOT deleted from an old install.
#>
param([string]$Target = (Join-Path $HOME ".claude\skills"), [switch]$Project, [string[]]$Only, [string[]]$Dept, [switch]$Agents, [switch]$List)
$ErrorActionPreference = "Stop"
if ($Project) { $Target = Join-Path (Get-Location) ".claude\skills" }
$ATarget = Join-Path (Split-Path $Target -Parent) "agents"
$root = Join-Path $PSScriptRoot "skills"
function Want($group, $skill) { (-not $Dept -or $Dept -contains $group) -and (-not $Only -or $Only -contains $skill) }  # not named $dept: PowerShell is case-insensitive and would shadow -Dept
if (-not $List) { New-Item -ItemType Directory -Force $Target | Out-Null }
foreach ($f in Get-ChildItem $root -Recurse -Filter SKILL.md | Sort-Object FullName) {
  $d = $f.Directory; $name = $d.Name
  $rel = $d.FullName.Substring($root.Length + 1) -replace '\\', '/'
  $dd = $rel.Split('/')[0]
  if (-not (Want $dd $name)) { continue }
  if ($List) { "{0,-11} {1,-42} skills/{2}" -f $dd, $name, $rel; continue }
  $dest = Join-Path $Target $name
  New-Item -ItemType Directory -Force $dest | Out-Null
  Copy-Item -Path (Join-Path $d.FullName "*") -Destination $dest -Recurse -Force   # contents, never the folder itself
  Write-Host "installed  $name  ->  $dest"
}
$agentsDir = Join-Path $PSScriptRoot "agents"
if ($Agents -and (Test-Path $agentsDir)) {
  foreach ($f in Get-ChildItem $agentsDir -Recurse -Filter *.md | Where-Object Name -ne "README.md") {
    $dd = $f.Directory.Name; $name = $f.BaseName
    if (-not (Want $dd $name)) { continue }
    if ($List) { "{0,-11} {1,-42} agent" -f $dd, $name; continue }
    New-Item -ItemType Directory -Force $ATarget | Out-Null
    Copy-Item $f.FullName $ATarget -Force
    Write-Host "installed  agent $name  ->  $ATarget"
  }
}
if (-not $List) { Write-Host "`nDone. Restart Claude Code (or start a new session) so it picks them up." }
