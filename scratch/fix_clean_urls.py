"""
Fix all HTML files:
1. Strip .html from <a href="..."> navigation links (keep clean URLs)
2. Fix broken JSON-LD @id and url fields (user removed colons accidentally)
3. Fix canonical + og:url meta to use clean URLs (no .html)
4. Keep asset src/href (CSS, JS, IMG) unchanged - they need extensions
"""

import os
import re
import glob

ROOT = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(ROOT, "*.html")) +
    glob.glob(os.path.join(ROOT, "services", "*.html")) +
    glob.glob(os.path.join(ROOT, "countries", "*.html"))
)

# Known asset extensions that must KEEP their extension
ASSET_EXTENSIONS = ('.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
                    '.woff', '.woff2', '.ttf', '.eot', '.min.css', '.min.js')

def is_asset_path(path):
    """Returns True if the path is an asset (CSS/JS/image) - keep extension."""
    pl = path.lower()
    return any(pl.endswith(e) for e in ASSET_EXTENSIONS)

def href_strip_html(m):
    """For <a href="..."> matches, strip .html from the href value (if not an asset)."""
    full = m.group(0)
    attr = m.group(1)   # href or src or action
    quote = m.group(2)
    val = m.group(3)

    # Only strip .html from href (navigation links), not src (assets)
    if attr.lower() != 'href':
        return full

    # Don't touch external URLs (http/https/mailto/tel/sms/whatsapp/ftp//)
    if re.match(r'^(https?://|mailto:|tel:|sms:|ftp:|//|#|javascript:)', val, re.I):
        return full

    # Don't touch assets
    if is_asset_path(val):
        return full

    # Strip .html extension
    new_val = re.sub(r'\.html$', '', val, flags=re.I)

    # Handle index.html → / (or just remove it)
    if new_val in ('index', './index'):
        new_val = '/'

    if new_val == val:
        return full

    return f'{attr}={quote}{new_val}{quote}'

# Pattern for href/src/action attributes
ATTR_PATTERN = re.compile(
    r'\b(href|src|action)=(["\'])([^"\']*)\2',
    re.IGNORECASE
)

# Fix broken JSON-LD: "@id"https://... → "@id": "https://...
# and "url"https://... → "url": "https://...
# Pattern: "key"value" (missing colon and opening quote)
BROKEN_JSONLD_PATTERN = re.compile(
    r'"(@id|url)"(https://[^"]+)"',
    re.IGNORECASE
)

def fix_jsonld_field(m):
    key = m.group(1)
    val = m.group(2)
    # Also strip /index.html from end of URL, and .html from JSON-LD URLs
    val = re.sub(r'/index\.html$', '/', val)
    val = re.sub(r'\.html(#[^"]*)?$', lambda mm: (mm.group(1) or ''), val)
    return f'"{key}": "{val}"'

# Fix canonical href that might have .html
CANONICAL_PATTERN = re.compile(
    r'(<link\s[^>]*rel=["\']canonical["\'][^>]*href=["\'])([^"\']+)(["\'])',
    re.IGNORECASE
)

def fix_canonical(m):
    prefix = m.group(1)
    url = m.group(2)
    suffix = m.group(3)
    # Strip .html from canonical URL
    url = re.sub(r'/index\.html$', '/', url)
    url = re.sub(r'\.html$', '', url)
    return f'{prefix}{url}{suffix}'

# Fix og:url meta content
OG_URL_PATTERN = re.compile(
    r'(<meta\s[^>]*(?:property=["\']og:url["\']|name=["\']twitter:url["\'])[^>]*content=["\'])([^"\']+)(["\'])',
    re.IGNORECASE
)

def fix_og_url(m):
    prefix = m.group(1)
    url = m.group(2)
    suffix = m.group(3)
    url = re.sub(r'/index\.html$', '/', url)
    url = re.sub(r'\.html$', '', url)
    return f'{prefix}{url}{suffix}'

# Also fix JSON-LD "url" field with proper colon but .html value
JSONLD_URL_CLEAN = re.compile(
    r'("(?:@id|url)"\s*:\s*")(https://airmedical24x7\.com[^"]*\.html)(#[^"]*)?(")',
    re.IGNORECASE
)

def clean_jsonld_url(m):
    prefix = m.group(1)
    url = m.group(2)
    anchor = m.group(3) or ''
    suffix = m.group(4)
    # Strip .html
    url = re.sub(r'/index\.html$', '/', url)
    url = re.sub(r'\.html$', '', url)
    return f'{prefix}{url}{anchor}{suffix}'

total_changed = 0

for filepath in html_files:
    rel = os.path.relpath(filepath, ROOT).replace('\\', '/')
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        original = f.read()
    
    content = original

    # Step 1: Fix broken JSON-LD (missing colons from user edits)
    content = BROKEN_JSONLD_PATTERN.sub(fix_jsonld_field, content)

    # Step 2: Clean .html from any properly-formatted JSON-LD url/@id values
    content = JSONLD_URL_CLEAN.sub(clean_jsonld_url, content)

    # Step 3: Fix canonical link tags
    content = CANONICAL_PATTERN.sub(fix_canonical, content)

    # Step 4: Fix og:url meta tags
    content = OG_URL_PATTERN.sub(fix_og_url, content)

    # Step 5: Strip .html from all <a href="..."> navigation links
    content = ATTR_PATTERN.sub(href_strip_html, content)

    if content != original:
        total_changed += 1
        with open(filepath, 'w', encoding='utf-8', newline='') as f:
            f.write(content)
        print(f"[UPDATED] {rel}")
    else:
        print(f"[OK]      {rel}")

print(f"\nDone. Updated {total_changed} of {len(html_files)} HTML files.")
