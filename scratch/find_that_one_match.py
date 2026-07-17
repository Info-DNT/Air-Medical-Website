import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []
for root, dirs, files in os.walk(workspace_dir):
    if ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

# Find any 24x7 (case-sensitive lowercase x) or 24/7 (case-insensitive)
pattern_24x7 = re.compile(r"24x7")
pattern_24_7 = re.compile(r"24/7")

found_count = 0

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            has_24x7 = pattern_24x7.search(line)
            has_24_7 = pattern_24_7.search(line)
            
            if has_24x7 or has_24_7:
                # Filter out lines that look like links, URLs, emails, schemas, or attributes
                # We want to keep plain text, headers, paragraphs, titles, alt texts, tooltips, etc.
                cleaned_line = line.strip()
                
                # Check if it's purely a URL, schema, or meta tag
                is_schema_or_meta = (
                    cleaned_line.startswith('"@id"') or 
                    cleaned_line.startswith('"url"') or 
                    cleaned_line.startswith('"logo"') or 
                    cleaned_line.startswith('"sameAs"') or
                    cleaned_line.startswith('<link') or
                    cleaned_line.startswith('<meta') or
                    cleaned_line.startswith('"@context"') or
                    cleaned_line.startswith('"image"')
                )
                
                # Check if it's an email or external social link inside href
                is_href_link = (
                    'href="https://' in cleaned_line or
                    "href='https://" in cleaned_line or
                    'href="mailto:' in cleaned_line or
                    'href="http://' in cleaned_line
                )
                
                # Check if it's a domain name inside sitemap
                is_sitemap = rel_path.endswith('.xml') or '<loc>' in cleaned_line
                
                if not (is_schema_or_meta or is_href_link or is_sitemap):
                    # Check if the match is inside a domain name (like airmedical24x7.com)
                    # We can replace the domain name with empty space and check if "24x7" or "24/7" still exists
                    no_domain = re.sub(r'airmedical24x7\.(com|in|org|net|ae)', '', cleaned_line, flags=re.IGNORECASE)
                    no_domain = re.sub(r'airmedical24x7', '', no_domain, flags=re.IGNORECASE)
                    
                    if pattern_24x7.search(no_domain) or pattern_24_7.search(no_domain):
                        found_count += 1
                        print(f"[{rel_path}:{idx + 1}] {cleaned_line}")

print(f"\nTotal text occurrences found: {found_count}")
