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

print(f"Verifying {len(html_files)} HTML files for native physical URL patterns...")

has_errors = False

# Asset file extensions that we skip
asset_extensions = ['css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'ico', 'xml', 'txt', 'php', 'eot', 'woff2', 'woff', 'ttf']

# 1. Verify anchor link structure
href_pattern = re.compile(r'href=(["\'])(.*?)\1', re.IGNORECASE)

for f_path in html_files:
    rel_path = os.path.relpath(f_path, workspace_dir).replace('\\', '/')
    if "404.html" in rel_path or "admin.html" in rel_path:
        continue
    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    for match in href_pattern.finditer(content):
        href_val = match.group(2)
        
        # Skip protocol/external, mailto, phone, SMS, JS, hashes
        if (href_val.startswith('http') or href_val.startswith('#') or 
            href_val.startswith('tel:') or href_val.startswith('mailto:') or 
            href_val.startswith('sms:') or href_val.startswith('javascript:')):
            continue
            
        # Ignore assets
        slug_base = href_val.split('?')[0].split('#')[0].lstrip('/')
        ext = slug_base.split('.')[-1].lower() if '.' in slug_base else ''
        if ext in asset_extensions:
            continue
            
        # Check if local href is clean (which is an error now!)
        # E.g. href="/about-us" is bad, it should be "/about-us.html"
        if not href_val.endswith('.html') and href_val != '/':
            # Also allow clean parameter links if they are to index/etc.
            if '.html?' not in href_val and '.html#' not in href_val:
                print(f"ERROR: Clean URL (missing .html extension) in {rel_path}: href=\"{href_val}\"")
                has_errors = True
                
        # Check that links are absolute root-relative (starts with '/')
        if not href_val.startswith('/') and href_val != '':
            print(f"ERROR: Relative URL (does not start with '/') in {rel_path}: href=\"{href_val}\"")
            has_errors = True

# 2. Verify canonical tag URLs
canonical_pattern = re.compile(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', re.IGNORECASE)
for f_path in html_files:
    rel_path = os.path.relpath(f_path, workspace_dir).replace('\\', '/')
    if "404.html" in rel_path or "admin.html" in rel_path:
        continue
    with open(f_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    canonical_matches = canonical_pattern.findall(content)
    if not canonical_matches:
        print(f"ERROR: Canonical tag missing in {rel_path}")
        has_errors = True
    else:
        for c_url in canonical_matches:
            if not c_url.endswith('.html') and c_url != 'https://airmedical24x7.com/':
                if '.html?' not in c_url and '.html#' not in c_url:
                    print(f"ERROR: Non-physical canonical URL in {rel_path}: {c_url}")
                    has_errors = True

# 3. Verify sitemap.xml URLs
sitemap_path = os.path.join(workspace_dir, "sitemap.xml")
with open(sitemap_path, 'r', encoding='utf-8') as f:
    sitemap_content = f.read()

sitemap_urls = re.findall(r'<loc>(.*?)</loc>', sitemap_content)
for s_url in sitemap_urls:
    if not s_url.endswith('.html') and s_url != 'https://airmedical24x7.com/':
        print(f"ERROR: Sitemap contains non-physical URL: {s_url}")
        has_errors = True

if not has_errors:
    print("SUCCESS: All URL structure verification checks passed successfully!")
else:
    print("FAILURE: Verification errors found.")
