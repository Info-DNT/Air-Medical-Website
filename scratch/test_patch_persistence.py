import urllib.request
import json
import urllib.error

supabase_url = "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"  # Ask PostgREST to return the updated rows
}

# Fetch the first blog
req = urllib.request.Request(f"{supabase_url}/blogs?limit=1", headers=headers)
try:
    with urllib.request.urlopen(req) as res:
        blogs = json.loads(res.read().decode('utf-8'))
    if not blogs:
        print("No blogs found.")
        exit(0)
    blog = blogs[0]
    blog_id = blog["id"]
    old_title = blog["title"]
    print(f"Current title of blog {blog_id}: '{old_title}'")
    
    # Try to patch it with a slightly modified title (e.g. adding a dot or similar)
    new_title = old_title + " " if not old_title.endswith(" ") else old_title[:-1]
    print(f"Attempting to patch title to: '{new_title}'")
    
    patch_url = f"{supabase_url}/blogs?id=eq.{blog_id}"
    patch_req = urllib.request.Request(
        patch_url,
        data=json.dumps({"title": new_title}).encode('utf-8'),
        headers=headers,
        method="PATCH"
    )
    
    with urllib.request.urlopen(patch_req) as patch_res:
        patched_data = json.loads(patch_res.read().decode('utf-8'))
        print(f"PATCH response body: {patched_data}")
        
    # Fetch again to verify
    req2 = urllib.request.Request(f"{supabase_url}/blogs?id=eq.{blog_id}", headers=headers)
    with urllib.request.urlopen(req2) as res2:
        blog_after = json.loads(res2.read().decode('utf-8'))[0]
    print(f"Fetched title after patch: '{blog_after['title']}'")
    
except Exception as e:
    print(f"Error: {e}")
