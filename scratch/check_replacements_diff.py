import subprocess

# Run git diff for services/air-ambulance.html and look for 24X7 replacement lines
res = subprocess.run(["git", "diff", "services/air-ambulance.html"], capture_output=True, text=True, encoding='utf-8')

lines = res.stdout.split("\n")
for line in lines:
    if line.startswith("-") or line.startswith("+"):
        if "24/7" in line or "24x7" in line or "24X7" in line:
            print(line)
