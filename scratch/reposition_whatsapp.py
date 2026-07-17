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

whatsapp_icon_html = """            <a class="text-body px-2" href="https://wa.me/971565542001" target="_blank">
              <i class="fab fa-whatsapp"></i>
            </a>"""

def process_file(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Left WhatsApp Text Link (and preceding separator)
    content = re.sub(r'<span class="topbar-separator">\|</span>\s*<a class="whatsapp-top-btn".*?</a>', '', content, flags=re.DOTALL)
    
    # 2. Remove Center WhatsApp Button
    content = re.sub(r'<!-- CENTER WHATSAPP \(PC ONLY\) -->\s*<div class="menu-whatsapp.*?</div>', '', content, flags=re.DOTALL)
    
    # 3. Add Right WhatsApp Icon (Only if not already added)
    if 'fab fa-whatsapp' not in content or 'text-body px-2' not in content:
        # Find the social media icons block
        # We look for the last social icon before the end of the col-md-6 text-lg-end
        social_pattern = r'(<a class="text-body px-2" href="https://www.instagram.com/airmedical24x7/">\s*<i class="fab fa-instagram"></i>\s*</a>)'
        if re.search(social_pattern, content):
            content = re.sub(social_pattern, r'\1\n' + whatsapp_icon_html, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for file in target_files:
    print(f"Processing {file}...")
    process_file(file)

print("Done!")
