import re

# Read apply_all_requested_updates.py
with open("scratch/apply_all_requested_updates.py", "r", encoding="utf-8") as f:
    code = f.read()

# Remove "(Landline)" and "(Kongkita's Number)" labels
code = code.replace(" (Landline)", "")
code = code.replace(" (Kongkita's Number)", "")
code = code.replace(" (Landline)\"", "\"")
code = code.replace(" (Kongkita's Number)\"", "\"")

# Write it back
with open("scratch/apply_all_requested_updates.py", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated scratch/apply_all_requested_updates.py")
