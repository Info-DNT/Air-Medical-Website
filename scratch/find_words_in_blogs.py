import glob
import json
import re

blog_files = glob.glob("scratch/blog_*.json")

search_words = ["1.6", "2.5", "lac", "lacs", "lakh", "lakhs", "hour", "escort", "globally", "reassurance", "available"]

for bf in blog_files:
    with open(bf, 'r', encoding='utf-8') as f:
        blog = json.load(f)
    
    # check everything (title, excerpt, content, author)
    for field in ["title", "excerpt", "content", "author"]:
        val = blog.get(field)
        if not val:
            continue
        for word in search_words:
            if word in val.lower():
                # print context
                matches = re.finditer(re.escape(word), val, re.IGNORECASE)
                for match in matches:
                    start = max(0, match.start() - 60)
                    end = min(len(val), match.end() + 60)
                    context = val[start:end].replace('\n', ' ')
                    print(f"[{bf}] Found '{word}' in '{field}':\n  -> Context: ...{context}...")
