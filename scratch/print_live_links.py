import urllib.request

req = urllib.request.Request(
    "https://airmedical24x7.com/blogs", 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
)
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    with open("scratch/live_blogs_page.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully wrote live blogs page to scratch/live_blogs_page.html")
except Exception as e:
    print(f"Error: {e}")
