import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

btn_re = re.compile(r'class="[^"]*btn-header-quote[^"]*"[^>]*>(.*?)</a>|class=\'[^\']*btn-header-quote[^\']*\'[^>]*>(.*?)</a>', re.IGNORECASE)

incorrect_count = 0

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
            
            # Find all a tags with class btn-header-quote
            # Let's search for <a and grab everything until </a>
            a_tags = re.findall(r'<a\s+[^>]*btn-header-quote[^>]*>.*?</a>', content, re.DOTALL | re.IGNORECASE)
            
            for a_tag in a_tags:
                # Extract inner text
                inner_text = re.sub(r'<[^>]*>', '', a_tag).strip()
                # Check if it contains "GET THE QUOTATION IN 30 MINS" or "GET THE QUOTATION IN 30 MINS"
                if inner_text not in ["GET THE QUOTATION IN 30 MINS", "GET THE QUOTATION IN 30 MINS"]:
                    rel = os.path.relpath(filepath, root_dir)
                    print(f"Incorrect button text in {rel}:")
                    print(f"  Tag: {a_tag.strip()}")
                    print(f"  Inner text: {inner_text!r}")
                    incorrect_count += 1

print(f"Total incorrect: {incorrect_count}")
