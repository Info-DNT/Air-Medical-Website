import os
import re

def main():
    root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
    pattern = re.compile(r'Stretcher\s+Services\s+Worldwide', re.IGNORECASE)
    
    for root, dirs, files in os.walk(root_dir):
        if any(p in root for p in ['node_modules', '.git', 'scratch', '.vscode']):
            continue
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                matches = list(pattern.finditer(content))
                if matches:
                    rel_path = os.path.relpath(path, root_dir).replace('\\', '/')
                    print(f"File: {rel_path}")
                    for m in matches:
                        # Find line number
                        line_no = content.count('\n', 0, m.start()) + 1
                        start_idx = max(0, m.start() - 60)
                        end_idx = min(len(content), m.end() + 60)
                        snippet = content[start_idx:end_idx].replace('\n', '\\n')
                        print(f"  Line {line_no}: ...{snippet}...")

if __name__ == '__main__':
    main()
