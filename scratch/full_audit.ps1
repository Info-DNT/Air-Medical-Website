$basePath = 'c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main'
$index = [System.IO.File]::ReadAllText("$basePath\index.html")

Write-Host '============================================'
Write-Host '   FULL SITE AUDIT - ALL 3 CHANGES'
Write-Host '============================================'
Write-Host ''

Write-Host '--- CHANGE 1: Certificate Cards (index.html) ---'
if ($index -match 'CAMTS ACCREDITED') { Write-Host '  FAIL: CAMTS card still exists' } else { Write-Host '  PASS: CAMTS card removed' }
if ($index -match 'DGCA-COMPLIANT OPERATIONS') { Write-Host '  FAIL: DGCA card still exists' } else { Write-Host '  PASS: DGCA card removed' }
if ($index -match 'ISO 9001:2015 CERTIFIED') { Write-Host '  PASS: ISO card present' } else { Write-Host '  FAIL: ISO card missing!' }
if ($index -match 'FAA-APPROVED MEDICAL EQUIPMENT') { Write-Host '  PASS: FAA card present' } else { Write-Host '  FAIL: FAA card missing!' }
if ($index -match 'col-xl-5') { Write-Host '  PASS: Cards resized to col-xl-5 (2-card balanced layout)' } else { Write-Host '  WARN: col-xl-5 not found' }

Write-Host ''
Write-Host '--- CHANGE 2: Services Section 4th Card (index.html) ---'
if ($index -match 'Medical Tourism') { Write-Host '  PASS: Medical Tourism is the 4th service card' } else { Write-Host '  FAIL: Medical Tourism card not found!' }
if ($index -match 'fa-globe') { Write-Host '  PASS: Globe icon on Medical Tourism card' } else { Write-Host '  FAIL: Globe icon missing!' }

Write-Host ''
Write-Host '--- CHANGE 3: Service Dropdown Canonical Options (all files) ---'
$allHtml = Get-ChildItem -Path $basePath -Filter '*.html' -Recurse | Where-Object { $_.FullName -notlike '*scratch*' }

$canonical = @('Air Ambulance', 'Airline Stretcher Services', 'Flight Medical Escort Services', 'ECMO Transfer Services', 'Organ Transplant Assistance', 'Medical Tourism', 'Medical Travel Assistance', 'Home Health Care')
$passCount = 0
$failCount = 0
$failFiles = @()

foreach ($f in $allHtml) {
    $content = [System.IO.File]::ReadAllText($f.FullName)
    $rel = $f.Name

    if ($content -notmatch 'name="service"' -and -not ($content -match 'id="service"' -and $content -match '<select')) { continue }

    $ok = $true
    $fileIssues = @()
    foreach ($svc in $canonical) {
        if ($content -notmatch "value=""$svc""") {
            $ok = $false
            $fileIssues += "MISSING: $svc"
        }
    }
    $badOptions = @('Overseas Medical Tourism', 'Doctor Appointment', 'Custom Medical Packages', 'Hospital Acceptance', 'Second Opinion Services', 'Air Ambulance Charter')
    foreach ($bad in $badOptions) {
        if ($content -match "<option[^>]*>$bad</option>") {
            $ok = $false
            $fileIssues += "BAD OPTION: $bad"
        }
    }

    if ($ok) {
        $passCount++
    } else {
        $failCount++
        $failFiles += [PSCustomObject]@{ File = $rel; Issues = $fileIssues }
    }
}

Write-Host "  Files with service forms: $($passCount + $failCount)"
Write-Host "  PASSED: $passCount"
Write-Host "  FAILED: $failCount"
if ($failCount -gt 0) {
    foreach ($ff in $failFiles) {
        Write-Host "  -- $($ff.File)"
        foreach ($issue in $ff.Issues) { Write-Host "       $issue" }
    }
}

Write-Host ''
Write-Host '--- OLD BAD VALUES SITE-WIDE SCAN ---'
$badTerms = @('Overseas Medical Tourism', 'CAMTS ACCREDITED', 'DGCA-COMPLIANT OPERATIONS', '<option>Flight Medical escort</option>')
foreach ($term in $badTerms) {
    $hits = $allHtml | Select-String -Pattern $term -SimpleMatch
    if ($hits.Count -gt 0) {
        Write-Host "  FAIL '$term' found in:"
        foreach ($h in $hits) { Write-Host "    $($h.Filename):$($h.LineNumber)" }
    } else {
        Write-Host "  PASS: '$term' not found anywhere"
    }
}

Write-Host ''
Write-Host '============================================'
Write-Host '            AUDIT COMPLETE'
Write-Host '============================================'
