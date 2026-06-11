import os
import re
import glob

ROOT = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

def verify():
    html_files = glob.glob(os.path.join(ROOT, "*.html")) + \
                 glob.glob(os.path.join(ROOT, "services", "*.html")) + \
                 glob.glob(os.path.join(ROOT, "countries", "*.html"))
                 
    sitemap_path = os.path.join(ROOT, "sitemap.xml")
    errors = []
    
    # 1. Verify sitemap.xml
    if os.path.exists(sitemap_path):
        with open(sitemap_path, "r", encoding="utf-8") as f:
            content = f.read()
        if ".html</loc>" in content:
            errors.append("sitemap.xml still contains references to .html in <loc> elements!")
    else:
        errors.append("sitemap.xml not found!")

    # 2. Verify HTML files
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, ROOT)
        
        # Skip admin.html
        if "admin.html" in rel_path:
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Check canonical
        canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content, re.IGNORECASE)
        if canonical_match:
            canonical_url = canonical_match.group(1)
            if ".html" in canonical_url:
                errors.append(f"{rel_path}: Canonical URL contains .html: {canonical_url}")
                
        # Check GTM & Google Ads Tag (early loading script)
        if "GTM-KG4BQ6SM" in content and "Optimized Google Analytics and GTM Lazy Loader" not in content:
            errors.append(f"{rel_path}: GTM exists but does not use the lazy loader script!")
            
        if "googletagmanager.com/gtag/js" in content and "Optimized Google Analytics and GTM Lazy Loader" not in content:
            errors.append(f"{rel_path}: Gtag.js exists but does not use the lazy loader script!")

        # Check for any remaining required fields in quoteForm
        form_pattern = re.compile(r'<form[^>]*id="quoteForm"[^>]*>([\s\S]+?)</form>', re.IGNORECASE)
        form_match = form_pattern.search(content)
        if form_match:
            form_body = form_match.group(1)
            required_tags = re.findall(r'<[^>]*\brequired\b[^>]*>', form_body, re.IGNORECASE)
            if required_tags:
                errors.append(f"{rel_path}: Form has required attributes: {required_tags}")
                
            # Check duplicate radio button for Flight Medical Escort
            if 'type="radio"' in form_body and 'value="Flight Medical Escort"' in form_body:
                errors.append(f"{rel_path}: Form still contains Flight Medical Escort radio option!")

            # Verify that stretcher service was renamed to Airline Stretcher Services Worldwide
            if 'Commercial Flight Stretcher' in form_body:
                errors.append(f"{rel_path}: Form still contains legacy Commercial Flight Stretcher option!")
            if 'Airline Stretcher Services' in form_body and 'Airline Stretcher Services Worldwide' not in form_body:
                errors.append(f"{rel_path}: Form contains Airline Stretcher Services without Worldwide!")

        # Check script deferring for config.js
        if 'config.js' in content and 'config.js" defer' not in content:
            config_pattern = re.compile(r'js/config\.js', re.IGNORECASE)
            if config_pattern.search(content) and 'js/config.js" defer' not in content and '../js/config.js" defer' not in content:
                errors.append(f"{rel_path}: config.js is not deferred!")

        # Check images loading attribute
        img_pattern = re.compile(r'<img\s+([^>]+)>', re.IGNORECASE)
        images = img_pattern.findall(content)
        for attrs in images:
            if 'loading=' not in attrs.lower():
                errors.append(f"{rel_path}: Image is missing loading attribute: <img {attrs}>")
                
    if errors:
        print(f"Verification FAILED with {len(errors)} errors:")
        for err in errors[:20]:
            print(f"  - {err}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors.")
    else:
        print("Verification PASSED! All optimizations, URL updates, form renames, and submission fixes are correct.")

if __name__ == "__main__":
    verify()
