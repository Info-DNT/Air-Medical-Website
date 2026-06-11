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

print(f"Total HTML files to process: {len(html_files)}")

# Stats counters
link_replacements = {}

def track_replacement(file_type, orig, new):
    key = f"[{file_type}] {orig} -> {new}"
    link_replacements[key] = link_replacements.get(key, 0) + 1

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    file_type = "root"
    if "countries" in rel_path:
        file_type = "countries"
    elif "services" in rel_path:
        file_type = "services"
        
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    new_content = content
    
    # 1. Replace absolute canonical/schema URLs
    # https://airmedical24x7.com/countries/air-ambulance-something -> https://airmedical24x7.com/air-ambulance-something
    # https://airmedical24x7.com/services/something -> https://airmedical24x7.com/something
    matches_abs_countries = re.findall(r'https://airmedical24x7\.com/countries/([^"\']*)', new_content)
    for m in matches_abs_countries:
        orig = f"https://airmedical24x7.com/countries/{m}"
        new = f"https://airmedical24x7.com/{m}"
        track_replacement(f"{file_type}_abs", orig, new)
        new_content = new_content.replace(orig, new)
        
    matches_abs_services = re.findall(r'https://airmedical24x7\.com/services/([^"\']*)', new_content)
    for m in matches_abs_services:
        orig = f"https://airmedical24x7.com/services/{m}"
        new = f"https://airmedical24x7.com/{m}"
        track_replacement(f"{file_type}_abs", orig, new)
        new_content = new_content.replace(orig, new)
        
    # 2. Replace relative links
    if file_type == "root":
        # countries/air-ambulance-*.html -> air-ambulance-*.html
        # services/*.html -> *.html
        # countries/index.html -> country.html
        
        # We can find href="countries/index.html"
        hrefs = re.findall(r'href=["\'](countries/[^"\']+)["\']', new_content)
        for h in hrefs:
            if h == "countries/index.html":
                new = "country.html"
            elif h.startswith("countries/"):
                new = h.replace("countries/", "")
            else:
                continue
            track_replacement("root_rel", f'href="{h}"', f'href="{new}"')
            new_content = new_content.replace(f'href="{h}"', f'href="{new}"')
            new_content = new_content.replace(f"href='{h}'", f"href='{new}'")
            
        hrefs = re.findall(r'href=["\'](services/[^"\']+)["\']', new_content)
        for h in hrefs:
            new = h.replace("services/", "")
            track_replacement("root_rel", f'href="{h}"', f'href="{new}"')
            new_content = new_content.replace(f'href="{h}"', f'href="{new}"')
            new_content = new_content.replace(f"href='{h}'", f"href='{new}'")
            
    elif file_type == "countries":
        # ../services/*.html -> ../*.html
        # ../countries/index.html -> ../country.html
        # href="./" -> href="../country.html"
        
        hrefs = re.findall(r'href=["\'](\.\./services/[^"\']+)["\']', new_content)
        for h in hrefs:
            new = h.replace("../services/", "../")
            track_replacement("countries_rel", f'href="{h}"', f'href="{new}"')
            new_content = new_content.replace(f'href="{h}"', f'href="{new}"')
            new_content = new_content.replace(f"href='{h}'", f"href='{new}'")
            
        # Global Pages link: href="./" in footer
        # Let's check for href="./" in footer and replace with href="../country.html"
        # Wait, is href="./" only used for Global Pages? Let's check!
        # Let's inspect where href="./" occurs in countries files.
        
    elif file_type == "services":
        # href="some-service.html" -> href="../some-service.html"
        # href="../countries/index.html" -> href="../country.html"
        
        # Since service files are inside services/ directory:
        # A relative href that does not start with http, #, or .. is relative to services/
        # So we should prepend ../ to make it relative to root
        hrefs = re.findall(r'href=["\']([^"\':#\.]+?\.html)["\']', new_content)
        for h in hrefs:
            if not h.startswith("..") and not h.startswith("http"):
                new = f"../{h}"
                track_replacement("services_rel", f'href="{h}"', f'href="{new}"')
                new_content = new_content.replace(f'href="{h}"', f'href="{new}"')
                new_content = new_content.replace(f"href='{h}'", f"href='{new}'")
                
        # Also replace ../countries/index.html with ../country.html
        if 'href="../countries/index.html"' in new_content:
            track_replacement("services_rel", 'href="../countries/index.html"', 'href="../country.html"')
            new_content = new_content.replace('href="../countries/index.html"', 'href="../country.html"')
        if "href='../countries/index.html'" in new_content:
            track_replacement("services_rel", "href='../countries/index.html'", "href='../country.html'")
            new_content = new_content.replace("href='../countries/index.html'", "href='../country.html'")

print("\n--- Link Replacements Dry Run ---")
for key, count in sorted(link_replacements.items(), key=lambda x: x[0]):
    print(f"{key}: {count} occurrences")
