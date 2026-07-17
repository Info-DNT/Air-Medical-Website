with open(r"C:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main\scratch\diff_output.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

current_file = None
file_diff = []
for line in lines:
    if line.startswith("diff --git"):
        if current_file and current_file.endswith("a/index.html b/index.html"):
            break
        current_file = line.strip()
        if "a/index.html b/index.html" in line:
            file_diff = [line]
        else:
            file_diff = []
    elif file_diff:
        file_diff.append(line)

with open(r"C:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main\scratch\index_real_diff.txt", "w", encoding="utf-8") as f:
    f.writelines(file_diff)
print("Extracted real index.html diff to scratch/index_real_diff.txt")
