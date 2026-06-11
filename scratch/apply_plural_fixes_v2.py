import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# Collect all HTML files (excluding .git and scratch)
html_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    parts = dirpath.split(os.sep)
    if ".git" in parts or "scratch" in parts:
        continue
    for filename in filenames:
        if filename.endswith(".html"):
            html_files.append(os.path.join(dirpath, filename))

print(f"Found {len(html_files)} HTML files to process.")

changed_count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Replace 'flight-medical-escort-service' (not followed by 's') with 'flight-medical-escort-services'
    content = re.sub(r'flight-medical-escort-service(?!s)', 'flight-medical-escort-services', content)
    content = re.sub(r'Flight Medical Escort Service(?!s)', 'Flight Medical Escort Services', content)
    
    # 2. Replace 'blogss' / 'Blogss' with 'blogs' / 'Blogs'
    content = re.sub(r'blogss', 'blogs', content)
    content = re.sub(r'Blogss', 'Blogs', content)
    
    # 3. Replace 'Latest Blog' footer text (possibly split across lines) with 'Latest Blogs'
    content = re.sub(r'Latest\s+Blog\s*</a>', 'Latest Blogs</a>', content, flags=re.IGNORECASE)
    
    # 4. Update JavaScript link interceptor to support modifier keys and target="_blank"
    # Find:
    #   e.preventDefault();
    #   window.location.href = finalUrl + queryHashPart;
    # Replace with check for target="_blank" or modifier keys
    interceptor_pattern = r'e\.preventDefault\(\);\s+window\.location\.href\s*=\s*finalUrl\s*\+\s*queryHashPart;'
    
    interceptor_replacement = (
        "var target = anchor.getAttribute('target');\n"
        "          if (target === '_blank' || e.ctrlKey || e.metaKey || e.shiftKey || e.button !== 0) {\n"
        "            e.preventDefault();\n"
        "            window.open(finalUrl + queryHashPart, '_blank');\n"
        "            return;\n"
        "          }\n"
        "          \n"
        "          e.preventDefault();\n"
        "          window.location.href = finalUrl + queryHashPart;"
    )
    
    # We check if the interceptor has already been replaced (e.g. contains 'e.ctrlKey')
    if 'e.ctrlKey' not in content:
        content = re.sub(interceptor_pattern, interceptor_replacement, content)
        
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        relpath = os.path.relpath(filepath, root_dir)
        print(f"  Updated: {relpath}")
        changed_count += 1

print(f"\nDone. Updated {changed_count} files.")
