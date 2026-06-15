$basePath = 'c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main'

Write-Host '============================================'
Write-Host '   FULL SITE AUDIT - SERVICE DROPDOWNS'
Write-Host '============================================'
Write-Host ''

# Canonical 8 options that MUST exist
$mustHave = @(
    'Air Ambulance',
    'Airline Stretcher Services', 
    'Flight Medical Escort Services',
    'ECMO Transfer Services',
    'Organ Transplant Assistance',
    'Medical Tourism',
    'Medical Travel Assistance',
    'Home Health Care'
)

# Old/bad values that must NOT exist
$mustNotHave = @(
    'Overseas Medical Tourism',
    'Flight Medical escort',
    'Flight Medical Escort"',
    'Hospital Acceptance',
    'Doctor Appointment',
    'Second Opinion Services',
    'Custom Medical Packages',
    'Air Ambulance Charter'
)

$allHtml = Get-ChildItem -Path $basePath -Filter '*.html' -Recurse | Where-Object { $_.FullName -notlike '*scratch*' }
Write-Host "Total HTML files scanned: $($allHtml.Count)"
Write-Host ''

$passed = 0
$failed = 0
$skipped = 0

foreach ($f in $allHtml) {
    $content = [System.IO.File]::ReadAllText($f.FullName)
    $rel = $f.FullName.Substring($basePath.Length)
    
    # Skip files without a service select
    if ($content -notmatch 'name="service"' -and -not ($content -match 'id="service"' -and $content -match '<select')) {
        $skipped++
        continue
    }
    
    $issues = @()
    
    # Check for bad old values in the dropdown
    foreach ($bad in $mustNotHave) {
        if ($content -match "<option[^>]*>$bad</option>") {
            $issues += "BAD OPTION: '$bad'"
        }
    }
    
    # Check missing canonical options
    foreach ($good in $mustHave) {
        if ($content -notmatch "value=""$good""") {
            $issues += "MISSING: '$good'"
        }
    }
    
    if ($issues.Count -eq 0) {
        Write-Host "  PASS: $rel"
        $passed++
    } else {
        Write-Host "  FAIL: $rel"
        foreach ($issue in $issues) {
            Write-Host "        -> $issue"
        }
        $failed++
    }
}

Write-Host ''
Write-Host "============================================"
Write-Host "RESULTS: $passed PASSED | $failed FAILED | $skipped skipped (no form)"
Write-Host "============================================"
