import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []
for root, dirs, files in os.walk(workspace_dir):
    if ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

# Match any 24/7 (case-insensitive) or 24x7 (case-insensitive)
pattern_any = re.compile(r"24/7|24[xX]7", re.IGNORECASE)

found_count = 0

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        # Find all occurrences of 24/7 or 24x7 (case-insensitive)
        for match in pattern_any.finditer(line):
            match_str = match.group(0)
            
            # If the match is already exactly "24X7", we skip it
            if match_str == "24X7":
                continue
                
            # Now let's check if this specific match is part of a domain name, URL, or email
            # We can inspect the surrounding characters or the match index in the line
            start, end = match.span()
            
            # To see if it's a domain/email:
            # Let's extract a window around the match
            window_start = max(0, start - 15)
            window_end = min(len(line), end + 15)
            window = line[window_start:window_end].lower()
            
            # If it's part of 'airmedical24x7', 'airmedical_24x7', 'airmedical-24x7', or email address, skip it
            if "airmedical" in window:
                continue
            
            found_count += 1
            print(f"[{rel_path}:{idx + 1}] match='{match_str}' in line: {line.strip()}")

print(f"\nTotal invalid casings found: {found_count}")
