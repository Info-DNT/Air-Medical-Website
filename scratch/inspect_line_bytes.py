with open('index.html', 'rb') as f:
    lines = f.readlines()

# Line 427 is index 426 (0-indexed)
line = lines[426]
print("Bytes:", line)
for b in line:
    print(f"{b} ({chr(b) if b < 128 else 'non-ascii'})")
