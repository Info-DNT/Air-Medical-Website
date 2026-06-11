import subprocess
import sys

def check_diff():
    # Run git diff against origin/main for all HTML files
    res = subprocess.run(["git", "diff", "origin/main"], capture_output=True, text=True, encoding="utf-8")
    with open(r"C:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main\scratch\diff_output.txt", "w", encoding="utf-8") as f:
        f.write(res.stdout)
    print("Done writing diff to scratch/diff_output.txt")

if __name__ == "__main__":
    check_diff()
