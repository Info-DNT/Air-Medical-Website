import urllib.request
import json
import urllib.error
import re

supabase_url = "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

def clean_db_text(text):
    if not text or not isinstance(text, str):
        return text
    
    # 1. missiona whispered reassurance -> mission, a whispered reassurance
    text = re.sub(r'missiona whispered reassurance', 'mission, a whispered reassurance', text, flags=re.IGNORECASE)
    
    # 2. Grammatical / Phrasing Replacements
    # "We provide globally air ambulance services..." -> "We provide global air ambulance..."
    text = re.sub(r'We provide globally air ambulance services', 'We provide global air ambulance services', text, flags=re.IGNORECASE)
    
    # "...quick facility with the greatest service..." -> "...rapid medical deployment and the highest quality care..."
    text = re.sub(r'quick facility with the greatest service', 'rapid medical deployment and the highest quality care', text, flags=re.IGNORECASE)
    
    # "Our team are available..." -> "Our team is available..."
    text = re.sub(r'Our team are available', 'Our team is available', text, flags=re.IGNORECASE)
    
    # 3. Terminology and Currency:
    # "...at a price you can afford which is 1.6 lacs to 2.5 lacs per hour..." -> "...at competitive hourly rates. Contact us for a customized, transparent quotation based on your routing."
    text = re.sub(r'at a price you can afford which is 1\.6 lacs to 2\.5 lacs per hour', 
                  'at competitive hourly rates. Contact us for a customized, transparent quotation based on your routing.', text, flags=re.IGNORECASE)
    text = re.sub(r'\b1\.6\s+lacs\b', 'competitive hourly rates', text, flags=re.IGNORECASE)
    text = re.sub(r'\b2\.5\s+lacs\b', 'competitive hourly rates', text, flags=re.IGNORECASE)
    text = re.sub(r'\blacs per hour\b', 'competitive hourly rates', text, flags=re.IGNORECASE)
    
    # 4. Brand Inconsistencies casing standardization:
    # First, handle 24/7/365 and 24x7/365 to 24X7/365
    text = re.sub(r'24/7/365', '24X7/365', text, flags=re.IGNORECASE)
    text = re.sub(r'24x7/365', '24X7/365', text, flags=re.IGNORECASE)
    text = re.sub(r'24×7/365', '24X7/365', text, flags=re.IGNORECASE)
    
    # Second, handle standalone 24/7, 24x7, 24×7 using safe lookbehinds/lookaheads
    # Preceded by NOT word, hyphen, slash, underscore, @, dot
    # Followed by NOT word, hyphen, slash, underscore, dot
    text = re.sub(r'(?<![\w\-@./])(24/7|24[xX]7|24×7)(?![\w\-@./])', '24X7', text)
    
    return text

print("=== Supabase Database Blogs Migration Script ===")

# Fetch all blogs
req = urllib.request.Request(f"{supabase_url}/blogs", headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        blogs = json.loads(response.read().decode('utf-8'))
    print(f"Successfully fetched {len(blogs)} blogs.")
except Exception as e:
    print(f"Error fetching blogs: {e}")
    blogs = []

updated_count = 0

for b in blogs:
    blog_id = b.get("id")
    slug = b.get("slug")
    print(f"\nAuditing blog ID: {blog_id} (slug: {slug})")
    
    # We check columns: title, excerpt, content, author, meta_title, meta_description
    cols_to_check = ["title", "excerpt", "content", "author", "meta_title", "meta_description"]
    updates = {}
    
    for col in cols_to_check:
        val = b.get(col)
        if val:
            cleaned = clean_db_text(val)
            if cleaned != val:
                updates[col] = cleaned
                # Print a small snippet of what changed
                print(f"  - Column '{col}' changed:")
                # find first difference
                for i in range(min(len(val), len(cleaned))):
                    if val[i] != cleaned[i]:
                        context_start = max(0, i-40)
                        context_end = min(len(val), i+60)
                        cleaned_end = min(len(cleaned), i+60)
                        print(f"    Original: ...{val[context_start:context_end].strip()}...")
                        print(f"    Updated:  ...{cleaned[context_start:cleaned_end].strip()}...")
                        break
                        
    if updates:
        # Send PATCH request to update this row
        patch_url = f"{supabase_url}/blogs?id=eq.{blog_id}"
        patch_req = urllib.request.Request(
            patch_url, 
            data=json.dumps(updates).encode('utf-8'),
            headers=headers,
            method="PATCH"
        )
        try:
            with urllib.request.urlopen(patch_req) as response:
                print(f"  -> Successfully patched row in Supabase!")
            updated_count += 1
        except urllib.error.HTTPError as e:
            print(f"  -> HTTP Error patching row: {e.code} - {e.read().decode('utf-8')}")
        except Exception as e:
            print(f"  -> Error patching row: {e}")
    else:
        print("  -> No changes needed.")

print(f"\nMigration complete. Updated {updated_count} blogs in database.")
