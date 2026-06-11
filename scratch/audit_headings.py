import os
import re

def audit_headings():
    root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
    html_files = []
    
    # Traverse directories to find HTML files
    for root, dirs, files in os.walk(root_dir):
        # Exclude node_modules, .git, scratch
        if 'node_modules' in root or '.git' in root or 'scratch' in root or '.vscode' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    out_lines = []
    for filepath in sorted(html_files):
        rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # Get title
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "N/A"
        
        # Get h1 headings (taking the first one)
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        h1_str = h1_match.group(1).strip() if h1_match else "N/A"
        h1_str = re.sub(r'<[^>]+>', '', h1_str)
        h1_str = " ".join(h1_str.split())
        
        # Find occurrences of Airline Stretcher / Commercial Flight Stretcher
        worldwide_matches = re.findall(r'Airline Stretcher Services Worldwide', content)
        stretcher_matches = re.findall(r'Commercial Flight Stretcher', content)
        
        out_lines.append(f"File: {rel_path}")
        out_lines.append(f"  Title: {title}")
        out_lines.append(f"  H1: {h1_str}")
        if worldwide_matches:
            out_lines.append(f"  [FOUND] 'Airline Stretcher Services Worldwide' count: {len(worldwide_matches)}")
        if stretcher_matches:
            out_lines.append(f"  [FOUND] 'Commercial Flight Stretcher' count: {len(stretcher_matches)}")
        out_lines.append("-" * 50)

    # Write output to scratch file
    dest_file = os.path.join(root_dir, "scratch", "headings_audit_full.txt")
    with open(dest_file, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print(f"Audit results written to {dest_file}")

if __name__ == "__main__":
    audit_headings()
