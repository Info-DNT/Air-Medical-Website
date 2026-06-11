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

print(f"Found {len(html_files)} HTML files to update links in.")

stats = {}

def track_change(file_rel, key):
    stats[key] = stats.get(key, 0) + 1

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    file_type = "root"
    if "countries" in rel_path:
        if rel_path == os.path.join("countries", "index.html"):
            file_type = "countries_index"
        else:
            file_type = "countries"
    elif "services" in rel_path:
        file_type = "services"
        
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    new_content = content
    
    # 1. Update absolute canonical/schema URLs in all files
    # Remove /countries/ and /services/ from airmedical24x7.com links
    matches_abs_countries = re.findall(r'https://airmedical24x7\.com/countries/([^"\']*)', new_content)
    for m in matches_abs_countries:
        orig = f"https://airmedical24x7.com/countries/{m}"
        new = f"https://airmedical24x7.com/{m}"
        track_change(rel_path, f"abs_countries_url_to_clean")
        new_content = new_content.replace(orig, new)
        
    matches_abs_services = re.findall(r'https://airmedical24x7\.com/services/([^"\']*)', new_content)
    for m in matches_abs_services:
        orig = f"https://airmedical24x7.com/services/{m}"
        new = f"https://airmedical24x7.com/{m}"
        track_change(rel_path, f"abs_services_url_to_clean")
        new_content = new_content.replace(orig, new)
        
    # 2. Update relative links based on file location
    if file_type == "root":
        # countries/air-ambulance-*.html -> air-ambulance-*.html
        # countries/index.html -> country.html
        # services/*.html -> *.html
        
        # Link to country index
        if 'href="countries/index.html"' in new_content:
            new_content = new_content.replace('href="countries/index.html"', 'href="country.html"')
            track_change(rel_path, "root_countries_index_to_country")
        if "href='countries/index.html'" in new_content:
            new_content = new_content.replace("href='countries/index.html'", "href='country.html'")
            track_change(rel_path, "root_countries_index_to_country")
            
        # Link to other country pages
        hrefs = re.findall(r'href=["\'](countries/[^"\']+)["\']', new_content)
        for h in hrefs:
            if h.startswith("countries/"):
                new = h.replace("countries/", "")
                new_content = new_content.replace(f'href="{h}"', f'href="{new}"')
                new_content = new_content.replace(f"href='{h}'", f"href='{new}'")
                track_change(rel_path, "root_country_link_prefix_strip")
                
        # Link to services
        hrefs = re.findall(r'href=["\'](services/[^"\']+)["\']', new_content)
        for h in hrefs:
            if h.startswith("services/"):
                new = h.replace("services/", "")
                new_content = new_content.replace(f'href="{h}"', f'href="{new}"')
                new_content = new_content.replace(f"href='{h}'", f"href='{new}'")
                track_change(rel_path, "root_service_link_prefix_strip")
                
    elif file_type in ("countries", "countries_index"):
        # ../services/*.html -> ../*.html
        # ../countries/index.html -> ../country.html
        # href="./" -> href="../country.html" in footer
        
        # ../countries/index.html
        if 'href="../countries/index.html"' in new_content:
            new_content = new_content.replace('href="../countries/index.html"', 'href="../country.html"')
            track_change(rel_path, "countries_index_link_to_country")
        if "href='../countries/index.html'" in new_content:
            new_content = new_content.replace("href='../countries/index.html'", "href='../country.html'")
            track_change(rel_path, "countries_index_link_to_country")
            
        # href="./" (only replace the Global Pages link in footer, wait - let's check if there are others)
        # We can specifically target href="./" where it says "Global Pages"
        if 'href="./">Global Pages' in new_content:
            new_content = new_content.replace('href="./">Global Pages', 'href="../country.html">Global Pages')
            track_change(rel_path, "countries_dot_slash_to_country")
        elif 'href="./"><i class="fa fa-angle-right me-2"></i>Global Pages' in new_content:
            new_content = new_content.replace('href="./"><i class="fa fa-angle-right me-2"></i>Global Pages', 'href="../country.html"><i class="fa fa-angle-right me-2"></i>Global Pages')
            track_change(rel_path, "countries_dot_slash_to_country")
            
        # services links
        hrefs = re.findall(r'href=["\'](\.\./services/[^"\']+)["\']', new_content)
        for h in hrefs:
            new = h.replace("../services/", "../")
            new_content = new_content.replace(f'href="{h}"', f'href="{new}"')
            new_content = new_content.replace(f"href='{h}'", f"href='{new}'")
            track_change(rel_path, "countries_services_link_prefix_strip")
            
    elif file_type == "services":
        # ../countries/index.html -> ../country.html
        # Links within services folder: e.g. ECMO-transfer.html -> ../ECMO-transfer.html
        
        if 'href="../countries/index.html"' in new_content:
            new_content = new_content.replace('href="../countries/index.html"', 'href="../country.html"')
            track_change(rel_path, "services_countries_index_link_to_country")
        if "href='../countries/index.html'" in new_content:
            new_content = new_content.replace("href='../countries/index.html'", "href='../country.html'")
            track_change(rel_path, "services_countries_index_link_to_country")
            
        # Find local service links (like ECMO-transfer.html, but not starting with http, #, or ..)
        # Let's inspect links that end in .html and do not contain /
        hrefs = re.findall(r'href=["\']([^"\':#\./]+?\.html)["\']', new_content)
        for h in hrefs:
            new = f"../{h}"
            new_content = new_content.replace(f'href="{h}"', f'href="{new}"')
            new_content = new_content.replace(f"href='{h}'", f"href='{new}'")
            track_change(rel_path, "services_local_link_to_root_rel")
            
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated links in {rel_path}")

print("\n--- Link Replacements Stats ---")
for key, val in sorted(stats.items()):
    print(f"  {key}: {val} occurrences")
