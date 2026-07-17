import os
import re
import glob

ROOT = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

def rename_stretcher_in_forms():
    html_files = glob.glob(os.path.join(ROOT, "*.html")) + \
                 glob.glob(os.path.join(ROOT, "services", "*.html")) + \
                 glob.glob(os.path.join(ROOT, "countries", "*.html"))
                 
    print(f"Scanning {len(html_files)} HTML files for form renames...")
    
    # 1. Regex patterns for form radio card updates
    radio_value_pattern = re.compile(r'value="Commercial Flight Stretcher"', re.IGNORECASE)
    radio_span_pattern = re.compile(r'<span>Commercial Flight Stretcher</span>', re.IGNORECASE)
    radio_alt_pattern = re.compile(r'alt="Commercial Flight Stretcher"', re.IGNORECASE)
    
    # 2. Regex patterns for select dropdown options
    opt_pattern_1 = re.compile(r'<option[^>]*value="Commercial Flight Stretcher(?: Service)?"[^>]*>[\s\S]*?</option>', re.IGNORECASE)
    opt_pattern_2 = re.compile(r'<option[^>]*>Commercial Flight Stretcher(?: Service)?</option>', re.IGNORECASE)
    
    # 3. New pattern: Rename "Airline Stretcher Services" to "Airline Stretcher Services Worldwide"
    # Negative lookahead ensures we don't touch it if "Worldwide" is already present.
    airline_stretcher_pattern = re.compile(r'Airline Stretcher Services(?! Worldwide)', re.IGNORECASE)
    
    modified_count = 0
    
    for file_path in html_files:
        rel_path = os.path.relpath(file_path, ROOT)
        
        # Skip admin.html
        if "admin.html" in rel_path:
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        modified = False
        
        # Find the form id="quoteForm" or id="quoteFormPopup"
        form_pattern = re.compile(r'(<form[^>]*id="(?:quoteForm|quoteFormPopup)"[^>]*>)([\s\S]+?)(</form>)', re.IGNORECASE)
        
        def replace_form(match):
            nonlocal modified
            start, body, end = match.groups()
            body_mod = body
            
            # Apply radio button replacements
            if radio_value_pattern.search(body_mod):
                body_mod = radio_value_pattern.sub('value="Airline Stretcher Services Worldwide"', body_mod)
                modified = True
            if radio_span_pattern.search(body_mod):
                body_mod = radio_span_pattern.sub('<span>Airline Stretcher Services Worldwide</span>', body_mod)
                modified = True
            if radio_alt_pattern.search(body_mod):
                body_mod = radio_alt_pattern.sub('alt="Airline Stretcher Services Worldwide"', body_mod)
                modified = True
                
            # Apply select option replacements
            if opt_pattern_1.search(body_mod):
                body_mod = opt_pattern_1.sub('<option value="Airline Stretcher Services Worldwide">Airline Stretcher Services Worldwide</option>', body_mod)
                modified = True
            if opt_pattern_2.search(body_mod):
                body_mod = opt_pattern_2.sub('<option value="Airline Stretcher Services Worldwide">Airline Stretcher Services Worldwide</option>', body_mod)
                modified = True
                
            # Apply Airline Stretcher Services -> Airline Stretcher Services Worldwide rename
            if airline_stretcher_pattern.search(body_mod):
                body_mod = airline_stretcher_pattern.sub('Airline Stretcher Services Worldwide', body_mod)
                modified = True
                
            return start + body_mod + end
            
        new_content = form_pattern.sub(replace_form, content)
        
        if modified:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"  Updated form in: {rel_path}")
            modified_count += 1
            
    print(f"Successfully updated forms in {modified_count} files.")

if __name__ == "__main__":
    rename_stretcher_in_forms()
