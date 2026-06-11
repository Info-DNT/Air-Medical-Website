import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check nav links
nav_links = re.findall(r'class="nav[^"]*"[^>]*href="([^"]+)"', content)
print('=== NAV LINKS ===')
for l in nav_links[:15]:
    print(' ', l)

# Check footer links
footer_links = re.findall(r'class="text-light[^"]*"[^>]*href="([^"]+)"', content)
print('\n=== FOOTER LINKS ===')
for l in footer_links[:12]:
    print(' ', l)

# Check JSON-LD @id and url
print('\n=== JSON-LD @id / url fields ===')
ids = re.findall(r'"(?:@id|url)"\s*:\s*"([^"]+)"', content)
for i in ids[:15]:
    print(' ', i)

# Check canonical
canonical = re.findall(r'rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', content)
print('\n=== CANONICAL ===')
for c in canonical:
    print(' ', c)

# Check for any remaining .html in hrefs
remaining = re.findall(r'href="([^"]*\.html[^"]*)"', content)
nav_remaining = [r for r in remaining if not any(r.lower().endswith(e) for e in ('.css','.js','.png','.jpg','.gif','.svg'))]
print('\n=== REMAINING .html IN HREFs (should be empty) ===')
for r in nav_remaining[:10]:
    print('  WARN:', r)
if not nav_remaining:
    print('  (none - all clean!)')
