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

# Regex patterns for matching
pattern_24_7 = re.compile(r"\b24/7\b", re.IGNORECASE)
pattern_24x7 = re.compile(r"\b24x7\b", re.IGNORECASE)

modified_files = 0
total_replacements = 0

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Perform replacements
    content_after_24_7, count_24_7 = pattern_24_7.subn("24X7", original_content)
    final_content, count_24x7 = pattern_24x7.subn("24X7", content_after_24_7)
    
    total_count = count_24_7 + count_24x7
    
    if total_count > 0:
        modified_files += 1
        total_replacements += total_count
        
        # Write the modified content back
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(final_content)
            
        print(f"[{rel_path}] Made {total_count} replacements (24/7: {count_24_7}, 24x7: {count_24x7})")

print(f"\nCompleted! Modified {modified_files} files with a total of {total_replacements} replacements.")
