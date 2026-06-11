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
    "title": "Dummy Cascade Delete Test Blog",
    "slug": "dummy-cascade-delete-test-blog",
    "excerpt": "Excerpt for cascade test blog",
    "content": "<p>Content for cascade test blog</p>",
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
        
        # 2. Insert comment referencing this blog
        comment_payload = {
            "blog_id": blog_id,
            "name": "Cascade Commenter",
            "email": "cascade@example.com",
            "message": "This comment should be deleted",
            "status": "approved"
        }
        req_comment = urllib.request.Request(
            f"{supabase_url}/comments",
            data=json.dumps(comment_payload).encode('utf-8'),
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req_comment) as res_comment:
            print("Successfully inserted comment referencing the blog!")
            
        # 3. Simulate cascading delete:
        # A. Delete comments associated with the blog
        req_del_comments = urllib.request.Request(
            f"{supabase_url}/comments?blog_id=eq.{blog_id}",
            headers=headers,
            method="DELETE"
        )
        with urllib.request.urlopen(req_del_comments) as res_del_comm:
            print("Successfully deleted associated comments!")
            
        # B. Delete the blog post
        req_del_blog = urllib.request.Request(
            f"{supabase_url}/blogs?id=eq.{blog_id}",
            headers=headers,
            method="DELETE"
        )
        with urllib.request.urlopen(req_del_blog) as res_del_blg:
            print("Successfully deleted the blog post!")
            
        # 4. Verify that comments are gone
        req_check_comments = urllib.request.Request(
            f"{supabase_url}/comments?blog_id=eq.{blog_id}",
            headers={"apikey": service_role_key, "Authorization": f"Bearer {service_role_key}"}
        )
        with urllib.request.urlopen(req_check_comments) as check_res:
            comm_list = json.loads(check_res.read().decode('utf-8'))
            print(f"Associated comments remaining in DB: {len(comm_list)}")
            
        # 5. Verify that blog is gone
        req_check_blog = urllib.request.Request(
            f"{supabase_url}/blogs?id=eq.{blog_id}",
            headers={"apikey": service_role_key, "Authorization": f"Bearer {service_role_key}"}
        )
        with urllib.request.urlopen(req_check_blog) as check_blg_res:
            blg_list = json.loads(check_blg_res.read().decode('utf-8'))
            print(f"Blog posts remaining in DB matching ID: {len(blg_list)}")

except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
