$basePath = 'c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main'

# Canonical 8-option dropdown inner HTML
$canonicalOptions = "
                    <option value=`"`">Select a Service</option>
                    <option value=`"Air Ambulance`">Air Ambulance</option>
                    <option value=`"Airline Stretcher Services`">Airline Stretcher Services</option>
                    <option value=`"Flight Medical Escort Services`">Flight Medical Escort Services</option>
                    <option value=`"ECMO Transfer Services`">ECMO Transfer Services</option>
                    <option value=`"Organ Transplant Assistance`">Organ Transplant Assistance</option>
                    <option value=`"Medical Tourism`">Medical Tourism</option>
                    <option value=`"Medical Travel Assistance`">Medical Travel Assistance</option>
                    <option value=`"Home Health Care`">Home Health Care</option>
                  "

$files = @(
  'services\air-ambulance.html',
  'services\air-ambulance-charters.html',
  'services\commercial-airlines-medical-transfer-services.html',
  'services\commercial-flight-stretcher.html',
  'services\custom-medical-packages.html',
  'services\doctor-appointment.html',
  'services\ECMO-transfer.html',
  'services\flight-medical-escort-services.html',
  'services\hospital-acceptance.html',
  'services\medical-tourism-services.html',
  'services\second-opinion-services.html',
  'countries.html',
  'about-us.html',
  'blogs-detail.html',
  'commercial-stretcher-service.html',
  'ecmo-air-transfer.html',
  'medical-escort-dubai.html',
  'medical-tourism-india.html',
  'repatriation-services-dubai.html',
  'countries\index.html',
  'countries\air-ambulance-bahrain.html',
  'countries\air-ambulance-dubai.html',
  'countries\air-ambulance-cost-dubai.html',
  'countries\air-ambulance-india.html',
  'countries\air-ambulance-to-india.html'
)

$pattern = '(?s)(<select[^>]*name="service"[^>]*>)(.*?)(</select>)'

$totalUpdated = 0

foreach ($file in $files) {
  $fullPath = Join-Path $basePath $file
  if (-not (Test-Path $fullPath)) {
    Write-Host "SKIP (not found): $file"
    continue
  }
  
  $content = [System.IO.File]::ReadAllText($fullPath, [System.Text.Encoding]::UTF8)
  
  if ($content -notmatch 'name="service"') {
    Write-Host "SKIP (no service select): $file"
    continue
  }
  
  $newContent = [regex]::Replace($content, $pattern, {
    param($m)
    return $m.Groups[1].Value + $canonicalOptions + $m.Groups[3].Value
  }, [System.Text.RegularExpressions.RegexOptions]::Singleline)
  
  if ($newContent -ne $content) {
    [System.IO.File]::WriteAllText($fullPath, $newContent, [System.Text.Encoding]::UTF8)
    Write-Host "UPDATED: $file"
    $totalUpdated++
  } else {
    Write-Host "NO CHANGE: $file"
  }
}

Write-Host ""
Write-Host "Done. Updated $totalUpdated files."
