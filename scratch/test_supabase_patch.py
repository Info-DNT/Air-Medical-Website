import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

supabase_url = "https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"

headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}"
}

req = urllib.request.Request(f"{supabase_url}/blogs?limit=1", headers=headers)
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode('utf-8'))
    if data:
        print("Columns in blogs table:")
        for k in data[0].keys():
            print(" -", k)
