import re

sitemap_path = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main\sitemap.xml"

with open(sitemap_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match <loc>...</loc> content
loc_pattern = re.compile(r'<loc>(https://airmedical24x7\.com/[^<]*)</loc>')

def clean_url(match):
    url = match.group(1)
    
    # 1. Handle special cases
    if url.endswith('/countries/index.html') or url.endswith('/countries/'):
        url = 'https://airmedical24x7.com/country'
    elif url.endswith('/countries'):
        url = 'https://airmedical24x7.com/country'
    elif url.endswith('/contact.html') or url.endswith('/contact'):
        url = 'https://airmedical24x7.com/contact-us'
    elif url.endswith('/about.html') or url.endswith('/about'):
        url = 'https://airmedical24x7.com/about-us'
    else:
        # Remove directory prefixes
        url = url.replace('/countries/', '/')
        url = url.replace('/services/', '/')
        
        # Remove .html extension
        if url.endswith('.html'):
            url = url[:-5]
            
    return f"<loc>{url}</loc>"

new_content = loc_pattern.sub(clean_url, content)

with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated sitemap.xml with clean URLs successfully.")
