import os
import re

def main():
    root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
    # Regex to find links to commercial-flight-stretcher
    pattern = re.compile(r'<a[^>]+href="[^"]*commercial-flight-stretcher[^"]*"[^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
    
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
                        link_text = " ".join(m.group(1).split())
                        # clean tag elements if any (like <i>)
                        link_text_clean = re.sub(r'<[^>]+>', '', link_text).strip()
                        print(f"  Href match: '{link_text_clean}'")

if __name__ == '__main__':
    main()
