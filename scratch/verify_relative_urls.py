import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html"))
)

print(f"Verifying {len(html_files)} HTML files for relative URL patterns...\n")

has_errors = False

# Patterns that should NOT remain as absolute root-relative (starting with /)
# The exception is canonical, og:url, twitter:image, etc. (meta tags) and external URLs
BAD_ABSOLUTE_PATH = re.compile(r'\b(href|src|action)=(["\'])(/[^"\']*)\2', re.IGNORECASE)

# We must exclude canonical tags, og: meta, twitter: meta, etc.
CANONICAL_LIKE = re.compile(r'<link\s[^>]*rel=["\']canonical["\']', re.IGNORECASE)
OG_META = re.compile(r'<meta\s[^>]*(og:|twitter:|property=)', re.IGNORECASE)

def line_is_in_meta_or_canonical(filepath, match_start, content):
    """Check if match is inside a <link rel="canonical"> or <meta og:...> tag."""
    tag_open = content.rfind('<', 0, match_start)
    if tag_open == -1:
        return False
    tag_content = content[tag_open:match_start + 10]
    if 'canonical' in tag_content.lower():
        return True
    if 'og:' in tag_content.lower() or 'twitter:' in tag_content.lower():
        return True
    return False

for filepath in html_files:
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    if rel_path in ["admin.html", "404.html"]:
        continue

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    file_errors = []

    for match in BAD_ABSOLUTE_PATH.finditer(content):
        attr = match.group(1)
        url_val = match.group(3)

        # Skip canonical and meta social tags
        if line_is_in_meta_or_canonical(filepath, match.start(), content):
            continue

        # Skip href="/" — valid homepage link
        if url_val == '/':
            continue

        # Skip external absolute URLs
        if url_val.startswith('//'):
            continue

        # This is an internal root-relative absolute path - flag it
        file_errors.append(f"  WARN: Absolute path still present [{attr}=\"{url_val}\"]")

    if file_errors:
        has_errors = True
        print(f"In {rel_path}:")
        for e in file_errors[:5]:
            print(e)
        if len(file_errors) > 5:
            print(f"  ... and {len(file_errors) - 5} more")
        print()

# Check JS files
js_check_files = [
    os.path.join(root_dir, "js", "blogs.js"),
    os.path.join(root_dir, "js", "blogs-detail.js"),
]
BAD_ABS_JS = re.compile(r'href=\\?["\']/(blogs[^"\'\\]*)', re.IGNORECASE)
for jsf in js_check_files:
    rel_path = os.path.relpath(jsf, root_dir).replace('\\', '/')
    with open(jsf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for match in BAD_ABS_JS.finditer(content):
        has_errors = True
        print(f"WARN JS: Absolute path in {rel_path}: href=\"/{match.group(1)}\"")

# Verify sitemap.xml has physical .html URLs
sitemap_path = os.path.join(root_dir, "sitemap.xml")
sitemap_urls = re.findall(r'<loc>(.*?)</loc>', open(sitemap_path, 'r').read())
for s_url in sitemap_urls:
    if not s_url.endswith('.html') and s_url != 'https://airmedical24x7.com/':
        has_errors = True
        print(f"SITEMAP WARN: Non-physical URL: {s_url}")

if not has_errors:
    print("SUCCESS: All checks passed! All links are relative, all JS uses physical paths, sitemap OK.")
else:
    print("\nSome issues found (see above). Review and fix before deploying.")
