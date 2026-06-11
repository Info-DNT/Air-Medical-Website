import urllib.request
import json

supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c"
headers = {
    "apikey": supabase_key,
    "Authorization": f"Bearer {supabase_key}"
}

req = urllib.request.Request("https://eiqpvuciihwmuznbsyob.supabase.co/rest/v1/blogs?limit=1", headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        blogs = json.loads(response.read().decode('utf-8'))
        if blogs:
            print("Blog keys and types:")
            for k, v in blogs[0].items():
                print(f"  {k}: {type(v).__name__} (sample: {str(v)[:100]})")
        else:
            print("No blogs found.")
except Exception as e:
    print(e)
