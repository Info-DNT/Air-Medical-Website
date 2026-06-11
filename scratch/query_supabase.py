import urllib.request
import json
import re

supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}"
}

def query_url(url):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error querying {url}: {e}")
        return None

# 1. Fetch blogs
print("Fetching blogs from Supabase...")
blogs = query_url("https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1/blogs")
if blogs is not None:
    print(f"Successfully fetched {len(blogs)} blogs.")
    for b in blogs:
        author = b.get("author", "")
        title = b.get("title", "")
        content = b.get("content", "")
        
        # Check author
        if author and ("24/7" in author or "24x7" in author or "24X7" in author):
            print(f"[Blog {b.get('id')}] Author: '{author}' (Title: '{title}')")
            
        # Check title
        if title and ("24/7" in title or "24x7" in title or "24X7" in title):
            print(f"[Blog {b.get('id')}] Title: '{title}'")
            
        # Check content
        if content:
            matches = re.findall(r'24/7|24[xX]7', content)
            bad_matches = [m for m in matches if m != '24X7']
            if bad_matches:
                print(f"[Blog {b.get('id')}] Content contains invalid casings: {set(bad_matches)}")
else:
    print("Failed to fetch blogs.")

# 2. Fetch comments
print("\nFetching comments from Supabase...")
comments = query_url("https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1/comments")
if comments is not None:
    print(f"Successfully fetched {len(comments)} comments.")
    for c in comments:
        name = c.get("name", "")
        message = c.get("message", "")
        admin_reply = c.get("admin_reply", "")
        
        if name and ("24/7" in name or "24x7" in name or "24X7" in name):
            print(f"[Comment {c.get('id')}] Name: '{name}'")
        if message and ("24/7" in message or "24x7" in message or "24X7" in message):
            print(f"[Comment {c.get('id')}] Message: '{message}'")
        if admin_reply and ("24/7" in admin_reply or "24x7" in admin_reply or "24X7" in admin_reply):
            print(f"[Comment {c.get('id')}] Admin Reply: '{admin_reply}'")
else:
    print("Failed to fetch comments.")
