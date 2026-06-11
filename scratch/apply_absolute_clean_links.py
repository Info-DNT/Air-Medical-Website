import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html"))
)

print(f"Total HTML files to process: {len(html_files)}")

# 1. Regex patterns for all service and country page links to make them root-relative absolute clean URLs
# E.g. href="air-ambulance" -> href="/air-ambulance"
# E.g. href="../air-ambulance" -> href="/air-ambulance"
# E.g. href="air-ambulance.html" -> href="/air-ambulance"

services = [
    'air-ambulance', 'air-ambulance-charters', 'commercial-flight-stretcher',
    'flight-medical-escort-services', 'hospital-acceptance', 'doctor-appointment',
    'second-opinion-services', 'custom-medical-packages', 'ecmo-transfer',
    'commercial-airlines-medical-transfer-services', 'medical-tourism-services',
    'medical-escort-dubai', 'commercial-stretcher-service', 'ecmo-air-transfer',
    'repatriation-services-dubai', 'medical-tourism-india', 'ECMO-transfer',
    'airline-stretcher-services'
]

# We also want to match any country URL e.g. air-ambulance-afghanistan
# And core pages
core_pages = [
    'about-us', 'contact-us', 'career', 'blogs', 'blogs-detail', 'countries',
    'privacy-policy', 'terms-and-conditions'
]

def clean_href(href_val):
    # If absolute web link or hash/phone/mail, do not modify
    if (href_val.startswith('http') or href_val.startswith('#') or 
        href_val.startswith('tel:') or href_val.startswith('mailto:') or 
        href_val.startswith('sms:') or href_val.startswith('javascript:')):
        return href_val
        
    parts = href_val.split('?')
    clean_part = parts[0].split('#')[0]
    query_hash_part = href_val[len(clean_part):]
    
    # Strip leading/trailing slashes or relative parent dirs
    clean_part = clean_part.replace('../', '').replace('./', '')
    if clean_part.endswith('.html'):
        clean_part = clean_part[:-5]
        
    if clean_part.startswith('countries/'):
        clean_part = clean_part[10:]
    elif clean_part.startswith('services/'):
        clean_part = clean_part[9:]
        
    if clean_part == 'index' or clean_part == '':
        return '/' + query_hash_part
        
    # Standardize ECMO-transfer -> ecmo-transfer, airline-stretcher-services -> commercial-flight-stretcher
    if clean_part == 'ECMO-transfer':
        clean_part = 'ecmo-transfer'
    elif clean_part == 'airline-stretcher-services':
        clean_part = 'commercial-flight-stretcher'
        
    return '/' + clean_part + query_hash_part

def process_content(content):
    # Regex to find all href="..." in anchors
    # We want to be careful to only target anchor hrefs
    def repl_href(match):
        full_match = match.group(0)
        quote_char = match.group(1)
        href_val = match.group(2)
        
        cleaned = clean_href(href_val)
        return f'href={quote_char}{cleaned}{quote_char}'
        
    content = re.sub(r'href=(["\'])(.*?)\1', repl_href, content, flags=re.IGNORECASE)
    return content

def remove_interceptor_script(content):
    # Regex to find the <script> block at the very start of <head> and replace it with a clean history clean path script
    # The block starts with (function () { var pathname = window.location.pathname; ... and ends with })(); </script>
    
    clean_history_script = """  <script>
    (function () {
      var pathname = window.location.pathname;
      var cleanPath = pathname;
      if (cleanPath.endsWith('.html')) {
        cleanPath = cleanPath.slice(0, -5);
      }
      if (cleanPath.endsWith('/index')) {
        cleanPath = cleanPath.slice(0, -6);
      }
      if (cleanPath !== pathname) {
        window.history.replaceState(null, '', cleanPath + window.location.search + window.location.hash);
      }
    })();
  </script>"""
    
    # Look for the block enclosing "Global Link Interceptor for Clean Extensionless Local Navigation"
    interceptor_pattern = r'<script>\s*\(function\s*\(\)\s*\{\s*var\s*pathname\s*=\s*window\.location\.pathname;.*?Global\s+Link\s+Interceptor.*?\}\)\(\);\s*</script>'
    
    # Run a dotall search
    if re.search(interceptor_pattern, content, re.DOTALL | re.IGNORECASE):
        content = re.sub(interceptor_pattern, clean_history_script, content, flags=re.DOTALL | re.IGNORECASE)
    else:
        # Alt check: let's replace by mapping standard start/end
        alt_pattern = r'<script>\s*\(function\s*\(\)\s*\{\s*var\s*pathname\s*=\s*window\.location\.pathname;.*?document\.write\(.*?baseHref.*?\);.*?\}\)\(\);\s*</script>'
        content = re.sub(alt_pattern, clean_history_script, content, flags=re.DOTALL | re.IGNORECASE)
        
    return content

for filepath in html_files:
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    if "diff" in rel_path.lower() or rel_path == "404.html" or rel_path == "admin.html":
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # 1. Update all links
    content = process_content(content)
    
    # 2. Remove client-side JS link routing interceptor
    content = remove_interceptor_script(content)
    
    # 3. Specifically replace config.js and main.js relative paths to absolute root-relative paths in the footer
    # Since we removed <base href>, relative scripts like '../js/main.js' or 'js/main.js' must be absolute '/js/main.js'!
    # Let's do this search and replace
    content = content.replace('src="js/main.js"', 'src="/js/main.js"')
    content = content.replace('src="../js/main.js"', 'src="/js/main.js"')
    content = content.replace('src="js/config.js"', 'src="/js/config.js"')
    content = content.replace('src="../js/config.js"', 'src="/js/config.js"')
    
    # Replace other library scripts
    content = content.replace('src="lib/', 'src="/lib/')
    content = content.replace('src="../lib/', 'src="/lib/')
    
    # Replace stylesheets
    content = content.replace('href="css/', 'href="/css/')
    content = content.replace('href="../css/', 'href="/css/')
    content = content.replace('href="lib/', 'href="/lib/')
    content = content.replace('href="../lib/', 'href="/lib/')
    content = content.replace('href="img/airmedicallogo.png"', 'href="/img/airmedicallogo.png"')
    content = content.replace('href="../img/airmedicallogo.png"', 'href="/img/airmedicallogo.png"')
    content = content.replace('href="img/air-medical-logo.png"', 'href="/img/air-medical-logo.png"')
    content = content.replace('href="../img/air-medical-logo.png"', 'href="/img/air-medical-logo.png"')
    
    # Replace images in footers and headers
    content = content.replace('src="img/', 'src="/img/')
    content = content.replace('src="../img/', 'src="/img/')

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Cleaned Links: {rel_path}")
    else:
        print(f"No Link Changes: {rel_path}")

print("Absolute clean link processing completed.")
