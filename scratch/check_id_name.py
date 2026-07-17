import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Occurrences of id="name":', len(re.findall(r'id="name"', text)))
print('Occurrences of id="email":', len(re.findall(r'id="email"', text)))
print('Occurrences of id="phone":', len(re.findall(r'id="phone"', text)))
print('Occurrences of id="service":', len(re.findall(r'id="service"', text)))
print('Occurrences of id="patientLocation":', len(re.findall(r'id="patientLocation"', text)))
print('Occurrences of id="destination":', len(re.findall(r'id="destination"', text)))
