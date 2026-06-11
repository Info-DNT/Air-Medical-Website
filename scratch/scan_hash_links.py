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

print(f"Scanning for hash/empty links in {len(html_files)} files...\n")

for f_path in html_files:
    rel_path = os.path.relpath(f_path, workspace_dir)
    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Match all href="#" or href="#!" or similar
    # We will search for href="..." and check if it's '#' or '#!'
    double_quote_regex = re.compile(r'href="([^"]+)"')
    single_quote_regex = re.compile(r"href='([^']+)'")
    
    matches = double_quote_regex.findall(content) + single_quote_regex.findall(content)
    hashes = [m for m in matches if m in ('#', '#!')]
    
    if hashes:
        # Let's find context around them
        # E.g. print the line content
        lines = content.splitlines()
        print(f"File: {rel_path}")
        for i, line in enumerate(lines):
            if 'href="#"' in line or "href='#'" in line or 'href="#!"' in line or "href='#!'" in line:
                print(f"  Line {i+1}: {line.strip()}")
        print()
