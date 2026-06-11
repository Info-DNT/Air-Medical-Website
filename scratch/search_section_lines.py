import os

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
files = [
    r"index.html",
    r"countries\air-ambulance-bangladesh.html",
    r"countries\air-ambulance-saudi-arabia.html",
    r"services\air-ambulance-charters.html",
    r"services\airline-stretcher-services.html"
]

for f in files:
    filepath = os.path.join(root_dir, f)
    if os.path.exists(filepath):
        print(f"\n--- Context in {f} ---")
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except:
            continue
        for idx, line in enumerate(lines):
            if "Ground Ambulance" in line or "Domestic transfer" in line:
                # Print 3 lines before and after
                start = max(0, idx - 3)
                end = min(len(lines), idx + 4)
                for line_idx in range(start, end):
                    print(f"{line_idx+1}: {lines[line_idx].strip()}")
                print("...")
