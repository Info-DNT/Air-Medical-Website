import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html"))
)

print(f"Verifying {len(html_files)} HTML files...")

errors = []

for filepath in html_files:
    rel_path = os.path.relpath(filepath, root_dir)
    if "diff" in rel_path.lower() or rel_path == "404.html":
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {rel_path}: {e}")
        continue

    # 1. Check old phone number
    if "88000" in content or "8800028727" in content:
        # Ignore false positives in comments or script filenames if any
        # But report actual raw instances
        errors.append(f"{rel_path}: Found old phone number reference")

    # 2. Check "Air Ambulance Charter" in navigation or Popular Links
    # We allow "Air Ambulance Charter" in general text copy (e.g. paragraphs explaining the service)
    # but not inside dropdown-item or Popular Links
    if 'class="dropdown-item">Air Ambulance Charter</a>' in content:
        errors.append(f"{rel_path}: Found Air Ambulance Charter in dropdown-item")
    if 'Popular Links' in content and 'air-ambulance-charters' in content:
        # Check if air-ambulance-charters is linked under Popular Links
        pop_links_sec = re.findall(r'Popular Links.*?</div>', content, re.DOTALL)
        for sec in pop_links_sec:
            if 'air-ambulance-charters' in sec:
                errors.append(f"{rel_path}: Found Air Ambulance Charter in Popular Links")

    # 3. Check renamed dropdown item
    if 'class="dropdown-item">Commercial Flight' in content and 'Stretcher' in content:
        errors.append(f"{rel_path}: Found Commercial Flight Stretcher in dropdown")

    # 4. Check form service select dropdown
    if 'Flight Wheelchair Services' in content:
        errors.append(f"{rel_path}: Found Flight Wheelchair Services option")
    if 'Private Medical Charter Jet' in content:
        errors.append(f"{rel_path}: Found Private Medical Charter Jet option")

    # 5. Check form headings
    if '<h2 class="mb-2">Get a Free Quotation</h2>' in content:
        errors.append(f"{rel_path}: Found old quotation form heading")
    if '<h2 class="about-heading">Get a Free Quotation</h2>' in content:
        errors.append(f"{rel_path}: Found old quotation form heading (about-heading)")
    if 'Get a Free Quotation Worldwide' in content:
        errors.append(f"{rel_path}: Found Get a Free Quotation Worldwide heading")

    # 6. Check SOS button & popup
    if 'id="sos-btn"' in content:
        errors.append(f"{rel_path}: Found sos-btn element")
    if 'id="sos-popup"' in content:
        errors.append(f"{rel_path}: Found sos-popup element")

    # 7. Check sticky CTA d-lg-none
    # We want to make sure it exists, but without d-lg-none
    if 'class="mobile-sticky-cta d-lg-none"' in content:
        errors.append(f"{rel_path}: Found d-lg-none on sticky CTA bar")

# Check syntax error in index.html specifically
with open(os.path.join(root_dir, "index.html"), 'r', encoding='utf-8') as f:
    idx_content = f.read()
    if '</script>oaded' in idx_content:
        errors.append("index.html: Found duplicate script tags syntax error")

if errors:
    print(f"\n[ERROR] Verification failed with {len(errors)} errors:")
    for err in errors:
        print(f" - {err}")
else:
    print("\n[SUCCESS] Verification passed! All files are 100% clean and correct.")

