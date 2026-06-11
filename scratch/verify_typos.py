import os
import re
import json
import urllib.request

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# 1. Verification of local files
html_files = []
for f in os.listdir(root_dir):
    if f.endswith(".html"):
        html_files.append(os.path.join(root_dir, f))
for d in ["countries", "services"]:
    d_path = os.path.join(root_dir, d)
    if os.path.exists(d_path):
        for f in os.listdir(d_path):
            if f.endswith(".html"):
                html_files.append(os.path.join(d_path, f))

js_files = [os.path.join(root_dir, "js", "blogs-detail.js")]
target_files = html_files + js_files + [os.path.join(root_dir, "scratch", "create_seo_pages.py")]

local_errors = []

# Pattern to check spacing
spacing_patterns = {
    "Expert<small": r'Expert<small',
    "Emergency<small": r'Emergency<small',
    "24X7<small": r'24X7<small',
    "Global<small": r'Global<small'
}

print("=== VERIFYING LOCAL CODEBASE ===")
for filepath in target_files:
    if not os.path.exists(filepath):
        continue
    
    rel_path = os.path.relpath(filepath, root_dir)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {rel_path}: {e}")
        continue

    # A. Check spacing typos
    for name, pattern in spacing_patterns.items():
        if re.search(pattern, content):
            local_errors.append(f"{rel_path}: Found spacing issue '{name}'")
            
    # B. Check grammatical and comma spacing typos
    if "globally air ambulance" in content.lower():
        local_errors.append(f"{rel_path}: Found 'globally air ambulance'")
    if "worldwide ," in content.lower():
        local_errors.append(f"{rel_path}: Found 'worldwide ,'")
    if "our team are available" in content.lower():
        local_errors.append(f"{rel_path}: Found 'our team are available'")
    if "quick facility with the greatest service" in content.lower():
        local_errors.append(f"{rel_path}: Found 'quick facility with the greatest service'")
    if "1.6 lacs" in content.lower() or "2.5 lacs" in content.lower() or "lacs per hour" in content.lower():
        local_errors.append(f"{rel_path}: Found 'lacs' pricing terms")

    # C. Check casing in index.html and js/blogs-detail.js
    if "index.html" in rel_path or "blogs-detail.js" in rel_path:
        # Standardize lookaround matching non-standard casings
        nonstandard_pattern = re.compile(r'(?<![\w\-@./])(24/7|24[xX]7|24×7)(?![\w\-@./])')
        matches = list(nonstandard_pattern.finditer(content))
        # Filter out 24X7 (correct)
        bad_matches = [m.group(1) for m in matches if m.group(1) != "24X7"]
        if bad_matches:
            local_errors.append(f"{rel_path}: Found non-standard casings: {bad_matches}")

if local_errors:
    print(f"[FAIL] Local codebase verification failed with {len(local_errors)} errors:")
    for err in local_errors:
        print(f"  - {err}")
else:
    print("[PASS] Local codebase is 100% clean!")


# 2. Verification of remote database
print("\n=== VERIFYING REMOTE SUPABASE DATABASE ===")
supabase_url = "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}"
}

db_errors = []

try:
    req = urllib.request.Request(f"{supabase_url}/blogs", headers=headers)
    with urllib.request.urlopen(req) as response:
        blogs = json.loads(response.read().decode('utf-8'))
        
    for b in blogs:
        slug = b.get("slug")
        # Check columns
        for col in ["title", "excerpt", "content", "author", "meta_title", "meta_description"]:
            val = b.get(col)
            if not val:
                continue
            
            # Check typo
            if "missiona whispered reassurance" in val.lower():
                db_errors.append(f"Blog '{slug}' ({col}): Found 'missiona whispered reassurance'")
            
            # Check casing
            nonstandard_pattern = re.compile(r'(?<![\w\-@./])(24/7|24[xX]7|24×7)(?![\w\-@./])')
            matches = list(nonstandard_pattern.finditer(val))
            bad_matches = [m.group(1) for m in matches if m.group(1) != "24X7"]
            if bad_matches:
                db_errors.append(f"Blog '{slug}' ({col}): Found non-standard casings {bad_matches}")
                
            # Check phasing & pricing
            if "globally air ambulance" in val.lower():
                db_errors.append(f"Blog '{slug}' ({col}): Found 'globally air ambulance'")
            if "our team are available" in val.lower():
                db_errors.append(f"Blog '{slug}' ({col}): Found 'our team are available'")
            if "quick facility with the greatest service" in val.lower():
                db_errors.append(f"Blog '{slug}' ({col}): Found 'quick facility with the greatest service'")
            if "1.6 lacs" in val.lower() or "2.5 lacs" in val.lower():
                db_errors.append(f"Blog '{slug}' ({col}): Found 'lacs' pricing terms")

    if db_errors:
        print(f"[FAIL] Remote database verification failed with {len(db_errors)} errors:")
        for err in db_errors:
            print(f"  - {err}")
    else:
        print("[PASS] Remote database is 100% clean!")
except Exception as e:
    print(f"Error querying database for verification: {e}")
