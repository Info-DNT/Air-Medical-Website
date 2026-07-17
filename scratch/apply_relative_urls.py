import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html"))
)

print(f"Found {len(html_files)} HTML files to process.")

def get_relative_prefix(filepath):
    # Determine the directory relative to root_dir
    rel_dir = os.path.dirname(os.path.relpath(filepath, root_dir))
    if rel_dir == "" or rel_dir == ".":
        return ""
    else:
        # e.g., services -> ../, countries -> ../
        depth = len(rel_dir.split(os.sep))
        return "../" * depth

def make_relative(url_str, rel_prefix):
    # If it is external, mailto, phone, sms, js, or starts with hash, return unmodified
    if (url_str.startswith('mailto:') or url_str.startswith('tel:') or 
        url_str.startswith('sms:') or url_str.startswith('#') or 
        url_str.startswith('javascript:') or 
        url_str.startswith('http://') or url_str.startswith('https://') or 
        url_str.startswith('//')):
        return url_str

    # Special case: root link "/" or "/index.html"
    if url_str == "/" or url_str == "/index.html":
        return rel_prefix + "index.html" if rel_prefix else "index.html"

    # If it starts with a single "/", make it relative
    if url_str.startswith('/'):
        clean_url = url_str.lstrip('/')
        return rel_prefix + clean_url
        
    return url_str

# We want to match:
# 1. href="... " or href='...'
# 2. src="..." or src='...'
# 3. action="..." or action='...'
# We should NOT match canonical links (<link rel="canonical" href="...">) because they must remain absolute!
# We should NOT match schema JSON strings.

pattern = re.compile(r'\b(href|src|action)=(["\'])(.*?)\2', re.IGNORECASE)

updated_count = 0

for filepath in html_files:
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    
    # Skip admin dashboard and 404 handler (we will update 404.html separately)
    if rel_path == "admin.html" or rel_path == "404.html":
        continue

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content
    rel_prefix = get_relative_prefix(filepath)

    def repl(match):
        attr = match.group(1)
        quote = match.group(2)
        val = match.group(3)
        
        # Check if this is a canonical tag match (by scanning context slightly before the match)
        # We can look up the starting index of the match in the content to check if it's within a <link rel="canonical"> tag.
        match_start = match.start()
        # Find the tag start '<' before match_start
        tag_start = content.rfind('<', 0, match_start)
        if tag_start != -1:
            tag_content = content[tag_start:match_start].lower()
            if 'rel=' in tag_content and 'canonical' in tag_content:
                # Keep canonical absolute URLs unmodified
                return match.group(0)

        new_val = make_relative(val, rel_prefix)
        return f'{attr}={quote}{new_val}{quote}'

    new_content = pattern.sub(repl, content)

    if new_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1
        print(f"Updated: {rel_path} with prefix '{rel_prefix}'")
    else:
        print(f"No changes in: {rel_path}")

print(f"Completed! Updated {updated_count} HTML files.")
