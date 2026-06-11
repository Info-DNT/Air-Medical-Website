import os
import re
import glob

ROOT = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

def search_commercial_stretcher():
    html_files = glob.glob(os.path.join(ROOT, "*.html")) + \
                 glob.glob(os.path.join(ROOT, "services", "*.html")) + \
                 glob.glob(os.path.join(ROOT, "countries", "*.html"))
                 
    pattern = re.compile(r'Commercial Flight Stretcher(?: Service)?', re.IGNORECASE)
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, ROOT)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        matches = pattern.findall(content)
        if matches:
            print(f"File: {rel_path} has {len(matches)} occurrences of Commercial Flight Stretcher:")
            for m in set(matches):
                print(f"  - {m}")

if __name__ == "__main__":
    search_commercial_stretcher()
