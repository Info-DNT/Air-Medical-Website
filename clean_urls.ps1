$base = 'c:/Users/Admin/Downloads/airmedical_24X7_jeet-main/airmedical_24X7_jeet-main'
Get-ChildItem -Path $base -Recurse -Filter *.html | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $content = $content -replace 'href="([^\"]+)\.html"', 'href="$1"'
    $content = $content -replace 'src="([^\"]+)\.html"', 'src="$1"'
    $content = $content -replace '<link rel="canonical" href="([^\"]+)\.html"', '<link rel="canonical" href="$1"'
    $content = $content -replace 'https://www.googletagmanager.com/gtm5445.html', 'https://www.googletagmanager.com/gtm.js'
    $content = $content -replace '(?<!https?:)\.html', ''
    Set-Content $_.FullName -Value $content
}
