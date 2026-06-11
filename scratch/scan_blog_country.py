import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []
js_files = []
other_files = []

for dirpath, dirnames, filenames in os.walk(root_dir):
    # skip .git
    if ".git" in dirpath.split(os.sep):
        continue
    if "scratch" in dirpath.split(os.sep):
        continue
        
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        relpath = os.path.relpath(filepath, root_dir)
        
        if filename.endswith(".html"):
            html_files.append(relpath)
        elif filename.endswith(".js"):
            js_files.append(relpath)
        elif filename in [".htaccess", "sitemap.xml", "robots.txt"]:
            other_files.append(relpath)

print(f"Found {len(html_files)} HTML files, {len(js_files)} JS files, {len(other_files)} other files.")

# We want to search for occurrences of 'blog' and 'country' (case-insensitive) in these files
# to see where they are referenced. We'll categorize matches.

blog_pattern = re.compile(r'\bblogs?\b', re.IGNORECASE)
country_pattern = re.compile(r'\bcountries\b|\bcountry\b', re.IGNORECASE)

# Also look for exact href values like href="blog", href="blog-detail", href="country"
href_blog = re.compile(r'href=["\']\./?blog["\']', re.IGNORECASE)
href_blog_detail = re.compile(r'href=["\']\./?blog-detail["\']', re.IGNORECASE)
href_country = re.compile(r'href=["\']\./?country["\']', re.IGNORECASE)

results = []

for relpath in html_files + js_files + other_files:
    filepath = os.path.join(root_dir, relpath)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        # try another encoding if utf-8 fails
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
        except Exception:
            continue
            
    # Check for specific references
    blog_matches = blog_pattern.findall(content)
    country_matches = country_pattern.findall(content)
    
    hb = href_blog.findall(content)
    hbd = href_blog_detail.findall(content)
    hc = href_country.findall(content)
    
    if blog_matches or country_matches or hb or hbd or hc:
        results.append({
            'file': relpath,
            'blog_count': len(blog_matches),
            'country_count': len(country_matches),
            'href_blog': len(hb),
            'href_blog_detail': len(hbd),
            'href_country': len(hc)
        })

# Print top matches
results.sort(key=lambda x: (x['href_blog'] + x['href_blog_detail'] + x['href_country']), reverse=True)
for r in results:
    print(f"{r['file']}: blog={r['blog_count']}, country={r['country_count']}, href_blog={r['href_blog']}, href_blog_detail={r['href_blog_detail']}, href_country={r['href_country']}")
