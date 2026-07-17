import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html"))
)

print(f"Total HTML files to process: {len(html_files)}")

# Pattern to match the history cleaning script
pattern = re.compile(
    r'\s*<script>\s*\(function\s*\(\)\s*\{\s*var\s*pathname\s*=\s*window\.location\.pathname;[\s\S]*?window\.history\.replaceState[\s\S]*?\}\)\(\);\s*</script>',
    re.IGNORECASE
)

removed_count = 0

for filepath in html_files:
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    if "diff" in rel_path.lower() or rel_path == "404.html" or rel_path == "admin.html":
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    
    # Remove the history cleaner script block
    new_content, count = pattern.subn('', content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        removed_count += 1
        print(f"Removed history script from: {rel_path}")
    else:
        print(f"No history script found in: {rel_path}")

print(f"Completed! Removed from {removed_count} files.")
