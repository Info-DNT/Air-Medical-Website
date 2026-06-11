"""
Final fixes for index.html:
1. Fix JSON-LD @id fragment: /index#xxx → /#xxx (root fragment)
2. Fix blog inline link: blogs-detail.html?slug= → blogs-detail?slug=
3. Fix navbar Home link: shows as "/" which is correct but let's verify nav section
"""
import re

filepath = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main\index.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

original = content

# Fix 1: JSON-LD @id with /index# → /# (the fragment anchor should be on the root)
# e.g. https://airmedical24x7.com/index#organization → https://airmedical24x7.com/#organization
content = re.sub(
    r'(https://airmedical24x7\.com)/index(#[a-zA-Z0-9_-]+)',
    r'\1/\2',
    content
)

# Fix 2: blogs-detail.html?slug= in inline JS template literal
content = content.replace(
    'href="blogs-detail.html?slug=${b.slug}"',
    'href="blogs-detail?slug=${b.slug}"'
)

if content != original:
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        f.write(content)
    print("Fixed index.html successfully.")
else:
    print("No changes needed.")

# Quick verify
ids = re.findall(r'"@id"\s*:\s*"([^"]+)"', content)
print("\n@id values:")
for i in ids:
    print(" ", i)
