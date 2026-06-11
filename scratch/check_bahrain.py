import re

with open('countries/air-ambulance-bahrain.html', 'r', encoding='utf-8') as f:
    text = f.read()

# find all forms
forms = re.findall(r'<form[^>]*id="([^"]+)"', text)
print("Forms found:", forms)

# find all inputs and selects and their IDs
inputs = re.findall(r'<input[^>]+id="([^"]+)"|<select[^>]+id="([^"]+)"', text)
print("IDs found:", [i[0] or i[1] for i in inputs])
