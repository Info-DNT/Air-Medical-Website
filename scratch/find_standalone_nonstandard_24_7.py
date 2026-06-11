import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"

html_files = (
    [os.path.join(root_dir, f) for f in os.listdir(root_dir) if f.endswith(".html")] +
    [os.path.join(root_dir, "countries", f) for f in os.listdir(os.path.join(root_dir, "countries")) if f.endswith(".html")] +
    [os.path.join(root_dir, "services", f) for f in os.listdir(os.path.join(root_dir, "services")) if f.endswith(".html")]
)

# Regex matching 24/7 or 24x7 or 24×7 case-insensitively,
# but using negative lookbehind and lookahead to avoid matches like airmedical24x7.com, etc.
# Standalone or spaced occurrences like "24/7 support", "24x7 service", etc.
pattern = re.compile(r'(?<!airmedical)(?<!airmedical-)(?<!airmedical_)(24/7|24[xX]7|24×7)', re.IGNORECASE)

with open("scratch/nonstandard_24_7_audit.txt", "w", encoding="utf-8") as out:
    out.write("Auditing workspace for standalone 24/7, 24x7, or 24×7 (excluding domain names/emails):\n")
    found_count = 0
    for hf in html_files:
        rel_path = os.path.relpath(hf, root_dir)
        try:
            with open(hf, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            out.write(f"Error reading {rel_path}: {e}\n")
            continue
        
        for idx, line in enumerate(lines):
            matches = list(pattern.finditer(line))
            # We want to filter out exact match of "24X7" (uppercase).
            # If the match group is "24/7" or "24x7" or "24×7" (not "24X7"), we report it.
            valid_matches = [m for m in matches if m.group(1) != "24X7"]
            if valid_matches:
                found_count += len(valid_matches)
                out.write(f"[{rel_path}:L{idx+1}] Found non-standard:\n")
                for m in valid_matches:
                    start = max(0, m.start() - 40)
                    end = min(len(line), m.end() + 40)
                    out.write(f"  -> Match '{m.group(1)}' in context: ...{line[start:end].strip()}...\n")
                    
    out.write(f"\nAudit complete. Found {found_count} non-standard occurrences in HTML files.\n")
print("Done writing non-standard 24/7 audit.")
