"""
Fix all remaining .html references in href navigation links across all HTML files.
Specifically handles links with fragment anchors like: ../contact-us.html#quoteForm
Also handles special cases in countries pages (cost-dubai, dubai, india, to-india) that 
may have additional .html links missed before.
"""
import re
import glob
import os

ROOT = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(ROOT, "*.html")) +
    glob.glob(os.path.join(ROOT, "services", "*.html")) +
    glob.glob(os.path.join(ROOT, "countries", "*.html"))
)

ASSET_EXTENSIONS = ('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
                    '.woff', '.woff2', '.ttf', '.eot')

def strip_html_from_href(m):
    quote = m.group(1)
    val = m.group(2)

    # Don't touch external URLs
    if re.match(r'^(https?://|mailto:|tel:|sms:|ftp:|//|#|javascript:)', val, re.I):
        return m.group(0)

    # Don't touch asset paths
    lower = val.lower().split('?')[0].split('#')[0]
    if any(lower.endswith(e) for e in ASSET_EXTENSIONS):
        return m.group(0)

    # Strip .html (preserve any query string or fragment after it)
    new_val = re.sub(r'\.html(?=[?#]|$)', '', val)

    # Handle index → /
    if new_val in ('index', '../index', './index'):
        new_val = '/'

    return f'href={quote}{new_val}{quote}'

HREF_PATTERN = re.compile(r'href=(["\'])([^"\']*)\1', re.IGNORECASE)

total_changed = 0
for filepath in html_files:
    rel = os.path.relpath(filepath, ROOT).replace("\\", "/")
    if rel in ["404.html", "admin.html"]:
        continue

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()

    content = HREF_PATTERN.sub(strip_html_from_href, original)

    if content != original:
        total_changed += 1
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        print(f"[FIXED] {rel}")

print(f"\nDone. Fixed {total_changed} files.")
