import urllib.request
import json

supabase_url = "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1/blogs"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Test inserting a draft blog post
test_blog = {
    "title": "Test Insert Blog Post",
    "slug": "test-insert-blog-post",
    "excerpt": "This is a test blog post to verify permissions.",
    "content": "<p>Test content.</p>",
    "author": "System Test",
    "status": "draft",
    "category": "test"
}

print("Testing INSERT...")
req = urllib.request.Request(supabase_url, data=json.dumps(test_blog).encode('utf-8'), headers=headers, method="POST")
try:
    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode('utf-8'))
        print("Insert successful!")
        print(json.dumps(res_data, indent=2))
        blog_id = res_data[0]["id"]
        
        # Test deleting it
        print("\nTesting DELETE...")
        del_headers = {
            "apikey": supabase_key,
            "Authorization": f"Bearer {supabase_key}"
        }
        del_req = urllib.request.Request(f"{supabase_url}?id=eq.{blog_id}", headers=del_headers, method="DELETE")
        with urllib.request.urlopen(del_req) as del_response:
            print("Delete successful!")
except Exception as e:
    print("Error during test:", e)
