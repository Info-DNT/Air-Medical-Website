import os
import re

root_dir = r"c:\Users\Admin\Downloads\airmedical_24X7_jeet-main\airmedical_24X7_jeet-main"
about_path = os.path.join(root_dir, "about-us.html")
countries_idx_path = os.path.join(root_dir, "countries", "index.html")

# Read template sources
with open(about_path, "r", encoding="utf-8") as f:
    about_content = f.read()

with open(countries_idx_path, "r", encoding="utf-8") as f:
    countries_idx_content = f.read()

def get_header_footer(content):
    # Split by <!-- About Start -->
    parts = content.split("<!-- About Start -->")
    header = parts[0]
    # Split by <!-- Footer Start -->
    footer_parts = parts[1].split("<!-- Footer Start -->")
    footer = "<!-- Footer Start -->" + footer_parts[1]
    return header, footer

root_header, root_footer = get_header_footer(about_content)
countries_header, countries_footer = get_header_footer(countries_idx_content)

def replace_metadata(header, title, description, keywords, canonical_url):
    header = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", header)
    
    # Handle both meta tags patterns
    if 'name="description"' in header:
        header = re.sub(r'<meta name="description"\s+content=".*?"', f'<meta name="description" content="{description}"', header)
    else:
        header = re.sub(r'<meta content=".*?"\s+name="description"', f'<meta content="{description}" name="description"', header)
        
    if 'name="keywords"' in header:
        header = re.sub(r'<meta name="keywords"\s+content=".*?"', f'<meta name="keywords" content="{keywords}"', header)
    else:
        header = re.sub(r'<meta content=".*?"\s+name="keywords"', f'<meta content="{keywords}" name="keywords"', header)
        
    header = re.sub(r'<link rel="canonical"\s+href=".*?"', f'<link rel="canonical" href="{canonical_url}"', header)
    
    # OG tags
    header = re.sub(r'<meta property="og:title"\s+content=".*?"', f'<meta property="og:title" content="{title}"', header)
    header = re.sub(r'<meta property="og:description"\s+content=".*?"', f'<meta property="og:description" content="{description}"', header)
    header = re.sub(r'<meta property="og:url"\s+content=".*?"', f'<meta property="og:url" content="{canonical_url}"', header)
    
    # Twitter tags
    header = re.sub(r'<meta name="twitter:title"\s+content=".*?"', f'<meta name="twitter:title" content="{title}"', header)
    header = re.sub(r'<meta name="twitter:description"\s+content=".*?"', f'<meta name="twitter:description" content="{description}"', header)
    
    return header

# Standard Quote Form for Root Pages
root_quote_form = """
        <!-- Right Section - New Form -->
        <div class="col-lg-5">
          <div class="bg-white text-center rounded p-5 shadow-lg">
            <h2 class="mb-2">Get a Free Quotation</h2>
            <p class="text-muted mb-4 small fw-bold"><i class="far fa-clock text-red me-1"></i> Get a quotation in 30 minutes</p>

            <form id="quoteForm">
              <div class="row g-3 text-start">
                <!-- Full Name -->
                <div class="col-12 col-sm-12">
                  <label class="fw-bold mb-1">Full Name</label>
                  <input type="text" id="name" name="name" class="form-control bg-light border-0"
                    placeholder="Enter your name" required pattern="[A-Za-z ]+" style="height:55px">
                </div>

                <!-- Phone -->
                <div class="col-12 col-sm-12">
                  <label class="fw-bold mb-1">Phone Number</label>
                  <div class="input-group">
                    <input type="text" id="countryCode" class="form-control bg-light border-0"
                      style="max-width:90px; height:55px;" readonly>
                    <input type="tel" id="phone" name="phone" class="form-control bg-light border-0"
                      placeholder="Enter your phone number" required style="height:55px">
                  </div>
                </div>

                <!-- Hidden combined phone -->
                <input type="hidden" name="full_phone" id="full_phone">

                <!-- Email -->
                <div class="col-12 col-sm-12">
                  <label class="fw-bold mb-1">Email</label>
                  <input type="email" id="email" name="email" class="form-control bg-light border-0"
                    placeholder="Enter your email" required style="height:55px">
                </div>

                <!-- Patient Location -->
                <div class="col-12 col-sm-6">
                  <label class="fw-bold mb-1">Patient Location</label>
                  <input type="text" id="patientLocation" name="patientLocation" class="form-control bg-light border-0"
                    placeholder="City / Country" required style="height:55px">
                </div>

                <!-- Destination -->
                <div class="col-12 col-sm-6">
                  <label class="fw-bold mb-1">Destination</label>
                  <input type="text" id="destination" name="destination" class="form-control bg-light border-0"
                    placeholder="City / Country" required style="height:55px">
                </div>

                <!-- Services -->
                <div class="col-12 col-sm-12">
                  <label class="fw-bold mb-1">Select Service</label>
                  <select id="service" name="service" class="form-select bg-light border-0" required style="height:55px">
                    <option value="Air Ambulance">Air Ambulance</option>
                    <option value="Flight Medical escort">Flight Medical escort</option>
                    <option value="Commercial Flight Stretcher Service">Commercial Flight Stretcher Service</option>
                    <option value="Medical Tourism">Medical Tourism</option>
                    <option value="Private Medical Charter Jet">Private Medical Charter Jet</option>
                    <option value="ECMO Transfer Services">ECMO Transfer Services</option>
                    <option value="Home Health Care">Home Health Care</option>
                  </select>
                </div>

                <div class="col-12">
                  <button class="btn btn-primary w-100 py-3" type="submit">
                    Get a Free Quotation
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
"""

# Standard Quote Form for Subdirectory Pages (countries/)
countries_quote_form = """
            <!-- RIGHT FORM -->
            <div class="col-lg-5">
                <div class="bg-light rounded p-4 p-lg-5 shadow-sm">
                    <h4 class="text-primary mb-2 text-center">
                        Get a Free Quotation
                    </h4>
                    <p class="text-muted mb-4 small fw-bold text-center"><i class="far fa-clock text-red me-1"></i> Get a quotation in 30 minutes</p>
                    
                    <form id="quoteForm">
                      <div class="row g-3 text-start">
                        <!-- Full Name -->
                        <div class="col-12 col-sm-12">
                          <label class="fw-bold mb-1">Full Name</label>
                          <input type="text" id="name" name="name" class="form-control bg-light border-0"
                            placeholder="Enter your name" required pattern="[A-Za-z ]+" style="height:55px">
                        </div>

                        <!-- Phone -->
                        <div class="col-12 col-sm-12">
                          <label class="fw-bold mb-1">Phone Number</label>
                          <div class="input-group">
                            <input type="text" id="countryCode" class="form-control bg-light border-0"
                              style="max-width:90px; height:55px;" readonly>
                            <input type="tel" id="phone" name="phone" class="form-control bg-light border-0"
                              placeholder="Enter your phone number" required style="height:55px">
                          </div>
                        </div>

                        <!-- Hidden combined phone -->
                        <input type="hidden" name="full_phone" id="full_phone">

                        <!-- Email -->
                        <div class="col-12 col-sm-12">
                          <label class="fw-bold mb-1">Email</label>
                          <input type="email" id="email" name="email" class="form-control bg-light border-0"
                            placeholder="Enter your email" required style="height:55px">
                        </div>

                        <!-- Patient Location -->
                        <div class="col-12 col-sm-6">
                          <label class="fw-bold mb-1">Patient Location</label>
                          <input type="text" id="patientLocation" name="patientLocation" class="form-control bg-light border-0"
                            placeholder="City / Country" required style="height:55px">
                        </div>

                        <!-- Destination -->
                        <div class="col-12 col-sm-6">
                          <label class="fw-bold mb-1">Destination</label>
                          <input type="text" id="destination" name="destination" class="form-control bg-light border-0"
                            placeholder="City / Country" required style="height:55px">
                        </div>

                        <!-- Services -->
                        <div class="col-12 col-sm-12">
                          <label class="fw-bold mb-1">Select Service</label>
                          <select id="service" name="service" class="form-select bg-light border-0" required style="height:55px">
                            <option value="Air Ambulance">Air Ambulance</option>
                            <option value="Flight Medical escort">Flight Medical escort</option>
                            <option value="Commercial Flight Stretcher Service">Commercial Flight Stretcher Service</option>
                            <option value="Medical Tourism">Medical Tourism</option>
                            <option value="Private Medical Charter Jet">Private Medical Charter Jet</option>
                            <option value="ECMO Transfer Services">ECMO Transfer Services</option>
                          </select>
                        </div>

                        <div class="col-12">
                          <button class="btn btn-primary w-100 py-3" type="submit">
                            Get a Free Quotation
                          </button>
                        </div>
                      </div>
                    </form>
                </div>
            </div>
"""

# Common Scripts block
root_scripts = """
  <script>
    // Auto-detect country code via IP
    fetch("https://ipapi.co/json/")
      .then(res => res.json())
      .then(data => {
        document.getElementById("countryCode").value = data.country_calling_code || "+1";
      })
      .catch(() => {
        document.getElementById("countryCode").value = "+1";
      });

    // Combine phone and concatenate locations on submit
    window.addEventListener("load", function () {
      const form = document.getElementById("quoteForm");
      if (!form) return;
      const supabase = window.supabaseClient;

      form.addEventListener("submit", async function (e) {
        e.preventDefault();
        const fullPhone = document.getElementById("countryCode").value + document.getElementById("phone").value;
        const selectedService = document.getElementById("service").value;
        const patientLocation = document.getElementById("patientLocation").value;
        const destination = document.getElementById("destination").value;

        const payload = {
          name: document.getElementById("name").value,
          email: document.getElementById("email").value,
          full_phone: fullPhone,
          service: `${selectedService} (From: ${patientLocation}, To: ${destination})`
        };

        const { error } = await supabase.from("main_page").insert([payload]);
        if (error) {
          alert("Error: " + error.message);
        } else {
          alert("✅ Thank you! Our team will contact you soon.");
          form.reset();
        }
      });
    });
  </script>
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="js/config.js"></script>
"""

countries_scripts = """
  <script>
    // Auto-detect country code via IP
    fetch("https://ipapi.co/json/")
      .then(res => res.json())
      .then(data => {
        document.getElementById("countryCode").value = data.country_calling_code || "+1";
      })
      .catch(() => {
        document.getElementById("countryCode").value = "+1";
      });

    // Combine phone and concatenate locations on submit
    window.addEventListener("load", function () {
      const form = document.getElementById("quoteForm");
      if (!form) return;
      const supabase = window.supabaseClient;

      form.addEventListener("submit", async function (e) {
        e.preventDefault();
        const fullPhone = document.getElementById("countryCode").value + document.getElementById("phone").value;
        const selectedService = document.getElementById("service").value;
        const patientLocation = document.getElementById("patientLocation").value;
        const destination = document.getElementById("destination").value;

        const payload = {
          name: document.getElementById("name").value,
          email: document.getElementById("email").value,
          full_phone: fullPhone,
          service: `${selectedService} (From: ${patientLocation}, To: ${destination})`
        };

        const { error } = await supabase.from("main_page").insert([payload]);
        if (error) {
          alert("Error: " + error.message);
        } else {
          alert("✅ Thank you! Our team will contact you soon.");
          form.reset();
        }
      });
    });
  </script>
  <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
  <script src="../js/config.js"></script>
"""

# Let's define the content pages data
pages = [
    # --- COUNTRIES DIRECTORY ---
    {
        "filename": "countries/air-ambulance-dubai.html",
        "title": "Air Ambulance Dubai | Emergency ICU Flights - Air Medical 24X7",
        "description": "Emergency ICU air ambulance services in Dubai. 24X7 bed-to-bed medical evacuation, critical care transfer, and neonatal flights with doctors onboard.",
        "keywords": "air ambulance dubai, emergency flight dubai, patient transfer dubai, dubai medical evacuation, icu flight dubai",
        "canonical": "https://airmedical24x7.com/air-ambulance-dubai",
        "is_country": True,
        "hero_title": "Air Ambulance Dubai",
        "hero_desc": "24X7 ICU medical flights and bed-to-bed evacuations globally.",
        "image": "img/uae-country.jpg",
        "h1": "Emergency Air Ambulance Services in Dubai",
        "intro": "Air Medical 24X7 provides prompt, bed-to-bed private air ambulance and medical repatriation services from Dubai (U.A.E.) to any country globally. Strategically based near Dubai International Airport (DXB), we coordinate fast take-off clearances and intensive care flights.",
        "content_html": """
            <div class="row g-5 align-items-start">
                <div class="col-lg-7">
                    <h2 class="mb-4 text-primary">Global Medical Evacuation from Dubai</h2>
                    <p>When critical illness or trauma strikes, time is the most valuable factor. Air Medical 24X7 delivers <strong>ICU-equipped private air ambulance charters</strong> operating out of Dubai. Our medical crews include intensive care specialists, flight doctors, and paramedics certified in aviation medicine.</p>
                    
                    <h4 class="mt-4 text-dark">Why Choose Our Dubai Air Ambulance Service?</h4>
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>DXB Proximity:</strong> Located minutes from Garhoud, enabling immediate logistics coordination.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Bed-to-Bed Care:</strong> Ground ambulance transfers from top Dubai hospitals (Rashid Hospital, Mediclinic City Hospital, American Hospital) directly to the aircraft.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>CAMTS Protocol:</strong> High-standard medical flights with FAA-approved equipment.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Fast Permits:</strong> Direct liaison with the Dubai Civil Aviation Authority (DCAA) for priority take-off permits.</li>
                    </ul>

                    <h4 class="mt-4 text-dark">Our Clinical Specialties</h4>
                    <p>We configure each private aircraft specifically for the patient's condition, including advanced cardiac monitoring, mechanical ventilation, neonatal incubators, and specialized ECMO life support setups.</p>
                </div>
                {quote_form}
            </div>
        """
    },
    {
        "filename": "countries/air-ambulance-india.html",
        "title": "Air Ambulance Service in India | 24X7 ICU Flights - Air Medical 24X7",
        "description": "24X7 emergency air ambulance service in India. Safe, bed-to-bed patient transfer, critical care medical flights, and organ transport across India.",
        "keywords": "air ambulance india, medical flight india, domestic air ambulance india, patient transfer india, air ambulance cost india",
        "canonical": "https://airmedical24x7.com/air-ambulance-india",
        "is_country": True,
        "hero_title": "Air Ambulance India",
        "hero_desc": "Emergency critical care flights and patient transfers across India and worldwide.",
        "image": "img/flight-medical.jpg",
        "h1": "24X7 ICU Air Ambulance Service in India",
        "intro": "Providing domestic and international air ambulance flights across India. With our primary Indian operations center in Rajendra Place, New Delhi, we coordinate seamless, fast bed-to-bed medical transfers.",
        "content_html": """
            <div class="row g-5 align-items-start">
                <div class="col-lg-7">
                    <h2 class="mb-4 text-primary">Emergency ICU Flights Across India</h2>
                    <p>Air Medical 24X7 provides specialized air ambulance services across all major cities in India, including Delhi NCR, Mumbai, Chennai, Bangalore, Hyderabad, Guwahati, and Kolkata. We connect patients with the country's leading super-specialty hospitals (Medanta, Fortis, Max, Apollo, AIIMS) via emergency medical flights.</p>
                    
                    <h4 class="mt-4 text-dark">Comprehensive Patient Shifting in India</h4>
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Wide Fleet Availability:</strong> Private turbo-props for shorter domestic runways and heavy jets for long-haul international flights.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Critical Care Doctors:</strong> Intensive care specialists and anesthesiologists onboard every flight.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Organ Transport:</strong> Rapid logistics for time-critical organ transplant transfers.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Cost-Effective Options:</strong> Offering custom flight stretcher solutions on scheduled domestic airlines.</li>
                    </ul>

                    <h4 class="mt-4 text-dark">Domestic & International Approvals</h4>
                    <p>Our operations team handles all DGCA compliance approvals, landing rights at defense airports, and ground coordination with local authorities to ensure zero delay in emergency situations.</p>
                </div>
                {quote_form}
            </div>
        """
    },
    {
        "filename": "countries/air-ambulance-cost-dubai.html",
        "title": "Air Ambulance Cost in Dubai | Transparent Pricing - Air Medical 24X7",
        "description": "Get transparent air ambulance cost details in Dubai. Free, detailed quotations in 30 minutes with zero hidden charges. Competitive worldwide rates.",
        "keywords": "air ambulance cost dubai, air ambulance price dubai, medical flight cost dubai, how much is air ambulance dubai",
        "canonical": "https://airmedical24x7.com/air-ambulance-cost-dubai",
        "is_country": True,
        "hero_title": "Air Ambulance Cost Dubai",
        "hero_desc": "Transparent pricing for private air ambulance charters and medical escorts.",
        "image": "img/uae-country.jpg",
        "h1": "Air Ambulance Cost & Price Breakdown in Dubai",
        "intro": "Understanding the cost of medical flights is vital during stressful times. Air Medical 24X7 guarantees transparent, detailed quotes in 30 minutes with absolutely no hidden charges, giving you competitive global rates from Dubai.",
        "content_html": """
            <div class="row g-5 align-items-start">
                <div class="col-lg-7">
                    <h2 class="mb-4 text-primary">How We Calculate Air Ambulance Prices</h2>
                    <p>The cost of an air ambulance is customized for each patient. We focus on providing the most clinical safety at the lowest possible operational expense. Key price factors include:</p>
                    
                    <table class="table table-bordered my-4">
                        <thead class="bg-primary text-white">
                            <tr>
                                <th>Cost Factor</th>
                                <th>What It Includes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Flight Distance</strong></td>
                                <td>Fuel, routing permits, and landing fees across borders.</td>
                            </tr>
                            <tr>
                                <td><strong>Aircraft Type</strong></td>
                                <td>Turbo-props vs. light jets or long-range heavy aircraft.</td>
                            </tr>
                            <tr>
                                <td><strong>Medical Equipment</strong></td>
                                <td>Advanced ventilators, pediatric incubators, or ECMO equipment.</td>
                            </tr>
                            <tr>
                                <td><strong>Clinical Staff</strong></td>
                                <td>Specific doctors (e.g. cardiologists, neonatologists) matching patient needs.</td>
                            </tr>
                        </tbody>
                    </table>
                    
                    <h4 class="mt-4 text-dark">Alternative Budget-Friendly Options</h4>
                    <p>If a private air ambulance charter is outside your budget, we can configure a <strong>commercial airline medical stretcher</strong> or arrange a <strong>flight medical escort</strong>. This offers similar clinical safety at a fraction of the charter cost.</p>
                </div>
                {quote_form}
            </div>
        """
    },
    {
        "filename": "countries/air-ambulance-to-india.html",
        "title": "Air Ambulance from Dubai to India | Patient Transfer - Air Medical 24X7",
        "description": "Emergency air ambulance service from Dubai to India. ICU medical flights, commercial stretchers, and bed-to-bed transfers with doctors onboard.",
        "keywords": "air ambulance dubai to india, patient transfer dubai to india, medical flight dubai to india, repatriation dubai to india",
        "canonical": "https://airmedical24x7.com/air-ambulance-to-india",
        "is_country": True,
        "hero_title": "Air Ambulance Dubai to India",
        "hero_desc": "Prompt bed-to-bed patient transfers and repatriation from UAE to India.",
        "image": "img/uae-country.jpg",
        "h1": "Emergency Air Ambulance from Dubai to India",
        "intro": "The Dubai-India route is one of our most active corridors. Air Medical 24X7 provides specialized ICU air charter flights and commercial stretcher medical escorts from Dubai to any city in India.",
        "content_html": """
            <div class="row g-5 align-items-start">
                <div class="col-lg-7">
                    <h2 class="mb-4 text-primary">Seamless Patient Transfers from Dubai to India</h2>
                    <p>Whether repatriating a loved one back home or seeking specialized medical treatment, we manage the entire transfer process. From bed-to-bed ground coordination in Dubai to hospital admission in Delhi, Mumbai, Hyderabad, Bangalore, Cochin, or Chennai, we ensure continuous clinical support.</p>
                    
                    <h4 class="mt-4 text-dark">Consular Help & Logistics</h4>
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Consular coordination:</strong> Fast-track Medical Visas (M-Visa) and Indian Embassy clearances.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Medical Crew:</strong> Doctors and nursing staff fluent in Arabic, Hindi, and Malayalam.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Commercial Options:</strong> Coordinating flat stretchers on scheduled flights with major airlines.</li>
                    </ul>
                </div>
                {quote_form}
            </div>
        """
    },

    # --- ROOT DIRECTORY ---
    {
        "filename": "medical-escort-dubai.html",
        "title": "Flight Medical Escort Dubai | Commercial Flight Doctor - Air Medical 24X7",
        "description": "Professional medical escort services in Dubai. Certified flight doctors and nurses accompanying patients on commercial airlines for safe, cost-effective travel.",
        "keywords": "medical escort dubai, flight doctor dubai, flight nurse dubai, patient flight escort dubai, commercial medical escort",
        "canonical": "https://airmedical24x7.com/medical-escort-dubai",
        "is_country": False,
        "hero_title": "Flight Medical Escort Dubai",
        "hero_desc": "ICU-trained doctors and flight nurses accompanying patients on commercial airlines.",
        "image": "img/flight-medical-escort-services.jpg",
        "h1": "Professional Flight Medical Escorts in Dubai",
        "intro": "If a patient is stable enough to travel on a commercial flight but needs medical monitoring, our Flight Medical Escort service in Dubai is the ideal, cost-effective alternative to a private air charter.",
        "content_html": """
            <div class="row g-5 align-items-start">
                <div class="col-lg-7">
                    <h2 class="mb-4 text-primary">Expert Flight Medics on Commercial Flights</h2>
                    <p>Our medical escort team consists of ICU-trained doctors and flight nurses who accompany the patient on commercial airlines (Emirates, flydubai, Etihad, etc.). They monitor vitals, manage oxygen therapy, administer medications, and coordinate airport boarding logistics.</p>
                    
                    <h4 class="mt-4 text-dark">What Our Medical Escort Service Includes:</h4>
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Comprehensive Medical Review:</strong> A fit-to-fly assessment by our clinical director prior to booking.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Airline Clearance:</strong> We submit the MEDIF (Medical Information Form) and coordinate directly with airline medical boards.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>In-Flight Clinical Care:</strong> Patient monitoring, medication administration, and emergency response capabilities.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Logistical Support:</strong> Handling ticketing, security clearance, airport lounges, and priority boarding.</li>
                    </ul>
                </div>
                {quote_form}
            </div>
        """
    },
    {
        "filename": "commercial-stretcher-service.html",
        "title": "Commercial Flight Stretcher Service | Patient Transfer - Air Medical 24X7",
        "description": "Affordable commercial flight stretcher services for patients requiring flat travel. Medical clearances, airline coordination, and ICU escort onboard.",
        "keywords": "commercial flight stretcher, airline stretcher service, patient flight stretcher, commercial stretcher medical escort",
        "canonical": "https://airmedical24x7.com/commercial-stretcher-service",
        "is_country": False,
        "hero_title": "Commercial Flight Stretcher Service",
        "hero_desc": "FAA-approved flight stretcher systems with full medical teams on scheduled flights.",
        "image": "img/commercial-airlines-medical-transfer-services.jpg",
        "h1": "Commercial Airline Stretcher Service for Patients",
        "intro": "For patients who cannot sit upright and must remain flat during transport, we arrange commercial airline stretcher systems. This allows for ICU-level bed-to-bed care on international routes at a reduced cost.",
        "content_html": """
            <div class="row g-5 align-items-start">
                <div class="col-lg-7">
                    <h2 class="mb-4 text-primary">ICU Patient Transfers via Scheduled Flights</h2>
                    <p>By removing a block of seats on a commercial passenger flight and installing an FAA-approved stretcher system with a privacy curtain, we create a specialized clinical environment. A dedicated flight doctor and nurse accompany the patient to provide continuous care.</p>
                    
                    <h4 class="mt-4 text-dark">Process & Coordination:</h4>
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Airline Liaison:</strong> Stretchers require booking multiple passenger seats, requiring 48 to 72 hours for airline clearance.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Onboard ICU Setup:</strong> Portable oxygen, patient monitoring, and standard critical care medications.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Ground Transportation:</strong> Coordinated ICU ground ambulances at both departure and destination airports.</li>
                    </ul>
                </div>
                {quote_form}
            </div>
        """
    },
    {
        "filename": "ecmo-air-transfer.html",
        "title": "ECMO Air Transport | Critical Care Lung-Heart Flight - Air Medical 24X7",
        "description": "Specialized ECMO air ambulance transfer for critically ill patients. ICU aircraft equipped with ECMO machines, perfusionists, and cardiac doctors.",
        "keywords": "ecmo air ambulance, ecmo patient transfer, ecmo medical flight, critical care ecmo transport, heart lung support flight",
        "canonical": "https://airmedical24x7.com/ecmo-air-transfer",
        "is_country": False,
        "hero_title": "ECMO Air Transport",
        "hero_desc": "Specialized cardiorespiratory support and life-safety flights with onboard perfusionists.",
        "image": "img/ECMO.jpg",
        "h1": "Critical Care ECMO Air Ambulance Transfers",
        "intro": "Extracorporeal Membrane Oxygenation (ECMO) transfers are the most complex medical flights. Air Medical 24X7 is equipped with specialized systems to safely transport heart and lung failure patients globally.",
        "content_html": """
            <div class="row g-5 align-items-start">
                <div class="col-lg-7">
                    <h2 class="mb-4 text-primary">Life-Support Air Ambulance Missions</h2>
                    <p>ECMO acts as an external heart and lung system, taking over the patient's cardiorespiratory function. Operating this equipment in-flight requires advanced aviation medicine protocols, specialized power supply systems, and highly trained clinical crews.</p>
                    
                    <h4 class="mt-4 text-dark">Our specialized ECMO setups feature:</h4>
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Dedicated Critical Care Team:</strong> Flights are staffed by a flight cardiologist/intensivist, an ICU nurse, and a certified perfusionist.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Specialized Equipment:</strong> FAA-certified mountings for ECMO machines (Rotaflow, Cardiohelp) and continuous gas supplies.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Zero-Altitude Cabins:</strong> Pressure-regulated cabins designed to avoid gas expansion risks during ascent.</li>
                    </ul>
                </div>
                {quote_form}
            </div>
        """
    },
    {
        "filename": "repatriation-services-dubai.html",
        "title": "Medical Repatriation Services Dubai | Global Patient Transfer - Air Medical 24X7",
        "description": "Worldwide medical repatriation from Dubai. Secure, bed-to-bed patient transfer, commercial stretcher, and air ambulance with medical escort.",
        "keywords": "medical repatriation dubai, patient repatriation dubai, emergency repatriation dubai, global repatriation dubai",
        "canonical": "https://airmedical24x7.com/repatriation-services-dubai",
        "is_country": False,
        "hero_title": "Medical Repatriation Services Dubai",
        "hero_desc": "Consular assistance, embassy clearances, and global bed-to-bed medical repatriation.",
        "image": "img/uae-country.jpg",
        "h1": "Worldwide Medical Repatriation Services from Dubai",
        "intro": "For tourists, expatriates, and corporate travelers who fall ill in Dubai, returning to their home country for treatment is often the best choice. Air Medical 24X7 coordinates complete medical repatriation.",
        "content_html": """
            <div class="row g-5 align-items-start">
                <div class="col-lg-7">
                    <h2 class="mb-4 text-primary">Bringing Loved Ones Home Safely</h2>
                    <p>We work closely with major travel insurance providers, corporate assistance programs, international embassies, and family members to manage all logistical aspects of returning a patient home safely.</p>
                    
                    <h4 class="mt-4 text-dark">Our Repatriation Capabilities:</h4>
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Embassy & Customs Clearances:</strong> Coordination of visa paperwork, border control approvals, and medical declarations.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Flexible Transport Modes:</strong> Private ICU air ambulances or scheduled airline stretchers depending on patient stability.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Hospital Handover:</strong> Managing direct transfers from local Dubai clinics to the receiving facility in the patient's home country.</li>
                    </ul>
                </div>
                {quote_form}
            </div>
        """
    },
    {
        "filename": "medical-tourism-india.html",
        "title": "Medical Tourism in India | Hospital Treatment - Air Medical 24X7",
        "description": "Coordinated medical tourism services in India. Hospital bookings, medical visas, flight escorts, and complete patient travel assistance to top Indian hospitals.",
        "keywords": "medical tourism india, medical travel india, treatment in india, hospital admission india, medical visa india",
        "canonical": "https://airmedical24x7.com/medical-tourism-india",
        "is_country": False,
        "hero_title": "Medical Tourism in India",
        "hero_desc": "End-to-end treatment travel care packages, visas, and appointments at top hospitals.",
        "image": "img/medical-tourism.png",
        "h1": "Comprehensive Medical Tourism Services in India",
        "intro": "India is a leading global hub for high-quality, affordable healthcare. Air Medical 24X7 provides end-to-end patient travel assistance, connecting international patients with top hospitals in India.",
        "content_html": """
            <div class="row g-5 align-items-start">
                <div class="col-lg-7">
                    <h2 class="mb-4 text-primary">Accessing World-Class Treatment in India</h2>
                    <p>From cardiac bypass surgeries and complex oncology protocols to organ transplants and orthopedic care, Indian super-specialty hospitals offer medical excellence at a fraction of Western costs. We guide you through every step of this journey.</p>
                    
                    <h4 class="mt-4 text-dark">Complete Travel Care Package:</h4>
                    <ul class="list-unstyled">
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Hospital Appointments:</strong> Liaison with accredited institutions (Fortis, Max, Medanta, Apollo).</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Medical Visa Support:</strong> Fast processing of official Indian Medical Visas (M-Visa) for patients and companions.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Escorted Flight Travel:</strong> Flight nurse or doctor accompaniment for senior citizens or physically challenged patients.</li>
                        <li class="mb-2"><i class="fas fa-check text-red me-2"></i> <strong>Local Logistics:</strong> Ground ambulance transfers, hotel bookings, and multilingual translation support in India.</li>
                    </ul>
                </div>
                {quote_form}
            </div>
        """
    }
]

# Process and write files
for page in pages:
    file_path = os.path.join(root_dir, page["filename"])
    
    # 1. Select correct header/footer templates and quote forms
    if page["is_country"]:
        header = replace_metadata(countries_header, page["title"], page["description"], page["keywords"], page["canonical"])
        footer = countries_footer
        quote_form = countries_quote_form
        scripts = countries_scripts
        hero_bg_style = "background: linear-gradient(rgba(26, 52, 107, 0.85), rgba(26, 52, 107, 0.85)), url('../img/hero-bg.jpg') no-repeat center center; background-size: cover;"
        img_src = "../" + page["image"]
    else:
        header = replace_metadata(root_header, page["title"], page["description"], page["keywords"], page["canonical"])
        footer = root_footer
        quote_form = root_quote_form
        scripts = root_scripts
        hero_bg_style = "background: linear-gradient(rgba(26, 52, 107, 0.85), rgba(26, 52, 107, 0.85)), url('img/hero-bg.jpg') no-repeat center center; background-size: cover;"
        img_src = page["image"]
        
    # 2. Build the body section
    intro_hero_title = page["hero_title"]
    intro_text = page["hero_desc"]
    
    # Insert custom header overview about section template
    about_section = f"""
    <!-- About Start -->
    <div class="container-fluid py-5">
        <div class="container">
            <div class="row gx-5">
                <div class="col-lg-5 mb-5 mb-lg-0" style="min-height: 500px;">
                    <div class="position-relative h-100">
                        <img class="position-absolute w-100 h-100 rounded" src="{img_src}"
                            alt="{page["h1"]}" style="object-fit: cover;">
                    </div>
                </div>
                <div class="col-lg-7">
                    <div class="mb-4">
                        <h3 class="d-inline-block text-primary text-uppercase border-bottom border-5">About Our Service</h3>
                        <h2 class="about-heading">{page["h1"]}</h2>
                    </div>
                    <p class="fs-5">{page["intro"]}</p>
                    <div class="row g-3 pt-3">
                        <div class="col-sm-3 col-6">
                            <div class="premium-card text-center py-4">
                                <i class="fa fa-3x fa-user-md premium-icon mb-3"></i>
                                <h6 class="mb-0">Expert<small class="d-block text-primary">Medical Escort</small></h6>
                            </div>
                        </div>
                        <div class="col-sm-3 col-6">
                            <div class="premium-card text-center py-4">
                                <i class="fa fa-3x fa-plane premium-icon mb-3"></i>
                                <h6 class="mb-0">Emergency<small class="d-block text-primary">Services</small></h6>
                            </div>
                        </div>
                        <div class="col-sm-3 col-6">
                            <div class="premium-card text-center py-4">
                                <i class="fas fa-clock fa-3x premium-icon mb-3"></i>
                                <h6 class="mb-0">24X7<small class="d-block text-primary">Support</small></h6>
                            </div>
                        </div>
                        <div class="col-sm-3 col-6">
                            <div class="premium-card text-center py-4">
                                <i class="fas fa-globe fa-3x premium-icon mb-3"></i>
                                <h6 class="mb-0">Global<small class="d-block text-primary">Service</small></h6>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- About End -->
    """
    
    # Insert custom hero section into middle block
    content_html = page["content_html"].format(quote_form=quote_form)
    
    middle_html = f"""
    <!-- Hero Start -->
    <div class="container-fluid bg-primary py-5 mb-5 hero-header" style="{hero_bg_style}">
        <div class="container py-5">
            <div class="row justify-content-start">
                <div class="col-lg-9 text-center text-lg-start">
                    <h1 class="display-3 text-white mb-3 fw-bold">{intro_hero_title}</h1>
                    <p class="text-white fs-5">{intro_text}</p>
                    <div class="pt-3">
                        <a href="tel:+971565542001" class="btn btn-request me-3 py-3 px-4"><i class="fas fa-phone-alt me-2"></i> Call emergency desk</a>
                        <a href="https://wa.me/971565542001" target="_blank" class="btn btn-ghost py-3 px-4"><i class="fab fa-whatsapp me-2"></i> WhatsApp Quote</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Hero End -->

    {about_section}

    <!-- Main Content Section Start -->
    <div class="container-fluid py-5">
        <div class="container">
            {content_html}
        </div>
    </div>
    <!-- Main Content Section End -->
    """
    
    # Append the scripts block to the bottom of the footer (before </body>)
    # The footer ends with </body>\n</html>. Since it already has the mobile sticky CTA, we only append scripts
    modified_footer = footer.replace("</body>", f"{scripts}\n</body>")
    
    # Assemble complete page
    full_html = header + middle_html + modified_footer
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w", encoding="utf-8") as out_f:
        out_f.write(full_html)
        
    print(f"Generated page: {page['filename']}")
