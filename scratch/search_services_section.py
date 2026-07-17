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
                    content = f.read()
            except:
                continue
            if "Ground Ambulance" in content or "Domestic transfer" in content:
                rel = os.path.relpath(filepath, root_dir)
                print(f"Found in: {rel}")
