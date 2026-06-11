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

new_block = """      var pathname = window.location.pathname;
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
      var countriesPrefix = basePath + '/countries/';
      var servicesPrefix = basePath + '/services/';
      if (cleanPath.startsWith(countriesPrefix) && cleanPath.length > countriesPrefix.length) {
        cleanPath = basePath + '/' + cleanPath.substring(countriesPrefix.length);
      } else if (cleanPath.startsWith(servicesPrefix) && cleanPath.length > servicesPrefix.length) {
        cleanPath = basePath + '/' + cleanPath.substring(servicesPrefix.length);
      }
      if (cleanPath === basePath + '/countries/index' || cleanPath === basePath + '/countries') {
        cleanPath = basePath + '/country';
      }
      var isDirRoot = (cleanPath === basePath || cleanPath === basePath + '/' || cleanPath === basePath + '/countries/' || cleanPath === '/');
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
        window.history.writeState || window.history.replaceState(null, '', cleanPath + window.location.search + window.location.hash);
      }"""

# Wait, let's keep the standard replaceState line as:
# window.history.replaceState(null, '', cleanPath + window.location.search + window.location.hash);
# to be safe and consistent.
new_block = new_block.replace("window.history.writeState || window.history.replaceState", "window.history.replaceState")

count = 0
for file_path in html_files:
    if "404.html" in file_path:
        continue
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    if target_block in content:
        new_content = content.replace(target_block, new_block)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1
        print(f"Updated router in {os.path.relpath(file_path, workspace_dir)}")
    else:
        print(f"WARNING: Target block not found in {os.path.relpath(file_path, workspace_dir)}")

print(f"Total files updated: {count}")
