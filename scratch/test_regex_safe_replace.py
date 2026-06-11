import re

# Negative lookbehind regex
pattern = re.compile(r'(?<!airmedical)(?<!airmedical-)(?<!airmedical_)(24/7|24[xX]7)', re.IGNORECASE)

test_cases = [
    # Should not change
    ("https://airmedical24x7.com", "https://airmedical24x7.com"),
    ("mailto:info@airmedical24x7.com", "mailto:info@airmedical24x7.com"),
    ("https://airmedical-24x7.com", "https://airmedical-24x7.com"),
    ("airmedical_24x7", "airmedical_24x7"),
    ("airmedical24x7", "airmedical24x7"),
    
    # Should change
    ("Air Medical 24x7", "Air Medical 24X7"),
    ("Available 24/7 Worldwide", "Available 24X7 Worldwide"),
    ("24/7 Support", "24X7 Support"),
    ("Air Medical 24x7 Team", "Air Medical 24X7 Team"),
    ("24x7 International Air Ambulance", "24X7 International Air Ambulance"),
    ("<p>Available 24/7</p>", "<p>Available 24X7</p>"),
]

print("Running Regex Tests:")
success = True
for original, expected in test_cases:
    result = pattern.sub("24X7", original)
    if result == expected:
        print(f"[PASS] '{original}' -> '{result}'")
    else:
        print(f"[FAIL] '{original}' -> '{result}' (expected '{expected}')")
        success = False

if success:
    print("\nAll tests passed successfully!")
else:
    print("\nSome tests failed.")
