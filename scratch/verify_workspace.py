import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

project_root = r"C:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# Garbled character patterns to look for
garbled_patterns = [
    'ðŸš¨', 'ðŸ“ž', 'ðŸ’¬', 'ðŸ†˜', 'âœ‰ï¸', 'Ã¢â‚¬â€œ', 'Ã¢â‚¬â„¢', 'âœ…', 'â Œ',
    'ðŸ”’', 'ðŸ“¦', 'âœ…ï¸', 'Ã¢Â Å’', 'Ã¢Å“â€¦', 'ðŸš€', 'ðŸ‘¦'
]

def verify_workspace():
    html_files = []
    for root, dirs, files in os.walk(project_root):
        if '.git' in root.split(os.sep):
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    print(f"Scanning {len(html_files)} HTML files in workspace for garbled characters...")
    found_any = False

    for f in html_files:
        try:
            with open(f, 'r', encoding='utf-8', errors='ignore') as file_obj:
                content = file_obj.read()
        except Exception as e:
            print(f"Error reading {f}: {e}")
            continue

        file_found = []
        for pattern in garbled_patterns:
            if pattern in content:
                count = content.count(pattern)
                file_found.append((pattern, count))
                found_any = True
        
        if file_found:
            rel_path = os.path.relpath(f, project_root)
            print(f"File: {rel_path}")
            for pattern, count in file_found:
                print(f"  - Pattern '{pattern}' found {count} times")

    if not found_any:
        print("Success! No garbled characters found in the workspace.")

if __name__ == '__main__':
    verify_workspace()
