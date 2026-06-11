import os
import re

def execute_renames():
    root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        if 'node_modules' in root or '.git' in root or 'scratch' in root or '.vscode' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    print(f"Starting site-wide rename in {len(html_files)} HTML files...")
    
    target_str = "Airline Stretcher Services Worldwide"
    replacement_str = "Airline Stretcher Services"
    
    modified_count = 0
    total_replacements = 0
    
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Count matches
        matches = len(re.findall(re.escape(target_str), content))
        if matches > 0:
            new_content = content.replace(target_str, replacement_str)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.relpath(filepath, root_dir)}: replaced {matches} occurrences.")
            modified_count += 1
            total_replacements += matches
            
    print("-" * 50)
    print(f"Completed! Modified {modified_count} files with {total_replacements} total replacements.")

if __name__ == "__main__":
    execute_renames()
