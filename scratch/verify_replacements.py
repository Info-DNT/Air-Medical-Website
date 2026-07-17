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

pattern_24_7 = re.compile(r"24/7", re.IGNORECASE)
pattern_24x7 = re.compile(r"24x7", re.IGNORECASE)

remaining = []

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Check for 24/7
    for m in pattern_24_7.finditer(content):
        start = max(0, m.start() - 40)
        end = min(len(content), m.end() + 40)
        context = content[start:end].replace('\n', ' ')
        remaining.append(f"[24/7] {rel_path}: {context}")
        
    # Check for 24x7 that is NOT part of airmedical24x7 or similar URL/email/directory structures
    for m in pattern_24x7.finditer(content):
        matched_str = m.group(0)
        if matched_str == "24X7":
            continue
            
        start_pos = max(0, m.start() - 20)
        end_pos = min(len(content), m.end() + 20)
        surrounding = content[start_pos:end_pos].lower()
        if "airmedical24x7" in surrounding or "airmedical_24x7" in surrounding or "airmedical-24x7" in surrounding:
            continue
        
        start = max(0, m.start() - 40)
        end = min(len(content), m.end() + 40)
        context = content[start:end].replace('\n', ' ')
        remaining.append(f"[{matched_str}] {rel_path}: {context}")

if remaining:
    print(f"Found {len(remaining)} occurrences of 24/7 or 24x7 remaining:")
    for rem in remaining:
        print(rem)
else:
    print("Success! No remaining occurrences of 24/7 or 24x7 found in the workspace (excluding domain/email).")
