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

print(f"Scanning all footer anchors in {len(html_files)} files...\n")

for f_path in html_files:
    rel_path = os.path.relpath(f_path, workspace_dir)
    if rel_path == "404.html":
        continue
        
    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Search for Footer Start to Footer End/script/body end
    # We can search for '<!-- Footer Start -->' to '<!-- Footer End -->'
    footer_match = re.search(r'<!--\s*Footer\s*Start\s*-->([\s\S]*?)<!--\s*Footer\s*End\s*-->', content, re.IGNORECASE)
    footer_bottom_match = re.search(r'<!--\s*Footer\s*Bottom\s*-->([\s\S]*?)</div>\s*</div>\s*</div>', content, re.IGNORECASE)
    
    anomalies = []
    
    def check_anchors(html_block, section_name):
        anchors = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>', html_block)
        for href, text in anchors:
            text_clean = re.sub(r'<[^>]+>', '', text).strip()
            text_clean = " ".join(text_clean.split())
            if href.startswith(('http', 'tel:', 'mailto:', 'javascript:')):
                continue
            # If it's a relative link, check its correctness
            if href in ('#', '#!', ''):
                anomalies.append((section_name, text_clean, href))
            # Check for incorrect relative paths depending on directory depth
            if "countries" in rel_path or "services" in rel_path:
                # Subdirectory files should use '../' for Home and Copyright links if they target the root
                if (text_clean == "Home" or text_clean == "Air Medical 24X7") and href != '../':
                    anomalies.append((section_name, f"{text_clean} (expected '../' in subfolder)", href))
            else:
                # Root files should use './' or similar for Home and Copyright links
                if (text_clean == "Home" or text_clean == "Air Medical 24X7") and href != './':
                    anomalies.append((section_name, f"{text_clean} (expected './' at root)", href))

    if footer_match:
        check_anchors(footer_match.group(1), 'Footer Main')
    else:
        print(f"WARNING: Footer Start comment not found in {rel_path}")
        
    if footer_bottom_match:
        check_anchors(footer_bottom_match.group(1), 'Footer Bottom')
    else:
        # If footer bottom comment is not there, check if there's a copyright text near the end of footer
        pass

    # Let's also check for any comments or blocks containing footer bottom
    # Often, the Copyright is in a separate container after Footer End
    copyright_match = re.search(r'<!--\s*Footer\s*Bottom\s*-->([\s\S]*?)</div>\s*</div>\s*</div>|border-top\s+border-secondary\s+py-4[\s\S]*?&copy;([\s\S]*?)</div>', content, re.IGNORECASE)
    if copyright_match:
        block = copyright_match.group(0)
        # Search for any anchors in this block
        anchors = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>', block)
        for href, text in anchors:
            text_clean = re.sub(r'<[^>]+>', '', text).strip()
            text_clean = " ".join(text_clean.split())
            if href.startswith(('http', 'tel:', 'mailto:', 'javascript:')):
                continue
            if "countries" in rel_path or "services" in rel_path:
                if (text_clean == "Air Medical 24X7" or text_clean == "Home") and href != '../':
                    anomalies.append(('Footer Copyright', f"{text_clean} (expected '../')", href))
            else:
                if (text_clean == "Air Medical 24X7" or text_clean == "Home") and href != './':
                    anomalies.append(('Footer Copyright', f"{text_clean} (expected './')", href))

    if anomalies:
        print(f"File: {rel_path}")
        for section, text, href in anomalies:
            print(f"  - [{section}] [{text}] -> {href}")
        print()
