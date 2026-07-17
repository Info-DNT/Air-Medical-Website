import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

all_files = []
for root, dirs, files in os.walk(workspace_dir):
    if ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith((".html", ".css", ".js", ".xml", ".txt", ".htaccess")):
            all_files.append(os.path.join(root, file))

pattern = re.compile(r"24/7|24[xX]7")

match_count = 0

for file_path in all_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        continue
        
    for match in pattern.finditer(content):
        match_count += 1
        start, end = match.span()
        context_start = max(0, start - 40)
        context_end = min(len(content), end + 40)
        context = content[context_start:context_end].replace('\n', ' ')
        safe_context = context.encode('ascii', errors='replace').decode('ascii')
        print(f"[{rel_path}] match='{match.group(0)}' context: ...{safe_context}...")

print(f"\nTotal raw matches listed: {match_count}")
