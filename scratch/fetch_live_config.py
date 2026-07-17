import urllib.request

req = urllib.request.Request(
    "https://airmedical24x7.com/js/config.js", 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)
try:
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
    print("Fetched config from live site:")
    for line in content.splitlines():
        if "supabase" in line.lower():
            print(f"  {line}")
except Exception as e:
    print(f"Error fetching live config: {e}")
