import os
import xml.etree.ElementTree as ET
import glob

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
sitemap_path = os.path.join(root_dir, "sitemap.xml")

# Parse sitemap URLs
tree = ET.parse(sitemap_path)
root = tree.getroot()
namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

sitemap_urls = []
for url in root.findall('ns:url', namespaces):
    loc = url.find('ns:loc', namespaces).text
    sitemap_urls.append(loc)

print(f"Total URLs in sitemap.xml: {len(sitemap_urls)}")

# Check clean URLs in sitemap.xml
print("\nFirst 15 Sitemap URLs:")
for u in sitemap_urls[:15]:
    print(f" - {u}")

# Find all HTML files recursively in workspace
all_html_files = []
for r, d, files in os.walk(root_dir):
    if ".git" in r or "scratch" in r:
        continue
    for f in files:
        if f.endswith(".html"):
            all_html_files.append(os.path.join(r, f))

print(f"\nTotal HTML files in workspace: {len(all_html_files)}")

# Map clean URLs to physical files
clean_to_physical = {}
# .htaccess routing rules:
# 1. countries/index.html -> /countries
# 2. countries/filename.html -> /filename
# 3. services/filename.html -> /filename
# 4. root/filename.html -> /filename
# Exception: /admin -> admin.html, index.html -> /

for filepath in all_html_files:
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
    
    if rel_path == "index.html":
        clean_url = "https://airmedical24x7.com/"
    elif rel_path == "countries/index.html":
        clean_url = "https://airmedical24x7.com/countries"
    elif rel_path.startswith("countries/"):
        clean_url = f"https://airmedical24x7.com/{filename_no_ext}"
    elif rel_path.startswith("services/"):
        clean_url = f"https://airmedical24x7.com/{filename_no_ext}"
    else:
        clean_url = f"https://airmedical24x7.com/{filename_no_ext}"
        
    clean_to_physical[clean_url] = rel_path

# Compare
print("\nHTML files NOT in sitemap.xml:")
for clean_url, physical in clean_to_physical.items():
    if clean_url not in sitemap_urls:
        print(f" - {physical} (routes to {clean_url})")

print("\nSitemap URLs NOT mapped to any physical HTML file:")
for u in sitemap_urls:
    if u not in clean_to_physical:
        print(f" - {u}")
