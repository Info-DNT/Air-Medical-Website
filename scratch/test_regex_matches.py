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

# Regex patterns with word boundary
pattern_24_7 = re.compile(r"\b24/7\b", re.IGNORECASE)
pattern_24x7 = re.compile(r"\b24[xX]7\b")  # We only target 24x7, 24X7, etc.

matches_count = 0
matches_details = []

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
        # Find all occurrences of 24/7
        for m in pattern_24_7.finditer(content):
            start = max(0, m.start() - 40)
            end = min(len(content), m.end() + 40)
            context = content[start:end].replace('\n', ' ')
            matches_details.append(f"[24/7] {rel_path}: ...{context}...")
            matches_count += 1
            
        # Find all occurrences of 24x7 (case-insensitive, excluding already uppercase 24X7 if we want, but let's see all first)
        # Wait, the user wants all 24x7 and 24/7 to be exactly "24X7". So if it's already "24X7", we don't need to change it,
        # but let's find all case-insensitive variations first.
        pattern_24x7_all = re.compile(r"\b24[xX]7\b", re.IGNORECASE)
        for m in pattern_24x7_all.finditer(content):
            # Skip if it is already exactly "24X7"
            if m.group(0) == "24X7":
                continue
            start = max(0, m.start() - 40)
            end = min(len(content), m.end() + 40)
            context = content[start:end].replace('\n', ' ')
            matches_details.append(f"[24x7] {rel_path}: ...{context}...")
            matches_count += 1

print(f"Total matching items: {matches_count}")
for detail in matches_details[:40]:
    print(detail)
if len(matches_details) > 40:
    print(f"... and {len(matches_details) - 40} more matches.")
