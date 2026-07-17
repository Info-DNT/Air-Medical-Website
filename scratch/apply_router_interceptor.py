import os
import re

workspace_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []
for root, dirs, files in os.walk(workspace_dir):
    if ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

print(f"Found {len(html_files)} HTML files to scan.")

router_regex = re.compile(r'<\s*script\s*>\s*\(function\s*\(\s*\)\s*\{[\s\S]*?var\s+pathname\s*=\s*window\.location\.pathname;[\s\S]*?\}\s*\)\s*\(\s*\)\s*;\s*<\s*/\s*script\s*>', re.IGNORECASE)

updated_count = 0

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    if rel_path == "404.html":
        continue
        
    # Determine the folder for baseHref
    if "countries" in rel_path:
        folder_prefix = "countries/"
    elif "services" in rel_path:
        folder_prefix = "services/"
    else:
        folder_prefix = ""
        
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    match = router_regex.search(content)
    if not match:
        print(f"WARNING: No matching router script found in {rel_path}")
        continue
        
    # Create the new script block using a standard template string
    new_script = """  <script>
    (function () {
      var pathname = window.location.pathname;
      var cleanPath = pathname;
      if (cleanPath.endsWith('.html')) {
        cleanPath = cleanPath.slice(0, -5);
      }
      if (cleanPath.endsWith('/index')) {
        cleanPath = cleanPath.slice(0, -6);
      }
      var basePath = '';
      if (window.location.hostname.indexOf('.github.io') !== -1) {
        var segments = pathname.split('/');
        if (segments.length > 1 && segments[1]) {
          basePath = '/' + segments[1];
        }
      }
      
      var countriesPrefix = basePath + '/countries/';
      var servicesPrefix = basePath + '/services/';
      if (cleanPath.startsWith(countriesPrefix) && cleanPath.length > countriesPrefix.length) {
        cleanPath = basePath + '/' + cleanPath.substring(countriesPrefix.length);
      } else if (cleanPath.startsWith(servicesPrefix) && cleanPath.length > servicesPrefix.length) {
        cleanPath = basePath + '/' + cleanPath.substring(servicesPrefix.length);
      }
      if (cleanPath === basePath + '/countries/index' || cleanPath === basePath + '/countries') {
        cleanPath = basePath + '/country';
      }
      var isDirRoot = (cleanPath === basePath || cleanPath === basePath + '/' || cleanPath === basePath + '/countries/' || cleanPath === '/');
      if (isDirRoot) {
        if (!cleanPath.endsWith('/')) {
          cleanPath += '/';
        }
      } else {
        if (cleanPath.endsWith('/') && cleanPath !== '/') {
          cleanPath = cleanPath.slice(0, -1);
        }
      }
      if (cleanPath === '') {
        cleanPath = '/';
      }
      if (cleanPath !== pathname) {
        window.history.replaceState(null, '', cleanPath + window.location.search + window.location.hash);
      }
      var currentFolder = '{{FOLDER}}';
      var baseHref = window.location.origin + basePath + '/' + currentFolder;
      document.write('<base href="' + baseHref + '">');

      // Global Link Interceptor for Clean Extensionless Local Navigation
      document.addEventListener('DOMContentLoaded', function() {
        document.body.addEventListener('click', function (e) {
          var anchor = e.target.closest('a');
          if (!anchor) return;
          var href = anchor.getAttribute('href');
          if (!href) return;
          
          if (href.startsWith('http') || href.startsWith('#') || href.startsWith('tel:') || href.startsWith('mailto:') || href.startsWith('sms:') || href.startsWith('javascript:')) {
            return;
          }
          
          var parts = href.split('?');
          var cleanHref = parts[0].split('#')[0];
          var queryHashPart = href.substring(parts[0].length);
          
          if (cleanHref.startsWith('/')) {
            cleanHref = cleanHref.substring(1);
          }
          if (cleanHref === '') {
            cleanHref = 'index';
          }
          
          var targetPath = '';
          if (cleanHref === 'country') {
            targetPath = 'countries/index.html';
          } else if (cleanHref.startsWith('air-ambulance-') && cleanHref !== 'air-ambulance-charters') {
            targetPath = 'countries/' + cleanHref + '.html';
          } else {
            var services = [
              'air-ambulance', 'air-ambulance-charters', 'ECMO-transfer', 
              'commercial-airlines-medical-transfer-services', 'commercial-flight-stretcher', 
              'custom-medical-packages', 'doctor-appointment', 'flight-medical-escort-service', 
              'hospital-acceptance', 'medical-tourism-services', 'second-opinion-services'
            ];
            if (services.indexOf(cleanHref) !== -1) {
              targetPath = 'services/' + cleanHref + '.html';
            } else {
              if (cleanHref.indexOf('.') !== -1) {
                targetPath = cleanHref;
              } else {
                targetPath = cleanHref + '.html';
              }
            }
          }
          
          var finalUrl = targetPath;
          if (currentFolder === 'countries/') {
            if (targetPath.startsWith('countries/')) {
              finalUrl = targetPath.substring(10);
            } else {
              finalUrl = '../' + targetPath;
            }
          } else if (currentFolder === 'services/') {
            if (targetPath.startsWith('services/')) {
              finalUrl = targetPath.substring(9);
            } else {
              finalUrl = '../' + targetPath;
            }
          }
          
          e.preventDefault();
          window.location.href = finalUrl + queryHashPart;
        });
      });
    })();
  </script>""".replace("{{FOLDER}}", folder_prefix)
    
    new_content = content.replace(match.group(0), new_script)
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1
        print(f"Updated router in {rel_path}")

print(f"Successfully updated router in {updated_count} files.")
