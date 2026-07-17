import urllib.request
import json
import urllib.error
from datetime import datetime

supabase_url = "https://dtiirdimtbmkvryvqten.supabase.co/rest/v1/blogs"
# Use the Service Role key to bypass write RLS constraints
service_role_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjE0NDQzOSwiZXhwIjoyMDkxNzIwNDM5fQ.NCnB3zI0ESnhCzM19y1UOlu7Qn07Lm3LujSbAh2IzZU"

blog_html = """<p class="lead">Medical emergencies do not give you time to think. A sudden cardiac event, a serious road accident, a health crisis while travelling — these situations need a response that is fast and medically sound. That is exactly what Air Ambulance & Medical Evacuation Services are built for. In the UAE, where patients may need to be moved quickly across emirates or airlifted internationally, having the right air medical partner already in mind is worth more than most people realise.</p>

<p>Whether in <strong>Dubai, Abu Dhabi, Sharjah, or Ras Al Khaimah</strong>, air ambulance services operate across the UAE to get patients to the right hospital before their condition gets worse.</p>

<h3 class="mt-4 text-primary">What Are Air Ambulance & Medical Evacuation Services?</h3>
<p>Air ambulance and medical evacuation services use medically equipped aircraft — fixed-wing planes or helicopters — to transport critically ill or injured patients to appropriate medical facilities, fast.</p>

<p>These services cover a wide range of critical care needs, including:</p>
<ul class="list-group list-group-flush mb-4">
    <li class="list-group-item bg-transparent border-0 ps-0"><i class="fas fa-check text-red me-2"></i><strong>Emergency evacuations</strong> from accident sites or remote areas.</li>
    <li class="list-group-item bg-transparent border-0 ps-0"><i class="fas fa-check text-red me-2"></i><strong>Inter-hospital transfers</strong> when patients require specialised care at tertiary centres.</li>
    <li class="list-group-item bg-transparent border-0 ps-0"><i class="fas fa-check text-red me-2"></i><strong>Repatriation flights</strong> to bring patients back home safely from abroad.</li>
    <li class="list-group-item bg-transparent border-0 ps-0"><i class="fas fa-check text-red me-2"></i><strong>Organ transport</strong> requiring absolute speed and logistics precision.</li>
    <li class="list-group-item bg-transparent border-0 ps-0"><i class="fas fa-check text-red me-2"></i><strong>Neonatal and pediatric transfers</strong> requiring specialised medical teams and incubators onboard.</li>
</ul>
<p>Each flight carries trained medical professionals — doctors, nurses, and paramedics — with ICU-level equipment to monitor and stabilise patients throughout the journey.</p>

<h3 class="mt-4 text-primary">Why Air Ambulance Services Are Critical in the UAE</h3>
<p>The UAE sees millions of expatriates, tourists, and business travellers every year. Medical emergencies do not care about timing or convenience — and road transport in a busy UAE city can cost precious minutes.</p>

<p>Here is why air ambulance services matter in the UAE:</p>
<div class="row g-4 my-3">
    <div class="col-md-6">
        <div class="premium-card h-100 p-4" style="background: #f8fafc; border: 1px solid rgba(0, 0, 0, 0.03); border-radius: 16px;">
            <h5 class="fw-bold text-dark"><i class="fas fa-bolt text-red me-2"></i>Speed</h5>
            <p class="mb-0 small text-muted">Air ambulances skip traffic entirely. Ground transport cannot compete in time-critical cases where every second counts.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="premium-card h-100 p-4" style="background: #f8fafc; border: 1px solid rgba(0, 0, 0, 0.03); border-radius: 16px;">
            <h5 class="fw-bold text-dark"><i class="fas fa-globe-americas text-red me-2"></i>Long-Distance Coverage</h5>
            <p class="mb-0 small text-muted">The UAE is a global transfer hub. We connect patients headed to super-specialty hospitals in Europe, Asia, or the Americas.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="premium-card h-100 p-4" style="background: #f8fafc; border: 1px solid rgba(0, 0, 0, 0.03); border-radius: 16px;">
            <h5 class="fw-bold text-dark"><i class="fas fa-heartbeat text-red me-2"></i>Advanced Onboard Care</h5>
            <p class="mb-0 small text-muted">Patients get hospital-level ICU treatment during the flight, including active monitoring, rather than basic stabilisation.</p>
        </div>
    </div>
    <div class="col-md-6">
        <div class="premium-card h-100 p-4" style="background: #f8fafc; border: 1px solid rgba(0, 0, 0, 0.03); border-radius: 16px;">
            <h5 class="fw-bold text-dark"><i class="fas fa-clock text-red me-2"></i>24X7 Availability</h5>
            <p class="mb-0 small text-muted">Medical emergencies happen at night, on weekends, and on holidays. Dedicated operations teams are on standby 24X7/365.</p>
        </div>
    </div>
</div>

<h3 class="mt-4 text-primary">How Air Medical 24X7 Delivers Trusted Medical Transport in UAE</h3>
<p>For Air Ambulance & Medical Evacuation Services in the UAE, Air Medical 24X7 is a provider worth knowing. Their team includes experienced flight doctors, nurses, and paramedics. Their aircraft are equipped for critical care, and they operate around the clock.</p>

<p>Their specialised services include:</p>
<ul>
    <li class="mb-2"><strong>Domestic Air Ambulance:</strong> Quick transfers across all UAE emirates (Dubai, Abu Dhabi, Sharjah, Ras Al Khaimah, Fujairah, Ajman, Umm Al Quwain).</li>
    <li class="mb-2"><strong>International Medical Evacuation:</strong> Safe transfers to and from the UAE globally.</li>
    <li class="mb-2"><strong>Bedside-to-Bedside Service:</strong> Full end-to-end coordination, including ground ambulance support at both ends.</li>
    <li class="mb-2"><strong>Critical Care Transfers:</strong> Fully configured ICU setups onboard advanced aircraft.</li>
    <li class="mb-2"><strong>Repatriation of Mortal Remains:</strong> Handled with utmost care, respect, and compliance with local regulations.</li>
</ul>

<h3 class="mt-4 text-primary">What to Expect During an Air Ambulance Flight</h3>
<p>Most families have never dealt with a medical evacuation before. Here is how the process works:</p>
<ol>
    <li class="mb-2"><strong>Initial Assessment</strong> — The medical team reviews the patient's condition and decides what transport setup is needed.</li>
    <li class="mb-2"><strong>Flight Planning</strong> — Route, aircraft type, and onboard equipment are confirmed based on patient requirements.</li>
    <li class="mb-2"><strong>Onboard Medical Care</strong> — Doctors and nurses manage vitals, medications, and any complications during the flight.</li>
    <li class="mb-2"><strong>Hospital Coordination</strong> — The receiving hospital is briefed ahead of arrival for immediate admission.</li>
    <li class="mb-2"><strong>Safe Handover</strong> — The patient is transferred directly to the destination medical team.</li>
</ol>
<p>The process is built around one goal: getting the patient to the right place in the right condition.</p>

<h3 class="mt-4 text-primary">Conclusion</h3>
<p>When time is short and the stakes are high, Air Ambulance & Medical Evacuation Services in the UAE give patients a real chance of getting the care they need. Whether the transfer is local or international, what matters is having a provider who responds fast, sends qualified medical staff, and gets the patient to the right hospital. Contact Air Medical 24X7 today — do not wait until an emergency to figure out your options.</p>"""

payload = {
    "title": "Air Ambulance & Medical Evacuation Services in UAE - Fast, Safe, and Trusted Medical Transport",
    "slug": "air-ambulance-medical-evacuation-uae",
    "excerpt": "Medical emergencies do not give you time to think. Discover how Air Ambulance & Medical Evacuation Services in the UAE provide fast, safe, and trusted critical care patient transfers.",
    "content": blog_html,
    "featured_image": "img/air-ambulance-uae.jpg",
    "author": "Air Medical 24X7",
    "status": "published",
    "category": "Air Ambulance",
    "meta_title": "Air Ambulance & Medical Evacuation Services in UAE | Air Medical 24X7",
    "meta_description": "Emergency ICU air ambulance and medical evacuation services in the UAE. 24X7 bed-to-bed medical escort and patient repatriation. Call +971565542001.",
    "created_at": datetime.utcnow().isoformat() + "Z"
}

headers = {
    "apikey": service_role_key,
    "Authorization": f"Bearer {service_role_key}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates" # Enables upsert on conflict
}

req = urllib.request.Request(
    supabase_url,
    data=json.dumps(payload).encode('utf-8'),
    headers=headers,
    method="POST"
)

try:
    with urllib.request.urlopen(req) as res:
        print("Blog successfully inserted/upserted into database!")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
