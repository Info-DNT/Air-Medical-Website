import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# Regex pattern to match "Get a free Quotation in 30 min" with optional "s" and whitespace tolerance
button_pattern = re.compile(r'Get\s+a\s+free\s+Quotation\s+in\s+30\s+mins?', re.IGNORECASE)

def update_button_text(text):
    def replace_match(match):
        matched_str = match.group(0)
        # Check if the matched string is uppercase
        if matched_str.isupper():
            return "GET THE QUOTATION IN 30 MINS"
        else:
            return "GET THE QUOTATION IN 30 MINS"
    
    return button_pattern.sub(replace_match, text)

modified_files = []

# Walk through directories
for dirpath, _, filenames in os.walk(root_dir):
    # Skip standard internal dirs
    if ".git" in dirpath or ".vscode" in dirpath or "node_modules" in dirpath:
        continue
    
    for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        
        # Process HTML files
        if filename.endswith(".html"):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            new_content = content
            
            # 1. Update header button text
            if button_pattern.search(new_content):
                new_content = update_button_text(new_content)
            
            # 2. Update H1 on Airline Stretcher services page
            if filename == "airline-stretcher-services.html":
                old_h1 = '<h1 class="about-heading">Airline Stretcher Services Worldwide | Medical Escort Onboard</h1>'
                new_h1 = '<h1 class="about-heading">Airline Stretcher Services</h1>'
                if old_h1 in new_content:
                    new_content = new_content.replace(old_h1, new_h1)
                else:
                    # Try fallback with variations of whitespace
                    new_content = re.sub(
                        r'<h1 class="about-heading">\s*Airline Stretcher Services Worldwide \| Medical Escort Onboard\s*</h1>',
                        new_h1,
                        new_content
                    )
            
            # 3. Update H1 on Flight Medical Escort page
            if filename == "flight-medical-escort-services.html":
                old_h1 = '<h1 class="about-heading">Worldwide Flight Medical Escort Service In-Flight Patient Care</h1>'
                new_h1 = '<h1 class="about-heading">Flight Medical Escort</h1>'
                if old_h1 in new_content:
                    new_content = new_content.replace(old_h1, new_h1)
                else:
                    new_content = re.sub(
                        r'<h1 class="about-heading">\s*Worldwide Flight Medical Escort Service In-Flight Patient Care\s*</h1>',
                        new_h1,
                        new_content
                    )
            
            if new_content != content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)
                modified_files.append(filepath)
                print(f"Updated: {filepath}")

# Process specific scratch python scripts that might hardcode this text
scripts_to_update = [
    os.path.join(root_dir, "scratch", "apply_cta_updates.py"),
]

for filepath in scripts_to_update:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = content
        # Replace instances in python file
        new_content = button_pattern.sub("GET THE QUOTATION IN 30 MINS", new_content)
        
        if new_content != content:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            modified_files.append(filepath)
            print(f"Updated python script: {filepath}")

print(f"\nTotal files updated: {len(modified_files)}")
