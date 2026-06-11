import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

patterns = [
    r"Quotation in \d+ min",
    r"Get a free Quotation",
    r"Get a Free Quotation",
    r"Get the Quotation",
    r"Get the free Quotation",
]

compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]

for dirpath, _, filenames in os.walk(root_dir):
    if any(p in dirpath for p in [".git", ".vscode", "node_modules", ".gemini"]):
        continue
    for filename in filenames:
        if filename.endswith(".html"):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            except Exception as e:
                continue
            
            for line_idx, line in enumerate(lines):
                for cp in compiled_patterns:
                    if cp.search(line):
                        rel_path = os.path.relpath(filepath, root_dir)
                        print(f"{rel_path}:{line_idx+1}: {line.strip()}")
