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

pattern = re.compile(r"24x7")

lowercase_occurrences = []

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            matches = list(pattern.finditer(line))
            for m in matches:
                lowercase_occurrences.append((rel_path, idx + 1, line.strip()))

print(f"Found {len(lowercase_occurrences)} total occurrences of lowercase '24x7':\n")
for file, line_num, line_content in lowercase_occurrences[:50]:
    print(f"[{file}:{line_num}] {line_content}")
if len(lowercase_occurrences) > 50:
    print(f"... and {len(lowercase_occurrences) - 50} more occurrences")
