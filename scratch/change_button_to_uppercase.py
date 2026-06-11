import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

modified_files = []

for dirpath, _, filenames in os.walk(root_dir):
    if any(p in dirpath for p in [".git", ".vscode", "node_modules", ".gemini"]):
        continue
    for filename in filenames:
        if filename.endswith(".html") or filename.endswith(".py"):
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                continue
            
            new_content = content
            
            # Replace case-insensitive variations of "GET THE QUOTATION IN 30 MINS" in html / py
            new_content = re.sub(
                r'Get\s+the\s+Quotation\s+in\s+30\s+mins?',
                "GET THE QUOTATION IN 30 MINS",
                new_content,
                flags=re.IGNORECASE
            )
            
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                rel = os.path.relpath(filepath, root_dir)
                modified_files.append(rel)
                print(f"Updated to uppercase: {rel}")

print(f"\nTotal files updated: {len(modified_files)}")
