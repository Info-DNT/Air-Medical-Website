with open("countries.html", "r", encoding="utf-8") as f1:
    c1 = f1.read()
with open("countries/index.html", "r", encoding="utf-8") as f2:
    c2 = f2.read()

print(f"countries.html size: {len(c1)}")
print(f"countries/index.html size: {len(c2)}")
print(f"Are they identical? {c1 == c2}")
