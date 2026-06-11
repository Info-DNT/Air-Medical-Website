import os

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
htaccess_path = os.path.join(root_dir, ".htaccess")

with open(htaccess_path, "r", encoding="utf-8") as f:
    content = f.read()

redirect_rule = """# Redirect legacy airline-stretcher-services to commercial-flight-stretcher
RewriteCond %{ENV:REDIRECT_STATUS} ^$
RewriteRule ^airline-stretcher-services(?:\\.html)?$ /commercial-flight-stretcher [R=301,L,NC]
"""

# Insert right after RewriteEngine On or before other redirects
if "airline-stretcher-services" not in content:
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        if "RewriteBase /" in line:
            lines.insert(idx + 1, "\n" + redirect_rule)
            break
    content = "\n".join(lines)
    with open(htaccess_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(".htaccess updated successfully.")
else:
    print(".htaccess already has redirect rule.")
