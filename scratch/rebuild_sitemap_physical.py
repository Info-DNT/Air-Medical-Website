import os
import glob
from datetime import datetime

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# Core files in root
core_files = [
    "about-us.html",
    "blogs-detail.html",
    "blogs.html",
    "career.html",
    "contact-us.html",
    "countries.html",
    "index.html",
    "privacy-policy.html",
    "terms-and-conditions.html",
    "commercial-stretcher-service.html",
    "ecmo-air-transfer.html",
    "medical-escort-dubai.html",
    "medical-tourism-india.html",
    "repatriation-services-dubai.html"
]

# Service files
service_files = glob.glob(os.path.join(root_dir, "services", "*.html"))
# Country files
country_files = glob.glob(os.path.join(root_dir, "countries", "*.html"))

urls = []
base_domain = "https://airmedical24x7.com"
today = datetime.now().strftime("%Y-%m-%d")

# Add core files
for f in core_files:
    if f == "index.html":
        # Root url
        urls.append((f"{base_domain}/", "1.0"))
    else:
        urls.append((f"{base_domain}/{f}", "0.9" if f in ["about-us.html", "contact-us.html", "career.html"] else "0.8"))

# Add service files
for fpath in service_files:
    fname = os.path.basename(fpath)
    urls.append((f"{base_domain}/services/{fname}", "0.9"))

# Add country files
for fpath in country_files:
    fname = os.path.basename(fpath)
    if fname == "index.html":
        urls.append((f"{base_domain}/countries/index.html", "0.8"))
    else:
        urls.append((f"{base_domain}/countries/{fname}", "0.8"))

# Generate XML
xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url, priority in sorted(urls, key=lambda x: x[0]):
    xml += '  <url>\n'
    xml += f'    <loc>{url}</loc>\n'
    xml += f'    <lastmod>{today}</lastmod>\n'
    xml += f'    <priority>{priority}</priority>\n'
    xml += '  </url>\n'

xml += '</urlset>\n'

sitemap_path = os.path.join(root_dir, "sitemap.xml")
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write(xml)

print(f"Sitemap updated successfully with {len(urls)} physical paths.")
