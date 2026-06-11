import urllib.request
import json

supabase_url = "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}"
}

req = urllib.request.Request(f"{supabase_url}/", headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        schema = json.loads(response.read().decode('utf-8'))
    print("Tables in blogs_db schema paths:")
    paths = schema.get("paths", {})
    for path in paths.keys():
        print(f"  {path}")
except Exception as e:
    print(f"Error querying blogs_db schema: {e}")

supabase_url_main = "https://dtiirdimtbmkvryvqten.supabase.co/rest/v1"
supabase_key_main = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDQ0MzksImV4cCI6MjA5MTcyMDQzOX0.MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI"

headers_main = {
    "apikey": supabase_key_main,
    "Authorization": f"Bearer {supabase_key_main}"
}

req = urllib.request.Request(f"{supabase_url_main}/", headers=headers_main)
try:
    with urllib.request.urlopen(req) as response:
        schema = json.loads(response.read().decode('utf-8'))
    print("Tables in main_db schema paths:")
    paths = schema.get("paths", {})
    for path in paths.keys():
        print(f"  {path}")
except Exception as e:
    print(f"Error querying main_db schema: {e}")
