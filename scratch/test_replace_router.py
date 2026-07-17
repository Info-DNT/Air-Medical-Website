import os

workspace_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = []
for root, dirs, files in os.walk(workspace_dir):
    if ".git" in root or "scratch" in root:
        continue
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

target_block = """      var pathname = window.location.pathname;
      var cleanPath = pathname;
      if (cleanPath.endsWith('.html')) {
        cleanPath = cleanPath.slice(0, -5);
      }
      if (cleanPath.endsWith('/index')) {
        cleanPath = cleanPath.slice(0, -6);
      }
      var basePath = '';
      if (window.location.hostname.indexOf('.github.io') !== -1) {
        var segments = pathname.split('/');
        if (segments.length > 1 && segments[1]) {
          basePath = '/' + segments[1];
        }
      }
      var isDirRoot = (cleanPath === basePath || cleanPath === basePath + '/' || cleanPath === basePath + '/countries' || cleanPath === '/countries' || cleanPath === '/');
      if (isDirRoot) {
        if (!cleanPath.endsWith('/')) {
          cleanPath += '/';
        }
      } else {
        if (cleanPath.endsWith('/') && cleanPath !== '/') {
          cleanPath = cleanPath.slice(0, -1);
        }
      }
      if (cleanPath === '') {
        cleanPath = '/';
      }
      if (cleanPath !== pathname) {
        window.history.replaceState(null, '', cleanPath + window.location.search + window.location.hash);
      }"""

found_count = 0
not_found_files = []

for file_path in html_files:
    if "404.html" in file_path:
        continue
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if target_block in content:
        found_count += 1
    else:
        not_found_files.append(os.path.relpath(file_path, workspace_dir))

print(f"Target block found in {found_count} of {len(html_files) - 1} files.")
if not_found_files:
    print("Not found in:")
    for f in not_found_files:
        print(f" - {f}")
