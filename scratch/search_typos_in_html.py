import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html"))
)

output_file = "scratch/typo_search_results.txt"
patterns = {
    "ExpertMedical Escort": r"ExpertMedical\s*Escort",
    "ExpertMedical": r"ExpertMedical",
    "EmergencyServices": r"EmergencyServices",
    "24X7Support": r"24X7Support",
    "GlobalService": r"GlobalService",
    "missiona whispered reassurance": r"missiona\s+whispered\s+reassurance",
    "globally air ambulance": r"globally\s+air\s+ambulance",
    "quick facility with the greatest service": r"quick\s+facility\s+with\s+the\s+greatest\s+service",
    "Air Transfers Worldwide ,": r"Air\s+Transfers\s+Worldwide\s+,",
    "Our team are available": r"Our\s+team\s+are\s+available",
    "lacs": r"lacs",
    "lakhs": r"lakhs"
}

with open(output_file, 'w', encoding='utf-8') as out:
    out.write(f"Checking {len(html_files)} HTML files:\n")
    for hf in html_files:
        rel_path = os.path.relpath(hf, root_dir)
        try:
            with open(hf, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            out.write(f"Error reading {rel_path}: {e}\n")
            continue
            
        for name, pat in patterns.items():
            if re.search(pat, content, re.IGNORECASE):
                out.write(f"[{rel_path}] Found '{name}':\n")
                matches = re.finditer(pat, content, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(content), match.end() + 50)
                    context = content[start:end].replace('\n', ' ')
                    out.write(f"  -> Context: ...{context}...\n")
                    
print("Done writing search results.")
