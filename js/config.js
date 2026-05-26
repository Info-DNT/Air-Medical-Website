// Air Medical 24X7 - Supabase Configuration
const supabaseUrl = "https://dtiirdimtbmkvryvqten.supabase.co/";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDQ0MzksImV4cCI6MjA5MTcyMDQzOX0.MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI";

// Initialize the Supabase client for lead capture
window.supabaseClient = supabase.createClient(supabaseUrl, supabaseKey);

// Initialize a separate Supabase client for blogs & comments (stored in original project)
const blogsSupabaseUrl = "https://eiqpvuciihwmuznbsyob.supabase.co/";
const blogsSupabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVpcXB2dWNpaWh3bXV6bmJzeW9iIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU2MDY1MDcsImV4cCI6MjA4MTE4MjUwN30.fY2QZkNa1nUB1UQxmV8r97WTpB32ocIiVXaHo1coB-c";
window.blogsSupabaseClient = supabase.createClient(blogsSupabaseUrl, blogsSupabaseKey);

// Cloudflare Turnstile Configuration
const turnstileSiteKey = "0x4AAAAAADTA3gG7SVL4awln";

// Automatically inject and handle Cloudflare Turnstile Captcha
document.addEventListener("DOMContentLoaded", () => {
  const forms = [
    document.getElementById("quoteForm"),
    document.getElementById("quoteFormPopup"),
    document.getElementById("careerForm")
  ].filter(Boolean);

  if (forms.length === 0) return;

  // 1. Inject the Turnstile container widget in the forms
  forms.forEach(form => {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (!submitBtn) return;

    // Create container wrapper
    const container = document.createElement("div");
    container.className = "cf-turnstile my-3";
    container.setAttribute("data-sitekey", turnstileSiteKey);
    container.style.display = "flex";
    container.style.justifyContent = "center";
    container.style.marginBottom = "15px";

    // Insert directly before the submit button
    submitBtn.parentNode.insertBefore(container, submitBtn);
  });

  // 2. Load the Turnstile API script dynamically
  const script = document.createElement("script");
  script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js";
  script.async = true;
  script.defer = true;
  document.head.appendChild(script);

  // 3. Intercept form submissions to validate Captcha status and route to Edge Function
  forms.forEach(form => {
    form.addEventListener("submit", async function (e) {
      if (typeof turnstile === "undefined") {
        e.preventDefault();
        e.stopImmediatePropagation();
        alert("Captcha is still loading. Please wait a moment.");
        return;
      }

      const response = turnstile.getResponse();
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

          // Include optional transport selection if exists
          const transportInput = form.querySelector('input[name="transport"]:checked');
          if (transportInput) {
            payload.transport = transportInput.value;
          }

          const res = await fetch(
            'https://dtiirdimtbmkvryvqten.supabase.co/functions/v1/submit-main-page',
            {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            }
          );

          const result = await res.json();

          if (result.success) {
            alert("✅ Thank you! Our team will contact you soon.");
            form.reset();
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
          if (window.turnstile) {
            window.turnstile.reset();
          }
        }
      }
    }, true); // Use capture phase so this check runs before standard form handlers
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

