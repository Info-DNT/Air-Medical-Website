import re

with open("career.html", "r", encoding="utf-8") as f:
    original = f.read()

content = original
print(f"Original length: {len(content)}")

# Step 1
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
print(f"After Step 1: {len(content)}")

# Step 2
content = re.sub(
    r'<a href="commercial-flight-stretcher" class="dropdown-item">Commercial Flight\s+Stretcher</a>',
    '<a href="commercial-flight-stretcher" class="dropdown-item">Airline Stretcher Services Worldwide</a>',
    content,
    flags=re.IGNORECASE
)
print(f"After Step 2: {len(content)}")

# Step 3
content_before = content
content = re.sub(
    r'<a[^>]*href="air-ambulance-charters"[^>]*>.*?Air\s+Ambulance\s+Charter.*?</a>\s*',
    '',
    content,
    flags=re.DOTALL
)
print(f"After Step 3 (Popular Links): {len(content)}")
if len(content_before) - len(content) > 1000:
    print(f"WARNING: Step 3 deleted {len(content_before) - len(content)} characters!")

# Step 4
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
print(f"After Step 4: {len(content)}")

# Step 5
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
print(f"After Step 5: {len(content)}")

# Step 6
old_footer_segment = """                    <p class="mb-0">
                        <i class="fa fa-phone-alt text-primary me-3"></i>
                        <a href="tel:+918800028727" style="text-decoration: none; color: inherit;">
                            +91 88000 28727
                        </a>
                    </p>"""
new_footer_segment = """                    <p class="mb-0">
                        <i class="fa fa-phone-alt text-primary me-3"></i>
                        <a href="tel:+911171859928" style="text-decoration: none; color: inherit;">
                            +91 11 7185 9928 (Landline)
                        </a>
                    </p>
                    <p class="mb-0">
                        <i class="fa fa-phone-alt text-primary me-3"></i>
                        <a href="tel:+919217710155" style="text-decoration: none; color: inherit;">
                            +91 9217710155 (Kongkita's Number)
                        </a>
                    </p>"""
content_before = content
content = content.replace(old_footer_segment, new_footer_segment)
print(f"After Step 6 (replace): {len(content)}")

# Step 9
content_before = content
content = re.sub(
    r'<!-- SOS Emergency Button -->\s*<div id="sos-btn" onclick="toggleSOS\(\)">.*?</div>\s*',
    '',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'<!-- SOS Popup -->\s*<div id="sos-popup">.*?</div>\s*</div>\s*',
    '',
    content,
    flags=re.DOTALL
)
content = re.sub(
    r'<div id="sos-popup">.*?</div>\s*</div>\s*',
    '',
    content,
    flags=re.DOTALL
)
print(f"After Step 9 (SOS): {len(content)}")
if len(content_before) - len(content) > 1000:
    print(f"WARNING: Step 9 deleted {len(content_before) - len(content)} characters!")
