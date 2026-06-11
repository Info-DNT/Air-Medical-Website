import os
import re

target_text = "GET THE QUOTATION IN 30 MINS"
replacement_text = "GET A QUOTATION IN 30 MINS"

print("Starting replacement of quote button text...")
count = 0

# Walk through all directories and subdirectories
for root, dirs, files in os.walk("."):
    # Skip git and hidden files
    if ".git" in root or ".gemini" in root:
        continue
        
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Check if target text exists in file
                if target_text in content:
                    updated_content = content.replace(target_text, replacement_text)
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(updated_content)
                    print(f"Updated file: {path}")
                    count += 1
            except Exception as e:
                print(f"Error processing {path}: {e}")

print(f"Done. Updated {count} files.")
