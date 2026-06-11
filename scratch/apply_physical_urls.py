import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html"))
)

print(f"Processing physical URL conversions in {len(html_files)} HTML files...")

asset_extensions = ['css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'ico', 'xml', 'txt', 'php', 'eot', 'woff2', 'woff', 'ttf']

def map_clean_to_physical(url_str):
    # If protocol/external, mailto, phone, sms, hash, or javascript, skip
    if (url_str.startswith('mailto:') or url_str.startswith('tel:') or 
        url_str.startswith('sms:') or url_str.startswith('#') or 
        url_str.startswith('javascript:') or 
        (url_str.startswith('http') and "airmedical24x7.com" not in url_str)):
        return url_str
        
    # Standardize domain prefix
    has_domain = False
    prefix = ""
    work_str = url_str
    
    if work_str.startswith("https://airmedical24x7.com"):
        has_domain = True
        prefix = "https://airmedical24x7.com"
        work_str = work_str[len("https://airmedical24x7.com"):]
    elif work_str.startswith("http://airmedical24x7.com"):
        has_domain = True
        prefix = "http://airmedical24x7.com"
        work_str = work_str[len("http://airmedical24x7.com"):]
        
    has_leading_slash = work_str.startswith('/')
    slug = work_str.lstrip('/')
    
    # Separate query parameters or hash
    parts = slug.split('?')
    slug_base = parts[0].split('#')[0]
    query_hash = work_str[len(slug_base) + (1 if has_leading_slash else 0):]
    
    # Skip asset files
    ext = slug_base.split('.')[-1].lower() if '.' in slug_base else ''
    if ext in asset_extensions:
        return url_str
        
    if slug_base.endswith('.html'):
        return url_str
        
    # Strip existing subdirectory folders if present
    if slug_base.startswith("services/"):
        slug_base = slug_base[9:]
    elif slug_base.startswith("countries/"):
        slug_base = slug_base[10:]
        
    # Normalize special cases
    if slug_base.lower() == "ecmo-transfer":
        slug_base = "ECMO-transfer"
    elif slug_base == "airline-stretcher-services":
        slug_base = "commercial-flight-stretcher"
        
    if slug_base == "" or slug_base == "index":
        new_slug = "index.html"
    elif slug_base in [
        "about-us", "contact-us", "career", "blogs", "blogs-detail", "countries",
        "privacy-policy", "terms-and-conditions", "commercial-stretcher-service",
        "ecmo-air-transfer", "medical-escort-dubai", "medical-tourism-india",
        "repatriation-services-dubai"
    ]:
        new_slug = f"{slug_base}.html"
    elif slug_base in [
        "air-ambulance", "air-ambulance-charters", "commercial-flight-stretcher",
        "flight-medical-escort-services", "hospital-acceptance", "doctor-appointment",
        "second-opinion-services", "custom-medical-packages", "ECMO-transfer",
        "commercial-airlines-medical-transfer-services", "medical-tourism-services"
    ]:
        new_slug = f"services/{slug_base}.html"
    elif slug_base.startswith("air-ambulance-"):
        new_slug = f"countries/{slug_base}.html"
    else:
        # Unknown slug without extension, keep unmodified
        return url_str
        
    new_url = prefix
    if has_leading_slash or has_domain:
        new_url += '/'
    new_url += new_slug + query_hash
    return new_url

# Regex to find double-quoted or single-quoted strings that look like URLs or paths
# E.g. href="/about-us", "url": "https://airmedical24x7.com/about-us", etc.
url_pattern = re.compile(r'(href|src|url|id|canonical|href=["\']canonical["\']\s+href|@id)["\']?\s*[:=]\s*(["\'])(.*?)\2', re.IGNORECASE)

updated_files_count = 0

for filepath in html_files:
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    if "diff" in rel_path.lower() or rel_path == "404.html" or rel_path == "admin.html":
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # 1. Update href attributes in anchors and canonical links
    def repl_href(match):
        prefix_tag = match.group(1)
        quote_char = match.group(2)
        url_val = match.group(3)
        mapped = map_clean_to_physical(url_val)
        
        # Keep formatting: prefix_tag="mapped"
        # Since the original match could have spaces or colon (e.g. "url": "value" or href="value")
        # Let's rebuild the match dynamically
        orig_match = match.group(0)
        start_idx = orig_match.index(quote_char)
        return orig_match[:start_idx] + quote_char + mapped + quote_char

    # Run replacements on tags/attributes
    content = url_pattern.sub(repl_href, content)
    
    # 2. Update clean URLs inside schema JSON strings (which are just strings inside script tags)
    # Let's target any absolute URL matching https://airmedical24x7.com/[slug] in quotes
    # E.g. "url": "https://airmedical24x7.com/about-us"
    # E.g. "@id": "https://airmedical24x7.com/about-us"
    schema_url_pattern = re.compile(r'(["\'])(https?://airmedical24x7\.com/[a-zA-Z0-9\-_/]+)\1')
    
    def repl_schema_url(match):
        quote_char = match.group(1)
        url_val = match.group(2)
        mapped = map_clean_to_physical(url_val)
        return quote_char + mapped + quote_char
        
    content = schema_url_pattern.sub(repl_schema_url, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_files_count += 1
        print(f"Updated physical URLs in: {rel_path}")
    else:
        print(f"No changes in: {rel_path}")

print(f"Completed! Updated physical URLs in {updated_files_count} HTML files.")
