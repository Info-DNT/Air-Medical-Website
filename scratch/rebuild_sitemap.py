import xml.etree.ElementTree as ET
import os

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
sitemap_path = os.path.join(root_dir, "sitemap.xml")

clean_urls = [
    # Core
    "https://airmedical24x7.com/",
    "https://airmedical24x7.com/about-us",
    "https://airmedical24x7.com/blogs-detail",
    "https://airmedical24x7.com/blogs",
    "https://airmedical24x7.com/career",
    "https://airmedical24x7.com/contact-us",
    "https://airmedical24x7.com/countries",
    "https://airmedical24x7.com/privacy-policy",
    "https://airmedical24x7.com/terms-and-conditions",

    # Services
    "https://airmedical24x7.com/air-ambulance",
    "https://airmedical24x7.com/air-ambulance-charters",
    "https://airmedical24x7.com/commercial-flight-stretcher",
    "https://airmedical24x7.com/flight-medical-escort-services",
    "https://airmedical24x7.com/hospital-acceptance",
    "https://airmedical24x7.com/doctor-appointment",
    "https://airmedical24x7.com/second-opinion-services",
    "https://airmedical24x7.com/custom-medical-packages",
    "https://airmedical24x7.com/ecmo-transfer",
    "https://airmedical24x7.com/commercial-airlines-medical-transfer-services",
    "https://airmedical24x7.com/medical-tourism-services",

    # Custom Landing Pages in Root
    "https://airmedical24x7.com/medical-escort-dubai",
    "https://airmedical24x7.com/commercial-stretcher-service",
    "https://airmedical24x7.com/ecmo-air-transfer",
    "https://airmedical24x7.com/repatriation-services-dubai",
    "https://airmedical24x7.com/medical-tourism-india",

    # Custom Country Landing Pages
    "https://airmedical24x7.com/air-ambulance-dubai",
    "https://airmedical24x7.com/air-ambulance-india",
    "https://airmedical24x7.com/air-ambulance-cost-dubai",
    "https://airmedical24x7.com/air-ambulance-to-india",

    # Standard Country Pages (30)
    "https://airmedical24x7.com/air-ambulance-afghanistan",
    "https://airmedical24x7.com/air-ambulance-albania",
    "https://airmedical24x7.com/air-ambulance-algeria",
    "https://airmedical24x7.com/air-ambulance-andorra",
    "https://airmedical24x7.com/air-ambulance-angola",
    "https://airmedical24x7.com/air-ambulance-antigua-and-barbuda",
    "https://airmedical24x7.com/air-ambulance-argentina",
    "https://airmedical24x7.com/air-ambulance-armenia",
    "https://airmedical24x7.com/air-ambulance-australia",
    "https://airmedical24x7.com/air-ambulance-austria",
    "https://airmedical24x7.com/air-ambulance-azerbaijan",
    "https://airmedical24x7.com/air-ambulance-bahamas",
    "https://airmedical24x7.com/air-ambulance-bahrain",
    "https://airmedical24x7.com/air-ambulance-bangladesh",
    "https://airmedical24x7.com/air-ambulance-barbados",
    "https://airmedical24x7.com/air-ambulance-belarus",
    "https://airmedical24x7.com/air-ambulance-belgium",
    "https://airmedical24x7.com/air-ambulance-belize",
    "https://airmedical24x7.com/air-ambulance-benin",
    "https://airmedical24x7.com/air-ambulance-bhutan",
    "https://airmedical24x7.com/air-ambulance-bolivia",
    "https://airmedical24x7.com/air-ambulance-bosnia-and-herzegovina",
    "https://airmedical24x7.com/air-ambulance-ethiopia",
    "https://airmedical24x7.com/air-ambulance-indonesia",
    "https://airmedical24x7.com/air-ambulance-kuwait",
    "https://airmedical24x7.com/air-ambulance-oman",
    "https://airmedical24x7.com/air-ambulance-qatar",
    "https://airmedical24x7.com/air-ambulance-saudi-arabia",
    "https://airmedical24x7.com/air-ambulance-seychelles",
    "https://airmedical24x7.com/air-ambulance-uae",
]

print(f"Total URLs to add to sitemap: {len(clean_urls)}")

# Generate XML content manually to have beautiful formatting and exact indentation
xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for url in clean_urls:
    # Set priority
    if url == "https://airmedical24x7.com/":
        priority = "1.0"
    elif any(x in url for x in ["about-us", "contact-us", "career", "countries"]):
        priority = "0.9"
    elif "air-ambulance-" in url:
        priority = "0.7"  # Country pages
    else:
        priority = "0.8"  # Service pages
        
    xml_content += '  <url>\n'
    xml_content += f'    <loc>{url}</loc>\n'
    xml_content += '    <lastmod>2026-06-09</lastmod>\n'
    xml_content += f'    <priority>{priority}</priority>\n'
    xml_content += '  </url>\n'

xml_content += '</urlset>\n'

with open(sitemap_path, "w", encoding="utf-8") as f:
    f.write(xml_content)

print(f"sitemap.xml successfully updated at {sitemap_path}")
