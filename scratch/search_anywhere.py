import os
import re

def search_text(pattern):
    root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
    matches = []
    
    for root, dirs, files in os.walk(root_dir):
        if 'node_modules' in root or '.git' in root or 'scratch' in root or '.vscode' in root:
            continue
        for file in files:
            if file.endswith('.html') or file.endswith('.js') or file.endswith('.json') or file.endswith('.xml') or file.endswith('.htaccess'):
                filepath = os.path.join(root, file)
                rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
                
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    for idx, line in enumerate(lines):
                        if re.search(pattern, line, re.IGNORECASE):
                            matches.append((rel_path, idx + 1, line.strip()))
                except Exception as e:
                    print(f"Error reading {rel_path}: {e}")
                    
    print(f"Found {len(matches)} matches for pattern '{pattern}':")
    for filepath, line_no, content in matches[:100]:
        print(f"{filepath}:{line_no}: {content}")
    if len(matches) > 100:
        print(f"... and {len(matches) - 100} more matches.")

if __name__ == "__main__":
    search_text("Airline Stretcher Services Worldwide")
