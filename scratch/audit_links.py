import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html"))
)

print(f"Auditing links in {len(html_files)} HTML files...")

href_pattern = re.compile(r'href=(["\'])(.*?)\1', re.IGNORECASE)

physical_links = []
clean_links = []
other_links = 0

for filepath in html_files:
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    if "diff" in rel_path.lower() or rel_path == "404.html" or rel_path == "admin.html":
        continue

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    for match in href_pattern.finditer(content):
        href = match.group(2)
        if (href.startswith('http') or href.startswith('#') or 
            href.startswith('tel:') or href.startswith('mailto:') or 
            href.startswith('sms:') or href.startswith('javascript:')):
            other_links += 1
            continue

        if href.endswith('.html') or '.html?' in href:
            physical_links.append((rel_path, href))
        else:
            clean_links.append((rel_path, href))

print(f"Audit completed:")
print(f"  Clean URLs (without .html): {len(clean_links)}")
print(f"  Physical URLs (with .html): {len(physical_links)}")
print(f"  Protocol/External URLs: {other_links}")

# Print sample clean links
if clean_links:
    print("\nSample clean links found:")
    for file, href in clean_links[:15]:
        print(f"  - In {file}: href=\"{href}\"")
