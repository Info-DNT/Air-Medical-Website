import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []
js_files = []

for dirpath, dirnames, filenames in os.walk(root_dir):
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

print(f"Loaded {len(html_files)} HTML files and {len(js_files)} JS files for processing.")

# Define the old/new router parts
old_router_block = """      var countriesPrefix = basePath + '/countries/';
      var servicesPrefix = basePath + '/services/';
      if (cleanPath.startsWith(countriesPrefix) && cleanPath.length > countriesPrefix.length) {
        cleanPath = basePath + '/' + cleanPath.substring(countriesPrefix.length);
      } else if (cleanPath.startsWith(servicesPrefix) && cleanPath.length > servicesPrefix.length) {
        cleanPath = basePath + '/' + cleanPath.substring(servicesPrefix.length);
      }
      if (cleanPath === basePath + '/countries/index' || cleanPath === basePath + '/countries') {
        cleanPath = basePath + '/country';
      }
      var isDirRoot = (cleanPath === basePath || cleanPath === basePath + '/' || cleanPath === '/countries/' || cleanPath === '/');"""

# Wait, let's be careful about '|| cleanPath === basePath + \'/countries/\'' or similar in some files.
# Let's check how the router is written exactly. In about-us.html line 35 it was:
# var isDirRoot = (cleanPath === basePath || cleanPath === basePath + '/' || cleanPath === basePath + '/countries/' || cleanPath === '/');
# In other files, is it the same? Let's check if the script can do a more robust find-and-replace for the router.
# Let's write the exact old block based on our viewing of about-us.html:
# var isDirRoot = (cleanPath === basePath || cleanPath === basePath + '/' || cleanPath === basePath + '/countries/' || cleanPath === '/');

# Let's define the replacements for HTML files:
def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    
    # 1. Update the head router
    # We will search for:
    # cleanPath = basePath + '/country';
    # and replace with:
    # cleanPath = basePath + '/countries';
    content = content.replace("cleanPath = basePath + '/country';", "cleanPath = basePath + '/countries';")
    
    # We will search for:
    # || cleanPath === basePath + '/countries/'
    content = content.replace(" || cleanPath === basePath + '/countries/'", "")
    content = content.replace(" || cleanPath === '/countries/'", "")
    
    # 2. Update the click interceptor:
    # cleanHref === 'country' -> cleanHref === 'countries'
    content = content.replace("cleanHref === 'country'", "cleanHref === 'countries'")
    
    # 3. Update href links:
    # href="blog" -> href="blogs"
    # href="country" -> href="countries"
    # href="blog-detail" -> href="blogs-detail"
    # also handle single quotes
    content = re.sub(r'href=(["\'])\./?blog(["\'])', r'href=\1blogs\2', content)
    content = re.sub(r'href=(["\'])\./?country(["\'])', r'href=\1countries\2', content)
    content = re.sub(r'href=(["\'])\./?blog-detail', r'href=\1blogs-detail', content)
    
    # Let's check if there are other href= values pointing to these clean urls.
    # Like href="blog?..." or href="blog-detail?..." or href="country?..."
    content = re.sub(r'href=(["\'])\./?blog\?', r'href=\1blogs?', content)
    content = re.sub(r'href=(["\'])\./?country\?', r'href=\1countries?', content)
    
    # 4. Update the menu text:
    # <a href="blog" ...>Blog</a> -> <a href="blogs" ...>Blogs</a>
    # <a class="text-light mb-2" href="blog"><i class="fa fa-angle-right me-2"></i>Latest Blog</a> -> Latest Blogs
    # Let's do this via specific replacements
    content = content.replace('>Blog</a>', '>Blogs</a>')
    content = content.replace('>Latest Blog</a>', '>Latest Blogs</a>')
    content = content.replace('>Latest Blog </a>', '>Latest Blogs</a>')
    
    # 5. Script tags at the bottom:
    # For blogs.html: src="js/blog.js" -> src="js/blogs.js"
    # For blogs-detail.html: src="js/blog-detail.js" -> src="js/blogs-detail.js"
    if filepath.endswith("blogs.html"):
        content = content.replace('src="js/blog.js"', 'src="js/blogs.js"')
    elif filepath.endswith("blogs-detail.html"):
        content = content.replace('src="js/blog-detail.js"', 'src="js/blogs-detail.js"')

    # 6. Structured Schema Data URLs:
    # We want to change schema URLs like:
    # "url": "https://airmedical24x7.com/blog" -> blogs
    # "mainEntityOfPage": "https://airmedical24x7.com/blog" -> blogs
    # "@id": "https://airmedical24x7.com/blog#..." -> blogs
    # "name": "Air Medical 24X7 Blog" -> Blogs
    # "headline": "Our Latest Medical Blog Posts" -> Blogs (optional)
    content = content.replace("airmedical24x7.com/blog", "airmedical24x7.com/blogs")
    content = content.replace("airmedical24x7.com/country", "airmedical24x7.com/countries")
    content = content.replace("Air Medical 24X7 Blog", "Air Medical 24X7 Blogs")
    
    # Canonical link tags:
    # <link rel="canonical" href="https://airmedical24x7.com/blog">
    # (already handled by the general airmedical24x7.com/blog replacement above)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Process JS files:
def process_js_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    
    # js/blogs.js
    if filepath.endswith("blogs.js"):
        content = content.replace("blog-detail.html", "blogs-detail.html")
        content = content.replace("blog-detail", "blogs-detail")
        
    # js/blogs-detail.js
    elif filepath.endswith("blogs-detail.js"):
        content = content.replace("/blog?category=", "/blogs?category=")
        content = content.replace("/blog-detail.html?slug=", "/blogs-detail.html?slug=")
        content = content.replace("/blog-detail?slug=", "/blogs-detail?slug=")
        content = content.replace("/blog?tag=", "/blogs?tag=")
        content = content.replace("Blog not found", "Blogs not found")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Run
html_changed = 0
for relpath in html_files:
    filepath = os.path.join(root_dir, relpath)
    if process_html_file(filepath):
        html_changed += 1

js_changed = 0
for relpath in js_files:
    filepath = os.path.join(root_dir, relpath)
    if process_js_file(filepath):
        js_changed += 1

print(f"Process completed. Changed {html_changed} HTML files and {js_changed} JS files.")
