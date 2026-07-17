import os
import re

pattern = re.compile(
    r'<p class="mb-0">\s*<i class="fa fa-phone-alt text-primary me-3"></i>\s*'
    r'<a href="tel:\+971565542001"[^>]*>\s*\+971 56 554 2001\s*</a>\s*</p>'
    r'\s*<p class="mb-0">\s*<i class="fa fa-phone-alt text-primary me-3"></i>\s*'
    r'<a href="tel:\+97143230261"[^>]*>\s*\+971 4 323 0261\s*</a>\s*</p>'
    r'\s*<p class="mb-0">\s*<i class="fa fa-phone-alt text-primary me-3"></i>\s*'
    r'<a href="tel:\+911171859928"[^>]*>\s*\+91 11 7185 9928\s*</a>\s*</p>'
    r'\s*<p class="mb-0">\s*<i class="fa fa-phone-alt text-primary me-3"></i>\s*'
    r'<a href="tel:\+919217710155"[^>]*>\s*\+91 92177 10155\s*</a>\s*</p>',
    re.DOTALL
)

html_files = []
matching_files = []
non_matching_files = []

for root, dirs, files in os.walk('.'):
    # Skip any ignored folders or temporary/venv folders
    if 'node_modules' in root or '.git' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            html_files.append(filepath)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if pattern.search(content):
                    matching_files.append(filepath)
                else:
                    # Let's see if it contains one of the numbers
                    if '+971 4 323 0261' in content:
                        non_matching_files.append(filepath)

print(f"Total HTML files scanned: {len(html_files)}")
print(f"Matching files: {len(matching_files)}")
print(f"Non-matching files containing the number: {len(non_matching_files)}")
if non_matching_files:
    print("Sample non-matching file:")
    print(non_matching_files[:5])
