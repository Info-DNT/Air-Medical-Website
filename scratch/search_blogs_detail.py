import glob
import json
import re

blog_files = glob.glob("scratch/blog_*.json")

patterns = {
    "ExpertMedical Escort/Expert Medical Escort": r"Expert\s*Medical\s*Escort",
    "EmergencyServices/Emergency Services": r"Emergency\s*Services",
    "24X7Support/24X7 Support": r"24[xX]7\s*Support|24/7\s*Support",
    "GlobalService/Global Service": r"Global\s*Service",
    "missiona whispered reassurance": r"mission\s*a\s*whispered\s*reassurance",
    "globally air ambulance": r"globally\s*air\s*ambulance",
    "quick facility/rapid medical deployment": r"quick\s+facility|rapid\s+medical\s+deployment",
    "Air Transfers Worldwide ,": r"Air\s+Transfers\s+Worldwide\s*,",
    "Our team are/is available": r"Our\s+team\s+(?:are|is)\s+available",
    "lacs/lakhs/price/hour": r"lac|lakh|price|hour|\b1\.6\b|\b2\.5\b"
}

for bf in blog_files:
    with open(bf, 'r', encoding='utf-8') as f:
        blog = json.load(f)
    
    slug = blog.get("slug")
    print(f"=== Blog: {slug} ===")
    
    for field in ["title", "excerpt", "content", "author"]:
        val = blog.get(field)
        if not val:
            continue
        for label, pat in patterns.items():
            matches = list(re.finditer(pat, val, re.IGNORECASE))
            if matches:
                print(f"  Field '{field}' matches '{label}':")
                for match in matches:
                    start = max(0, match.start() - 50)
                    end = min(len(val), match.end() + 50)
                    context = val[start:end].replace('\n', ' ')
                    print(f"    -> ...{context}...")
