import os
import re

def find_mismatches():
    root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
    html_files = []
    
    for root, dirs, files in os.walk(root_dir):
        if 'node_modules' in root or '.git' in root or 'scratch' in root or '.vscode' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    mismatches = []
    for filepath in sorted(html_files):
        rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Get title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "N/A"
        
        # Get h1
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        h1_str = h1_match.group(1).strip() if h1_match else "N/A"
        h1_str = re.sub(r'<[^>]+>', '', h1_str)
        h1_str = " ".join(h1_str.split())
        
        basename = os.path.splitext(os.path.basename(filepath))[0]
        if basename == 'index':
            continue
            
        # Clean words from basename
        base_words = set(re.findall(r'[a-zA-Z0-9]+', basename.lower()))
        # Remove common short words/stop words
        stop_words = {'services', 'service', 'air', 'ambulance', 'transfer', 'packages', 'in', 'to', 'for', 'with', 'dubai', 'india'}
        base_words = base_words - stop_words
        
        h1_words = set(re.findall(r'[a-zA-Z0-9]+', h1_str.lower()))
        
        # Check if base_words is not empty and has low overlap with h1_words
        overlap = base_words.intersection(h1_words)
        
        # Check if we should flag it
        is_mismatch = False
        reason = ""
        
        # Specific manual checks for services files
        if 'services/' in rel_path:
            if basename == 'doctor-appointment' and 'second opinion' in h1_str.lower():
                is_mismatch = True
                reason = "H1 mentions 'Second Opinion' instead of 'Doctor Appointment'."
            elif basename == 'custom-medical-packages' and 'custom' not in h1_str.lower():
                is_mismatch = True
                reason = "H1 lacks the word 'Custom'."
            elif basename == 'medical-tourism-services' and 'services' in h1_str.lower() and 'tourism' in h1_str.lower() and 'air transport' in h1_str.lower():
                is_mismatch = True
                reason = "H1 has 'Medical Tourism Air Transport' instead of 'Global Medical Tourism Services'."
            elif basename == 'commercial-flight-stretcher':
                is_mismatch = True
                reason = "Should be renamed to 'Airline Stretcher Services'."
        elif rel_path == 'commercial-stretcher-service.html':
            is_mismatch = True
            reason = "Should be renamed to 'Airline Stretcher Services'."
            
        if is_mismatch:
            mismatches.append({
                'file': rel_path,
                'title': title,
                'h1': h1_str,
                'reason': reason
            })
            
    print(f"Found {len(mismatches)} mismatches:")
    for m in mismatches:
        print(f"File: {m['file']}")
        print(f"  H1: {m['h1']}")
        print(f"  Reason: {m['reason']}")
        print("-" * 50)

if __name__ == "__main__":
    find_mismatches()
