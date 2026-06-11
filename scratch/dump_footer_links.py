import os
import re
from collections import defaultdict

workspace_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []
for root, dirs, files in os.walk(workspace_dir):
    if ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

print(f"Analyzing footer links in {len(html_files)} files...\n")

footer_contents = defaultdict(list)

for f_path in html_files:
    rel_path = os.path.relpath(f_path, workspace_dir)
    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Grab Quick Links section
    quick_match = re.search(r'Quick\s+Links</h4>([\s\S]*?)</div>', content, re.IGNORECASE)
    # Grab Popular Links section
    popular_match = re.search(r'Popular\s+Links</h4>([\s\S]*?)</div>', content, re.IGNORECASE)
    
    quick_links = []
    if quick_match:
        anchors = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>', quick_match.group(1))
        for href, text in anchors:
            text_clean = re.sub(r'<[^>]+>', '', text).strip()
            quick_links.append((text_clean, href))
            
    popular_links = []
    if popular_match:
        anchors = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>', popular_match.group(1))
        for href, text in anchors:
            text_clean = re.sub(r'<[^>]+>', '', text).strip()
            popular_links.append((text_clean, href))
            
    key = (tuple(quick_links), tuple(popular_links))
    footer_contents[key].append(rel_path)

print(f"Found {len(footer_contents)} distinct footer patterns:\n")

for i, (key, files) in enumerate(footer_contents.items(), 1):
    quick_links, popular_links = key
    print(f"Pattern #{i} (Present in {len(files)} files):")
    print(f"Files (sample up to 5): {files[:5]}")
    print("  Quick Links:")
    for text, href in quick_links:
        print(f"    - {text} -> {href}")
    print("  Popular Links:")
    for text, href in popular_links:
        print(f"    - {text} -> {href}")
    print("-" * 50)
