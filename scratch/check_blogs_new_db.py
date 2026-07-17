import urllib.request
import json

new_supabase_url = "https://dtiirdimtbmkvryvqten.supabase.co/rest/v1/blogs"
new_supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDQ0MzksImV4cCI6MjA5MTcyMDQzOX0.MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI"

headers = {
    "apikey": new_supabase_key,
    "Authorization": f"Bearer {new_supabase_key}"
}

req = urllib.request.Request(new_supabase_url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        blogs = json.loads(response.read().decode('utf-8'))
        print(f"Blogs found in new DB: {len(blogs)}")
        for i, b in enumerate(blogs):
            print(f"{i+1}. Title: {b.get('title')} | Status: {b.get('status')} | Created At: {b.get('created_at')}")
except Exception as e:
    print("Error querying new DB:", e)
