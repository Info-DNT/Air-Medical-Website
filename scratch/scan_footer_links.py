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

print(f"Scanning footer links in {len(html_files)} files...\n")

for f_path in html_files:
    rel_path = os.path.relpath(f_path, workspace_dir)
    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Find Quick Links or Popular Links sections
    # They are typically under an h4 like "Quick Links" or "Popular Links"
    # Let's search for '<h4 ...>Quick Links</h4>' or similar and grab the links in the div immediately following it.
    quick_links_match = re.search(r'Quick\s+Links</h4>([\s\S]*?)</div>', content, re.IGNORECASE)
    popular_links_match = re.search(r'Popular\s+Links</h4>([\s\S]*?)</div>', content, re.IGNORECASE)
    
    anomalies = []
    
    if quick_links_match:
        anchors = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>', quick_links_match.group(1))
        for href, text in anchors:
            text_clean = re.sub(r'<[^>]+>', '', text).strip()
            if href.startswith(('http', 'tel:', 'mailto:', 'javascript:')):
                continue
            if href in ('#', '#!', ''):
                anomalies.append(('Quick Links', text_clean, href))
                
    if popular_links_match:
        anchors = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>', popular_links_match.group(1))
        for href, text in anchors:
            text_clean = re.sub(r'<[^>]+>', '', text).strip()
            if href.startswith(('http', 'tel:', 'mailto:', 'javascript:')):
                continue
            if href in ('#', '#!', ''):
                anomalies.append(('Popular Links', text_clean, href))
                
    if anomalies:
        print(f"File: {rel_path}")
        for section, text, href in anomalies:
            print(f"  - [{section}] [{text}] -> {href}")
        print()
