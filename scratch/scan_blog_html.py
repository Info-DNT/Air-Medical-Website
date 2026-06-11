import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main\blog.html"

pattern = re.compile(r"24/7|24[xX]7", re.IGNORECASE)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if pattern.search(line):
        print(f"Line {idx + 1}: {line.strip()}")
