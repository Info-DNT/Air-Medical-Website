import os
import re
import glob

ROOT = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

def search_stretcher_variants():
    html_files = glob.glob(os.path.join(ROOT, "*.html")) + \
                 glob.glob(os.path.join(ROOT, "services", "*.html")) + \
                 glob.glob(os.path.join(ROOT, "countries", "*.html"))
                 
    # We want to find any text inside the form block that matches:
    # 1. Commercial Flight Stretcher
    # 2. Commercial Flight Stretcher Service
    # 3. Airline Stretcher Services
    # 4. Airline Stretcher Services Worldwide
    
    pattern = re.compile(r'(Commercial Flight Stretcher(?: Service)?|Airline Stretcher Services(?: Worldwide)?)', re.IGNORECASE)
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, ROOT)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        form_match = re.search(r'<form[^>]*id="(?:quoteForm|quoteFormPopup)"[^>]*>([\s\S]+?)</form>', content, re.IGNORECASE)
        if form_match:
            body = form_match.group(1)
            matches = pattern.findall(body)
            if matches:
                print(f"File: {rel_path} | Matches: {set(matches)}")

if __name__ == "__main__":
    search_stretcher_variants()
