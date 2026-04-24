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

# Professional WhatsApp button for the navbar
whatsapp_nav_btn = """
          <a href="https://wa.me/971565542001" class="btn btn-success rounded-pill py-2 px-3 ms-3 d-none d-lg-block" target="_blank">
            <i class="fab fa-whatsapp me-1"></i>WhatsApp
          </a>"""

def process_file(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean up the icon I added INSIDE the Contact link in the previous turn
    content = re.sub(r'(<a href="contact.html" class="nav-item nav-link">Contact)\s*<i class="fab fa-whatsapp ms-1 text-success"></i>(</a>)', r'\1\2', content)
    
    # 2. Add the professional WhatsApp button at the end of the navbar-collapse
    # Find the closing tag of <div class="navbar-nav ...">
    nav_nav_end_pattern = r'(<div class="navbar-nav ms-auto py-0">.*?)(</div>\s*</div>)'
    if re.search(nav_nav_end_pattern, content, flags=re.DOTALL):
        # Only add if not already there
        if 'btn-success' not in content[content.find('navbar-collapse') : content.find('navbar-collapse')+1000]:
            content = re.sub(nav_nav_end_pattern, r'\1\2' + whatsapp_nav_btn, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for file in target_files:
    print(f"Processing {file}...")
    process_file(file)

print("Done!")
