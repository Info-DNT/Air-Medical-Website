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

print(f"Verifying {len(html_files)} HTML files...")

has_errors = False

# 1. Verify router script is updated and contains the click interceptor
interceptor_marker = "Global Link Interceptor for Clean Extensionless Local Navigation"
for f_path in html_files:
    if "404.html" in f_path:
        continue
    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if interceptor_marker not in content:
        print(f"ERROR: Click interceptor not found in {os.path.relpath(f_path, workspace_dir)}")
        has_errors = True

# 2. Verify links do not have .html extensions or folder prefixes in anchor tags
# We will match href="..." and href='...' in all html files and check them.
double_quote_regex = re.compile(r'href="([^"]+)"')
single_quote_regex = re.compile(r"href='([^']+)'")

for f_path in html_files:
    rel_path = os.path.relpath(f_path, workspace_dir)
    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    matches = double_quote_regex.findall(content) + single_quote_regex.findall(content)
    for m in matches:
        # Ignore external links, mailto, tel, javascript, hash, and assets (like .css, .js, .png, etc.)
        if m.startswith(('http', 'tel:', 'mailto:', 'javascript:', '#')):
            continue
        # Allow assets (anything ending in .css, .png, .jpg, .js, etc. or containing subdirectories other than countries/services)
        if any(m.endswith(ext) for ext in ['.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.json', '.xml', '.ico']):
            continue
        if m.startswith(('css/', 'js/', 'img/', 'lib/', '../css/', '../js/', '../img/', '../lib/')):
            continue
            
        # Check if the internal link contains countries/, services/, or .html
        if 'countries/' in m or 'services/' in m or '.html' in m:
            print(f"ERROR: Dirty internal link found in {rel_path}: {m}")
            has_errors = True

if not has_errors:
    print("SUCCESS: All verification checks passed!")
else:
    print("FAILURE: Verification errors found.")
