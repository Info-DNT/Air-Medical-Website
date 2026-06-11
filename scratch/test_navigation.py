# Simulate the fixed router navigation logic
def simulate_navigation_fixed(current_pathname, href, folder_prefix):
    # folder_prefix: physical folder of the current page ('countries/', 'services/', '')
    
    # Simulating click interceptor with fixed logic
    currentFolder = folder_prefix # In JS this is '{{FOLDER}}' which is hardcoded per file
    
    parts = href.split('?')
    cleanHref = parts[0].split('#')[0]
    queryHashPart = href[len(parts[0]):]
    
    if cleanHref.startswith('/'):
        cleanHref = cleanHref[1:]
    if cleanHref == '':
        cleanHref = 'index'
        
    targetPath = ''
    if cleanHref == 'country':
        targetPath = 'countries/index.html'
    elif cleanHref.startswith('air-ambulance-') and cleanHref != 'air-ambulance-charters':
        targetPath = 'countries/' + cleanHref + '.html'
    else:
        services = [
            'air-ambulance', 'air-ambulance-charters', 'ECMO-transfer', 
            'commercial-airlines-medical-transfer-services', 'commercial-flight-stretcher', 
            'custom-medical-packages', 'doctor-appointment', 'flight-medical-escort-service', 
            'hospital-acceptance', 'medical-tourism-services', 'second-opinion-services'
        ]
        if cleanHref in services:
            targetPath = 'services/' + cleanHref + '.html'
        else:
            if '.' in cleanHref:
                targetPath = cleanHref
            else:
                targetPath = cleanHref + '.html'
                
    finalUrl = targetPath
    if currentFolder == 'countries/':
        if targetPath.startswith('countries/'):
            finalUrl = targetPath[10:]
        else:
            finalUrl = '../' + targetPath
    elif currentFolder == 'services/':
        if targetPath.startswith('services/'):
            finalUrl = targetPath[9:]
        else:
            finalUrl = '../' + targetPath
            
    # Browser resolves finalUrl relative to <base href>
    # baseHref is window.location.origin + basePath + '/' + currentFolder
    baseHref = f"http://localhost:3000/{currentFolder}"
    # Simple relative path resolution:
    if finalUrl.startswith('../'):
        # resolve one level up from currentFolder
        resolved = f"http://localhost:3000/{finalUrl[3:]}"
    else:
        resolved = f"http://localhost:3000/{currentFolder}{finalUrl}"
        
    return {
        'currentFolder': currentFolder,
        'targetPath': targetPath,
        'finalUrl': finalUrl,
        'resolved_url': resolved
    }

# Test navigation from services/air-ambulance.html (folder_prefix='services/')
res1 = simulate_navigation_fixed('/services/air-ambulance.html', 'about-us', 'services/')
print("Fixed navigation from services/air-ambulance.html to 'about-us':")
for k, v in res1.items():
    print(f"  {k}: {v}")

print()

# Test navigation from services/air-ambulance.html to another service page (e.g. 'ECMO-transfer')
res2 = simulate_navigation_fixed('/services/air-ambulance.html', 'ECMO-transfer', 'services/')
print("Fixed navigation from services/air-ambulance.html to 'ECMO-transfer':")
for k, v in res2.items():
    print(f"  {k}: {v}")

print()

# Test navigation from countries/air-ambulance-afghanistan.html to 'about-us'
res3 = simulate_navigation_fixed('/countries/air-ambulance-afghanistan.html', 'about-us', 'countries/')
print("Fixed navigation from countries/air-ambulance-afghanistan.html to 'about-us':")
for k, v in res3.items():
    print(f"  {k}: {v}")

print()

# Test navigation from countries/air-ambulance-afghanistan.html to 'air-ambulance-albania'
res4 = simulate_navigation_fixed('/countries/air-ambulance-afghanistan.html', 'air-ambulance-albania', 'countries/')
print("Fixed navigation from countries/air-ambulance-afghanistan.html to 'air-ambulance-albania':")
for k, v in res4.items():
    print(f"  {k}: {v}")
