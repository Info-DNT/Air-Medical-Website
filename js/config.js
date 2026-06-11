// Air Medical 24X7 - Supabase Configuration
const supabaseUrl = "https://dtiirdimtbmkvryvqten.supabase.co/";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDQ0MzksImV4cCI6MjA5MTcyMDQzOX0.MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI";

// Initialize the Supabase client for lead capture
window.supabaseClient = supabase.createClient(supabaseUrl, supabaseKey);

// Initialize a separate Supabase client for blogs & comments (stored in original project)
const blogsSupabaseUrl = "https://dtiirdimtbmkvryvqten.supabase.co/";
const blogsSupabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDQ0MzksImV4cCI6MjA5MTcyMDQzOX0.MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI";
window.blogsSupabaseClient = supabase.createClient(blogsSupabaseUrl, blogsSupabaseKey);

// Automatically inject and handle Cloudflare Turnstile Captcha
const turnstileSiteKey = "0x4AAAAAADTA3gG7SVL4awln";

// Map to store widget IDs for each form
const turnstileWidgets = new Map();

// Global callback for Turnstile explicit rendering
window.onloadTurnstileCallback = function () {
  const forms = [
    document.getElementById("quoteForm"),
    document.getElementById("quoteFormPopup"),
    document.getElementById("careerForm")
  ].filter(Boolean);

  // Dynamic sitekey selection for local environment bypass
  const activeSiteKey = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") 
    ? "1x00000000000000000000AA" 
    : turnstileSiteKey;

  forms.forEach(form => {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (!submitBtn) return;

    // Create a container placeholder
    const container = document.createElement("div");
    container.className = "cf-turnstile-container my-3";
    container.style.display = "flex";
    container.style.justifyContent = "center";
    container.style.marginBottom = "15px";

    // Insert directly before the submit button
    submitBtn.parentNode.insertBefore(container, submitBtn);

    try {
      // Explicitly render Turnstile widget using activeSiteKey
      const widgetId = turnstile.render(container, {
        sitekey: activeSiteKey,
        theme: "light",
        callback: function (token) {
          console.log(`[Turnstile] Challenge solved for ${form.id}`);
        },
        "error-callback": function (code) {
          console.error(`[Turnstile] Error in form ${form.id}:`, code);
        },
        "expired-callback": function () {
          console.warn(`[Turnstile] Token expired for ${form.id}, resetting...`);
          turnstile.reset(widgetId);
        }
      });

      // Keep track of the widget ID for this form
      turnstileWidgets.set(form, widgetId);
    } catch (err) {
      console.error("[Turnstile] Render failed:", err);
    }
  });
};

document.addEventListener("DOMContentLoaded", () => {
  const forms = [
    document.getElementById("quoteForm"),
    document.getElementById("quoteFormPopup"),
    document.getElementById("careerForm")
  ].filter(Boolean);

  if (forms.length === 0) return;

  // Load the Turnstile API script dynamically specifying explicit rendering callback
  const script = document.createElement("script");
  script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?onload=onloadTurnstileCallback&render=explicit";
  script.async = true;
  script.defer = true;
  document.head.appendChild(script);

  // Intercept form submissions
  forms.forEach(form => {
    form.addEventListener("submit", async function (e) {
      // Route quotation forms to secure Edge Function instead of direct DB insertion
      if (form.id === "quoteForm" || form.id === "quoteFormPopup") {
        e.preventDefault();
        e.stopImmediatePropagation();

        const btn = form.querySelector('button[type="submit"]');
        if (btn) {
          btn.disabled = true;
          btn.setAttribute("data-orig-text", btn.textContent);
          btn.textContent = "Submitting...";
        }

        // Fetch Turnstile response, with fallback if Turnstile fails to load
        let response = "";
        let widgetId = null;
        if (typeof turnstile !== "undefined") {
          widgetId = turnstileWidgets.get(form);
          response = widgetId ? turnstile.getResponse(widgetId) : turnstile.getResponse();
        }

        // If no token, check if we are on localhost (bypass it) or prod (alert)
        const isLocal = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";
        if (!response && !isLocal) {
          alert("Please complete the Cloudflare Turnstile verification.");
          if (btn) {
            btn.disabled = false;
            btn.textContent = btn.getAttribute("data-orig-text") || "Get a Free Quotation";
          }
          return;
        }

        try {
          const isPopup = form.id === "quoteFormPopup";
          const nameId = isPopup ? "popupName" : "name";
          const emailId = isPopup ? "popupEmail" : "email";
          const codeId = isPopup ? "popupCountryCode" : "countryCode";
          const phoneId = isPopup ? "popupPhone" : "phone";
          const serviceId = isPopup ? "popupService" : "service";

          const codeVal = document.getElementById(codeId)?.value || "";
          const phoneVal = document.getElementById(phoneId)?.value || "";
          // Send empty full_phone if phone number itself is empty
          const fullPhone = phoneVal ? (codeVal + phoneVal) : "";

          // Combine transport radio option and service dropdown value
          const transportInput = form.querySelector('input[name="transport"]:checked');
          let serviceVal = document.getElementById(serviceId)?.value || "";
          
          if (transportInput) {
            if (serviceVal) {
              serviceVal = `${transportInput.value} (${serviceVal})`;
            } else {
              serviceVal = transportInput.value;
            }
          }

          const payload = {
            name: document.getElementById(nameId)?.value || "",
            email: document.getElementById(emailId)?.value || "",
            full_phone: fullPhone,
            service: serviceVal,
            token: response
          };

          // Capture new patient location and destination fields
          const patientLocEl = form.querySelector('[name="patientLocation"]') || document.getElementById("patientLocation");
          const destEl = form.querySelector('[name="destination"]') || document.getElementById("destination");

          if (patientLocEl) {
            payload.patient_location = patientLocEl.value;
          }
          if (destEl) {
            payload.destination = destEl.value;
          }

          // Also keep transport inside payload if backend requires it
          if (transportInput) {
            payload.transport = transportInput.value;
          }

          const res = await fetch(
            'https://dtiirdimtbmkvryvqten.supabase.co/functions/v1/submit-main-page',
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${supabaseKey}`,
                'apikey': supabaseKey
              },
              body: JSON.stringify(payload)
            }
          );

          const result = await res.json();

          if (result.success) {
            alert("✅ Thank you! Our team will contact you soon.");
            form.reset();
            if (btn) {
              btn.disabled = false;
              btn.textContent = btn.getAttribute("data-orig-text") || "Get a Free Quotation";
            }
            if (isPopup && typeof window.closeQuoteModal === "function") {
              window.closeQuoteModal();
            }
          } else {
            alert("Error: " + (result.error || "Submission failed."));
            if (btn) {
              btn.disabled = false;
              btn.textContent = btn.getAttribute("data-orig-text") || "Get a Free Quotation";
            }
          }
        } catch (err) {
          console.error("Submission error:", err);
          alert("Something went wrong. Please try again.");
          if (btn) {
            btn.disabled = false;
            btn.textContent = btn.getAttribute("data-orig-text") || "Get a Free Quotation";
          }
        } finally {
          if (typeof turnstile !== "undefined" && widgetId) {
            turnstile.reset(widgetId);
          } else if (window.turnstile) {
            window.turnstile.reset();
          }
        }
      }
    }, true);
  });
});

// Sanitizer function to ensure "24X7" casing everywhere client-side
window.sanitize24X7 = function (text) {
  if (!text || typeof text !== "string") return text;
  try {
    const regex = new RegExp("(?<!airmedical)(?<!airmedical-)(?<!airmedical_)(24/7|24[xX]7)", "gi");
    return text.replace(regex, "24X7");
  } catch (e) {
    // Fallback if lookbehind is not supported: placeholder airmedical domains, replace, then restore
    let temp = text;
    const placeholders = [];
    temp = temp.replace(/airmedical[-_]?24[xX]7/gi, (match) => {
      placeholders.push(match);
      return `__AIRMED_PLACEHOLDER_${placeholders.length - 1}__`;
    });
    temp = temp.replace(/(24\/7|24[xX]7)/gi, "24X7");
    temp = temp.replace(/__AIRMED_PLACEHOLDER_(\d+)__/g, (match, idx) => {
      return placeholders[parseInt(idx)];
    });
    return temp;
  }
};

// Admin Configuration for Blog Editor
window.BLOGS_ADMIN_CONFIG = {
  username: "Nitin@admin@24X7@",
  // SHA-256 hash of "@admin@24X7@Global@" (lowercase sha256 hex)
  passwordHash: "a2bf3a92c6e4c20febc5b11f542fd5af1e10997dd65f29a4ea4627cb7642d39b",
  // Optional: Paste your Supabase Service Role Key here to bypass database RLS write restrictions
  serviceRoleKey: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NjE0NDQzOSwiZXhwIjoyMDkxNzIwNDM5fQ.NCnB3zI0ESnhCzM19y1UOlu7Qn07Lm3LujSbAh2IzZU"
};

// Rebind blogsSupabaseClient with custom/service key if provided
window.rebindBlogsSupabaseClient = function (serviceKey) {
  if (serviceKey) {
    window.blogsSupabaseClient = supabase.createClient(blogsSupabaseUrl, serviceKey);
  } else {
    window.blogsSupabaseClient = supabase.createClient(blogsSupabaseUrl, blogsSupabaseKey);
  }
};

