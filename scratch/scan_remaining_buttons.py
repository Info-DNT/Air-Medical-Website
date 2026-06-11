import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

patterns = [
    r"Get a free Quotation in 30 min",
    r"GET A FREE QUOTATION IN 30 MINS",
    r"Get a free Quotation",
    r"free Quotation",
    r"Quotation in 30 min",
]

compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

found = False

for dirpath, _, filenames in os.walk(root_dir):
    if any(p in dirpath for p in [".git", ".vscode", "node_modules", ".gemini"]):
        continue
    for filename in filenames:
        if filename.endswith(".html") or filename.endswith(".js") or filename.endswith(".py"):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                continue
            
            for p in compiled_patterns:
                matches = p.findall(content)
                if matches:
                    print(f"Match found in: {filepath}")
                    print(f"  Pattern: {p.pattern}")
                    print(f"  Sample: {matches[:3]}")
                    found = True

if not found:
    print("No matching patterns found!")
