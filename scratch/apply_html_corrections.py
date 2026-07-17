import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# 1. Collect all target files
html_files = []
# Scan root HTML files
for f in os.listdir(root_dir):
    if f.endswith(".html"):
        html_files.append(os.path.join(root_dir, f))

# Scan countries directory
countries_dir = os.path.join(root_dir, "countries")
if os.path.exists(countries_dir):
    for f in os.listdir(countries_dir):
        if f.endswith(".html"):
            html_files.append(os.path.join(countries_dir, f))

# Scan services directory
services_dir = os.path.join(root_dir, "services")
if os.path.exists(services_dir):
    for f in os.listdir(services_dir):
        if f.endswith(".html"):
            html_files.append(os.path.join(services_dir, f))

target_files = html_files + [
    os.path.join(root_dir, "js", "blogs-detail.js"),
    os.path.join(root_dir, "scratch", "create_seo_pages.py")
]

# Replacements list: (pattern, replacement, description, run_on_all)
# If run_on_all is True, we run it on all targets. If False, we only run it on index.html and js/blogs-detail.js (for casing fixes).
replacements = [
    # 1. Spacing and Typos (Missing Spaces)
    (r'\b(Expert|Emergency|24X7|Global)(<small\b)', r'\1 \2', "Insert space before <small> in cards", True),
    (r'\b(expert|emergency|24x7|global)(<small\b)', r'\1 \2', "Insert space before <small> in cards (lowercase)", True),
    
    # 2. Grammatical and Phrasing Corrections
    (r'We provide globally air ambulance services and medical evacuation worldwide\.', 
     'We provide global air ambulance services and medical evacuation worldwide.', 
     "We provide globally air ambulance... -> global air ambulance", True),
     
    (r'Air Transfers Worldwide\s+,\s+Air Medical 24X7', 
     'Air Transfers Worldwide, Air Medical 24X7', 
     "Air Transfers Worldwide , -> Worldwide,", True),
     
    (r'Our team are available', 
     'Our team is available', 
     "Our team are available -> is available", True),
     
    (r'quick facility with the greatest service', 
     'rapid medical deployment and the highest quality care', 
     "quick facility with the greatest service -> rapid medical deployment...", True),
     
    # 3. Terminology and Currency Adjustments
    (r'at a price you can afford which is 1\.6 lacs to 2\.5 lacs per hour', 
     'at competitive hourly rates. Contact us for a customized, transparent quotation based on your routing.', 
     "1.6 lacs to 2.5 lacs per hour pricing -> competitive hourly rates...", True),
     
    (r'\b1\.6\s+lacs\b', 'competitive hourly rates', "Replace 1.6 lacs with competitive rates", True),
    (r'\b2\.5\s+lacs\b', 'competitive hourly rates', "Replace 2.5 lacs with competitive rates", True),
    (r'\blacs per hour\b', 'competitive hourly rates', "Replace lacs per hour with competitive rates", True)
]

casing_replacements = [
    # 4. Brand Inconsistencies (24/7 or 24x7 -> 24X7)
    # Using negative lookbehind and lookahead to avoid touching domain names, emails, and paths
    (r'(?<!airmedical)(?<!airmedical-)(?<!airmedical_)(?<!\d)(24/7|24[xX]7|24×7)(?!\d)(?!\.com)(?![-_]?24[xX]7)', 
     '24X7', 
     "Standardize 24/7, 24x7, 24×7 -> 24X7", False)
]

print("=== Running Local Codebase Corrections ===")
changed_files_count = 0

for file_path in target_files:
    if not os.path.exists(file_path):
        continue
    
    rel_path = os.path.relpath(file_path, root_dir)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"Error reading {rel_path}: {e}")
        continue
        
    content = original_content
    file_changes = []
    
    # Run general replacements
    for pattern, rep, desc, run_on_all in replacements:
        new_content, count = re.subn(pattern, rep, content, flags=re.IGNORECASE if "lacs" in desc or "team" in desc or "facility" in desc else 0)
        if count > 0:
            content = new_content
            file_changes.append(f"  - {desc} (Count: {count})")
            
    # Run casing replacements on specific files (index.html, blogs-detail.js)
    # We explicitly exclude js/config.js and create_seo_pages.py from general casing replacements to prevent breaking code/regexes.
    is_casing_target = ("index.html" in rel_path or "blogs-detail.js" in rel_path)
    if is_casing_target:
        for pattern, rep, desc, run_on_all in casing_replacements:
            new_content, count = re.subn(pattern, rep, content)
            # Filter out no-op changes (like replacing 24X7 with 24X7)
            if count > 0:
                content = new_content
                file_changes.append(f"  - {desc} (Count: {count})")
                
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {rel_path}:")
            for change in file_changes:
                print(change)
            changed_files_count += 1
        except Exception as e:
            print(f"Error writing {rel_path}: {e}")

print(f"\nDone. Updated {changed_files_count} files in total.")
