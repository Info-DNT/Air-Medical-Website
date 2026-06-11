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

print(f"Found {len(html_files)} HTML files to inspect.")

pattern_24_7 = re.compile(r"24/7", re.IGNORECASE)
pattern_24x7 = re.compile(r"24x7", re.IGNORECASE)

occurrences = []

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            matches_24_7 = list(pattern_24_7.finditer(line))
            matches_24x7 = list(pattern_24x7.finditer(line))
            
            if matches_24_7 or matches_24x7:
                occurrences.append({
                    "file": rel_path,
                    "line_num": idx + 1,
                    "line": line.strip(),
                    "matches_24_7": [m.group(0) for m in matches_24_7],
                    "matches_24x7": [m.group(0) for m in matches_24x7]
                })

print(f"Total lines with matches: {len(occurrences)}")

# Let's categorize the matches to see where they are
urls_or_emails = []
other_matches = []

for occ in occurrences:
    line = occ["line"]
    # Simple check if match looks like part of a URL, email, path, or id attribute
    # e.g., containing 'airmedical24x7' or '@airmedical' or 'href=' etc.
    if any(domain_part in line.lower() for domain_part in ["airmedical24x7", "airmedical_24x7", "airmedical-24x7"]):
        urls_or_emails.append(occ)
    else:
        other_matches.append(occ)

print(f"\n--- URL or Email matches ({len(urls_or_emails)}) ---")
for idx, occ in enumerate(urls_or_emails[:15]):
    print(f"[{occ['file']}:{occ['line_num']}] {occ['line']}")
if len(urls_or_emails) > 15:
    print(f"... and {len(urls_or_emails) - 15} more URL/Email matches")

print(f"\n--- Other matches (Text/Content) ({len(other_matches)}) ---")
for idx, occ in enumerate(other_matches[:30]):
    print(f"[{occ['file']}:{occ['line_num']}] {occ['line']}")
if len(other_matches) > 30:
    print(f"... and {len(other_matches) - 30} more Text/Content matches")
