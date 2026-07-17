import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
html_files = []

for root, dirs, files in os.walk(root_dir):
    if ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

# Regex to find href attributes
href_pattern = re.compile(r'href=["\']([^"\']+)["\']')

countries_by_dir = {"root": set(), "countries": set(), "services": set()}
services_by_dir = {"root": set(), "countries": set(), "services": set()}

for file_path in html_files:
    rel_path = os.path.relpath(file_path, root_dir)
    dir_type = "root"
    if "countries" in rel_path:
        dir_type = "countries"
    elif "services" in rel_path:
        dir_type = "services"
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {rel_path}: {e}")
        continue
    
    matches = href_pattern.findall(content)
    for match in matches:
        if "countries/" in match:
            countries_by_dir[dir_type].add(match)
        if "services/" in match:
            services_by_dir[dir_type].add(match)

print("\n--- Countries Links by Directory Level ---")
for key, vals in countries_by_dir.items():
    print(f"\nDirectory level: {key} ({len(vals)} unique links)")
    for val in sorted(list(vals)):
        print(f"  {val}")

print("\n--- Services Links by Directory Level ---")
for key, vals in services_by_dir.items():
    print(f"\nDirectory level: {key} ({len(vals)} unique links)")
    for val in sorted(list(vals)):
        print(f"  {val}")
