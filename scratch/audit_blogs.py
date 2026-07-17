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

# Fetch blogs
req = urllib.request.Request(f"{supabase_url}/blogs", headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        blogs = json.loads(response.read().decode('utf-8'))
except Exception as e:
    print(f"Error fetching blogs: {e}")
    blogs = []

print(f"Fetched {len(blogs)} blogs.")

search_terms = {
    "ExpertMedical Escort": "ExpertMedical Escort",
    "ExpertMedical": "ExpertMedical",
    "EmergencyServices": "EmergencyServices",
    "24X7Support": "24X7Support",
    "GlobalService": "GlobalService",
    "missiona whispered reassurance": "missiona whispered reassurance",
    "We provide globally air ambulance services": "We provide globally air ambulance services",
    "quick facility with the greatest service": "quick facility with the greatest service",
    "Air Transfers Worldwide ,": "Air Transfers Worldwide ,",
    "Our team are available": "Our team are available",
    "1.6 lacs": "1.6 lacs",
    "lacs": "lacs",
    "24/7": "24/7",
    "24x7": "24x7",
    "24×7": "24×7",
}

for b in blogs:
    blog_id = b.get("id")
    slug = b.get("slug")
    title = b.get("title", "")
    author = b.get("author", "")
    content = b.get("content", "")
    excerpt = b.get("excerpt", "")
    
    found_in_blog = []
    for term_name, term_pattern in search_terms.items():
        # check title
        if title and term_pattern in title:
            found_in_blog.append(f"title: '{term_name}'")
        # check author
        if author and term_pattern in author:
            found_in_blog.append(f"author: '{term_name}'")
        # check excerpt
        if excerpt and term_pattern in excerpt:
            found_in_blog.append(f"excerpt: '{term_name}'")
        # check content
        if content and term_pattern in content:
            # find snippet
            idx = content.find(term_pattern)
            start = max(0, idx - 50)
            end = min(len(content), idx + len(term_pattern) + 50)
            snippet = content[start:end].replace('\n', ' ')
            found_in_blog.append(f"content: '{term_name}' (context: ...{snippet}...)")
            
    if found_in_blog:
        print(f"\nBlog ID: {blog_id}")
        print(f"Slug: {slug}")
        print(f"Title: {title}")
        for match in found_in_blog:
            print(f"  - Match: {match}")
