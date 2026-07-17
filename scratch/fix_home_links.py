import os
import glob

workspace_dir = r"c:\Users\DELL\Downloads\AIR-MEDICAL-24X7-Tushar-main (2)\AIR-MEDICAL-24X7-Tushar-main"

def fix_root_files():
    root_files = glob.glob(os.path.join(workspace_dir, "*.html"))
    for file_path in root_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Replace logo link
            new_content = content.replace('class="navbar-brand" href="/"', 'class="navbar-brand" href="index.html"')
            # Replace home link
            new_content = new_content.replace('href="/" class="nav-item nav-link">Home</a>', 'href="index.html" class="nav-item nav-link">Home</a>')
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed root file: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")

def fix_country_files():
    country_files = glob.glob(os.path.join(workspace_dir, "countries", "*.html"))
    for file_path in country_files:
        try:
            # Let's handle different possible encodings if any
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Replace logo link
            new_content = content.replace('class="navbar-brand" href="/"', 'class="navbar-brand" href="../index.html"')
            # Replace home link
            new_content = new_content.replace('href="/" class="nav-item nav-link">Home</a>', 'href="../index.html" class="nav-item nav-link">Home</a>')
            
            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"Fixed country file: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error fixing {file_path}: {e}")

if __name__ == "__main__":
    print("Fixing root files...")
    fix_root_files()
    print("Fixing country files...")
    fix_country_files()
    print("Done!")
