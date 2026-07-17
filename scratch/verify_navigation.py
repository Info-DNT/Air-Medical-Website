import os
import re

base_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

expected_slugs = [
    "air-ambulance",
    "commercial-flight-stretcher",
    "flight-medical-escort-services",
    "ECMO-transfer",
    "organ-transplant-assistance",
    "medical-tourism",
    "medical-travel-assistance",
    "home-health-care",
    "hospital-acceptance",
    "doctor-appointment",
    "second-opinion-services",
]

dropdown_pattern = re.compile(
    r'<div class="dropdown-menu[^"]*">(.*?)</div>',
    re.DOTALL | re.IGNORECASE
)

popular_links_pattern = re.compile(
    r'<h4[^>]*>\s*Popular Links\s*</h4>\s*<div class="d-flex flex-column[^"]*">(.*?)</div>',
    re.DOTALL | re.IGNORECASE
)

def verify_file(filepath, relative_path):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify dropdown
    dropdown_match = dropdown_pattern.search(content)
    if not dropdown_match:
        # Some files might not have a dropdown (e.g. 404.html, if it exists)
        # Let's check if there's any dropdown menu at all
        if "Our Services" in content:
            print(f"[FAIL] {relative_path}: Has 'Our Services' text but no matching dropdown-menu block")
            return False
        return True

    dropdown_inner = dropdown_match.group(1)
    # Extract all href attributes
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', dropdown_inner)
    
    # Check that they match the expected slugs and order
    actual_slugs = []
    for href in hrefs:
        slug = href.replace("\\", "/").split("/")[-1]
        actual_slugs.append(slug)

    # Filter out empty or unrelated (e.g. '#') if any
    actual_slugs = [s for s in actual_slugs if s and s != "#"]

    if actual_slugs != expected_slugs:
        print(f"[FAIL] {relative_path}: Dropdown slugs mismatch.\n  Expected: {expected_slugs}\n  Actual:   {actual_slugs}")
        return False

    # Verify popular links
    popular_match = popular_links_pattern.search(content)
    if not popular_match:
        # Check if popular links footer block is expected
        if "Popular Links" in content:
            print(f"[FAIL] {relative_path}: Has 'Popular Links' text but no matching popular-links block")
            return False
        return True

    popular_inner = popular_match.group(1)
    hrefs_pop = re.findall(r'href=["\']([^"\']+)["\']', popular_inner)
    actual_slugs_pop = []
    for href in hrefs_pop:
        slug = href.replace("\\", "/").split("/")[-1]
        actual_slugs_pop.append(slug)
    actual_slugs_pop = [s for s in actual_slugs_pop if s and s != "#"]

    if actual_slugs_pop != expected_slugs:
        print(f"[FAIL] {relative_path}: Popular Links footer slugs mismatch.\n  Expected: {expected_slugs}\n  Actual:   {actual_slugs_pop}")
        return False

    # Check for .html extension in any service links
    for href in hrefs + hrefs_pop:
        if ".html" in href:
            print(f"[FAIL] {relative_path}: Contains .html extension in link: {href}")
            return False

    return True

def main():
    print("Starting verification of service links in all HTML files...\n")
    
    failed = 0
    passed = 0
    
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in {".git", "scratch", "lib", "css", "img", "js"}]
        
        for file in files:
            if file.endswith(".html"):
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, base_dir)
                
                # Skip 404.html if it exists and has no dropdown/footer
                if file == "404.html":
                    continue
                    
                if verify_file(full_path, relative_path):
                    passed += 1
                else:
                    failed += 1
                    
    print(f"\nVerification completed: {passed} passed, {failed} failed.")

if __name__ == "__main__":
    main()
