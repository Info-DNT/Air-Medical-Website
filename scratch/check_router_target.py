import os

workspace_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []
for root, dirs, files in os.walk(workspace_dir):
    if ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

target_content = """      if (cleanPath === '') {
        cleanPath = '/';
      }
      if (cleanPath !== pathname) {
        window.history.replaceState(null, '', cleanPath + window.location.search + window.location.hash);
      }"""

found_count = 0
not_found_files = []

for file_path in html_files:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if target_content in content:
        found_count += 1
    else:
        not_found_files.append(os.path.relpath(file_path, workspace_dir))

print(f"Target found in {found_count} of {len(html_files)} files.")
if not_found_files:
    print("Not found in:")
    for f in not_found_files:
        print(f" - {f}")
