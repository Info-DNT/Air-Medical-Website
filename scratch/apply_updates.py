import os
import re
import sys

# Ensure stdout handles UTF-8 correctly
sys.stdout.reconfigure(encoding='utf-8')

project_root = r"C:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# Regular expression to find href attributes
href_pattern = re.compile(r'href="([^"]+)"')
href_single_pattern = re.compile(r"href='([^']+)'")

def map_href(href):
    # Skip if baseHref is part of the string
    if 'baseHref' in href:
        return href

    # Skip external, hash-only, mailto, tel, javascript, or empty/root base links
    if (href.startswith('http') or href.startswith('#') or 
        href.startswith('tel:') or href.startswith('mailto:') or 
        href.startswith('javascript:') or href == './' or href == ''):
        return href
        
    # Split query/hash
    path_part = href
    query_hash_part = ""
    if '?' in href:
        parts = href.split('?', 1)
        path_part = parts[0]
        query_hash_part = '?' + parts[1]
    elif '#' in href:
        parts = href.split('#', 1)
        path_part = parts[0]
        query_hash_part = '#' + parts[1]
        
    if not path_part or path_part in ['./', '../', '.', '..']:
        return href
        
    # Check if path already has an extension
    _, ext = os.path.splitext(path_part)
    if ext:
        # If it has an extension (like .html, .css, .js, .png, etc.), keep it.
        # But if it points to contact.html, map to contact-us.html
        if path_part.endswith('contact.html'):
            return path_part[:-12] + 'contact-us.html' + query_hash_part
        return href
        
    # Handle folder links ending with /
    if path_part.endswith('/'):
        return path_part + 'index.html' + query_hash_part
        
    # Normalize path and check if it's contact-us or contact
    normalized_path = path_part.lower()
    if normalized_path.endswith('contact') or normalized_path.endswith('contact-us') or normalized_path.endswith('contact us'):
        for term in ['contact-us', 'contact us', 'contact']:
            if path_part.lower().endswith(term):
                idx = path_part.lower().rfind(term)
                path_part = path_part[:idx] + 'contact-us.html'
                break
    else:
        # Just append .html
        path_part = path_part + '.html'
        
    return path_part + query_hash_part

def process_file(file_path):
    rel_path = os.path.relpath(file_path, project_root)
    print(f"Processing {rel_path}...")
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # 1. Update hrefs
    def replace_href(match):
        original_href = match.group(1)
        new_href = map_href(original_href)
        if new_href != original_href:
            return f'href="{new_href}"'
        return match.group(0)
        
    def replace_href_single(match):
        original_href = match.group(1)
        new_href = map_href(original_href)
        if new_href != original_href:
            return f"href='{new_href}'"
        return match.group(0)
        
    new_content = href_pattern.sub(replace_href, content)
    new_content = href_single_pattern.sub(replace_href_single, new_content)
    
    # 2. Fix encoding issues
    new_content = new_content.replace('âœ…', '✅')
    
    # 3. Standardize Navbar Menu labels
    # Service -> Our Services
    navbar_service_old = '>Service</a>'
    navbar_service_new = '>Our Services</a>'
    new_content = new_content.replace(navbar_service_old, navbar_service_new)
    
    # Contact -> Contact Us
    new_content = re.sub(
        r'href="([^"]*contact-us\.html)"([^>]*)>Contact</a>',
        r'href="\1"\2>Contact Us</a>',
        new_content
    )
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Updated {rel_path}")

def main():
    html_files = []
    for root, dirs, files in os.walk(project_root):
        if '.git' in root.split(os.sep):
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    print(f"Found {len(html_files)} HTML files to update.")
    for file_path in html_files:
        process_file(file_path)
    print("Done!")

if __name__ == '__main__':
    main()
