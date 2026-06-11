import os
import subprocess

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

# Get list of files in the commit
cmd = 'git diff-tree --no-commit-id --name-only -r 15fb4c2e414f106b438741c03686db38200a6fdf'
output = subprocess.check_output(cmd, shell=True, cwd=root_dir).decode("utf-8")
commit_files = set(line.strip() for line in output.splitlines())

for dirpath, _, filenames in os.walk(root_dir):
    if any(p in dirpath for p in [".git", ".vscode", "node_modules", ".gemini"]):
        continue
    for filename in filenames:
        if filename.endswith(".html"):
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)
            # Git uses forward slashes
            git_path = rel_path.replace("\\", "/")
            if git_path not in commit_files:
                # Read file and check if it has the button class at all
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                has_btn = "btn-header-quote" in content
                print(f"Unchanged HTML file: {rel_path} (has btn-header-quote: {has_btn})")
