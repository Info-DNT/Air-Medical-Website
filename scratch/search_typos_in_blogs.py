import glob
import json
import re

blog_files = glob.glob("scratch/blog_*.json")
print(f"Checking {len(blog_files)} blog files:")

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

for bf in blog_files:
    with open(bf, 'r', encoding='utf-8') as f:
        blog = json.load(f)
    
    # check everything (title, excerpt, content, author)
    for field in ["title", "excerpt", "content", "author"]:
        val = blog.get(field)
        if not val:
            continue
        for name, pat in patterns.items():
            if re.search(pat, val, re.IGNORECASE):
                print(f"[{bf}] Found '{name}' in field '{field}':")
                # print context
                matches = re.finditer(pat, val, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(val), match.end() + 50)
                    context = val[start:end].replace('\n', ' ')
                    print(f"  -> Context: ...{context}...")
