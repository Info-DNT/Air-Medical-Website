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

whatsapp_nav_html = ' <i class="fab fa-whatsapp ms-1 text-success"></i>'

def process_file(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Topbar completely
    content = re.sub(r'<!-- Topbar Start -->.*?<!-- Topbar End -->', '', content, flags=re.DOTALL)
    
    # 2. Add WhatsApp icon to the right of the "Contact" nav link
    # Pattern to find the Contact link
    contact_pattern = r'(<a href="contact.html" class="nav-item nav-link">Contact)(</a>)'
    if re.search(contact_pattern, content):
        # Only add if not already there
        if 'fa-whatsapp' not in content[content.find('Contact')-50 : content.find('Contact')+100]:
            content = re.sub(contact_pattern, r'\1' + whatsapp_nav_html + r'\2', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for file in target_files:
    print(f"Processing {file}...")
    process_file(file)

print("Done!")
