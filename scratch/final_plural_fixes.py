import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# Collect all HTML, JS, and XML files (excluding .git and scratch)
target_files = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    # Skip .git and scratch directories
    parts = dirpath.split(os.sep)
    if ".git" in parts or "scratch" in parts:
        continue
    for filename in filenames:
        if filename.endswith((".html", ".js", ".xml")):
            target_files.append(os.path.join(dirpath, filename))

print(f"Found {len(target_files)} files to process.")

changed_count = 0
for filepath in target_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. href="blog" -> href="blogs" (with or without ./ prefix, double or single quotes)
    content = re.sub(r'href="\.?/?blog"', 'href="blogs"', content)
    content = re.sub(r"href='\.?/?blog'", "href='blogs'", content)
    
    # 2. href="country" -> href="countries" (with or without ./ prefix)
    content = re.sub(r'href="\.?/?country"', 'href="countries"', content)
    content = re.sub(r"href='\.?/?country'", "href='countries'", content)
    
    # 3. href="blog-detail -> href="blogs-detail (for query strings like ?slug=...)
    content = re.sub(r'href="\.?/?blog-detail', 'href="blogs-detail', content)
    content = re.sub(r"href='\.?/?blog-detail", "href='blogs-detail", content)
    
    # 4. href="blog? -> href="blogs? (for query strings like ?category=...)
    content = re.sub(r'href="\.?/?blog\?', 'href="blogs?', content)
    content = re.sub(r"href='\.?/?blog\?", "href='blogs?", content)
    
    # 5. Sitemap URLs
    content = content.replace("airmedical24x7.com/blog-detail", "airmedical24x7.com/blogs-detail")
    content = content.replace("airmedical24x7.com/blog", "airmedical24x7.com/blogs")
    content = content.replace("airmedical24x7.com/country", "airmedical24x7.com/countries")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        relpath = os.path.relpath(filepath, root_dir)
        print(f"  Updated: {relpath}")
        changed_count += 1

print(f"\nDone. Updated {changed_count} files.")
