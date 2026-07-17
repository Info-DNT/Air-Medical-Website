$basePath = 'c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main'

Write-Host '=== Checking for OLD values (should be 0) ==='

$oldTerms = @('Overseas Medical Tourism', 'CAMTS ACCREDITED', 'DGCA-COMPLIANT OPERATIONS')
foreach ($term in $oldTerms) {
    $results = Get-ChildItem -Path $basePath -Filter '*.html' -Recurse |
               Select-String -Pattern $term |
               Where-Object { $_.Path -notlike '*scratch*' -and $_.Path -notlike '*diff*' }
    Write-Host "  '$term': $($results.Count) occurrences"
    foreach ($r in $results) {
        Write-Host "    $($r.Filename) line $($r.LineNumber)"
    }
}

Write-Host ''
Write-Host '=== Checking NEW canonical values ==='

$checks = @(
    @{ Label = 'Flight Medical Escort Services (option)'; Pattern = '<option value="Flight Medical Escort Services">' },
    @{ Label = 'Air Ambulance (option)'; Pattern = '<option value="Air Ambulance">' },
    @{ Label = 'Home Health Care (option)'; Pattern = '<option value="Home Health Care">' }
)
foreach ($check in $checks) {
    $results = Get-ChildItem -Path $basePath -Filter '*.html' -Recurse |
               Select-String -Pattern $check.Pattern |
               Where-Object { $_.Path -notlike '*scratch*' }
    Write-Host "  $($check.Label): $($results.Count) occurrences"
}

Write-Host ''
Write-Host '=== Spot-check index.html cert section ==='
$indexContent = Get-Content (Join-Path $basePath 'index.html') -Raw
if ($indexContent -match 'CAMTS ACCREDITED') { Write-Host '  FAIL: CAMTS still in index.html' } else { Write-Host '  PASS: CAMTS removed from index.html' }
if ($indexContent -match 'DGCA-COMPLIANT') { Write-Host '  FAIL: DGCA still in index.html' } else { Write-Host '  PASS: DGCA removed from index.html' }
if ($indexContent -match 'ISO 9001:2015') { Write-Host '  PASS: ISO card still present' } else { Write-Host '  FAIL: ISO card missing!' }
if ($indexContent -match 'FAA-APPROVED') { Write-Host '  PASS: FAA card still present' } else { Write-Host '  FAIL: FAA card missing!' }

Write-Host ''
Write-Host '=== Spot-check Services section ==='
if ($indexContent -match 'Flight Medical Escort Services') { Write-Host '  PASS: Flight Medical Escort Services card present' } else { Write-Host '  FAIL: Card missing!' }
if ($indexContent -match '<h4 class="mb-3">Medical Tourism</h4>') { Write-Host '  FAIL: Medical Tourism card still exists!' } else { Write-Host '  PASS: Medical Tourism card removed' }

Write-Host ''
Write-Host 'Verification complete.'
