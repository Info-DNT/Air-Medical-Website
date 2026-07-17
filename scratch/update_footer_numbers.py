import os
import re

pattern = re.compile(
    r'<p class="mb-0">\s*<i class="fa fa-phone-alt text-primary me-3"></i>\s*'
    r'<a href="tel:\+971565542001"[^>]*>\s*\+971 56 554 2001\s*</a>\s*</p>'
    r'\s*<p class="mb-0">\s*<i class="fa fa-phone-alt text-primary me-3"></i>\s*'
    r'<a href="tel:\+97143230261"[^>]*>\s*\+971 4 323 0261\s*</a>\s*</p>'
    r'\s*<p class="mb-0">\s*<i class="fa fa-phone-alt text-primary me-3"></i>\s*'
    r'<a href="tel:\+911171859928"[^>]*>\s*\+91 11 7185 9928\s*</a>\s*</p>'
    r'\s*<p class="mb-0">\s*<i class="fa fa-phone-alt text-primary me-3"></i>\s*'
    r'<a href="tel:\+919217710155"[^>]*>\s*\+91 92177 10155\s*</a>\s*</p>',
    re.DOTALL
)

replacement = """          <p class="mb-0">
            <i class="fa fa-phone-alt text-primary me-3"></i>
            <a href="tel:+971565542001" style="text-decoration: none; color: inherit;">
              +971 56 554 2001
            </a>
          </p>
          <p class="mb-1">
            <i class="fa fa-phone-alt text-primary me-2"></i>
            <small class="text-uppercase fw-bold text-muted" style="font-size: 0.75rem; letter-spacing: 0.5px;">India:</small> 
            <a href="tel:+918000504740" style="text-decoration: none; color: inherit;">+91 80005 04740</a>
          </p>
          <p class="mb-1">
            <i class="fa fa-phone-alt text-primary me-2"></i>
            <small class="text-uppercase fw-bold text-muted" style="font-size: 0.75rem; letter-spacing: 0.5px;">USA:</small> 
            <a href="tel:+18335186535" style="text-decoration: none; color: inherit;">+1 833-518-6535</a>
          </p>
          <p class="mb-1">
            <i class="fa fa-phone-alt text-primary me-2"></i>
            <small class="text-uppercase fw-bold text-muted" style="font-size: 0.75rem; letter-spacing: 0.5px;">UK:</small> 
            <a href="tel:+448002294751" style="text-decoration: none; color: inherit;">+44 800 229 4751</a>
          </p>
          <p class="mb-1">
            <i class="fa fa-phone-alt text-primary me-2"></i>
            <small class="text-uppercase fw-bold text-muted" style="font-size: 0.75rem; letter-spacing: 0.5px;">Canada:</small> 
            <a href="tel:+18337257598" style="text-decoration: none; color: inherit;">+1 833-725-7598</a>
          </p>
          <p class="mb-1">
            <i class="fa fa-phone-alt text-primary me-2"></i>
            <small class="text-uppercase fw-bold text-muted" style="font-size: 0.75rem; letter-spacing: 0.5px;">Vietnam:</small> 
            <a href="tel:+8412032123" style="text-decoration: none; color: inherit;">+84 1203 2123</a>
          </p>
          <p class="mb-0">
            <i class="fa fa-phone-alt text-primary me-2"></i>
            <small class="text-uppercase fw-bold text-muted" style="font-size: 0.75rem; letter-spacing: 0.5px;">Seychelles:</small> 
            <a href="tel:+2484632054" style="text-decoration: none; color: inherit;">+248 4 632 054</a>
          </p>"""

updated_count = 0

for root, dirs, files in os.walk('.'):
    if 'node_modules' in root or '.git' in root or '.gemini' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if pattern.search(content):
                new_content = pattern.sub(replacement, content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_count += 1

print(f"Success: Updated {updated_count} HTML files with the new footer numbers.")
