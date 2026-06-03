import os
import glob
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# Get all HTML files in root, services, and countries
html_files = (
    glob.glob(os.path.join(root_dir, "*.html")) +
    glob.glob(os.path.join(root_dir, "countries", "*.html")) +
    glob.glob(os.path.join(root_dir, "services", "*.html"))
)

print(f"Found {len(html_files)} HTML files to process.")

def process_file(filepath):
    rel_path = os.path.relpath(filepath, root_dir)
    # Skip temporary diff files and 404
    if "diff" in rel_path.lower() or rel_path == "404.html":
        return
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {rel_path}: {e}")
        return

    # 1. Check if the page has a local quote form
    has_local_form = 'id="quoteForm"' in content or "id='quoteForm'" in content
    
    # 2. Determine the quote URL (only for the header button)
    is_in_subdir = filepath.count(os.sep) > root_dir.count(os.sep)
    if has_local_form:
        quote_link = "#quoteForm"
    else:
        if is_in_subdir:
            quote_link = "../contact-us#quoteForm"
        else:
            quote_link = "contact-us#quoteForm"

    original_content = content

    # 3. Clean up any existing mobile header button
    content = re.sub(
        r'<!-- Mobile Quote Button.*?-->\s*<a[^>]*btn-header-quote[^>]*>.*?</a>[\s\x01]*', 
        '', 
        content, 
        flags=re.DOTALL
    )

    # 4. Insert the new mobile header button before the navbar-toggler with the text "Get the Quotation in 30 mins"
    # Using \\1 instead of \1 in python strings to avoid f-string parsing it as octal escape character \x01!
    toggler_pattern = r'(\s*)<button class="navbar-toggler"'
    header_button_html = (
        r'\1<!-- Mobile Quote Button (ONLY phone view) -->\1'
        f'<a href="{quote_link}" class="btn btn-request btn-header-quote ms-auto me-2">Get the Quotation in 30 mins</a>\\1'
        r'<button class="navbar-toggler"'
    )
    
    content, count_header = re.subn(toggler_pattern, header_button_html, content, count=1)

    # 5. Handle the bottom Mobile Sticky CTA
    # Remove existing mobile sticky CTA block first (including comments)
    cta_pattern = r'<!-- Mobile Sticky bottom CTA Bar -->.*?</div>\s*(?=</body>)'
    # Also handle cases where it's there without comment
    cta_pattern_no_comment = r'<div class="mobile-sticky-cta.*?</div>\s*(?=</body>)'
    
    content = re.sub(cta_pattern, '', content, flags=re.DOTALL)
    content = re.sub(cta_pattern_no_comment, '', content, flags=re.DOTALL)

    # Clean trailing whitespaces before body end to make insertion clean
    content = re.sub(r'\s*(?=</body>)', '\n\n', content)

    # Define new Mobile Sticky CTA HTML with Call, WhatsApp and iMessage (using sms:)
    new_cta_html = """  <!-- Mobile Sticky bottom CTA Bar -->
  <div class="mobile-sticky-cta d-lg-none">
    <div class="row g-2">
      <div class="col-4">
        <a href="tel:+971565542001" class="btn btn-call w-100 py-2.5 text-center">
          <i class="fas fa-phone-alt me-1"></i> Call
        </a>
      </div>
      <div class="col-4">
        <a href="https://wa.me/971565542001" target="_blank" class="btn btn-whatsapp w-100 py-2.5 text-center">
          <i class="fab fa-whatsapp me-1"></i> WhatsApp
        </a>
      </div>
      <div class="col-4">
        <a href="sms:+971565542001" class="btn btn-imessage w-100 py-2.5 text-center">
          <i class="fas fa-comment me-1"></i> iMessage
        </a>
      </div>
    </div>
  </div>\n\n"""

    # Insert new CTA right before </body>
    content = content.replace("</body>", f"{new_cta_html}</body>")

    # Only save if changed
    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {rel_path}")
        except Exception as e:
            print(f"Error writing {rel_path}: {e}")
    else:
        print(f"No changes for: {rel_path}")

for f in html_files:
    process_file(f)
