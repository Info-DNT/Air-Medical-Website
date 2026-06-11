import os
import re

workspace_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []
for root, dirs, files in os.walk(workspace_dir):
    if ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

print(f"Discovered {len(html_files)} HTML files to update.\n")

updated_count = 0

for file_path in html_files:
    rel_path = os.path.relpath(file_path, workspace_dir)
    if rel_path == "404.html":
        continue
        
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    original_content = content
    
    # 1. If it's career.html, fix the comments first
    if rel_path == "career.html":
        # Fix double Footer Start
        content = re.sub(r'<!--\s*Footer\s*Start\s*-->\s*<!--\s*Footer\s*Start\s*-->', '<!-- Footer Start -->', content)
        
        # Fix missing Footer End (insert it after the closing tag of footer bottom)
        # Find Footer Bottom and its closing div
        footer_bottom_pattern = r'(<!--\s*Footer\s*Bottom\s*-->[\s\S]*?<!--\s*Payment\s*Methods\s*-->[\s\S]*?</div>\s*</div>\s*</div>)'
        if re.search(footer_bottom_pattern, content):
            content = re.sub(footer_bottom_pattern, r'\1\n\n    <!-- Footer End -->', content)
            print("Fixed footer comments in career.html")
            
    # 2. Update Career link in Quick Links
    # We find Quick Links and replace href="#!" with href="career" inside it
    quick_links_pattern = r'(Quick\s+Links</h4>[\s\S]*?</div>)'
    
    def replace_career(match):
        block = match.group(1)
        # Replace href="#!" with href="career" where text is Career
        # This matches <a ... href="#!" ...> ... Career </a>
        # We can use a pattern that catches href="#!" specifically in the anchor containing Career
        sub_pattern = r'href=["\']#!["\']([^>]*?>[\s\S]*?Career\s*</a>)'
        new_block = re.sub(sub_pattern, r'href="career"\1', block)
        return new_block

    if re.search(quick_links_pattern, content, re.IGNORECASE):
        content = re.sub(quick_links_pattern, replace_career, content, flags=re.IGNORECASE)
        
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1
        print(f"Updated footer in {rel_path}")

print(f"\nSuccessfully updated {updated_count} files.")
