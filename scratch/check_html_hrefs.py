import re, glob, os

ROOT = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
files = (glob.glob(os.path.join(ROOT, "services", "*.html")) + 
         glob.glob(os.path.join(ROOT, "countries", "*.html")) +
         glob.glob(os.path.join(ROOT, "*.html")))

total_issues = 0
for f in files:
    rel = os.path.relpath(f, ROOT).replace("\\", "/")
    if rel in ["404.html", "admin.html"]:
        continue
    with open(f, encoding="utf-8", errors="ignore") as fh:
        content = fh.read()
    hrefs = re.findall(r'href="([^"]*\.html[^"]*)"', content)
    # filter out assets
    nav_issues = [h for h in hrefs if not any(h.lower().endswith(e) for e in (".css",".js",".png",".jpg",".ico",".gif"))]
    if nav_issues:
        total_issues += len(nav_issues)
        print(f"In {rel}:")
        for h in nav_issues[:5]:
            print(f"  WARN: href=\"{h}\"")
        print()

if total_issues == 0:
    print("ALL CLEAN - no .html in href links found!")
else:
    print(f"Total issues: {total_issues}")
