// Air Medical 24X7 - Supabase Configuration
const supabaseUrl = "https://dtiirdimtbmkvryvqten.supabase.co/";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDQ0MzksImV4cCI6MjA5MTcyMDQzOX0.MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI";

// Initialize the Supabase client for lead capture
window.supabaseClient = supabase.createClient(supabaseUrl, supabaseKey);

// Initialize a separate Supabase client for blogs & comments (stored in original project)
const blogsSupabaseUrl = "https://eiqpvuciihwmuznbsyob.supabase.co/";
const blogsSupabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c";
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

  const activeSiteKey = turnstileSiteKey;

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
      // Explicitly render Turnstile widget
      const widgetId = turnstile.render(container, {
        sitekey: turnstileSiteKey,
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
      if (typeof turnstile === "undefined") {
        e.preventDefault();
        e.stopImmediatePropagation();
        alert("Captcha is still loading. Please wait a moment.");
        return;
      }

      const widgetId = turnstileWidgets.get(form);
      const response = widgetId ? turnstile.getResponse(widgetId) : turnstile.getResponse();

      if (!response) {
        e.preventDefault();
        e.stopImmediatePropagation();
        alert("Please complete the Cloudflare Turnstile verification.");
        return;
      }

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

        try {
          const isPopup = form.id === "quoteFormPopup";
          const nameId = isPopup ? "popupName" : "name";
          const emailId = isPopup ? "popupEmail" : "email";
          const codeId = isPopup ? "popupCountryCode" : "countryCode";
          const phoneId = isPopup ? "popupPhone" : "phone";
          const serviceId = isPopup ? "popupService" : "service";

          const codeVal = document.getElementById(codeId)?.value || "";
          const phoneVal = document.getElementById(phoneId)?.value || "";
          const fullPhone = codeVal + phoneVal;

          const payload = {
            name: document.getElementById(nameId)?.value || "",
            email: document.getElementById(emailId)?.value || "",
            full_phone: fullPhone,
            service: document.getElementById(serviceId)?.value || "",
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

          // Include optional transport selection if exists
          const transportInput = form.querySelector('input[name="transport"]:checked');
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
          if (widgetId) {
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
window.sanitize24X7 = function(text) {
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
