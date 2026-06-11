import urllib.request
import json
import urllib.error
import re

old_supabase_url = "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1"
old_supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

new_supabase_url = "https://dtiirdimtbmkvryvqten.supabase.co/rest/v1"
new_supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjE0NDQzOSwiZXhwIjoyMDkxNzIwNDM5fQ.NCnB3zI0ESnhCzM19y1UOlu7Qn07Lm3LujSbAh2IzZU"

def clean_db_text(text):
    if not text or not isinstance(text, str):
        return text
    
    # 1. missiona whispered reassurance -> mission, a whispered reassurance
    text = re.sub(r'missiona whispered reassurance', 'mission, a whispered reassurance', text, flags=re.IGNORECASE)
    
    # 2. Grammatical / Phrasing Replacements
    text = re.sub(r'We provide globally air ambulance services', 'We provide global air ambulance services', text, flags=re.IGNORECASE)
    text = re.sub(r'quick facility with the greatest service', 'rapid medical deployment and the highest quality care', text, flags=re.IGNORECASE)
    text = re.sub(r'Our team are available', 'Our team is available', text, flags=re.IGNORECASE)
    
    # 3. Terminology and Currency:
    text = re.sub(r'at a price you can afford which is 1\.6 lacs to 2\.5 lacs per hour', 
                  'at competitive hourly rates. Contact us for a customized, transparent quotation based on your routing.', text, flags=re.IGNORECASE)
    text = re.sub(r'\b1\.6\s+lacs\b', 'competitive hourly rates', text, flags=re.IGNORECASE)
    text = re.sub(r'\b2\.5\s+lacs\b', 'competitive hourly rates', text, flags=re.IGNORECASE)
    text = re.sub(r'\blacs per hour\b', 'competitive hourly rates', text, flags=re.IGNORECASE)
    
    # 4. Brand Inconsistencies casing standardization:
    text = re.sub(r'24/7/365', '24X7/365', text, flags=re.IGNORECASE)
    text = re.sub(r'24x7/365', '24X7/365', text, flags=re.IGNORECASE)
    text = re.sub(r'24×7/365', '24X7/365', text, flags=re.IGNORECASE)
    text = re.sub(r'(?<![\w\-@./])(24/7|24[xX]7|24×7)(?![\w\-@./])', '24X7', text)
    
    return text

print("=== Fetching blogs from old Supabase database ===")
old_headers = {
    "apikey": old_supabase_key,
    "Authorization": f"Bearer {old_supabase_key}"
}
req = urllib.request.Request(f"{old_supabase_url}/blogs", headers=old_headers)
try:
    with urllib.request.urlopen(req) as res:
        blogs = json.loads(res.read().decode('utf-8'))
    print(f"Fetched {len(blogs)} blogs.")
except Exception as e:
    print(f"Error fetching old blogs: {e}")
    exit(1)

print("\n=== Cleaning data and migrating to new Supabase database ===")
new_headers = {
    "apikey": new_supabase_key,
    "Authorization": f"Bearer {new_supabase_key}",
    "Content-Type": "application/json"
}

migrated_count = 0

for b in blogs:
    # Clean fields
    cleaned_blog = {
        "id": b.get("id"),
        "title": clean_db_text(b.get("title")),
        "slug": b.get("slug"),
        "excerpt": clean_db_text(b.get("excerpt")),
        "content": clean_db_text(b.get("content")),
        "featured_image": b.get("featured_image"),
        "author": clean_db_text(b.get("author")),
        "status": b.get("status"),
        "created_at": b.get("created_at"),
        "meta_title": clean_db_text(b.get("meta_title")),
        "meta_description": clean_db_text(b.get("meta_description")),
        "category": b.get("category", "general")
    }
    
    # Send POST request to insert into new database (or UPSERT by using query id=eq.<id>)
    # We do a standard POST insert. If it already exists, it can fail or we can upsert.
    # To upsert in PostgREST, we can add header Prefer: resolution=merge-duplicates
    insert_headers = new_headers.copy()
    insert_headers["Prefer"] = "resolution=merge-duplicates"
    
    post_req = urllib.request.Request(
        f"{new_supabase_url}/blogs",
        data=json.dumps(cleaned_blog).encode('utf-8'),
        headers=insert_headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(post_req) as post_res:
            print(f"Migrated blog: {cleaned_blog['slug']}")
            migrated_count += 1
    except urllib.error.HTTPError as e:
        print(f"Error migrating {cleaned_blog['slug']}: HTTP {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Error migrating {cleaned_blog['slug']}: {e}")

print(f"\nDone. Migrated {migrated_count} blogs to the new database.")
