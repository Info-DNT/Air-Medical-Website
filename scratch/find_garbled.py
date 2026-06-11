import os
import re

project_root = r"C:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

garbled_patterns = [
    r"ðŸ",
    r"âœ",
    r"Ã¢â",
    r"â€”",
    r"â€“",
    r"â€™"
]

def scan_files():
    for root, dirs, files in os.walk(project_root):
        # Skip git directory
        if '.git' in root.split(os.sep):
            continue
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    found = []
                    for pattern in garbled_patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            found.append(f"{pattern} ({len(matches)} matches)")
                    
                    if found:
                        # Print matching lines for context
                        print(f"File: {os.path.relpath(file_path, project_root)}")
                        print(f"  Detected: {', '.join(found)}")
                        lines = content.splitlines()
                        for i, line in enumerate(lines):
                            for pattern in garbled_patterns:
                                if re.search(pattern, line):
                                    print(f"    Line {i+1}: {line.strip()[:100]}")
                                    break
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

if __name__ == "__main__":
    scan_files()
