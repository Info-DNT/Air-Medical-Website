import os
import re

def fix_html_files():
    root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
    
    pattern_double = re.compile(r'onload\s*=\s*"\s*this\.media\s*=\s*\\*\'all\\*\'\s*"', re.IGNORECASE)
    pattern_single = re.compile(r'onload\s*=\s*\'\s*this\.media\s*=\s*\\*\'all\\*\'\s*\'', re.IGNORECASE)
    
    html_count = 0
    onload_fix_count = 0
    
    for root, dirs, files in os.walk(root_dir):
        if any(p in root for p in ['node_modules', '.git', 'scratch', '.vscode']):
            continue
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                modified = False
                new_content = content
                
                # Perform regex replacement
                new_content, count = pattern_double.subn('onload="this.media=\'all\'"', new_content)
                new_content, count_sq = pattern_single.subn('onload="this.media=\'all\'"', new_content)
                
                total_fixes = count + count_sq
                if total_fixes > 0:
                    modified = True
                    onload_fix_count += total_fixes
                
                # Now, if it's blogs.html, add defer to js/blogs.js
                if file == 'blogs.html':
                    if 'src="js/blogs.js"' in new_content and 'src="js/blogs.js" defer' not in new_content:
                        new_content = new_content.replace('src="js/blogs.js"', 'src="js/blogs.js" defer')
                        modified = True
                        print("Deferred blogs.js in blogs.html")

                # Now, if it's blogs-detail.html, add defer to js/blogs-detail.js
                if file == 'blogs-detail.html':
                    if 'src="js/blogs-detail.js"' in new_content and 'src="js/blogs-detail.js" defer' not in new_content:
                        new_content = new_content.replace('src="js/blogs-detail.js"', 'src="js/blogs-detail.js" defer')
                        modified = True
                        print("Deferred blogs-detail.js in blogs-detail.html")

                if modified:
                    html_count += 1
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {os.path.relpath(path, root_dir)}")
                    
    print(f"\nTotal HTML files updated: {html_count}")
    print(f"Total onload fixes: {onload_fix_count}")

if __name__ == '__main__':
    fix_html_files()
