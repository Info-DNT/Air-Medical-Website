import os
import re
import shutil
import glob

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

print("Starting SEO Updates...")

# 1. Rename airline-stretcher-services.html to commercial-flight-stretcher.html
old_stretcher_path = os.path.join(root_dir, "services", "airline-stretcher-services.html")
new_stretcher_path = os.path.join(root_dir, "services", "commercial-flight-stretcher.html")

if os.path.exists(old_stretcher_path):
    print(f"Renaming {old_stretcher_path} to {new_stretcher_path}")
    shutil.move(old_stretcher_path, new_stretcher_path)
else:
    print("airline-stretcher-services.html already renamed or does not exist.")

# Get all current HTML files
html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html"))
)

print(f"Found {len(html_files)} HTML files to process.")

def update_metadata(content, title, description, canonical_url, keywords=None):
    # Update title
    content = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", content, flags=re.IGNORECASE)
    
    # Update meta description
    if re.search(r'<meta[^>]*name="description"[^>]*content=".*?"', content, re.IGNORECASE):
        content = re.sub(r'(<meta[^>]*name="description"[^>]*content=").*?(")', f'\\g<1>{description}\\g<2>', content, flags=re.IGNORECASE)
    elif re.search(r'<meta[^>]*content=".*?"[^>]*name="description"', content, re.IGNORECASE):
        content = re.sub(r'(<meta[^>]*content=").*?("[^>]*name="description")', f'\\g<1>{description}\\g<2>', content, flags=re.IGNORECASE)
    else:
        # Insert meta description before title or preconnect
        content = content.replace("<head>", f'<head>\n  <meta name="description" content="{description}">')

    # Update meta keywords if provided
    if keywords:
        if re.search(r'<meta[^>]*name="keywords"[^>]*content=".*?"', content, re.IGNORECASE):
            content = re.sub(r'(<meta[^>]*name="keywords"[^>]*content=").*?(")', f'\\g<1>{keywords}\\g<2>', content, flags=re.IGNORECASE)
        elif re.search(r'<meta[^>]*content=".*?"[^>]*name="keywords"', content, re.IGNORECASE):
            content = re.sub(r'(<meta[^>]*content=").*?("[^>]*name="keywords")', f'\\g<1>{keywords}\\g<2>', content, flags=re.IGNORECASE)
        else:
            content = content.replace("<head>", f'<head>\n  <meta name="keywords" content="{keywords}">')

    # Update canonical url
    if re.search(r'<link[^>]*rel="canonical"[^>]*href=".*?"', content, re.IGNORECASE):
        content = re.sub(r'(<link[^>]*rel="canonical"[^>]*href=").*?(")', f'\\g<1>{canonical_url}\\g<2>', content, flags=re.IGNORECASE)
    else:
        content = content.replace("</head>", f'  <link rel="canonical" href="{canonical_url}">\n</head>')
        
    # Update OpenGraph Title, Description, and URL
    content = re.sub(r'(<meta[^>]*property="og:title"[^>]*content=").*?(")', f'\\g<1>{title}\\g<2>', content, flags=re.IGNORECASE)
    content = re.sub(r'(<meta[^>]*property="og:description"[^>]*content=").*?(")', f'\\g<1>{description}\\g<2>', content, flags=re.IGNORECASE)
    content = re.sub(r'(<meta[^>]*property="og:url"[^>]*content=").*?(")', f'\\g<1>{canonical_url}\\g<2>', content, flags=re.IGNORECASE)
    
    # Update Twitter Title & Description
    content = re.sub(r'(<meta[^>]*name="twitter:title"[^>]*content=").*?(")', f'\\g<1>{title}\\g<2>', content, flags=re.IGNORECASE)
    content = re.sub(r'(<meta[^>]*name="twitter:description"[^>]*content=").*?(")', f'\\g<1>{description}\\g<2>', content, flags=re.IGNORECASE)
    
    return content

def update_robots_tag(content):
    if "name=\"robots\"" not in content.lower():
        content = content.replace("</head>", '  <meta name="robots" content="index, follow">\n</head>')
    return content

def fix_h1_headings(content, main_h1_text=None):
    # Find all H1s
    h1_matches = list(re.finditer(r'<h1([^>]*)>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL))
    if len(h1_matches) > 1:
        # Keep the first H1, change subsequent ones to H2
        new_content = ""
        last_idx = 0
        for i, match in enumerate(h1_matches):
            start, end = match.span()
            new_content += content[last_idx:start]
            attrs = match.group(1)
            text = match.group(2)
            if i == 0:
                # First H1
                if main_h1_text:
                    new_content += f"<h1{attrs}>{main_h1_text}</h1>"
                else:
                    new_content += match.group(0)
            else:
                # Demote to H2
                # Remove display-4 classes or keep attrs and change h1 to h2
                new_content += f"<h2{attrs}>{text}</h2>"
            last_idx = end
        new_content += content[last_idx:]
        content = new_content
    elif len(h1_matches) == 1 and main_h1_text:
        content = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1>{main_h1_text}</h1>', content, count=1, flags=re.IGNORECASE | re.DOTALL)
    elif len(h1_matches) == 0 and main_h1_text:
        # Inject H1 before first H2 or main container
        # For simplicity, if there is a main heading like an H2 about-heading, we replace it with H1
        if "about-heading" in content:
            content = re.sub(r'<h2 class="about-heading">(.*?)</h2>', f'<h1 class="about-heading">\\g<1></h1>', content, count=1, flags=re.IGNORECASE)
    return content

# Read about-us.html footer to sync with career.html
about_us_path = os.path.join(root_dir, "about-us.html")
with open(about_us_path, "r", encoding="utf-8") as f:
    about_us_content = f.read()

# Extract about-us.html footer section
footer_start_idx = about_us_content.find("<!-- Footer Start -->")
footer_end_idx = about_us_content.find("<!-- Footer End -->")
about_us_footer_block = about_us_content[footer_start_idx:footer_end_idx + len("<!-- Footer End -->")]

# Extract scripts at bottom of about-us.html (from footer to </html>)
scripts_start_idx = footer_end_idx + len("<!-- Footer End -->")
about_us_scripts_block = about_us_content[scripts_start_idx:about_us_content.find("</html>")]

# Process each file
for filepath in html_files:
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    if "diff" in rel_path.lower() or rel_path == "404.html" or rel_path == "admin.html":
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # Global replace old stretcher link
    content = content.replace("airline-stretcher-services", "commercial-flight-stretcher")

    # Core Pages
    if rel_path == "index.html":
        content = update_metadata(
            content,
            title="Trusted Air Ambulance Globally | Air Medical 24X7",
            description="Air Medical 24X7 is a globally trusted provider of 24/7 ICU air ambulance flights, flight medical escorts, and international patient transfers.",
            canonical_url="https://airmedical24x7.com/"
        )
        # Verify Alt Tags
        content = content.replace('alt="Flight Medics Air Medical 24X7"', 'alt="Flight Medics Air Medical 24X7 Global ICU Air Ambulance"')
        
    elif rel_path == "about-us.html":
        content = update_metadata(
            content,
            title="About Air Medical 24X7 | Global Air Ambulance Experts",
            description="Learn about Air Medical 24X7, a trusted global provider of 24/7 ICU air ambulance flights, flight medical escorts, and worldwide patient transfers.",
            canonical_url="https://airmedical24x7.com/about-us"
        )
        # Change <h2> banner title to H1
        content = re.sub(
            r'<h2 class="about-heading">Providing 24X7 Air Ambulance, Medical Evacuation and Patient Transfer Services\s+Across The World</h2>',
            '<h1 class="about-heading">Air Medical 24X7 Trusted Global Air Ambulance & Medical Evacuation Services</h1>',
            content,
            flags=re.IGNORECASE
        )
        # Update Image Alt
        content = content.replace('src="img/about-us.png" alt=""', 'src="img/about-us.png" alt="Air Medical 24X7 Global ICU Air Ambulance and Medical Evacuation Specialists"')
        content = content.replace('src="img/about-us.png" alt="About Us"', 'src="img/about-us.png" alt="Air Medical 24X7 Global ICU Air Ambulance and Medical Evacuation Specialists"')

    elif rel_path == "contact-us.html":
        content = update_metadata(
            content,
            title="Contact Air Medical 24X7 | 24/7 Global Air Ambulance Helpdesk",
            description="Contact Air Medical 24X7 for 24/7 emergency medical flights, flight stretcher services, and worldwide patient transfers. Get a free quotation in 30 minutes.",
            canonical_url="https://airmedical24x7.com/contact-us"
        )
        content = fix_h1_headings(content, "Get In Touch With Air Medical 24X7")
        # Update Image Alt
        content = content.replace('src="img/about-us.png"\r\n                            alt="Contact Air Medical 24X7"', 'src="img/about-us.png"\r\n                            alt="Contact Air Medical 24X7 24/7 Emergency Support Team"')
        content = content.replace('src="img/about-us.png"\n                            alt="Contact Air Medical 24X7"', 'src="img/about-us.png"\n                            alt="Contact Air Medical 24X7 24/7 Emergency Support Team"')
        content = content.replace('src="img/about-us.png" alt="Contact Air Medical 24X7"', 'src="img/about-us.png" alt="Contact Air Medical 24X7 24/7 Emergency Support Team"')

    elif rel_path == "career.html":
        content = update_metadata(
            content,
            title="Careers | Join Air Medical 24X7 Life-Saving Team",
            description="Explore career opportunities at Air Medical 24X7. Join our global team of dedicated medical professionals, flight doctors, nurses, and paramedics.",
            canonical_url="https://airmedical24x7.com/career",
            keywords="Air Medical 24X7 careers, air ambulance jobs, flight doctor careers, flight nurse jobs, flight paramedic openings"
        )
        content = fix_h1_headings(content, "Join Our Global Life-Saving Team")
        # Update Image Alt
        content = content.replace('src="img/about-us.png"\r\n                            alt="Join Air Medical 24X7 Team"', 'src="img/about-us.png"\r\n                            alt="Air Medical 24X7 Careers - Join Our Flight Medical Crew"')
        content = content.replace('src="img/about-us.png"\n                            alt="Join Air Medical 24X7 Team"', 'src="img/about-us.png"\n                            alt="Air Medical 24X7 Careers - Join Our Flight Medical Crew"')
        content = content.replace('src="img/about-us.png" alt="Join Air Medical 24X7 Team"', 'src="img/about-us.png" alt="Air Medical 24X7 Careers - Join Our Flight Medical Crew"')
        
        # Inject JobPosting Schema
        job_schema = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "JobPosting",
    "title": "Flight Doctor",
    "description": "Critical care flight doctor supporting advanced cardiorespiratory life support and emergency patient evacuations globally.",
    "datePosted": "2026-06-01",
    "validThrough": "2027-06-01",
    "employmentType": "FULL_TIME",
    "hiringOrganization": {
      "@type": "Organization",
      "name": "Air Medical 24X7",
      "sameAs": "https://airmedical24x7.com/"
    },
    "jobLocation": {
      "@type": "Place",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Dubai",
        "addressCountry": "AE"
      }
    }
  }
  </script>"""
        if "JobPosting" not in content:
            content = content.replace("</head>", f"{job_schema}\n</head>")

        # Synchronize Footer with about-us.html
        f_start = content.find("<!-- Footer Start -->")
        f_end = content.find("<!-- Footer End -->")
        if f_start != -1 and f_end != -1:
            career_footer_block = content[f_start:f_end + len("<!-- Footer End -->")]
            content = content.replace(career_footer_block, about_us_footer_block)
            
            # Also sync libraries/scripts after footer
            scripts_start = content.find("<!-- Footer End -->") + len("<!-- Footer End -->")
            career_scripts_block = content[scripts_start:content.find("</html>")]
            content = content.replace(career_scripts_block, about_us_scripts_block)

    elif rel_path == "terms-and-conditions.html":
        content = update_metadata(
            content,
            title="Terms & Conditions | Air Medical 24X7",
            description="Read the Terms and Conditions of Air Medical 24X7 for air ambulance, medical evacuation, medical escorts, and global patient transportation services.",
            canonical_url="https://airmedical24x7.com/terms-and-conditions"
        )
        
    elif rel_path == "privacy-policy.html":
        content = update_metadata(
            content,
            title="Privacy Policy | Air Medical 24X7",
            description="Read the Privacy Policy of Air Medical 24X7 explaining how we collect, protect, and handle personal and medical data for patient transfer services.",
            canonical_url="https://airmedical24x7.com/privacy-policy"
        )
        
    elif rel_path == "blogs.html":
        content = update_metadata(
            content,
            title="Medical Blog & Insights | Air Medical 24X7",
            description="Stay updated with the Air Medical 24X7 blog. Read insights, tips, and news on global air ambulance services, medical evacuations, and patient transfers.",
            canonical_url="https://airmedical24x7.com/blogs"
        )
        
    elif rel_path == "blogs-detail.html":
        content = update_metadata(
            content,
            title="Medical Blog Detail | Air Medical 24X7",
            description="Read detailed medical insights, patient transfer guidelines, and air ambulance updates on the Air Medical 24X7 blog.",
            canonical_url="https://airmedical24x7.com/blogs-detail"
        )
        # Ensure we have H1 fallback tag
        if "<h1>" not in content.lower():
            content = content.replace("<body>", '<body>\n  <h1 style="display:none;">Air Medical 24X7 Medical Blog Detail</h1>')

    # Standard Service Pages (in services/)
    elif rel_path.startswith("services/"):
        filename = os.path.basename(rel_path)
        
        if filename == "air-ambulance.html":
            content = update_metadata(
                content,
                title="Air Ambulance Services Worldwide | 24/7 ICU Flights",
                description="Air Medical 24X7 provides global air ambulance services with ICU-equipped aircraft, onboard doctors, and international critical care evacuation.",
                canonical_url="https://airmedical24x7.com/air-ambulance"
            )
            content = fix_h1_headings(content, "24X7 Emergency Air Ambulance Worldwide | Critical Care Flights")
            content = content.replace('alt="Air Ambulance"', 'alt="Air Ambulance Services Worldwide"')
            
        elif filename == "air-ambulance-charters.html":
            content = update_metadata(
                content,
                title="24/7 Air Ambulance Charters | ICU Flights Worldwide",
                description="Book 24/7 worldwide air ambulance charters with ICU-equipped flights, onboard doctors, and emergency critical care evacuation by Air Medical 24X7.",
                canonical_url="https://airmedical24x7.com/air-ambulance-charters"
            )
            content = fix_h1_headings(content, "24X7 Air Ambulance Charter | ICU Medical Flights Worldwide")
            content = content.replace('alt="Air Ambulance Charter Services"', 'alt="24/7 Air Ambulance Charter Services Worldwide"')
            
        elif filename == "commercial-flight-stretcher.html":
            content = update_metadata(
                content,
                title="Commercial Flight Stretcher Service | Air Medical 24X7",
                description="Affordable commercial flight stretcher services worldwide with ICU medical escorts, FAA-approved equipment, and bed-to-bed patient care.",
                canonical_url="https://airmedical24x7.com/commercial-flight-stretcher",
                keywords="commercial flight stretcher, airline stretcher service, medical escort, patient transfer commercial flight, patient travel flat"
            )
            content = fix_h1_headings(content, "Commercial Flight Stretcher Service")
            content = content.replace('alt="Airline Stretcher Services"', 'alt="Commercial Flight Stretcher Service for Patients"')
            
        elif filename == "flight-medical-escort-services.html":
            content = update_metadata(
                content,
                title="Flight Medical Escort Service Worldwide | Air Medical 24X7",
                description="Professional flight medical escort services worldwide. Flight doctors and nurses provide expert in-flight care and bed-to-bed patient transfers.",
                canonical_url="https://airmedical24x7.com/flight-medical-escort-services",
                keywords="flight medical escort, medical travel escort, commercial flight medical escort, travel doctor escort"
            )
            content = fix_h1_headings(content, "Flight Medical Escort Service")
            content = content.replace('alt="Flight Medical Escort Service"', 'alt="Flight Medical Escort Service Worldwide"')
            
        elif filename == "hospital-acceptance.html":
            content = update_metadata(
                content,
                title="Hospital Acceptance & Bed Booking | Air Medical 24X7",
                description="Fast international hospital acceptance and ICU bed booking. We arrange global hospital admissions, doctor confirmation, and medical coordination.",
                canonical_url="https://airmedical24x7.com/hospital-acceptance",
                keywords="hospital acceptance, hospital bed booking, medical admission abroad, global hospital admission"
            )
            content = fix_h1_headings(content, "International Hospital Acceptance | Fast Bed Booking Service")
            content = content.replace('alt="Hospital Acceptance"', 'alt="International Hospital Acceptance & Bed Booking"')
            
        elif filename == "doctor-appointment.html":
            content = update_metadata(
                content,
                title="Global Doctor Appointments | Book Verified Specialists",
                description="Book doctor appointments abroad with verified specialists. Access second opinions, consultations, and full medical travel coordination support.",
                canonical_url="https://airmedical24x7.com/doctor-appointment",
                keywords="global doctor appointment, book doctor abroad, medical travel specialist, book doctor appointment"
            )
            content = fix_h1_headings(content, "Get Expert Second Opinions from Verified Doctors & Worldwide Specialists 24X7")
            content = content.replace('alt="Doctor Appointment"', 'alt="Global Doctor Appointments & Specialty Consultations"')
            
        elif filename == "second-opinion-services.html":
            content = update_metadata(
                content,
                title="Medical Second Opinion Online | Global Specialists",
                description="Get a medical second opinion online from world-renowned doctors. Expert diagnosis review and specialist treatment recommendations.",
                canonical_url="https://airmedical24x7.com/second-opinion-services",
                keywords="medical second opinion online, doctor second opinion, specialist diagnosis review"
            )
            content = fix_h1_headings(content, "Online Medical Second Opinion Expert Diagnosis Review")
            content = content.replace('alt="Medical Second Opinion Services"', 'alt="Online Medical Second Opinion by Global Specialists"')
            
        elif filename == "custom-medical-packages.html":
            content = update_metadata(
                content,
                title="Custom Medical Packages Abroad | Air Medical 24X7",
                description="We offer custom medical packages abroad with expert doctors, accredited hospitals, affordable treatments, and 24/7 global support.",
                canonical_url="https://airmedical24x7.com/custom-medical-packages",
                keywords="custom medical packages, affordable treatment abroad, medical packages overseas, global healthcare packages"
            )
            content = fix_h1_headings(content, "Affordable Medical Packages Abroad Global Treatment Plans")
            content = content.replace('alt="Custom Medical Packages"', 'alt="Custom Medical Packages Abroad - Global Treatment Plans"')
            
        elif filename == "ECMO-transfer.html":
            content = update_metadata(
                content,
                title="ECMO Medical Transfer Services | Critical Care Flights",
                description="Worldwide ECMO air transport for critically ill heart and lung failure patients. Safe ICU medical flights with onboard cardiac specialists.",
                canonical_url="https://airmedical24x7.com/ecmo-transfer"
            )
            content = fix_h1_headings(content, "ECMO Transfer Services | Air Medical 24X7 Air Ambulance")
            content = content.replace('alt="ECMO Transfer Services"', 'alt="ECMO Medical Transfer Services and Critical Care Flights"')
            
        elif filename == "commercial-airlines-medical-transfer-services.html":
            content = update_metadata(
                content,
                title="Commercial Flight Patient Transfers | Air Medical 24X7",
                description="Safe and reliable patient transfers on commercial airlines. Complete medical clearance, in-flight nursing care, and global bed-to-bed transfers.",
                canonical_url="https://airmedical24x7.com/commercial-airlines-medical-transfer-services"
            )
            content = fix_h1_headings(content, "Commercial Airlines Medical Transfer Services")
            content = content.replace('alt="Commercial Airlines Medical Transfer Services"', 'alt="Commercial Airlines Medical Transfer Services Worldwide"')
            
        elif filename == "medical-tourism-services.html":
            content = update_metadata(
                content,
                title="Global Medical Tourism Services | Air Medical 24X7",
                description="Coordinated international medical tourism services. Hospital admissions, treatment scheduling, medical travel coordination, and patient transfer support.",
                canonical_url="https://airmedical24x7.com/medical-tourism-services"
            )
            content = fix_h1_headings(content, "Medical Tourism Air Transport | Air Medical 24X7")
            content = content.replace('alt="Medical Tourism Services"', 'alt="Global Medical Tourism Services and Patient Transfers"')

    # Custom SEO Landing Pages in Root
    elif rel_path == "medical-escort-dubai.html":
        content = update_metadata(
            content,
            title="Flight Medical Escort Dubai | Commercial Flight Doctor",
            description="Affordable flight medical escorts in Dubai. ICU-trained doctors and nurses accompany patients on commercial flights for safe, bed-to-bed travel.",
            canonical_url="https://airmedical24x7.com/medical-escort-dubai"
        )
        content = fix_h1_headings(content, "Flight Medical Escort Dubai")
        
    elif rel_path == "commercial-stretcher-service.html":
        content = update_metadata(
            content,
            title="Commercial Flight Stretcher Service | Air Medical 24X7",
            description="Commercial flight stretcher services worldwide. We coordinate medical clearances, airline seat removal, and ICU escort support on scheduled flights.",
            canonical_url="https://airmedical24x7.com/commercial-stretcher-service"
        )
        content = fix_h1_headings(content, "Commercial Flight Stretcher Service")
        
    elif rel_path == "ecmo-air-transfer.html":
        content = update_metadata(
            content,
            title="ECMO Air Transport | Critical Care Life-Support Flight",
            description="Specialized ECMO air ambulance transfer for critically ill heart and lung failure patients. ICU-equipped aircraft staffed with onboard perfusionists.",
            canonical_url="https://airmedical24x7.com/ecmo-air-transfer"
        )
        content = fix_h1_headings(content, "ECMO Air Transport")
        
    elif rel_path == "repatriation-services-dubai.html":
        content = update_metadata(
            content,
            title="Medical Repatriation Dubai | Global Patient Transfer",
            description="Worldwide medical repatriation from Dubai. Secure, bed-to-bed patient transfers, commercial flight stretchers, and air ambulance with medical escort.",
            canonical_url="https://airmedical24x7.com/repatriation-services-dubai"
        )
        content = fix_h1_headings(content, "Medical Repatriation Services Dubai")
        
    elif rel_path == "medical-tourism-india.html":
        content = update_metadata(
            content,
            title="Medical Tourism in India | Hospital Admissions & Travel",
            description="Access world-class treatment in India. We coordinate verified doctor appointments, accredited hospital admissions, medical visas, and flight escorts.",
            canonical_url="https://airmedical24x7.com/medical-tourism-india"
        )
        content = fix_h1_headings(content, "Medical Tourism in India")

    # Custom SEO Landing Pages in countries/
    elif rel_path.startswith("countries/"):
        filename = os.path.basename(rel_path)
        
        # 30 standard country pages vs 4 custom ones
        if filename in ["air-ambulance-dubai.html", "air-ambulance-india.html", "air-ambulance-cost-dubai.html", "air-ambulance-to-india.html"]:
            slug = filename[:-5]
            title = ""
            desc = ""
            h1 = ""
            if filename == "air-ambulance-dubai.html":
                title = "Air Ambulance Dubai | Emergency ICU Medical Flights"
                desc = "Emergency ICU air ambulance services in Dubai. 24/7 bed-to-bed medical evacuation, critical care patient transfers, and neonatal flights with doctors."
                h1 = "Air Ambulance Dubai"
            elif filename == "air-ambulance-india.html":
                title = "Air Ambulance India | Emergency ICU Medical Flights"
                desc = "Emergency air ambulance service in India. Safe, bed-to-bed patient transfers, critical care medical flights, and organ transport domestic and globally."
                h1 = "Air Ambulance India"
            elif filename == "air-ambulance-cost-dubai.html":
                title = "Air Ambulance Cost in Dubai | Transparent Pricing"
                desc = "Get transparent details on air ambulance cost in Dubai. Free, detailed quotations in 30 minutes with zero hidden charges and competitive global rates."
                h1 = "Air Ambulance Cost Dubai"
            elif filename == "air-ambulance-to-india.html":
                title = "Air Ambulance Dubai to India | Emergency Repatriation"
                desc = "Emergency ICU air ambulance flights from Dubai to India. Bed-to-bed patient transfers, scheduled airline stretchers, and full medical team escort."
                h1 = "Air Ambulance Dubai to India"

            content = update_metadata(
                content,
                title=title,
                description=desc,
                canonical_url=f"https://airmedical24x7.com/{slug}"
            )
            content = update_robots_tag(content)
            content = fix_h1_headings(content, h1)
            # Schema
            schema_block = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{
      "@type": "Question",
      "name": "How quickly can you arrange an air ambulance?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We can typically coordinate flight readiness and clearances within 30 minutes of receiving patient details."
      }
    }]
  }
  </script>"""
            if "FAQPage" not in content:
                content = content.replace("</head>", f"{schema_block}\n</head>")
        
        elif filename != "index.html":
            # Standard 30 country pages
            slug = filename[:-5]
            country_name = slug.replace("air-ambulance-", "").title()
            
            # Special manual overrides for formatted names if needed
            if country_name == "Uae":
                country_name = "UAE"
            elif country_name == "Antigua-And-Barbuda":
                country_name = "Antigua and Barbuda"
            elif country_name == "Bosnia-And-Herzegovina":
                country_name = "Bosnia and Herzegovina"
                
            title = f"Air Ambulance Service in {country_name} | Air Medical 24X7"
            desc = f"Emergency air ambulance and medical evacuation services in {country_name} by Air Medical 24X7. 24/7 ICU flights, flight medical escorts, and bed-to-bed transfers."
            keywords = f"air ambulance {country_name}, medical evacuation {country_name}, ICU flight {country_name}, patient transfer {country_name}, medical repatriation {country_name}, Air Medical 24X7"
            
            content = update_metadata(
                content,
                title=title,
                description=desc,
                canonical_url=f"https://airmedical24x7.com/{slug}",
                keywords=keywords
            )
            content = update_robots_tag(content)
            
            # Fix duplicate headings
            content = fix_h1_headings(content)
            
            # Alt tag update
            old_img_str = f'src="../img/{slug[14:]}-country.jpg"'
            if old_img_str in content:
                content = content.replace(old_img_str, f'{old_img_str} alt="Air Ambulance and Medical Evacuation Services in {country_name}"')
            
            # Inject FAQ schema based on the HTML text
            faq_schema = f"""  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{{
      "@type": "Question",
      "name": "What is an air ambulance service in {country_name}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "An air ambulance service in {country_name} provides critical medical transportation by specially equipped aircraft for patients who require urgent or advanced medical care."
      }}
    }}, {{
      "@type": "Question",
      "name": "Does Air Medical 24X7 provide air ambulance services from {country_name}?",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "Yes. Air Medical 24X7 provides air ambulance and medical evacuation services from {country_name}, including coordination from major cities and airports."
      }}
    }}]
  }}
  </script>"""
            if "FAQPage" not in content:
                content = content.replace("</head>", f"{faq_schema}\n</head>")

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {rel_path}")
    else:
        print(f"No change: {rel_path}")

print("HTML pages optimization completed.")
