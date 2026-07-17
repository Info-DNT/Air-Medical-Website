import os
import re

def verify_changes():
    root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        if 'node_modules' in root or '.git' in root or 'scratch' in root or '.vscode' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    failed = False
    
    # 1. Verify that "Airline Stretcher Services Worldwide" is completely gone
    print("Checking for leftover 'Airline Stretcher Services Worldwide'...")
    leftover_count = 0
    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        matches = re.findall(r'Airline Stretcher Services Worldwide', content)
        if matches:
            print(f"  [ERROR] Found {len(matches)} occurrences in {os.path.relpath(filepath, root_dir)}")
            leftover_count += len(matches)
            failed = True
            
    if leftover_count == 0:
        print("  [SUCCESS] No occurrences of 'Airline Stretcher Services Worldwide' found!")
    else:
        print(f"  [FAIL] Found a total of {leftover_count} occurrences of 'Airline Stretcher Services Worldwide'.")
        
    print("-" * 50)
    
    # 2. Verify target page headings
    print("Checking target page headings...")
    
    targets = {
        "services/doctor-appointment.html": {
            "title": "Global Doctor Appointments | Book Verified Specialists",
            "h1": "Book Global Doctor Appointments with Verified Specialists 24X7"
        },
        "services/custom-medical-packages.html": {
            "title": "Custom Medical Packages Abroad | Air Medical 24X7",
            "h1": "Affordable Custom Medical Packages Abroad | Global Treatment Plans"
        },
        "services/medical-tourism-services.html": {
            "title": "Global Medical Tourism Services | Air Medical 24X7",
            "h1": "Global Medical Tourism Services | Air Medical 24X7"
        },
        "services/commercial-flight-stretcher.html": {
            "title": "Airline Stretcher Services | Air Medical 24X7",
            "h1": "Airline Stretcher Services"
        },
        "commercial-stretcher-service.html": {
            "title": "Airline Stretcher Services | Air Medical 24X7",
            "h1": "Airline Stretcher Services"
        },
        "ecmo-air-transfer.html": {
            "title": "ECMO Air Transport | Critical Care Life-Support Flight",
            "h1": "ECMO Air Transfer Services"
        }
    }
    
    for rel_path, expected in targets.items():
        filepath = os.path.join(root_dir, rel_path)
        if not os.path.exists(filepath):
            print(f"  [ERROR] File does not exist: {rel_path}")
            failed = True
            continue
            
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Check Title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        actual_title = title_match.group(1).strip() if title_match else "N/A"
        
        # Check H1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        actual_h1 = h1_match.group(1).strip() if h1_match else "N/A"
        actual_h1 = re.sub(r'<[^>]+>', '', actual_h1)
        actual_h1 = " ".join(actual_h1.split())
        
        # We compare expected H1 and Title
        if actual_title != expected["title"]:
            print(f"  [ERROR] {rel_path} title mismatch:")
            print(f"    Expected: {expected['title']}")
            print(f"    Actual:   {actual_title}")
            failed = True
        else:
            print(f"  [SUCCESS] {rel_path} title matches.")
            
        if actual_h1 != expected["h1"]:
            print(f"  [ERROR] {rel_path} H1 mismatch:")
            print(f"    Expected: {expected['h1']}")
            print(f"    Actual:   {actual_h1}")
            failed = True
        else:
            print(f"  [SUCCESS] {rel_path} H1 matches.")
            
    print("-" * 50)
    if not failed:
        print("[VERIFICATION PASSED] All checks completed successfully!")
    else:
        print("[VERIFICATION FAILED] One or more checks failed.")
        
if __name__ == "__main__":
    verify_changes()
