# Add entrance animations to a Satva deck via PowerPoint COM.
#
# python-pptx cannot write animations, and hand-authoring <p:timing> XML is the
# fastest way to make PowerPoint declare a deck corrupt. PowerPoint writes it
# correctly itself, so drive it instead.
#
# Components built by satva_deck.py are named  A<group>_<n>. Every shape in a
# group appears together; each group costs one click. Untagged shapes (title,
# kicker, background) are always visible.
#
# Usage: powershell -File animate.ps1 -Deck "C:\path\deck.pptx" [-Embed]
param(
    [Parameter(Mandatory = $true)][string]$Deck
)

$Deck = (Resolve-Path $Deck).Path
$msoAnimEffectFade = 10
$msoAnimTriggerOnPageClick = 1
$msoAnimTriggerWithPrevious = 2

$app = New-Object -ComObject PowerPoint.Application
try {
    $pres = $app.Presentations.Open($Deck, 0, 0, -1)
    # Font embedding is NOT exposed on the Presentation object in Office 2013 COM
    # (File > Options > Save > Embed fonts does it by hand). Install the font on
    # the presenting machine instead — see SKILL.md.

    $total = 0
    foreach ($slide in $pres.Slides) {
        $seq = $slide.TimeLine.MainSequence
        while ($seq.Count -gt 0) { $seq.Item(1).Delete() }

        # group shapes by the A<group>_ prefix, preserving z-order within a group
        # NB: keys must be strings — an [ordered] dictionary reads an int as a
        # positional index, not a key, and throws on the first insert.
        $groups = @{}
        foreach ($sh in $slide.Shapes) {
            if ($sh.Name -match '^A(\d+)_') {
                $g = $Matches[1]
                if (-not $groups.ContainsKey($g)) { $groups[$g] = @() }
                $groups[$g] += $sh
            }
        }
        foreach ($g in ($groups.Keys | Sort-Object { [int]$_ })) {
            $first = $true
            foreach ($sh in $groups[$g]) {
                $trigger = if ($first) { $msoAnimTriggerOnPageClick } else { $msoAnimTriggerWithPrevious }
                $e = $seq.AddEffect($sh, $msoAnimEffectFade, 0, $trigger)
                $e.Timing.Duration = 0.4
                if (-not $first) { $e.Timing.TriggerDelayTime = 0.0 }
                $first = $false
                $total++
            }
        }
    }
    $pres.Save()
    $pres.Close()
    "animated $total shapes"
} finally {
    $app.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
