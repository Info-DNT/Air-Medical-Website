import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# Get all HTML files in root, services, and countries
html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html"))
)

print(f"Found {len(html_files)} HTML files to process.")

def process_file(filepath):
    rel_path = os.path.relpath(filepath, root_dir)
    # Skip temporary diff files and 404
    if "diff" in rel_path.lower() or rel_path == "404.html":
        return
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {rel_path}: {e}")
        return

    original_content = content

    # 1. Update "Our Services" dropdown menu: Remove Air Ambulance Charter
    content = re.sub(
        r'<li><a href="air-ambulance-charters" class="dropdown-item">Air Ambulance Charter</a></li>\s*',
        '',
        content
    )
    content = re.sub(
        r'<a href="air-ambulance-charters" class="dropdown-item">Air Ambulance Charter</a>\s*',
        '',
        content
    )

    # 2. Update "Our Services" dropdown menu: Rename Commercial Flight Stretcher
    content = re.sub(
        r'<a href="commercial-flight-stretcher" class="dropdown-item">Commercial Flight\s+Stretcher</a>',
        '<a href="commercial-flight-stretcher" class="dropdown-item">Airline Stretcher Services Worldwide</a>',
        content,
        flags=re.IGNORECASE
    )

    # 3. Update Popular Links in footer: Remove Air Ambulance Charter
    content = re.sub(
        r'<a[^>]*class="text-light[^"]*"[^>]*href="air-ambulance-charters"[^>]*>\s*<i[^>]*>.*?</i>\s*Air\s+Ambulance\s+Charter\s*</a>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # 4. Update "More Services" select options in forms
    content = re.sub(
        r'<option>Flight Wheelchair Services</option>\s*',
        '',
        content
    )
    content = re.sub(
        r'<option value="Private Medical Charter Jet">Private Medical Charter Jet</option>\s*',
        '',
        content
    )
    content = re.sub(
        r'<option>Private Medical Charter Jet</option>\s*',
        '',
        content
    )

    # 5. Update form headings from "Get a Free Quotation" to "Get a quotation in 30 minutes"
    content = re.sub(
        r'<h2 class="mb-2">Get a Free Quotation</h2>',
        '<h2 class="mb-2">Get a quotation in 30 minutes</h2>',
        content
    )
    content = re.sub(
        r'<h2 class="about-heading">Get a Free Quotation</h2>',
        '<h2 class="about-heading">Get a quotation in 30 minutes</h2>',
        content
    )
    content = re.sub(
        r'<h4 class="text-primary mb-2 text-center">\s*Get a Free Quotation Worldwide\s*</h4>',
        '<h4 class="text-primary mb-2 text-center">Get a quotation in 30 minutes</h4>',
        content
    )
    content = re.sub(
        r'<h4 class="quote-modal-title">Get a Free Quotation Worldwide</h4>',
        '<h4 class="quote-modal-title">Get a quotation in 30 minutes</h4>',
        content
    )

    # Remove redundant sub-heading clock text
    content = re.sub(
        r'<p class="text-muted mb-4 small fw-bold[^"]*">\s*<i class="far fa-clock text-red me-1"></i>\s*Get a quotation in 30\s*minutes\s*</p>\s*',
        '',
        content,
        flags=re.IGNORECASE
    )

    # 6. Replace Indian mobile phone number (+91 88000 28727) in footer
    footer_phone_pattern = r'<p class="mb-0">\s*<i class="fa fa-phone-alt text-primary me-3"></i>\s*<a href="tel:\+918800028727"[^>]*>\s*\+91 88000 28727\s*</a>\s*</p>'
    new_footer_phones = """          <p class="mb-0">
            <i class="fa fa-phone-alt text-primary me-3"></i>
            <a href="tel:+911171859928" style="text-decoration: none; color: inherit;">
              +91 11 7185 9928
            </a>
          </p>
          <p class="mb-0">
            <i class="fa fa-phone-alt text-primary me-3"></i>
            <a href="tel:+919217710155" style="text-decoration: none; color: inherit;">
              +91 9217710155
            </a>
          </p>"""
    content = re.sub(footer_phone_pattern, new_footer_phones, content)

    # Also handle alternate indentation in countries/services folder footers
    footer_phone_pattern_indent = r'<p class="mb-0">\s*<i class="fa fa-phone-alt text-primary me-3"></i>\s*<a href="tel:\+918800028727"[^>]*>\s*\+91 88000 28727\s*</a>\s*</p>'
    # We can perform a general string replacement for the footer block to be safe:
    old_footer_segment = """                    <p class="mb-0">
                        <i class="fa fa-phone-alt text-primary me-3"></i>
                        <a href="tel:+918800028727" style="text-decoration: none; color: inherit;">
                            +91 88000 28727
                        </a>
                    </p>"""
    new_footer_segment = """                    <p class="mb-0">
                        <i class="fa fa-phone-alt text-primary me-3"></i>
                        <a href="tel:+911171859928" style="text-decoration: none; color: inherit;">
                            +91 11 7185 9928
                        </a>
                    </p>
                    <p class="mb-0">
                        <i class="fa fa-phone-alt text-primary me-3"></i>
                        <a href="tel:+919217710155" style="text-decoration: none; color: inherit;">
                            +91 9217710155
                        </a>
                    </p>"""
    content = content.replace(old_footer_segment, new_footer_segment)

    # 7. Replace phone numbers in contact-us.html body
    if rel_path == "contact-us.html":
        old_body_phone = """                        <a href="tel:+918800028727" class="text-dark mb-2">+91 88000 28727</a>"""
        new_body_phone = """                        <a href="tel:+911171859928" class="text-dark mb-2">+91 11 7185 9928</a>
                        <a href="tel:+919217710155" class="text-dark mb-2">+91 9217710155</a>"""
        content = content.replace(old_body_phone, new_body_phone)

    # 8. Replace phone numbers in Schema.org JSON-LD structured data
    schema_point_pattern = r'\{\s*"@type":\s*"ContactPoint",\s*"telephone":\s*"\+918800028727",\s*"contactType":\s*"Customer Support / Emergency",\s*"areaServed":\s*"IN",\s*"availableLanguage":\s*\[\s*"en",\s*"hi"\s*\]\s*\}'
    new_schema_points = """{
      "@type": "ContactPoint",
      "telephone": "+911171859928",
      "contactType": "Customer Support / Emergency",
      "areaServed": "IN",
      "availableLanguage": [
        "en",
        "hi"
      ]
    },
    {
      "@type": "ContactPoint",
      "telephone": "+919217710155",
      "contactType": "Customer Support / Emergency",
      "areaServed": "IN",
      "availableLanguage": [
        "en",
        "hi"
      ]
    }"""
    content = re.sub(schema_point_pattern, new_schema_points, content)

    # Fallback/alternate schema matching:
    schema_point_pattern_alt = r'\{\s*"@type":\s*"ContactPoint",\s*"telephone":\s*"\+918800028727",\s*"contactType":\s*"Emergency Medical Transport",\s*"areaServed":\s*"IN",\s*"availableLanguage":\s*\[\s*"en",\s*"hi"\s*\]\s*\}'
    new_schema_points_alt = """{
      "@type": "ContactPoint",
      "telephone": "+911171859928",
      "contactType": "Emergency Medical Transport",
      "areaServed": "IN",
      "availableLanguage": [
        "en",
        "hi"
      ]
    },
    {
      "@type": "ContactPoint",
      "telephone": "+919217710155",
      "contactType": "Emergency Medical Transport",
      "areaServed": "IN",
      "availableLanguage": [
        "en",
        "hi"
      ]
    }"""
    content = re.sub(schema_point_pattern_alt, new_schema_points_alt, content)

    # General replacements for any leftover JSON-LD references
    content = content.replace('"telephone": "+918800028727"', '"telephone": "+911171859928", "telephone2": "+919217710155"')

    # 9. Delete the SOS button and popup
    # Match SOS button div
    content = re.sub(
        r'<!-- SOS Emergency Button -->\s*<div id="sos-btn" onclick="toggleSOS\(\)">.*?</div>\s*',
        '',
        content,
        flags=re.DOTALL
    )
    # Match SOS popup block
    content = re.sub(
        r'<!-- SOS Popup -->\s*<div id="sos-popup">.*?</div>\s*</div>\s*',
        '',
        content,
        flags=re.DOTALL
    )
    # Alternate without comment
    content = re.sub(
        r'<div id="sos-popup">.*?</div>\s*</div>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # 10. Make mobile sticky bottom CTA bar visible on desktop
    content = content.replace(
        '<div class="mobile-sticky-cta d-lg-none">',
        '<div class="mobile-sticky-cta">'
    )

    # Check if anything changed and write
    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {rel_path}")
        except Exception as e:
            print(f"Error writing {rel_path}: {e}")
    else:
        print(f"No changes for: {rel_path}")

if __name__ == "__main__":
    for f in html_files:
        process_file(f)
    print("Batch processing completed.")
