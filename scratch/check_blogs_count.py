import urllib.request
import json

supabase_url = "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Prefer": "count=exact"
}

req = urllib.request.Request(f"{supabase_url}/blogs?select=id,title,slug", headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        info = response.info()
        print("Response Headers:")
        for k, v in info.items():
            print(f"  {k}: {v}")
        blogs = json.loads(response.read().decode('utf-8'))
        print(f"\nFetched {len(blogs)} blogs.")
except Exception as e:
    print(f"Error: {e}")
