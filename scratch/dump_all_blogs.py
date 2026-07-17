import urllib.request
import json

supabase_url = "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json"
}

req = urllib.request.Request(f"{supabase_url}/blogs", headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        blogs = json.loads(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error fetching blogs: {e}")
    blogs = []

print(f"Fetched {len(blogs)} blogs.")
for idx, b in enumerate(blogs):
    print(f"[{idx}] ID: {b.get('id')} | Slug: {b.get('slug')} | Title: {b.get('title')}")
    # save to a file
    filename = f"scratch/blog_{idx}_{b.get('slug')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(b, f, indent=2, ensure_ascii=False)
    print(f"  Saved to {filename}")
