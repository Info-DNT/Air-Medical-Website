import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html"))
)

print(f"Total HTML files found: {len(html_files)}")

results = []

for filepath in html_files:
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    if "diff" in rel_path.lower() or rel_path == "404.html" or rel_path == "admin.html":
        continue
        
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        results.append(f"Error reading {rel_path}: {e}")
        continue
        
    # Get Title
    title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
    title = title_match.group(1).strip() if title_match else "N/A"
    
    # Get H1 tags
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", content, re.IGNORECASE | re.DOTALL)
    h1_clean = [re.sub(r'<[^>]+>', '', h).strip() for h in h1s]
    
    # Get H2 tags (optional, first few)
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", content, re.IGNORECASE | re.DOTALL)
    h2_clean = [re.sub(r'<[^>]+>', '', h).strip() for h in h2s][:2]
    
    # Get Canonical URL
    canonical_match = re.search(r'<link rel="canonical"\s+href="(.*?)"', content, re.IGNORECASE)
    canonical = canonical_match.group(1).strip() if canonical_match else "N/A"
    
    # Get Meta Description
    desc_match = re.search(r'<meta[^>]*(?:name|content)="description"[^>]*(?:name|content)="(.*?)"', content, re.IGNORECASE)
    if not desc_match:
        desc_match = re.search(r'<meta[^>]*(?:name|content)="(.*?)"[^>]*(?:name|content)="description"', content, re.IGNORECASE)
    desc = desc_match.group(1).strip() if desc_match else "N/A"
    
    results.append({
        "file": rel_path,
        "title": title,
        "canonical": canonical,
        "h1s": h1_clean,
        "h2s": h2_clean,
        "desc": desc
    })

# Sort by file path
results.sort(key=lambda x: x["file"])

with open("scratch/inspect_all_html_meta.txt", "w", encoding="utf-8") as out:
    for res in results:
        if isinstance(res, str):
            out.write(res + "\n")
            continue
        out.write(f"File: {res['file']}\n")
        out.write(f"  Title: {res['title']} (len: {len(res['title'])})\n")
        out.write(f"  Canonical: {res['canonical']}\n")
        out.write(f"  H1s: {res['h1s']}\n")
        out.write(f"  H2s: {res['h2s']}\n")
        out.write(f"  Description: {res['desc']} (len: {len(res['desc'])})\n")
        out.write("-" * 50 + "\n")

print("Done inspecting HTML metadata. Saved to scratch/inspect_all_html_meta.txt")
