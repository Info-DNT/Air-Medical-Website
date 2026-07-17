import urllib.request
import json
import urllib.error

supabase_url = "https://dtiirdimtbmkvryvqten.supabase.co/rest/v1"
service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjE0NDQzOSwiZXhwIjoyMDkxNzIwNDM5fQ.NCnB3zI0ESnhCzM19y1UOlu7Qn07Lm3LujSbAh2IzZU"

headers = {
    "apikey": service_role_key,
    "Authorization": f"Bearer {service_role_key}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# 1. Insert dummy blog
blog_payload = {
    "title": "Dummy Delete Test Blog",
    "slug": "dummy-delete-test-blog",
    "excerpt": "Excerpt for test blog",
    "content": "<p>Content for test blog</p>",
    "featured_image": "img/airmedicallogo.png",
    "author": "Air Medical 24X7",
    "status": "published",
    "category": "General"
}

req_insert = urllib.request.Request(
    f"{supabase_url}/blogs",
    data=json.dumps(blog_payload).encode('utf-8'),
    headers=headers,
    method="POST"
)

try:
    with urllib.request.urlopen(req_insert) as res:
        inserted = json.loads(res.read().decode('utf-8'))[0]
        blog_id = inserted['id']
        print(f"Successfully inserted blog with ID: {blog_id}")
        
        # 2. Try to insert comment referencing this blog
        comment_payload = {
            "blog_id": blog_id,
            "name": "Test Commenter",
            "email": "test@example.com",
            "message": "This is a test comment",
            "status": "approved"
        }
        req_comment = urllib.request.Request(
            f"{supabase_url}/comments",
            data=json.dumps(comment_payload).encode('utf-8'),
            headers=headers,
            method="POST"
        )
        try:
            with urllib.request.urlopen(req_comment) as res_comment:
                print("Successfully inserted comment referencing the blog!")
        except Exception as ce:
            print("Failed to insert comment:", ce)
            
        # 3. Try to delete the blog
        req_delete = urllib.request.Request(
            f"{supabase_url}/blogs?id=eq.{blog_id}",
            headers=headers,
            method="DELETE"
        )
        try:
            with urllib.request.urlopen(req_delete) as res_del:
                print("Successfully deleted blog from blogs table!")
        except urllib.error.HTTPError as he:
            print(f"Failed to delete blog: HTTP Error {he.code} - {he.read().decode('utf-8')}")
        except Exception as de:
            print("Failed to delete blog:", de)
            
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
