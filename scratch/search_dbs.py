import urllib.request
import json
import urllib.error

dbs = {
    "main_db": {
        "url": "https://dtiirdimtbmkvryvqten.supabase.co/rest/v1",
        "key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDQ0MzksImV4cCI6MjA5MTcyMDQzOX0.MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI"
    },
    "blogs_db": {
        "url": "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1",
        "key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"
    }
}

tables_to_test = ["blogs", "comments", "leads", "quotes", "appointments", "contacts", "careers", "services"]
search_terms = ["1.6", "2.5", "lac", "lakh", "afford", "globally", "facility", "team are", "reassurance", "ExpertMedical", "EmergencyServices", "24X7Support", "GlobalService"]

for db_name, db_info in dbs.items():
    print(f"\n=== DB: {db_name} ===")
    url = db_info["url"]
    key = db_info["key"]
    
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    for table in tables_to_test:
        req = urllib.request.Request(f"{url}/{table}", headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                rows = json.loads(response.read().decode('utf-8'))
            print(f"Table '{table}': successfully fetched {len(rows)} rows.")
            for idx, row in enumerate(rows):
                row_str = json.dumps(row).lower()
                matches = [t for t in search_terms if t.lower() in row_str]
                if matches:
                    print(f"  Row {idx} contains matches: {matches}")
                    for k, v in row.items():
                        if isinstance(v, str):
                            for t in search_terms:
                                if t.lower() in v.lower():
                                    print(f"    Col '{k}' matches '{t}': {v[:100]}...")
        except urllib.error.HTTPError as e:
            if e.code != 404:
                print(f"Table '{table}': HTTP Error {e.code}")
        except Exception as e:
            print(f"Table '{table}': Error {e}")
