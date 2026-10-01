# Render every slide of a .pptx to PNG for visual QA.
# LibreOffice is not installed on this machine; PowerPoint COM is (Office15).
# Usage: powershell -File render.ps1 -Deck "C:\path\deck.pptx" -Out "C:\path\shots"
param(
    [Parameter(Mandatory = $true)][string]$Deck,
    [Parameter(Mandatory = $true)][string]$Out,
    [int]$Width = 1600
)

$Deck = (Resolve-Path $Deck).Path
if (-not (Test-Path $Out)) { New-Item -ItemType Directory -Force -Path $Out | Out-Null }
$Out = (Resolve-Path $Out).Path

$app = New-Object -ComObject PowerPoint.Application
try {
    # msoFalse=0 for ReadOnly/Untitled, msoTrue=-1 for WithWindow (PPT refuses hidden open)
    $pres = $app.Presentations.Open($Deck, -1, 0, -1)
    $h = [int]($Width * $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth)
    $pres.Export($Out, "PNG", $Width, $h)
    $pres.Close()
} finally {
    $app.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
Get-ChildItem $Out -Filter *.PNG | Sort-Object Name | Select-Object -ExpandProperty FullName
