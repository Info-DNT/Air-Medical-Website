with open('css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
print("=== Testimonial Section in style.css ===")
for i, line in enumerate(lines):
    if 'testimonial-section' in line:
        start = max(0, i - 2)
        end = min(len(lines), i + 15)
        print(f"Lines {start+1}-{end}:")
        for j in range(start, end):
            print(f"{j+1}: {lines[j]}")
