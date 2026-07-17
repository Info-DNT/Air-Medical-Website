import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

errors = []
html_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    parts = dirpath.split(os.sep)
    if ".git" in parts or "scratch" in parts:
        continue
    for filename in filenames:
        if filename.endswith((".html", ".xml")):
            html_files.append(os.path.join(dirpath, filename))

print(f"Verifying {len(html_files)} files...")

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    relpath = os.path.relpath(filepath, root_dir)
    
    # Check for legacy flight-medical-escort-service (except in 404.html redirect check)
    match_singular_service = re.search(r'flight-medical-escort-service(?!s)', content)
    if match_singular_service and relpath != '404.html':
        errors.append(f"[{relpath}] Found singular service 'flight-medical-escort-service' around index {match_singular_service.start()}")
        
    # Check for blogss typo
    match_blogss = re.search(r'blogss', content, re.IGNORECASE)
    if match_blogss:
        errors.append(f"[{relpath}] Found typo 'blogss' around index {match_blogss.start()}")
        
    # Check for Latest Blog in footers
    match_latest_blog = re.search(r'Latest\s+Blog\s*</a>', content, re.IGNORECASE)
    if match_latest_blog:
        errors.append(f"[{relpath}] Found singular footer link 'Latest Blog' around index {match_latest_blog.start()}")

    # For HTML files only, check for the updated interceptor (except 404.html which has no interceptor)
    if filepath.endswith(".html") and relpath != '404.html':
        if 'e.ctrlKey' not in content:
            errors.append(f"[{relpath}] Missing updated JavaScript link interceptor with 'e.ctrlKey' check.")

if errors:
    print("\n--- Verification Failed with errors: ---")
    for err in errors:
        print(f"x {err}")
else:
    print("\n--- Verification Passed! All files are perfectly updated. ---")
