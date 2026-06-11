import os
import re

workspace_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []
for root, dirs, files in os.walk(workspace_dir):
    if ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

print(f"Found {len(html_files)} HTML files to scan.")

def clean_href(href_val):
    # Ignore external links, anchor links, phone/email, and javascript
    if href_val.startswith(('http', 'tel:', 'mailto:', 'javascript:', '#')):
        return href_val
        
    # We only care about internal html page links
    if '.html' not in href_val:
        return href_val
        
    # Separate pathname from query parameters or hashes
    parts = href_val.split('?')
    path = parts[0].split('#')[0]
    suffix = href_val[len(path):]
    
    if not path.endswith('.html'):
        return href_val
        
    # Strip .html extension
    clean_path = path[:-5]
    
    # Map index files
    if clean_path == 'index' or clean_path == '../index':
        return 'index' + suffix
        
    # Map country index/overview files to "country"
    if clean_path.endswith('countries/index') or clean_path.endswith('country'):
        return 'country' + suffix
        
    # Extract the base file name (the slug)
    last_segment = clean_path.split('/')[-1]
    return last_segment + suffix

# Match both double and single quoted href values
double_quote_regex = re.compile(r'href="([^"]+)"')
single_quote_regex = re.compile(r"href='([^']+)'")

updated_files = 0
total_replacements = 0

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    new_content = content
    
    # Process double quotes
    matches = double_quote_regex.findall(new_content)
    file_replacements = 0
    for m in matches:
        cleaned = clean_href(m)
        if cleaned != m:
            orig_attr = f'href="{m}"'
            new_attr = f'href="{cleaned}"'
            new_content = new_content.replace(orig_attr, new_attr)
            file_replacements += 1
            total_replacements += 1
            
    # Process single quotes
    matches = single_quote_regex.findall(new_content)
    for m in matches:
        cleaned = clean_href(m)
        if cleaned != m:
            orig_attr = f"href='{m}'"
            new_attr = f"href='{cleaned}'"
            new_content = new_content.replace(orig_attr, new_attr)
            file_replacements += 1
            total_replacements += 1
            
    if file_replacements > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_files += 1
        print(f"Cleaned {file_replacements} links in {rel_path}")

print(f"\nSuccessfully cleaned {total_replacements} links across {updated_files} files.")
