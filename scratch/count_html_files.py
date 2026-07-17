import os

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []

for dirpath, _, filenames in os.walk(root_dir):
    if any(p in dirpath for p in [".git", ".vscode", "node_modules", ".gemini"]):
        continue
    for filename in filenames:
        if filename.endswith(".html"):
            html_files.append(os.path.join(dirpath, filename))

print(f"Total HTML files: {len(html_files)}")
