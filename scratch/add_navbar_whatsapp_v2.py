import os
import re

# List of files to process
target_files = [
    "index.html", "about.html", "contact.html", "country.html", "career.html", "blog.html", "blog-detail.html", "privacy-policy.html", "terms-and-conditions.html"
]

# Add services and countries directories
for root, dirs, files in os.walk("services"):
    for file in files:
        if file.endswith(".html"):
            target_files.append(os.path.join(root, file))

for root, dirs, files in os.walk("countries"):
    for file in files:
        if file.endswith(".html"):
            target_files.append(os.path.join(root, file))

# Professional WhatsApp CTA Button for Navbar
# Using a specific class 'btn-nav-whatsapp' for custom styling
whatsapp_nav_btn = """
          <a href="https://wa.me/971565542001" class="btn btn-nav-whatsapp rounded-pill d-none d-lg-inline-flex align-items-center ms-3" target="_blank">
            <i class="fab fa-whatsapp me-2"></i>WhatsApp Chat
          </a>"""

def process_file(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove any previous attempts (icon inside Contact or misplaced button)
    content = re.sub(r'<a href="contact.html" class="nav-item nav-link">Contact\s*<i class="fab fa-whatsapp ms-1 text-success"></i></a>', '<a href="contact.html" class="nav-item nav-link">Contact</a>', content)
    content = re.sub(r'<a href="https://wa.me/971565542001" class="btn btn-success rounded-pill py-2 px-3 ms-3 d-none d-lg-block" target="_blank">\s*<i class="fab fa-whatsapp me-1"></i>WhatsApp\s*</a>', '', content, flags=re.DOTALL)
    
    # 2. Place the new button AFTER the "Contact" link
    contact_link = '<a href="contact.html" class="nav-item nav-link">Contact</a>'
    if contact_link in content:
        # Avoid double adding
        if 'btn-nav-whatsapp' not in content[content.find('navbar-collapse') : content.find('navbar-collapse')+1500]:
            content = content.replace(contact_link, contact_link + whatsapp_nav_btn)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for file in target_files:
    print(f"Processing {file}...")
    process_file(file)

print("Done!")
