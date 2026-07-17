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

# The WhatsApp icon link to be placed next to email
whatsapp_top_html = """
            <span class="topbar-separator">|</span>
            <a class="text-decoration-none text-body" href="https://wa.me/971565542001" target="_blank">
              <i class="fab fa-whatsapp"></i>
            </a>"""

def process_file(file_path):
    if not os.path.exists(file_path):
        return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ensure any old whatsapp-top-btn is gone
    content = re.sub(r'<span class="topbar-separator">\|</span>\s*<a class="whatsapp-top-btn".*?</a>', '', content, flags=re.DOTALL)
    
    # 2. Remove the one I previously added to the social bar (right side of topbar)
    content = re.sub(r'<a class="text-body px-2" href="https://wa.me/971565542001" target="_blank">\s*<i class="fab fa-whatsapp"></i>\s*</a>', '', content, flags=re.DOTALL)

    # 3. Add WhatsApp icon to the right side of the email in topbar-contact
    # Look for the email link and append the icon after it
    email_pattern = r'(<a class="text-decoration-none text-body" href="mailto:info@airmedical24x7.com">.*?</a>)'
    if re.search(email_pattern, content, flags=re.DOTALL):
        # Only add if it doesn't already have a whatsapp icon right after it
        if 'https://wa.me/971565542001' not in content[:content.find('topbar-contact') + 500]: 
            content = re.sub(email_pattern, r'\1' + whatsapp_top_html, content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

for file in target_files:
    print(f"Processing {file}...")
    process_file(file)

print("Done!")
