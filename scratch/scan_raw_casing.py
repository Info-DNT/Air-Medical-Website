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
        if file.endswith((".html", ".css", ".js")):
            all_files.append(os.path.join(root, file))

pattern_24_7 = re.compile(r"24/7", re.IGNORECASE)
pattern_24x7 = re.compile(r"24x7", re.IGNORECASE)

found_count = 0

for file_path in all_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    for idx, line in enumerate(lines):
        # Temporarily replace domain/email occurrences to see if there is any other occurrence of 24x7 or 24/7
        cleaned_line = re.sub(r'airmedical24x7', 'DOMAIN', line, flags=re.IGNORECASE)
        cleaned_line = re.sub(r'airmedical_24x7', 'DOMAIN', cleaned_line, flags=re.IGNORECASE)
        cleaned_line = re.sub(r'airmedical-24x7', 'DOMAIN', cleaned_line, flags=re.IGNORECASE)
        
        has_24_7 = pattern_24_7.search(cleaned_line)
        has_24x7 = pattern_24x7.search(cleaned_line)
        
        # Also filter out the exact correct string "24X7"
        if has_24_7 or has_24x7:
            # Let's verify that the match in cleaned_line is not "24X7"
            # Get all matches of 24/7 or 24x7 in cleaned_line
            matches = re.findall(r'24/7|24[xX]7', cleaned_line)
            # If all matches are exactly '24X7', then it's correct and we skip
            if all(m == '24X7' for m in matches):
                continue
                
            found_count += 1
            clean_line = line.strip()
            safe_line = clean_line.encode('ascii', errors='replace').decode('ascii')
            print(f"[{rel_path}:{idx + 1}] {safe_line}")

print(f"\nTotal potential invalid occurrences: {found_count}")
