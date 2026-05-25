// Air Medical 24X7 - Supabase Configuration
const supabaseUrl = "https://dtiirdimtbmkvryvqten.supabase.co/";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImR0aWlyZGltdGJta3ZyeXZxdGVuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNDQ0MzksImV4cCI6MjA5MTcyMDQzOX0.MwOkE8tsM2itUhTxNJDDHPPPAxImjRS9Ch1ACWzdTmI";

// Initialize the Supabase client
window.supabaseClient = supabase.createClient(supabaseUrl, supabaseKey);

// Cloudflare Turnstile Configuration
const turnstileSiteKey = "0x4AAAAAADTA3gG7SVL4awln";

// Automatically inject and handle Cloudflare Turnstile Captcha
document.addEventListener("DOMContentLoaded", () => {
  const forms = [
    document.getElementById("quoteForm"),
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

  // 3. Intercept form submissions to validate Captcha status
  forms.forEach(form => {
    form.addEventListener("submit", function (e) {
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
    }, true); // Use capture phase so this check runs before the main form submission scripts
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

