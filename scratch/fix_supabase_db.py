import urllib.request
import json
import re

supabase_url = "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json"
}

# Safe negative lookbehind regex to match 24/7 or 24x7 (case-insensitive) except when part of airmedical domain
pattern = re.compile(r'(?<!airmedical)(?<!airmedical-)(?<!airmedical_)(24/7|24[xX]7)', re.IGNORECASE)

def safe_replace(text):
    if not text:
        return text
    return pattern.sub("24X7", text)

# Fetch blogs
req = urllib.request.Request(f"{supabase_url}/blogs", headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        blogs = json.loads(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error fetching blogs: {e}")
    blogs = []

print(f"Fetched {len(blogs)} blogs. Checking for casing updates...")

updated_count = 0

for b in blogs:
    blog_id = b.get("id")
    author = b.get("author", "")
    title = b.get("title", "")
    content = b.get("content", "")
    
    new_author = safe_replace(author)
    new_title = safe_replace(title)
    new_content = safe_replace(content)
    
    # If any fields changed, update the blog in Supabase
    if new_author != author or new_title != title or new_content != content:
        print(f"\nUpdating blog {blog_id}:")
        if new_author != author:
            print(f"  Author: '{author}' -> '{new_author}'")
        if new_title != title:
            print(f"  Title: '{title}' -> '{new_title}'")
        if new_content != content:
            print(f"  Content: content length={len(content)}, differences found.")
            
        update_data = {
            "author": new_author,
            "title": new_title,
            "content": new_content
        }
        
        # Send PATCH request to update this row
        patch_url = f"{supabase_url}/blogs?id=eq.{blog_id}"
        patch_req = urllib.request.Request(
            patch_url,
            data=json.dumps(update_data).encode('utf-8'),
            headers=headers,
            method="PATCH"
        )
        
        try:
            with urllib.request.urlopen(patch_req) as patch_res:
                print(f"  Successfully updated blog {blog_id} (Status: {patch_res.status})")
                updated_count += 1
        except Exception as e:
            print(f"  Error updating blog {blog_id}: {e}")

print(f"\nDatabase casing migration finished. Total updated blogs: {updated_count}")
