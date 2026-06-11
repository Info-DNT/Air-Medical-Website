import os
import re

def main():
    root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
    pattern = re.compile(r'Airline\s+Stretcher\s+Service(s)?(?:\s+Worldwide)?', re.IGNORECASE)
    
    for root, dirs, files in os.walk(root_dir):
        if any(p in root for p in ['node_modules', '.git', 'scratch', '.vscode']):
            continue
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                matches = list(pattern.finditer(content))
                for m in matches:
                    text = m.group(0)
                    if "worldwide" in text.lower():
                        line_no = content.count('\n', 0, m.start()) + 1
                        start_idx = max(0, m.start() - 40)
                        end_idx = min(len(content), m.end() + 40)
                        snippet = content[start_idx:end_idx].replace('\n', '\\n')
                        rel_path = os.path.relpath(path, root_dir).replace('\\', '/')
                        print(f"File: {rel_path} (Line {line_no})")
                        print(f"  Snippet: ...{snippet}...")

if __name__ == '__main__':
    main()
