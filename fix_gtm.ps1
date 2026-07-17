$base = 'c:/Users/Admin/Downloads/airmedical_24X7_jeet-main/airmedical_24X7_jeet-main'
Get-ChildItem -Path $base -Recurse -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $changed = $false

    # 1. Fix GTM noscript iframe: ns -> ns.html (was incorrectly stripped)
    if ($content -match 'googletagmanager\.com/ns\?') {
        $content = $content -replace 'googletagmanager\.com/ns\?', 'googletagmanager.com/ns.html?'
        $changed = $true
    }

    # 2. Fix GTM script: gtm5445 or just gtm -> gtm.js
    if ($content -match 'googletagmanager\.com/gtm5445\?') {
        $content = $content -replace 'googletagmanager\.com/gtm5445\?', 'googletagmanager.com/gtm.js?'
        $changed = $true
    }
    if ($content -match "googletagmanager\.com/gtm\?id") {
        $content = $content -replace "googletagmanager\.com/gtm\?id", "googletagmanager.com/gtm.js?id"
        $changed = $true
    }

    if ($changed) {
        Set-Content $_.FullName -Value $content
        Write-Host "Fixed: $($_.Name)"
    }
}
Write-Host "Done - GTM URLs restored."
