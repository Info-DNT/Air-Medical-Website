import urllib.request
import re
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.links.append(value)

def fetch_url(url):
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# 1. Fetch live blogs index page
print("Fetching blogs index from live site...")
html = fetch_url("https://airmedical24x7.com/blogs")
if not html:
    print("Could not fetch live index page.")
    # Fallback: check blogs.html directly
    html = fetch_url("https://airmedical24x7.com/blogs.html")

if html:
    print("Successfully fetched blogs page.")
    parser = LinkParser()
    parser.feed(html)
    
    # Filter for blog detail links
    # They usually look like blogs-detail?slug=... or /blogs-detail?slug=... or similar
    blog_slugs = []
    for link in parser.links:
        if 'slug=' in link:
            match = re.search(r'slug=([^&]+)', link)
            if match:
                blog_slugs.append(match.group(1))
        elif 'blogs-detail/' in link:
            # maybe clean url path
            parts = link.split('/')
            blog_slugs.append(parts[-1])
            
    blog_slugs = list(set(blog_slugs))
    print(f"Found blog slugs on live page: {blog_slugs}")
    
    # Search terms to look for on live site
    patterns = {
        "ExpertMedical Escort": r"ExpertMedical\s*Escort",
        "ExpertMedical": r"ExpertMedical",
        "EmergencyServices": r"EmergencyServices",
        "24X7Support": r"24X7Support",
        "GlobalService": r"GlobalService",
        "missiona whispered reassurance": r"missiona\s+whispered\s+reassurance",
        "globally air ambulance": r"globally\s+air\s+ambulance",
        "quick facility with the greatest service": r"quick\s+facility\s+with\s+the\s+greatest\s+service",
        "Air Transfers Worldwide ,": r"Air\s+Transfers\s+Worldwide\s+,",
        "Our team are available": r"Our\s+team\s+are\s+available",
        "1.6 lacs": r"1.6\s+lacs",
        "lacs": r"lacs",
        "lakhs": r"lakhs"
    }
    
    # Crawl each slug detail page from live site
    for slug in blog_slugs:
        url = f"https://airmedical24x7.com/blogs-detail?slug={slug}"
        print(f"Fetching details for slug: {slug} from {url}...")
        detail_html = fetch_url(url)
        if not detail_html:
            # try alternative URL
            url = f"https://airmedical24x7.com/blogs-detail.html?slug={slug}"
            detail_html = fetch_url(url)
            
        if detail_html:
            for name, pat in patterns.items():
                if re.search(pat, detail_html, re.IGNORECASE):
                    print(f"  -> Found match for '{name}' on page {url}")
                    # Find context in body or print page content matching it
                    matches = re.finditer(pat, detail_html, re.IGNORECASE)
                    for match in matches:
                        start = max(0, match.start() - 60)
                        end = min(len(detail_html), match.end() + 60)
                        context = detail_html[start:end].replace('\n', ' ')
                        print(f"    Context: ...{context}...")
        else:
            print(f"  -> Failed to fetch detail page for {slug}")
else:
    print("Failed to get live blogs html.")
