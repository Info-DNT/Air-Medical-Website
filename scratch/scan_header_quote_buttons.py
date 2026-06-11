import os

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

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
            
            for idx, line in enumerate(lines):
                if "btn-header-quote" in line:
                    rel = os.path.relpath(filepath, root_dir)
                    print(f"{rel}:{idx+1}: {line.strip()}")
