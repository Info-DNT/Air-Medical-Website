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
        all_files.append(os.path.join(root, file))

pattern_any = re.compile(r"24/7|24[xX]7")

for file_path in all_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        continue
        
    # Check if there is any match at all
    if pattern_any.search(content):
        # Let's count how many times it matches, excluding the domain name airmedical24x7
        # and excluding the correct casing '24X7'
        cleaned = re.sub(r'airmedical24x7', 'DOMAIN', content, flags=re.IGNORECASE)
        cleaned = re.sub(r'airmedical_24x7', 'DOMAIN', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'airmedical-24x7', 'DOMAIN', cleaned, flags=re.IGNORECASE)
        
        matches = pattern_any.findall(cleaned)
        # Filter matches that are not exactly '24X7'
        bad_matches = [m for m in matches if m != '24X7']
        if bad_matches:
            print(f"[{rel_path}] Found {len(bad_matches)} invalid matches: {set(bad_matches)}")
