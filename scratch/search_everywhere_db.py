import urllib.request
import json

dbs = {
    "main_db": {
        "url": "https://dtiirdimtbmkvryvqten.supabase.co/rest/v1",
        "key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDQ0MzksImV4cCI6Mj91NzIwNDM5fQ.MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI" # key in config.js is MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI
    },
    "blogs_db": {
        "url": "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1",
        "key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"
    }
}

# The key for main_db from config.js:
main_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDQ0MzksImV4cCI6MjA5MTcyMDQzOX0.MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI"
dbs["main_db"]["key"] = main_key

search_terms = ["1.6", "2.5", "lac", "lakh", "afford", "globally", "facility", "team are", "reassurance", "ExpertMedical", "EmergencyServices", "24X7Support", "GlobalService"]

for db_name, db_info in dbs.items():
    print(f"=== DB: {db_name} ===")
    url = db_info["url"]
    key = db_info["key"]
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # We query the blogs table
    req = urllib.request.Request(f"{url}/blogs", headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            rows = json.loads(response.read().decode('utf-8'))
        print(f"Fetched {len(rows)} rows from blogs table.")
        for idx, row in enumerate(rows):
            row_str = json.dumps(row).lower()
            found = [t for t in search_terms if t.lower() in row_str]
            if found:
                print(f"  Row {idx} (ID: {row.get('id')}, Slug: {row.get('slug')}): contains {found}")
                # print exact context of matches
                for val_k, val_v in row.items():
                    if not isinstance(val_v, str):
                        continue
                    for term in search_terms:
                        if term.lower() in val_v.lower():
                            # find all occurences
                            start_idx = 0
                            while True:
                                match_idx = val_v.lower().find(term.lower(), start_idx)
                                if match_idx == -1:
                                    break
                                context = val_v[max(0, match_idx - 60):min(len(val_v), match_idx + len(term) + 60)].replace('\n', ' ')
                                print(f"    Field '{val_k}' matches '{term}': ...{context}...")
                                start_idx = match_idx + 1
    except Exception as e:
        print(f"Error querying {db_name} blogs table: {e}")
        
    # We query the comments table
    req = urllib.request.Request(f"{url}/comments", headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            rows = json.loads(response.read().decode('utf-8'))
        print(f"Fetched {len(rows)} rows from comments table.")
        for idx, row in enumerate(rows):
            row_str = json.dumps(row).lower()
            found = [t for t in search_terms if t.lower() in row_str]
            if found:
                print(f"  Comment {idx} (ID: {row.get('id')}): contains {found}")
    except Exception as e:
        print(f"Error querying {db_name} comments table: {e}")
